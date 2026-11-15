"""CLI/report tests that do not require internet access."""

import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from skulltrace.cli import main
from skulltrace.core.reports import create_report, write_report
from skulltrace.modules.file_hash import analyze_file_hash


class CLIAndReportTests(unittest.TestCase):
    def test_ip_json_output_is_valid(self):
        buffer = StringIO()
        with redirect_stdout(buffer):
            code = main(["ip", "8.8.8.8", "--json"])
        self.assertEqual(code, 0)
        payload = json.loads(buffer.getvalue())
        self.assertEqual(payload["tool"], "SKULLTRACE")
        self.assertEqual(payload["module"], "ip")

    def test_invalid_ip_returns_nonzero(self):
        buffer = StringIO()
        with redirect_stdout(buffer):
            code = main(["ip", "invalid", "--json"])
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(buffer.getvalue())["status"], "error")

    def test_report_file_is_valid_json(self):
        report = create_report("test", "example", "ok", {"value": 1}, "unit test")
        with tempfile.TemporaryDirectory() as directory:
            path = write_report(report, Path(directory) / "nested" / "report.json")
            loaded = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(loaded["results"]["value"], 1)

    def test_hash_reference_check_reports_match_mismatch_and_bad_digest(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.bin"
            path.write_bytes(b"abc")
            matching = analyze_file_hash(str(path), "BA7816BF8F01CFEA414140DE5DAE2223B00361A396177A9CB410FF61F20015AD")
            mismatch = analyze_file_hash(str(path), "0" * 64)
            invalid = analyze_file_hash(str(path), "not-a-digest")

        self.assertEqual(matching["status"], "ok")
        self.assertTrue(matching["results"]["sha256_verification"]["matches"])
        self.assertEqual(mismatch["status"], "mismatch")
        self.assertFalse(mismatch["results"]["sha256_verification"]["matches"])
        self.assertEqual(invalid["status"], "error")


if __name__ == "__main__":
    unittest.main()
