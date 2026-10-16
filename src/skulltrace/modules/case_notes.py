"""Create a structured, local observation note for a research case."""

from __future__ import annotations

from typing import Any

from skulltrace.core.reports import create_report


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
    return create_report(
        module="case-note", target=name, status="ok",
        results={"observation": note, "source_verified": False, "evidence_attached": False},
        note="User-authored note only. Preserve provenance and avoid unnecessary personal data.",
    )
