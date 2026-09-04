from __future__ import annotations

import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]


class _Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(str(values["id"]))
        for name in ("href", "src"):
            value = values.get(name)
            if value:
                self.links.append(value)


class PublicLinkContractTests(unittest.TestCase):
    def test_every_local_link_stays_inside_the_public_export_and_resolves(self) -> None:
        documents: dict[Path, _Links] = {}
        for path in sorted(ROOT.glob("*.html")):
            parser = _Links()
            parser.feed(path.read_text(encoding="utf-8"))
            documents[path.resolve()] = parser

        failures: list[str] = []
        for source, parser in documents.items():
            for raw in parser.links:
                parsed = urlsplit(raw)
                if parsed.scheme in {"http", "https", "mailto", "tel", "data", "javascript"}:
                    continue
                target_path = unquote(parsed.path)
                if not target_path:
                    target = source
                elif target_path == "/":
                    target = ROOT / "index.html"
                else:
                    rel = target_path[1:] if target_path.startswith("/") else target_path
                    target = (ROOT / rel).resolve()
                    try:
                        target.relative_to(ROOT.resolve())
                    except ValueError:
                        failures.append(f"{source.name}: escapes public export: {raw}")
                        continue
                if target.is_dir():
                    sibling_html = target.with_suffix(".html")
                    index = target / "index.html"
                    if sibling_html.is_file():
                        target = sibling_html
                    elif index.is_file():
                        target = index
                if not target.exists() and target.suffix == "":
                    html_target = target.with_name(target.name + ".html")
                    if html_target.exists():
                        target = html_target
                if not target.exists():
                    failures.append(f"{source.name}: missing target: {raw}")
                    continue
                if parsed.fragment and target.suffix.lower() == ".html":
                    target_parser = documents.get(target)
                    if target_parser is None:
                        target_parser = _Links()
                        target_parser.feed(target.read_text(encoding="utf-8"))
                        documents[target] = target_parser
                    if parsed.fragment not in target_parser.ids:
                        failures.append(f"{source.name}: missing anchor: {raw}")

        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
