#!/usr/bin/env bash
# Signet7 company-computer setup. Recipients should not run this.
# Live check (no install): https://verify.signet7.io/email/verify
set -euo pipefail
SETUP="${SIGNET7_SETUP:-help}"
SETUP="$(printf '%s' "$SETUP" | tr '[:upper:]' '[:lower:]')"
VERIFY="https://verify.signet7.io/email/verify"
UNAME="$(uname -s 2>/dev/null || echo unknown)"
ROOT="${HOME}/.local/share/signet7"

watch_url() {
  case "$UNAME" in
    Darwin) echo "https://signet7.io/files/signet7-watch-macos.zip" ;;
    Linux) echo "https://signet7.io/files/signet7-watch-linux.zip" ;;
    *) echo "https://signet7.io/files/signet7-watch-linux.zip" ;;
  esac
}

show_help() {
  echo "Signet7 setup (${UNAME})"
  echo "Recipients install nothing. ${VERIFY}"
  echo
  echo "This script is for one company computer. Unsigned preview. Not a store listing."
  echo "Set SIGNET7_SETUP then re-run:"
  echo "  watch     download Watch zip for this OS (one company inbox)"
  echo "  desktop   pip install signet7 if Python is present"
  echo "  outlook   save Outlook manifest (Add from File, not AppSource)"
  echo "  help      this list (default)"
  echo
  echo "Example:"
  echo "  curl -fsSL https://signet7.io/install.sh | SIGNET7_SETUP=watch bash"
}

install_watch() {
  mkdir -p "$ROOT"
  zip="$ROOT/signet7-watch.zip"
  echo "Downloading unsigned Watch. Gatekeeper may warn. Recipients should not install."
  curl -fsSL "$(watch_url)" -o "$zip"
  mkdir -p "$ROOT/watch"
  unzip -o "$zip" -d "$ROOT/watch" >/dev/null
  echo "Unpacked to $ROOT/watch"
  echo "One company inbox only. Checkout is not live."
}

install_desktop() {
  if ! command -v pip >/dev/null 2>&1 && ! command -v pip3 >/dev/null 2>&1; then
    echo "Python/pip not found. Use Watch on https://signet7.io/download or install Python first."
    echo "Recipients still use ${VERIFY}"
    return 0
  fi
  echo "Installing company desktop (pip). Recipients do not need this."
  if command -v pip3 >/dev/null 2>&1; then pip3 install --upgrade signet7; else pip install --upgrade signet7; fi
  echo "Run: signet7"
  echo "Or: signet7-setup --list"
}

install_outlook() {
  dest="${HOME}/Downloads"
  mkdir -p "$dest"
  curl -fsSL "https://signet7.io/outlook/manifest.xml" -o "$dest/signet7-outlook-manifest.xml"
  echo "Saved $dest/signet7-outlook-manifest.xml"
  echo "In cloud Outlook: Add from File. Not AppSource. Not Add from URL."
  echo "Recipients who never sideload: ${VERIFY}"
}

case "$SETUP" in
  watch) install_watch ;;
  desktop) install_desktop ;;
  outlook) install_outlook ;;
  *) show_help ;;
esac
