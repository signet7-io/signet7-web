from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SiteFreeze20260822Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.home = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.css = (ROOT / "assets" / "site.css").read_text(encoding="utf-8")

    def test_door_keeps_people_behind_type(self) -> None:
        self.assertIn('class="sell-hero"', self.home)
        self.assertIn("people-light.png", self.home)
        self.assertIn("people-dark.png", self.home)
        self.assertIn("Make email something you can", self.home)
        self.assertNotIn("not just trust", self.home)
        self.assertIn("Signet7 is the cryptographic check for high-stakes email", self.home)

    def test_name_bridge_not_a_crawl(self) -> None:
        self.assertIn('class="name-bridge"', self.home)
        self.assertIn("A signet is a seal. The 7 is the long memory.", self.home)
        self.assertIn("You need to know it is authentic.", self.home)
        self.assertIn("You need proof of exactly what you received.", self.home)
        for banned in ("data-wave-pin", "data-crawl", "wave-pin", "crawl-stage"):
            self.assertNotIn(banned, self.home)
            self.assertNotIn(banned, self.css)

    def test_seasons_stay_after_the_bridge(self) -> None:
        bridge = self.home.index('class="name-bridge"')
        seasons = self.home.index("tech-scene.jpg")
        self.assertGreater(seasons, bridge)
        self.assertIn("tech-scene-dark.jpg", self.home)
        self.assertTrue((ROOT / "assets" / "tech-scene.jpg").is_file())
        self.assertTrue((ROOT / "assets" / "tech-scene-dark.jpg").is_file())

    def test_frozen_chrome_tokens(self) -> None:
        self.assertIn("--nav-h: 72px;", self.css)
        self.assertIn("--nav-seal: 46px;", self.css)
        self.assertIn("--nav-word: 20px;", self.css)
        self.assertIn("--nav-type: 16px;", self.css)

    def test_footer_rights_and_wrongs(self) -> None:
        line = "All rights reserved, All wrongs revenged."
        for path in sorted(ROOT.glob("*.html")):
            with self.subTest(page=path.name):
                self.assertIn(line, path.read_text(encoding="utf-8"))
