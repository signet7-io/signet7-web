(function () {
  var ua = (navigator.userAgent || "").toLowerCase();
  var platform = "windows";
  if (/mac os x|macintosh/.test(ua) && !/iphone|ipad/.test(ua)) platform = "macos";
  else if (/linux/.test(ua) && !/android/.test(ua)) platform = "linux";

  document.querySelectorAll("[data-os]").forEach(function (card) {
    if (card.getAttribute("data-os") === platform) {
      card.classList.add("is-you");
      var hint = card.querySelector("[data-you]");
      if (hint) hint.hidden = false;
    }
  });

  function applyFiles(meta) {
    if (!meta) return;
    var el = document.getElementById("build-version");
    if (el && meta.version) el.textContent = meta.version;
    var files = (meta.files) || {};
    document.querySelectorAll("[data-watch-file]").forEach(function (link) {
      var key = link.getAttribute("data-watch-file");
      var row = files[key];
      if (row && row.href) link.href = row.href;
    });
    var filesEl = document.getElementById("watch-files");
    if (filesEl) filesEl.hidden = false;
    var chooser = document.getElementById("install-chooser");
    if (chooser) chooser.hidden = false;
  }

  fetch("files/latest.json")
    .then(function (r) { return r.json(); })
    .then(applyFiles)
    .catch(function () {});

  var API = "https://verify.signet7.io";
  var form = document.getElementById("unlock-form");
  var statusEl = document.getElementById("unlock-status");

  function setStatus(text) {
    if (statusEl) statusEl.textContent = text || "";
  }

  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var mailbox = (document.getElementById("unlock-mailbox") || {}).value || "";
      setStatus("Sending a code to that work email.");
      fetch(API + "/api/v1/download/unlock", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mailbox: mailbox })
      })
        .then(function (r) { return r.json(); })
        .then(function () {
          setStatus("If that mailbox can register, the code is on its way. Recipients never install Signet7 desktop. The zip buttons above do not wait for this.");
        })
        .catch(function () {
          setStatus("Could not reach Signet7. The zip buttons above still work.");
        });
    });
  }

  var redeem = document.getElementById("unlock-redeem");
  if (redeem) {
    redeem.addEventListener("click", function () {
      var mailbox = (document.getElementById("unlock-mailbox") || {}).value || "";
      var code = (document.getElementById("unlock-code") || {}).value || "";
      fetch(API + "/api/v1/download/unlock/redeem", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mailbox: mailbox, code: code })
      })
        .then(function (r) { return r.json().then(function (body) { return { ok: r.ok, body: body }; }); })
        .then(function (result) {
          if (!result.ok) {
            setStatus((result.body && result.body.error) || "That code did not work. The zip buttons above still work.");
            return;
          }
          applyFiles({ files: result.body.files, version: result.body.version });
          setStatus("Setup note accepted. Recipients still use the live check.");
        })
        .catch(function () {
          setStatus("Could not reach Signet7. The zip buttons above still work.");
        });
    });
  }
})();
