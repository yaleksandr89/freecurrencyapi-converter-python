"""Package a native executable and test the actual archived copy offline."""

import argparse
import csv
import hashlib
import io
import os
import platform
import re
import subprocess
import sys
import sysconfig
import tarfile
import tempfile
import zipfile
from importlib import metadata
from pathlib import Path, PurePosixPath

SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPTS_DIR.parent
SUPPORT_FILES = (
    SCRIPTS_DIR / "standalone" / "README.md",
    PROJECT_ROOT / ".env.example",
    PROJECT_ROOT / "LICENSE.md",
)
MACOS_LAUNCHER = SCRIPTS_DIR / "Launch Currency Converter.command"
NOTICE_NAME = "THIRD_PARTY_NOTICES.txt"
RUNTIME_DISTRIBUTIONS = (
    "certifi",
    "charset-normalizer",
    "idna",
    "python-dotenv",
    "requests",
    "urllib3",
)


def read_notice(root: Path, relative: PurePosixPath, component: str) -> bytes:
    path = root.joinpath(*relative.parts)
    try:
        if path.resolve(strict=True) != path or not path.is_file():
            raise ValueError
        content = path.read_bytes()
        if not content.decode("utf-8").strip():
            raise ValueError
    except (OSError, RuntimeError, ValueError):
        raise SystemExit(
            f"{component}: missing, unreadable, or invalid license file {relative}"
        ) from None
    return content


def cpython_notice() -> bytes:
    component = f"CPython {platform.python_version()}"
    for directory in (Path(sys.base_prefix), Path(sysconfig.get_path("stdlib"))):
        if not directory.is_absolute():
            continue
        root = directory.resolve()
        for name in ("LICENSE.txt", "LICENSE"):
            if (root / name).exists():
                return f"=== {component} / {name} ===\n".encode() + read_notice(
                    root, PurePosixPath(name), component
                )
    raise SystemExit(
        f"{component}: LICENSE.txt or LICENSE missing from the base Python "
        "installation and standard library"
    )


def safe_metadata_path(value: str) -> bool:
    return all(
        re.fullmatch(r'[^\\:<>|"\x00-\x1f?*]+', part)
        and not part.startswith(".")
        and not part.endswith((".", " "))
        for part in value.split("/")
    )


def installed_records(dist: metadata.Distribution) -> set[PurePosixPath]:
    # Keep missing entries so a recorded license that vanished still fails the build.
    rows = csv.reader(io.StringIO(dist.read_text("RECORD") or ""))
    return {PurePosixPath(row[0]) for row in rows if row and safe_metadata_path(row[0])}


def distribution_notices(dist: metadata.Distribution, label: str) -> list[bytes]:
    name, version = dist.name, dist.version
    if (
        not name
        or not version
        or not all(
            re.fullmatch(r"[A-Za-z0-9._+!-]+", value) for value in (name, version)
        )
    ):
        raise SystemExit(f"{label}: invalid installed distribution name or version")
    component = f"{name} {version}"
    records = installed_records(dist)
    metadata_dirs = {
        file.parent
        for file in records
        if len(file.parts) == 2
        and file.name == "METADATA"
        and file.parent.suffix == ".dist-info"
    }
    if len(metadata_dirs) != 1:
        raise SystemExit(
            f"{component}: could not identify installed .dist-info records"
        )
    (dist_info,) = metadata_dirs
    licenses = dist_info / "licenses"
    files = {
        file for file in records if file.is_relative_to(licenses) and file != licenses
    }
    files.update(
        file
        for file in records
        if file.parent == dist_info
        and file.name.upper().split(".", 1)[0] in {"LICENSE", "NOTICE", "COPYING"}
    )
    for value in dist.metadata.get_all("License-File", []):
        if not safe_metadata_path(value):
            raise SystemExit(f"{component}: unsafe License-File metadata path")
        if licenses / value not in files and dist_info / value not in files:
            raise SystemExit(f"{component}: declared license file {value} missing")
    if not files:
        raise SystemExit(f"{component}: no installed license files recorded")

    root = Path(dist.locate_file("")).resolve()
    return [
        f"=== {component} / {file} ===\n".encode() + read_notice(root, file, component)
        for file in sorted(files)
    ]


def collected_modules(executable: Path) -> set[str]:
    # Use the same pinned PyInstaller used to build this executable.
    try:
        from PyInstaller.archive.readers import CArchiveReader, NotAnArchiveError
        from PyInstaller.loader.pyimod01_archive import PYZ_ITEM_NSPKG, ArchiveReadError
    except ModuleNotFoundError:
        raise SystemExit(
            "PyInstaller is required in the standalone build venv"
        ) from None

    try:
        archive = CArchiveReader(str(executable)).open_embedded_archive("PYZ.pyz")
    except (OSError, KeyError, NotAnArchiveError, ArchiveReadError):
        raise SystemExit(
            "Could not read the executable's PyInstaller module table"
        ) from None
    return {name for name, entry in archive.toc.items() if entry[0] != PYZ_ITEM_NSPKG}


def installed_distribution(name: str) -> metadata.Distribution:
    try:
        return metadata.distribution(name)
    except metadata.PackageNotFoundError:
        raise SystemExit(f"{name}: required build distribution is missing") from None


def vendored_notices(
    setuptools: metadata.Distribution, modules: set[str]
) -> list[bytes]:
    prefix = "setuptools._vendor."
    bundled = {name.removeprefix(prefix) for name in modules if name.startswith(prefix)}
    if not bundled:
        return []

    # Match shipped modules to RECORDs only in setuptools' vendor directory.
    root = Path(setuptools.locate_file("")).resolve()
    vendor = root / "setuptools" / "_vendor"
    if vendor.resolve() != vendor or not vendor.is_dir():
        raise SystemExit(
            f"setuptools {setuptools.version}: missing or invalid vendor directory"
        )
    distributions = metadata.Distribution.discover(path=[str(vendor)])
    notices = []
    covered = set()
    for dist in distributions:
        supplied = {
            ".".join(
                file.parts[:-1]
                if file.name == "__init__.py"
                else file.with_suffix("").parts
            )
            for file in installed_records(dist)
            if file.suffix == ".py"
        }
        if bundled & supplied:
            covered.update(supplied)
            notices.extend(
                distribution_notices(dist, "setuptools vendored distribution")
            )
    if missing := bundled - covered:
        raise SystemExit(
            f"setuptools {setuptools.version}: missing distribution records for "
            f"bundled vendor modules {', '.join(sorted(missing))}"
        )
    return notices


def build_notices(executable: Path) -> bytes:
    python = cpython_notice()
    modules = collected_modules(executable)
    notices = []
    for name in (*RUNTIME_DISTRIBUTIONS, "packaging", "setuptools"):
        if name in RUNTIME_DISTRIBUTIONS or name in modules:
            dist = installed_distribution(name)
            notices.extend(distribution_notices(dist, name))
            if name == "setuptools":
                notices.extend(vendored_notices(dist, modules))
    return b"\n\n".join(
        [b"Third-party notices for Currency Converter", python, *sorted(notices)]
    )


def create_archive(
    executable: Path, archive: Path, launcher: Path | None, notices: bytes
) -> None:
    archive.parent.mkdir(parents=True, exist_ok=True)
    files = (executable, *SUPPORT_FILES)
    if launcher is not None:
        files += (launcher,)
    if archive.suffix == ".zip":
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
            for path in files:
                bundle.write(path, arcname=path.name)
            bundle.writestr(NOTICE_NAME, notices)
    else:
        with tarfile.open(archive, "w:gz") as bundle:
            for path in files:
                bundle.add(path, arcname=path.name, recursive=False)
            entry = tarfile.TarInfo(NOTICE_NAME)
            entry.size = len(notices)
            bundle.addfile(entry, io.BytesIO(notices))


def extract_archive(
    archive: Path,
    destination: Path,
    executable_name: str,
    launcher: Path | None,
    notices: bytes,
) -> None:
    support_files = SUPPORT_FILES
    if launcher is not None:
        support_files += (launcher,)
    expected = sorted([executable_name, NOTICE_NAME, *(p.name for p in support_files)])
    if archive.suffix == ".zip":
        with zipfile.ZipFile(archive) as bundle:
            if sorted(bundle.namelist()) != expected:
                raise SystemExit(f"Unexpected archive members: {bundle.namelist()}")
            bundle.extractall(destination)
    else:
        with tarfile.open(archive, "r:gz") as bundle:
            members = bundle.getmembers()
            if sorted(bundle.getnames()) != expected or not all(
                member.isfile() for member in members
            ):
                raise SystemExit(f"Unexpected archive members: {bundle.getnames()}")
            bundle.extractall(destination, filter="data")
        if not os.access(destination / executable_name, os.X_OK):
            raise SystemExit("Archived executable lost its execute permission")
    if launcher is not None and not os.access(destination / launcher.name, os.X_OK):
        raise SystemExit("Archived macOS launcher lost its execute permission")
    for source in support_files:
        if (destination / source.name).read_bytes() != source.read_bytes():
            raise SystemExit(f"Archived {source.name} content differs from the source")
    if (destination / NOTICE_NAME).read_bytes() != notices:
        raise SystemExit(f"Archived {NOTICE_NAME} content differs from the source")
    print(f"{archive.name} contains only {', '.join(expected)}")


def check_native_executable(executable: Path) -> None:
    system = platform.system()
    with executable.open("rb") as binary:
        header = binary.read(64)
        if system == "Linux":
            # ELF class 2, little-endian, EM_X86_64.
            native = (
                header.startswith(b"\x7fELF\x02\x01") and header[18:20] == b"\x3e\0"
            )
        elif system == "Windows":
            # The DOS header points to the PE signature and AMD64 COFF machine.
            binary.seek(int.from_bytes(header[60:64], "little"))
            native = header.startswith(b"MZ") and binary.read(6) == b"PE\0\0\x64\x86"
        elif system == "Darwin":
            # Thin 64-bit little-endian Mach-O with CPU_TYPE_ARM64.
            native = header.startswith(b"\xcf\xfa\xed\xfe\x0c\0\0\x01")
        else:
            raise SystemExit(f"Unexpected smoke test platform: {system}")
    if not native:
        raise SystemExit(f"Unexpected native executable format on {system}")
    print(f"Verified native executable format on {system} {platform.machine()}")


def run_cli(
    entrypoint: Path, args: tuple[str, ...], workdir: Path, env: dict[str, str]
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(entrypoint), *args],
        cwd=workdir,
        env=env,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        encoding="utf-8",
        timeout=30,
        check=False,
    )


def smoke_test(executable: Path, workdir: Path, launcher: Path | None) -> None:
    env = {
        "PYTHON_DOTENV_DISABLED": "1",
        "TEMP": str(workdir),
        "TMP": str(workdir),
        "TMPDIR": str(workdir),
    }
    if platform.system() == "Windows":
        env["SystemRoot"] = os.environ["SystemRoot"]

    cases = (
        (("--help",), 0, ("Использование:", "Показать справку"), ""),
        (("--lang", "en", "--help"), 0, ("Usage:", "Show this help"), ""),
        (
            ("--unknown",),
            2,
            (),
            "Некорректные аргументы. Используйте --help для справки.",
        ),
        (
            (),
            1,
            (),
            "Ошибка: Отсутствует обязательная переменная окружения: API_TOKEN",
        ),
    )
    for args, status, stdout_markers, stderr in cases:
        result = run_cli(executable, args, workdir, env)
        label = " ".join(args) or "(no arguments)"
        if (
            result.returncode != status
            or not all(marker in result.stdout for marker in stdout_markers)
            or result.stderr != (f"{stderr}\n" if stderr else "")
        ):
            raise SystemExit(
                f"{label}: expected exit {status}, stdout markers {stdout_markers!r} "
                f"and stderr {stderr!r}. Got exit {result.returncode}\n"
                f"stdout: {result.stdout!r}\nstderr: {result.stderr!r}"
            )
        print(f"{label}: exit {status}, output verified")
        if launcher is not None:
            launched = run_cli(launcher, args, workdir, env)
            if (launched.returncode, launched.stdout, launched.stderr) != (
                result.returncode,
                result.stdout,
                result.stderr,
            ):
                raise SystemExit(
                    f"{launcher.name} {label}: expected the binary's exit and output. "
                    f"Got exit {launched.returncode}\n"
                    f"stdout: {launched.stdout!r}\nstderr: {launched.stderr!r}"
                )
            print(f"{launcher.name} {label}: exit {status}, output verified")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("executable", type=Path)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    executable = args.executable
    archive = args.archive
    system = platform.system()
    executable_name = (
        "currency-converter.exe" if system == "Windows" else "currency-converter"
    )
    extension = ".zip" if system == "Windows" else ".tar.gz"
    if executable.name != executable_name or not archive.name.endswith(extension):
        parser.error(
            f"Expected {executable_name} and a {extension} archive on {system}"
        )
    launcher = MACOS_LAUNCHER if system == "Darwin" else None
    notices = build_notices(executable)
    create_archive(executable, archive, launcher, notices)
    with tempfile.TemporaryDirectory(prefix="currency-converter-") as temp:
        root = Path(temp).resolve()
        extracted = root / ("extracted bundle" if launcher is not None else "extracted")
        workdir = root / "work"
        workdir.mkdir()
        extract_archive(archive, extracted, executable_name, launcher, notices)
        archived_executable = extracted / executable_name
        check_native_executable(archived_executable)
        archived_launcher = extracted / launcher.name if launcher is not None else None
        smoke_test(archived_executable, workdir, archived_launcher)

    with archive.open("rb") as bundle:
        digest = hashlib.file_digest(bundle, "sha256").hexdigest()
    checksum = archive.with_name(f"{archive.name}.sha256")
    checksum.write_text(f"{digest}  {archive.name}\n", encoding="ascii", newline="\n")
    print(f"Wrote {checksum.name}")


if __name__ == "__main__":
    main()
