from __future__ import annotations

import os
import re
import shutil
import subprocess
import unittest
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import urlopen

from tests.site_html import ROOT
from tests.test_site_crawl import _Doc, _public_html, _resolve


MOBILE_CRITICAL = (
    "index.html",
    "product.html",
    "docs.html",
    "about.html",
    "download.html",
    "programs.html",
    "record.html",
    "register.html",
)


def _css() -> str:
    return (ROOT / "assets" / "site.css").read_text(encoding="utf-8")


def _motion() -> str:
    return (ROOT / "assets" / "motion.js").read_text(encoding="utf-8")


def _last_header_cta_display(css: str) -> str | None:
    matches = list(re.finditer(r"\.header-cta[^{}]*\{[^{}]*display:\s*([^;}]+)", css))
    if not matches:
        return None
    return matches[-1].group(1).strip()


class MobileViewportContractTests(unittest.TestCase):
    def test_phone_css_keeps_live_check_and_hides_header_login(self) -> None:
        css = _css()
        self.assertEqual(_last_header_cta_display(css), "inline-flex")
        self.assertIn("@media (max-width: 720px)", css)
        self.assertIn(".account-login { display: none; }", css)
        self.assertIn(".nav-account-login", css)
        self.assertIn(".header-register { display: none; }", css)

    def test_phone_css_enlarges_tap_targets_and_lightbox(self) -> None:
        css = _css()
        self.assertIn("min-width: 44px;\n    min-height: 44px;", css)
        self.assertIn("min-height: 44px;\n    min-width: 72px;", css)
        self.assertIn("touch-action: pinch-zoom;", css)
        self.assertIn("max-height: min(70vh, calc(100dvh - var(--nav-h) - 16px));", css)
        self.assertIn("overflow-wrap: break-word;", css)
        self.assertIn("max-height: none;", css)
        self.assertNotIn("max-height: min(160px, 28vh);", css)
        self.assertIn(".nutshell .hero-actions { order: 2;", css)
        self.assertIn(".price-grid {\n    grid-template-columns: 1fr;", css)
        self.assertIn("overflow: visible;", css)
        self.assertIn("padding: 28px 0 max(40px, env(safe-area-inset-bottom, 24px));", css)
        self.assertIn("@media (max-width: 430px)", css)
        self.assertIn("@media (max-height: 700px)", css)

    def test_hamburger_closes_on_link_and_clones_login(self) -> None:
        motion = _motion()
        self.assertIn("nav-account-login", motion)
        self.assertIn("setNavOpen(false)", motion)
        self.assertIn('toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu")', motion)

    def test_mobile_critical_pages_keep_viewport_and_honest_pay(self) -> None:
        for name in MOBILE_CRITICAL:
            html = (ROOT / name).read_text(encoding="utf-8")
            with self.subTest(page=name):
                self.assertRegex(
                    html,
                    r'name="viewport" content="width=device-width,\s*initial-scale=1"',
                )
                self.assertIn("nav-toggle", html)
                self.assertIn("header-cta", html)
                self.assertIn("https://verify.signet7.io/email/verify", html)
        pay = (ROOT / "programs.html").read_text(encoding="utf-8")
        self.assertIn("nothing can be billed today", pay)

    def test_mobile_critical_links_and_assets_resolve(self) -> None:
        documents: dict[Path, _Doc] = {}
        failures: list[str] = []
        for name in MOBILE_CRITICAL:
            path = ROOT / name
            parser = _Doc()
            parser.feed(path.read_text(encoding="utf-8"))
            documents[path.resolve()] = parser
            for img in parser.imgs:
                if img.get("aria-hidden") == "true":
                    continue
                target = _resolve(path, img.get("src", ""))
                if target is not None and not target.exists():
                    failures.append(f"{path.name}: missing image: {img.get('src', '')}")
        for source, parser in documents.items():
            for raw in parser.links:
                target = _resolve(source, raw)
                if target is None:
                    continue
                if not target.exists():
                    failures.append(f"{source.name}: missing target: {raw}")
        self.assertEqual(failures, [])
        self.assertGreaterEqual(len(_public_html()), len(MOBILE_CRITICAL))


class OptionalPhoneRuntimeTests(unittest.TestCase):
    """Runtime checks. Skip in GitHub Actions; run locally when Chrome/Playwright exist."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.chrome = shutil.which("google-chrome") or shutil.which("chromium")
        cls.base = os.environ.get("SITE_BASE_URL", "http://127.0.0.1:8080/")
        cls.server_up = False
        try:
            with urlopen(urljoin(cls.base, "index.html"), timeout=2) as response:
                cls.server_up = response.status == 200
        except OSError:
            cls.server_up = False

    def _require_local_server(self) -> None:
        if os.environ.get("CI") == "true" or os.environ.get("GITHUB_ACTIONS") == "true":
            self.skipTest("optional phone runtime check is local-only")
        if not self.server_up:
            self.skipTest("static server is not reachable")

    def test_playwright_phone_chrome_keeps_cta_and_menu(self) -> None:
        self._require_local_server()
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            self.skipTest("Playwright is not installed")
        chrome = Path(os.environ.get("CHROME_PATH", self.chrome or ""))
        launch = {"headless": True}
        if chrome and chrome.exists():
            launch["executable_path"] = str(chrome)
        pages = ["index.html", "product.html", "record.html", "programs.html", "register.html"]
        viewports = [{"width": 390, "height": 844}, {"width": 430, "height": 932}, {"width": 390, "height": 667}]
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(**launch)
            try:
                for viewport in viewports:
                    context = browser.new_context(viewport=viewport, device_scale_factor=1, has_touch=True)
                    page = context.new_page()
                    for name in pages:
                        page.goto(urljoin(self.base, name), wait_until="domcontentloaded")
                        report = page.evaluate(
                            """() => {
                              const cta = document.querySelector('.header-cta');
                              const toggle = document.querySelector('.nav-toggle');
                              const login = document.querySelector('.account-login');
                              const h1 = document.querySelector('h1');
                              const cs = (el) => el ? getComputedStyle(el) : null;
                              return {
                                ctaDisplay: cs(cta) && cs(cta).display,
                                ctaHeight: cta ? cta.getBoundingClientRect().height : 0,
                                toggleDisplay: cs(toggle) && cs(toggle).display,
                                loginDisplay: cs(login) && cs(login).display,
                                overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
                                h1Clipped: h1 ? (h1.scrollHeight > h1.clientHeight + 2) : false,
                              };
                            }"""
                        )
                        with self.subTest(page=name, width=viewport["width"], height=viewport["height"]):
                            self.assertNotEqual(report["ctaDisplay"], "none")
                            self.assertGreaterEqual(report["ctaHeight"], 44)
                            self.assertNotEqual(report["toggleDisplay"], "none")
                            if viewport["width"] <= 720:
                                self.assertEqual(report["loginDisplay"], "none")
                            self.assertFalse(report["overflow"])
                            self.assertFalse(report["h1Clipped"])
                    context.close()
            finally:
                browser.close()

    def test_chrome_dumps_homepage_at_phone_width(self) -> None:
        self._require_local_server()
        if os.environ.get("SITE_CHROME_DUMP") != "1":
            self.skipTest("set SITE_CHROME_DUMP=1 to run Chrome --dump-dom")
        if not self.chrome:
            self.skipTest("Chrome is not installed")
        import tempfile

        with tempfile.TemporaryDirectory(prefix="s7-chrome-") as profile:
            result = subprocess.run(
                [
                    self.chrome,
                    "--headless=new",
                    "--disable-gpu",
                    "--no-sandbox",
                    f"--user-data-dir={profile}",
                    "--virtual-time-budget=4000",
                    "--window-size=390,844",
                    "--dump-dom",
                    urljoin(self.base, "index.html"),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=40,
            )
        self.assertEqual(result.returncode, 0, result.stderr[-500:])
        html = result.stdout
        self.assertIn("header-cta", html)
        self.assertIn("Live check", html)
        self.assertIn("nav-toggle", html)
        self.assertNotIn("Phase 6", html)
