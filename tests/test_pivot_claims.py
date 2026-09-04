from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AgentActionGatingPivotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pages = {
            path.name: path.read_text(encoding="utf-8")
            for path in sorted(ROOT.glob("*.html"))
        }
        cls.all_copy = "\n".join(cls.pages.values())

    def test_pilot_page_exists_and_is_linked_from_product(self) -> None:
        self.assertIn("pilot.html", self.pages)
        self.assertIn('href="pilot"', self.pages["product.html"])
        self.assertIn('href="pilot"', self.pages["programs.html"])

    def test_public_export_has_canonical_discovery_metadata(self) -> None:
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("Sitemap: https://signet7.io/sitemap.xml", robots)
        for name, html in self.pages.items():
            with self.subTest(page=name):
                canonical = "https://signet7.io/" if name == "index.html" else f"https://signet7.io/{name.removesuffix('.html')}"
                self.assertIn(f'<link rel="canonical" href="{canonical}">', html)
                self.assertIn(f'<meta property="og:url" content="{canonical}">', html)
                if name in {"terms.html", "disclaimer.html", "404.html"}:
                    if name in {"terms.html", "disclaimer.html"}:
                        self.assertIn('<meta name="robots" content="noindex, nofollow">', html)
                    self.assertNotIn(f"<loc>{canonical}</loc>", sitemap)
                else:
                    self.assertIn(f"<loc>{canonical}</loc>", sitemap)

    def test_legal_drafts_exist_and_are_linked_once_from_every_page(self) -> None:
        for target in ("terms", "disclaimer"):
            self.assertIn(f"{target}.html", self.pages)
            for name, html in self.pages.items():
                with self.subTest(page=name, target=target):
                    self.assertIn(f'href="{target}"', html)
        self.assertEqual(self.pages["terms.html"].count("DRAFT — NON-OPERATIVE"), 1)
        self.assertEqual(self.pages["disclaimer.html"].count("DRAFT — NON-OPERATIVE"), 1)

    def test_front_door_owns_consequential_email(self) -> None:
        home = self.pages["index.html"].lower()
        for phrase in (
            "trust layer for consequential email",
            "check the seal before you act.",
            "nobody else puts the whole check together",
            "businesses that move money or change accounts",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, home)
        self.assertNotIn("call them on a number you already have", home)
        self.assertNotIn("listed is not trusted", home.lower())
        self.assertNotIn("you still decide", home.lower())
        self.assertNotIn("cryptographic agent-action gating", home)
        self.assertNotIn("gate what the agent does.", home)

    def test_enterprise_page_is_plain_and_linked(self) -> None:
        self.assertIn("enterprise.html", self.pages)
        ent = self.pages["enterprise.html"]
        self.assertIn("A company can prove the email before anyone acts.", ent)
        self.assertIn("Technical specification", ent)
        self.assertIn("This brochure site does not take passwords.", ent)
        self.assertNotIn("<form", ent)
        self.assertNotIn("API token", ent)
        self.assertNotIn("EXECUTEWIRE", ent)
        self.assertNotIn("pip install", ent)
        self.assertIn('href="enterprise"', self.pages["product.html"])
        for name, html in self.pages.items():
            with self.subTest(page=name):
                self.assertNotIn("AKIA", html)
                self.assertNotIn("BEGIN PRIVATE KEY", html)
                self.assertNotIn("ghp_", html)

    def test_current_product_truth_is_bounded_to_implemented_contract(self) -> None:
        spec = self.pages["docs.html"]
        product = self.pages["product.html"]
        for phrase in (
            "Action-bound signatures",
            "Fail-closed unknown actions",
            "no separate inbound/outbound",
            "EXECUTEWIRE",
            "PURCHASE",
            "REFUND",
            "TRANSFER",
            "HTTP and MCP decision surfaces",
            "s7-email-1",
            "text and HTML alternatives",
            "attachment bytes plus declared metadata",
            "caller refuses or performs",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, spec)
        self.assertNotIn("signet7-circuit.jpg", self.pages["index.html"])
        self.assertNotIn("door-loop.mp4", product)
        self.assertNotIn("seasons-scene", product)
        self.assertNotIn("signet7-circuit.jpg", product)
        self.assertNotIn("EXECUTEWIRE", product)
        self.assertNotIn("EXECUTEWIRE", self.pages["index.html"])

    def test_docs_page_is_a_customer_handbook(self) -> None:
        docs = self.pages["docs.html"]
        self.assertIn("account.signet7.io/account", docs)
        self.assertIn("verify.signet7.io/email/verify", docs)
        self.assertIn("verify.signet7.io/vsn", docs)
        self.assertIn("seal.signet7.io", docs)
        self.assertIn("Create a Google Cloud app for Gmail", docs)
        self.assertIn("console.cloud.google.com", docs)
        self.assertIn("gmail.googleapis.com", docs)
        self.assertIn("Desktop app", docs)
        self.assertNotIn("check@signet7.io", docs)
        self.assertNotIn("Forward the original", docs)
        self.assertIn(
            '<a href="https://verify.signet7.io/email/verify">Recipients still check at the live check</a>',
            docs,
        )
        self.assertIn("Sideload the manifest", docs)
        self.assertIn("outlook/manifest.xml", docs)
        self.assertIn("Other Mail Account", docs)
        self.assertIn("docs-signet7-mailbox-helper.png", docs)
        self.assertIn("docs-apple-mail-server-settings.png", docs)
        self.assertIn("Authentication <strong>None</strong>", docs)
        self.assertTrue((ROOT / "assets" / "docs-signet7-mailbox-helper.png").is_file())
        self.assertTrue((ROOT / "assets" / "docs-apple-mail-server-settings.png").is_file())
        self.assertIn("127.0.0.1", docs)
        self.assertIn("The signed app is not open yet", docs)
        self.assertIn("id=\"install\"", docs)
        self.assertTrue((ROOT / "docs" / "index.html").is_file())
        self.assertIn("/docs.html", (ROOT / "docs" / "index.html").read_text(encoding="utf-8"))
        self.assertIn("How to use Signet7", docs)
        self.assertIn("class=\"docs-manual\"", docs)
        self.assertIn("Contents", docs)
        self.assertIn("docs-sidebar", docs)
        self.assertIn("assets/docs.css", docs)
        self.assertIn("assets/docs-nav.js", docs)
        self.assertNotIn("door-loop.mp4", docs)
        self.assertNotIn("seasons-scene", docs)
        self.assertNotIn("admin.signet7.io", docs)
        self.assertNotIn("qual.signet7.io", docs)
        self.assertNotIn("pip install", docs)
        self.assertIn("You received an important email", docs)
        self.assertIn("Seal from Apple Mail", docs)
        self.assertLess(docs.find('id="verify"'), docs.find('id="signup"'))
        self.assertLess(docs.find('id="limits"'), docs.find('id="signup"'))
        self.assertLess(docs.find('id="seal"'), docs.find('id="clients"'))
        self.assertIn("id=\"desktop\"", docs)
        self.assertIn("The desktop helper", docs)
        self.assertIn("Right — Status", docs)
        self.assertLess(docs.find('id="desktop"'), docs.find('id="apple-mail"'))
        self.assertLess(docs.find('id="apple-mail"'), docs.find('id="install"'))

    def test_trust_page_separates_identity_evidence_and_compliance(self) -> None:
        spec = self.pages["docs.html"]
        for phrase in (
            "Signature-bound sender identity",
            "Self-signed",
            "Unresolved",
            "does not block every phishing technique",
            "Evidence support is not certification",
            "No universal legal duration or seven-year default",
            "Bind a signing key to a domain. Check whether that binding still holds.",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, spec)

    def test_integration_page_keeps_caller_enforcement_explicit(self) -> None:
        spec = self.pages["docs.html"]
        for phrase in (
            "API/MCP-first",
            "No replacement mailbox",
            "No traditional SEG",
            "No endpoint agent",
            "Integration still required",
            "Caller enforces",
            "treating the response as advisory while executing anyway defeats the control",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, spec)

    def test_program_page_retires_old_public_prices(self) -> None:
        programs = self.pages["programs.html"]
        for phrase in (
            "Check for free. Company app for several work emails.",
            "Checkout not live yet",
            "Amounts not set",
            "Inactive catalog",
            "Team is not a catalog SKU",
            "vanity seats",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, programs)
        for stale_price in (
            "$12 / $29 / $99 / from $1,000",
            "$12/month",
            "$29/month",
            "$99/month",
            "$1,000/month",
        ):
            self.assertNotIn(stale_price, programs)

    def test_pilot_is_bounded_and_not_a_production_offer(self) -> None:
        pilot = self.pages["pilot.html"]
        for phrase in (
            "Founding Design Partner Evaluation",
            "four-week",
            "No automatic paid conversion",
            "not a production service",
            "Synthetic or lower-risk actions first",
            "Test one payment-instruction email.",
            "Senders with one payment-instruction workflow.",
            "Exact pivot pricing is not approved",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, pilot)
        self.assertNotRegex(pilot, r"<form\b")
        price_copy = re.sub(r'<section class="facts".*?</section>', "", pilot, flags=re.S)
        self.assertEqual(re.findall(r"\$\s*\d+", price_copy), ["$0"])

    def test_check_page_exists_and_is_honest_about_hosting(self) -> None:
        self.assertIn("check.html", self.pages)
        check = self.pages["check.html"].lower()
        self.assertIn("check the email that asks you to act", check)
        self.assertIn("this brochure site cannot run that check", check)
        self.assertIn("this brochure does not run the check", check)
        self.assertIn("no seal is ordinary mail", check)
        self.assertIn("will not say a message is safe", check)
        self.assertIn("/email/verify", check)
        self.assertNotIn("no install for the other side", check)
        self.assertIn('href="product"', self.pages["index.html"])

    def test_scenarios_page_is_living_and_cross_platform(self) -> None:
        self.assertIn("scenarios.html", self.pages)
        page = self.pages["scenarios.html"].lower()
        for phrase in (
            "living document",
            "windows, macos, and linux",
            "not a mail app",
            "small company",
            "corporation",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, page)
        self.assertIn('href="scenarios"', self.pages["product.html"])

    def test_smtp_recipes_are_cross_platform(self) -> None:
        self.assertIn("smtp.html", self.pages)
        page = self.pages["smtp.html"].lower()
        for phrase in ("127.0.0.1", "2525", "outlook", "apple mail", "thunderbird", "windows, macos, and linux"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, page)

    def test_it_one_pager_exists(self) -> None:
        self.assertIn("it.html", self.pages)
        page = self.pages["it.html"].lower()
        for phrase in ("several named emails", "windows, mac, and linux", "127.0.0.1"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, page)

    def test_download_page_ships_unsigned_watch_zips(self) -> None:
        self.assertIn("download.html", self.pages)
        download = self.pages["download.html"]
        self.assertNotIn("pip install", download)
        self.assertNotIn("pypi.org", download)
        self.assertNotIn("money mailbox", download.lower())
        self.assertNotIn("is-off", download)
        self.assertNotIn("Not open yet", download)
        self.assertIn("unlock-form", download)
        self.assertIn("Step 1", download)
        self.assertIn("Recipients never install", download)
        self.assertIn("not code-signed yet", download)
        self.assertIn("Checkout is not live", download)
        self.assertNotIn("href=\"files/signet7-watch-windows.zip\"", download)
        self.assertNotIn("href=\"files/signet7-watch-macos.zip\"", download)
        self.assertNotIn("href=\"files/signet7-watch-linux.zip\"", download)
        self.assertTrue((ROOT / "files" / "signet7-watch-windows.zip").is_file())
        self.assertTrue((ROOT / "files" / "signet7-watch-macos.zip").is_file())
        self.assertTrue((ROOT / "files" / "signet7-watch-linux.zip").is_file())
        self.assertTrue((ROOT / "files" / "latest.json").is_file())

    def test_customer_copy_never_says_money_mailbox(self) -> None:
        paths = list(ROOT.glob("*.html")) + list((ROOT / "outlook").glob("*.html")) + [ROOT / "assets" / "motion.js"]
        for path in paths:
            with self.subTest(path=path.name):
                self.assertNotIn("money mailbox", path.read_text(encoding="utf-8").lower())
                self.assertNotIn("money inbox", path.read_text(encoding="utf-8").lower())

    def test_feedback_page_posts_send_without_mailto(self) -> None:
        html = self.pages["feedback.html"]
        js = (ROOT / "assets" / "feedback.js").read_text(encoding="utf-8")
        self.assertNotIn("<form", html)
        self.assertIn("Tell us what to build, fix, or change.", html)
        self.assertIn("Press Send", html)
        self.assertNotIn("mailto:", html)
        self.assertNotIn("qual", html.lower())
        self.assertIn('href="pilot"', self.pages["product.html"])
        self.assertIn("https://verify.signet7.io/api/v1/feedback", js)
        self.assertIn("fetch(", js)
        self.assertNotIn("mailto:", js)
        self.assertNotIn("qual", js.lower())
        programs = self.pages["programs.html"]
        self.assertIn('href="feedback"', programs)
        self.assertNotIn("mailto:sales@signet7.io", programs)
        contact = self.pages["contact.html"]
        self.assertIn('href="feedback"', contact)
        home_footer = self.pages["index.html"].split("<footer", 1)[1]
        self.assertIn('href="feedback">Feedback</a>', home_footer)
        self.assertIn('href="about">About</a>', self.pages["index.html"].split('<nav class="site-nav"', 1)[1].split("</nav>", 1)[0])

    def test_homepage_situation_chooser_and_terminal_install(self) -> None:
        home = self.pages["index.html"]
        self.assertIn("From one person checking a message to a company of a thousand.", home)
        self.assertIn("Most people do not download anything", home)
        self.assertIn("I received one email", home)
        self.assertIn("Many people, one company", home)
        self.assertNotIn("data-install-chooser", home)
        self.assertNotIn("irm https://signet7.io/install.ps1 | iex", home)
        self.assertNotIn("Show options", home)
        self.assertNotIn("pip install signet7", home)
        download = self.pages["download.html"]
        self.assertIn("data-install-chooser", download)
        self.assertIn("one company download", download.lower())
        self.assertNotIn("Show options", download)
        self.assertNotIn("Chrome Web Store", home)
        self.assertNotIn("Play Store", home)
        js = (ROOT / "assets" / "install-chooser.js").read_text(encoding="utf-8")
        self.assertIn("install.sh", js)
        self.assertNotIn("pip install signet7", js)
        ps1 = (ROOT / "install.ps1").read_text(encoding="utf-8")
        sh = (ROOT / "install.sh").read_text(encoding="utf-8")
        self.assertIn("SIGNET7_SETUP", ps1)
        self.assertIn("verify.signet7.io/email/verify", ps1)
        self.assertIn("Recipients should not run this", ps1)
        self.assertNotIn("qual", ps1.lower())
        self.assertIn("SIGNET7_SETUP", sh)
        self.assertNotIn("qual", sh.lower())
        integrations = self.pages["integrations.html"]
        self.assertIn("Do you need a download?", integrations)
        self.assertIn("Live check — no download", integrations)
        self.assertIn("Not Play Store", integrations)
        self.assertIn("Not AppSource", integrations)
        self.assertNotIn("qual", integrations.lower())

    def test_outlook_directory_has_index_for_pages(self) -> None:
        index = ROOT / "outlook" / "index.html"
        self.assertTrue(index.is_file())
        html = index.read_text(encoding="utf-8")
        self.assertIn("manifest.xml", html)
        self.assertIn("Sideload", html)
        self.assertIn("Checkout is not live", html)
        self.assertIn("verify.signet7.io/email/verify", html)
        self.assertNotIn("qual", html.lower())

    def test_pay_page_stays_closed(self) -> None:
        self.assertIn("pay.html", self.pages)
        pay = self.pages["pay.html"]
        self.assertIn("Placeholder $12", pay)
        self.assertIn("Placeholder $29", pay)
        self.assertIn("Placeholder $99", pay)
        self.assertIn("Placeholder from $1,000", pay)
        self.assertIn("Free for a limited time", pay)
        self.assertIn("Amount not set", pay)
        self.assertIn("is-off", pay)
        self.assertIn("Checkout is not live", pay)
        self.assertNotIn("free forever", pay.lower())
        self.assertNotRegex(pay, r"<form\b")
        for name, html in self.pages.items():
            with self.subTest(page=name):
                self.assertRegex(html, r'href="(\.\./)?download"')
                self.assertNotIn("pypi.org", html)
                if name in {"index.html", "product.html", "about.html", "enterprise.html"}:
                    self.assertIn('class="facts"', html)
                else:
                    self.assertNotIn('class="facts"', html)

    def test_every_page_keeps_live_service_boundary(self) -> None:
        for name, html in self.pages.items():
            with self.subTest(page=name):
                self.assertIn("live check and company accounts are available", html.lower())

    def test_every_page_has_dropdown_nav(self) -> None:
        for name, html in self.pages.items():
            with self.subTest(page=name):
                self.assertIn("drop-btn", html)
                self.assertIn(">Feedback</a>", html)
                self.assertNotIn("Use cases", html)
                self.assertNotIn("Install (pip)", html)
                nav = html.split('<nav class="site-nav"', 1)[1].split("</nav>", 1)[0]
                self.assertIn(">Product</button>", nav)
                self.assertIn(">Company</button>", nav)
                self.assertNotIn(">Help</button>", nav)
                self.assertNotIn("How it works", nav)
                self.assertIn("What it is", nav)
                self.assertRegex(nav, r'href="(\.\./)?about">About</a>')
                self.assertRegex(nav, r'href="(\.\./)?register">Register</a>')
                self.assertRegex(nav, r'href="(\.\./)?faq">FAQ</a>')
                self.assertRegex(nav, r'href="(\.\./)?download">Download</a>')
                product_menu = nav.split(">Product</button>", 1)[1].split("</div>", 1)[0]
                self.assertNotIn("Docs", product_menu)
                self.assertRegex(
                    nav,
                    r">Product</button>[\s\S]*?</div>\s*</div>\s*<a href=\"(\.\./)?docs\.html\">Docs</a>\s*<div class=\"drop\">",
                )
                self.assertNotIn(">Check</button>", nav)
                self.assertNotIn(">Legal</button>", nav)
                self.assertNotIn(">Docs</button>", nav)
                self.assertNotIn(">About</button>", nav)
                self.assertNotIn('<p class="drop-head">Product</p>', nav)
                self.assertNotIn(">About Signet7</a>", nav)
        self.assertIn("Inbox Watch", self.pages["index.html"])
        self.assertIn("Team", self.pages["about.html"])

    def test_public_copy_does_not_overclaim(self) -> None:
        visible = re.sub(r"<[^>]+>", " ", self.all_copy).lower()
        forbidden = (
            r"signet7\s+(?:prevents|blocks|stops)\s+(?:phishing|fraud|scams|malware|ransomware)",
            r"signet7\s+makes\s+(?:email|messages?|actions?)\s+safe",
            r"verified\s+means\s+safe",
            r"unverified\s+means\s+fraud",
            r"hipaa compliant email",
            r"seven-year retention by default",
            r"no integration required",
        )
        for pattern in forbidden:
            with self.subTest(pattern=pattern):
                self.assertIsNone(re.search(pattern, visible))

    def test_public_pages_have_no_mascot(self) -> None:
        for name, html in self.pages.items():
            with self.subTest(page=name):
                low = html.lower()
                self.assertNotIn("sidekick", low)
                self.assertNotIn("data-buddy", low)
                self.assertNotIn("meet-buddy", low)
                self.assertNotIn("click me", low)
        motion = (ROOT / "assets" / "motion.js").read_text(encoding="utf-8").lower()
        css = (ROOT / "assets" / "site.css").read_text(encoding="utf-8").lower()
        for blob in (motion, css):
            self.assertNotIn("data-buddy", blob)
            self.assertNotIn("sidekick", blob)
            self.assertNotIn("buddy-hit", blob)

    def test_homepage_is_a_customer_front_door(self) -> None:
        home = self.pages["index.html"]
        low = home.lower()
        self.assertIn("$3.05B", home)
        self.assertIn("24,768", home)
        self.assertIn("$20.9B", home)
        self.assertIn("191K+", home)
        self.assertIn("Business Email Compromise", home)
        self.assertNotIn("BEC ", home)
        self.assertNotIn(">BEC", home)
        self.assertIn("Law office", home)
        self.assertIn("A record you can produce", home)
        self.assertIn("You hand them the check", home)
        self.assertIn("That file is the record.", home)
        self.assertIn("fbi ic3", low)
        self.assertNotIn("pip install signet7", home)
        self.assertNotIn("pip install signet7", self.pages["download.html"])
        self.assertIn("href=\"download\"", home)
        self.assertIn("Verifiable Sender Network (VSN)", home)
        self.assertIn("Verifiable Sender Network", home)
        self.assertNotIn("$12 / $29 / $99", home)
        self.assertIn("Placeholder $12", self.pages["pay.html"])
        self.assertIn("https://account.signet7.io/account", home)
        self.assertIn("Login to Signet7", home)
        self.assertIn("drop-btn", home)
        self.assertIn("Programs", self.pages["product.html"])
        self.assertIn('href="programs"', self.pages["product.html"])
        self.assertNotRegex(home, r"<form\b")
        self.assertNotIn("dual-control", low)
        self.assertNotIn("isolated qualification", low)
        self.assertNotIn("api/mcp-first", low)
        self.assertNotIn("executewire", low)
        self.assertIn("The check. One Watch. A company that can be looked up.", home)
        self.assertIn("Not a thousand installs", home)
        self.assertIn("vanity seats", home)
        self.assertIn("What Watch does", self.pages["download.html"])
        self.assertIn("What does Watch do?", self.pages["faq.html"])
        self.assertIn("the no-install door", self.pages["faq.html"])
        self.assertIn("Recipients still never install", self.pages["faq.html"])
        self.assertNotIn("going to the factory", self.pages["faq.html"])
        self.assertIn("id=\"three-jobs\"", self.pages["faq.html"])
        self.assertIn("id=\"status-chips\"", self.pages["faq.html"])
        self.assertIn("People and agents use the same check", self.pages["faq.html"])
        self.assertIn("only between you and them", self.pages["faq.html"])
        self.assertIn("Sideload is not Watch", self.pages["faq.html"])
        self.assertIn("more than one listing", self.pages["faq.html"])
        self.assertNotIn("One listing covers every mailbox", self.pages["faq.html"])
        self.assertIn("Named work emails", self.pages["enterprise.html"])
        programs = self.pages["programs.html"]
        self.assertIn("Team is not a catalog SKU", programs)
        self.assertNotIn("Governed agents", programs)
        self.assertIn("vanity seats", programs)
        self.assertIn("Checkout is not live", programs)


class ContentSecurityPolicy(unittest.TestCase):
    """GitHub Pages cannot set response headers, so the policy ships in the markup.

    frame-ancestors is ignored when delivered via <meta>; it is declared here so the
    policy is correct the moment the domain moves behind a header-capable layer, which
    must happen before any verification surface is hosted on signet7.io.
    """

    def setUp(self) -> None:
        self.pages = {
            path.name: path.read_text(encoding="utf-8") for path in sorted(ROOT.glob("*.html"))
        }

    def test_every_page_declares_the_restrictive_policy(self) -> None:
        self.assertTrue(self.pages)
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
                self.assertIn('<meta name="referrer" content="strict-origin-when-cross-origin">', html)
                self.assertIn('<meta http-equiv="X-Content-Type-Options" content="nosniff">', html)

    def test_no_inline_script_or_style_can_silently_rely_on_an_exemption(self) -> None:
        """Self-hosted motion scripts are allowed. Inline script/style is not."""
        for name, html in self.pages.items():
            with self.subTest(page=name):
                self.assertNotIn("unsafe-inline", html)
                self.assertNotIn("<style", html)
                self.assertNotIn('style="', html)
                for match in re.finditer(r"<script([^>]*)>(.*?)</script>", html, flags=re.I | re.S):
                    attrs, body = match.group(1), match.group(2)
                    self.assertIn('src="assets/', attrs)
                    self.assertNotIn("http:", attrs.lower())
                    self.assertEqual(body.strip(), "")

    def test_every_page_has_theme_switch_and_dark_scene_asset(self) -> None:
        self.assertTrue((ROOT / "assets" / "tech-scene-dark.jpg").is_file())
        self.assertTrue((ROOT / "assets" / "theme.js").is_file())
        for name, html in self.pages.items():
            with self.subTest(page=name):
                self.assertIn('data-theme="light"', html)
                self.assertNotIn("data-theme-toggle", html)
                self.assertNotIn("Dark mode", html)
                self.assertNotIn("Light mode", html)
                self.assertIn('src="assets/theme.js', html)
                self.assertIn("signet7-logo-mark.png", html)
                self.assertIn('width="768"', html)
                self.assertIn("https://account.signet7.io/account", html)
                self.assertIn(">Login to Signet7</a>", html)
                self.assertEqual(html.count(">Login to Signet7</a>"), 1)
                self.assertIn('class="header-register"', html)
                self.assertLess(html.index('class="header-register"'), html.index('class="account-login"'))
                self.assertNotIn(">Account</a>", html)
                self.assertIn("header-cta", html)
                self.assertEqual(html.count("header-cta"), 1)
        theme = (ROOT / "assets" / "theme.js").read_text(encoding="utf-8")
        self.assertIn('data-theme", "light"', theme)
        self.assertNotIn("s7-theme-v2", theme)
        home = self.pages["index.html"]
        self.assertNotIn("signet7-circuit.jpg", home)
        self.assertNotIn("seasons-scene", home)
        self.assertNotIn("door-loop.mp4", home)
        self.assertIn("zoom/01.jpg", home)
        self.assertIn("data-demo-next", home)
        self.assertIn("Step 1 of 4", home)
        self.assertIn('data-panel="vsn"', home)
        self.assertIn('data-panel="decide"', home)
        motion = (ROOT / "assets" / "motion.js").read_text(encoding="utf-8")
        self.assertIn("Next · Verifiable Sender Network (VSN)", motion)
        self.assertIn("demoStep === 4", motion)
        home = self.pages["index.html"]
        self.assertIn("High-stakes email, finally", home)
        self.assertIn("provable", home)
        self.assertNotIn("Make email something you can prove", home)
        self.assertNotIn("not just trust", home)
        self.assertIn("cryptographic check for high-stakes email", home.lower())
        self.assertIn("powered by our Verifiable Sender Network (VSN)", home)
        self.assertIn("signed file you can produce later", home.lower())
        self.assertIn("gate actions proposed by people or AI agents", home)

    def test_dark_mode_uses_tokens_so_menus_keep_ink(self) -> None:
        css = (ROOT / "assets" / "site.css").read_text(encoding="utf-8")
        self.assertIn("--card:", css)
        self.assertIn("--ink:", css)
        self.assertIn('html[data-theme="dark"]', css)
        self.assertIn(".home .site-nav .drop-menu a", css)
        self.assertNotIn(".drop-menu a { color: #e8eef4", css)

    def test_outlook_stay_in_mail(self) -> None:
        manifest = (ROOT / "outlook" / "manifest.xml").read_text(encoding="utf-8")
        self.assertIn("<SupportsPinning>true</SupportsPinning>", manifest)
        self.assertIn("OnMessageSend", manifest)
        pane = (ROOT / "outlook" / "taskpane.html").read_text(encoding="utf-8")
        self.assertIn("inviteBtn", pane)
        js = (ROOT / "outlook" / "taskpane.js").read_text(encoding="utf-8")
        self.assertIn("/api/v1/vsn/listing", js)
        self.assertIn("account.signet7.io/account?invite=", js)
        self.assertNotIn("This message was sealed with Signet7", js)
        compose = (ROOT / "outlook" / "compose.js").read_text(encoding="utf-8")
        self.assertIn("signet7-invite-asked-v1", compose)
        self.assertIn("invitePrompt", compose)
        self.assertNotIn("item.body.setAsync", compose)
        self.assertNotIn("verify.signet7.io/email/verify", compose)
        html = (ROOT / "outlook" / "compose.html").read_text(encoding="utf-8")
        self.assertIn("inviteBtn", html)
        self.assertIn("Do not put a check link in the business letter", html)

    def test_outlook_sideload_does_not_whisper_hedge(self) -> None:
        manifest = (ROOT / "outlook" / "manifest.xml").read_text(encoding="utf-8")
        readme = (ROOT / "outlook" / "README.md").read_text(encoding="utf-8")
        for blob in (manifest, readme):
            lower = blob.lower()
            self.assertNotIn("verified is not safe", lower)
            self.assertNotIn("unknown is not fraud", lower)
            self.assertNotIn("listed is not trusted", lower)
            self.assertNotIn("you still decide", lower)
            self.assertNotIn("safe to pay", lower)
        self.assertIn("Passive incoming check. Keep writing in Outlook.", manifest)
        self.assertIn("Not Exchange.", readme)
        self.assertIn("Sideload `manifest.xml`.", readme)

    def test_outlook_pane_uses_same_two_facts_as_the_website_check(self) -> None:
        js = (ROOT / "outlook" / "taskpane.js").read_text(encoding="utf-8")
        pane = (ROOT / "outlook" / "taskpane.html").read_text(encoding="utf-8")
        self.assertIn("function wordsLine", js)
        self.assertIn("function listingLine", js)
        self.assertIn("function formatRecipientResult", js)
        self.assertIn("formatRecipientResult(", js)
        self.assertIn("Words match", js)
        self.assertIn("Words do not match", js)
        self.assertIn("No seal", js)
        self.assertIn("Listed", js)
        self.assertIn("Not listed", js)
        self.assertIn("Listing doesn’t match this address", js)
        self.assertIn("The words still match the seal.", js)
        self.assertIn("Do not pay. Call a number you already have.", js)
        self.assertIn("Ordinary mail", js)
        self.assertNotIn("safe to pay", js.lower())
        self.assertNotIn("congrats", js.lower())
        self.assertNotIn("Words matching is not safe to pay", js)
        self.assertNotIn("VSN lookup", js)
        self.assertNotIn("Verifiable Sender", js)
        self.assertNotIn("safe to pay", pane.lower())
        self.assertNotIn("VSN", pane)

    def test_marketing_kit_honest_watch_and_frozen_h1(self) -> None:
        home = self.pages["index.html"]
        self.assertIn('id="hero-title"', home)
        self.assertIn("High-stakes email, finally", home)
        self.assertIn("Questionable email? Check it here.", home)
        self.assertIn("Save the original.", home)
        self.assertIn("Drop it here.", home)
        how = self.pages["how.html"]
        self.assertIn("https://verify.signet7.io/email/verify", how)
        self.assertIn("Questionable email? Check it here.", how)
        self.assertNotIn("never check this", how.lower())
        self.assertNotIn("never check them again", how.lower())
        download = self.pages["download.html"]
        self.assertIn("Not a product feature today", download)
        self.assertIn("Do not call this set and forget", download)
        self.assertIn("There is no Uninstall button", download)
        watch = self.pages["watch.html"]
        self.assertIn("There is no Uninstall button", watch)
        self.assertIn("This is not set and forget", watch)
        companies = self.pages["companies.html"]
        self.assertIn("You list your address", companies)
        self.assertIn("They list theirs", companies)
        loop = self.pages["loop.html"]
        self.assertIn("link-loop", loop)
        self.assertIn("https://verify.signet7.io/email/verify", loop)
        self.assertIn("Open the live check", loop)
        self.assertNotIn("door-loop.mp4", loop)
        kit = "\n".join(
            self.pages[n]
            for n in ("how.html", "watch.html", "vsn.html", "companies.html", "one-pager.html", "loop.html")
        ).lower()
        self.assertNotIn("verified means trusted", kit)
        self.assertNotIn("is safe to pay", kit)
        one = self.pages["one-pager.html"]
        self.assertIn("AP", one)
        nav = home.split('<nav class="site-nav"', 1)[1].split("</nav>", 1)[0]
        self.assertNotIn("How it works", nav)
        self.assertIn("What it is", nav)
        self.assertNotIn(">Watch</a>", nav)
        self.assertNotIn("Send &amp; seal", nav)
        self.assertIn('href="watch"', self.pages["product.html"])
        self.assertIn('href="smtp"', self.pages["product.html"])
        self.assertIn("The check. Inbox Watch. Send", self.pages["product.html"])
        self.assertNotIn(">Help</button>", nav)
        self.assertIn(">Company</button>", nav)
        self.assertNotIn(">About Signet7</a>", nav)

    def test_try_samples_and_locked_register_login(self) -> None:
        home = self.pages["index.html"]
        self.assertNotIn(">Check a message</a>", home)
        self.assertIn('id="try"', home)
        self.assertIn("assets/samples/intact-message", home)
        self.assertIn("assets/samples/tampered-message", home)
        self.assertIn("They kept the wax", home)
        self.assertIn("assets/art/pitch-looks.jpg", home)
        self.assertIn("assets/art/pitch-caught.jpg", home)
        self.assertIn("$20,699", home)
        self.assertIn("That is the link", home)
        self.assertNotIn(".eml", home)
        self.assertTrue((ROOT / "assets" / "samples" / "intact-message").is_file())
        self.assertTrue((ROOT / "assets" / "samples" / "tampered-message").is_file())
        css = (ROOT / "assets" / "site.css").read_text(encoding="utf-8")
        self.assertIn(".site-header {\n  position: fixed;", css)
        self.assertIn("body:not(.home) { padding-top: var(--nav-h); }", css)
        header = home.split("<header", 1)[1].split("</header>", 1)[0]
        self.assertLess(header.index("header-register"), header.index("account-login"))

    def test_public_copy_does_not_say_one_listing_covers_every_mailbox(self) -> None:
        for name, html in self.pages.items():
            low = html.lower()
            with self.subTest(page=name):
                self.assertNotIn("one listing covers every mailbox", low)
                self.assertNotIn("covers every mailbox", low)
                self.assertNotIn("bound to a domain", low)
        docs = self.pages["docs.html"]
        self.assertIn("addresses assigned to it", docs)
        self.assertIn("Domain-wide is a choice", docs)


if __name__ == "__main__":
    unittest.main()
