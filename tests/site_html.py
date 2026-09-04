from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def root_html_pages() -> list[Path]:
    """Public brochure pages. Skip Google Search Console verification files."""
    return [path for path in sorted(ROOT.glob("*.html")) if not path.name.startswith("google")]
