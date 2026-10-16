<div align="center">
  <img src="assets/skulltrace.svg" alt="SKULLTRACE grinning skull and serpent emblem" width="190" />

  <h1>SKULLTRACE</h1>
  <p><strong>Trace the signal. Respect the boundaries.</strong></p>
  <p>A modular Python OSINT and local-analysis workbench with a grinning skull, serpent-inspired terminal UI, and privacy-conscious design.</p>

  <p>
    <img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" />
    <img alt="MIT License" src="https://img.shields.io/badge/License-MIT-14B8A6.svg" />
    <img alt="No runtime dependencies" src="https://img.shields.io/badge/Runtime%20dependencies-None-64748B.svg" />
    <a href="https://github.com/raxwqx/SKULLTRACE-/actions/workflows/tests.yml"><img alt="Tests" src="https://github.com/raxwqx/SKULLTRACE-/actions/workflows/tests.yml/badge.svg?branch=main" /></a>
  </p>

  <p>
    <a href="#-features">Features</a> •
    <a href="#-installation">Installation</a> •
    <a href="#-usage">Usage</a> •
    <a href="#-privacy--safe-use">Privacy &amp; safety</a> •
    <a href="#-tests">Tests</a>
  </p>
</div>

---

## 🐍 What is SKULLTRACE?

**SKULLTRACE** is an original, modular Python project for learning about Open Source Intelligence (OSINT), inspecting public network metadata, and analyzing local files. It combines a colorful terminal interface with small command-line modules that can be tested independently.

The project is inspired by the general idea of an OSINT workbench. Its code, name, visual identity, and implementation are its own.

> [!NOTE]
> SKULLTRACE is an educational and low-impact analysis toolkit. It is not a people-tracking tool, and it does not try to break into accounts, bypass access controls, or secretly collect private information.

## ✨ Features

| Module | What it does | Network activity |
| --- | --- | --- |
| 🧭 **DNS Intelligence** | Resolves a hostname to A/AAAA addresses using the configured system resolver. | Sends a DNS query through your configured resolver. |
| 🌐 **IP Inspector** | Classifies an IPv4 or IPv6 address, including private, global, loopback and reserved ranges. | None; local analysis. |
| 🔎 **URL Risk Hints** | Parses URL structure and flags basic warning signs without opening the link. Sensitive URL components are excluded from the report target. | None; does not fetch pages or follow redirects. |
| ✉️ **Email Syntax** | Checks basic email-address formatting. | None; does not contact a mail server or verify mailbox ownership. |
| 🏷️ **Domain Validator** | Normalizes and checks hostname/domain syntax, including internationalized names. | None; offline validation. |
| #️⃣ **File Fingerprint** | Computes SHA-256, SHA-1 and MD5 hashes for a local file. | None; reads the file locally without modifying or uploading it. MD5 is for legacy comparison only. |
| 🖥️ **Local Info** | Displays local hostname, operating system, architecture, Python version and resolver-provided local addresses. | May ask the system resolver about the local hostname. |
| 🗒️ **Case Notes** | Turns a researcher-written observation into a structured report. | None. |
| 📄 **JSON Reports** | Prints JSON or saves a result to a path you choose. | File output is local. |
| 💀 **Interactive terminal** | Opens a snake-framed, grinning-skull ASCII splash and numbered menu. | Depends on the selected module. |

A result is an **informational hint**, not proof that a domain, URL, address or file is malicious or safe.

## 🧰 Requirements

- Kali Linux or another Linux distribution; macOS and Windows may also work.
- Python **3.10 or newer**.
- Git for the clone-based installation.
- No third-party **runtime** dependencies.

Check your Python version:

```bash
python3 --version
```

## 🚀 Installation

### Option A: Clone with Git (recommended)

Open a terminal and run:

```bash
# 1. Create a place for projects
mkdir -p ~/projeler
cd ~/projeler

# 2. Download the repository
# The final dash in SKULLTRACE- is part of the repository name.
git clone https://github.com/raxwqx/SKULLTRACE-.git SKULLTRACE
cd SKULLTRACE

# 3. Create and activate an isolated Python environment
python3 -m venv .venv
source .venv/bin/activate

# 4. Install SKULLTRACE in editable mode
python -m pip install -e .
```

### Option B: Download the ZIP

1. Open the [SKULLTRACE repository](https://github.com/raxwqx/SKULLTRACE-).
2. Click **Code → Download ZIP**.
3. Extract the archive and open the extracted project folder in a terminal.
4. From the folder containing `pyproject.toml`, run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

> [!TIP]
> If you do not want to install the package yet, launch it directly from the repository root with `PYTHONPATH=src python3 -m skulltrace`.

## 🎮 Usage

### Launch the interactive terminal

After installation:

```bash
skulltrace
```

Or, from the repository root without installing:

```bash
PYTHONPATH=src python3 -m skulltrace
```

Choose a numbered option from the menu. Enter `0`, `q`, or `quit` to exit.

### Command-line examples

The commands below use documentation-safe sample values. Replace them with your own authorized research targets.

```bash
# DNS: resolve a public hostname
skulltrace dns example.com

# Inspect an IP locally
skulltrace ip 8.8.8.8

# Inspect URL syntax only; the page is not visited
skulltrace url 'https://example.com/login?campaign=test'

# Check basic email syntax only
skulltrace email researcher@example.com

# Validate a domain/hostname offline
skulltrace domain example.com

# Hash a file on your own machine
skulltrace hash ./sample.bin

# Show local system/runtime metadata
skulltrace local-info

# Create a structured observation note
skulltrace case-note lab-01 'Observed the expected test result'

# Display project scope and safety notes
skulltrace about

# Show version and command help
skulltrace --version
skulltrace --help
```

### 📦 Export JSON reports

Append `--json` to print machine-readable JSON. Use `--output PATH` to save the report to a file.

```bash
# Print JSON to the terminal
skulltrace ip 8.8.8.8 --json

# Create the output folder first if it does not exist
mkdir -p reports

# Save a DNS report
skulltrace dns example.com --output reports/dns-report.json

# Save a URL syntax report and print JSON
skulltrace url 'https://example.com' --json --output reports/url-report.json
```

For commands that perform analysis, a non-zero exit status can indicate that the input could not be analyzed successfully. Check the printed report and error message.

## 🗂️ Project structure

```text
SKULLTRACE/
├── assets/
│   └── skulltrace.svg         # Original snake + grinning skull emblem
├── docs/
│   ├── methodology.md         # Analysis approach and limitations
│   └── scenarios/
│       └── TEMPLATE.md        # Research scenario template
├── src/skulltrace/
│   ├── core/                  # Shared configuration and JSON reports
│   ├── modules/               # Independent analysis modules
│   ├── ui/                    # ASCII splash and terminal output
│   ├── cli.py                 # CLI commands and interactive menu
│   └── __main__.py            # python -m skulltrace entry point
├── tests/                     # Offline unit tests
├── .github/workflows/         # Automated test workflow
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── pyproject.toml
├── README.md
└── SECURITY.md
```

## 🧪 Tests

Run these commands from the repository root:

```bash
python3 -m compileall -q src tests
python3 -m unittest discover -s tests -v
```

The test suite is designed to run offline and mocks DNS-related behavior where appropriate. GitHub Actions also runs the test workflow for supported Python versions when changes are pushed or a pull request is opened.

## 🔐 Privacy & safe use

- Use SKULLTRACE only for lawful learning, systems you own, or targets for which you have explicit authorization.
- DNS lookups use your machine's configured resolver and may be visible to that resolver.
- URL inspection is static: the program does **not** visit the URL, fetch the page or follow redirects.
- IP classification, domain syntax checks and email syntax checks run locally.
- File hashing reads local file contents but does not modify or upload them.
- Avoid putting passwords, tokens, private personal data or other secrets into case notes and reports.
- Review JSON reports before sharing them; they may include values you entered.
- Do not treat an automated flag as a definitive security verdict.

Read [SECURITY.md](SECURITY.md) for reporting security concerns and [docs/methodology.md](docs/methodology.md) for the project's analysis principles.

## 🧭 Roadmap

Potential future improvements include richer offline report formatting, more unit tests for edge cases, and additional passive data sources with clear privacy boundaries. Features will be added only when their behavior can be documented and tested.

## 🤝 Contributing

Issues, bug reports, documentation improvements and pull requests are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before contributing. Keep changes modular, testable and respectful of user privacy.

## 📜 License

SKULLTRACE is released under the **MIT License**. See [LICENSE](LICENSE).

---

<div align="center">
  <p><strong>SKULLTRACE</strong> · Trace responsibly. 🐍</p>
  <sub>Built for learning, transparent analysis, and authorized research.</sub>
</div>
