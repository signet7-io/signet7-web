/* global Office */
var ACK = "terms-disclaimer-2026-08-15";
var DEFAULT_BASE = "https://qual.signet7.io";

function apiBase() {
  var el = document.getElementById("baseUrl");
  var base = (el && el.value ? el.value : DEFAULT_BASE).replace(/\/$/, "");
  return base || DEFAULT_BASE;
}

function setOut(text) {
  var out = document.getElementById("out");
  if (out) out.textContent = text;
}

function field(item, name) {
  return new Promise(function (resolve) {
    if (!item[name] || !item[name].getAsync) {
      resolve("");
      return;
    }
    item[name].getAsync(function (result) {
      if (result.status !== Office.AsyncResultStatus.Succeeded) {
        resolve("");
        return;
      }
      var value = result.value;
      if (Array.isArray(value)) {
        resolve(value.map(function (entry) { return entry.emailAddress || entry.displayName || ""; }).filter(Boolean).join(", "));
        return;
      }
      resolve(value || "");
    });
  });
}

function bodyText(item) {
  return new Promise(function (resolve, reject) {
    item.body.getAsync(Office.CoercionType.Text, function (result) {
      if (result.status !== Office.AsyncResultStatus.Succeeded) {
        reject(new Error(result.error.message));
        return;
      }
      resolve(result.value || "");
    });
  });
}

function fromAddress(item) {
  if (item.from && item.from.emailAddress) return Promise.resolve(item.from.emailAddress);
  if (Office.context.mailbox && Office.context.mailbox.userProfile) {
    return Promise.resolve(Office.context.mailbox.userProfile.emailAddress || "");
  }
  return Promise.resolve("");
}

function sealDraft() {
  var item = Office.context.mailbox.item;
  var tokenEl = document.getElementById("token");
  var token = tokenEl && tokenEl.value ? tokenEl.value.trim() : "";
  if (!token) {
    setOut("A sender API token is required to seal. Incoming checks stay free.");
    return;
  }
  setOut("Reading this draft…");
  Promise.all([fromAddress(item), field(item, "to"), field(item, "subject"), bodyText(item)])
    .then(function (parts) {
      var payload = {
        from_address: parts[0],
        to_address: parts[1],
        subject: parts[2],
        body: parts[3],
        selector: "outlook-addin",
        return_private_key: false,
        enroll: false
      };
      if (!payload.from_address || !payload.to_address || !payload.subject || !String(payload.body).trim()) {
        setOut("Need From, To, Subject, and a body in the draft. No .eml file.");
        return null;
      }
      return fetch(apiBase() + "/api/v1/email/sign", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + token,
          "X-Signet7-Ack": ACK
        },
        body: JSON.stringify(payload)
      }).then(function (response) {
        return response.json().then(function (body) { return { ok: response.ok, body: body }; });
      });
    })
    .then(function (pack) {
      if (!pack) return;
      if (!pack.ok) {
        setOut(pack.body.error || "Seal failed. Sender programs are not free.");
        return;
      }
      var notice = "This message was sealed with Signet7. The original signed copy is attached. Recipients can check it at https://qual.signet7.io/email/verify . Verified is not safe.\n\n";
      item.body.setAsync(notice, { coercionType: Office.CoercionType.Text }, function () {
        if (item.addFileAttachmentFromBase64Async && pack.body.eml_base64) {
          item.addFileAttachmentFromBase64Async(pack.body.eml_base64, "Signet7-sealed.eml", function () {
            setOut("Sealed. A signed copy is attached. Send from Outlook as usual.");
          });
          return;
        }
        setOut("Sealed on the server, but this Outlook build cannot attach the signed copy.");
      });
    })
    .catch(function (error) {
      setOut(String(error));
    });
}

Office.onReady(function () {
  var button = document.getElementById("sealBtn");
  if (button) button.onclick = sealDraft;
});
