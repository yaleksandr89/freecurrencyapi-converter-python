"""Package a native executable and test the actual archived copy offline."""

import argparse
import hashlib
import os
import platform
import subprocess
import tarfile
import tempfile
import zipfile
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPTS_DIR.parent
SUPPORT_FILES = (
    SCRIPTS_DIR / "standalone" / "README.md",
    PROJECT_ROOT / ".env.example",
    PROJECT_ROOT / "LICENSE.md",
)
MACOS_LAUNCHER = SCRIPTS_DIR / "Launch Currency Converter.command"


def create_archive(executable: Path, archive: Path, launcher: Path | None) -> None:
    archive.parent.mkdir(parents=True, exist_ok=True)
    files = (executable, *SUPPORT_FILES)
    if launcher is not None:
        files += (launcher,)
    if archive.suffix == ".zip":
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
            for path in files:
                bundle.write(path, arcname=path.name)
    else:
        with tarfile.open(archive, "w:gz") as bundle:
            for path in files:
                bundle.add(path, arcname=path.name, recursive=False)


def extract_archive(
    archive: Path, destination: Path, executable_name: str, launcher: Path | None
) -> None:
    support_files = SUPPORT_FILES
    if launcher is not None:
        support_files += (launcher,)
    expected = sorted([executable_name, *(path.name for path in support_files)])
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
    create_archive(executable, archive, launcher)
    with tempfile.TemporaryDirectory(prefix="currency-converter-") as temp:
        root = Path(temp).resolve()
        extracted = root / ("extracted bundle" if launcher is not None else "extracted")
        workdir = root / "work"
        workdir.mkdir()
        extract_archive(archive, extracted, executable_name, launcher)
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
