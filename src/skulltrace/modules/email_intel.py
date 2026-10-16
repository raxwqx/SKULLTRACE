"""Privacy-conscious email address syntax inspection; no mailbox verification."""

from __future__ import annotations

import re
from typing import Any

from skulltrace.core.reports import create_report
from skulltrace.modules.dns_intel import normalize_hostname

_LOCAL_RE = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+$")


def analyze_email(value: str) -> dict[str, Any]:
    """Check basic email syntax without contacting DNS or a mail server."""
    raw = value.strip() if isinstance(value, str) else ""
    if not raw or any(ord(char) < 32 or char.isspace() for char in raw):
        return create_report(
            module="email", target="[invalid email]", status="error", results={},
            note="Enter one email address without whitespace or control characters.",
        )
    if raw.count("@") != 1:
        return create_report(
            module="email", target="[invalid email]", status="error", results={},
            note="An email address must contain exactly one @ symbol.",
        )

    local, domain_raw = raw.rsplit("@", 1)
    if (
        not local or len(local) > 64 or local.startswith(".") or local.endswith(".")
        or ".." in local or not _LOCAL_RE.fullmatch(local)
    ):
        return create_report(
            module="email", target="[invalid email]", status="error", results={},
            note="The local part does not pass SKULLTRACE's basic syntax checks.",
        )
    try:
        domain = normalize_hostname(domain_raw)
    except ValueError as exc:
        return create_report(
            module="email", target="[invalid email]", status="error", results={},
            note=f"The domain part is invalid: {exc}",
        )
    if "." not in domain or domain.startswith(".") or domain.endswith("."):
        return create_report(
            module="email", target="[invalid email]", status="error", results={},
            note="The domain part must contain at least two labels.",
        )

    return create_report(
        module="email", target=f"{local}@{domain}", status="ok",
        results={
            "syntax_valid_basic": True,
            "local_part": local,
            "domain": domain,
            "domain_labels": domain.split("."),
            "mailbox_checked": False,
            "dns_checked": False,
        },
        note="Basic syntax only. This does not establish ownership, deliverability, or whether the mailbox exists.",
    )
