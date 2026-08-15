# Signet7 public website export

This repository is the sanitized static export of the canonical website source in
`signet7-io/Signet7-Active/10-product/www/`.

## Product position

Signet7 is the trust layer for consequential email. It is designed to help a
recipient inspect supported sender/key evidence and declared protected-component
integrity before acting, then preserve the verifier response for later review.

> **Verified does not mean the message is safe, truthful, lawful, malware-free,
> confidential, or prudent to act on.**

> **This message is not Signet7-sealed. That is normal for ordinary email and is
> not evidence of tampering or fraud.**

> **Verified does not mean safe to act. Unknown, unsealed, unsupported, or
> unverified does not mean fraudulent.**

## Export boundary

- Canonical edits happen in the governance repository, not here.
- This export may contain only public-safe HTML, CSS, approved images, tests, and
  deployment metadata.
- Internal governance, owner-only strategy, legal working files, private paths,
  credentials, local integration packages, and release evidence do not belong here.
- Relative links must remain inside the exported site.
- Managed VSN, marketplace distribution, live billing, pricing, customer use,
  certification, SLA, and production availability must remain explicitly unproven
  unless later exact evidence and approval support them.
- A commit or push updates source only. It is not deployment or public-launch
  authorization.

## Static-site behavior

The source contains no lead form, analytics script, or external runtime dependency.
The pilot route uses a `mailto:` link and warns users not to send message content or
sensitive data. A deployed host may create separate logs, cookies, or headers and must
be evaluated independently.

## Local verification

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

The canonical synchronization gate also requires source/export byte comparison,
responsive screenshots, zero horizontal overflow, accessibility checks, link and
fragment validation, restricted-path scanning, and exact approved-asset hashes.

Passing local checks does not mean this export has been committed, pushed, merged, or
deployed.
