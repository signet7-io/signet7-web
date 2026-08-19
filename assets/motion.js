(() => {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const canvas = document.getElementById("field");
  const toggle = document.querySelector(".nav-toggle");

  if (toggle) {
    toggle.addEventListener("click", () => {
      const open = document.body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  const scenes = [...document.querySelectorAll("[data-scene]")];
  const onScroll = () => {
    const vh = window.innerHeight || 1;
    scenes.forEach((scene) => {
      const r = scene.getBoundingClientRect();
      const start = r.top - vh * 0.15;
      const end = r.bottom - vh * 0.55;
      const p = 1 - Math.min(1, Math.max(0, end / (end - start || 1)));
      scene.classList.toggle("is-on", r.top < vh * 0.72 && r.bottom > vh * 0.28);
      scene.style.setProperty("--p", String(p));
    });
  };

  if (!reduce) {
    let ticking = false;
    window.addEventListener(
      "scroll",
      () => {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(() => {
          onScroll();
          ticking = false;
        });
      },
      { passive: true }
    );
    onScroll();
  } else {
    scenes.forEach((s) => s.classList.add("is-on"));
  }

  if (!canvas || reduce || !canvas.getContext) return;

  const ctx = canvas.getContext("2d", { alpha: true });
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  let w = 0;
  let h = 0;
  const COUNT = 1400;
  const pts = [];

  const resize = () => {
    w = canvas.clientWidth;
    h = canvas.clientHeight;
    canvas.width = Math.floor(w * dpr);
    canvas.height = Math.floor(h * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  };

  const target = (i, n) => {
    const a = (i / n) * Math.PI * 2;
    const band = i % 6 === 0 ? 0.36 : i % 3 === 0 ? 0.58 : 0.8;
    return [Math.cos(a) * band, Math.sin(a) * band];
  };

  for (let i = 0; i < COUNT; i += 1) {
    const [sx, sy] = target(i, COUNT);
    pts.push({
      x: (Math.random() - 0.5) * 2,
      y: (Math.random() - 0.5) * 2,
      sx,
      sy,
      s: 1.2 + Math.random() * 2.4,
      hue: Math.random() < 0.18 ? "gold" : "cyan",
    });
  }

  resize();
  window.addEventListener("resize", resize, { passive: true });

  let t0 = performance.now();
  const tick = (now) => {
    const t = (now - t0) / 1000;
    const scroll = Math.min(1, window.scrollY / Math.max(1, window.innerHeight * 1.2));
    const rot = t * 0.18;
    const mix = 1;
    ctx.clearRect(0, 0, w, h);
    const cx = w * 0.70;
    const cy = h * 0.52;
    const scale = Math.min(w, h) * 0.32;
    const fade = Math.max(0.35, 1 - scroll * 0.7);
    for (const p of pts) {
      const tx = p.sx * Math.cos(rot) - p.sy * Math.sin(rot);
      const ty = p.sx * Math.sin(rot) + p.sy * Math.cos(rot);
      p.x += (tx - p.x) * 0.06;
      p.y += (ty - p.y) * 0.06;
      const wobble = Math.sin(t * 1.4 + p.x * 6) * 4;
      const px = cx + p.x * scale + wobble * (1 - scroll);
      const py = cy + p.y * scale;
      ctx.beginPath();
      ctx.fillStyle =
        p.hue === "gold"
          ? `rgba(255, 209, 109, ${0.45 * fade + 0.2})`
          : `rgba(88, 222, 248, ${0.4 * fade + 0.25})`;
      ctx.arc(px, py, p.s, 0, Math.PI * 2);
      ctx.fill();
    }
    requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
})();
