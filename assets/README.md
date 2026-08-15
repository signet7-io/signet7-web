# Website Assets

## Reasoning

Generic logo and icon paths previously contained retired AI-inbox artwork. They now resolve to the owner-approved v2 circular seal so navigation, touch, favicon, and social surfaces share one identity.

## Final implementation

- `signet7-circle-logo-official-v2.png` — canonical visible website mark.
- `signet7-logo.png` — compatibility alias (byte-identical).
- `apple-touch-icon.png` — 180×180 touch icon downscaled (LANCZOS) from the seal (not byte-identical).
- `favicon.png` — 32×32 browser icon downscaled (LANCZOS) from the seal (not byte-identical).
- `og-image.png` — distinct 1200×630 social-preview card derived from the seal (not byte-identical).
- `site.css` — local website stylesheet.

The artwork reads **VERIFY THE SENDER • SEAL THE DECISION** and has SHA-256 `63ffd6be248b79a86b83f5da5aaa971490ebd7a5b1fa521bcb9785f699b7695e`. Keep the site self-contained and mirror this directory to `signet7-io/signet7-web`.
