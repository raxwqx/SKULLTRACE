# Changelog

Notable changes to SKULLTRACE are documented here.

## [0.3.0] - 2026-11-19

### Added
- `verify PATH --sha256 DIGEST` checks a local file against a trusted SHA-256 reference with constant-time comparison. It accepts uppercase digests and an optional `sha256:` prefix.
- Interactive menu option **[9] Verify SHA-256** for the same local-only check.
- Reports distinguish a match (`ok`) from a mismatch (`mismatch`) and include the expected and actual digests.

### Fixed
- Report files are now written atomically, so an interrupted write cannot truncate an existing report. Unwritable paths, invalid home-directory expansion and other path errors return a clear message instead of a traceback.
- URL reports now use the normalized hostname, keeping the report target consistent with the parsed hostname for trailing-dot and internationalized names.
- URLs with control characters are rejected, and malformed percent escapes in URL paths are flagged. Human-readable output strips terminal control sequences from untrusted values.
- Hostnames ending in more than one dot are rejected instead of silently normalized.
- Hashing a path with an unresolvable `~user` expansion returns an error report instead of crashing.
- Local hostname addresses are sorted numerically by IP family instead of as raw strings.
- Case notes reject terminal control characters while still allowing line breaks and tabs in observations.
- README repository links now point to `raxwqx/SKULLTRACE` instead of the old `SKULLTRACE-` name, and the user agent follows the package version automatically.

### Changed
- Expanded the automated test workflow to Ubuntu, Windows and macOS across Python 3.10-3.13.
- Added Turkish documentation alongside the English README.

## [0.2.0] - 2026-10-16

### Added
- Grinning skull and snake ASCII splash screen at startup.
- Static URL risk-hint analysis that never visits the supplied URL.
- Basic email syntax inspection without mailbox verification.
- Offline hostname/domain validation and IDN normalization.
- Local file fingerprinting with SHA-256, SHA-1 and legacy MD5 output.
- Local machine/runtime snapshot and structured case-note reports.
- Optional JSON export from every analysis command.
- Offline unit tests for all new modules.

### Changed
- Expanded the interactive terminal menu from two analysis modules to eight functional workflows.
- Updated SVG emblem with a more visible smile and teeth.
- Expanded the README with usage, privacy boundaries and command examples.

## [0.1.0] - 2026-10-16

### Added
- Initial modular Python package and interactive terminal menu.
- DNS hostname resolution through the system resolver.
- Local IPv4/IPv6 address classification.
- JSON output and file-based reports.
- Offline unit tests and GitHub Actions test workflow.
- Original snake-themed SVG project mark and project documentation.
