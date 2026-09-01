from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class FaqWhoCanReadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.faq = (ROOT / "faq.html").read_text(encoding="utf-8")

    def test_faq_answers_who_can_read_a_check(self) -> None:
        faq = self.faq
        self.assertIn('id="who-can-read"', faq)
        self.assertIn("Who can read a check?", faq)
        self.assertIn("Only you see this check in your browser.", faq)
        self.assertIn("Signet7 does not keep the letter for others to look up.", faq)
        self.assertIn("A short status link, if one exists, is not the letter.", faq)
        self.assertIn("Company Watch status needs a company login.", faq)
        self.assertIn("Staff tools are a different door.", faq)

    def test_faq_who_copy_stays_claim_safe(self) -> None:
        faq = self.faq
        self.assertNotIn("VSN", faq)
        self.assertNotIn("Qual", faq)
        self.assertNotIn("is safe to pay", faq)
        self.assertNotIn("you’re safe", faq)
        self.assertNotIn("you're safe", faq)
