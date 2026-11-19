"""Human-readable terminal output without third-party dependencies."""

from __future__ import annotations

import re
from typing import Any

from skulltrace.ui.banner import paint

_CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]")


def _safe_text(value: Any) -> str:
    """Render untrusted report text without terminal control sequences."""
    text = str(value).replace("\r\n", "\n").replace("\r", "\n")
    return _CONTROL_RE.sub("\uFFFD", text)


def print_report(report: dict[str, Any]) -> None:
    """Render a report for people; JSON output is handled separately."""
    title = f"{report.get('module', 'analysis').upper()} INTELLIGENCE"
    print(paint(f"\n[ {title} ]", "96;1"))
    print(paint("-" * 54, "90"))
    print(f"Target : {_safe_text(report.get('target', ''))}")
    status = str(report.get("status", "unknown")).upper()
    color = "32;1" if status == "OK" else "33;1" if status == "NO_RESULTS" else "31;1"
    print(f"Status : {paint(status, color)}")
    results = report.get("results", {})
    if "addresses" in results:
        addresses = results.get("addresses", [])
        if addresses:
            for index, address in enumerate(addresses, start=1):
                print(f"  {index:>2}. {_safe_text(address)}")
        else:
            print("  No addresses returned.")
    elif results:
        for key, value in results.items():
            label = str(key).replace("_", " ").capitalize()
            print(f"  {label:<23}: {_safe_text(value)}")
    print(f"Note   : {_safe_text(report.get('note', ''))}")
    print()
