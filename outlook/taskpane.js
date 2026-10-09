/* global Office */
var ACK = "terms-disclaimer-2026-08-15";
var DEFAULT_BASE = "https://verify.signet7.io";
var CONSEQUENTIAL = /\b(wire(?:\s+transfer)?|wiring|routing\s+number|iban|swift|account\s+number|bank\s+account|change.{0,40}account|new\s+account|update.{0,40}payment|payment\s+instruction|beneficiary|w-?9|gift\s+cards?|invoice.{0,80}pay)\b/i;

function bytesToBase64(bytes) {
  var binary = "";
  var chunk = 0x8000;
  for (var i = 0; i < bytes.length; i += chunk) {
    binary += String.fromCharCode.apply(null, bytes.subarray(i, i + chunk));
  }
  return btoa(binary);
}

function apiBase() {
  return DEFAULT_BASE;
}

function looksSealed(result) {
  if (!result) return false;
  if (result.integrity_ok === true) return true;
  var signature = String(result.signature || "").toUpperCase();
  if (signature === "VALID" || signature === "OK" || signature === "PASS") return true;
  return result.sealed === true;
}

function classifyAlert(result, subject, body) {
  if (!result) return null;
  var signature = String(result.signature || "").toUpperCase();
  var replay = String(result.replay || "").toUpperCase();
  var status = String(result.current_status || result.vsn_status || "").toLowerCase();
  if (result.integrity_ok === false || signature === "INVALID" || signature === "FAIL" || signature === "FAILED") {
    return {
      level: "alert",
      title: "Signet7: protected parts do not match",
      body: "This message has a Signet7 seal, but the protected parts no longer match or the signature is not valid. Do not change payment details from this email."
    };
  }
  if (replay === "SUSPECTED_REPLAY") {
    return {
      level: "alert",
      title: "Signet7: suspected replay",
      body: "This sealed message looks like a reuse. Do not treat it as a fresh instruction."
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
      body: "The sender/key binding is recorded as " + status + ". Do not act on this message."
    };
  }
  if (CONSEQUENTIAL.test(String(subject || "") + "\n" + String(body || "")) && !looksSealed(result)) {
    return {
      level: "warn",
      title: "Signet7: payment or account change, no seal",
      body: "This looks like a payment or account-change instruction and it is not sealed."
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

function markFile(label) {
  if (label === "Changed since sealed") return "sealed-changed.jpg";
  if (label === "Unchanged since sealed") return "sealed-unchanged.jpg";
  if (label === "Not sealed" || label === "Ordinary mail") return "not-sealed.jpg";
  if (label === "Address listed") return "address-listed.jpg";
  if (label === "Address mismatch") return "address-mismatch.jpg";
  if (label === "Address not listed") return "address-not-listed.jpg";
  return "";
}

function setOut(text) {
  var out = document.getElementById("out");
  if (out) out.textContent = text;
  var lines = String(text || "").split("\n");
  var words = document.getElementById("mark-words");
  var list = document.getElementById("mark-list");
  var wordFile = markFile((lines[0] || "").trim());
  var listFile = markFile((lines[1] || "").trim());
  if (words) {
    words.hidden = !wordFile;
    if (wordFile) words.src = wordFile;
  }
  if (list) {
    list.hidden = !listFile;
    if (listFile) list.src = listFile;
  }
}

function ackHeader() {
  return { "Content-Type": "application/json", "X-Signet7-Ack": ACK };
}

function fromAddress() {
  var item = Office.context.mailbox.item;
  if (item && item.from && item.from.emailAddress) return item.from.emailAddress;
  return "";
}

function lookupListing(fromAddr, key) {
  if (!fromAddr || fromAddr.indexOf("@") < 0) return Promise.resolve(null);
  var url = apiBase() + "/api/v1/vsn/listing?sender=" + encodeURIComponent(fromAddr);
  if (key) url += "&public_key_b64=" + encodeURIComponent(key);
  return fetch(url)
    .then(function (response) { return response.json(); })
    .catch(function () { return null; });
}

function wordsLine(result) {
  if (!result) return "Not sealed";
  if (result.sealed === false) return "Not sealed";
  var signature = String(result.signature || "").toUpperCase();
  var ok = result.integrity_ok === true;
  if (!ok && (signature === "UNKNOWN" || signature === "") && !result.profile) {
    return "Not sealed";
  }
  var currentStatus = String(result.current_status || "").toUpperCase();
  var statusAtSigning = String(result.status_at_signing || "").toUpperCase();
  var adverse = ["COMPROMISED", "REVOKED", "SUSPENDED"];
  if (
    !ok ||
    signature === "INVALID" ||
    signature === "FAIL" ||
    signature === "FAILED" ||
    adverse.indexOf(currentStatus) >= 0 ||
    adverse.indexOf(statusAtSigning) >= 0
  ) {
    return "Changed since sealed";
  }
  return "Unchanged since sealed";
}

function listingLine(listing) {
  var label = listing && listing.label ? String(listing.label) : "";
  if (listing && listing.code === "listing_matches") return "Address listed";
  if (listing && listing.code === "listing_does_not_match") return "Address mismatch";
  if (/doesn[’']t match/i.test(label)) return "Address mismatch";
  if (/^listed$/i.test(label)) return "Address listed";
  if (/not listed|no listing/i.test(label)) return "Address not listed";
  if (label) return label;
  return "Address not listed";
}

function formatRecipientResult(result, listing) {
  var words = wordsLine(result);
  var listed = listingLine(listing);
  var note = "Ordinary mail.";
  if (words === "Unchanged since sealed") {
    note = "The email has not changed since it was sealed.";
  } else if (words === "Changed since sealed") {
    note = "The email changed after it was sealed. Do not pay from this email. Call a number you already have.";
  }
  return words + "\n" + listed + "\n" + note;
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
          var item = Office.context.mailbox.item;
          var subject = item && item.subject ? item.subject : "";
          var alert = classifyAlert(pack.body, subject, "");
          var from = fromAddress();
          var key = pack.body.public_key_b64 || pack.body.key_fingerprint || "";
          lookupListing(from, key).then(function (listing) {
            setOut(formatRecipientResult(pack.body, listing));
            if (alert) {
              showBanner(alert);
              if (!silent) showPopup(alert);
            }
            resolve();
          });
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

function inviteSender() {
  var from = fromAddress();
  if (!from) {
    setOut("Open a message first.");
    return;
  }
  window.open("https://account.signet7.io/account?invite=" + encodeURIComponent(from), "_blank");
}

Office.onReady(function () {
  var verifyBtn = document.getElementById("verifyBtn");
  if (verifyBtn) verifyBtn.onclick = function () { verifyCurrentMessage({ silent: false }); };
  var inviteBtn = document.getElementById("inviteBtn");
  if (inviteBtn) inviteBtn.onclick = inviteSender;
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
