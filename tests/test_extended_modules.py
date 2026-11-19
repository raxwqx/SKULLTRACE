"""Offline tests for the additional SKULLTRACE modules."""

import hashlib
import socket
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from skulltrace.modules.case_notes import create_case_note
from skulltrace.modules.domain_intel import analyze_domain
from skulltrace.modules.email_intel import analyze_email
from skulltrace.modules.file_hash import analyze_file_hash
from skulltrace.modules.local_info import analyze_local_info
from skulltrace.modules.url_intel import analyze_url


class URLAnalysisTests(unittest.TestCase):
    def test_https_url_has_no_network_fetch(self):
        report = analyze_url("https://example.com/research")
        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["results"]["scheme"], "https")
        self.assertIn("not fetched", report["results"]["checks_performed"])

    def test_http_is_flagged(self):
        report = analyze_url("http://example.com")
        self.assertTrue(any("HTTP" in flag for flag in report["results"]["flags"]))

    def test_credentials_and_query_are_removed_from_report_target(self):
        report = analyze_url("https://user:secret@example.com/login?token=hidden#section")
        self.assertEqual(report["status"], "ok")
        self.assertNotIn("secret", report["target"])
        self.assertNotIn("hidden", report["target"])

    def test_rejects_unsupported_scheme(self):
        report = analyze_url("javascript:alert(1)")
        self.assertEqual(report["status"], "error")

    def test_trailing_dot_and_idn_are_normalized_in_target(self):
        trailing = analyze_url("https://example.com./path")
        self.assertEqual(trailing["target"], "https://example.com/path")
        idn = analyze_url("https://bücher.example/path")
        self.assertEqual(idn["results"]["hostname"], "xn--bcher-kva.example")
        self.assertEqual(idn["target"], "https://xn--bcher-kva.example/path")

    def test_malformed_percent_escape_is_flagged(self):
        report = analyze_url("https://example.com/%zz")
        self.assertEqual(report["status"], "ok")
        self.assertTrue(any("malformed percent" in flag for flag in report["results"]["flags"]))

    def test_control_characters_are_rejected(self):
        report = analyze_url("https://example.com/\x1b[31mred")
        self.assertEqual(report["status"], "error")
        self.assertIn("control characters", report["note"])


class DomainAndEmailTests(unittest.TestCase):
    def test_domain_is_normalized(self):
        report = analyze_domain("Example.COM.")
        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["results"]["ascii_hostname"], "example.com")

    def test_bad_domain_rejected(self):
        self.assertEqual(analyze_domain("https://example.com")["status"], "error")

    def test_email_basic_syntax(self):
        report = analyze_email("Researcher@example.com")
        self.assertEqual(report["status"], "ok")
        self.assertFalse(report["results"]["mailbox_checked"])

    def test_email_with_multiple_at_symbols_rejected(self):
        self.assertEqual(analyze_email("a@@example.com")["status"], "error")


class LocalAnalysisTests(unittest.TestCase):
    def test_file_hash_matches_sha256(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.bin"
            path.write_bytes(b"SKULLTRACE test data")
            report = analyze_file_hash(str(path))
        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["results"]["sha256"], hashlib.sha256(b"SKULLTRACE test data").hexdigest())
        self.assertTrue(report["results"]["read_only"])

    def test_missing_file_returns_error(self):
        report = analyze_file_hash("/definitely/not/a/real/skulltrace-file")
        self.assertEqual(report["status"], "error")

    def test_unresolvable_home_expansion_returns_error(self):
        with mock.patch.object(Path, "expanduser", side_effect=RuntimeError("no home directory")):
            report = analyze_file_hash("~/sample.bin")
        self.assertEqual(report["status"], "error")
        self.assertIn("Could not open", report["note"])

    def test_local_addresses_are_sorted_numerically(self):
        answers = [
            (socket.AF_INET6, socket.SOCK_STREAM, 6, "", ("::1", 0, 0, 0)),
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("127.0.0.1", 0)),
        ]
        with mock.patch("skulltrace.modules.local_info.socket.getaddrinfo", return_value=answers):
            report = analyze_local_info()
        self.assertEqual(report["results"]["local_hostname_addresses"], ["127.0.0.1", "::1"])

    def test_case_note_rejects_terminal_controls(self):
        self.assertEqual(create_case_note("case\x1b[31m", "observation")["status"], "error")
        self.assertEqual(create_case_note("case", "observation\x00")["status"], "error")
        self.assertEqual(create_case_note("case", "line one\nline two")["status"], "ok")

    def test_local_snapshot_has_runtime_fields(self):
        report = analyze_local_info()
        self.assertEqual(report["status"], "ok")
        self.assertIn("python_version", report["results"])

    def test_case_note_requires_both_fields(self):
        self.assertEqual(create_case_note("", "observation")["status"], "error")

    def test_case_note_keeps_observation(self):
        report = create_case_note("lab-01", "Observed a test result")
        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["results"]["observation"], "Observed a test result")


if __name__ == "__main__":
    unittest.main()
