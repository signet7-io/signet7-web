from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DocsPaperChromeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.docs = (ROOT / "docs.html").read_text(encoding="utf-8")
        cls.check = (ROOT / "check.html").read_text(encoding="utf-8")

    def test_docs_page_uses_check_paper_chrome(self) -> None:
        """Docs uses the same paper browser chrome as the live check brochure."""
        docs = self.docs
        check = self.check
        self.assertIn('data-theme="light"', check)
        self.assertIn('content="#f7f4ee"', check)
        self.assertIn('data-theme="light"', docs)
        self.assertIn('content="#f7f4ee"', docs)
        self.assertNotIn('content="#030609"', docs)
        self.assertIn('href="vsn"', docs)
