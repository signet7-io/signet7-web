from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def root_html_pages() -> list[Path]:
    """Public brochure pages. Skip Google Search Console verification files."""
    return [path for path in sorted(ROOT.glob("*.html")) if not path.name.startswith("google")]


_PUBLIC_TEXT_SUFFIXES = {
    ".html",
    ".htm",
    ".css",
    ".js",
    ".svg",
    ".json",
    ".xml",
    ".txt",
    ".md",
}


def public_text_assets() -> list[Path]:
    """Textual files GitHub Pages can serve (site pages, assets, outlook, docs)."""
    paths: list[Path] = []
    paths.extend(root_html_pages())
    paths.extend(sorted(ROOT.glob("*/index.html")))
    for sub in ("assets", "outlook", "docs", "files"):
        base = ROOT / sub
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if path.is_file() and path.suffix.lower() in _PUBLIC_TEXT_SUFFIXES:
                paths.append(path)
    for name in ("install.ps1", "install.sh", "sitemap.xml", "robots.txt"):
        path = ROOT / name
        if path.is_file():
            paths.append(path)
    seen: set[Path] = set()
    unique: list[Path] = []
    for path in paths:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        unique.append(path)
    return unique
