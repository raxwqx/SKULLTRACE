"""Static URL inspection. This module never fetches or visits the URL."""

from __future__ import annotations

import ipaddress
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from skulltrace.core.reports import create_report
from skulltrace.modules.dns_intel import normalize_hostname

_ALLOWED_SCHEMES = {"http", "https"}
_DEFAULT_PORTS = {"http": 80, "https": 443}


def _safe_target(parts) -> str:
    """Build a report target that omits credentials, query strings and fragments."""
    host = parts.hostname or ""
    try:
        ipaddress.ip_address(host)
        if ":" in host:
            host = f"[{host}]"
    except ValueError:
        pass
    try:
        port = parts.port
    except ValueError:
        port = None
    netloc = host if port is None else f"{host}:{port}"
    return urlunsplit((parts.scheme.lower(), netloc, parts.path or "/", "", ""))


def analyze_url(value: str) -> dict[str, Any]:
    """Inspect URL syntax and common warning signs without network access."""
    raw = value.strip() if isinstance(value, str) else ""
    try:
        parts = urlsplit(raw)
        scheme = parts.scheme.lower()
        if scheme not in _ALLOWED_SCHEMES:
            raise ValueError("Use a complete http:// or https:// URL.")
        if not parts.hostname:
            raise ValueError("URL must contain a hostname.")
        if any(ch.isspace() for ch in raw):
            raise ValueError("URL must not contain whitespace.")
        hostname = parts.hostname
        try:
            ipaddress.ip_address(hostname)
            is_ip_literal = True
            normalized_host = hostname
        except ValueError:
            normalized_host = normalize_hostname(hostname)
            is_ip_literal = False
        port = parts.port  # May raise ValueError for a malformed port.
        if port is not None and not 1 <= port <= 65535:
            raise ValueError("Port must be between 1 and 65535.")
    except (ValueError, UnicodeError) as exc:
        return create_report(
            module="url", target="[invalid URL]", status="error", results={},
            note=str(exc),
        )

    flags: list[str] = []
    if scheme == "http":
        flags.append("Connection scheme is HTTP, not encrypted HTTPS.")
    if parts.username is not None or parts.password is not None:
        flags.append("URL contains embedded user information; avoid sharing it.")
    if port is not None and port != _DEFAULT_PORTS[scheme]:
        flags.append(f"Non-default port specified: {port}.")
    if normalized_host.lower().startswith("xn--") or ".xn--" in normalized_host.lower():
        flags.append("Hostname uses an IDN punycode label; verify the intended spelling.")
    if is_ip_literal:
        flags.append("URL uses an IP literal instead of a domain name.")
    if "%" in parts.path:
        flags.append("Path contains percent-encoded characters; inspect the decoded meaning carefully.")
    if "\\" in raw:
        flags.append("URL contains a backslash; browser parsing can differ across contexts.")
    if not flags:
        flags.append("No listed syntactic warning signs detected. This is not a safety verdict.")

    report_target = _safe_target(parts)
    results = {
        "scheme": scheme,
        "hostname": normalized_host,
        "port": port if port is not None else _DEFAULT_PORTS[scheme],
        "explicit_port": port is not None,
        "path_present": bool(parts.path and parts.path != "/"),
        "query_present": bool(parts.query),
        "fragment_present": bool(parts.fragment),
        "embedded_credentials": parts.username is not None or parts.password is not None,
        "hostname_is_ip_literal": is_ip_literal,
        "flags": flags,
        "checks_performed": "Static parsing only; URL was not fetched.",
    }
    return create_report(
        module="url", target=report_target, status="ok", results=results,
        note="Syntax-based hints only. A clean result does not mean a URL is trustworthy.",
    )
