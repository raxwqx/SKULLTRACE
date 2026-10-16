"""Calculate local file fingerprints using Python's standard library."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from skulltrace.core.reports import create_report

_CHUNK_SIZE = 1024 * 1024


def analyze_file_hash(value: str) -> dict[str, Any]:
    """Hash a user-selected regular file without uploading or modifying it."""
    path = Path(value).expanduser()
    display_name = path.name or str(value)
    try:
        if not path.exists():
            raise FileNotFoundError("File does not exist.")
        if not path.is_file():
            raise ValueError("Choose a regular file, not a directory or special file.")
        digests = {
            "sha256": hashlib.sha256(),
            "sha1": hashlib.sha1(),
            "md5": hashlib.md5(),
        }
        size = 0
        with path.open("rb") as stream:
            while chunk := stream.read(_CHUNK_SIZE):
                size += len(chunk)
                for digest in digests.values():
                    digest.update(chunk)
    except (OSError, ValueError) as exc:
        return create_report(
            module="hash", target=display_name, status="error", results={},
            note=f"Could not hash file: {exc}",
        )
    return create_report(
        module="hash", target=display_name, status="ok",
        results={
            "size_bytes": size,
            "sha256": digests["sha256"].hexdigest(),
            "sha1": digests["sha1"].hexdigest(),
            "md5": digests["md5"].hexdigest(),
            "read_only": True,
            "uploaded": False,
            "md5_note": "Included for legacy compatibility only; do not use MD5 as a modern security guarantee.",
        },
        note="Hashes were calculated locally. The file was not modified or uploaded.",
    )
