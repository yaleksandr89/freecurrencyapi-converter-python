"""Verify the standalone archive layout without building platform binaries."""

import os
import stat
import tarfile
import zipfile
from importlib import metadata
from pathlib import Path

import pytest

from scripts import standalone_smoke

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "scripts" / "standalone" / "README.md"
LAUNCHER = ROOT / "scripts" / "Launch Currency Converter.command"
POSIX_ONLY = pytest.mark.skipif(os.name != "posix", reason="requires Unix file modes")
NOTICE_NAME = "THIRD_PARTY_NOTICES.txt"
NOTICES = b"Third-party notices for Currency Converter\n\nSynthetic license\n"


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

    standalone_smoke.create_archive(executable, archive, launcher, NOTICES)
    standalone_smoke.extract_archive(
        archive, extracted, executable_name, launcher, NOTICES
    )

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
    assert {path.name for path in extracted.iterdir()} == set(sources) | {NOTICE_NAME}
    assert (extracted / NOTICE_NAME).read_bytes() == NOTICES
    for name, source in sources.items():
        assert (extracted / name).read_bytes() == source.read_bytes()
    readme = (extracted / "README.md").read_text(encoding="utf-8")
    assert readme.splitlines()[0] == "# Currency Converter / Конвертер валют"
    assert [line for line in readme.splitlines() if line.startswith("## ")] == [
        "## Русский",
        "## English",
    ]


@pytest.mark.parametrize(
    "extension", [".zip", pytest.param(".tar.gz", marks=POSIX_ONLY)]
)
@pytest.mark.parametrize(
    ("name", "content", "error"),
    [
        (".env", b"unexpected data", "Unexpected archive members"),
        ("../unexpected", b"unexpected data", "Unexpected archive members"),
        (".env.example", b"changed", r"Archived \.env\.example content differs"),
        (NOTICE_NAME, b"changed", f"Archived {NOTICE_NAME} content differs"),
        (NOTICE_NAME, None, "Unexpected archive members"),
    ],
)
def test_standalone_archive_rejects_extra_or_changed_file(
    tmp_path: Path, extension: str, name: str, content: bytes | None, error: str
) -> None:
    archive = tmp_path / f"invalid{extension}"
    executable = tmp_path / "currency-converter"
    executable.write_bytes(b"offline executable stub")
    executable.chmod(0o755)
    notices = tmp_path / NOTICE_NAME
    notices.write_bytes(NOTICES)
    files = {
        source.name: source
        for source in (
            executable,
            README,
            ROOT / "LICENSE.md",
            ROOT / ".env.example",
            notices,
        )
        if source.name != name
    }
    if content is not None:
        replacement = tmp_path / "replacement"
        replacement.write_bytes(content)
        files[name] = replacement
    if extension == ".zip":
        with zipfile.ZipFile(archive, "w") as bundle:
            for arcname, source in files.items():
                bundle.write(source, arcname=arcname)
    else:
        with tarfile.open(archive, "w:gz") as bundle:
            for arcname, source in files.items():
                bundle.add(source, arcname=arcname, recursive=False)

    with pytest.raises(SystemExit, match=error):
        standalone_smoke.extract_archive(
            archive, tmp_path / "extracted", executable.name, None, NOTICES
        )
    assert not (tmp_path / "unexpected").exists()


def installed_dist(
    root: Path, name: str, files: dict[str, bytes], *declared: str
) -> metadata.Distribution:
    dist_info = root / f"{name.replace('-', '_')}-1.2.dist-info"
    dist_info.mkdir(parents=True)
    declarations = "".join(f"License-File: {file}\n" for file in declared)
    (dist_info / "METADATA").write_text(
        f"Name: {name}\nVersion: 1.2\n{declarations}", encoding="utf-8"
    )
    for relative, content in files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    records = [f"{dist_info.name}/METADATA", *files]
    (dist_info / "RECORD").write_text(
        "".join(f"{path},,\n" for path in records), encoding="utf-8"
    )
    return metadata.Distribution.at(dist_info)


def test_build_notices_uses_complete_text_and_bundled_distributions(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    python = tmp_path / "python"
    stdlib = python / "Lib"
    stdlib.mkdir(parents=True)
    python_license = b"CPython terms\r\nCopyright PSF\r\n\r\n"
    (stdlib / "LICENSE.txt").write_bytes(python_license)
    monkeypatch.setattr(standalone_smoke.sys, "base_prefix", str(python))
    monkeypatch.setattr(standalone_smoke.sysconfig, "get_path", lambda _: str(stdlib))
    monkeypatch.setattr(
        standalone_smoke,
        "collected_modules",
        lambda _: {"setuptools", "setuptools._vendor.example.module"},
    )
    site = tmp_path / "site"
    required = {}
    for name in standalone_smoke.RUNTIME_DISTRIBUTIONS:
        dist_info = f"{name.replace('-', '_')}-1.2.dist-info"
        required[name] = installed_dist(
            site,
            name,
            {f"{dist_info}/licenses/LICENSE": b"Full terms\n"},
            "LICENSE",
        )
    required["setuptools"] = installed_dist(
        site,
        "setuptools",
        {"setuptools-1.2.dist-info/LICENSE.txt": b"Legacy terms\n"},
        "LICENSE.txt",
    )
    vendor = site / "setuptools" / "_vendor"
    installed_dist(
        vendor,
        "example",
        {
            "example-1.2.dist-info/licenses/LICENSE": b"Vendor terms\n",
            "example-1.2.dist-info/licenses/NOTICE": b"Copyright attribution\n\n",
            "example/module.py": b"Bundled Python module",
        },
        "NOTICE",
        "LICENSE",
    )
    installed_dist(vendor, "unused", {"unused.py": b"Unbundled Python module"})
    monkeypatch.setattr(standalone_smoke.metadata, "distribution", required.__getitem__)

    notices = standalone_smoke.build_notices(tmp_path / "executable")
    assert python_license in notices
    for name in required:
        assert f"=== {name} 1.2 / ".encode() in notices
    assert b"example-1.2.dist-info/licenses/LICENSE ===\nVendor terms\n" in notices
    assert (
        b"example-1.2.dist-info/licenses/NOTICE ===\nCopyright attribution\n\n"
        in notices
    )
    assert b"Legacy terms\n" in notices
    assert b"Unbundled Python module" not in notices
    assert notices == standalone_smoke.build_notices(tmp_path / "executable")


@pytest.mark.parametrize(
    ("declared", "reason"),
    [
        ("NOTICE", "declared license file NOTICE missing"),
        ("../outside", "unsafe License-File metadata path"),
        ("C:/outside", "unsafe License-File metadata path"),
        ("sub\\outside", "unsafe License-File metadata path"),
    ],
)
def test_distribution_notices_reject_invalid_declarations(
    tmp_path: Path, declared: str, reason: str
) -> None:
    dist = installed_dist(
        tmp_path,
        "example",
        {"example-1.2.dist-info/LICENSE": b"Full terms\n"},
        declared,
    )
    with pytest.raises(SystemExit, match=rf"example 1\.2: {reason}"):
        standalone_smoke.distribution_notices(dist, "example")


def test_distribution_notices_fail_when_recorded_file_is_missing(
    tmp_path: Path,
) -> None:
    relative = "example-1.2.dist-info/licenses/LICENSE"
    dist = installed_dist(tmp_path, "example", {relative: b"Full terms\n"}, "LICENSE")
    (tmp_path / relative).unlink()
    with pytest.raises(SystemExit, match=r"example 1\.2: missing.*LICENSE"):
        standalone_smoke.distribution_notices(dist, "example")


@POSIX_ONLY
def test_distribution_notices_reject_symlink_to_unrelated_file(tmp_path: Path) -> None:
    relative = "example-1.2.dist-info/licenses/LICENSE"
    dist = installed_dist(tmp_path, "example", {relative: b"Full terms\n"}, "LICENSE")
    unrelated = tmp_path / ".env"
    unrelated.write_bytes(b"synthetic unrelated content")
    license_file = tmp_path / relative
    license_file.unlink()
    license_file.symlink_to(unrelated)
    with pytest.raises(SystemExit, match=r"example 1\.2: .*invalid license file"):
        standalone_smoke.distribution_notices(dist, "example")


def test_missing_cpython_license_fails_before_archive_creation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "LICENSE.txt").write_bytes(b"Unrelated license")
    python = tmp_path / "python"
    monkeypatch.setattr(standalone_smoke.sys, "base_prefix", str(python))
    monkeypatch.setattr(
        standalone_smoke.sysconfig, "get_path", lambda _: str(python / "Lib")
    )
    monkeypatch.setattr(standalone_smoke.platform, "system", lambda: "Linux")
    archive = tmp_path / "dist" / "bundle.tar.gz"
    monkeypatch.setattr(
        standalone_smoke.sys,
        "argv",
        ["standalone_smoke.py", "currency-converter", str(archive)],
    )
    with pytest.raises(SystemExit, match="CPython .* LICENSE.txt or LICENSE missing"):
        standalone_smoke.main()
    assert not archive.parent.exists()
