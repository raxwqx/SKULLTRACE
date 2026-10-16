<div align="center">
  <img src="assets/skulltrace.svg" alt="SKULLTRACE grinning skull and serpent emblem" width="180" />
  <h1>SKULLTRACE</h1>
  <p><strong>A modular OSINT and local-analysis workbench with a grinning skull + snake terminal splash.</strong></p>
  <p>
    <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" />
    <img alt="License" src="https://img.shields.io/badge/License-MIT-14B8A6" />
    <img alt="Runtime dependencies" src="https://img.shields.io/badge/Runtime%20dependencies-None-64748B" />
  </p>
</div>

SKULLTRACE is an original Python project for learning and performing low-impact analysis of public network metadata and local files. It is inspired by the broad idea of an OSINT workbench, not by another project's source code, branding, or implementation.

## Features

1. **DNS intelligence:** resolve a hostname to A/AAAA addresses through the configured system resolver.
2. **IP inspector:** classify IPv4/IPv6 addresses locally, including private, global, loopback and reserved status.
3. **URL risk hints:** parse URLs for common syntax warning signs without fetching or opening the page. Credentials, query strings and fragments are omitted from the report target.
4. **Email syntax check:** inspect basic formatting without checking a mailbox, contacting a mail server or establishing ownership.
5. **Domain validation:** normalize IDN hostnames and summarize labels offline, without checking ownership or registration.
6. **File fingerprinting:** calculate SHA-256, SHA-1 and MD5 hashes locally; files are read-only and never uploaded. MD5 is included for legacy comparison only.
7. **Local machine snapshot:** show local hostname, OS, architecture, Python version and addresses returned by the system resolver for the local hostname.
8. **Case notes:** format a researcher-authored observation as a structured JSON report.
9. **Report export:** display any command's result as JSON or save it to a path you choose.
10. **Interactive terminal:** a colored, snake-framed grinning skull ASCII splash and numbered menu.
11. **Test suite and CI:** offline unit tests plus a GitHub Actions workflow.

## Requirements

- Python 3.10 or newer
- Kali Linux, another Linux distribution, macOS, or Windows
- No third-party runtime dependencies

## Quick start on Kali Linux

```bash
cd ~/projeler/SKULLTRACE
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Launch the interactive splash and menu:

```bash
skulltrace
```

If you have not installed the package yet, run it from the repository root:

```bash
PYTHONPATH=src python3 -m skulltrace
```

## Command examples

```bash
# DNS resolution through the system resolver
skulltrace dns example.com

# Local IP classification
skulltrace ip 8.8.8.8

# Static URL checks only, no page visit
skulltrace url 'https://example.com/login?campaign=test'

# Syntax only, no mailbox verification
skulltrace email researcher@example.com

# Offline domain-name validation
skulltrace domain example.com

# Local file fingerprint
skulltrace hash ./sample.bin

# Local machine/runtime snapshot
skulltrace local-info

# Create a structured observation note
skulltrace case-note lab-01 'Observed the expected test result'
```

Append `--json` to print machine-readable output. Add `--output reports/result.json` to save JSON to a file. For example:

```bash
skulltrace url 'https://example.com' --json
skulltrace ip 8.8.8.8 --output reports/ip-report.json
```

## Privacy and scope notes

- DNS hostname resolution may send a DNS query through the resolver configured on the machine.
- URL inspection is entirely static: SKULLTRACE never visits the URL or follows redirects.
- IP classification, domain syntax and email syntax analysis are local calculations; email analysis does not check mailbox existence.
- File hashes are calculated on the machine; files are not modified or uploaded.
- The local machine snapshot asks the system resolver about the local hostname, so exact behavior follows local system configuration.
- A warning flag is only a hint, not proof that something is malicious or safe.

Use SKULLTRACE only for lawful research, systems you own, or targets for which you have explicit authorization. Minimize personal data in notes and reports. See [SECURITY.md](SECURITY.md) and [docs/methodology.md](docs/methodology.md).

## Project layout

```text
SKULLTRACE/
├── assets/skulltrace.svg
├── docs/
├── src/skulltrace/
│   ├── core/             # Shared configuration and JSON reports
│   ├── modules/          # DNS, IP, URL, email, domain, hash, local info, notes
│   ├── ui/               # Skull-and-snake splash and terminal report renderer
│   └── cli.py
├── tests/
├── .github/workflows/tests.yml
├── pyproject.toml
├── SECURITY.md
└── CONTRIBUTING.md
```

## Tests

Run from the repository root:

```bash
python3 -m compileall -q src tests
python3 -m unittest discover -s tests -v
```

The tests avoid external dependencies and mock DNS resolution where necessary.

## License

MIT. See [LICENSE](LICENSE).
