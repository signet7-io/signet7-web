from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ProvidersPaperChromeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.providers = (ROOT / "providers.html").read_text(encoding="utf-8")
        cls.check = (ROOT / "check.html").read_text(encoding="utf-8")

    def test_providers_page_uses_check_paper_chrome(self) -> None:
        """Providers uses the same paper browser chrome as the live check brochure."""
        providers = self.providers
        check = self.check
        self.assertIn('data-theme="light"', check)
        self.assertIn('content="#f7f4ee"', check)
        self.assertIn('data-theme="light"', providers)
        self.assertIn('content="#f7f4ee"', providers)
        self.assertNotIn('content="#030609"', providers)
        self.assertIn('href="vsn"', providers)
        self.assertNotIn("VSN", providers)
