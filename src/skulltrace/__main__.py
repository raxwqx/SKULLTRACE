"""Allow `python -m skulltrace` to run the CLI."""

from skulltrace.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
