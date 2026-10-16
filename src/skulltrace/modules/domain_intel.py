"""Offline domain-name syntax analysis."""

from __future__ import annotations

from typing import Any

from skulltrace.core.reports import create_report
from skulltrace.modules.dns_intel import normalize_hostname


def analyze_domain(value: str) -> dict[str, Any]:
    """Validate and describe a domain-like hostname without resolving it."""
    try:
        domain = normalize_hostname(value)
    except ValueError as exc:
        return create_report(
            module="domain", target=str(value), status="error", results={}, note=str(exc)
        )
    labels = domain.split(".")
    return create_report(
        module="domain", target=domain, status="ok",
        results={
            "ascii_hostname": domain,
            "labels": labels,
            "label_count": len(labels),
            "top_level_label": labels[-1],
            "subdomain_label_count": max(0, len(labels) - 2),
            "has_multiple_labels": len(labels) > 1,
            "contains_punycode": any(label.startswith("xn--") for label in labels),
            "resolved": False,
        },
        note="Offline syntax analysis only; this does not verify domain registration or ownership.",
    )
