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

    def test_program_page_spans_free_verification_through_enterprise_without_amounts(self) -> None:
        programs = self.pages["programs.html"]
        for phrase in (
            "Verify Free",
            "Individual",
            "Professional",
            "Business",
            "Enterprise",
            "No live checkout or approved public amount",
            "Recipient verification stays free",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, programs)
        self.assertNotRegex(programs, r"\$\s*\d+")
        self.assertNotIn("subscribe now", programs.lower())

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
        self.assertNotRegex(pilot, r"\$\s*\d+")

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
