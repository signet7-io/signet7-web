#!/usr/bin/env python3
"""Serve the export the way GitHub Pages does.

Site links are extensionless (`href="product"`). Pages resolves those to
`product.html`; `python3 -m http.server` returns 404 instead. This helper
matches Pages so local link checks mean something.
"""
from __future__ import annotations

import argparse
import functools
import http.server
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PagesHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path: str) -> str:
        resolved = Path(super().translate_path(path))
        if not resolved.exists() and not resolved.suffix:
            sibling = resolved.with_name(resolved.name + ".html")
            if sibling.is_file():
                return str(sibling)
        return str(resolved)

    def send_error(self, code: int, message: str | None = None, explain: str | None = None) -> None:
        custom = ROOT / "404.html"
        if code == 404 and custom.is_file():
            body = custom.read_bytes()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)
            return
        super().send_error(code, message, explain)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--bind", default="127.0.0.1")
    args = parser.parse_args()

    handler = functools.partial(PagesHandler, directory=str(ROOT))
    with http.server.ThreadingHTTPServer((args.bind, args.port), handler) as httpd:
        print(f"Serving {ROOT} at http://{args.bind}:{args.port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
