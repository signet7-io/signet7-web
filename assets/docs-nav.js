(() => {
  const sidebar = document.getElementById("docs-sidebar");
  const toggle = document.querySelector(".docs-nav-toggle");
  const mask = document.querySelector(".docs-nav-mask");
  if (!sidebar) return;

  const links = [...sidebar.querySelectorAll('a[href^="#"], a[href*="#"]')].filter(
    (link) => {
      if (link.classList.contains("docs-nav-ext")) return false;
      return Boolean(link.hash && document.getElementById(link.hash.slice(1)));
    }
  );

  const setDrawer = (open) => {
    document.body.classList.toggle("docs-nav-open", open);
    if (toggle) toggle.setAttribute("aria-expanded", open ? "true" : "false");
  };

  const setActive = (id) => {
    links.forEach((link) => {
      const on = link.hash === `#${id}`;
      link.classList.toggle("is-active", on);
      if (on) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    });
  };

  if (toggle) {
    toggle.addEventListener("click", () => {
      setDrawer(!document.body.classList.contains("docs-nav-open"));
    });
  }
  if (mask) mask.addEventListener("click", () => setDrawer(false));
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") setDrawer(false);
  });

  links.forEach((link) => {
    link.addEventListener("click", () => {
      const id = link.hash.slice(1);
      if (!id) return;
      setDrawer(false);
      const cat = link.closest("details.docs-nav-cat");
      if (cat) cat.open = true;
      setActive(id);
    });
  });

  const hash = (window.location.hash || "").slice(1);
  if (hash && document.getElementById(hash)) {
    const current = links.find((link) => link.hash === `#${hash}`);
    if (current) {
      const cat = current.closest("details.docs-nav-cat");
      if (cat) cat.open = true;
    }
    setActive(hash);
  }
})();
