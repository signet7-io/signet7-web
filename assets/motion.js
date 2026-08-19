(() => {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const toggle = document.querySelector(".nav-toggle");
  if (toggle) {
    toggle.addEventListener("click", () => {
      const open = document.body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  const mail = document.querySelector("[data-mail]");
  const hint = document.querySelector("[data-hint]");
  const hots = [...document.querySelectorAll("[data-hot]")];
  const inspect = document.querySelector("[data-inspect]");
  const tabs = [...document.querySelectorAll("[data-tab]")];
  const panels = [...document.querySelectorAll("[data-panel]")];

  const say = (text) => {
    if (hint) hint.textContent = text;
  };

  hots.forEach((el) => {
    const msg = el.getAttribute("data-hot") || "";
    const on = () => {
      hots.forEach((h) => h.classList.remove("is-on"));
      el.classList.add("is-on");
      say(msg);
    };
    el.addEventListener("mouseenter", on);
    el.addEventListener("focus", on);
    el.addEventListener("click", on);
  });

  const showPanel = (name) => {
    tabs.forEach((t) => t.setAttribute("aria-selected", t.getAttribute("data-tab") === name ? "true" : "false"));
    panels.forEach((p) => p.classList.toggle("is-on", p.getAttribute("data-panel") === name));
  };

  if (inspect) {
    inspect.addEventListener("click", () => {
      showPanel("inspect");
      say("Walkthrough only. This page is not the live check.");
    });
  }

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => showPanel(tab.getAttribute("data-tab")));
  });

  window.addEventListener("keydown", (e) => {
    if (e.key === "1") showPanel("received");
    if (e.key === "2") showPanel("inspect");
    if (e.key === "3") showPanel("limits");
  });

  if (mail && !reduce) {
    mail.addEventListener("mousemove", (e) => {
      const r = mail.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width - 0.5;
      const y = (e.clientY - r.top) / r.height - 0.5;
      mail.style.setProperty("--ry", `${x * 8}deg`);
      mail.style.setProperty("--rx", `${-y * 6}deg`);
    });
    mail.addEventListener("mouseleave", () => {
      mail.style.setProperty("--ry", "0deg");
      mail.style.setProperty("--rx", "0deg");
    });
  }
})();
