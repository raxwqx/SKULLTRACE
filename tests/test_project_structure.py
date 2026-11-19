"""Smoke tests for the source layout and package entry point."""

import unittest
from pathlib import Path

import skulltrace
from skulltrace.cli import build_parser


class ProjectStructureTests(unittest.TestCase):
    def test_version_exists(self):
        self.assertRegex(skulltrace.__version__, r"^\d+\.\d+\.\d+$")
        pyproject = Path(skulltrace.__file__).parent.parent.parent / "pyproject.toml"
        self.assertIn(f'version = "{skulltrace.__version__}"', pyproject.read_text(encoding="utf-8"))

    def test_expected_package_directories_exist(self):
        package_dir = Path(skulltrace.__file__).parent
        for relative in ("cli.py", "modules/dns_intel.py", "modules/ip_intel.py", "modules/url_intel.py", "modules/email_intel.py", "modules/domain_intel.py", "modules/file_hash.py", "modules/checksum_verify.py", "modules/local_info.py", "modules/case_notes.py", "ui/banner.py", "core/reports.py"):
            with self.subTest(path=relative):
                self.assertTrue((package_dir / relative).is_file())

    def test_parser_has_expected_commands(self):
        parser = build_parser()
        parsed = parser.parse_args(["ip", "127.0.0.1"])
        self.assertEqual(parsed.command, "ip")
        for command, arguments in (
            ("url", ["https://example.com"]),
            ("email", ["a@example.com"]),
            ("domain", ["example.com"]),
            ("hash", ["README.md"]),
            ("verify", ["README.md", "--sha256", "0" * 64]),
            ("local-info", []),
            ("case-note", ["lab", "example", "observation"]),
        ):
            with self.subTest(command=command):
                parsed_command = build_parser().parse_args([command, *arguments])
                self.assertEqual(parsed_command.command, command)


if __name__ == "__main__":
    unittest.main()
