"""Offline tests for the DNS intelligence module."""

import socket
import unittest
from unittest.mock import patch

from skulltrace.modules.dns_intel import analyze_hostname, normalize_hostname


class HostnameValidationTests(unittest.TestCase):
    def test_normalizes_case_and_trailing_dot(self):
        self.assertEqual(normalize_hostname(" Example.COM. "), "example.com")

    def test_encodes_internationalized_domain(self):
        self.assertEqual(normalize_hostname("bücher.example"), "xn--bcher-kva.example")

    def test_rejects_url(self):
        with self.assertRaises(ValueError):
            normalize_hostname("https://example.com/path")

    def test_rejects_ip_literal(self):
        with self.assertRaises(ValueError):
            normalize_hostname("8.8.8.8")

    def test_rejects_invalid_label(self):
        with self.assertRaises(ValueError):
            normalize_hostname("-bad.example")


class DNSAnalysisTests(unittest.TestCase):
    @patch("skulltrace.modules.dns_intel.socket.getaddrinfo")
    def test_returns_deduplicated_addresses(self, mock_getaddrinfo):
        mock_getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("203.0.113.5", 0)),
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("203.0.113.5", 0)),
            (socket.AF_INET6, socket.SOCK_STREAM, 6, "", ("2001:db8::5", 0, 0, 0)),
        ]
        report = analyze_hostname("example.com")
        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["results"]["count"], 2)
        self.assertEqual(report["results"]["addresses"], ["203.0.113.5", "2001:db8::5"])
        mock_getaddrinfo.assert_called_once()

    @patch("skulltrace.modules.dns_intel.socket.getaddrinfo", side_effect=socket.gaierror("not found"))
    def test_resolver_error_is_reported(self, _mock_getaddrinfo):
        report = analyze_hostname("missing.example")
        self.assertEqual(report["status"], "error")
        self.assertEqual(report["results"]["addresses"], [])

    def test_invalid_input_returns_error_report(self):
        report = analyze_hostname("https://example.com")
        self.assertEqual(report["status"], "error")
        self.assertIn("hostname only", report["note"])


if __name__ == "__main__":
    unittest.main()
