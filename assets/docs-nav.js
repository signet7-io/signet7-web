(() => {
  const sidebar = document.getElementById("docs-sidebar");
  const toggle = document.querySelector(".docs-nav-toggle");
  const mask = document.querySelector(".docs-nav-mask");
  if (!sidebar) return;

  const links = [...sidebar.querySelectorAll('a[href^="#"], a[href*="#"]')].filter(
    (link) => {
      const hash = link.hash;
      return hash && document.getElementById(hash.slice(1));
    }
  );

  const setOpen = (open) => {
    document.body.classList.toggle("docs-nav-open", open);
    if (toggle) toggle.setAttribute("aria-expanded", open ? "true" : "false");
  };

  if (toggle) {
    toggle.addEventListener("click", () => {
      setOpen(!document.body.classList.contains("docs-nav-open"));
    });
  }
  if (mask) mask.addEventListener("click", () => setOpen(false));
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") setOpen(false);
  });
  links.forEach((link) => {
    link.addEventListener("click", () => setOpen(false));
  });

  const setActive = (id) => {
    links.forEach((link) => {
      const on = link.hash === `#${id}`;
      link.classList.toggle("is-active", on);
      if (on) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    });
  };

  const sections = links
    .map((link) => document.getElementById(link.hash.slice(1)))
    .filter(Boolean);

  if (!sections.length || !("IntersectionObserver" in window)) return;

  const visible = new Map();
  const pick = () => {
    const header = parseFloat(
      getComputedStyle(document.documentElement).getPropertyValue("--nav-h")
    ) || 72;
    let current = sections[0].id;
    let best = Infinity;
    sections.forEach((section) => {
      const top = section.getBoundingClientRect().top - header - 16;
      if (top <= 0 && Math.abs(top) < best) {
        best = Math.abs(top);
        current = section.id;
      }
    });
    if (best === Infinity) {
      const firstVisible = sections.find(
        (section) => visible.get(section.id)
      );
      if (firstVisible) current = firstVisible.id;
    }
    setActive(current);
  };

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        visible.set(entry.target.id, entry.isIntersecting);
      });
      pick();
    },
    { rootMargin: "-80px 0px -55% 0px", threshold: [0, 0.15, 1] }
  );
  sections.forEach((section) => observer.observe(section));
  window.addEventListener("scroll", pick, { passive: true });
  pick();
})();
