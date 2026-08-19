from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LawsuitRiskPages(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pages = {path.name: path.read_text(encoding="utf-8") for path in ROOT.glob("*.html")}

    def test_ten_item_pages_exist_and_are_linked(self) -> None:
        for target in ("privacy.html", "ai.html", "providers.html", "cancel.html", "safety.html"):
            self.assertIn(target, self.pages)
            for name, html in self.pages.items():
                with self.subTest(page=name, target=target):
                    self.assertIn(f'href="{target}"', html)

    def test_privacy_is_a_filled_policy(self) -> None:
        privacy = self.pages["privacy.html"]
        self.assertIn("Privacy Policy", privacy)
        self.assertIn("Data we collect", privacy)
        self.assertIn("raw email", privacy.lower())
        self.assertIn("justin.daines@signet7.io", privacy)
        self.assertIn("We do not sell personal data", privacy)
        self.assertEqual(privacy.count("DRAFT — NON-OPERATIVE"), 1)
        self.assertNotIn("Not a final privacy policy", privacy)
        self.assertNotIn("[DECISION]", privacy)

    def test_ai_page_does_not_invent_a_chatbot(self) -> None:
        ai = self.pages["ai.html"].lower()
        self.assertIn("artificial intelligence", ai)
        self.assertIn("not a generative chatbot", ai)
        self.assertNotIn("chatgpt", ai)

    def test_providers_page_names_hosts(self) -> None:
        providers = self.pages["providers.html"]
        self.assertIn("GitHub Pages", providers)
        self.assertIn("Stripe", providers)
        self.assertIn("not a live subprocessor", providers.lower())

    def test_cancel_page_is_first_party_and_has_no_trial_trap(self) -> None:
        cancel = self.pages["cancel.html"].lower()
        self.assertIn("cancel is one request", cancel)
        self.assertIn("zero trial days", cancel)
        self.assertIn("does not auto-convert", cancel)

    def test_safety_page_points_to_988(self) -> None:
        safety = self.pages["safety.html"]
        self.assertIn("988", safety)
        self.assertIn("https://988lifeline.org/", safety)

    def test_no_fake_testimonials_on_the_public_site(self) -> None:
        combined = "\n".join(self.pages.values()).lower()
        self.assertNotIn("what our customers say", combined)
        self.assertNotIn("five stars", combined)
        self.assertNotIn('"acme corp"', combined)


if __name__ == "__main__":
    unittest.main()
