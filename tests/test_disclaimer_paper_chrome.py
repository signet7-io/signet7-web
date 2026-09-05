from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DisclaimerPaperChromeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.disclaimer = (ROOT / "disclaimer.html").read_text(encoding="utf-8")
        cls.check = (ROOT / "check.html").read_text(encoding="utf-8")

    def test_disclaimer_page_uses_check_paper_chrome(self) -> None:
        """Disclaimer uses the same paper browser chrome as the live check brochure."""
        disclaimer = self.disclaimer
        check = self.check
        self.assertIn('data-theme="light"', check)
        self.assertIn('content="#f7f4ee"', check)
        self.assertIn('data-theme="light"', disclaimer)
        self.assertIn('content="#f7f4ee"', disclaimer)
        self.assertNotIn('content="#030609"', disclaimer)
        self.assertIn('href="vsn"', disclaimer)
        self.assertNotIn("VSN", disclaimer)
