"""Collect a small local machine snapshot using Python's standard library."""

from __future__ import annotations

import platform
import socket
import sys
from typing import Any

from skulltrace.core.reports import create_report


def analyze_local_info() -> dict[str, Any]:
    """Return local host and runtime metadata; no remote target is queried."""
    hostname = socket.gethostname() or "unknown"
    resolved_addresses: set[str] = set()
    resolution_note = "Local hostname resolution returned no addresses."
    try:
        for answer in socket.getaddrinfo(hostname, None, type=socket.SOCK_STREAM):
            sockaddr = answer[4]
            if sockaddr:
                resolved_addresses.add(str(sockaddr[0]).split("%", 1)[0])
        resolution_note = "Addresses were obtained from the system's resolver for the local hostname."
    except (socket.gaierror, OSError):
        pass
    results = {
        "hostname": hostname,
        "platform": platform.system(),
        "platform_release": platform.release(),
        "machine_architecture": platform.machine(),
        "python_version": platform.python_version(),
        "local_hostname_addresses": sorted(resolved_addresses),
    }
    return create_report(
        module="local-info", target=hostname, status="ok", results=results,
        note=resolution_note + " System resolver behavior depends on local configuration.",
    )
