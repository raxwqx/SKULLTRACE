"""Offline tests for SHA-256 reference verification."""

import hashlib
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

from skulltrace.cli import main
from skulltrace.modules.checksum_verify import normalize_sha256_reference, verify_file_sha256

_SAMPLE = b"SKULLTRACE verification sample\n"
_SAMPLE_SHA256 = hashlib.sha256(_SAMPLE).hexdigest()


class ChecksumVerificationTests(unittest.TestCase):
    def _write_sample(self, directory: str) -> Path:
        path = Path(directory) / "sample.bin"
        path.write_bytes(_SAMPLE)
        return path

    def test_matching_reference_accepts_uppercase_and_prefix(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_sample(directory)
            report = verify_file_sha256(str(path), f"sha256:{_SAMPLE_SHA256.upper()}")
        self.assertEqual(report["status"], "ok")
        self.assertTrue(report["results"]["matches"])
        self.assertEqual(report["results"]["actual_sha256"], _SAMPLE_SHA256)
        self.assertTrue(report["results"]["read_only"])
        self.assertFalse(report["results"]["uploaded"])

    def test_mismatching_reference_is_reported_without_crashing(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_sample(directory)
            report = verify_file_sha256(str(path), "0" * 64)
        self.assertEqual(report["status"], "mismatch")
        self.assertFalse(report["results"]["matches"])
        self.assertEqual(report["results"]["actual_sha256"], _SAMPLE_SHA256)

    def test_invalid_reference_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_sample(directory)
            for reference in ("", "abc", "0" * 63, "g" * 64, "sha512:" + "0" * 64):
                with self.subTest(reference=reference):
                    report = verify_file_sha256(str(path), reference)
                    self.assertEqual(report["status"], "error")

    def test_missing_file_is_reported(self):
        report = verify_file_sha256("/definitely/not/a/real/skulltrace-file", _SAMPLE_SHA256)
        self.assertEqual(report["status"], "error")
        self.assertIn("Could not hash file", report["note"])

    def test_normalize_reference(self):
        self.assertEqual(normalize_sha256_reference(f"  SHA-256:{_SAMPLE_SHA256.upper()}  "), _SAMPLE_SHA256)
        with self.assertRaises(ValueError):
            normalize_sha256_reference("sha1:abc")

    def test_cli_exit_codes_and_json_report(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_sample(directory)
            output = StringIO()
            with redirect_stdout(output):
                code = main(["verify", str(path), "--sha256", _SAMPLE_SHA256, "--json"])
            self.assertEqual(code, 0)
            payload = json.loads(output.getvalue())
            self.assertEqual(payload["module"], "verify")
            self.assertEqual(payload["status"], "ok")

            output = StringIO()
            with redirect_stdout(output):
                code = main(["verify", str(path), "--sha256", "0" * 64, "--json"])
            self.assertEqual(code, 1)
            self.assertEqual(json.loads(output.getvalue())["status"], "mismatch")

            output = StringIO()
            with redirect_stdout(output):
                code = main(["verify", str(path), "--sha256", "not-a-digest", "--json"])
            self.assertEqual(code, 1)
            self.assertEqual(json.loads(output.getvalue())["status"], "error")

    def test_verify_report_can_be_saved(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_sample(directory)
            destination = Path(directory) / "reports" / "verify.json"
            output = StringIO()
            with redirect_stdout(output):
                code = main(
                    [
                        "verify",
                        str(path),
                        "--sha256",
                        _SAMPLE_SHA256,
                        "--output",
                        str(destination),
                    ]
                )
            self.assertEqual(code, 0)
            payload = json.loads(destination.read_text(encoding="utf-8"))
            self.assertEqual(payload["module"], "verify")
            self.assertTrue(payload["results"]["matches"])


class ReportWriteErrorTests(unittest.TestCase):
    def test_bad_output_path_returns_friendly_error(self):
        stderr = StringIO()
        with redirect_stderr(stderr), redirect_stdout(StringIO()):
            code = main(["ip", "127.0.0.1", "--output", "bad\x00path.json"])
        self.assertEqual(code, 2)
        self.assertIn("could not write report", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
