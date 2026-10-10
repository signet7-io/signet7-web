from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

from tests.site_html import home_page_markup  # noqa: E402


class DownloadVaultWizardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.download = (ROOT / "download.html").read_text(encoding="utf-8")
        cls.home = home_page_markup()

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
        self.assertIn("install.ps1", html)
        self.assertIn("Recipients never run it", html)
        self.assertNotIn("pip install", html)
        self.assertNotIn("Qual", html)
        self.assertNotIn("VSN", html)
        self.assertNotIn("is safe to pay", html)
        self.assertIn("The last look before you act.", self.home)

    def test_watch_product_docs_name_optional_vault(self) -> None:
        pages = {
            "download.html": (ROOT / "download.html").read_text(encoding="utf-8"),
            "product.html": (ROOT / "product.html").read_text(encoding="utf-8"),
            "docs.html": (ROOT / "docs.html").read_text(encoding="utf-8"),
        }
        ids = {
            "download.html": "company-records-vault",
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
                if name == "docs.html":
                    self.assertIn("The public website check does not keep the email", html)
                else:
                    self.assertIn("The public website check does not keep the letter", html)
                self.assertIn("Recipients never use the vault", html)
                self.assertNotIn("pip install", html)
                self.assertNotIn("Qual", html)
                self.assertNotIn("VSN", html)
                self.assertNotIn("is safe to pay", html)
                self.assertNotIn("How it works", html)
        self.assertIn("The last look before you act.", self.home)

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
        self.assertIn("Early access — extra OS warnings until signing is done", html)
        self.assertNotIn("pip install", html)
        self.assertNotIn("Qual", html)
        self.assertNotIn("VSN", html)
        self.assertNotIn("is safe to pay", html)
        self.assertNotIn("How it works", html)
        self.assertIn("The last look before you act.", self.home)

    def test_docs_and_download_name_helper_instruction_card(self) -> None:
        docs = (ROOT / "docs.html").read_text(encoding="utf-8")
        download = self.download
        self.assertIn('id="docs-agent-card"', docs)
        self.assertIn('id="agent-card"', docs)
        self.assertIn("Do not train a model on company mail", docs)
        self.assertIn("not a plugin", docs)
        self.assertIn('id="company-agent-card"', download)
        self.assertIn("Do not train a model on company mail", download)
        self.assertIn("not a plugin", download)
        self.assertNotIn("AGENT-CHECK.md", download)
        self.assertNotIn("pip install", docs)
        self.assertNotIn("pip install", download)
        self.assertNotIn("Qual", docs)
        self.assertNotIn("Qual", download)
        self.assertNotIn("VSN", docs)
        self.assertNotIn("VSN", download)
        self.assertNotIn("is safe to pay", docs)
        self.assertNotIn("is safe to pay", download)
        self.assertNotIn("How it works", docs)
        self.assertIn("The last look before you act.", self.home)

    def test_latest_json_is_unsigned_preview_not_pip(self) -> None:
        meta = json.loads((ROOT / "files" / "latest.json").read_text(encoding="utf-8"))
        self.assertIs(meta["signed"], False)
        self.assertEqual(meta["channel"], "preview")
        self.assertEqual(meta["source"]["repo"], "signet7-io/signet7")
        self.assertIn("windows", meta["files"])
        self.assertIn("macos", meta["files"])
        self.assertNotIn("linux", meta["files"])
        self.assertNotIn("macos_dmg", meta["files"])
        self.assertEqual(
            meta["files"]["windows"]["href"],
            "files/Signet7-Windows.zip",
        )
        self.assertEqual(
            meta["files"]["macos"]["href"],
            "files/Signet7-Mac.zip",
        )
        for key in ("windows", "macos"):
            href = meta["files"][key]["href"]
            path = ROOT / href
            self.assertTrue(path.is_file(), path)
            self.assertEqual(path.stat().st_size, meta["files"][key]["bytes"])

    def test_windows_zip_includes_one_file_wizard(self) -> None:
        import zipfile

        path = ROOT / "files" / "Signet7-Windows.zip"
        with zipfile.ZipFile(path) as zf:
            names = zf.namelist()
        self.assertIn("README.txt", names)
        self.assertIn("install.ps1", names)
        self.assertIn("Signet7/Signet7.exe", names)
        self.assertIn("Signet7/signet7-setup.exe", names)
        self.assertNotIn("AGENT-CHECK.md", names)
        self.assertNotIn("NOT-A-PUBLIC-RELEASE.txt", names)
        self.assertNotIn("Qual", " ".join(names))


if __name__ == "__main__":
    unittest.main()
