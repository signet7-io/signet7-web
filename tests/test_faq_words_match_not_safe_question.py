from __future__ import annotations

import unittest

from tests.site_html import ROOT


class FaqResultQuestionTests(unittest.TestCase):
    def test_faq_explains_the_unchanged_result_without_calling_it_safe(self) -> None:
        faq = (ROOT / "faq.html").read_text(encoding="utf-8")
        self.assertIn("What does Unchanged since sealed mean?", faq)
        self.assertIn("does not approve payment", faq)
        self.assertNotIn("is it safe?", faq.lower())
