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
        self.assertIn('data-theme="dark"', self.check)
        self.assertIn('content="#05080d"', self.check)
        self.assertIn("Check an important email before you act", self.home)
        self.assertIn("before you act", self.home)
        self.assertIn('content="#05080d"', self.home)

    def test_inner_pages_match_check_paper_chrome(self) -> None:
        for name, html in self.pages.items():
            with self.subTest(page=name):
                self.assertIn('data-theme="dark"', html)
                self.assertIn('content="#05080d"', html)
                self.assertNotIn('content="#030609"', html)
                self.assertIn('href="vsn"', html)
                self.assertNotIn("How it works", html)

    def test_prior_inner_pages_do_not_name_vsn(self) -> None:
        for name in INNER:
            html = self.pages[name]
            with self.subTest(page=name):
                self.assertNotIn("VSN", html)

    def test_product_and_programs_do_not_name_vsn(self) -> None:
        product = self.pages["product.html"]
        programs = self.pages["programs.html"]
        for name, html in (("product.html", product), ("programs.html", programs)):
            with self.subTest(page=name):
                self.assertNotIn("VSN", html)
                self.assertIn('href="vsn"', html)
                self.assertIn("Check an important email before you act", self.home)
                self.assertNotIn("Qual", html)
        self.assertIn("Listing lookup is", product)
        self.assertNotIn("VSN lookup", product)
        self.assertIn("https://verify.signet7.io/vsn", product)
        self.assertIn("Each of those emails gets its own listing.", programs)
        self.assertNotIn("VSN identity", programs)

    def test_watch_and_download_do_not_name_vsn(self) -> None:
        watch = (ROOT / "watch.html").read_text(encoding="utf-8")
        download = (ROOT / "download.html").read_text(encoding="utf-8")
        for name, html in (("watch.html", watch), ("download.html", download)):
            with self.subTest(page=name):
                self.assertNotIn("VSN", html)
                self.assertIn('href="vsn"', html)
                self.assertIn("Check an important email before you act", self.home)
                self.assertNotIn("Qual", html)
                self.assertIn("Each of those emails gets its own listing.", html)
                self.assertNotIn("VSN identity", html)
