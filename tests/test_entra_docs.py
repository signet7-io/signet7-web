from __future__ import annotations

import unittest

from tests.site_html import ROOT


class EntraDocsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.docs = (ROOT / "docs.html").read_text(encoding="utf-8")

    def test_entra_and_seal_where_sections_exist(self) -> None:
        for section_id in ("entra", "entra-push", "entra-troubleshoot", "seal-where"):
            with self.subTest(section_id=section_id):
                self.assertIn(f'id="{section_id}"', self.docs)

    def test_entra_docs_stay_off_appsource_and_admin_hosts(self) -> None:
        docs = self.docs
        self.assertIn("aka.ms/olksideload", docs)
        self.assertNotIn("Settings → Add-ins → My add-ins", docs)
        self.assertNotIn("listed on AppSource", docs)
        self.assertNotIn("pip install", docs)
        self.assertNotIn("admin.signet7.io", docs)
        outlook = (ROOT / "outlook" / "index.html").read_text(encoding="utf-8")
        self.assertIn("Not AppSource", outlook)

    def test_figures_exist(self) -> None:
        self.assertTrue((ROOT / "assets" / "docs-entra-flow.png").is_file())
        self.assertTrue((ROOT / "assets" / "docs-entra-permissions.png").is_file())
