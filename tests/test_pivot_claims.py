from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AgentActionGatingPivotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pages = {
            path.name: path.read_text(encoding="utf-8")
            for path in sorted(ROOT.glob("*.html"))
        }
        cls.all_copy = "\n".join(cls.pages.values())

    def test_pilot_page_exists_and_is_linked_from_every_page(self) -> None:
        self.assertIn("pilot.html", self.pages)
        for name, html in self.pages.items():
            with self.subTest(page=name):
                self.assertIn('href="pilot.html"', html)

    def test_public_export_has_canonical_discovery_metadata(self) -> None:
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("Sitemap: https://signet7.io/sitemap.xml", robots)
        for name, html in self.pages.items():
            with self.subTest(page=name):
                canonical = "https://signet7.io/" if name == "index.html" else f"https://signet7.io/{name}"
                self.assertIn(f'<link rel="canonical" href="{canonical}">', html)
                self.assertIn(f'<meta property="og:url" content="{canonical}">', html)
                if name in {"terms.html", "disclaimer.html"}:
                    self.assertIn('<meta name="robots" content="noindex, nofollow">', html)
                    self.assertNotIn(f"<loc>{canonical}</loc>", sitemap)
                else:
                    self.assertIn(f"<loc>{canonical}</loc>", sitemap)

    def test_legal_drafts_exist_and_are_linked_once_from_every_page(self) -> None:
        for target in ("terms.html", "disclaimer.html"):
            self.assertIn(target, self.pages)
            for name, html in self.pages.items():
                with self.subTest(page=name, target=target):
                    self.assertIn(f'href="{target}"', html)
        self.assertEqual(self.pages["terms.html"].count("DRAFT — NON-OPERATIVE"), 1)
        self.assertEqual(self.pages["disclaimer.html"].count("DRAFT — NON-OPERATIVE"), 1)

    def test_front_door_owns_agent_action_gating(self) -> None:
        home = self.pages["index.html"].lower()
        for phrase in (
            "cryptographic agent-action gating",
            "gate what the agent does.",
            "not just what lands in the inbox.",
            "inbox security stops at delivery.",
            "signed instruction",
            "exact proposed action",
            "policy decision",
            "caller enforcement",
            "managed vsn planned",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, home)

    def test_current_product_truth_is_bounded_to_implemented_contract(self) -> None:
        product = self.pages["product.html"]
        for phrase in (
            "Action-bound signatures",
            "Fail-closed unknown actions",
            "no separate inbound/outbound",
            "EXECUTEWIRE",
            "PURCHASE",
            "REFUND",
            "TRANSFER",
            "HTTP and MCP decision surfaces",
            "s7-email-1",
            "text and HTML alternatives",
            "attachment bytes plus declared metadata",
            "caller refuses or performs",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, product)

    def test_trust_page_separates_identity_evidence_and_compliance(self) -> None:
        trust = self.pages["trust.html"]
        for phrase in (
            "Signature-bound sender identity",
            "Self-signed",
            "Unresolved",
            "does not block every phishing technique",
            "Evidence support is not certification",
            "No universal legal duration or seven-year default",
            "The planned managed trust layer",
            "Verified is not safe. Unresolved is not fraudulent.",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, trust)

    def test_integration_page_keeps_caller_enforcement_explicit(self) -> None:
        integrations = self.pages["integrations.html"]
        for phrase in (
            "API/MCP-first",
            "No replacement mailbox",
            "No traditional SEG",
            "No endpoint agent",
            "Integration still required",
            "Caller enforces",
            "treating the response as advisory while executing anyway defeats the control",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, integrations)

    def test_program_page_retires_old_public_prices(self) -> None:
        programs = self.pages["programs.html"]
        for phrase in (
            "Price the governed decision. Not the inbox.",
            "Per-agent / decision-band direction",
            "Exact prices not approved",
            "No live offer",
            "Inactive legacy catalog",
            "no longer the controlling public model",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, programs)
        for stale_price in ("$12/month", "$29/month", "$99/month", "$1,000/month"):
            self.assertNotIn(stale_price, programs)

    def test_pilot_is_bounded_and_not_a_production_offer(self) -> None:
        pilot = self.pages["pilot.html"]
        for phrase in (
            "Founding Design Partner Evaluation",
            "four-week",
            "No automatic paid conversion",
            "not a production service",
            "Synthetic or lower-risk actions first",
            "A named agent, named caller, exact action vocabulary",
            "Exact pivot pricing is not approved",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, pilot)
        self.assertNotRegex(pilot, r"<form\b")
        self.assertEqual(re.findall(r"\$\s*\d+", pilot), ["$0"])

    def test_every_page_keeps_local_candidate_boundary(self) -> None:
        for name, html in self.pages.items():
            with self.subTest(page=name):
                self.assertIn("local candidate", html.lower())

    def test_public_copy_does_not_overclaim(self) -> None:
        visible = re.sub(r"<[^>]+>", " ", self.all_copy).lower()
        forbidden = (
            r"signet7\s+(?:prevents|blocks|stops)\s+(?:phishing|fraud|scams|malware|ransomware)",
            r"signet7\s+makes\s+(?:email|messages?|actions?)\s+safe",
            r"verified\s+means\s+safe",
            r"unverified\s+means\s+fraud",
            r"hipaa compliant email",
            r"seven-year retention by default",
            r"no integration required",
        )
        for pattern in forbidden:
            with self.subTest(pattern=pattern):
                self.assertIsNone(re.search(pattern, visible))


if __name__ == "__main__":
    unittest.main()