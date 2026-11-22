"""Check the Windows archive and launcher with an offline native stub."""

import os
import shutil
import zipfile
from pathlib import Path

import pytest

from scripts import standalone_smoke as smoke


@pytest.mark.parametrize("tampered", [False, True])
def test_windows_archive_contains_launcher(tmp_path: Path, tampered: bool) -> None:
    executable = tmp_path / "currency-converter.exe"
    executable.write_bytes(b"stub")
    archive = tmp_path / "converter.zip"
    launcher = smoke.WINDOWS_LAUNCHER
    smoke.create_archive(executable, archive, launcher)
    with zipfile.ZipFile(archive) as bundle:
        assert sorted(bundle.namelist()) == [
            "LICENSE.md",
            "Launch Currency Converter.cmd",
            "currency-converter.exe",
        ]
        assert bundle.read(launcher.name) == launcher.read_bytes()

    extracted = tmp_path / "extracted bundle"
    if tampered:
        altered = tmp_path / launcher.name
        altered.write_bytes(b"changed launcher")
        smoke.create_archive(executable, archive, altered)
        with pytest.raises(SystemExit, match="content differs from the source"):
            smoke.extract_archive(archive, extracted, executable.name, launcher)
    else:
        smoke.extract_archive(archive, extracted, executable.name, launcher)
        assert (extracted / launcher.name).read_bytes() == launcher.read_bytes()


@pytest.mark.skipif(os.name != "nt", reason="requires Windows cmd.exe")
@pytest.mark.parametrize(
    ("args", "status", "stdout"),
    [
        (("/d", "/c", "type", "bundle-marker.txt"), 0, "From the bundle\n"),
        (("/d", "/c", "exit", "1"), 1, ""),
        (("/d", "/c", "exit", "2"), 2, ""),
    ],
)
def test_windows_launcher_runs_adjacent_executable(
    tmp_path: Path, args: tuple[str, ...], status: int, stdout: str
) -> None:
    bundle = tmp_path / "extracted bundle"
    bundle.mkdir()
    launcher = Path(shutil.copy2(smoke.WINDOWS_LAUNCHER, bundle))
    system_root = os.environ["SystemRoot"]
    shutil.copy2(
        Path(system_root) / "System32" / "cmd.exe", bundle / "currency-converter.exe"
    )
    (bundle / "bundle-marker.txt").write_bytes(b"From the bundle\r\n")

    result = smoke.run_cli(launcher, args, tmp_path, {"SystemRoot": system_root})
    assert result.returncode == status
    assert result.stdout == stdout + "Press Enter to close\n"
    assert result.stderr == ""
