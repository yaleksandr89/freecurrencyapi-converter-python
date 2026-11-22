"""Entry point for the interactive currency converter."""

import sys

from currency_converter.main import main

if __name__ == "__main__":
    status = main()
    if sys.platform == "win32" and getattr(sys, "frozen", False):
        from currency_converter.windows_console import pause_after_explorer_launch

        status = pause_after_explorer_launch(status)
    sys.exit(status)
