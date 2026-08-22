(() => {
  const canvas = document.getElementById("mail-flow");
  if (!canvas || !canvas.getContext) return;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce) {
    canvas.hidden = true;
    return;
  }

  const ctx = canvas.getContext("2d");
  const trail = document.createElement("canvas");
  const tctx = trail.getContext("2d");
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  let w = 0;
  let h = 0;

  const routes = [];
  const packets = [];

  const theme = () => document.documentElement.getAttribute("data-theme") === "dark";

  const resize = () => {
    w = canvas.clientWidth || window.innerWidth;
    h = canvas.clientHeight || Math.max(420, window.innerHeight * 0.72);
    canvas.width = Math.floor(w * dpr);
    canvas.height = Math.floor(h * dpr);
    trail.width = canvas.width;
    trail.height = canvas.height;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    tctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    buildRoutes();
  };

  const hub = (x, y) => [x * w, y * h];

  const buildRoutes = () => {
    routes.length = 0;
    const nodes = [
      hub(0.06, 0.58),
      hub(0.22, 0.42),
      hub(0.48, 0.36),
      hub(0.72, 0.44),
      hub(0.9, 0.38),
      hub(0.82, 0.68),
      hub(0.58, 0.78),
      hub(0.3, 0.74)
    ];
    for (let i = 0; i < nodes.length; i++) {
      const a = nodes[i];
      const b = nodes[(i + 1) % nodes.length];
      const c = nodes[(i + 3) % nodes.length];
      routes.push({ a, b, k: 70 + (i % 4) * 24, seal: i % 2 === 0 });
      routes.push({ a, b: c, k: -50 - (i % 3) * 18, seal: i % 3 === 0 });
    }
  };

  const ctrl = (a, b, k) => {
    const mx = (a[0] + b[0]) / 2;
    const my = (a[1] + b[1]) / 2;
    const dx = b[1] - a[1];
    const dy = a[0] - b[0];
    const m = Math.hypot(dx, dy) || 1;
    return [mx + (dx / m) * k, my + (dy / m) * k];
  };

  const bez = (p0, p1, p2, p3, t) => {
    const u = 1 - t;
    return [
      u * u * u * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t * t * t * p3[0],
      u * u * u * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t * t * t * p3[1]
    ];
  };

  const spawn = () => {
    const r = routes[(Math.random() * routes.length) | 0];
    if (!r) return;
    const c1 = ctrl(r.a, r.b, r.k);
    const c2 = ctrl(r.a, r.b, r.k * 0.25);
    packets.push({
      p0: r.a,
      p1: c1,
      p2: c2,
      p3: r.b,
      t: Math.random() * 0.2,
      v: 0.0014 + Math.random() * 0.0028,
      seal: r.seal && Math.random() < 0.55,
      flash: 0,
      last: null
    });
  };

  const drawEnvelope = (x, y, ang, sealed, gold, ink) => {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(ang);
    ctx.fillStyle = sealed ? gold : ink;
    ctx.globalAlpha = sealed ? 0.95 : 0.72;
    ctx.beginPath();
    ctx.roundRect(-9, -6, 18, 12, 2);
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(-9, -6);
    ctx.lineTo(0, 2);
    ctx.lineTo(9, -6);
    ctx.strokeStyle = sealed ? "#fff6d8" : "rgba(255,255,255,.55)";
    ctx.lineWidth = 1.2;
    ctx.stroke();
    ctx.restore();
  };

  const tick = () => {
    const dark = theme();
    const gold = dark ? "rgba(228,174,58,1)" : "rgba(215,161,46,1)";
    const ink = dark ? "rgba(232,242,248,.88)" : "rgba(22,32,44,.78)";
    const glow = dark ? "rgba(88,194,216,.55)" : "rgba(47,138,166,.4)";

    tctx.globalCompositeOperation = "source-over";
    tctx.fillStyle = dark ? "rgba(7,16,24,0.08)" : "rgba(247,251,254,0.1)";
    tctx.fillRect(0, 0, w, h);

    if (packets.length < 56 && Math.random() < 0.35) spawn();

    tctx.lineCap = "round";
    for (let i = packets.length - 1; i >= 0; i--) {
      const p = packets[i];
      const prev = bez(p.p0, p.p1, p.p2, p.p3, p.t);
      p.t += p.v;
      const now = bez(p.p0, p.p1, p.p2, p.p3, Math.min(p.t, 1));
      tctx.beginPath();
      tctx.moveTo(prev[0], prev[1]);
      tctx.lineTo(now[0], now[1]);
      tctx.strokeStyle = p.seal ? gold : glow;
      tctx.lineWidth = p.seal ? 2.4 : 1.3;
      tctx.globalAlpha = p.seal ? 0.85 : 0.45;
      tctx.stroke();
      p.last = now;
      if (p.t > 0.97 && p.seal) p.flash = 1;
      if (p.t >= 1) packets.splice(i, 1);
    }

    ctx.clearRect(0, 0, w, h);
    ctx.globalAlpha = 1;
    ctx.drawImage(trail, 0, 0, w, h);

    packets.forEach((p) => {
      if (!p.last) return;
      const look = bez(p.p0, p.p1, p.p2, p.p3, Math.min(p.t + 0.01, 1));
      const ang = Math.atan2(look[1] - p.last[1], look[0] - p.last[0]);
      ctx.save();
      if (p.seal) {
        ctx.shadowColor = gold;
        ctx.shadowBlur = 18;
      }
      drawEnvelope(p.last[0], p.last[1], ang, p.seal, gold, ink);
      if (p.flash > 0.04) {
        ctx.beginPath();
        ctx.arc(p.last[0], p.last[1], 10 + (1 - p.flash) * 26, 0, Math.PI * 2);
        ctx.strokeStyle = gold;
        ctx.globalAlpha = p.flash;
        ctx.lineWidth = 2;
        ctx.stroke();
        p.flash *= 0.9;
      }
      ctx.restore();
    });

    requestAnimationFrame(tick);
  };

  resize();
  window.addEventListener("resize", resize, { passive: true });
  new MutationObserver(resize).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
  for (let i = 0; i < 24; i++) spawn();
  requestAnimationFrame(tick);
})();
