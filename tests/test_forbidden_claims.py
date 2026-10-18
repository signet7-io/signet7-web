from __future__ import annotations

import re
import unittest

from tests.forbidden_claims import FORBIDDEN, allowed_for, claim_assets
from tests.site_html import public_text_assets, root_html_pages


class ForbiddenClaimsTests(unittest.TestCase):
    def test_public_export_does_not_make_retired_claims(self) -> None:
        for path in claim_assets(list(public_text_assets())):
            text = path.read_text(encoding="utf-8", errors="replace")
            lowered = text.lower()
            for phrase, reason, _allowed in FORBIDDEN:
                if allowed_for(phrase, path):
                    continue
                with self.subTest(asset=path.name, phrase=phrase, reason=reason):
                    self.assertNotIn(phrase, text)
                    if phrase == phrase.lower():
                        self.assertNotIn(phrase, lowered)

    def test_register_keeps_the_vsn_line(self) -> None:
        pages = {path.name: path.read_text(encoding="utf-8") for path in root_html_pages()}
        self.assertIn("Now with VSN.", pages["register.html"])
        self.assertNotIn("Now with VSN.", pages["index.html"])

    def test_public_copy_does_not_overclaim_safety(self) -> None:
        combined = "\n".join(path.read_text(encoding="utf-8") for path in root_html_pages())
        visible = re.sub(r"<[^>]+>", " ", combined).lower()
        forbidden = (
            r"signet7\s+(?:prevents|blocks|stops)\s+(?:phishing|fraud|scams|malware|ransomware)",
            r"signet7\s+makes\s+(?:email|messages?|actions?)\s+safe",
            r"verified\s+means\s+safe",
            r"unverified\s+means\s+fraud",
            r"hipaa compliant email",
            r"seven-year retention by default",
            r"no integration required",
        )
        for pattern in forbidden:
            with self.subTest(pattern=pattern):
                self.assertIsNone(re.search(pattern, visible))
