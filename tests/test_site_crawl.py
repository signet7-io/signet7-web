from __future__ import annotations

import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from tests.site_html import ROOT, root_html_pages


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
            nav = html.split('<nav class="site-nav"', 1)[1].split("</nav>", 1)[0]
            footer = html.split("<footer", 1)[1]
            with self.subTest(page=str(path.relative_to(ROOT))):
                self.assertRegex(nav, r'href="(\.\./)?record">Keep the file</a>')
                self.assertRegex(nav, r'href="(\.\./)?trust-center">Trust center</a>')
                self.assertNotRegex(nav, r'href="(\.\./)?download">Download</a>')
                self.assertRegex(footer, r'href="(\.\./)?trust-center">Trust center</a>')
                self.assertIn('aria-label="Signet7 home"', html)
                self.assertNotIn("qual.signet7.io", html.lower())

    def test_sitemap_covers_public_brochure_and_outlook(self) -> None:
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        skip = {"terms.html", "disclaimer.html", "404.html"}
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

    def test_homepage_below_fold_plates_lazy_load(self) -> None:
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        hero = home.split('id="features"', 1)[0]
        self.assertIn("fetchpriority=\"high\"", hero)
        self.assertNotIn("loading=\"lazy\"", hero)
        below = home.split('id="features"', 1)[1]
        self.assertGreaterEqual(below.count('loading="lazy"'), 6)

    def test_homepage_drawing_cards_keep_text_links(self) -> None:
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        features = home.split('id="features"', 1)[1].split("</section>", 1)[0]
        self.assertIn('<h3><a href="check">Check a message</a></h3>', features)
        self.assertIn('<h3><a href="download">List the work email</a></h3>', features)
        self.assertIn('<h3><a href="record">Keep the file</a></h3>', features)
        play = home.split('id="play"', 1)[1].split("</section>", 1)[0]
        self.assertIn('<h3><a href="product">Product</a></h3>', play)
        self.assertIn('<h3><a href="programs">Programs</a></h3>', play)
        self.assertIn('<h3><a href="docs.html">Docs</a></h3>', play)


if __name__ == "__main__":
    unittest.main()
