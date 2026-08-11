from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from PIL import Image, ImageOps
from playwright.sync_api import sync_playwright

PAGES = ("index.html", "product.html", "trust.html", "integrations.html", "programs.html", "pilot.html")
VIEWPORTS = {
    "desktop": {"width": 1440, "height": 1000},
    "mobile": {"width": 390, "height": 844},
}
CHROME = Path(os.environ.get("CHROME_PATH", "C:/Program Files/Google/Chrome/Application/chrome.exe"))


def contact_sheet(paths: list[Path], destination: Path, thumb_width: int) -> None:
    thumbs = []
    for path in paths:
        image = Image.open(path).convert("RGB")
        ratio = thumb_width / image.width
        height = min(int(image.height * ratio), 2400)
        thumbs.append(ImageOps.fit(image, (thumb_width, height), method=Image.Resampling.LANCZOS, centering=(0.5, 0.0)))
    gap = 24
    canvas = Image.new("RGB", (len(thumbs) * (thumb_width + gap) + gap, max(im.height for im in thumbs) + 2 * gap), "#dfe7ea")
    for index, image in enumerate(thumbs):
        canvas.paste(image, (gap + index * (thumb_width + gap), gap))
    canvas.save(destination, quality=90, optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8765")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    report: dict[str, dict] = {}

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, executable_path=str(CHROME))
        for viewport_name, viewport in VIEWPORTS.items():
            context = browser.new_context(viewport=viewport, device_scale_factor=1)
            report[viewport_name] = {}
            screenshots: list[Path] = []
            for page_name in PAGES:
                page = context.new_page()
                response = page.goto(f"{args.base_url}/{page_name}", wait_until="networkidle")
                page.wait_for_timeout(250)
                overflow = page.evaluate("document.documentElement.scrollWidth > window.innerWidth")
                title = page.title()
                path = output / f"{viewport_name}-{page_name.replace('.html', '')}.png"
                page.screenshot(path=str(path), full_page=True)
                screenshots.append(path)
                report[viewport_name][page_name] = {
                    "status": response.status if response else None,
                    "title": title,
                    "horizontal_overflow": overflow,
                    "scroll_width": page.evaluate("document.documentElement.scrollWidth"),
                    "viewport_width": viewport["width"],
                }
                page.close()
            contact_sheet(screenshots, output / f"{viewport_name}-contact-sheet.jpg", 320 if viewport_name == "desktop" else 260)
            context.close()
        browser.close()

    (output / "browser-qa.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
