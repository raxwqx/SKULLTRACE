"""Verify a local file against a SHA-256 reference without any network access."""

from __future__ import annotations

import hmac
import re
from pathlib import Path
from typing import Any

from skulltrace.core.reports import create_report
from skulltrace.modules.file_hash import analyze_file_hash

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def normalize_sha256_reference(value: str) -> str:
    """Normalize a SHA-256 reference to 64 lowercase hexadecimal characters.

    A leading ``sha256:`` or ``sha-256:`` label is accepted for convenience,
    as are surrounding whitespace and uppercase hexadecimal digits. All other
    forms are rejected so a typo cannot silently become a comparison failure.
    """
    if not isinstance(value, str):
        raise ValueError("Reference SHA-256 must be text.")
    candidate = value.strip()
    if not candidate:
        raise ValueError("Enter a SHA-256 reference digest.")
    if ":" in candidate:
        algorithm, _, candidate = candidate.partition(":")
        if algorithm.strip().lower() not in {"sha256", "sha-256"}:
            raise ValueError("Only SHA-256 references are supported; use a 64-character hexadecimal digest.")
        candidate = candidate.strip()
    if not candidate:
        raise ValueError("Enter a SHA-256 reference digest.")
    candidate = candidate.lower()
    if not _SHA256_RE.fullmatch(candidate):
        raise ValueError("Reference SHA-256 must contain exactly 64 hexadecimal characters (0-9, a-f).")
    return candidate


def verify_file_sha256(value: str, reference: str) -> dict[str, Any]:
    """Compare a local file's SHA-256 with a user-supplied trusted reference.

    The file is read once through :func:`analyze_file_hash`. Nothing is
    uploaded, modified or executed, and the comparison uses
    :func:`hmac.compare_digest` for constant-time behavior.
    """
    display_name = Path(value).name if isinstance(value, str) else str(value)
    display_name = display_name or str(value)
    try:
        expected = normalize_sha256_reference(reference)
    except ValueError as exc:
        return create_report(
            module="verify", target=display_name, status="error", results={}, note=str(exc)
        )

    fingerprint = analyze_file_hash(value)
    if fingerprint.get("status") != "ok":
        return create_report(
            module="verify",
            target=fingerprint.get("target", display_name),
            status="error",
            results={},
            note=fingerprint.get("note", "The file could not be hashed."),
        )

    actual = fingerprint["results"]["sha256"]
    matches = hmac.compare_digest(actual, expected)
    if matches:
        note = (
            "SHA-256 matches the supplied reference. This confirms integrity relative to that "
            "reference only; make sure the reference came from a trusted source."
        )
    else:
        note = (
            "SHA-256 does not match the supplied reference. Do not treat the file as verified. "
            "The file was not modified or uploaded."
        )
    return create_report(
        module="verify",
        target=fingerprint["target"],
        status="ok" if matches else "mismatch",
        results={
            "algorithm": "SHA-256",
            "expected_sha256": expected,
            "actual_sha256": actual,
            "matches": matches,
            "size_bytes": fingerprint["results"]["size_bytes"],
            "read_only": True,
            "uploaded": False,
            "comparison": "hmac.compare_digest (constant-time)",
        },
        note=note,
    )
