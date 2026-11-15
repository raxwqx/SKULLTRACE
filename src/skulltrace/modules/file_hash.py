"""Calculate local file fingerprints using Python's standard library."""

from __future__ import annotations

import hashlib
import hmac
import re
from pathlib import Path
from typing import Any

from skulltrace.core.reports import create_report

_CHUNK_SIZE = 1024 * 1024


def analyze_file_hash(value: str, expected_sha256: str | None = None) -> dict[str, Any]:
    """Hash a user-selected regular file without uploading or modifying it."""
    path = Path(value).expanduser()
    display_name = path.name or str(value)
    expected = None
    if expected_sha256 is not None:
        expected = expected_sha256.strip().lower()
        if not re.fullmatch(r"[0-9a-f]{64}", expected):
            return create_report(
                module="hash", target=display_name, status="error", results={},
                note="Expected SHA-256 must contain exactly 64 hexadecimal characters.",
            )
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
    actual_sha256 = digests["sha256"].hexdigest()
    matches = expected is None or hmac.compare_digest(actual_sha256, expected)
    results: dict[str, Any] = {
        "size_bytes": size,
        "sha256": actual_sha256,
        "sha1": digests["sha1"].hexdigest(),
        "md5": digests["md5"].hexdigest(),
        "read_only": True,
        "uploaded": False,
        "md5_note": "Included for legacy compatibility only; do not use MD5 as a modern security guarantee.",
    }
    if expected is not None:
        results["sha256_verification"] = {"expected": expected, "matches": matches}
    return create_report(
        module="hash", target=display_name, status="ok" if matches else "mismatch",
        results=results,
        note=(
            "SHA-256 matches the supplied reference. The file was not modified or uploaded."
            if expected is not None and matches else
            "SHA-256 does not match the supplied reference. The file was not modified or uploaded."
            if expected is not None else
            "Hashes were calculated locally. The file was not modified or uploaded."
        ),
    )
