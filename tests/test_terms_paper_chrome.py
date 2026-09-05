from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TermsPaperChromeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.terms = (ROOT / "terms.html").read_text(encoding="utf-8")
        cls.check = (ROOT / "check.html").read_text(encoding="utf-8")

    def test_terms_page_uses_check_paper_chrome(self) -> None:
        """Terms uses the same paper browser chrome as the live check brochure."""
        terms = self.terms
        check = self.check
        self.assertIn('data-theme="light"', check)
        self.assertIn('content="#f7f4ee"', check)
        self.assertIn('data-theme="light"', terms)
        self.assertIn('content="#f7f4ee"', terms)
        self.assertNotIn('content="#030609"', terms)
        self.assertIn('href="vsn"', terms)
        self.assertNotIn("VSN", terms)
