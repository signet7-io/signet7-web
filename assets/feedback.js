"use strict";

const API = "https://verify.signet7.io/api/v1/feedback";

const LABELS = {
  feedback: "Feedback",
  bug: "Bug",
  feature: "Feature request",
  sales: "Sales",
  marketing: "Marketing",
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
  const subject = (document.getElementById("feedback-subject").value || "").trim();
  const content = (document.getElementById("feedback-content").value || "").trim();
  const replyTo = (document.getElementById("feedback-reply") && document.getElementById("feedback-reply").value || "").trim();
  const status = document.getElementById("feedback-status");
  const button = document.getElementById("feedback-submit");
  if (!content) {
    status.textContent = "Write a few words in Content first.";
    return;
  }
  button.disabled = true;
  status.textContent = "Sending…";
  fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      type: type,
      subject: subject,
      content: content,
      reply_to: replyTo,
    }),
  })
    .then(function (res) {
      return res.json().then(function (body) {
        return { ok: res.ok, status: res.status, body: body };
      });
    })
    .then(function (result) {
      if (result.ok && result.body && result.body.accepted) {
        status.textContent = result.body.mailed
          ? "Sent. Thank you."
          : "Received. Thank you.";
        document.getElementById("feedback-content").value = "";
        document.getElementById("feedback-subject").value = "";
        if (document.getElementById("feedback-reply")) {
          document.getElementById("feedback-reply").value = "";
        }
        return;
      }
      const err = (result.body && result.body.error) || "Could not send.";
      status.textContent = err;
    })
    .catch(function () {
      status.textContent = "Could not send. Try again in a moment.";
    })
    .then(function () {
      button.disabled = false;
    });
}

document.querySelectorAll(".feedback-types button").forEach((btn) => {
  btn.addEventListener("click", () => setType(btn.getAttribute("data-type")));
});
document.getElementById("feedback-submit").addEventListener("click", submitFeedback);
