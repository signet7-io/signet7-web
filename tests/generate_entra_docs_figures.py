"""Schematic Docs figures. No Azure portal screenshots."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
BG = (11, 18, 28)
INK = (232, 238, 244)
MUTED = (158, 201, 220)
LINE = (80, 140, 160)
BOX = (20, 32, 48)
ACCENT = (126, 214, 240)


def _font(size: int):
    for name in ("Arial.ttf", "Helvetica.ttc", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _box(draw: ImageDraw.ImageDraw, xy, title: str, body: str, font_h, font_s) -> None:
    draw.rounded_rectangle(xy, radius=10, fill=BOX, outline=LINE, width=2)
    x0, y0, x1, y1 = xy
    draw.text((x0 + 16, y0 + 12), title, fill=ACCENT, font=font_h)
    draw.text((x0 + 16, y0 + 40), body, fill=INK, font=font_s)


def _arrow(draw: ImageDraw.ImageDraw, x0: int, y: int, x1: int) -> None:
    draw.line((x0, y, x1, y), fill=ACCENT, width=2)
    draw.polygon([(x1, y), (x1 - 8, y - 5), (x1 - 8, y + 5)], fill=ACCENT)


def flow() -> None:
    img = Image.new("RGB", (960, 420), BG)
    draw = ImageDraw.Draw(img)
    h, s = _font(16), _font(13)
    _box(draw, (24, 150, 200, 270), "Outlook", "People write here", h, s)
    _box(draw, (248, 40, 456, 160), "Add-in", "Seal this draft", h, s)
    _box(draw, (248, 260, 456, 380), "Desktop", "127.0.0.1:2525", h, s)
    _box(draw, (504, 150, 700, 270), "Entra", "Consent only", h, s)
    _box(draw, (748, 40, 936, 160), "Graph watch", "Verify named mail", h, s)
    _box(draw, (748, 260, 936, 380), "Hosted Signet7", "seal / verify APIs", h, s)
    _arrow(draw, 200, 190, 248)
    draw.line((352, 160, 352, 260), fill=ACCENT, width=2)
    _arrow(draw, 456, 210, 504)
    _arrow(draw, 700, 190, 748)
    caption = _font(14)
    draw.text((24, 16), "Entra grants Graph permission. It does not sign mail.", fill=MUTED, font=caption)
    img.save(ASSETS / "docs-entra-flow.png")


def permissions() -> None:
    img = Image.new("RGB", (720, 360), BG)
    draw = ImageDraw.Draw(img)
    h, s = _font(18), _font(15)
    draw.text((24, 20), "Entra app (single-tenant, public client)", fill=ACCENT, font=h)
    rows = (
        ("offline_access", "Keep a refresh token in the OS store"),
        ("Mail.Read", "Watch named work emails"),
        ("Mail.Send", "Send sealed MIME without rebuild"),
        ("Admin consent", "Once per tenant. Human step."),
    )
    y = 70
    for title, body in rows:
        _box(draw, (24, y, 696, y + 58), title, body, h, s)
        y += 68
    img.save(ASSETS / "docs-entra-permissions.png")


if __name__ == "__main__":
    ASSETS.mkdir(parents=True, exist_ok=True)
    flow()
    permissions()
    print("wrote", ASSETS / "docs-entra-flow.png")
    print("wrote", ASSETS / "docs-entra-permissions.png")
