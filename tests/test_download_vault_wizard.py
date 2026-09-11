from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DownloadVaultWizardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.download = (ROOT / "download.html").read_text(encoding="utf-8")
        cls.home = (ROOT / "index.html").read_text(encoding="utf-8")

    def test_download_names_optional_vault_and_one_file_wizard(self) -> None:
        html = self.download
        self.assertIn('id="company-records-vault"', html)
        self.assertIn("Optional encrypted records vault", html)
        self.assertIn("The public website check does not keep the letter", html)
        self.assertIn("Cap is 10 GB", html)
        self.assertIn("50%", html)
        self.assertIn("90%", html)
        self.assertIn("Recipients never use the vault", html)
        self.assertIn('id="company-setup-wizard"', html)
        self.assertIn("One-file wizard", html)
        self.assertIn("Recipients never run it", html)
        self.assertNotIn("pip install", html)
        self.assertNotIn("Qual", html)
        self.assertNotIn("VSN", html)
        self.assertNotIn("is safe to pay", html)
        hero = self.home.split("<h1", 1)[1].split("</h1>", 1)[0]
        self.assertIn("High-stakes email, finally", hero)
        self.assertIn("provable", hero)

    def test_watch_product_docs_name_optional_vault(self) -> None:
        pages = {
            "watch.html": (ROOT / "watch.html").read_text(encoding="utf-8"),
            "product.html": (ROOT / "product.html").read_text(encoding="utf-8"),
            "docs.html": (ROOT / "docs.html").read_text(encoding="utf-8"),
        }
        ids = {
            "watch.html": "watch-records-vault",
            "product.html": "product-records-vault",
            "docs.html": "docs-records-vault",
        }
        for name, html in pages.items():
            with self.subTest(page=name):
                self.assertIn(f'id="{ids[name]}"', html)
                self.assertIn("recovery key", html.lower())
                self.assertIn("Cap is 10 GB", html)
                self.assertIn("50%", html)
                self.assertIn("90%", html)
                self.assertIn("The public website check does not keep the letter", html)
                self.assertIn("Recipients never use the vault", html)
                self.assertNotIn("pip install", html)
                self.assertNotIn("Qual", html)
                self.assertNotIn("VSN", html)
                self.assertNotIn("is safe to pay", html)
                self.assertNotIn("How it works", html)
        hero = self.home.split("<h1", 1)[1].split("</h1>", 1)[0]
        self.assertIn("High-stakes email, finally", hero)

    def test_faq_names_optional_vault_cap(self) -> None:
        html = (ROOT / "faq.html").read_text(encoding="utf-8")
        self.assertIn('id="faq-records-vault"', html)
        self.assertIn("Cap is 10 GB", html)
        self.assertIn("50%", html)
        self.assertIn("90%", html)
        self.assertIn("The public website check does not keep the letter", html)
        self.assertIn("Recipients never use the vault", html)
        self.assertIn("Not a court stamp", html)
        self.assertNotIn("pip install", html)
        self.assertNotIn("Qual", html)
        self.assertNotIn("VSN", html)
        self.assertNotIn("is safe to pay", html)
        self.assertNotIn("How it works", html)

    def test_faq_names_one_file_wizard(self) -> None:
        html = (ROOT / "faq.html").read_text(encoding="utf-8")
        self.assertIn('id="faq-setup-wizard"', html)
        self.assertIn('id="faq-one-file-wizard"', html)
        self.assertIn("One-file wizard", html)
        self.assertIn("company zip", html)
        self.assertIn("Recipients never run it", html)
        self.assertIn("not pip", html)
        self.assertIn("The app has Check for update", html)
        self.assertIn("Unsigned Preview", html)
        self.assertNotIn("pip install", html)
        self.assertNotIn("Qual", html)
        self.assertNotIn("VSN", html)
        self.assertNotIn("is safe to pay", html)
        self.assertNotIn("How it works", html)
        hero = self.home.split("<h1", 1)[1].split("</h1>", 1)[0]
        self.assertIn("High-stakes email, finally", hero)
        self.assertIn("provable", hero)

    def test_docs_and_download_name_helper_instruction_card(self) -> None:
        docs = (ROOT / "docs.html").read_text(encoding="utf-8")
        download = self.download
        self.assertIn('id="docs-agent-card"', docs)
        self.assertIn('id="agent-card"', docs)
        self.assertIn("Do not train a model on company mail", docs)
        self.assertIn("not a plugin", docs)
        self.assertIn('id="company-agent-card"', download)
        self.assertIn("Do not train a model on company mail", download)
        self.assertIn("AGENT-CHECK.md", download)
        self.assertNotIn("pip install", docs)
        self.assertNotIn("pip install", download)
        self.assertNotIn("Qual", docs)
        self.assertNotIn("Qual", download)
        self.assertNotIn("VSN", docs)
        self.assertNotIn("VSN", download)
        self.assertNotIn("is safe to pay", docs)
        self.assertNotIn("is safe to pay", download)
        self.assertNotIn("How it works", docs)
        hero = self.home.split("<h1", 1)[1].split("</h1>", 1)[0]
        self.assertIn("High-stakes email, finally", hero)

    def test_latest_json_is_unsigned_preview_not_pip(self) -> None:
        meta = json.loads((ROOT / "files" / "latest.json").read_text(encoding="utf-8"))
        self.assertIs(meta["signed"], False)
        self.assertEqual(meta["channel"], "preview")
        self.assertEqual(meta["source"]["repo"], "signet7-io/signet7")
        self.assertIn("windows", meta["files"])
        self.assertIn("macos", meta["files"])
        self.assertIn("linux", meta["files"])
        self.assertEqual(
            meta["source"]["sha"],
            "7a3554fd3c91893bf137e1a8b7b9ce216dbddce9",
        )
        self.assertEqual(meta["source"]["run"], 34635483135)
        for key in ("windows", "macos", "linux"):
            href = meta["files"][key]["href"]
            self.assertEqual(href, f"files/signet7-watch-{key}.zip")
            path = ROOT / href
            self.assertTrue(path.is_file(), path)
            self.assertEqual(path.stat().st_size, meta["files"][key]["bytes"])

    def test_windows_zip_includes_one_file_wizard(self) -> None:
        import zipfile

        path = ROOT / "files" / "signet7-watch-windows.zip"
        with zipfile.ZipFile(path) as zf:
            names = zf.namelist()
        self.assertIn("payload/signet7-setup.exe", names)
        self.assertIn("AGENT-CHECK.md", names)
        self.assertNotIn("Qual", " ".join(names))


if __name__ == "__main__":
    unittest.main()
