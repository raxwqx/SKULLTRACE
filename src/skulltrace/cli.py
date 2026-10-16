"""Command-line interface and interactive menu for SKULLTRACE."""

from __future__ import annotations

import argparse
import sys
from typing import Sequence

from skulltrace import __version__
from skulltrace.core.reports import report_to_json, write_report
from skulltrace.modules.case_notes import create_case_note
from skulltrace.modules.dns_intel import analyze_hostname
from skulltrace.modules.domain_intel import analyze_domain
from skulltrace.modules.email_intel import analyze_email
from skulltrace.modules.file_hash import analyze_file_hash
from skulltrace.modules.ip_intel import analyze_ip
from skulltrace.modules.local_info import analyze_local_info
from skulltrace.modules.url_intel import analyze_url
from skulltrace.ui.banner import print_banner
from skulltrace.ui.console import print_report


def _add_output_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--json", action="store_true", help="print the result as JSON")
    parser.add_argument("--output", metavar="PATH", help="save the JSON report to PATH")


def build_parser() -> argparse.ArgumentParser:
    """Build the reusable argument parser."""
    parser = argparse.ArgumentParser(
        prog="skulltrace",
        description="A modular, low-impact OSINT and local-analysis workbench.",
        epilog="Use only for lawful research and authorized targets. URL analysis does not fetch pages.",
    )
    parser.add_argument("--version", action="version", version=f"SKULLTRACE {__version__}")
    subparsers = parser.add_subparsers(dest="command")

    dns_parser = subparsers.add_parser("dns", help="resolve a hostname via the system resolver")
    dns_parser.add_argument("hostname", help="hostname only, for example example.com")
    _add_output_options(dns_parser)

    ip_parser = subparsers.add_parser("ip", help="classify an IP address locally")
    ip_parser.add_argument("address", help="IPv4 or IPv6 address")
    _add_output_options(ip_parser)

    url_parser = subparsers.add_parser("url", help="inspect URL syntax without visiting it")
    url_parser.add_argument("url", help="complete http:// or https:// URL")
    _add_output_options(url_parser)

    email_parser = subparsers.add_parser("email", help="check basic email syntax only")
    email_parser.add_argument("address", help="one email address")
    _add_output_options(email_parser)

    domain_parser = subparsers.add_parser("domain", help="validate hostname syntax offline")
    domain_parser.add_argument("hostname", help="domain or hostname")
    _add_output_options(domain_parser)

    hash_parser = subparsers.add_parser("hash", help="calculate hashes for a local file")
    hash_parser.add_argument("path", help="path to a regular file")
    _add_output_options(hash_parser)

    local_parser = subparsers.add_parser("local-info", help="show local host and runtime metadata")
    _add_output_options(local_parser)

    note_parser = subparsers.add_parser("case-note", help="format a local research observation")
    note_parser.add_argument("case_name", help="short case or project label")
    note_parser.add_argument("observation", nargs="+", help="observation text; quote it to preserve spaces")
    _add_output_options(note_parser)

    subparsers.add_parser("about", help="show project scope and safety notes")
    return parser


def _display(report: dict, as_json: bool, output: str | None) -> int:
    """Render one report and, optionally, save a JSON copy."""
    if output:
        try:
            written = write_report(report, output)
        except OSError as exc:
            print(f"SKULLTRACE: could not write report: {exc}", file=sys.stderr)
            return 2
        if not as_json:
            print(f"JSON report saved to: {written}")
    if as_json:
        print(report_to_json(report))
    else:
        print_report(report)
    return 0 if report.get("status") == "ok" else 1


def _interactive_report(report: dict) -> None:
    """Show a result and optionally export it."""
    print_report(report)
    destination = input("  JSON report path (Enter to skip): ").strip()
    if destination:
        try:
            written = write_report(report, destination)
            print(f"  Report saved: {written}\n")
        except OSError as exc:
            print(f"  Could not save report: {exc}\n")


def _run_interactive() -> int:
    """Run the numbered terminal menu."""
    if not sys.stdin.isatty():
        build_parser().print_help()
        return 0

    while True:
        print_banner()
        print("  [1] DNS intelligence       Hostname A/AAAA resolution")
        print("  [2] IP inspector           Local IPv4/IPv6 classification")
        print("  [3] URL risk hints         Static parsing; no page fetch")
        print("  [4] Email syntax           No mailbox or DNS verification")
        print("  [5] Domain validation      Offline hostname syntax")
        print("  [6] File fingerprint       SHA-256 / SHA-1 / MD5")
        print("  [7] Local machine info     Host/runtime snapshot")
        print("  [8] Case note              Structured observation report")
        print("  [9] About & safety")
        print("  [0] Exit")
        try:
            choice = input("\n  skulltrace > ").strip().lower()
            if choice in {"0", "q", "quit", "exit"}:
                print("\n  Stay curious. Trace responsibly. 🐍\n")
                return 0
            if choice == "1":
                report = analyze_hostname(input("  Hostname: ").strip())
            elif choice == "2":
                report = analyze_ip(input("  IPv4/IPv6 address: ").strip())
            elif choice == "3":
                report = analyze_url(input("  Full URL: ").strip())
            elif choice == "4":
                report = analyze_email(input("  Email address: ").strip())
            elif choice == "5":
                report = analyze_domain(input("  Domain/hostname: ").strip())
            elif choice == "6":
                report = analyze_file_hash(input("  File path: ").strip())
            elif choice == "7":
                report = analyze_local_info()
            elif choice == "8":
                case_name = input("  Case name: ").strip()
                observation = input("  Observation: ").strip()
                report = create_case_note(case_name, observation)
            elif choice == "9":
                print("\n  SKULLTRACE is built for low-impact learning and authorized research.")
                print("  DNS uses your configured system resolver.")
                print("  IP, domain, email and URL syntax checks do not contact the target.")
                print("  File hashes are calculated locally; files are not uploaded or changed.")
                print("  Avoid unnecessary personal data and never treat a hint as proof.\n")
                input("  Press Enter to return to the menu...")
                continue
            else:
                print("  Unknown option. Choose 0-9.\n")
                continue
            _interactive_report(report)
        except (EOFError, KeyboardInterrupt):
            print("\n  Exiting SKULLTRACE. Trace responsibly.\n")
            return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Run SKULLTRACE and return a process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        return _run_interactive()
    if args.command == "about":
        print_banner()
        print("SKULLTRACE is a low-impact OSINT and local-analysis workbench.")
        print("DNS resolution uses the system resolver; URL inspection never fetches pages.")
        print("IP, domain and email checks are syntax/local analysis; file hashes stay local.")
        print("Use only for lawful research and authorized targets.")
        return 0

    if args.command == "dns":
        report = analyze_hostname(args.hostname)
    elif args.command == "ip":
        report = analyze_ip(args.address)
    elif args.command == "url":
        report = analyze_url(args.url)
    elif args.command == "email":
        report = analyze_email(args.address)
    elif args.command == "domain":
        report = analyze_domain(args.hostname)
    elif args.command == "hash":
        report = analyze_file_hash(args.path)
    elif args.command == "local-info":
        report = analyze_local_info()
    elif args.command == "case-note":
        report = create_case_note(args.case_name, " ".join(args.observation))
    else:
        parser.print_help()
        return 0
    return _display(report, args.json, args.output)


if __name__ == "__main__":
    raise SystemExit(main())
