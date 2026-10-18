"""Claims the public export must not make.

One phrase, one reason. Scan HTML, JS, JSON, and markdown the site ships.
register.html may say VSN; every other public page may not.

Do not ban honest negations such as "not permission to pay".
"""

from __future__ import annotations

from pathlib import Path

# phrase, reason, paths allowed to contain the phrase (empty = nowhere)
FORBIDDEN: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("is safe to pay", "A check is not payment approval", ()),
    ("Verified is not safe", "Retired hedge line", ()),
    ("Unknown is not fraud", "Retired hedge line", ()),
    ("Listed is not trusted", "Retired hedge line", ()),
    ("you still decide", "Hedge leftover; say the two facts", ()),
    ("then you decide", "Hedge leftover; say the two facts", ()),
    ("you're safe", "A check is not a safety verdict", ()),
    ("you’re safe", "A check is not a safety verdict", ()),
    ("free forever", "Preview is not a forever price", ()),
    ("Placeholder $", "Do not publish placeholder prices", ()),
    ("$12/month", "Retired public price", ()),
    ("$29/month", "Retired public price", ()),
    ("$99/month", "Retired public price", ()),
    ("$1,000/month", "Retired public price", ()),
    ("$12 / $29 / $99", "Retired public price ladder", ()),
    ("money mailbox", "Retired product name", ()),
    ("money inbox", "Retired product name", ()),
    ("Inbox Watch", "Retired product name", ()),
    ("pip install", "Public site is not a pip install", ()),
    ("pypi.org", "Public site is not a pip install", ()),
    ("admin.signet7.io", "Admin host is not public", ()),
    ("qual.signet7.io", "Qual host is not public", ()),
    ("tamper-proof", "A seal is tamper-evident, not proof against change", ()),
    ("Recipients never install", "Say: Recipients are not required to install", ()),
    ("never need to install", "Say: Recipients are not required to install", ()),
    ("never need it", "Say: Recipients are not required to install", ()),
    ("one listing covers every mailbox", "Listings are per address", ()),
    ("covers every mailbox", "Listings are per address", ()),
    ("data-buddy", "Retired mascot", ()),
    ("five stars", "No fake ratings", ()),
    ("what our customers say", "No fake testimonials", ()),
    ("googletagmanager", "No analytics tags", ()),
    ("gtag(", "No analytics tags", ()),
    ('id="cookie-banner"', "No cookie banner", ()),
    ("VSN", "Internal name; keep the /vsn URL", ("register.html",)),
    ("Qual", "Retired environment name", ()),
)

SCAN_SUFFIXES = {".html", ".js", ".md", ".json"}


def claim_assets(paths: list[Path]) -> list[Path]:
    return [path for path in paths if path.suffix.lower() in SCAN_SUFFIXES]


def allowed_for(phrase: str, path: Path) -> bool:
    for token, _reason, allowed in FORBIDDEN:
        if token == phrase:
            return path.name in allowed
    return False
