/* global Office */
var ACK = "terms-disclaimer-2026-08-15";
var DEFAULT_BASE = "https://seal.signet7.io";

function apiBase() {
  var el = document.getElementById("baseUrl");
  var base = (el && el.value ? el.value : DEFAULT_BASE).replace(/\/$/, "");
  return base || DEFAULT_BASE;
}

function setOut(text) {
  var out = document.getElementById("out");
  if (out) out.textContent = text;
}

var ASKED_KEY = "signet7-invite-asked-v1";
var TOKEN_KEY = "signet7-sender-token-v1";

function roaming() {
  try {
    return Office.context && Office.context.roamingSettings;
  } catch (err) {
    return null;
  }
}

function readSavedToken() {
  var settings = roaming();
  if (settings && settings.get) {
    var fromRoam = settings.get(TOKEN_KEY);
    if (fromRoam) return String(fromRoam);
  }
  try {
    return localStorage.getItem(TOKEN_KEY) || "";
  } catch (err) {
    return "";
  }
}

function writeSavedToken(token) {
  var value = String(token || "").trim();
  var settings = roaming();
  if (settings && settings.set) {
    if (value) settings.set(TOKEN_KEY, value);
    else if (settings.remove) settings.remove(TOKEN_KEY);
    if (settings.saveAsync) settings.saveAsync(function () {});
  }
  try {
    if (value) localStorage.setItem(TOKEN_KEY, value);
    else localStorage.removeItem(TOKEN_KEY);
  } catch (err) {}
}

function fillTokenField() {
  var tokenEl = document.getElementById("token");
  if (!tokenEl || tokenEl.value) return;
  var saved = readSavedToken();
  if (saved) tokenEl.value = saved;
}

function currentToken() {
  var tokenEl = document.getElementById("token");
  var typed = tokenEl && tokenEl.value ? tokenEl.value.trim() : "";
  return typed || readSavedToken();
}

function askedMap() {
  try {
    return JSON.parse(localStorage.getItem(ASKED_KEY) || "{}") || {};
  } catch (err) {
    return {};
  }
}

function markAsked(addr) {
  var map = askedMap();
  map[String(addr).toLowerCase()] = true;
  localStorage.setItem(ASKED_KEY, JSON.stringify(map));
}

function wasAsked(addr) {
  return Boolean(askedMap()[String(addr).toLowerCase()]);
}

function firstRecipient(toField) {
  return String(toField || "").split(",")[0].trim().toLowerCase();
}

function openInvite(addr) {
  if (!addr) return;
  window.open("https://account.signet7.io/account?invite=" + encodeURIComponent(addr), "_blank");
}

function showInvitePrompt(addr) {
  var box = document.getElementById("invitePrompt");
  if (!box || !addr) return;
  if (wasAsked(addr)) {
    box.hidden = true;
    setOut("Invited / already asked for " + addr + ". Invite is still available.");
    return;
  }
  box.hidden = false;
  box.setAttribute("data-recipient", addr);
}

function hideInvitePrompt() {
  var box = document.getElementById("invitePrompt");
  if (box) box.hidden = true;
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
  var token = currentToken();
  if (!token) {
    setOut("A sender API token is required to seal. Incoming checks stay free.");
    return;
  }
  writeSavedToken(token);
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
        setOut("Need From, To, Subject, and a body in the draft.");
        return null;
      }
      window.__signet7LastTo = firstRecipient(payload.to_address);
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
        if (pack.body.entitlement_state === "intro_expired") {
          setOut("This sender intro has ended. Checking stays free. Sealing needs a paid program when checkout is live.");
          return;
        }
        if (pack.body.required_capability === "integration.outlook") {
          setOut("Outlook sealing needs an active intro or a Business program. Use the sender token from account.signet7.io/account.");
          return;
        }
        setOut(pack.body.error || "Seal failed. Sender programs are not free.");
        return;
      }
      var toAddr = window.__signet7LastTo || firstRecipient(pack.body.to_address || "");
      function afterAttach() {
        setOut("Sealed. A signed copy is attached. Send from Outlook as usual. The letter does not contain a check link.");
        if (toAddr) showInvitePrompt(toAddr);
      }
      if (item.addFileAttachmentFromBase64Async && pack.body.eml_base64) {
        item.addFileAttachmentFromBase64Async(pack.body.eml_base64, "Signet7-sealed.eml", function (result) {
          if (result && result.status && result.status !== Office.AsyncResultStatus.Succeeded) {
            var detail = result.error && result.error.message ? result.error.message : "attach failed";
            setOut("Sealed on the server, but Outlook did not attach Signet7-sealed.eml. " + detail);
            return;
          }
          afterAttach();
        });
        return;
      }
      setOut("Sealed on the server, but this Outlook build cannot attach the signed copy.");
      if (toAddr) showInvitePrompt(toAddr);
    })
    .catch(function (error) {
      var text = String(error);
      if (/networkerror|failed to fetch/i.test(text)) {
        setOut("Seal host blocked this browser call. Need From/To/Subject/body, then retry after the seal API allows https://signet7.io.");
        return;
      }
      setOut(text);
    });
}

Office.onReady(function () {
  fillTokenField();
  var tokenEl = document.getElementById("token");
  if (tokenEl) {
    tokenEl.addEventListener("change", function () {
      writeSavedToken(tokenEl.value);
    });
  }
  var button = document.getElementById("sealBtn");
  if (button) button.onclick = sealDraft;
  var inviteBtn = document.getElementById("inviteBtn");
  if (inviteBtn) {
    inviteBtn.onclick = function () {
      var item = Office.context.mailbox && Office.context.mailbox.item;
      field(item, "to").then(function (toField) {
        var addr = firstRecipient(toField);
        if (!addr) {
          setOut("Add a recipient first.");
          return;
        }
        markAsked(addr);
        hideInvitePrompt();
        openInvite(addr);
      });
    };
  }
  var yes = document.getElementById("inviteYes");
  if (yes) {
    yes.onclick = function () {
      var box = document.getElementById("invitePrompt");
      var addr = box && box.getAttribute("data-recipient");
      if (addr) {
        markAsked(addr);
        openInvite(addr);
      }
      hideInvitePrompt();
    };
  }
  var no = document.getElementById("inviteNo");
  if (no) {
    no.onclick = function () {
      var box = document.getElementById("invitePrompt");
      var addr = box && box.getAttribute("data-recipient");
      if (addr) markAsked(addr);
      hideInvitePrompt();
    };
  }
});
