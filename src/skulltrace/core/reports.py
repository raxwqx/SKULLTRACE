"""Creation and serialization helpers for structured reports."""

from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from skulltrace import __version__


class ReportWriteError(OSError):
    """Raised when a report cannot be serialized or written safely."""


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
    """Atomically write a report as UTF-8 JSON and return the resolved path.

    The report is first written to a temporary file in the destination
    directory and then moved into place, so an interrupted write cannot
    truncate an existing report.
    """
    temporary: Path | None = None
    try:
        destination = Path(path).expanduser()
        destination.parent.mkdir(parents=True, exist_ok=True)
        payload = report_to_json(report) + "\n"
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=".skulltrace-report-", suffix=".tmp", dir=str(destination.parent)
        )
        temporary = Path(temporary_name)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, destination)
        temporary = None
        return destination.resolve()
    except ReportWriteError:
        raise
    except (OSError, ValueError, RuntimeError, TypeError) as exc:
        raise ReportWriteError(f"could not write report to {str(path)!r}: {exc}") from exc
    finally:
        if temporary is not None:
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass
