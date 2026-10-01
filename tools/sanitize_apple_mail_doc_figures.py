#!/usr/bin/env python3
"""One-off sanitizer for public Apple Mail doc screenshots."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

FONT_PATHS = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
)


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in FONT_PATHS:
        if Path(path).is_file():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _median_rgb(samples: list[tuple[int, int, int]]) -> tuple[int, int, int]:
    rs = sorted(s for s, _, _ in samples)
    gs = sorted(g for _, g, _ in samples)
    bs = sorted(b for _, _, b in samples)
    mid = len(samples) // 2
    return rs[mid], gs[mid], bs[mid]


def _field_fill(im: Image.Image, box: tuple[int, int, int, int]) -> tuple[int, int, int]:
    x0, y0, x1, y1 = box
    pts = [
        im.getpixel((x0 + 8, y0 + (y1 - y0) // 2)),
        im.getpixel((x0 + 20, y0 + (y1 - y0) // 2)),
        im.getpixel((x1 - 12, y0 + (y1 - y0) // 2)),
    ]
    return _median_rgb([tuple(p[:3]) for p in pts])


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


def _paint_sidebar_title(
    draw: ImageDraw.ImageDraw,
    im: Image.Image,
    box: tuple[int, int, int, int],
    text: str,
    *,
    selected: bool = False,
    font_size: int = 22,
) -> None:
    x0, y0, x1, y1 = box
    if selected:
        fill = (0, 88, 200)
    else:
        fill = (40, 40, 42)
    draw.rectangle([x0, y0, x1, y1], fill=fill)
    font = _font(font_size)
    color = (255, 255, 255) if selected else (210, 212, 218)
    draw.text((x0 + 4, y0 + (y1 - y0 - font_size) // 2 - 1), text, fill=color, font=font)


def _erase_box(
    draw: ImageDraw.ImageDraw,
    im: Image.Image,
    box: tuple[int, int, int, int],
    *,
    fill: tuple[int, int, int] | None = None,
) -> None:
    if fill is None:
        fill = _field_fill(im, box)
    draw.rectangle(box, fill=fill)


def sanitize_server_settings(path: Path) -> None:
    im = Image.open(path).convert("RGB")
    draw = ImageDraw.Draw(im)
    # Incoming / outgoing username fields (value area only).
    _paint_field(draw, im, (612, 352, 1290, 388), "user@example.com", font_size=27)
    _paint_field(draw, im, (612, 864, 1290, 900), "user@example.com", font_size=27)
    _erase_box(draw, im, (605, 832, 955, 862), fill=(36, 36, 38))
    _erase_box(draw, im, (605, 766, 955, 798), fill=(36, 36, 38))
    # Sidebar account titles (personal nicknames / names).
    _paint_sidebar_title(draw, im, (128, 398, 268, 434), "Personal")
    _paint_sidebar_title(draw, im, (128, 488, 268, 524), "Personal")
    _paint_sidebar_title(draw, im, (128, 582, 268, 618), "Personal")
    draw.rectangle([55, 628, 285, 720], fill=(0, 88, 200))
    font = _font(22)
    draw.text((128, 652), "Company inbox", fill=(255, 255, 255), font=font)
    im.save(path, optimize=True)


def sanitize_add_account(path: Path) -> None:
    im = Image.open(path).convert("RGB")
    draw = ImageDraw.Draw(im)
    _paint_sidebar_title(draw, im, (128, 398, 268, 434), "Personal")
    _paint_sidebar_title(draw, im, (128, 488, 268, 524), "Personal")
    _paint_sidebar_title(draw, im, (128, 582, 268, 618), "Personal")
    draw.rectangle([55, 628, 285, 720], fill=(0, 88, 200))
    font = _font(22)
    draw.text((128, 652), "Company inbox", fill=(255, 255, 255), font=font)
    im.save(path, optimize=True)


def sanitize_desktop_listening(path: Path) -> None:
    im = Image.open(path).convert("RGB")
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
