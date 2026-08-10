from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ConsequentialEmailPivotTests(unittest.TestCase):
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
                canonical = f"https://signet7.io/{name}"
                self.assertIn(f'<link rel="canonical" href="{canonical}">', html)
                self.assertIn(f'<meta property="og:url" content="{canonical}">', html)
                if name in {"terms.html", "disclaimer.html"}:
                    self.assertIn('<meta name="robots" content="noindex, nofollow">', html)
                    self.assertNotIn(f"<loc>{canonical}</loc>", sitemap)
                else:
                    self.assertIn(f"<loc>{canonical}</loc>", sitemap)

    def test_legal_drafts_exist_and_are_linked_from_every_page(self) -> None:
        for target in ("terms.html", "disclaimer.html"):
            with self.subTest(target=target):
                self.assertIn(target, self.pages)
            for name, html in self.pages.items():
                with self.subTest(page=name, target=target):
                    self.assertIn(f'href="{target}"', html)
        self.assertIn("DRAFT — NON-OPERATIVE", self.pages["terms.html"])
        self.assertIn("DRAFT — NON-OPERATIVE", self.pages["disclaimer.html"])

    def test_front_door_owns_consequential_email_for_three_beneficiary_groups(self) -> None:
        home = self.pages["index.html"]
        for phrase in (
            "The trust layer for consequential email",
            "organizations, professionals, and the individuals",
            "Before you act on an important email",
            "Free recipient verification",
            "Invoices and payment instructions",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, home)

    def test_current_product_truth_includes_implemented_email_profile_surfaces(self) -> None:
        product = self.pages["product.html"]
        for phrase in (
            "s7-email-1",
            "protected text and HTML alternatives",
            "Attachment bytes and declared metadata",
            "recipient verifier",
            "Five-program catalog",
            "Browser extension",
            "Gmail add-on",
            "Outlook add-in",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, product)

    def test_program_page_shows_approved_launch_prices_without_live_offer(self) -> None:
        programs = self.pages["programs.html"]
        for phrase in (
            "Verify Free",
            "Individual",
            "Professional",
            "Business",
            "Enterprise",
            "Approved launch prices · no live offer",
            "Recipient verification stays free",
            "$0",
            "$12/month",
            "$29/month",
            "$99/month",
            "From $1,000/month · annual agreement",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, programs)
        self.assertNotIn("subscribe now", programs.lower())
        self.assertIn("No self-serve checkout", programs)

    def test_pilot_is_bounded_and_not_a_commercial_or_production_offer(self) -> None:
        pilot = self.pages["pilot.html"]
        for phrase in (
            "Founding Design Partner Pilot",
            "four-week",
            "No automatic paid conversion",
            "not a production service",
            "simulated or lower-risk communications",
            "what verification does and does not prove",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, pilot)
        self.assertNotRegex(pilot, r"<form\b")
        self.assertEqual(re.findall(r"\$\s*\d+", pilot), ["$0"])
        self.assertIn("bounded, non-renewing, and never converts automatically", pilot)

    def test_every_page_keeps_local_candidate_boundary(self) -> None:
        required = "Local candidate - not a live service"
        for name, html in self.pages.items():
            with self.subTest(page=name):
                self.assertIn(required, html)

    def test_stale_implementation_denials_are_gone(self) -> None:
        stale = (
            "Complete MIME and attachment processing is not implemented",
            "Complete MIME canonicalization and comprehensive attachment coverage are not yet implemented",
            "recipient-facing verification UX remain roadmap work",
            "recipient UX, and the complete managed VSN service remain to be built",
        )
        for phrase in stale:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, self.all_copy)

    def test_public_copy_does_not_overclaim_safety_or_fraud_prevention(self) -> None:
        visible = re.sub(r"<[^>]+>", " ", self.all_copy).lower()
        forbidden = (
            r"signet7\s+(?:prevents|blocks|stops)\s+(?:phishing|fraud|scams)",
            r"signet7\s+makes\s+(?:email|messages?)\s+safe",
            r"verified\s+means\s+safe",
            r"unverified\s+means\s+fraud",
        )
        for pattern in forbidden:
            with self.subTest(pattern=pattern):
                self.assertIsNone(re.search(pattern, visible))


if __name__ == "__main__":
    unittest.main()
