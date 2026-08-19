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
    const dock = () => buddy.classList.toggle("is-docked", window.scrollY > 140);
    dock();
    window.addEventListener("scroll", dock, { passive: true });
    const hintEl = buddy.querySelector(".buddy-hint");
    const img = buddy.querySelector("img");
    const acts = [
      "toss","bank","hi5","catch","rocket","stampede","taplogo","hide",
      "coin","bow","portal","stack","cannon","tug","clone","ladder",
      "pinball","rain","parade","zoom"
    ];
    const lines = [
      "incoming","got it","tag","nice catch","blast off","gang's here",
      "tapped the seal","peek","heads","encore","gone","up we go",
      "fire","tug","twins","climbing","boing","mail call","walk-on","whoa"
    ];
    let last = "";
    let busy = false;
    const stage = document.createElement("div");
    stage.className = "buddy-stage";
    stage.setAttribute("aria-hidden", "true");
    document.body.appendChild(stage);

    const wait = (ms) => new Promise((r) => window.setTimeout(r, ms));
    const rect = (el) => el.getBoundingClientRect();
    const home = () => {
      const r = rect(buddy);
      return { x: r.left + r.width / 2, y: r.top + r.height / 2, w: r.width, h: r.height };
    };
    const spawn = (cls, extra) => {
      const el = document.createElement("div");
      el.className = "buddy-prop " + cls;
      if (extra) Object.assign(el, extra);
      stage.appendChild(el);
      return el;
    };
    const place = (el, x, y) => {
      el.style.left = Math.round(x) + "px";
      el.style.top = Math.round(y) + "px";
    };
    const run = (el, keyframes, ms, ease) => {
      const a = el.animate(keyframes, { duration: ms, easing: ease || "cubic-bezier(.22,.8,.28,1)", fill: "forwards" });
      return a.finished || wait(ms);
    };
    const kill = (el) => { if (el && el.remove) el.remove(); };

    const mailProp = (x, y) => {
      const el = spawn("buddy-mail");
      place(el, x, y);
      return el;
    };
    const palProp = (x, y) => {
      const el = spawn("buddy-pal");
      const pic = document.createElement("img");
      pic.src = "assets/sidekick-pal.svg";
      pic.alt = "";
      pic.width = 160;
      pic.height = 168;
      el.appendChild(pic);
      place(el, x, y);
      return el;
    };
    const mini = (x, y) => {
      const el = spawn("buddy-mini");
      const pic = document.createElement("img");
      pic.src = "assets/sidekick.svg?v=2";
      pic.alt = "";
      el.appendChild(pic);
      place(el, x, y);
      return el;
    };

    const actsMap = {
      async toss() {
        const h = home();
        const letter = mailProp(h.x, h.y - 20);
        await run(letter, [
          { transform: "translate(0,0) rotate(0)" },
          { transform: `translate(${window.innerWidth * 0.38}px,-180px) rotate(160deg)` },
          { transform: `translate(${window.innerWidth * 0.62}px, 20px) rotate(300deg)` },
          { transform: `translate(${window.innerWidth * 0.78}px, ${window.innerHeight * 0.35}px) rotate(420deg)` }
        ], 1400);
        await run(letter, [
          { transform: `translate(${window.innerWidth * 0.78}px, ${window.innerHeight * 0.35}px) rotate(420deg)` },
          { transform: `translate(${window.innerWidth * 0.7}px, ${window.innerHeight * 0.12}px) rotate(480deg)` },
          { transform: `translate(${window.innerWidth - 80}px, ${window.innerHeight - 80}px) rotate(620deg)` }
        ], 900, "cubic-bezier(.2,.9,.3,1)");
        kill(letter);
      },
      async bank() {
        const h = home();
        const mail = document.querySelector("[data-mail]");
        const wall = mail ? rect(mail).left - 80 : window.innerWidth - 120;
        await run(buddy, [
          { transform: "translate(0,0)" },
          { transform: `translate(${wall - h.x}px, -20px)` },
          { transform: `translate(${wall - h.x + 18}px, 8px)` },
          { transform: "translate(0,0)" }
        ], 1600);
      },
      async hi5() {
        const h = home();
        const pal = palProp(window.innerWidth + 20, h.y - 90);
        await run(pal, [
          { transform: "translate(0,0)" },
          { transform: `translate(${h.x - window.innerWidth + 90}px, 0)` }
        ], 700);
        await run(buddy, [{ transform: "rotate(0)" }, { transform: "rotate(-18deg) scale(1.08)" }, { transform: "rotate(0)" }], 500);
        await run(pal, [{ transform: `translate(${h.x - window.innerWidth + 90}px, 0) rotate(0)` }, { transform: `translate(${h.x - window.innerWidth + 90}px, 0) rotate(16deg)` }, { transform: `translate(${h.x - window.innerWidth + 90}px, 0) rotate(0)` }], 400);
        await run(pal, [
          { transform: `translate(${h.x - window.innerWidth + 90}px, 0)` },
          { transform: "translate(40px,-20px)" }
        ], 600);
        kill(pal);
      },
      async catch() {
        const h = home();
        const pal = palProp(window.innerWidth - 200, h.y - 80);
        await run(pal, [{ opacity: 0 }, { opacity: 1 }], 200);
        const letter = mailProp(h.x, h.y - 10);
        for (let i = 0; i < 3; i += 1) {
          const toPal = i % 2 === 0;
          await run(letter, [
            { transform: "translate(0,0)" },
            { transform: `translate(${(toPal ? window.innerWidth - 240 - h.x : 0)}px, ${toPal ? -40 : 0}px) rotate(${180 + i * 90}deg)` }
          ], 450);
        }
        kill(letter);
        await run(pal, [{ opacity: 1 }, { opacity: 0 }], 250);
        kill(pal);
      },
      async rocket() {
        await run(buddy, [
          { transform: "translateY(0) rotate(0)" },
          { transform: "translateY(-40px) rotate(-8deg)" },
          { transform: `translateY(${-home().y - 80}px) rotate(-4deg)` }
        ], 800);
        const chute = spawn("buddy-mail");
        const h = home();
        place(chute, h.x - 20, 20);
        await run(buddy, [
          { transform: `translateY(${-h.y - 80}px)` },
          { transform: "translateY(0)" }
        ], 1100, "cubic-bezier(.2,.9,.2,1.2)");
        await run(chute, [{ opacity: 1, transform: "translateY(0)" }, { opacity: 0, transform: "translateY(80px)" }], 400);
        kill(chute);
      },
      async stampede() {
        const y = window.innerHeight - 110;
        const pack = [0, 1, 2, 3].map((i) => mini(-90 - i * 70, y));
        await Promise.all(pack.map((el, i) => run(el, [
          { transform: "translateX(0)" },
          { transform: `translateX(${window.innerWidth + 220}px)` }
        ], 1600 + i * 120)));
        pack.forEach(kill);
      },
      async taplogo() {
        const logo = document.querySelector(".site-header .brand img") || document.querySelector(".brand img");
        const h = home();
        const t = logo ? rect(logo) : { left: 40, top: 20, width: 80, height: 80 };
        await run(buddy, [
          { transform: "translate(0,0)" },
          { transform: `translate(${t.left + t.width / 2 - h.x}px, ${t.top + t.height - h.y + 20}px) scale(.7)` },
          { transform: `translate(${t.left + t.width / 2 - h.x}px, ${t.top + t.height - h.y}px) scale(.7)` },
          { transform: "translate(0,0)" }
        ], 1800);
        if (logo) await run(logo, [{ transform: "rotate(0)" }, { transform: "rotate(-10deg)" }, { transform: "rotate(8deg)" }, { transform: "rotate(0)" }], 500);
      },
      async hide() {
        const mail = document.querySelector("[data-mail]");
        const h = home();
        const t = mail ? rect(mail) : { left: window.innerWidth - 280, top: h.y, width: 200, height: 200 };
        await run(buddy, [
          { transform: "translate(0,0)", opacity: 1 },
          { transform: `translate(${t.left + 40 - h.x}px, ${t.top + 40 - h.y}px)`, opacity: 0.15 },
          { transform: `translate(${t.left + 40 - h.x}px, ${t.top + 10 - h.y}px)`, opacity: 1 },
          { transform: "translate(0,0)", opacity: 1 }
        ], 2000);
      },
      async coin() {
        const h = home();
        const coin = spawn("buddy-coin");
        place(coin, h.x + 30, h.y + 20);
        await run(buddy, [{ transform: "rotate(0)" }, { transform: "rotate(20deg)" }, { transform: "rotate(0)" }], 280);
        await run(coin, [
          { transform: "translate(0,0) rotate(0)" },
          { transform: `translate(${window.innerWidth * 0.35}px, -80px) rotate(280deg)` },
          { transform: `translate(${window.innerWidth * 0.7}px, 40px) rotate(620deg)` },
          { transform: `translate(${window.innerWidth - 40}px, ${window.innerHeight - 60}px) rotate(980deg)` }
        ], 1600);
        kill(coin);
      },
      async bow() {
        const h = home();
        const spot = spawn("buddy-spot");
        place(spot, h.x - 110, h.y - 80);
        const pal = palProp(h.x + 90, h.y - 80);
        await run(spot, [{ opacity: 0 }, { opacity: 1 }], 200);
        await run(buddy, [{ transform: "rotate(0)" }, { transform: "rotate(18deg) translateY(12px)" }, { transform: "rotate(0)" }], 700);
        await run(pal, [{ transform: "rotate(0)" }, { transform: "rotate(-16deg) translateY(10px)" }, { transform: "rotate(0)" }], 700);
        await run(spot, [{ opacity: 1 }, { opacity: 0 }], 250);
        kill(spot); kill(pal);
      },
      async portal() {
        const h = home();
        const hole = spawn("buddy-portal");
        place(hole, h.x - 40, h.y + 40);
        await run(hole, [{ transform: "scale(0)" }, { transform: "scale(1)" }], 280);
        await run(buddy, [{ transform: "scale(1)", opacity: 1 }, { transform: "scale(0.1) translateY(40px)", opacity: 0 }], 400);
        const cta = document.querySelector(".button-primary") || document.querySelector("h1");
        const t = cta ? rect(cta) : { left: window.innerWidth / 2, top: window.innerHeight / 2, width: 40, height: 40 };
        place(hole, t.left, t.top);
        await run(buddy, [{ transform: `translate(${t.left - h.x}px, ${t.top - h.y}px) scale(0.2)`, opacity: 0 }, { transform: `translate(${t.left - h.x}px, ${t.top - h.y}px) scale(1)`, opacity: 1 }, { transform: "translate(0,0) scale(1)", opacity: 1 }], 1100);
        await run(hole, [{ transform: "scale(1)" }, { transform: "scale(0)" }], 220);
        kill(hole);
      },
      async stack() {
        const h = home();
        const pal = palProp(h.x - 20, h.y - 200);
        await run(pal, [{ transform: "translateY(-80px)" }, { transform: "translateY(70px)" }], 500, "cubic-bezier(.2,1.3,.3,1)");
        await run(buddy, [{ transform: "translateY(0)" }, { transform: "translateY(10px) rotate(-6deg)" }, { transform: "translateY(0) rotate(8deg)" }, { transform: "translateY(0)" }], 700);
        await run(pal, [{ transform: "translateY(70px) rotate(0)" }, { transform: "translate(80px, 40px) rotate(90deg)", opacity: 1 }, { opacity: 0 }], 600);
        kill(pal);
      },
      async cannon() {
        const h = home();
        await run(buddy, [{ transform: "rotate(0)" }, { transform: "rotate(-24deg)" }], 180);
        const sparks = Array.from({ length: 18 }, (_, i) => {
          const s = spawn("buddy-spark" + (i % 3 === 0 ? " gold" : ""));
          place(s, h.x + 20, h.y - 10);
          return run(s, [
            { transform: "translate(0,0)", opacity: 1 },
            { transform: `translate(${180 + Math.random() * 520}px, ${-80 + Math.random() * 220}px)`, opacity: 0 }
          ], 700 + Math.random() * 400);
        });
        await Promise.all(sparks);
        await run(buddy, [{ transform: "rotate(-24deg)" }, { transform: "rotate(0)" }], 200);
        [...stage.querySelectorAll(".buddy-spark")].forEach(kill);
      },
      async tug() {
        const h = home();
        const pal = palProp(h.x + 140, h.y - 80);
        const rope = mailProp(h.x + 40, h.y - 10);
        rope.style.width = "90px";
        await run(buddy, [{ transform: "translateX(0)" }, { transform: "translateX(-16px)" }, { transform: "translateX(10px)" }, { transform: "translateX(0)" }], 800);
        await run(pal, [{ transform: "translateX(0)" }, { transform: "translateX(16px)" }, { transform: "translateX(-10px)" }, { transform: "translateX(0)" }], 800);
        await run(rope, [{ transform: "scaleX(1)" }, { transform: "scaleX(1.4) rotate(8deg)" }, { transform: "scale(.2) rotate(40deg)", opacity: 0 }], 400);
        kill(rope); kill(pal);
      },
      async clone() {
        const h = home();
        const twin = mini(h.x - 40, h.y - 90);
        twin.style.width = home().w + "px";
        twin.style.height = home().h + "px";
        await run(twin, [{ transform: "translateX(0) scaleX(-1)", opacity: 0 }, { transform: "translateX(-70px) scaleX(-1)", opacity: 1 }], 300);
        await run(buddy, [{ transform: "rotate(0)" }, { transform: "rotate(-12deg)" }, { transform: "rotate(12deg)" }, { transform: "rotate(0)" }], 700);
        await run(twin, [{ transform: "translateX(-70px) scaleX(-1)", opacity: 1 }, { transform: "translateX(-70px) scaleX(-1) scale(0.2)", opacity: 0 }], 280);
        kill(twin);
      },
      async ladder() {
        const h = home();
        const lad = spawn("buddy-ladder");
        place(lad, h.x + 30, h.y - 40);
        await run(lad, [{ transform: "scaleY(0)", transformOrigin: "bottom" }, { transform: "scaleY(1)" }], 280);
        await run(buddy, [{ transform: "translateY(0)" }, { transform: "translate(30px,-120px)" }, { transform: "translate(30px,-120px) rotate(-8deg)" }, { transform: "translate(0,0)" }], 1600);
        await run(lad, [{ opacity: 1 }, { opacity: 0 }], 200);
        kill(lad);
      },
      async pinball() {
        const h = home();
        await run(buddy, [
          { transform: "translate(0,0)" },
          { transform: `translate(${window.innerWidth - h.x - 80}px, ${80 - h.y}px)` },
          { transform: `translate(${40 - h.x}px, ${window.innerHeight - h.y - 80}px)` },
          { transform: `translate(${window.innerWidth - h.x - 100}px, ${window.innerHeight / 2 - h.y}px)` },
          { transform: "translate(0,0)" }
        ], 2200, "linear");
      },
      async rain() {
        const drops = Array.from({ length: 10 }, (_, i) => {
          const el = mailProp(80 + i * 110, -50);
          return run(el, [
            { transform: "translateY(0) rotate(0)", opacity: 1 },
            { transform: `translateY(${window.innerHeight + 40}px) rotate(${120 + i * 20}deg)`, opacity: 1 }
          ], 900 + i * 70);
        });
        await run(buddy, [{ transform: "translateY(0)" }, { transform: "translate(20px,-24px)" }, { transform: "translate(-10px,0)" }], 900);
        await Promise.all(drops);
        [...stage.querySelectorAll(".buddy-mail")].forEach(kill);
      },
      async parade() {
        const h = home();
        const pal = palProp(-180, h.y - 80);
        await run(buddy, [{ transform: "translateX(0)" }, { transform: `translateX(${window.innerWidth - h.x - 80}px)` }, { transform: "translateX(0)" }], 2200);
        await run(pal, [{ transform: "translateX(0)" }, { transform: `translateX(${window.innerWidth + 80}px)` }], 2200);
        kill(pal);
      },
      async zoom() {
        const root = document.querySelector(".meet") || document.body;
        await run(root, [
          { transform: "scale(1)" },
          { transform: "scale(1.06) rotate(-1.2deg)" },
          { transform: "scale(1)" }
        ], 900);
      }
    };

    const play = async () => {
      if (busy) return;
      let pick = acts[Math.floor(Math.random() * acts.length)];
      if (pick === last) pick = acts[(acts.indexOf(pick) + 1) % acts.length];
      last = pick;
      busy = true;
      buddy.classList.add("is-busy");
      if (hintEl) hintEl.textContent = lines[acts.indexOf(pick)] || "click me";
      try {
        if (!reduce && actsMap[pick]) await actsMap[pick]();
      } finally {
        buddy.style.transform = "";
        buddy.classList.remove("is-busy");
        if (hintEl) hintEl.textContent = "click me";
        stage.innerHTML = "";
        busy = false;
      }
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
