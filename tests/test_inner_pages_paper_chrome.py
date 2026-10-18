from __future__ import annotations

import unittest

from tests.site_html import brochure_html_pages


class InnerPagesPaperChromeTests(unittest.TestCase):
    def test_brochure_pages_stay_dark(self) -> None:
        for path in brochure_html_pages():
            html = path.read_text(encoding="utf-8")
            with self.subTest(page=path.name):
                self.assertIn('data-theme="dark"', html)
                self.assertIn('content="#050', html)
