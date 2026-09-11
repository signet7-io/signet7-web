from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

INNER = (
    "about.html",
    "docs.html",
    "terms.html",
    "privacy.html",
    "ai.html",
    "cancel.html",
    "disclaimer.html",
    "pilot.html",
    "providers.html",
    "safety.html",
)

PAPER = INNER + (
    "product.html",
    "programs.html",
    "integrations.html",
    "trust.html",
)


class InnerPagesPaperChromeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.check = (ROOT / "check.html").read_text(encoding="utf-8")
        cls.home = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.pages = {name: (ROOT / name).read_text(encoding="utf-8") for name in PAPER}

    def test_check_and_home_keep_paper_chrome(self) -> None:
        self.assertIn('data-theme="light"', self.check)
        self.assertIn('content="#f7f4ee"', self.check)
        self.assertIn("High-stakes email, finally", self.home)
        self.assertIn("provable", self.home)
        self.assertIn('content="#f7f4ee"', self.home)

    def test_inner_pages_match_check_paper_chrome(self) -> None:
        for name, html in self.pages.items():
            with self.subTest(page=name):
                self.assertIn('data-theme="light"', html)
                self.assertIn('content="#f7f4ee"', html)
                self.assertNotIn('content="#030609"', html)
                self.assertIn('href="vsn"', html)
                self.assertNotIn("How it works", html)

    def test_prior_inner_pages_do_not_name_vsn(self) -> None:
        for name in INNER:
            html = self.pages[name]
            with self.subTest(page=name):
                self.assertNotIn("VSN", html)
