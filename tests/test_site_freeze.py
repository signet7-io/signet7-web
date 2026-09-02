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
        self.assertIn("sell-hero", self.home)
        self.assertIn("zoom/01.jpg", self.home)
        self.assertIn("data-zoom-pin", self.home)
        self.assertNotIn("door-loop.mp4", self.home.split("seasons-scene")[0])
        self.assertIn("High-stakes email, finally", self.home)
        self.assertIn("provable", self.home)
        self.assertNotIn("Make email something you can prove", self.home)
        self.assertNotIn("not just trust", self.home)
        self.assertIn("Signet7 is the cryptographic check for high-stakes email", self.home)

    def test_name_story_lives_on_about_and_homepage_studies(self) -> None:
        about = (ROOT / "about.html").read_text(encoding="utf-8")
        self.assertIn("A signet is a seal. The 7 is the long memory.", about)
        self.assertIn("You need to know it is authentic.", about)
        self.assertIn("You need proof of exactly what you received.", about)
        self.assertIn('id="play"', self.home)
        play = self.home.split('id="play"', 1)[1].split('id="demo"', 1)[0]
        self.assertIn("A signet is a seal. The 7 is the long memory.", play)
        hero = self.home.split("<h1", 1)[1].split("</section>", 1)[0]
        self.assertNotIn("A signet is a seal. The 7 is the long memory.", hero)
        for banned in ("data-wave-pin", "data-crawl", "wave-pin", "crawl-stage"):
            self.assertNotIn(banned, self.home)
            self.assertNotIn(banned, self.css)

    def test_seasons_stay_after_the_hero(self) -> None:
        self.assertIn("sell-hero", self.home)
        self.assertNotIn("seasons-scene", self.home)
        self.assertNotIn("signet7-circuit.jpg", self.home)
        self.assertNotIn("tech-scene.jpg", self.home)
        self.assertNotIn("tech-scene-dark.jpg", self.home)
        self.assertNotIn("door-loop.mp4", self.home)

    def test_frozen_chrome_tokens(self) -> None:
        self.assertIn("--nav-h: 72px;", self.css)
        self.assertIn("--nav-seal: 46px;", self.css)
        self.assertIn("--nav-word: 20px;", self.css)
        self.assertIn("--nav-type: 16px;", self.css)

    def test_loop_on_every_page_under_the_hero(self) -> None:
        self.assertIn("calc(12px + 1.5in)", self.css)
        for path in sorted(ROOT.glob("*.html")):
            html = path.read_text(encoding="utf-8")
            with self.subTest(page=path.name):
                pin = "assets/site.css?v=20260901d"
                self.assertIn(pin, html)
                self.assertNotIn("seasons-scene", html)
                self.assertNotIn("door-loop.mp4", html)
                self.assertNotIn("signet7-circuit.jpg", html)

    def test_homepage_mute_study_films(self) -> None:
        self.assertIn("media-src 'self'", self.home)
        facts_end = self.home.find("</section>", self.home.find('class="facts"'))
        demo = self.home.find('id="demo"')
        play = self.home.find('id="play"')
        self.assertTrue(0 < facts_end < play < demo)
        self.assertIn("assets/studies/seal.mp4", self.home)
        self.assertIn("assets/studies/network.mp4", self.home)
        self.assertIn("assets/studies/stamp.mp4", self.home)
        self.assertIn("autoplay muted loop playsinline", self.home)
        self.assertIn(".study-grid", self.css)
        self.assertIn('url("studies/seal.jpg")', self.css)
        self.assertIn("High-stakes email, finally", self.home)
        self.assertIn('id="created"', self.home)
        self.assertIn("That file is the record.", self.home)
        self.assertIn("Looks ordinary", self.home)

    def test_footer_rights_and_wrongs(self) -> None:
        line = "All rights reserved, All wrongs revenged."
        for path in sorted(ROOT.glob("*.html")):
            with self.subTest(page=path.name):
                self.assertIn(line, path.read_text(encoding="utf-8"))
