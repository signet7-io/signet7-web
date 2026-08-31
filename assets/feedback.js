"use strict";

const DEST = {
  feedback: "customerservice@signet7.io",
  bug: "customerservice@signet7.io",
  feature: "customerservice@signet7.io",
};

const LABELS = {
  feedback: "Feedback",
  bug: "Bug",
  feature: "Feature request",
};

function selectedType() {
  const pressed = document.querySelector(".feedback-types button[aria-pressed='true']");
  return (pressed && pressed.getAttribute("data-type")) || "feedback";
}

function setType(type) {
  document.querySelectorAll(".feedback-types button").forEach((btn) => {
    btn.setAttribute("aria-pressed", btn.getAttribute("data-type") === type ? "true" : "false");
  });
}

function submitFeedback() {
  const type = selectedType();
  const to = DEST[type];
  const subjectRaw = (document.getElementById("feedback-subject").value || "").trim();
  const content = (document.getElementById("feedback-content").value || "").trim();
  const status = document.getElementById("feedback-status");
  if (!content) {
    status.textContent = "Write a few words in Content first. Signet7 does not store this page.";
    return;
  }
  const subject = "[Signet7 " + LABELS[type] + "] " + (subjectRaw || LABELS[type]);
  const body =
    "Type: " + LABELS[type] + "\n\n" + content + "\n\n— sent from signet7.io/feedback\nDo not attach live invoices, passwords, or customer files.";
  const href =
    "mailto:" +
    to +
    "?subject=" +
    encodeURIComponent(subject) +
    "&body=" +
    encodeURIComponent(body);
  status.textContent = "Opening your mail app to " + to + ". Nothing is uploaded to this website.";
  window.location.href = href;
}

document.querySelectorAll(".feedback-types button").forEach((btn) => {
  btn.addEventListener("click", () => setType(btn.getAttribute("data-type")));
});
document.getElementById("feedback-submit").addEventListener("click", submitFeedback);
