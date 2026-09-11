from __future__ import annotations

import re
import unittest

from tests.site_html import ROOT


class LayoutLoginDownloadTests(unittest.TestCase):
    """Public zip is not a login gate. Layout must not overflow or miscount."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.download = (ROOT / "download.html").read_text(encoding="utf-8")
        cls.docs = (ROOT / "docs.html").read_text(encoding="utf-8")
        cls.product = (ROOT / "product.html").read_text(encoding="utf-8")
        cls.watch = (ROOT / "watch.html").read_text(encoding="utf-8")
        cls.home = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.css = (ROOT / "assets" / "site.css").read_text(encoding="utf-8")

    def test_download_zips_come_before_optional_unlock_form(self) -> None:
        html = self.download
        self.assertIn('id="watch-files"', html)
        self.assertIn('id="unlock-form"', html)
        self.assertLess(html.index('id="watch-files"'), html.index('id="unlock-form"'))
        self.assertIn("The zip is public.", html)
        self.assertIn("No login for the file.", html)
        self.assertNotIn("Email my unlock code", html)
        self.assertNotIn("$12", html)
        self.assertNotIn("$29", html)
        self.assertNotIn("$99", html)
        self.assertNotIn("Placeholder $", html)

    def test_docs_do_not_require_registration_before_the_zip(self) -> None:
        html = self.docs
        self.assertNotIn("after Registration", html)
        self.assertIn("The zip is public.", html)
        self.assertIn("No login for the file.", html)

    def test_product_desktop_card_sends_people_to_download(self) -> None:
        card = self.product.split('id="watch"', 1)[1].split("</article>", 1)[0]
        self.assertIn('href="download"', card)
        self.assertNotIn('href="watch"', card)

    def test_watch_brochure_says_the_zip_is_public(self) -> None:
        html = self.watch
        self.assertIn("The zip is public.", html)
        self.assertIn("No login for the file.", html)
        actions = html.split('class="hero-actions"', 1)[1].split("</p>", 1)[0]
        self.assertLess(actions.index('href="download"'), actions.index('href="register"'))

    def test_home_feature_heading_matches_three_cards(self) -> None:
        features = self.home.split('id="features"', 1)[1].split("</section>", 1)[0]
        self.assertIn("Three things. That is the product.", features)
        self.assertNotIn("Four things. That is the product.", features)
        self.assertEqual(features.count("<article class=\"feat\">"), 3)

    def test_art_trio_images_are_constrained(self) -> None:
        self.assertIn(".art-trio", self.css)
        self.assertIn(".art-trio img", self.css)
        self.assertRegex(self.css, r"\.art-trio img\s*\{[^}]*max-width:\s*100%")
        self.assertIn("art-trio", self.product)

    def test_live_h1_billboard_is_not_sixteen_ch(self) -> None:
        block = re.search(r"\.nutshell \.billboard\s*\{[^}]+\}", self.css)
        self.assertIsNotNone(block)
        self.assertNotIn("max-width: 16ch", block.group(0))
        self.assertIn("Check an important email before you act.", self.home)


if __name__ == "__main__":
    unittest.main()
