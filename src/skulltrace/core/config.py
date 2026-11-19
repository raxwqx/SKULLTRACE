"""Small, dependency-free configuration constants."""

from pathlib import Path

from skulltrace import __version__

APP_NAME = "SKULLTRACE"
DEFAULT_REPORT_DIR = Path("reports")
USER_AGENT = f"SKULLTRACE/{__version__} (low-impact OSINT research)"
