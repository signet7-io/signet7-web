from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AboutPaperChromeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.about = (ROOT / "about.html").read_text(encoding="utf-8")
        cls.check = (ROOT / "check.html").read_text(encoding="utf-8")

    def test_about_page_uses_check_paper_chrome(self) -> None:
        """About uses the same paper browser chrome as the live check brochure."""
        about = self.about
        check = self.check
        self.assertIn('data-theme="light"', check)
        self.assertIn('content="#f7f4ee"', check)
        self.assertIn('data-theme="light"', about)
        self.assertIn('content="#f7f4ee"', about)
        self.assertNotIn('content="#030609"', about)
        self.assertIn('href="vsn"', about)
        self.assertNotIn("VSN", about)
