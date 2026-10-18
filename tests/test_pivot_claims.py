from __future__ import annotations

import json
import re
import unittest

from tests.site_html import (
    NOINDEX_PAGES,
    ROOT,
    brochure_html_pages,
    home_page_markup,
    home_served_copy,
    root_html_pages,
)


class PublicExportContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pages = {path.name: path.read_text(encoding="utf-8") for path in root_html_pages()}
        cls.brochure = {path.name: path.read_text(encoding="utf-8") for path in brochure_html_pages()}

    def test_public_export_has_canonical_discovery_metadata(self) -> None:
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("Sitemap: https://signet7.io/sitemap.xml", robots)
        for name, html in self.brochure.items():
            with self.subTest(page=name):
                canonical = f"https://signet7.io/{name.removesuffix('.html')}"
                self.assertIn(f'<link rel="canonical" href="{canonical}">', html)
                self.assertIn(f'<meta property="og:url" content="{canonical}">', html)
                if name in NOINDEX_PAGES:
                    if name != "404.html":
                        self.assertIn('<meta name="robots" content="noindex, nofollow">', html)
                    self.assertNotIn(f"<loc>{canonical}</loc>", sitemap)
                else:
                    self.assertIn(f"<loc>{canonical}</loc>", sitemap)

    def test_structured_data_does_not_claim_certification(self) -> None:
        payload = json.loads((ROOT / "assets" / "ld-website.json").read_text(encoding="utf-8"))
        types = {node.get("@type") for node in payload["@graph"]}
        self.assertEqual(types, {"WebSite", "Organization"})
        combined = json.dumps(payload).lower()
        for banned in ("compliant", "certified", "soc 2", "eidas", "five stars", "aggregaterating"):
            self.assertNotIn(banned, combined)

    def test_bing_indexnow_key_file_matches_its_name(self) -> None:
        key = "31c6ab5cca284146bb0b26bd193d25e2"
        self.assertEqual((ROOT / f"{key}.txt").read_text(encoding="utf-8").strip(), key)

    def test_google_search_console_file_is_exact(self) -> None:
        path = ROOT / "googled2cf3c6d0c5a81c5.html"
        self.assertEqual(
            path.read_text(encoding="utf-8").strip(),
            "google-site-verification: googled2cf3c6d0c5a81c5.html",
        )
        self.assertNotIn("googled2cf3c6d0c5a81c5", (ROOT / "sitemap.xml").read_text(encoding="utf-8"))

    def test_legal_drafts_exist_and_are_linked_from_brochure_pages(self) -> None:
        for target in ("terms", "disclaimer"):
            self.assertIn(f"{target}.html", self.pages)
        for name, html in self.brochure.items():
            with self.subTest(page=name):
                self.assertIn('href="terms"', html)
                self.assertIn('href="disclaimer"', html)
        self.assertEqual(self.pages["terms.html"].count("DRAFT — NON-OPERATIVE"), 1)
        self.assertEqual(self.pages["disclaimer.html"].count("DRAFT — NON-OPERATIVE"), 1)

    def test_brochure_pages_do_not_ship_secrets_or_signup_forms(self) -> None:
        for name, html in self.pages.items():
            with self.subTest(page=name):
                self.assertNotIn("AKIA", html)
                self.assertNotIn("BEGIN PRIVATE KEY", html)
                self.assertNotIn("ghp_", html)
                if name != "download.html":
                    self.assertNotRegex(html, r"<form\b")

    def test_check_page_does_not_pretend_to_run_the_check(self) -> None:
        check = self.pages["check.html"].lower()
        self.assertIn("this brochure site cannot run that check", check)
        self.assertIn("/email/verify", check)
        self.assertIn("not sealed is ordinary mail", check)

    def test_download_page_does_not_publish_zip_links(self) -> None:
        download = self.pages["download.html"]
        self.assertIn("https://account.signet7.io/account", download)
        self.assertNotIn('href="files/signet7-watch-windows.zip"', download)
        self.assertTrue((ROOT / "files" / "signet7-watch-windows.zip").is_file())
        self.assertTrue((ROOT / "files" / "signet7-watch-macos.zip").is_file())
        self.assertTrue((ROOT / "files" / "signet7-watch-linux.zip").is_file())

    def test_programs_page_does_not_publish_a_price(self) -> None:
        programs = self.pages["programs.html"]
        self.assertIn("no card can be charged", programs.lower())
        self.assertNotRegex(programs, r"<form\b")

    def test_feedback_posts_to_the_live_host(self) -> None:
        js = (ROOT / "assets" / "feedback.js").read_text(encoding="utf-8")
        self.assertIn("https://verify.signet7.io/api/v1/feedback", js)
        self.assertIn("fetch(", js)
        self.assertNotIn("mailto:", js)

    def test_install_scripts_are_not_a_recipient_path(self) -> None:
        ps1 = (ROOT / "install.ps1").read_text(encoding="utf-8")
        sh = (ROOT / "install.sh").read_text(encoding="utf-8")
        self.assertIn("Recipients should not run this", ps1)
        self.assertNotIn("qual", ps1.lower())
        self.assertNotIn("qual", sh.lower())

    def test_spec_jargon_stays_off_marketing_pages(self) -> None:
        for name in ("index.html", "product.html"):
            html = home_page_markup() if name == "index.html" else self.pages[name]
            with self.subTest(page=name):
                self.assertNotIn("EXECUTEWIRE", html)
                self.assertNotIn("signet7-circuit.jpg", html)
                self.assertNotIn("door-loop.mp4", html)


class ContentSecurityPolicy(unittest.TestCase):
    """GitHub Pages cannot set response headers, so the policy ships in the markup."""

    def setUp(self) -> None:
        self.pages = {path.name: path.read_text(encoding="utf-8") for path in root_html_pages()}

    def test_every_page_declares_the_restrictive_policy(self) -> None:
        for name, html in self.pages.items():
            with self.subTest(page=name):
                self.assertIn('<meta http-equiv="Content-Security-Policy"', html)
                for directive in (
                    "default-src 'self'",
                    "object-src 'none'",
                    "base-uri 'none'",
                    "frame-ancestors 'none'",
                    "upgrade-insecure-requests",
                ):
                    self.assertIn(directive, html)

    def test_no_inline_script_or_style_can_silently_rely_on_an_exemption(self) -> None:
        for name, html in self.pages.items():
            with self.subTest(page=name):
                self.assertNotIn("unsafe-inline", html)
                self.assertNotIn("<style", html)
                self.assertNotIn('style="', html)
                for match in re.finditer(r"<script([^>]*)>(.*?)</script>", html, flags=re.I | re.S):
                    attrs, body = match.group(1), match.group(2)
                    self.assertTrue('src="' in attrs or "src='" in attrs)
                    self.assertNotIn("http:", attrs.lower())
                    self.assertEqual(body.strip(), "")

    def test_brochure_pages_use_dark_chrome_and_account_links(self) -> None:
        for path in brochure_html_pages():
            html = path.read_text(encoding="utf-8")
            with self.subTest(page=path.name):
                self.assertIn('data-theme="dark"', html)
                self.assertIn("https://account.signet7.io/account", html)
                self.assertIn("cad-mark", html)

    def test_outlook_stay_in_mail(self) -> None:
        manifest = (ROOT / "outlook" / "manifest.xml").read_text(encoding="utf-8")
        self.assertIn("<SupportsPinning>true</SupportsPinning>", manifest)
        self.assertNotIn("OnMessageSend", manifest)
        self.assertNotIn("LaunchEvent", manifest)
        js = (ROOT / "outlook" / "taskpane.js").read_text(encoding="utf-8")
        self.assertIn("/api/v1/vsn/listing", js)
        self.assertIn("https://verify.signet7.io", js)
        compose = (ROOT / "outlook" / "compose.js").read_text(encoding="utf-8")
        self.assertNotIn("item.body.setAsync", compose)
        self.assertNotIn("verify.signet7.io/email/verify", compose)

    def test_homepage_bundle_does_not_name_vsn(self) -> None:
        home = home_served_copy()
        self.assertNotIn("Verifiable Sender Network (VSN)", home)
        self.assertNotIn("VSN (Verifiable Sender Network)", home)


if __name__ == "__main__":
    unittest.main()
