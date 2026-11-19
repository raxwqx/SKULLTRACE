"""Create a structured, local observation note for a research case."""

from __future__ import annotations

import re
from typing import Any

from skulltrace.core.reports import create_report

_CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]")


def create_case_note(case_name: str, observation: str) -> dict[str, Any]:
    """Wrap a user-provided observation in the common report format."""
    name = case_name.strip() if isinstance(case_name, str) else ""
    note = observation.strip() if isinstance(observation, str) else ""
    if not name or not note:
        return create_report(
            module="case-note", target=name or "[unnamed case]", status="error", results={},
            note="Both a case name and an observation are required.",
        )
    if len(name) > 120 or len(note) > 10_000:
        return create_report(
            module="case-note", target=name[:120], status="error", results={},
            note="Case name must be at most 120 characters and observation at most 10,000 characters.",
        )
    if (
        _CONTROL_RE.search(name) or "\r" in name or "\n" in name or "\t" in name
        or _CONTROL_RE.search(note)
    ):
        return create_report(
            module="case-note", target=name[:120], status="error", results={},
            note=(
                "Case name and observation must not contain terminal control characters. "
                "Line breaks and tabs are allowed in the observation only."
            ),
        )
    return create_report(
        module="case-note", target=name, status="ok",
        results={"observation": note, "source_verified": False, "evidence_attached": False},
        note="User-authored note only. Preserve provenance and avoid unnecessary personal data.",
    )
