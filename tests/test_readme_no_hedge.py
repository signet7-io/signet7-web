"""GitHub README does not whisper hedge quips."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeNoHedgeTests(unittest.TestCase):
    def test_github_readme_does_not_whisper_verified_is_not_safe(self) -> None:
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        lower = text.lower()
        self.assertNotIn("verified does not mean safe to act", lower)
        self.assertNotIn("verified does not mean the message is safe", lower)
        self.assertNotIn("verified is not safe", lower)
        self.assertNotIn("unknown is not fraud", lower)
        self.assertNotIn("you still decide", lower)
        self.assertNotIn("listed is not trusted", lower)
        self.assertIn("trust layer for consequential email", text)
        self.assertIn("This message is not Signet7-sealed.", text)
        self.assertIn("public website export", text)


if __name__ == "__main__":
    unittest.main()
