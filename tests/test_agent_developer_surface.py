from __future__ import annotations

import unittest
from pathlib import Path

from tests.site_html import ROOT

AGENTS = ROOT / "agents.html"
DOCS = ROOT / "docs.html"
LLMS = ROOT / "llms.txt"
LLMS_FULL = ROOT / "llms-full.txt"


class AgentDeveloperSurfaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.agents = AGENTS.read_text(encoding="utf-8")
        cls.docs = DOCS.read_text(encoding="utf-8")
        cls.llms = LLMS.read_text(encoding="utf-8")
        cls.llms_full = LLMS_FULL.read_text(encoding="utf-8")
        cls.home = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.product = (ROOT / "product.html").read_text(encoding="utf-8")

    def test_agents_page_is_linked_from_home_and_product(self) -> None:
        self.assertIn('href="/agents"', self.home)
        self.assertIn('href="agents"', self.product)

    def test_agents_positioning_and_scenario(self) -> None:
        for phrase in (
            "Know which emails came from your people",
            "does not encrypt",
            "signet7-mcp",
            "unsealed",
            "wire transfer",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.agents.lower() if phrase == "unsealed" else self.agents)

    def test_docs_agent_sections_exist(self) -> None:
        for anchor in ("agent-quickstart", "agent-verify-v1", "agent-device-code"):
            with self.subTest(anchor=anchor):
                self.assertIn(f'id="{anchor}"', self.docs)
        self.assertIn("signet7.verify.v1", self.docs)
        self.assertIn("signet7-mcp", self.docs)
        self.assertIn("claude_desktop_config.json", self.docs)
        self.assertIn("/api/v1/account/device/start", self.docs)

    def test_verify_v1_fields_documented(self) -> None:
        for field in (
            '"verdict"',
            "unsealed",
            "tampered",
            "revoked",
            "unknown",
            "agent_label",
            "principal",
            "receipt_id",
            "checked_at",
        ):
            with self.subTest(field=field):
                self.assertIn(field, self.docs)

    def test_llms_files_point_at_agent_docs_and_openapi(self) -> None:
        self.assertIn("https://signet7.io/agents", self.llms)
        self.assertIn("https://signet7.io/docs#agent-quickstart", self.llms)
        self.assertIn("https://verify.signet7.io/openapi.json", self.llms)
        self.assertIn("signet7.verify.v1", self.llms)
        self.assertIn("llms-full.txt", self.llms)
        self.assertIn("PLACEHOLDER:signet7_seal_email", self.llms_full)


if __name__ == "__main__":
    unittest.main()