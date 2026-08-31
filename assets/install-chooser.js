"use strict";

const COMMANDS = {
  windows: {
    help: "irm https://signet7.io/install.ps1 | iex",
    watch: "$env:SIGNET7_SETUP='watch'; irm https://signet7.io/install.ps1 | iex",
    desktop: "$env:SIGNET7_SETUP='desktop'; irm https://signet7.io/install.ps1 | iex",
    outlook: "$env:SIGNET7_SETUP='outlook'; irm https://signet7.io/install.ps1 | iex",
  },
  macos: {
    help: "curl -fsSL https://signet7.io/install.sh | bash",
    watch: "curl -fsSL https://signet7.io/install.sh | SIGNET7_SETUP=watch bash",
    desktop: "curl -fsSL https://signet7.io/install.sh | SIGNET7_SETUP=desktop bash",
    outlook: "curl -fsSL https://signet7.io/install.sh | SIGNET7_SETUP=outlook bash",
  },
};

const NOTES = {
  help: "Prints the list. Does not install Watch until you choose Watch. Unsigned software. Not a store listing.",
  watch: "Downloads unsigned Watch for this OS into a Signet7 folder. Recipients should not run this. SmartScreen or Gatekeeper will warn.",
  desktop: "Company setup window on this computer. Recipients still use the live check. Not a store listing.",
  outlook: "Saves the Outlook manifest. Add from File. Not AppSource. Recipients who never sideload still use the live check.",
};

function selected(group, attr) {
  const pressed = document.querySelector(group + " button[aria-pressed='true']");
  return pressed ? pressed.getAttribute(attr) : null;
}

function setPressed(group, attr, value) {
  document.querySelectorAll(group + " button").forEach((btn) => {
    btn.setAttribute("aria-pressed", btn.getAttribute(attr) === value ? "true" : "false");
  });
}

function detectOs() {
  const ua = (navigator.userAgent || "").toLowerCase();
  if (/mac os x|macintosh|linux/.test(ua) && !/android/.test(ua)) return "macos";
  return "windows";
}

function render() {
  const os = selected(".install-os", "data-os-tab") || "windows";
  const kind = selected(".install-kind", "data-kind") || "help";
  const cmd = COMMANDS[os][kind];
  const el = document.getElementById("install-command");
  const note = document.getElementById("install-note");
  if (el) el.textContent = cmd;
  if (note) note.textContent = NOTES[kind];
}

const root = document.querySelector("[data-install-chooser]");
if (root) {
  setPressed(".install-os", "data-os-tab", detectOs());
  document.querySelectorAll(".install-os button").forEach((btn) => {
    btn.addEventListener("click", () => {
      setPressed(".install-os", "data-os-tab", btn.getAttribute("data-os-tab"));
      render();
    });
  });
  document.querySelectorAll(".install-kind button").forEach((btn) => {
    btn.addEventListener("click", () => {
      setPressed(".install-kind", "data-kind", btn.getAttribute("data-kind"));
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
