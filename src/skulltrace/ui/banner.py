"""SKULLTRACE's terminal splash: a grinning skull guarded by a serpent."""

from __future__ import annotations

import os
import sys

from skulltrace import __version__


def color_enabled() -> bool:
    """Return whether ANSI color is appropriate for the current terminal."""
    return (
        "NO_COLOR" not in os.environ
        and os.environ.get("TERM", "") != "dumb"
        and hasattr(sys.stdout, "isatty")
        and sys.stdout.isatty()
    )


def paint(text: str, code: str) -> str:
    """Apply ANSI color only when stdout appears to support it."""
    if not color_enabled():
        return text
    return f"\033[{code}m{text}\033[0m"


def print_banner() -> None:
    """Print an original ASCII smile-skull and snake splash screen."""
    snake = r'''                  /^\/^\
            __   /      \__
        _.-'  `-/  /\/\    `-.
      .'         \_/   \__     `.
     /      .-******-.  \       \
    ;      /  .----.  \  \       ;
    |     |  /      \  |  |      |
    |     | |  (o)(o) | |  |      |
    |     | |   \__/  | |  |      |
    |     | |  .----.  | |  |      |
    |     | |  | | | | | |  |      |
    ;      \ \ '----' / /      ;
     \      '._      _.' /      /
      `-._     '----'   /   _.-'
          `--..______..--~~~'''
    teeth = r"""              S K U L L T R A C E
             [ grin wide. trace wisely ]"""
    print(paint(snake, "96;1"))
    print(paint(teeth, "92;1"))
    print(paint(f"                OSINT WORKBENCH  v{__version__}", "90"))
    print(paint("          Passive-first • Modular • Safety-minded", "90"))
    print()
