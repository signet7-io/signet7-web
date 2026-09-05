from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PilotPaperChromeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pilot = (ROOT / "pilot.html").read_text(encoding="utf-8")
        cls.check = (ROOT / "check.html").read_text(encoding="utf-8")

    def test_pilot_page_uses_check_paper_chrome(self) -> None:
        """Pilot uses the same paper browser chrome as the live check brochure."""
        pilot = self.pilot
        check = self.check
        self.assertIn('data-theme="light"', check)
        self.assertIn('content="#f7f4ee"', check)
        self.assertIn('data-theme="light"', pilot)
        self.assertIn('content="#f7f4ee"', pilot)
        self.assertNotIn('content="#030609"', pilot)
        self.assertIn('href="vsn"', pilot)
        self.assertNotIn("VSN", pilot)
