from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CancelPaperChromeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cancel = (ROOT / "cancel.html").read_text(encoding="utf-8")
        cls.check = (ROOT / "check.html").read_text(encoding="utf-8")

    def test_cancel_page_uses_check_paper_chrome(self) -> None:
        """Cancel uses the same paper browser chrome as the live check brochure."""
        cancel = self.cancel
        check = self.check
        self.assertIn('data-theme="light"', check)
        self.assertIn('content="#f7f4ee"', check)
        self.assertIn('data-theme="light"', cancel)
        self.assertIn('content="#f7f4ee"', cancel)
        self.assertNotIn('content="#030609"', cancel)
        self.assertIn('href="vsn"', cancel)
        self.assertNotIn("VSN", cancel)
