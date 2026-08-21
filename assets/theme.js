(() => {
  const KEY = "s7-theme";
  const apply = (theme) => {
    const next = theme === "dark" ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", next);
    document.documentElement.style.colorScheme = next;
    try {
      localStorage.setItem(KEY, next);
    } catch (err) {
      /* private mode */
    }
    const dark = next === "dark";
    document.querySelectorAll("[data-theme-toggle]").forEach((btn) => {
      btn.setAttribute("aria-pressed", dark ? "true" : "false");
      btn.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode");
      btn.textContent = dark ? "Light" : "Dark";
    });
    document.querySelectorAll('meta[name="theme-color"]').forEach((meta) => {
      meta.setAttribute("content", dark ? "#071018" : "#f7fbfe");
    });
  };
  let saved = "light";
  try {
    saved = localStorage.getItem(KEY) || "light";
  } catch (err) {
    saved = "light";
  }
  apply(saved);
  const bind = () => {
    apply(document.documentElement.getAttribute("data-theme") || "light");
    document.querySelectorAll("[data-theme-toggle]").forEach((btn) => {
      if (btn.dataset.bound === "1") return;
      btn.dataset.bound = "1";
      btn.addEventListener("click", () => {
        const now = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
        apply(now);
      });
    });
  };
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bind);
  } else {
    bind();
  }
})();
