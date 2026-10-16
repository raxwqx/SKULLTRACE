"""Low-impact hostname resolution using the operating system's resolver."""

from __future__ import annotations

import ipaddress
import re
import socket
from typing import Any

from skulltrace.core.reports import create_report

_LABEL_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$", re.IGNORECASE)


def normalize_hostname(value: str) -> str:
    """Validate and normalize a hostname; URLs and raw IP addresses are rejected."""
    if not isinstance(value, str):
        raise ValueError("Hostname must be text.")
    candidate = value.strip().rstrip(".")
    if not candidate:
        raise ValueError("Enter a hostname such as example.com.")
    if any(char in candidate for char in "/\\?#@") or ":" in candidate:
        raise ValueError("Enter a hostname only, not a URL, path, or IP address.")
    try:
        ipaddress.ip_address(candidate)
    except ValueError:
        pass
    else:
        raise ValueError("This module expects a hostname. Use the IP module for IP addresses.")
    try:
        ascii_name = candidate.encode("idna").decode("ascii").lower()
    except UnicodeError as exc:
        raise ValueError("Hostname contains invalid internationalized characters.") from exc
    if len(ascii_name) > 253:
        raise ValueError("Hostname is longer than the DNS limit of 253 characters.")
    labels = ascii_name.split(".")
    if any(not _LABEL_RE.fullmatch(label) for label in labels):
        raise ValueError("Hostname contains an invalid DNS label.")
    return ascii_name


def analyze_hostname(value: str) -> dict[str, Any]:
    """Resolve one hostname and return a structured report without scanning."""
    try:
        hostname = normalize_hostname(value)
    except ValueError as exc:
        return create_report(
            module="dns", target=str(value), status="error", results={"addresses": []},
            note=str(exc),
        )

    addresses: set[str] = set()
    try:
        answers = socket.getaddrinfo(hostname, None, type=socket.SOCK_STREAM)
        for answer in answers:
            sockaddr = answer[4]
            if sockaddr:
                try:
                    addresses.add(str(ipaddress.ip_address(sockaddr[0])))
                except ValueError:
                    continue
    except (socket.gaierror, OSError) as exc:
        return create_report(
            module="dns", target=hostname, status="error", results={"addresses": []},
            note=f"The system resolver could not resolve this hostname: {exc}",
        )

    sorted_addresses = sorted(
        addresses,
        key=lambda item: (ipaddress.ip_address(item).version, int(ipaddress.ip_address(item))),
    )
    status = "ok" if sorted_addresses else "no_results"
    note = (
        "Resolved through the operating system's configured resolver. This is a lookup, not a scan."
        if sorted_addresses else
        "The resolver returned no usable A/AAAA addresses."
    )
    return create_report(
        module="dns", target=hostname, status=status,
        results={"addresses": sorted_addresses, "count": len(sorted_addresses)}, note=note,
    )
