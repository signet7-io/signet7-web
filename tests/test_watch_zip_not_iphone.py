from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class WatchZipNotIphoneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.watch = (ROOT / "watch.html").read_text(encoding="utf-8")
        cls.download = (ROOT / "download.html").read_text(encoding="utf-8")
        cls.home = (ROOT / "index.html").read_text(encoding="utf-8")

    def test_watch_page_says_unsigned_zip_not_iphone(self) -> None:
        watch = self.watch
        self.assertIn('id="watch-not-iphone"', watch)
        self.assertIn("Not Watch on iPhone.", watch)
        self.assertIn("Windows or Mac", watch)
        self.assertIn("unsigned zip", watch)
        self.assertIn("On a phone, use the live check.", watch)
        self.assertIn("https://verify.signet7.io/email/verify", watch)

    def test_download_page_says_unsigned_zip_not_iphone(self) -> None:
        download = self.download
        self.assertIn('id="watch-not-iphone"', download)
        self.assertIn("Not Watch on iPhone.", download)
        self.assertIn("Windows or Mac", download)
        self.assertIn("On a phone, use the live check.", download)
        self.assertIn("https://verify.signet7.io/email/verify", download)

    def test_watch_and_download_stay_claim_safe(self) -> None:
        for name, html in (("watch", self.watch), ("download", self.download)):
            with self.subTest(page=name):
                self.assertNotIn("VSN", html)
                self.assertNotIn("Qual", html)
                self.assertNotIn("is safe to pay", html)
                self.assertNotIn("you’re safe", html)
                self.assertNotIn("you're safe", html)
                self.assertNotIn("App Store", html)
                self.assertNotIn("Play Store", html)
        self.assertIn("High-stakes email, finally", self.home)
        hero = self.home.split("<h1", 1)[1].split("</h1>", 1)[0]
        self.assertIn("provable", hero)
        self.assertNotIn("Watch on iPhone", hero)


if __name__ == "__main__":
    unittest.main()
