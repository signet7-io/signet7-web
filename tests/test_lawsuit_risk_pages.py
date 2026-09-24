from __future__ import annotations

import unittest

from tests.site_html import ROOT, root_html_pages


class LawsuitRiskPages(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pages = {path.name: path.read_text(encoding="utf-8") for path in root_html_pages()}

    def test_ten_item_pages_exist_and_are_linked(self) -> None:
        for target in ("privacy", "ai", "providers", "cancel", "safety"):
            self.assertIn(f"{target}.html", self.pages)
            for name, html in self.pages.items():
                with self.subTest(page=name, target=target):
                    self.assertIn(f'href="{target}"', html)

    def test_privacy_is_a_filled_policy(self) -> None:
        privacy = self.pages["privacy.html"]
        self.assertIn("Privacy Policy", privacy)
        self.assertIn("Data we collect", privacy)
        self.assertIn("raw email", privacy.lower())
        self.assertIn("samuel.sanderson@signet7.io", privacy)
        self.assertNotIn("justin.daines@signet7.io", privacy)
        self.assertNotIn("Justin D. Daines", privacy)
        self.assertIn("We do not sell personal data", privacy)
        self.assertEqual(privacy.count("DRAFT — NON-OPERATIVE"), 1)
        self.assertNotIn("Not a final privacy policy", privacy)
        self.assertNotIn("[DECISION]", privacy)

    def test_public_pages_do_not_name_private_team_contacts(self) -> None:
        combined = "\n".join(self.pages.values())
        self.assertNotIn("Justin D. Daines", combined)
        self.assertNotIn("justin.daines@signet7.io", combined)
        self.assertNotIn("george@eaglevisionseo.com", combined)
        about = self.pages["about.html"]
        self.assertIn("George T. Terris II", about)
        self.assertNotIn("Justin", about)

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

    def test_privacy_says_no_tracking_cookies_and_no_banner(self) -> None:
        privacy = self.pages["privacy.html"]
        self.assertIn("does not set tracking or advertising cookies", privacy)
        self.assertIn("no cookie consent banner", privacy)
        self.assertEqual(privacy.count("DRAFT — NON-OPERATIVE"), 1)
        combined = "\n".join(self.pages.values()).lower()
        self.assertNotIn("googletagmanager", combined)
        self.assertNotIn("gtag(", combined)
        self.assertNotIn('id="cookie-banner"', combined)

    def test_feedback_send_states_what_is_posted(self) -> None:
        feedback = self.pages["feedback.html"]
        self.assertIn("posts this note to Signet7 so we can read it", feedback)
        self.assertIn("used only to answer you", feedback)
        self.assertIn('href="privacy"', feedback)

    def test_self_hosted_fonts_keep_their_license(self) -> None:
        fonts = ROOT / "assets" / "fonts"
        outfit = (fonts / "OFL-Outfit.txt").read_text(encoding="utf-8")
        serif = (fonts / "OFL-InstrumentSerif.txt").read_text(encoding="utf-8")
        self.assertIn("The Outfit Project Authors", outfit)
        self.assertIn("SIL Open Font License", outfit)
        self.assertIn("The Instrument Serif Project Authors", serif)
        self.assertIn("SIL Open Font License", serif)
        notice = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("assets/fonts/", notice)
        self.assertIn("SIL Open Font License", notice)
        self.assertIn("not covered by the proprietary notice", notice)


if __name__ == "__main__":
    unittest.main()
