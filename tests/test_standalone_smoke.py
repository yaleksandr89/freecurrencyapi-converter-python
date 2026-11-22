"""Verify the standalone archive layout without building platform binaries."""

import os
import stat
import zipfile
from pathlib import Path

import pytest

from scripts import standalone_smoke

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "scripts" / "standalone" / "README.md"
LAUNCHER = ROOT / "scripts" / "Launch Currency Converter.command"
POSIX_ONLY = pytest.mark.skipif(os.name != "posix", reason="requires Unix file modes")


@pytest.mark.parametrize(
    ("archive_name", "executable_name", "launcher"),
    [
        ("windows.zip", "currency-converter.exe", None),
        pytest.param("linux.tar.gz", "currency-converter", None, marks=POSIX_ONLY),
        pytest.param("macos.tar.gz", "currency-converter", LAUNCHER, marks=POSIX_ONLY),
    ],
)
def test_standalone_archive(
    tmp_path: Path, archive_name: str, executable_name: str, launcher: Path | None
) -> None:
    executable = tmp_path / executable_name
    executable.write_bytes(b"offline executable stub")
    executable.chmod(0o755)
    (tmp_path / ".env").write_bytes(b"not for distribution")
    archive = tmp_path / archive_name
    extracted = tmp_path / "extracted bundle"

    standalone_smoke.create_archive(executable, archive, launcher)
    standalone_smoke.extract_archive(archive, extracted, executable_name, launcher)

    sources = {
        "README.md": README,
        ".env.example": ROOT / ".env.example",
        "LICENSE.md": ROOT / "LICENSE.md",
        executable_name: executable,
    }
    if launcher is not None:
        sources["Launch Currency Converter.command"] = launcher
        assert stat.S_IMODE((extracted / launcher.name).stat().st_mode) == 0o755
    if archive_name.endswith(".tar.gz"):
        assert stat.S_IMODE((extracted / executable_name).stat().st_mode) == 0o755
    assert {path.name for path in extracted.iterdir()} == sources.keys()
    for name, source in sources.items():
        assert (extracted / name).read_bytes() == source.read_bytes()
    readme = (extracted / "README.md").read_text(encoding="utf-8")
    assert readme.splitlines()[0] == "# Currency Converter / Конвертер валют"
    assert [line for line in readme.splitlines() if line.startswith("## ")] == [
        "## Русский",
        "## English",
    ]


@pytest.mark.parametrize(
    ("name", "error"),
    [
        (".env", "Unexpected archive members"),
        (".env.example", r"Archived \.env\.example content differs"),
    ],
)
def test_standalone_archive_rejects_extra_or_changed_file(
    tmp_path: Path, name: str, error: str
) -> None:
    archive = tmp_path / "invalid.zip"
    with zipfile.ZipFile(archive, "w") as bundle:
        bundle.writestr("currency-converter.exe", b"offline executable stub")
        for source in (README, ROOT / "LICENSE.md", ROOT / ".env.example"):
            if source.name != name:
                bundle.write(source, arcname=source.name)
        bundle.writestr(name, b"unexpected data")

    with pytest.raises(SystemExit, match=error):
        standalone_smoke.extract_archive(
            archive, tmp_path / "extracted", "currency-converter.exe", None
        )
