from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SafetyPaperChromeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.safety = (ROOT / "safety.html").read_text(encoding="utf-8")
        cls.check = (ROOT / "check.html").read_text(encoding="utf-8")

    def test_safety_page_uses_check_paper_chrome(self) -> None:
        """Safety uses the same paper browser chrome as the live check brochure."""
        safety = self.safety
        check = self.check
        self.assertIn('data-theme="light"', check)
        self.assertIn('content="#f7f4ee"', check)
        self.assertIn('data-theme="light"', safety)
        self.assertIn('content="#f7f4ee"', safety)
        self.assertNotIn('content="#030609"', safety)
        self.assertIn('href="vsn"', safety)
        self.assertNotIn("VSN", safety)
