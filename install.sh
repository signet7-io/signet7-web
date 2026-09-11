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
  echo "  watch     download Signet7 desktop zip for this OS (one company inbox)"
  echo "  desktop   same as watch: unsigned zip for this OS"
  echo "  outlook   save Outlook manifest (Add from File, not AppSource)"
  echo "  help      this list (default)"
  echo
  echo "Example:"
  echo "  curl -fsSL https://signet7.io/install.sh | SIGNET7_SETUP=watch bash"
}

install_watch() {
  mkdir -p "$ROOT"
  zip="$ROOT/signet7-watch.zip"
  echo "Downloading unsigned Signet7 desktop. Gatekeeper may warn. Recipients should not install."
  curl -fsSL "$(watch_url)" -o "$zip"
  mkdir -p "$ROOT/watch"
  unzip -o "$zip" -d "$ROOT/watch" >/dev/null
  echo "Unpacked to $ROOT/watch"
  echo "One company inbox only. Checkout is not live."
}

install_desktop() {
  echo "Company desktop is the unsigned zip, not pip. Recipients do not install."
  install_watch
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
