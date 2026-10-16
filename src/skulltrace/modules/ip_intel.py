"""Local-only IPv4/IPv6 address classification."""

from __future__ import annotations

import ipaddress
from typing import Any

from skulltrace.core.reports import create_report


def analyze_ip(value: str) -> dict[str, Any]:
    """Classify an IP address locally; no external service is contacted."""
    candidate = value.strip() if isinstance(value, str) else ""
    try:
        address = ipaddress.ip_address(candidate)
    except ValueError:
        return create_report(
            module="ip", target=str(value), status="error", results={},
            note="Enter a valid IPv4 or IPv6 address.",
        )

    if address.is_unspecified:
        classification = "unspecified"
    elif address.is_loopback:
        classification = "loopback"
    elif address.is_multicast:
        classification = "multicast"
    elif address.is_link_local:
        classification = "link_local"
    elif address.is_private:
        classification = "private"
    elif address.is_reserved:
        classification = "reserved"
    elif address.is_global:
        classification = "global"
    else:
        classification = "special_or_unclassified"

    result = {
        "address": str(address),
        "version": address.version,
        "classification": classification,
        "is_global": address.is_global,
        "is_private": address.is_private,
        "is_loopback": address.is_loopback,
        "is_link_local": address.is_link_local,
        "is_multicast": address.is_multicast,
        "is_reserved": address.is_reserved,
        "is_unspecified": address.is_unspecified,
        "reverse_dns_name": address.reverse_pointer,
    }
    return create_report(
        module="ip", target=str(address), status="ok", results=result,
        note="Classification was computed locally with Python's ipaddress module; no external lookup was performed.",
    )
