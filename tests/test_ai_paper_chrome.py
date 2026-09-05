from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AiPaperChromeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ai = (ROOT / "ai.html").read_text(encoding="utf-8")
        cls.check = (ROOT / "check.html").read_text(encoding="utf-8")

    def test_ai_page_uses_check_paper_chrome(self) -> None:
        """AI use uses the same paper browser chrome as the live check brochure."""
        ai = self.ai
        check = self.check
        self.assertIn('data-theme="light"', check)
        self.assertIn('content="#f7f4ee"', check)
        self.assertIn('data-theme="light"', ai)
        self.assertIn('content="#f7f4ee"', ai)
        self.assertNotIn('content="#030609"', ai)
        self.assertIn('href="vsn"', ai)
        self.assertNotIn("VSN", ai)
