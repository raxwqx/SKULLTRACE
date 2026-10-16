"""CLI/report tests that do not require internet access."""

import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from skulltrace.cli import main
from skulltrace.core.reports import create_report, write_report


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


if __name__ == "__main__":
    unittest.main()
