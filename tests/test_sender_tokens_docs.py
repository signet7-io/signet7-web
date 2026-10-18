from __future__ import annotations

import unittest

from tests.site_html import ROOT


class SenderTokensDocsTests(unittest.TestCase):
    def test_section_and_nav(self) -> None:
        docs = (ROOT / "docs.html").read_text(encoding="utf-8")
        self.assertIn('id="manage-sender-tokens"', docs)
        self.assertIn("five sender tokens", docs.lower())
        self.assertIn("seven days", docs.lower())
