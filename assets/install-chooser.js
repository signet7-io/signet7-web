"use strict";

const COMMANDS = {
  windows: "$env:SIGNET7_SETUP='watch'; irm https://signet7.io/install.ps1 | iex",
  macos: "curl -fsSL https://signet7.io/install.sh | SIGNET7_SETUP=watch bash",
};

const NOTES = {
  windows: "Downloads unsigned Watch for Windows. Recipients should not run this. SmartScreen will warn.",
  macos: "Downloads unsigned Watch for this Mac or Linux PC. Recipients should not run this. Gatekeeper may warn.",
};

function selectedOs() {
  const pressed = document.querySelector(".install-os button[aria-pressed='true']");
  return (pressed && pressed.getAttribute("data-os-tab")) || "windows";
}

function setOs(os) {
  document.querySelectorAll(".install-os button").forEach((btn) => {
    btn.setAttribute("aria-pressed", btn.getAttribute("data-os-tab") === os ? "true" : "false");
  });
}

function detectOs() {
  const ua = (navigator.userAgent || "").toLowerCase();
  if (/mac os x|macintosh|linux/.test(ua) && !/android/.test(ua)) return "macos";
  return "windows";
}

function render() {
  const os = selectedOs();
  const el = document.getElementById("install-command");
  const note = document.getElementById("install-note");
  if (el) el.textContent = COMMANDS[os];
  if (note) note.textContent = NOTES[os];
}

const root = document.querySelector("[data-install-chooser]");
if (root) {
  setOs(detectOs());
  document.querySelectorAll(".install-os button").forEach((btn) => {
    btn.addEventListener("click", () => {
      setOs(btn.getAttribute("data-os-tab"));
      render();
    });
  });
  const copyBtn = document.querySelector("[data-install-copy]");
  if (copyBtn) {
    copyBtn.addEventListener("click", () => {
      const text = document.getElementById("install-command").textContent;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
          copyBtn.textContent = "Copied";
          setTimeout(() => {
            copyBtn.textContent = "Copy";
          }, 1200);
        }).catch(() => {});
      }
    });
  }
  render();
}
