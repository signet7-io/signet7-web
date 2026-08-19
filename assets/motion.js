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

  const buddy = document.querySelector("[data-buddy]");
  if (buddy) {
    const tricks = [
      "hop","spin","wiggle","grow","flip","wave","glow","slide","tilt","shake",
      "blink","moonwalk","stretch","squash","twirl","peek","drop","wobble","pulse","salute"
    ];
    const lines = [
      "sealed","hop","spin","check first","not spam","keep the proof",
      "call the person","bound?","still match?","click again"
    ];
    const hintEl = buddy.querySelector(".buddy-hint");
    let last = "";
    const play = () => {
      if (buddy.classList.contains("is-busy")) return;
      let pick = tricks[Math.floor(Math.random() * tricks.length)];
      if (pick === last) pick = tricks[(tricks.indexOf(pick) + 1) % tricks.length];
      last = pick;
      buddy.classList.add("is-busy");
      buddy.dataset.trick = pick;
      if (hintEl) hintEl.textContent = lines[Math.floor(Math.random() * lines.length)];
      const img = buddy.querySelector("img");
      let finished = false;
      const done = () => {
        if (finished) return;
        finished = true;
        buddy.removeAttribute("data-trick");
        buddy.classList.remove("is-busy");
        if (hintEl) hintEl.textContent = "click me";
        if (img) img.removeEventListener("animationend", done);
      };
      if (reduce) {
        done();
        return;
      }
      if (img) img.addEventListener("animationend", done);
      window.setTimeout(done, 1100);
    };
    buddy.addEventListener("click", play);
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
