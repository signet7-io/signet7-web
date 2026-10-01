#!/usr/bin/env python3
"""Sanitizer for public Apple Mail doc screenshots (from git-stored captures)."""
from __future__ import annotations

import subprocess
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

# First docs commit on the Apple Mail PR branch (user capture, pre-redaction).
_CAPTURE_COMMIT = "e2213ca"

SIDEBAR_BG = (37, 38, 39)
SIDEBAR_TITLE = (255, 255, 255)
# Text column in the accounts sidebar (full width through trailing name glyphs).
SIDEBAR_TEXT_X0 = 118
SIDEBAR_TEXT_X1 = 320
# Selected-row blue fill spans the full selection bar (see capture at y≈655).
SELECTED_TEXT_X0 = 47
SELECTED_TEXT_X1 = 320

FONT_PATHS = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
)


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in FONT_PATHS:
        if Path(path).is_file():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _git_png(commit: str, repo_path: str) -> Image.Image:
    data = subprocess.check_output(
        ["git", "-C", str(ROOT), "show", f"{commit}:{repo_path}"],
    )
    return Image.open(BytesIO(data)).convert("RGB")


def _field_fill(im: Image.Image, box: tuple[int, int, int, int]) -> tuple[int, int, int]:
    x0, y0, x1, y1 = box
    pts = [im.getpixel((x0 + 8, y0 + (y1 - y0) // 2))[:3], im.getpixel((x1 - 12, y0 + (y1 - y0) // 2))[:3]]
    rs = sorted(p[0] for p in pts)
    gs = sorted(p[1] for p in pts)
    bs = sorted(p[2] for p in pts)
    return rs[0], gs[0], bs[0]


def _paint_field(
    draw: ImageDraw.ImageDraw,
    im: Image.Image,
    box: tuple[int, int, int, int],
    text: str,
    *,
    font_size: int = 26,
) -> None:
    x0, y0, x1, y1 = box
    fill = _field_fill(im, box)
    draw.rectangle([x0, y0, x1, y1], fill=fill)
    font = _font(font_size)
    draw.text((x0 + 10, y0 + (y1 - y0 - font_size) // 2 - 2), text, fill=(220, 222, 228), font=font)


def _label_in_band(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    *,
    fill: tuple[int, int, int],
    font_size: int = 17,
) -> None:
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], fill=fill)
    font = _font(font_size)
    bbox = draw.textbbox((0, 0), text, font=font)
    th = bbox[3] - bbox[1]
    ty = y0 + (y1 - y0 - th) // 2 - 1
    draw.text((x0 + 4, ty), text, fill=SIDEBAR_TITLE, font=font)


def _repaint_selected_company_inbox(im: Image.Image, draw: ImageDraw.ImageDraw) -> None:
    """Wipe the full title band on the selected row; leave the IMAP subtitle intact."""
    y0, y1 = 642, 677
    blue = im.getpixel((250, 694))[:3]
    draw.rectangle([SELECTED_TEXT_X0, y0, SELECTED_TEXT_X1, y1], fill=blue)
    text = "Company inbox"
    font = _font(15)
    bbox = draw.textbbox((0, 0), text, font=font)
    th = bbox[3] - bbox[1]
    tx = 128
    ty = y0 + (y1 - y0 - th) // 2
    draw.text((tx, ty), text, fill=SIDEBAR_TITLE, font=font)


def _repaint_personal_account(
    draw: ImageDraw.ImageDraw,
    im: Image.Image,
    *,
    wipe_y0: int,
    wipe_y1: int,
    label_y0: int,
    label_y1: int,
) -> None:
    """Clear title + leftover name smudges; redraw Personal; keep IMAP subtitle."""
    bg = im.getpixel((240, wipe_y0 + 2))[:3]
    draw.rectangle([SIDEBAR_TEXT_X0, wipe_y0, SIDEBAR_TEXT_X1, wipe_y1], fill=bg)
    _label_in_band(
        draw,
        (128, label_y0, SIDEBAR_TEXT_X1 - 4, label_y1),
        "Personal",
        fill=bg,
        font_size=17,
    )


def _sanitize_sidebar(im: Image.Image) -> None:
    draw = ImageDraw.Draw(im)
    _repaint_personal_account(
        draw, im, wipe_y0=407, wipe_y1=449, label_y0=407, label_y1=433
    )
    _repaint_personal_account(
        draw, im, wipe_y0=486, wipe_y1=529, label_y0=486, label_y1=512
    )
    _repaint_personal_account(
        draw, im, wipe_y0=566, wipe_y1=609, label_y0=566, label_y1=592
    )
    _repaint_selected_company_inbox(im, draw)


def sanitize_server_settings(path: Path) -> None:
    im = _git_png(_CAPTURE_COMMIT, "assets/docs-apple-mail-server-settings.png")
    draw = ImageDraw.Draw(im)
    _paint_field(draw, im, (645, 352, 1290, 388), "user@example.com", font_size=27)
    _paint_field(draw, im, (645, 866, 1290, 900), "user@example.com", font_size=27)
    _sanitize_sidebar(im)
    im.save(path, optimize=True)


def sanitize_add_account(path: Path) -> None:
    im = _git_png(_CAPTURE_COMMIT, "assets/docs-apple-mail-add-account.png")
    _sanitize_sidebar(im)
    im.save(path, optimize=True)


def sanitize_desktop_listening(path: Path) -> None:
    im = _git_png(_CAPTURE_COMMIT, "assets/docs-signet7-mailbox-helper.png")
    draw = ImageDraw.Draw(im)
    _paint_field(draw, im, (518, 638, 1180, 676), "user@example.com", font_size=28)
    _paint_field(
        draw,
        im,
        (518, 998, 1185, 1036),
        "user@example.com, company@example.com",
        font_size=24,
    )
    im.save(path, optimize=True)


def main() -> None:
    sanitize_server_settings(ASSETS / "docs-apple-mail-server-settings.png")
    sanitize_add_account(ASSETS / "docs-apple-mail-add-account.png")
    sanitize_desktop_listening(ASSETS / "docs-signet7-mailbox-helper.png")
    print("Sanitized three Apple Mail doc figures.")


if __name__ == "__main__":
    main()
