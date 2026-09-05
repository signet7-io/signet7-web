from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PrivacyPaperChromeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.privacy = (ROOT / "privacy.html").read_text(encoding="utf-8")
        cls.check = (ROOT / "check.html").read_text(encoding="utf-8")

    def test_privacy_page_uses_check_paper_chrome(self) -> None:
        """Privacy uses the same paper browser chrome as the live check brochure."""
        privacy = self.privacy
        check = self.check
        self.assertIn('data-theme="light"', check)
        self.assertIn('content="#f7f4ee"', check)
        self.assertIn('data-theme="light"', privacy)
        self.assertIn('content="#f7f4ee"', privacy)
        self.assertNotIn('content="#030609"', privacy)
        self.assertIn('href="vsn"', privacy)
        self.assertNotIn("VSN", privacy)
