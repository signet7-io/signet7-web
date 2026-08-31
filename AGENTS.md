# Agent instructions

This is the public `signet7.io` website export (`signet7-io/signet7-web`).
It is static HTML, CSS, JS, and tests. There is no Node app, no package
manager, and no runtime backend.

Canonical copy lives in `signet7-io/signet7-active`. Edits here update the
public export only. A commit or push is not deployment.

## Boundaries

- Keep this export public-safe. Do not add credentials, private paths,
  owner-only strategy, or unpublished pricing/availability claims.
- Do not add analytics, lead forms, or external runtime dependencies.
- Do not dispatch GitHub Pages. Deploy is a separate, manual workflow.
- Relative links must stay inside this export.

## Verify locally

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 -m http.server 8765 --bind 127.0.0.1
```

The site is then at `http://127.0.0.1:8765`. Visual QA helper:
`tests/render_site_qa.py` (needs Playwright, Pillow, and Chrome). CI only
runs the unittest suite.

## Cursor Cloud specific instructions

Cloud agents clone this repository and start a static server on port 8765.
Use that origin to inspect pages. After HTML/CSS/JS changes, re-run:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

Do not treat a passing cloud run as a public launch. Pages deploy only
through the manual `pages.yml` workflow.
