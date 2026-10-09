"""Check result labels. Must stay in lockstep with signet7-core _FACE / _LIST_FACE."""

from __future__ import annotations

from pathlib import Path

from tests.site_html import ROOT

SEAL_RESULTS = (
    "Unchanged since sealed",
    "Changed since sealed",
    "Not sealed",
)

ADDRESS_RESULTS = (
    "Address listed",
    "Address not listed",
    "Address mismatch",
)

CURRENT_LABELS = SEAL_RESULTS + ADDRESS_RESULTS

# Exact chip / pane strings the site used to ship. Do not match ordinary English
# such as "the words still matched".
RETIRED_LABELS = (
    "Wording same",
    "Wording changed",
    "Words match",
    "Words do not match",
    "No seal is ordinary mail",
    "Listed for this address",
    "Listing doesn’t match this address",
    "Listing doesn't match this address",
    "Listed, Not listed, or Listing",
)

MARK_FILES = (
    "sealed-unchanged.jpg",
    "sealed-changed.jpg",
    "not-sealed.jpg",
    "address-listed.jpg",
    "address-not-listed.jpg",
    "address-mismatch.jpg",
)

# Pages and scripts that name the six results for a recipient.
RESULT_SURFACES = (
    ROOT / "check.html",
    ROOT / "faq.html",
    ROOT / "product.html",
    ROOT / "vsn.html",
    ROOT / "docs.html",
    ROOT / "outlook" / "taskpane.js",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")
