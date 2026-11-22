"""Keep an Explorer-launched Windows onefile console open after the CLI exits."""

from __future__ import annotations

import ctypes
import os
import sys
from ctypes import wintypes

_CLOSE_PROMPT = "\nНажмите Enter, чтобы закрыть / Press Enter to close: "
_TH32CS_SNAPPROCESS = 0x00000002
_ERROR_NO_MORE_FILES = 18
_ENABLE_LINE_INPUT = 0x0002
_INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value


class _ProcessEntry(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("cntUsage", wintypes.DWORD),
        ("th32ProcessID", wintypes.DWORD),
        ("th32DefaultHeapID", wintypes.WPARAM),
        ("th32ModuleID", wintypes.DWORD),
        ("cntThreads", wintypes.DWORD),
        ("th32ParentProcessID", wintypes.DWORD),
        ("pcPriClassBase", wintypes.LONG),
        ("dwFlags", wintypes.DWORD),
        ("szExeFile", wintypes.WCHAR * wintypes.MAX_PATH),
    ]


def _process_snapshot(kernel32: ctypes.WinDLL) -> dict[int, tuple[int, str]]:
    create_snapshot = kernel32.CreateToolhelp32Snapshot
    create_snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
    create_snapshot.restype = wintypes.HANDLE

    first, next_entry = kernel32.Process32FirstW, kernel32.Process32NextW
    for read_entry in (first, next_entry):
        read_entry.argtypes = [wintypes.HANDLE, ctypes.POINTER(_ProcessEntry)]
        read_entry.restype = wintypes.BOOL

    close_handle = kernel32.CloseHandle
    close_handle.argtypes = [wintypes.HANDLE]
    close_handle.restype = wintypes.BOOL

    snapshot = create_snapshot(_TH32CS_SNAPPROCESS, 0)
    if snapshot == _INVALID_HANDLE_VALUE:
        return {}

    try:
        entry = _ProcessEntry(dwSize=ctypes.sizeof(_ProcessEntry))
        if not first(snapshot, ctypes.byref(entry)):
            return {}
        processes = {}
        while True:
            processes[entry.th32ProcessID] = (
                entry.th32ParentProcessID,
                entry.szExeFile,
            )
            if not next_entry(snapshot, ctypes.byref(entry)):
                return (
                    processes if ctypes.get_last_error() == _ERROR_NO_MORE_FILES else {}
                )
    finally:
        close_handle(snapshot)


def _launched_by_explorer(processes: dict[int, tuple[int, str]], pid: int) -> bool:
    # A Windows onefile bundle runs the CLI in a child of the same executable.
    # The snapshot records parent PIDs, which can be stale after a parent exits.
    # Missing entries and launchers between Explorer and the EXE skip the pause.
    try:
        bootloader_pid, image = processes[pid]
        launcher_pid, bootloader_image = processes[bootloader_pid]
        _, launcher_image = processes[launcher_pid]
    except KeyError:
        return False
    return (
        len({pid, bootloader_pid, launcher_pid}) == 3
        and image.casefold() == bootloader_image.casefold()
        and launcher_image.casefold() == "explorer.exe"
    )


def _has_console_streams(kernel32: ctypes.WinDLL) -> bool:
    import msvcrt

    get_mode = kernel32.GetConsoleMode
    get_mode.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
    get_mode.restype = wintypes.BOOL

    mode = wintypes.DWORD()
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if stream is None or not stream.isatty():
            return False
        if not get_mode(msvcrt.get_osfhandle(stream.fileno()), ctypes.byref(mode)):
            return False
        if stream is sys.stdin and not mode.value & _ENABLE_LINE_INPUT:
            return False
    return True


def pause_after_explorer_launch(status: int) -> int:
    """Wait for Enter only in a console with the expected onefile ancestry."""
    if status == 130 or "CI" in os.environ:
        return status
    try:
        kernel32 = ctypes.WinDLL("kernel32.dll", use_last_error=True)
        if _has_console_streams(kernel32) and _launched_by_explorer(
            _process_snapshot(kernel32), os.getpid()
        ):
            input(_CLOSE_PROMPT)
    except KeyboardInterrupt:
        return 130
    except (OSError, ValueError, EOFError):
        # The console or its streams may have become unavailable.
        pass
    return status
