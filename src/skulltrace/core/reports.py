"""Creation and serialization helpers for structured reports."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from skulltrace import __version__


def create_report(module: str, target: str, status: str, results: dict[str, Any], note: str) -> dict[str, Any]:
    """Return a consistent JSON-serializable report envelope."""
    return {
        "tool": "SKULLTRACE",
        "version": __version__,
        "module": module,
        "target": target,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": status,
        "results": results,
        "note": note,
    }


def report_to_json(report: dict[str, Any]) -> str:
    """Serialize a report in stable, readable JSON."""
    return json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True)


def write_report(report: dict[str, Any], path: str | Path) -> Path:
    """Write a report as UTF-8 JSON and return the resolved output path."""
    output_path = Path(path).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_to_json(report) + "\n", encoding="utf-8")
    return output_path
