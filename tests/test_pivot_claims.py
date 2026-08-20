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
                self.assertIn('href="pilot"', html)

    def test_public_export_has_canonical_discovery_metadata(self) -> None:
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("Sitemap: https://signet7.io/sitemap.xml", robots)
        for name, html in self.pages.items():
            with self.subTest(page=name):
                canonical = "https://signet7.io/" if name == "index.html" else f"https://signet7.io/{name.removesuffix('.html')}"
                self.assertIn(f'<link rel="canonical" href="{canonical}">', html)
                self.assertIn(f'<meta property="og:url" content="{canonical}">', html)
                if name in {"terms.html", "disclaimer.html", "404.html"}:
                    if name in {"terms.html", "disclaimer.html"}:
                        self.assertIn('<meta name="robots" content="noindex, nofollow">', html)
                    self.assertNotIn(f"<loc>{canonical}</loc>", sitemap)
                else:
                    self.assertIn(f"<loc>{canonical}</loc>", sitemap)

    def test_legal_drafts_exist_and_are_linked_once_from_every_page(self) -> None:
        for target in ("terms", "disclaimer"):
            self.assertIn(f"{target}.html", self.pages)
            for name, html in self.pages.items():
                with self.subTest(page=name, target=target):
                    self.assertIn(f'href="{target}"', html)
        self.assertEqual(self.pages["terms.html"].count("DRAFT — NON-OPERATIVE"), 1)
        self.assertEqual(self.pages["disclaimer.html"].count("DRAFT — NON-OPERATIVE"), 1)

    def test_front_door_owns_consequential_email(self) -> None:
        home = self.pages["index.html"].lower()
        for phrase in (
            "trust layer for consequential email",
            "check the seal before you act.",
            "you already have a product: call the person.",
            "verified does not mean safe",
            "unknown does not mean fraud",
            "vsn check hosted on qual",
            "nobody else puts the whole check together",
            "businesses that move money or change accounts",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, home)
        self.assertNotIn("cryptographic agent-action gating", home)
        self.assertNotIn("gate what the agent does.", home)

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
            "Bind a signing key to a domain. Check whether that binding still holds.",
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
            "Price the sender habit. Keep recipient checks free.",
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
            "Test one payment-instruction email.",
            "Senders with one payment-instruction workflow.",
            "Exact pivot pricing is not approved",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, pilot)
        self.assertNotRegex(pilot, r"<form\b")
        self.assertEqual(re.findall(r"\$\s*\d+", pilot), ["$0"])

    def test_check_page_exists_and_is_honest_about_hosting(self) -> None:
        self.assertIn("check.html", self.pages)
        check = self.pages["check.html"].lower()
        self.assertIn("no install for the other side", check)
        self.assertIn("this static site cannot run that check", check)
        self.assertIn("/email/verify", check)
        self.assertIn("this static site cannot run that check", check)
        self.assertIn('href="check"', self.pages["index.html"])

    def test_scenarios_page_is_living_and_cross_platform(self) -> None:
        self.assertIn("scenarios.html", self.pages)
        page = self.pages["scenarios.html"].lower()
        for phrase in (
            "living document",
            "windows, macos, and linux",
            "not a mail app",
            "small company",
            "corporation",
            "verified is not safe",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, page)
        self.assertIn('href="scenarios"', self.pages["index.html"])

    def test_smtp_recipes_are_cross_platform(self) -> None:
        self.assertIn("smtp.html", self.pages)
        page = self.pages["smtp.html"].lower()
        for phrase in ("127.0.0.1", "2525", "outlook", "apple mail", "thunderbird", "windows, macos, and linux"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, page)

    def test_it_one_pager_exists(self) -> None:
        self.assertIn("it.html", self.pages)
        page = self.pages["it.html"].lower()
        for phrase in ("one mailbox", "pip install signet7", "windows, mac, and linux", "127.0.0.1"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, page)

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

    def test_public_pages_have_no_mascot(self) -> None:
        for name, html in self.pages.items():
            with self.subTest(page=name):
                low = html.lower()
                self.assertNotIn("sidekick", low)
                self.assertNotIn("data-buddy", low)
                self.assertNotIn("meet-buddy", low)
                self.assertNotIn("click me", low)
        motion = (ROOT / "assets" / "motion.js").read_text(encoding="utf-8").lower()
        css = (ROOT / "assets" / "site.css").read_text(encoding="utf-8").lower()
        for blob in (motion, css):
            self.assertNotIn("data-buddy", blob)
            self.assertNotIn("sidekick", blob)
            self.assertNotIn("buddy-hit", blob)

    def test_homepage_is_a_customer_front_door(self) -> None:
        home = self.pages["index.html"]
        low = home.lower()
        self.assertIn("data-quest", home)
        self.assertIn('class="scale"', home)
        self.assertIn(">Agree</span>", home)
        self.assertIn("<strong>3</strong>", home)
        self.assertIn("<strong>5</strong>", home)
        self.assertIn("<strong>1</strong>", home)
        self.assertIn("<strong>0</strong>", home)
        self.assertNotRegex(home, r"<form\b")
        self.assertNotIn("dual-control", low)
        self.assertNotIn("isolated qualification", low)
        self.assertNotIn("api/mcp-first", low)
        self.assertNotIn("executewire", low)


class ContentSecurityPolicy(unittest.TestCase):
    """GitHub Pages cannot set response headers, so the policy ships in the markup.

    frame-ancestors is ignored when delivered via <meta>; it is declared here so the
    policy is correct the moment the domain moves behind a header-capable layer, which
    must happen before any verification surface is hosted on signet7.io.
    """

    def setUp(self) -> None:
        self.pages = {
            path.name: path.read_text(encoding="utf-8") for path in sorted(ROOT.glob("*.html"))
        }

    def test_every_page_declares_the_restrictive_policy(self) -> None:
        self.assertTrue(self.pages)
        for name, html in self.pages.items():
            with self.subTest(page=name):
                self.assertIn('<meta http-equiv="Content-Security-Policy"', html)
                for directive in (
                    "default-src 'self'",
                    "object-src 'none'",
                    "base-uri 'none'",
                    "frame-ancestors 'none'",
                    "upgrade-insecure-requests",
                ):
                    self.assertIn(directive, html)
                self.assertIn('<meta name="referrer" content="strict-origin-when-cross-origin">', html)
                self.assertIn('<meta http-equiv="X-Content-Type-Options" content="nosniff">', html)

    def test_no_inline_script_or_style_can_silently_rely_on_an_exemption(self) -> None:
        """Self-hosted motion scripts are allowed. Inline script/style is not."""
        for name, html in self.pages.items():
            with self.subTest(page=name):
                self.assertNotIn("unsafe-inline", html)
                self.assertNotIn("<style", html)
                self.assertNotIn('style="', html)
                for match in re.finditer(r"<script([^>]*)>(.*?)</script>", html, flags=re.I | re.S):
                    attrs, body = match.group(1), match.group(2)
                    self.assertIn('src="assets/', attrs)
                    self.assertNotIn("http:", attrs.lower())
                    self.assertEqual(body.strip(), "")

if __name__ == "__main__":
    unittest.main()
