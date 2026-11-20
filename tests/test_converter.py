"""Offline tests for the converter CLI and FreecurrencyAPI client."""

import errno
import json
import os
import runpy
import select
import subprocess
import sys
import time
from collections.abc import Sequence
from pathlib import Path
from unittest.mock import Mock

import pytest
import requests

from currency_converter.api_service import (
    CurrencyAPIError,
    fetch_currency_rates,
    get_all_currencies,
    get_currency_codes,
)
from currency_converter.main import start_converter

PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def offline(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")
    monkeypatch.setenv("API_TOKEN", "test-token")
    monkeypatch.setenv("API_URL", "https://example.invalid/v1/")
    monkeypatch.setattr(
        requests.sessions.Session,
        "send",
        Mock(side_effect=AssertionError("Unexpected HTTP request")),
    )


def make_response(body: str, status: int = 200) -> requests.Response:
    response = requests.Response()
    response.status_code = status
    response.encoding = "utf-8"
    response._content = body.encode()
    return response


def test_conversion(monkeypatch: pytest.MonkeyPatch) -> None:
    get = Mock(return_value=make_response('{"data":{"EUR":0.8,"GBP":0.5}}'))
    monkeypatch.setattr(requests, "get", get)

    assert fetch_currency_rates("USD", ["EUR", "GBP"], 2.3456) == pytest.approx(
        {"EUR": 1.8768, "GBP": 1.173}
    )
    get.assert_called_once_with(
        "https://example.invalid/v1/latest",
        params={
            "apikey": "test-token",
            "base_currency": "USD",
            "currencies": "EUR,GBP",
        },
        timeout=(4, 10),
        allow_redirects=False,
    )


@pytest.mark.parametrize("extra_rate", ["0.5", '"invalid"'])
def test_conversion_ignores_unrequested_rates(
    monkeypatch: pytest.MonkeyPatch, extra_rate: str
) -> None:
    response = make_response(f'{{"data":{{"EUR":0.8,"GBP":{extra_rate}}}}}')
    monkeypatch.setattr(requests, "get", Mock(return_value=response))

    assert fetch_currency_rates("USD", ["EUR"], 2.5) == {"EUR": 2.0}


def test_amount_that_rounds_to_zero_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    get = Mock()
    monkeypatch.setattr(requests, "get", get)

    with pytest.raises(ValueError, match="^amount_zero$"):
        fetch_currency_rates(amount=0.0001)
    get.assert_not_called()


@pytest.mark.parametrize("amount", [0, -1, float("nan"), float("inf"), True])
def test_invalid_amount(amount: float) -> None:
    with pytest.raises(ValueError, match="^amount_invalid$"):
        fetch_currency_rates(amount=amount)


@pytest.mark.parametrize(
    ("error", "message"),
    [
        (requests.Timeout("test-token"), "timeout"),
        (requests.ConnectionError("test-token"), "request_failed"),
    ],
)
def test_network_errors(
    monkeypatch: pytest.MonkeyPatch, error: requests.RequestException, message: str
) -> None:
    monkeypatch.setattr(requests, "get", Mock(side_effect=error))

    with pytest.raises(CurrencyAPIError, match=message) as failure:
        fetch_currency_rates()
    assert "test-token" not in str(failure.value)


@pytest.mark.parametrize(
    ("status", "body", "message"),
    [
        (302, "", "http_status"),
        (429, "<html>quota</html>", "http_status"),
        (200, "invalid JSON", "invalid_json"),
        (200, "[]", "invalid_response"),
        (200, '{"data":[]}', "invalid_response"),
        (200, '{"data":{}}', "invalid_response"),
        (200, '{"data":{"EUR":"0.9"}}', "invalid_rate"),
        (200, '{"data":{"EUR":true}}', "invalid_rate"),
        (200, '{"data":{"EUR":1e400}}', "invalid_rate"),
        (200, '{"data":{"GBP":0.9}}', "missing_rates"),
    ],
)
def test_bad_rates_response(
    monkeypatch: pytest.MonkeyPatch, status: int, body: str, message: str
) -> None:
    monkeypatch.setattr(requests, "get", Mock(return_value=make_response(body, status)))

    with pytest.raises(CurrencyAPIError, match=message) as failure:
        fetch_currency_rates(currencies=["EUR"])
    if status != 200:
        assert failure.value.details == {"status": status}


def mock_currency_list(
    monkeypatch: pytest.MonkeyPatch, *responses: requests.Response
) -> Mock:
    data = {
        "USD": {"name": "US Dollar"},
        "EUR": {"name": "Euro"},
        "GBP": {"name": "British Pound"},
    }
    get = Mock(side_effect=[make_response(json.dumps({"data": data})), *responses])
    monkeypatch.setattr(requests, "get", get)
    return get


def test_currency_metadata_keeps_extra_fields(monkeypatch: pytest.MonkeyPatch) -> None:
    data = {"USD": {"name": "US Dollar", "symbol": "$", "decimal_digits": 2}}
    response = make_response(json.dumps({"data": data}))
    monkeypatch.setattr(requests, "get", Mock(return_value=response))

    assert get_all_currencies() == data


def test_currency_codes(monkeypatch: pytest.MonkeyPatch) -> None:
    get = mock_currency_list(monkeypatch)
    assert get_currency_codes() == ["USD", "EUR", "GBP"]
    get.assert_called_once_with(
        "https://example.invalid/v1/currencies",
        params={"apikey": "test-token"},
        timeout=(4, 10),
        allow_redirects=False,
    )


@pytest.mark.parametrize(
    ("amount", "expected"),
    [("2.5", "2.5"), ("2.5004", "2.5"), ("2.4999", "2.5")],
)
@pytest.mark.parametrize(
    ("args", "welcome", "results", "prompt"),
    [
        ([], "Приветствуем", "Результаты конвертации", "Введите валюту"),
        (["--lang", "ru"], "Приветствуем", "Результаты конвертации", "Введите валюту"),
        (["--lang", "en"], "Welcome", "Conversion results", "Enter the currency"),
    ],
)
def test_cli_conversion(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    amount: str,
    expected: str,
    args: list[str],
    welcome: str,
    results: str,
    prompt: str,
) -> None:
    mock_currency_list(monkeypatch, make_response('{"data":{"EUR":0.8,"GBP":0.5}}'))
    user_input = Mock(side_effect=[" usd ", amount, " eur, gbp "])
    monkeypatch.setattr("builtins.input", user_input)
    monkeypatch.setattr(sys, "argv", ["index.py", *args])

    with pytest.raises(SystemExit) as exit_info:
        runpy.run_path(str(PROJECT_ROOT / "index.py"), run_name="__main__")

    assert exit_info.value.code == 0
    output = capsys.readouterr()
    assert welcome in output.out
    assert results in output.out
    assert prompt in user_input.call_args_list[0].args[0]
    assert "1. [USD] US Dollar" in output.out
    assert f"{expected} USD = 2.00 EUR" in output.out
    assert f"{expected} USD = 1.25 GBP" in output.out
    assert not output.err


def test_entry_point_returns_130_on_interrupt(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    mock_currency_list(monkeypatch)
    monkeypatch.setattr("builtins.input", Mock(side_effect=KeyboardInterrupt))
    monkeypatch.setattr(sys, "argv", ["index.py"])

    with pytest.raises(SystemExit) as exit_info:
        runpy.run_path(str(PROJECT_ROOT / "index.py"), run_name="__main__")

    assert exit_info.value.code == 130
    assert "Конвертация отменена." in capsys.readouterr().err


@pytest.mark.skipif(sys.platform != "linux", reason="requires Linux IUTF8")
def test_cli_backspace_erases_utf8_characters() -> None:
    import pty
    import termios

    script = """
import locale
import sys
from importlib.util import find_spec
from unittest.mock import patch

if find_spec("readline") is None or locale.getencoding() != "UTF-8":
    raise SystemExit(77)

import index

def capture(_prompt):
    raw = input("PTY input: ")
    print(f"PTY result: {ascii(raw)}")
    raise SystemExit(0)

currencies = {"RUB": {"name": "Ruble"}}
with (
    patch("currency_converter.main.get_all_currencies", return_value=currencies),
    patch("currency_converter.main.input", capture, create=True),
    patch("requests.sessions.Session.send", side_effect=AssertionError("HTTP called")),
):
    raise SystemExit(index.main(["--lang", "en"]))
"""
    try:
        master, slave = pty.openpty()
    except OSError as error:
        pytest.skip(f"PTY unavailable: {error}")

    with (
        os.fdopen(master, "rb", buffering=0) as terminal,
        os.fdopen(slave, "rb") as tty,
    ):
        attrs = termios.tcgetattr(tty)
        attrs[0] &= ~getattr(termios, "IUTF8", 0x4000)  # Linux IUTF8 on older Python
        attrs[6][termios.VERASE] = b"\x7f"
        termios.tcsetattr(tty, termios.TCSANOW, attrs)
        env = dict(os.environ, LC_ALL="C.UTF-8", TERM="dumb")
        env.update(INPUTRC=os.devnull, EDITRC=os.devnull)
        with subprocess.Popen(
            [sys.executable, "-c", script],
            cwd=PROJECT_ROOT,
            stdin=tty,
            stdout=tty,
            stderr=tty,
            env=env,
        ) as child:
            tty.close()
            try:
                output = b""
                prompt = b"PTY input: "
                sent = False
                deadline = time.monotonic() + 10
                while select.select(
                    [terminal], [], [], max(0, deadline - time.monotonic())
                )[0]:
                    try:
                        chunk = terminal.read(4096)
                    except OSError as error:
                        if error.errno != errno.EIO:  # Linux PTY hangup
                            raise
                        break
                    if not chunk:
                        break
                    output += chunk
                    if not sent and prompt in output:
                        os.write(master, "КГИ".encode() + b"\x7f" * 3 + b"RUB\n")
                        sent = True
                else:
                    pytest.fail(f"PTY timed out: {output!r}")
                child.wait(timeout=10)
            finally:
                if child.poll() is None:
                    child.kill()

    if child.returncode == 77:
        pytest.skip("requires readline and a UTF-8 locale")
    assert child.returncode == 0, output
    assert b"PTY result: 'RUB'\r\n" in output


@pytest.mark.parametrize(
    ("answers", "ru", "en"),
    [
        (["XXX"], "исходную валюту", "source currency"),
        (["USD", "текст"], "количество числом", "Enter a number"),
        (["USD", "0.0001"], "округляется до нуля", "rounds to zero"),
        (["USD", "NaN"], "положительным", "finite positive number"),
        (["USD", "1", "EUR, "], "через запятую", "separated by commas"),
        (["USD", "1", "XXX"], "через запятую", "separated by commas"),
    ],
)
@pytest.mark.parametrize("lang", ["ru", "en"])
def test_cli_invalid_input(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    answers: Sequence[str],
    ru: str,
    en: str,
    lang: str,
) -> None:
    get = mock_currency_list(monkeypatch)
    monkeypatch.setattr("builtins.input", Mock(side_effect=answers))

    assert start_converter(lang) == 1
    output = capsys.readouterr().err
    assert output.startswith("Ошибка:" if lang == "ru" else "Error:")
    assert (ru if lang == "ru" else en) in output
    assert get.call_count == 1


@pytest.mark.parametrize(
    ("status", "body", "ru", "en"),
    [
        (503, "", "HTTP 503", "HTTP 503"),
        (200, "invalid JSON", "некорректный JSON", "invalid JSON"),
        (
            200,
            '{"data":{"USD":{}}}',
            "некорректный список валют",
            "invalid currency list",
        ),
    ],
)
@pytest.mark.parametrize("lang", ["ru", "en"])
def test_cli_currency_list_failure(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    status: int,
    body: str,
    ru: str,
    en: str,
    lang: str,
) -> None:
    monkeypatch.setattr(requests, "get", Mock(return_value=make_response(body, status)))
    user_input = Mock()
    monkeypatch.setattr("builtins.input", user_input)

    assert start_converter(lang) == 1
    output = capsys.readouterr().err
    assert output.startswith("Ошибка:" if lang == "ru" else "Error:")
    assert (ru if lang == "ru" else en) in output
    user_input.assert_not_called()


def test_missing_token(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.delenv("API_TOKEN")

    assert start_converter() == 1
    assert "API_TOKEN" in capsys.readouterr().err


def test_import_has_no_side_effects(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("API_TOKEN")
    monkeypatch.delenv("API_URL")
    script = """
import sys
from unittest.mock import patch

original_path = sys.path[:]
original_readline = sys.modules.get("readline")
with (
    patch("dotenv.load_dotenv", side_effect=AssertionError("dotenv called")),
    patch("requests.sessions.Session.send", side_effect=AssertionError("HTTP called")),
    patch("builtins.input", side_effect=AssertionError("input called")),
):
    import index
    import currency_converter.api_service
    import currency_converter.main

assert sys.path == original_path
assert sys.modules.get("readline") is original_readline
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    assert not result.stdout
    assert not result.stderr


@pytest.mark.parametrize(
    ("args", "status", "message"),
    [
        (["--help"], 0, "Показать справку"),
        (["--lang", "en", "--help"], 0, "Show this help"),
        (["--lang", "de"], 2, "Для --lang укажите ru или en"),
        (["--lang"], 2, "Для --lang укажите ru или en"),
        (["--lang", "en", "--unknown"], 2, "Invalid arguments"),
        (["unexpected"], 2, "Некорректные аргументы"),
    ],
)
def test_cli_options_without_configuration(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    args: list[str],
    status: int,
    message: str,
) -> None:
    monkeypatch.delenv("API_TOKEN")
    monkeypatch.delenv("API_URL")
    monkeypatch.setattr(sys, "argv", ["index.py", *args])
    load_dotenv = Mock(side_effect=AssertionError("dotenv called"))
    monkeypatch.setattr("currency_converter.main.load_dotenv", load_dotenv)

    with pytest.raises(SystemExit) as exit_info:
        runpy.run_path(str(PROJECT_ROOT / "index.py"), run_name="__main__")

    assert exit_info.value.code == status
    output = capsys.readouterr()
    if status == 0:
        assert message in output.out
        assert not output.err
    else:
        assert message in output.err
        assert not output.out
    load_dotenv.assert_not_called()


@pytest.mark.parametrize(
    ("lang", "message"),
    [("ru", "время ожидания"), ("en", "request timed out")],
)
def test_cli_api_failure_hides_token(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    lang: str,
    message: str,
) -> None:
    monkeypatch.setattr(
        requests, "get", Mock(side_effect=requests.Timeout("test-token"))
    )

    assert start_converter(lang) == 1
    output = capsys.readouterr().err
    assert message in output
    assert "test-token" not in output


@pytest.mark.parametrize(
    ("lang", "exception", "status", "message"),
    [
        ("ru", EOFError, 1, "Ввод завершён"),
        ("en", EOFError, 1, "Input ended"),
        ("en", KeyboardInterrupt, 130, "Conversion cancelled"),
    ],
)
def test_cli_incomplete_input(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    lang: str,
    exception: type[BaseException],
    status: int,
    message: str,
) -> None:
    mock_currency_list(monkeypatch)
    monkeypatch.setattr("builtins.input", Mock(side_effect=exception))

    assert start_converter(lang) == status
    assert message in capsys.readouterr().err
