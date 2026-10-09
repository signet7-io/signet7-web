from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class FaqUsEuProofTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.faq = (ROOT / "faq.html").read_text(encoding="utf-8")
        cls.docs = (ROOT / "docs.html").read_text(encoding="utf-8")

    def test_faq_has_the_us_eu_proof_entry(self) -> None:
        self.assertIn('id="us-eu-proof"', self.faq)

    def test_docs_limits_name_us_eu_demand(self) -> None:
        self.assertIn("US and EU rules create demand for records", self.docs)
        self.assertIn("they do not certify signet7", self.docs.lower())


if __name__ == "__main__":
    unittest.main()
