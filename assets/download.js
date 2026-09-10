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

  var API = "https://verify.signet7.io";
  var form = document.getElementById("unlock-form");
  var statusEl = document.getElementById("unlock-status");
  var filesEl = document.getElementById("watch-files");

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
          setStatus("If that mailbox can register, the code is on its way. Recipients never install Watch.");
        })
        .catch(function () {
          setStatus("Could not reach Signet7. Try again, or use the live check.");
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
          if (!result.ok || !result.body.files) {
            setStatus(result.body.error || "That code did not work.");
            return;
          }
          document.querySelectorAll("[data-watch-file]").forEach(function (link) {
            var key = link.getAttribute("data-watch-file");
            if (result.body.files[key]) link.href = result.body.files[key];
          });
          if (filesEl) filesEl.hidden = false;
          var chooser = document.getElementById("install-chooser");
          if (chooser) chooser.hidden = false;
          setStatus("Unlocked. Pick one computer. Recipients still use the live check.");
        })
        .catch(function () {
          setStatus("Could not reach Signet7.");
        });
    });
  }
})();
