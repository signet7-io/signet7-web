/* global Office */
var ACK = "terms-disclaimer-2026-08-15";
var DEFAULT_BASE = "https://verify.signet7.io";

function bytesToBase64(bytes) {
  var binary = "";
  var chunk = 0x8000;
  for (var i = 0; i < bytes.length; i += chunk) {
    binary += String.fromCharCode.apply(null, bytes.subarray(i, i + chunk));
  }
  return btoa(binary);
}

function apiBase() {
  var el = document.getElementById("baseUrl");
  var base = (el && el.value ? el.value : DEFAULT_BASE).replace(/\/$/, "");
  return base || DEFAULT_BASE;
}

function classifyAlert(result) {
  if (!result) return null;
  var signature = String(result.signature || "").toUpperCase();
  var replay = String(result.replay || "").toUpperCase();
  var status = String(result.current_status || result.vsn_status || "").toLowerCase();
  if (result.integrity_ok === false || signature === "INVALID" || signature === "FAIL" || signature === "FAILED") {
    return {
      level: "alert",
      title: "Signet7: protected parts do not match",
      body: "This message has a Signet7 seal, but the protected parts no longer match or the signature is not valid. Do not change payment details from this email. Call the person you already know. Verified is not safe. Unknown is not fraud."
    };
  }
  if (replay === "SUSPECTED_REPLAY") {
    return {
      level: "alert",
      title: "Signet7: suspected replay",
      body: "This sealed message looks like a reuse. Do not treat it as a fresh instruction. Call the person you already know."
    };
  }
  if (status === "revoked" || status === "compromised" || status === "terminated") {
    return {
      level: "alert",
      title: "Signet7: sender binding is " + status,
      body: "The sender/key binding is recorded as " + status + ". Do not act on payment changes in this message."
    };
  }
  if (status === "suspended" || status === "expired") {
    return {
      level: "warn",
      title: "Signet7: sender binding is " + status,
      body: "The sender/key binding is recorded as " + status + ". Use a known callback before you act."
    };
  }
  return null;
}

function showBanner(alert) {
  var item = Office.context.mailbox.item;
  if (!item || !item.notificationMessages) return;
  var kind = Office.MailboxEnums.ItemNotificationMessageType;
  item.notificationMessages.replaceAsync("signet7Passive", {
    type: alert.level === "alert" ? kind.ErrorMessage : kind.InformationalMessage,
    message: alert.title,
    persistent: true
  });
}

function showPopup(alert) {
  var root = window.location.href.replace(/taskpane\.html.*/, "");
  var url = root + "alert.html?title=" + encodeURIComponent(alert.title) + "&body=" + encodeURIComponent(alert.body);
  Office.context.ui.displayDialogAsync(url, { height: 40, width: 36, displayInIframe: true });
}

function setOut(text) {
  var out = document.getElementById("out");
  if (out) out.textContent = text;
}

function ackHeader() {
  var headers = { "Content-Type": "application/json", "X-Signet7-Ack": ACK };
  return headers;
}

function verifyCurrentMessage(opts) {
  opts = opts || {};
  var silent = opts.silent === true;
  setOut(silent ? "Checking in the background…" : "Fetching message…");
  return new Promise(function (resolve) {
    if (!Office.context.mailbox || !Office.context.mailbox.item || !Office.context.mailbox.item.getAsFileAsync) {
      if (!silent) setOut("Open a received message.");
      resolve();
      return;
    }
    Office.context.mailbox.item.getAsFileAsync(function (result) {
      if (result.status !== Office.AsyncResultStatus.Succeeded) {
        if (!silent) setOut("Need the opened message: " + result.error.message);
        resolve();
        return;
      }
      var bytes = new Uint8Array(result.value);
      fetch(apiBase() + "/api/v1/email/verify", {
        method: "POST",
        headers: ackHeader(),
        body: JSON.stringify({ eml: bytesToBase64(bytes), eml_encoding: "base64", record_evidence: false })
      })
        .then(function (response) { return response.json().then(function (body) { return { ok: response.ok, body: body }; }); })
        .then(function (pack) {
          if (!pack.ok) {
            if (!silent) setOut(pack.body.error || "Check failed");
            resolve();
            return;
          }
          var alert = classifyAlert(pack.body);
          if (alert) {
            showBanner(alert);
            showPopup(alert);
            setOut(alert.title + "\n\n" + alert.body);
          } else {
            setOut("No Signet7 warning. Ordinary unsigned mail stays quiet. Verified is not safe. Unknown is not fraud.");
          }
          resolve();
        })
        .catch(function (error) {
          if (!silent) setOut(String(error));
          resolve();
        });
    });
  });
}

function bindPassive() {
  verifyCurrentMessage({ silent: true });
  if (Office.context.mailbox.addHandlerAsync && Office.EventType && Office.EventType.ItemChanged) {
    Office.context.mailbox.addHandlerAsync(Office.EventType.ItemChanged, function () {
      verifyCurrentMessage({ silent: true });
    });
  }
}

Office.onReady(function () {
  var verifyBtn = document.getElementById("verifyBtn");
  if (verifyBtn) verifyBtn.onclick = function () { verifyCurrentMessage({ silent: false }); };
  var base = document.getElementById("baseUrl");
  if (base && !base.value) base.value = DEFAULT_BASE;
  var fbBtn = document.getElementById("feedbackBtn");
  if (fbBtn) {
    fbBtn.onclick = function () {
      var text = (document.getElementById("feedbackText") || {}).value || "";
      var out = document.getElementById("feedbackOut");
      if (!String(text).trim()) {
        if (out) out.textContent = "Write a few words first.";
        return;
      }
      if (out) out.textContent = "Sending…";
      fetch(apiBase() + "/api/v1/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ type: "feedback", content: String(text).trim() })
      }).then(function (res) { return res.json().then(function (body) { return { ok: res.ok, body: body }; }); })
        .then(function (result) {
          if (result.ok && result.body && result.body.accepted) {
            if (out) out.textContent = result.body.mailed ? "Sent. Thank you." : "Received. Thank you.";
            var box = document.getElementById("feedbackText");
            if (box) box.value = "";
            return;
          }
          if (out) out.textContent = (result.body && result.body.error) || "Could not send.";
        })
        .catch(function () { if (out) out.textContent = "Could not send."; });
    };
  }
  bindPassive();
});
