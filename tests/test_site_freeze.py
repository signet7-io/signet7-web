from __future__ import annotations

import unittest

from tests.site_html import ROOT, root_html_pages


class SiteFreeze20260822Tests(unittest.TestCase):
    """Door unlocked 2026-09-15: CAD blueprint envelope, same H1 and nav chrome."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.home = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.css = (ROOT / "assets" / "site.css").read_text(encoding="utf-8")

    def test_door_keeps_people_behind_type(self) -> None:
        self.assertIn("sell-hero", self.home)
        self.assertIn("cad-scene", self.home)
        self.assertIn("cad-envelope", self.home)
        self.assertIn("assets/blueprint/homepage.jpg?v=20260916j", self.home)
        self.assertNotIn("people-dark.png", self.home)
        self.assertNotIn("people-light.png", self.home)
        self.assertNotIn("people-scene", self.home)
        self.assertNotIn("zoom/01.jpg", self.home)
        self.assertIn("Check an important email before you act", self.home)
        self.assertIn("before you act", self.home)
        self.assertIn("<h1 id=\"hero-title\" class=\"billboard\">Signet7 is the cryptographic seal and check for high-stakes email.</h1>", self.home)
        self.assertNotIn("Make email something you can prove", self.home)
        self.assertNotIn("not just trust", self.home)
        self.assertIn("Signet7 is the cryptographic seal and check for high-stakes email", self.home)

    def test_name_story_lives_on_about_and_homepage_studies(self) -> None:
        about = (ROOT / "about.html").read_text(encoding="utf-8")
        self.assertIn("The seal is on the message. You can show later that the words still matched.", about)
        self.assertIn('id="play"', self.home)
        play = self.home.split('id="play"', 1)[1]
        self.assertIn("The drawings", play)
        hero = self.home.split("<h1", 1)[1].split("</section>", 1)[0]
        self.assertNotIn("A signet is a seal. The 7 is the long memory.", hero)

    def test_seasons_stay_after_the_hero(self) -> None:
        self.assertIn("sell-hero", self.home)
        self.assertNotIn("seasons-scene", self.home)
        self.assertNotIn("signet7-circuit.jpg", self.home)
        self.assertNotIn("door-loop.mp4", self.home)

    def test_frozen_chrome_tokens(self) -> None:
        self.assertIn("--nav-h: 72px;", self.css)
        self.assertIn("--nav-seal: 46px;", self.css)
        self.assertIn("--nav-word: 20px;", self.css)
        self.assertIn("--nav-type: 16px;", self.css)

    def test_loop_on_every_page_under_the_hero(self) -> None:
        self.assertIn('html[data-theme="dark"]', self.css)
        for path in root_html_pages():
            html = path.read_text(encoding="utf-8")
            with self.subTest(page=path.name):
                self.assertIn("assets/site.css?v=20260916j", html)
                self.assertIn('data-theme="dark"', html)
                self.assertNotIn("door-loop.mp4", html)
                self.assertNotIn("signet7-circuit.jpg", html)

    def test_homepage_mute_study_films(self) -> None:
        self.assertIn("media-src 'self'", self.home)
        self.assertIn('id="play"', self.home)
        self.assertIn("assets/blueprint/check.jpg?v=20260916j", self.home)
        self.assertIn("assets/blueprint/evidence.jpg?v=20260916j", self.home)
        self.assertIn("assets/blueprint/howto.jpg?v=20260916j", self.home)
        self.assertNotIn("assets/studies/seal.mp4", self.home)
        self.assertIn("Check an important email before you act", self.home)
        self.assertNotIn("Who uses it", self.home)
        self.assertNotIn("Law, title, construction, payroll, finance.", self.home)
        self.assertNotIn("You keep the result.", self.home)
        self.assertNotIn("If you received one email, check it.", self.home)

    def test_footer_rights_and_wrongs(self) -> None:
        line = "All rights reserved."
        for path in root_html_pages():
            with self.subTest(page=path.name):
                self.assertIn(line, path.read_text(encoding="utf-8"))

    def test_people_panorama_only_once_and_new_art(self) -> None:
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("cad-envelope", home)
        self.assertNotIn("people-dark.png", home)
        self.assertNotIn("people-light.png", home)
        for path in root_html_pages():
            html = path.read_text(encoding="utf-8")
            with self.subTest(page=path.name):
                self.assertNotIn("people-once.jpg", html)
                self.assertNotIn("people-light.png", html)
                self.assertNotIn("people-dark.png", html)

    def test_header_is_full_width_and_docs_rows_have_room(self) -> None:
        self.assertIn("top: 0; left: 0; right: 0;", self.css)
        self.assertIn("minmax(14rem, 22rem)", self.css)
        self.assertIn("#unlock-form input", self.css)
        self.assertIn(".header-register,", self.css)
        self.assertIn(".docs-content .scope-row", self.css)
