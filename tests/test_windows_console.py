"""Exercise the frozen Windows entry point and its conservative pause decision."""

import runpy
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from currency_converter import main as cli
from currency_converter import windows_console

INDEX = Path(__file__).resolve().parents[1] / "index.py"


@pytest.mark.parametrize(
    ("launcher", "expected"),
    [
        ("EXPLORER.EXE", True),
        ("powershell.exe", False),
        ("pwsh.exe", False),
        ("cmd.exe", False),
        ("WindowsTerminal.exe", False),
        ("python.exe", False),
        (None, False),
    ],
)
def test_onefile_launcher(launcher: str | None, expected: bool) -> None:
    processes = {30: (20, "converter.exe"), 20: (10, "Converter.exe")}
    if launcher is not None:
        # Explorer can also be the ancestor of a shell or other launcher.
        processes.update({10: (5, launcher), 5: (1, "explorer.exe")})
    assert windows_console._launched_by_explorer(processes, 30) is expected


@pytest.mark.parametrize("parent", [None, "explorer.exe", "python.exe"])
def test_requires_same_image_bootloader(parent: str | None) -> None:
    processes = {30: (20, "converter.exe"), 10: (5, "explorer.exe")}
    if parent is not None:
        processes[20] = (10, parent)
    assert not windows_console._launched_by_explorer(processes, 30)


@pytest.mark.parametrize(
    ("redirected", "tty", "expected"),
    [
        (None, True, True),
        (0, False, False),
        (1, False, False),
        (2, False, False),
        (1, True, False),  # Windows NUL may pass isatty() but has no console mode.
    ],
)
def test_requires_three_console_streams(
    monkeypatch: pytest.MonkeyPatch,
    redirected: int | None,
    tty: bool,
    expected: bool,
) -> None:
    for fd, name in enumerate(("stdin", "stdout", "stderr")):
        stream = Mock()
        stream.isatty.return_value = fd != redirected or tty
        stream.fileno.return_value = fd
        monkeypatch.setattr(sys, name, stream)
    monkeypatch.setitem(
        sys.modules, "msvcrt", SimpleNamespace(get_osfhandle=lambda fd: fd + 10)
    )

    def get_mode(handle: int, mode) -> bool:
        mode._obj.value = 0x0002  # ENABLE_LINE_INPUT
        return handle - 10 != redirected

    kernel32 = SimpleNamespace(GetConsoleMode=Mock(side_effect=get_mode))
    assert windows_console._has_console_streams(kernel32) is expected


@pytest.fixture
def explorer_console(monkeypatch: pytest.MonkeyPatch) -> Mock:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.setattr(windows_console.ctypes, "WinDLL", Mock(), raising=False)
    monkeypatch.setattr(
        windows_console, "_has_console_streams", Mock(return_value=True)
    )
    processes = {
        30: (20, "converter.exe"),
        20: (10, "converter.exe"),
        10: (5, "explorer.exe"),
    }
    monkeypatch.setattr(windows_console.os, "getpid", Mock(return_value=30))
    monkeypatch.setattr(
        windows_console, "_process_snapshot", Mock(return_value=processes)
    )
    wait = Mock()
    monkeypatch.setattr("builtins.input", wait)
    return wait


@pytest.mark.parametrize("status", [0, 1, 2, 130])
def test_frozen_entry_point_preserves_status(
    monkeypatch: pytest.MonkeyPatch, explorer_console: Mock, status: int
) -> None:
    monkeypatch.setattr(sys, "platform", "win32")
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(cli, "main", Mock(return_value=status))

    with pytest.raises(SystemExit) as exit_info:
        runpy.run_path(str(INDEX), run_name="__main__")

    assert exit_info.value.code == status
    if status == 130:
        explorer_console.assert_not_called()
    else:
        explorer_console.assert_called_once_with(windows_console._CLOSE_PROMPT)


@pytest.mark.parametrize("reason", ["ci", "redirected", "missing snapshot"])
def test_uncertain_launch_skips_pause(
    monkeypatch: pytest.MonkeyPatch, explorer_console: Mock, reason: str
) -> None:
    if reason == "ci":
        monkeypatch.setenv("CI", "true")
    elif reason == "redirected":
        windows_console._has_console_streams.return_value = False
    else:
        windows_console._process_snapshot.return_value = {}

    assert windows_console.pause_after_explorer_launch(1) == 1
    explorer_console.assert_not_called()


@pytest.mark.parametrize(
    ("error", "status"), [(KeyboardInterrupt, 130), (EOFError, 1), (OSError, 1)]
)
def test_interrupted_pause(
    explorer_console: Mock, error: type[BaseException], status: int
) -> None:
    explorer_console.side_effect = error
    assert windows_console.pause_after_explorer_launch(1) == status
