from __future__ import annotations

import unittest

from tests.site_html import ROOT


class EntraDocsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.docs = (ROOT / "docs.html").read_text(encoding="utf-8")
        cls.it = (ROOT / "download.html").read_text(encoding="utf-8")
        cls.check = (ROOT / "check.html").read_text(encoding="utf-8")
        cls.smtp = (ROOT / "docs.html").read_text(encoding="utf-8")
        cls.outlook = (ROOT / "outlook" / "index.html").read_text(encoding="utf-8")
        cls.integrations = (ROOT / "download.html").read_text(encoding="utf-8")

    def test_entra_sections_and_nav(self) -> None:
        for section_id in (
            "entra",
            "entra-install",
            "entra-push",
            "entra-troubleshoot",
            "entra-integrations",
            "seal-where",
        ):
            self.assertIn(f'id="{section_id}"', self.docs)
            self.assertIn(f'href="#{section_id}"', self.docs)

    def test_path_b_steps_and_honesty(self) -> None:
        docs = self.docs
        self.assertIn("SIGNET7_GRAPH_CLIENT_ID", docs)
        self.assertIn("--login-entra", docs)
        self.assertIn("--check-entra", docs)
        self.assertIn("Mail.Read", docs)
        self.assertIn("Mail.Send", docs)
        self.assertIn("Seal this draft", docs)
        self.assertIn("Sign and send email", docs)
        self.assertIn("Signet7-sealed.eml", docs)
        self.assertIn("The email itself is sealed", docs)
        self.assertIn("Where the seal lives", docs)
        self.assertIn("Where each product lives", docs)
        self.assertIn("Signet7 Outlook pane", docs)
        self.assertIn("signet7.io/outlook", docs)
        self.assertIn("Outlook on the web (the checked path)", docs)
        self.assertIn("127.0.0.1:2525", docs)
        self.assertIn("Recipients are not required to install", docs)
        self.assertIn("Not Exchange", docs)
        self.assertIn("the <strong>send</strong> button in outlook on the web and the <strong>send</strong> button in outlook desktop are not sealed by the backend watcher", docs.lower())
        self.assertIn("sign and send email needs the sender token", docs.lower())
        self.assertIn("paid outlook sealing is the business program", docs.lower())
        self.assertIn("email signing is not provisioned", docs.lower())
        self.assertIn("s7-", docs)
        self.assertIn("tenant_ids", docs)
        self.assertIn("accounts.sqlite3", docs.lower())
        self.assertIn("Entra does not sign mail", docs)
        self.assertIn("IMAP still works", docs)
        self.assertIn("SIGNET7_MAX_WATCHED_INBOXES", docs)
        self.assertIn("signed order form", docs)
        self.assertIn("docs#entra", self.it)
        self.assertIn("docs#entra-push", self.it)
        self.assertIn("Integrated apps", docs)
        self.assertIn("Do not push Signet7 desktop to every laptop", docs)
        self.assertIn("You are IT", docs)
        self.assertIn("IT pushes the add-in. Not the desktop.", docs)
        self.assertNotIn("It does not seal outgoing mail", docs)
        self.assertIn("admin.microsoft.com", docs)
        self.assertIn("Do not push Signet7 desktop to every laptop", self.it)
        self.assertNotIn("install on the Entra server", docs)
        self.assertNotIn("FedRAMP", docs)
        self.assertIn("Not AppSource", docs)
        self.assertIn("aka.ms/olksideload", docs)
        self.assertIn("The new Apps store cannot upload XML", docs)
        self.assertNotIn("Settings → Add-ins → My add-ins", docs)
        self.assertNotIn("listed on AppSource", docs)
        self.assertIn("GCC High is not this path", docs)
        self.assertNotIn("pip install", docs)
        self.assertNotIn("admin.signet7.io", docs)
        self.assertNotIn(">VSN<", docs)

    def test_section_order(self) -> None:
        docs = self.docs
        self.assertLess(docs.find('id="gmail-gcp"'), docs.find('id="entra"'))
        self.assertLess(docs.find('id="entra"'), docs.find('id="entra-install"'))
        self.assertLess(docs.find('id="entra-install"'), docs.find('id="entra-push"'))
        self.assertLess(docs.find('id="entra-push"'), docs.find('id="entra-troubleshoot"'))
        self.assertLess(docs.find('id="entra-troubleshoot"'), docs.find('id="entra-integrations"'))
        self.assertLess(docs.find('id="entra-integrations"'), docs.find('id="desktop"'))
        self.assertLess(docs.find('id="outlook"'), docs.find('id="seal-where"'))
        self.assertLess(docs.find('id="seal-where"'), docs.find('id="signup"'))

    def test_figures_exist(self) -> None:
        self.assertIn("docs-entra-flow.png", self.docs)
        self.assertIn("docs-entra-permissions.png", self.docs)
        self.assertTrue((ROOT / "assets" / "docs-entra-flow.png").is_file())
        self.assertTrue((ROOT / "assets" / "docs-entra-permissions.png").is_file())

    def test_seal_where_table_and_satellite_pages(self) -> None:
        docs = self.docs
        self.assertIn('id="seal-where"', docs)
        self.assertIn('aria-label="Where the Signet7 seal lives"', docs)
        self.assertIn("How the sender seals", docs)
        self.assertIn("What the recipient gets", docs)
        self.assertIn("What to drop on the live check", docs)
        self.assertIn('aria-label="Where each Signet7 product lives"', docs)
        self.assertIn("Product", docs)
        self.assertIn("Where it lives", docs)
        self.assertIn("Where you open it", docs)
        self.assertIn("the email gmail or outlook saves is the unsigned carrier", docs.lower())
        self.assertIn("the <strong>send</strong> button in outlook on the web does not attach", docs.lower())
        self.assertIn("the <strong>send</strong> button in outlook desktop does not attach", docs.lower())
        self.assertIn("the <strong>send</strong> button in outlook on the web, or the <strong>send</strong> button in outlook desktop", docs.lower())
        self.assertIn("Signet7-sealed.eml", self.check)
        self.assertIn("docs#seal-where", self.check)
        self.assertIn("The email itself is sealed", self.smtp)
        self.assertIn("Signet7-sealed.eml", self.smtp)
        self.assertIn("Sign and send email", self.outlook)
        self.assertIn("Signet7-sealed.eml", self.outlook)
        self.assertIn("Signet7-sealed.eml", self.it)
        self.assertIn("docs#seal-where", self.it)
        self.assertIn("Signet7-sealed.eml", self.integrations)
        self.assertIn("That hop seals the email itself", self.integrations)
