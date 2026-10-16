"""Tests for local IP address classification."""

import unittest
from skulltrace.modules.ip_intel import analyze_ip


class IPAnalysisTests(unittest.TestCase):
    def test_ipv4_global(self):
        report = analyze_ip("8.8.8.8")
        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["results"]["version"], 4)
        self.assertEqual(report["results"]["classification"], "global")
        self.assertTrue(report["results"]["is_global"])

    def test_private_ipv4(self):
        report = analyze_ip("192.168.1.1")
        self.assertEqual(report["results"]["classification"], "private")
        self.assertTrue(report["results"]["is_private"])

    def test_ipv6_loopback(self):
        report = analyze_ip("::1")
        self.assertEqual(report["results"]["version"], 6)
        self.assertEqual(report["results"]["classification"], "loopback")

    def test_invalid_address(self):
        report = analyze_ip("not-an-ip")
        self.assertEqual(report["status"], "error")
        self.assertEqual(report["results"], {})


if __name__ == "__main__":
    unittest.main()
