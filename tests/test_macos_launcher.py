"""Exercise the Finder launcher as a shell script using an offline CLI stub."""

import os
import select
import shutil
import signal
import subprocess
import time
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
LAUNCHER = SCRIPTS_DIR / "Launch Currency Converter.command"
PROMPT = b"Press Enter to close"

pytestmark = pytest.mark.skipif(os.name != "posix", reason="requires a POSIX PTY")


@pytest.fixture
def launcher(tmp_path: Path) -> Path:
    bundle = tmp_path / "extracted bundle"
    bundle.mkdir()
    executable = bundle / "currency-converter"
    executable.write_text(
        '#!/bin/sh\nprintf "result: %s\\n" "$2" >&2\nexit "$1"\n', encoding="utf-8"
    )
    executable.chmod(0o755)
    return Path(shutil.copy2(LAUNCHER, bundle))


@pytest.mark.parametrize(("status", "expected"), [(0, 0), (1, 1), (2, 2), (1, 130)])
def test_interactive_launcher_waits_after_output_and_keeps_status(
    launcher: Path, tmp_path: Path, status: int, expected: int
) -> None:
    master, slave = os.openpty()
    try:
        with subprocess.Popen(
            [launcher, str(status), "with spaces"],
            cwd=tmp_path,
            stdin=slave,
            stdout=slave,
            stderr=slave,
        ) as child:
            try:
                output = b""
                deadline = time.monotonic() + 5
                while PROMPT not in output:
                    ready, _, _ = select.select(
                        [master], [], [], max(0, deadline - time.monotonic())
                    )
                    assert ready, output
                    output += os.read(master, 4096)
                assert output.index(b"result: with spaces") < output.index(PROMPT)
                with pytest.raises(subprocess.TimeoutExpired):
                    child.wait(timeout=0.1)
                if expected == 130:
                    child.send_signal(signal.SIGINT)
                else:
                    os.write(master, b"\n")
                assert child.wait(timeout=5) == expected
            finally:
                if child.poll() is None:
                    child.kill()
    finally:
        os.close(master)
        os.close(slave)


@pytest.mark.parametrize("redirected", ["stdin", "stdout", "stderr", None])
def test_launcher_skips_pause_for_redirection_or_interrupt(
    launcher: Path, tmp_path: Path, redirected: str | None
) -> None:
    master, slave = os.openpty()
    try:
        streams = dict.fromkeys(("stdin", "stdout", "stderr"), slave)
        if redirected is not None:
            streams[redirected] = subprocess.DEVNULL
        status = 130 if redirected is None else 1
        result = subprocess.run(
            [launcher, str(status), "with spaces"],
            cwd=tmp_path,
            **streams,
            timeout=5,
            check=False,
        )
        output = os.read(master, 4096) if select.select([master], [], [], 0)[0] else b""
        assert result.returncode == status
        assert PROMPT not in output
    finally:
        os.close(master)
        os.close(slave)
