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

  fetch("files/latest.json", { credentials: "same-origin" })
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (info) {
      if (!info || !info.version) return;
      var el = document.getElementById("build-version");
      if (el) el.textContent = info.version;
    })
    .catch(function () {});
})();
