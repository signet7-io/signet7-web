from __future__ import annotations

import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from tests.site_html import NOINDEX_PAGES, ROOT, root_html_pages


class _Doc(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.ids: set[str] = set()
        self.imgs: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: (value or "") for key, value in attrs}
        if values.get("id"):
            self.ids.add(values["id"])
        if tag == "img":
            self.imgs.append(values)
        for name in ("href", "src"):
            if values.get(name):
                self.links.append(values[name])


def _public_html() -> list[Path]:
    pages = root_html_pages()
    pages.append(ROOT / "outlook" / "index.html")
    pages.append(ROOT / "docs" / "index.html")
    return pages


def _resolve(source: Path, raw: str) -> Path | None:
    parsed = urlsplit(raw)
    if parsed.scheme in {"http", "https", "mailto", "tel", "data", "javascript"}:
        return None
    target_path = unquote(parsed.path)
    if not target_path:
        return source
    if target_path == "/":
        return ROOT / "index.html"
    rel = target_path[1:] if target_path.startswith("/") else target_path
    if source.parent != ROOT and not target_path.startswith("/"):
        target = (source.parent / rel).resolve()
    else:
        target = (ROOT / rel).resolve()
    try:
        target.relative_to(ROOT.resolve())
    except ValueError:
        return target
    if target.is_dir():
        sibling = target.with_suffix(".html")
        index = target / "index.html"
        if sibling.is_file():
            return sibling
        if index.is_file():
            return index
    if not target.exists() and target.suffix == "":
        html_target = target.with_name(target.name + ".html")
        if html_target.exists():
            return html_target
    return target


class SiteCrawlHardeningTests(unittest.TestCase):
    def test_brochure_and_outlook_links_resolve_and_images_have_alt(self) -> None:
        documents: dict[Path, _Doc] = {}
        failures: list[str] = []
        for path in _public_html():
            parser = _Doc()
            parser.feed(path.read_text(encoding="utf-8"))
            documents[path.resolve()] = parser
            for img in parser.imgs:
                if img.get("aria-hidden") == "true":
                    continue
                if not img.get("alt", "").strip():
                    failures.append(f"{path}: img missing alt: {img.get('src', '')}")

        for source, parser in documents.items():
            for raw in parser.links:
                parsed = urlsplit(raw)
                if parsed.scheme in {"http", "https", "mailto", "tel", "data", "javascript"}:
                    continue
                target = _resolve(source, raw)
                if target is None:
                    continue
                if not target.exists():
                    failures.append(f"{source.name}: missing target: {raw}")
                    continue
                if parsed.fragment and target.suffix.lower() == ".html":
                    target_parser = documents.get(target)
                    if target_parser is None:
                        target_parser = _Doc()
                        target_parser.feed(target.read_text(encoding="utf-8"))
                        documents[target] = target_parser
                    if parsed.fragment.startswith("/"):
                        continue
                    if parsed.fragment not in target_parser.ids:
                        failures.append(f"{source.name}: missing anchor: {raw}")
        self.assertEqual(failures, [])

    def test_css_font_and_study_urls_exist(self) -> None:
        css = (ROOT / "assets" / "site.css").read_text(encoding="utf-8")
        missing = []
        for match in re.finditer(r'url\("([^"]+)"\)', css):
            rel = match.group(1)
            if not (ROOT / "assets" / rel).is_file():
                missing.append(rel)
        self.assertEqual(missing, [])

    def test_public_chrome_is_the_same_on_brochure_pages(self) -> None:
        for path in root_html_pages() + [ROOT / "outlook" / "index.html"]:
            html = path.read_text(encoding="utf-8")
            if '<nav class="site-nav"' not in html or path.name in {"docs.html", "preview-agreement.html"}:
                continue
            nav = html.split('<nav class="site-nav"', 1)[1].split("</nav>", 1)[0]
            footer = html.split("<footer", 1)[1]
            with self.subTest(page=str(path.relative_to(ROOT))):
                self.assertRegex(nav, r'href="/docs">Docs</a>')
                self.assertRegex(nav, r'href="/#/about">Meet the Team</a>')
                self.assertRegex(nav, r'href="/#/security">Trust &amp; security</a>')
                self.assertNotRegex(nav, r'Download the app')
                self.assertRegex(footer, r'href="/#/security">Trust &amp; security</a>')
                self.assertIn('aria-label="Signet7 home"', html)
                self.assertNotIn("qual.signet7.io", html.lower())

    def test_sitemap_covers_public_brochure_and_outlook(self) -> None:
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        skip = set(NOINDEX_PAGES)
        for path in root_html_pages():
            if path.name in skip:
                continue
            loc = (
                "https://signet7.io/"
                if path.name == "index.html"
                else f"https://signet7.io/{path.name.removesuffix('.html')}"
            )
            with self.subTest(loc=loc):
                self.assertIn(f"<loc>{loc}</loc>", sitemap)
        self.assertIn("<loc>https://signet7.io/outlook</loc>", sitemap)

    def test_docs_slash_redirect_has_no_inline_script(self) -> None:
        html = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
        self.assertIn('src="../assets/docs-redirect.js"', html)
        self.assertIn("/docs.html", html)
        self.assertNotIn("<script>", html)
        self.assertTrue((ROOT / "assets" / "docs-redirect.js").is_file())

    def test_download_fallback_version_matches_latest_json(self) -> None:
        meta = json.loads((ROOT / "files" / "latest.json").read_text(encoding="utf-8"))
        download = (ROOT / "download.html").read_text(encoding="utf-8")
        self.assertIn(f'id="build-version">{meta["version"]}</span>', download)

    def test_drawing_lightbox_covers_cad_plates(self) -> None:
        motion = (ROOT / "assets" / "motion.js").read_text(encoding="utf-8")
        self.assertIn(".art-trio img", motion)
        self.assertIn(".art-hero img", motion)
        self.assertIn("drawing-dialog", motion)
        css = (ROOT / "assets" / "site.css").read_text(encoding="utf-8")
        self.assertIn(".art-hero img", css)
        self.assertIn("@media (max-width: 720px)", css)
        self.assertIn(".header-register { display: none; }", css)
        billboard = re.search(r"\.nutshell \.billboard\s*\{[^}]+\}", css)
        self.assertIsNotNone(billboard)
        self.assertNotIn("line-height: 0.95", billboard.group(0))
        self.assertIn("line-height: 1.12", billboard.group(0))

    def test_indexable_brochure_pages_have_og_image(self) -> None:
        skip = {"404.html"}
        missing = []
        for path in root_html_pages():
            if path.name in skip:
                continue
            html = path.read_text(encoding="utf-8")
            if 'property="og:image"' not in html:
                missing.append(path.name)
        self.assertEqual(missing, [])

    def test_social_preview_uses_the_approved_mark(self) -> None:
        # The retired homepage plate claimed an on-chain ledger and IP54
        # compliance. It must not return as the card for brochure pages.
        approved = ("assets/og-image.png", "assets/og-link-two.png", "/og.jpg")
        wrong = []
        for path in root_html_pages():
            if path.name == "index.html":
                continue
            html = path.read_text(encoding="utf-8")
            for tag in re.findall(r'<meta property="og:image" content="([^"]+)"', html):
                if not any(mark in tag for mark in approved):
                    wrong.append((path.name, tag))
        self.assertEqual(wrong, [])

    def test_every_page_declares_the_same_dark_chrome(self) -> None:
        pages = list(root_html_pages()) + sorted(ROOT.glob("*/index.html"))
        off = []
        for path in pages:
            html = path.read_text(encoding="utf-8")
            if path.name == "index.html" or "http-equiv=\"refresh\"" in html:
                wanted = ('data-theme="dark"',)
            else:
                wanted = ('data-theme="dark"',)
            missing = [token for token in wanted if token not in html]
            if missing:
                off.append((str(path.relative_to(ROOT)), missing))
        self.assertEqual(off, [])

    def test_seal_is_described_as_tamper_evident(self) -> None:
        # A signature reveals alteration. It does not prevent it.
        for path in root_html_pages():
            self.assertNotIn("tamper-proof", path.read_text(encoding="utf-8"), path.name)

    def test_recipients_use_the_approved_phrasing(self) -> None:
        # customer-terms: "Recipients are not required to install".
        banned = ("never install", "never need it", "never need to install")
        wrong = []
        for path in root_html_pages():
            html = path.read_text(encoding="utf-8")
            wrong += [(path.name, phrase) for phrase in banned if phrase in html]
        self.assertEqual(wrong, [])

    def test_glossary_lives_on_the_faq(self) -> None:
        faq = (ROOT / "faq.html").read_text(encoding="utf-8")
        self.assertIn('id="plain-words"', faq)
        self.assertIn("it is not a verdict", faq)

    def test_programs_plate_is_marked_a_draft_and_carries_no_amount(self) -> None:
        programs = (ROOT / "programs.html").read_text(encoding="utf-8")
        self.assertIn("Amounts are not set, so the plate does not carry one.", programs)
        self.assertNotIn("1,200", programs)
        self.assertNotIn("$600", programs)

    def test_hero_bands_do_not_reintroduce_a_light_panel(self) -> None:
        css = (ROOT / "assets" / "site.css").read_text(encoding="utf-8")
        # #e7f1f8 was the paper panel behind the retired light blueprint. On a
        # dark page it also drove drawing captions to 1.35:1 contrast.
        self.assertNotIn("#e7f1f8", css)

    def test_retired_homepage_plate_is_gone(self) -> None:
        self.assertFalse((ROOT / "assets" / "blueprint" / "homepage.jpg").exists())
        for path in root_html_pages():
            self.assertNotIn(
                "blueprint/homepage.jpg", path.read_text(encoding="utf-8"), path.name
            )

    def test_homepage_bundle_still_routes_inner_pages(self) -> None:
        from tests.site_html import home_served_copy

        home = home_served_copy()
        self.assertIn("product", home)
        self.assertIn("docs", home)


if __name__ == "__main__":
    unittest.main()
