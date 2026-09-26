(() => {
  const sidebar = document.getElementById("docs-sidebar");
  const toggle = document.querySelector(".docs-nav-toggle");
  const mask = document.querySelector(".docs-nav-mask");
  if (!sidebar) return;

  const usedIds = new Set(
    [...document.querySelectorAll("[id]")].map((el) => el.id)
  );

  const slugId = (sectionId, text) => {
    const base = `${sectionId}-${text
      .toLowerCase()
      .replace(/&/g, " and ")
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-|-$/g, "")}`.slice(0, 72);
    let id = base || `${sectionId}-part`;
    let n = 2;
    while (usedIds.has(id)) id = `${base}-${n++}`;
    usedIds.add(id);
    return id;
  };

  const setSubOpen = (page, open) => {
    const sub = page.querySelector(":scope > .docs-nav-sub");
    const button = page.querySelector(":scope > .docs-nav-subtoggle");
    const parent = page.querySelector(":scope > a");
    if (!sub || !button || !parent) return;
    sub.hidden = !open;
    button.setAttribute("aria-expanded", open ? "true" : "false");
    const name = parent.textContent.trim();
    button.setAttribute(
      "aria-label",
      `${open ? "Hide" : "Show"} subpages for ${name}`
    );
  };

  [...sidebar.querySelectorAll(".docs-nav-pages > a[href^='#']")].forEach(
    (link) => {
      if (link.classList.contains("docs-nav-ext")) return;
      const section = document.getElementById(link.hash.slice(1));
      if (!section) return;
      const heads = [...section.querySelectorAll("h3")];
      if (!heads.length) return;
      const page = document.createElement("div");
      page.className = "docs-nav-page";
      link.replaceWith(page);
      page.appendChild(link);
      const button = document.createElement("button");
      button.type = "button";
      button.className = "docs-nav-subtoggle";
      const sub = document.createElement("div");
      sub.className = "docs-nav-sub";
      sub.hidden = true;
      heads.forEach((heading) => {
        if (!heading.id) heading.id = slugId(section.id, heading.textContent);
        const child = document.createElement("a");
        child.href = `#${heading.id}`;
        child.textContent = heading.textContent.trim();
        sub.appendChild(child);
      });
      page.append(button, sub);
      setSubOpen(page, false);
      button.addEventListener("click", () => {
        setSubOpen(page, button.getAttribute("aria-expanded") !== "true");
      });
    }
  );

  const links = [...sidebar.querySelectorAll('a[href^="#"], a[href*="#"]')].filter(
    (link) => {
      if (link.classList.contains("docs-nav-ext")) return false;
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

  const reveal = (link) => {
    const cat = link.closest("details.docs-nav-cat");
    if (cat) {
      cat.open = true;
      sidebar.querySelectorAll("details.docs-nav-cat").forEach((other) => {
        if (other !== cat) other.open = false;
      });
    }
    const sub = link.closest(".docs-nav-sub");
    if (sub) setSubOpen(sub.parentElement, true);
    const sb = sidebar.getBoundingClientRect();
    const lr = link.getBoundingClientRect();
    if (lr.top < sb.top + 8 || lr.bottom > sb.bottom - 8) {
      sidebar.scrollTop += lr.top - sb.top - 48;
    }
  };

  const setActive = (id) => {
    let current = null;
    links.forEach((link) => {
      const on = link.hash === `#${id}`;
      link.classList.toggle("is-active", on);
      if (on) {
        link.setAttribute("aria-current", "location");
        current = link;
      } else {
        link.removeAttribute("aria-current");
      }
    });
    if (current) reveal(current);
  };

  const sections = links
    .map((link) => document.getElementById(link.hash.slice(1)))
    .filter(Boolean);

  if (!sections.length || !("IntersectionObserver" in window)) {
    const hash = (window.location.hash || "").slice(1);
    if (hash) setActive(hash);
    return;
  }

  const visible = new Map();
  let lastId = "";
  const pick = () => {
    const header =
      parseFloat(
        getComputedStyle(document.documentElement).getPropertyValue("--nav-h")
      ) || 72;
    let current = sections[0].id;
    let best = Infinity;
    sections.forEach((section) => {
      const top = section.getBoundingClientRect().top - header - 16;
      if (top <= 8 && Math.abs(top) < best) {
        best = Math.abs(top);
        current = section.id;
      }
    });
    if (best === Infinity) {
      const firstVisible = sections.find((section) => visible.get(section.id));
      if (firstVisible) current = firstVisible.id;
    }
    if (current === lastId) return;
    lastId = current;
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
  const hash = (window.location.hash || "").slice(1);
  if (hash && document.getElementById(hash)) setActive(hash);
  else pick();
})();
