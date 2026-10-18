"""Mac Gatekeeper first-open guidance on the public download and help pages."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class MacFirstOpenDocsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.download = (ROOT / "download.html").read_text(encoding="utf-8")
        cls.docs = (ROOT / "docs.html").read_text(encoding="utf-8")
        cls.faq = (ROOT / "faq.html").read_text(encoding="utf-8")

    def test_download_has_mac_first_open_section(self) -> None:
        html = self.download
        self.assertIn('id="mac-first-open"', html)
        self.assertIn("Opening Signet7 on a Mac (first time)", html)
        self.assertIn("Open Anyway", html)
        self.assertIn("xattr -dr com.apple.quarantine", html)
        self.assertIn("/Applications/Signet7.app", html)
        self.assertIn("Connect to Signet7", html)
        self.assertIn("Sequoia", html)
        self.assertIn("support.apple.com/guide/mac-help/open-a-mac-app-from-an-unknown-developer-mh40616", html)

    def test_mac_download_links_to_section(self) -> None:
        html = self.download
        self.assertIn('data-os="macos"', html)
        mac_start = html.index('data-os="macos"')
        mac_card = html[mac_start : mac_start + 1200]
        self.assertIn('href="#mac-first-open"', mac_card)
        self.assertIn("First time on a Mac?", mac_card)

    def test_docs_and_faq_point_at_download_anchor(self) -> None:
        self.assertIn('href="download#mac-first-open"', self.docs)
        self.assertIn('href="download#mac-first-open"', self.faq)


if __name__ == "__main__":
    unittest.main()
