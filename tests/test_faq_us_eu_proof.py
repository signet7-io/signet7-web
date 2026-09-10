from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class FaqUsEuProofTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.faq = (ROOT / "faq.html").read_text(encoding="utf-8")
        cls.docs = (ROOT / "docs.html").read_text(encoding="utf-8")

    def test_faq_says_us_eu_rules_create_demand_not_a_certificate(self) -> None:
        faq = self.faq
        self.assertIn('id="us-eu-proof"', faq)
        self.assertIn("Do US or EU rules make Signet7 a seven-year archive?", faq)
        self.assertIn("Those rules create demand for records you can produce.", faq)
        self.assertIn("They do not require Signet7, certify Signet7, or set a seven-year default here.", faq)
        self.assertIn("A public check does not keep the letter.", faq)

    def test_docs_limits_name_us_eu_demand_without_hedge(self) -> None:
        docs = self.docs
        self.assertIn("US and EU rules create demand for records.", docs)
        self.assertIn("They do not certify Signet7.", docs)
        self.assertNotIn("Verified is not safe", docs)
        self.assertNotIn("Unresolved is not fraudulent", docs)
        self.assertNotIn("you still decide", docs.lower())

    def test_faq_us_eu_copy_stays_claim_safe(self) -> None:
        faq = self.faq
        self.assertNotIn("VSN", faq)
        self.assertNotIn("Verified is not safe", faq)
        self.assertNotIn("You still decide", faq)
        self.assertNotIn("is safe to pay", faq)


if __name__ == "__main__":
    unittest.main()
