from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class FaqWordsMatchNotSafeQuestionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.faq = (ROOT / "faq.html").read_text(encoding="utf-8")

    def test_faq_does_not_ask_if_words_match_is_safe(self) -> None:
        faq = self.faq
        self.assertNotIn("is it safe?", faq.lower())
        self.assertNotIn("If the words match, is it safe?", faq)

    def test_faq_says_what_words_match_means(self) -> None:
        faq = self.faq
        self.assertIn("What does words match mean?", faq)
        self.assertIn("The protected words still match the seal.", faq)
        self.assertIn("does not approve payment", faq)

    def test_faq_words_match_stays_claim_safe(self) -> None:
        faq = self.faq
        self.assertNotIn("Verified is not safe", faq)
        self.assertNotIn("Unknown is not fraud", faq)
        self.assertNotIn("You still decide", faq)
        self.assertNotIn("Listed is not trusted", faq)
        self.assertNotIn("is safe to pay", faq)
        self.assertNotIn("VSN", faq)
        self.assertNotIn("Qual", faq)
