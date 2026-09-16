from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CheckAtAttachTests(unittest.TestCase):
    def test_integrations_and_contact_attach_not_forward(self) -> None:
        for name in ("integrations.html", "contact.html", "check.html"):
            html = (ROOT / name).read_text(encoding="utf-8")
            with self.subTest(page=name):
                self.assertIn("check@signet7.io", html)
                self.assertIn("attach the saved original", html.lower())
                self.assertNotIn("forward a saved message to", html)

    def test_register_names_vsn_bind(self) -> None:
        html = (ROOT / "register.html").read_text(encoding="utf-8")
        self.assertIn("Now with VSN.", html)
        self.assertIn("lasting listed identity", html)
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("Now with VSN.", home)

    def test_vsn_page_hosted_listings_not_planned_directory(self) -> None:
        html = (ROOT / "vsn.html").read_text(encoding="utf-8")
        self.assertIn(
            "Hosted listings on the company desk after they enroll, not a public directory",
            html,
        )
        self.assertNotIn("Hosted listings after they enroll.", html)
        self.assertNotIn("a managed company directory is not", html)
