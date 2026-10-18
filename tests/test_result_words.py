from __future__ import annotations

import unittest

from tests.result_words import (
    ADDRESS_RESULTS,
    CURRENT_LABELS,
    MARK_FILES,
    RESULT_SURFACES,
    RETIRED_LABELS,
    SEAL_RESULTS,
    ROOT,
    read,
)
from tests.site_html import home_served_copy, public_text_assets, root_html_pages


class ResultWordsTests(unittest.TestCase):
    def test_mark_files_exist_on_the_site_and_in_the_pane(self) -> None:
        for name in MARK_FILES:
            with self.subTest(name=name):
                self.assertTrue((ROOT / "assets" / "marks" / name).is_file(), name)
                self.assertTrue((ROOT / "outlook" / name).is_file(), name)

    def test_recipient_surfaces_use_every_current_label(self) -> None:
        for path in RESULT_SURFACES:
            text = read(path)
            for label in CURRENT_LABELS:
                with self.subTest(page=path.name, label=label):
                    self.assertIn(label, text)

    def test_homepage_bundle_names_the_seal_results(self) -> None:
        home = home_served_copy()
        for label in SEAL_RESULTS:
            with self.subTest(label=label):
                self.assertIn(label, home)

    def test_faq_explains_the_unchanged_result(self) -> None:
        faq = read(ROOT / "faq.html")
        self.assertIn('id="plain-words"', faq)
        self.assertIn("What does Unchanged since sealed mean?", faq)
        self.assertIn("does not approve payment", faq)
        for label in CURRENT_LABELS:
            with self.subTest(label=label):
                self.assertIn(label, faq)

    def test_outlook_pane_maps_each_label_to_its_mark(self) -> None:
        js = read(ROOT / "outlook" / "taskpane.js")
        self.assertIn('return "Unchanged since sealed"', js)
        self.assertIn('return "Changed since sealed"', js)
        self.assertIn('return "Not sealed"', js)
        for label, mark in zip(SEAL_RESULTS + ADDRESS_RESULTS, MARK_FILES, strict=True):
            with self.subTest(label=label):
                self.assertIn(f'return "{mark}"', js)
                self.assertIn(label, js)

    def test_retired_labels_do_not_return(self) -> None:
        blobs = [(path, path.read_text(encoding="utf-8", errors="replace")) for path in public_text_assets()]
        blobs.extend((path, path.read_text(encoding="utf-8")) for path in root_html_pages())
        seen: set[str] = set()
        for path, text in blobs:
            key = str(path.resolve())
            if key in seen:
                continue
            seen.add(key)
            for phrase in RETIRED_LABELS:
                with self.subTest(asset=path.name, phrase=phrase):
                    self.assertNotIn(phrase, text)
