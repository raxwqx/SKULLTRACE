# Contributing

Thanks for helping improve SKULLTRACE. Keep contributions small, testable, documented, and respectful of privacy.

## Before opening a change

1. Explain the use case and data source.
2. Document whether a module sends network traffic or shares the target with a third party.
3. Keep modules independent and return structured dictionaries suitable for JSON output.
4. Add offline unit tests. Mock network operations instead of relying on real services.
5. Update the README, methodology, and changelog when behavior changes.

## Local checks

```bash
python3 -m compileall -q src tests
python3 -m unittest discover -s tests -v
```

## Style

Use clear names, type hints for public functions, small functions, and actionable error messages. Do not commit API keys, personal data, local reports, virtual environments, or machine-specific configuration.
