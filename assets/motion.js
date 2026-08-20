(() => {
  const path = window.location.pathname;
  if (path.endsWith("/index.html")) {
    history.replaceState(null, "", `/${window.location.search}${window.location.hash}`);
  } else if (path.endsWith(".html")) {
    history.replaceState(null, "", `${path.slice(0, -5)}${window.location.search}${window.location.hash}`);
  }

  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (!document.querySelector(".sky")) {
    const sky = document.createElement("div");
    sky.className = "sky";
    sky.setAttribute("aria-hidden", "true");
    sky.innerHTML = '<i class="blob a"></i><i class="blob b"></i><i class="blob c"></i>';
    const grain = document.createElement("div");
    grain.className = "grain";
    grain.setAttribute("aria-hidden", "true");
    const spot = document.createElement("div");
    spot.className = "spot";
    spot.setAttribute("aria-hidden", "true");
    const dust = document.createElement("canvas");
    dust.id = "dust";
    dust.setAttribute("aria-hidden", "true");
    document.body.prepend(sky, dust, grain, spot);
  }

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
  const spot = document.querySelector(".spot");

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
  tabs.forEach((tab) => tab.addEventListener("click", () => showPanel(tab.getAttribute("data-tab"))));
  window.addEventListener("keydown", (e) => {
    if (e.key === "1") showPanel("received");
    if (e.key === "2") showPanel("inspect");
    if (e.key === "3") showPanel("limits");
  });

  if (!reduce) {
    window.addEventListener(
      "pointermove",
      (e) => {
        const x = `${(e.clientX / window.innerWidth) * 100}%`;
        const y = `${(e.clientY / window.innerHeight) * 100}%`;
        if (spot) {
          spot.style.setProperty("--mx", x);
          spot.style.setProperty("--my", y);
        }
        if (mail) {
          const r = mail.getBoundingClientRect();
          const inside = e.clientX >= r.left && e.clientX <= r.right && e.clientY >= r.top && e.clientY <= r.bottom;
          if (inside) {
            mail.style.setProperty("--ry", `${((e.clientX - r.left) / r.width - 0.5) * 10}deg`);
            mail.style.setProperty("--rx", `${-((e.clientY - r.top) / r.height - 0.5) * 8}deg`);
          }
        }
      },
      { passive: true }
    );
    if (mail) {
      mail.addEventListener("mouseleave", () => {
        mail.style.setProperty("--ry", "0deg");
        mail.style.setProperty("--rx", "0deg");
      });
    }
  }

  const hero = document.querySelector("[data-buddy]");
  const actor = document.querySelector("[data-actor]");
  const walkSrc = "assets/mascot-s7-walk.png";
  const standSrc = "assets/mascot-s7-cut.png?v=sword2";

  if (hero) {
    hero.dataset.pose = "idle";
    hero.addEventListener("click", () => {
      hero.dataset.pose = "wave";
      window.setTimeout(() => { hero.dataset.pose = "idle"; }, 900);
    });
  }

  if (actor) {
    const img = actor.querySelector("img");
    const sections = [...document.querySelectorAll(".film-hero, .meet, .site-banner, main > section")];
    const poseFor = (el) => {
      if (!el) return "idle";
      if (el.classList.contains("meet")) return "look";
      if (el.getAttribute("aria-label") === "Why Signet7 exists") return "nod";
      if (el.querySelector && el.querySelector("#who-title")) return "point";
      if (el.querySelector && el.querySelector("[data-mail]")) return "guard";
      if (el.classList.contains("vsn-section")) return "look";
      return "idle";
    };
    let lastY = window.scrollY;
    let walkUntil = 0;
    const place = () => {
      const y = window.scrollY;
      if (Math.abs(y - lastY) > 2) walkUntil = performance.now() + 320;
      lastY = y;
      const walking = performance.now() < walkUntil;
      const heroBox = hero ? hero.getBoundingClientRect() : { bottom: -1 };
      const show = heroBox.bottom < 100;
      actor.hidden = !show;
      actor.classList.toggle("is-on", show);
      if (!show) return;
      const mid = window.innerHeight * 0.52;
      let cur = sections[0];
      for (const s of sections) {
        const r = s.getBoundingClientRect();
        if (r.top < mid && r.bottom > 150) cur = s;
      }
      const r = cur.getBoundingClientRect();
      const top = Math.min(Math.max(r.top + 20, 120), window.innerHeight - 220);
      actor.style.top = top + "px";
      const pose = walking ? "walk" : poseFor(cur);
      actor.dataset.pose = pose;
      if (img) img.src = pose === "walk" ? walkSrc : standSrc;
    };
    window.addEventListener("scroll", place, { passive: true });
    window.addEventListener("resize", place, { passive: true });
    place();
    actor.addEventListener("click", () => {
      actor.dataset.pose = "wave";
      if (img) img.src = standSrc;
      window.setTimeout(place, 850);
    });
  }

  const canvas = document.getElementById("dust");
  if (!canvas || reduce || !canvas.getContext) return;
  const ctx = canvas.getContext("2d");
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  let w = 0;
  let h = 0;
  const bits = Array.from({ length: 70 }, () => ({
    x: Math.random(),
    y: Math.random(),
    s: 0.6 + Math.random() * 1.8,
    v: 0.08 + Math.random() * 0.22,
    gold: Math.random() < 0.28,
  }));
  const resize = () => {
    w = window.innerWidth;
    h = window.innerHeight;
    canvas.width = Math.floor(w * dpr);
    canvas.height = Math.floor(h * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  };
  resize();
  window.addEventListener("resize", resize, { passive: true });
  const tick = () => {
    ctx.clearRect(0, 0, w, h);
    bits.forEach((b) => {
      b.y -= b.v / 180;
      if (b.y < -0.02) {
        b.y = 1.02;
        b.x = Math.random();
      }
      ctx.beginPath();
      ctx.fillStyle = b.gold ? "rgba(255,209,109,0.45)" : "rgba(88,222,248,0.38)";
      ctx.arc(b.x * w, b.y * h, b.s, 0, Math.PI * 2);
      ctx.fill();
    });
    requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
})();
