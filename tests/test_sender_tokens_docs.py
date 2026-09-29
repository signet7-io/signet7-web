from __future__ import annotations

import unittest

from tests.site_html import ROOT


class SenderTokensDocsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.docs = (ROOT / "docs.html").read_text(encoding="utf-8")

    def test_section_and_nav(self) -> None:
        self.assertIn('id="manage-sender-tokens"', self.docs)
        self.assertIn('href="#manage-sender-tokens"', self.docs)

    def test_locked_product_copy(self) -> None:
        docs = self.docs
        self.assertIn("Account owner only", docs)
        self.assertIn("By default up to five sender tokens are allowed per account.", docs)
        self.assertIn("emails the raw token <strong>once</strong>", docs)
        self.assertIn("never displays the full token again", docs)
        self.assertIn("Signet7 Outlook pane", docs)
        self.assertIn("Signet7 Token</strong> field", docs)
        self.assertIn("stops <strong>immediately</strong>", docs)
        self.assertIn("<strong>seven days</strong>", docs)
        self.assertIn("support@signet7.io", docs)
        self.assertIn("created, marked for deactivation, and deleted", docs)
