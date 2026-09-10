"""Lock the last live dark Pages tree (7898012104400db6ad9ff9aa97da92f5c109caa7)."""

from __future__ import annotations

import unittest

from tests.site_html import ROOT, root_html_pages


class DarkLivePagesTests(unittest.TestCase):
    def test_theme_js_forces_dark(self) -> None:
        js = (ROOT / "assets" / "theme.js").read_text(encoding="utf-8")
        self.assertIn('setAttribute("data-theme", "dark")', js)
        self.assertIn("colorScheme = \"dark\"", js)
        self.assertNotIn('setAttribute("data-theme", "light")', js)

    def test_public_pages_declare_dark_theme(self) -> None:
        for path in root_html_pages():
            html = path.read_text(encoding="utf-8")
            with self.subTest(page=path.name):
                self.assertIn('data-theme="dark"', html)
                self.assertNotIn('data-theme="light"', html)
                self.assertNotIn("#f7f4ee", html)

    def test_homepage_keeps_cinematic_dark_door(self) -> None:
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "assets" / "site.css").read_text(encoding="utf-8")
        self.assertIn('class="scroll-progress"', home)
        self.assertIn("people-scene", home)
        self.assertIn("people-dark.png", home)
        self.assertIn("assets/motion.js", home)
        self.assertIn("High-stakes email, finally", home)
        self.assertNotIn("Check the seal before you pay", home)
        self.assertNotIn("zoom/01.jpg", home)
        self.assertNotIn("air-zoom.js", home)
        self.assertIn('html[data-theme="dark"]', css)
        self.assertIn("--page: #071018;", css)
        self.assertNotIn("#f7f4ee", css)

    def test_search_verification_files_remain(self) -> None:
        key = "31c6ab5cca284146bb0b26bd193d25e2"
        self.assertEqual((ROOT / f"{key}.txt").read_text(encoding="utf-8").strip(), key)
        self.assertEqual(
            (ROOT / "googled2cf3c6d0c5a81c5.html").read_text(encoding="utf-8").strip(),
            "google-site-verification: googled2cf3c6d0c5a81c5.html",
        )


if __name__ == "__main__":
    unittest.main()
