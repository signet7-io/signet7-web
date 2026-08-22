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

  const drops = [...document.querySelectorAll(".drop")];
  drops.forEach((drop) => {
    const btn = drop.querySelector(".drop-btn");
    if (!btn) return;
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      const open = !drop.classList.contains("is-open");
      drops.forEach((d) => {
        d.classList.toggle("is-open", d === drop && open);
        const b = d.querySelector(".drop-btn");
        if (b) b.setAttribute("aria-expanded", d === drop && open ? "true" : "false");
      });
    });
  });
  document.addEventListener("click", () => {
    drops.forEach((d) => {
      d.classList.remove("is-open");
      const b = d.querySelector(".drop-btn");
      if (b) b.setAttribute("aria-expanded", "false");
    });
  });

  const mail = document.querySelector("[data-mail]");
  const spot = document.querySelector(".spot");
  const hint = document.querySelector("[data-hint]");
  const nextBtn = document.querySelector("[data-demo-next]");
  const backBtn = document.querySelector("[data-demo-back]");
  const label = document.querySelector("[data-demo-label]");
  const panels = [...document.querySelectorAll("[data-panel]")];
  const acct = document.querySelector("[data-hot-acct]");
  const from = document.querySelector("[data-hot-from]");
  let demoStep = 1;
  const hints = {
    1: "This looks like a real vendor. It isn't enough.",
    2: "The words still match. The sender is not tied to that company.",
    3: "VSN: that company's key is not listed as still theirs. Customer companies are not in this lookup yet.",
    4: "You can keep this result as a file. Signet7 does not send money.",
  };
  const nextLabel = {
    1: "Next · Check the seal",
    2: "Next · Check VSN",
    3: "Next · Keep the record",
    4: "Start over",
  };
  const say = (text) => {
    if (hint) hint.textContent = text;
  };
  const showDemo = (step) => {
    demoStep = Math.min(4, Math.max(1, step));
    if (label) label.textContent = `Step ${demoStep} of 4`;
    panels.forEach((panel) => {
      const name = panel.getAttribute("data-panel");
      const on = (demoStep === 2 && name === "inspect") || (demoStep === 3 && name === "vsn") || (demoStep === 4 && name === "decide");
      panel.classList.toggle("is-on", on);
    });
    if (backBtn) backBtn.hidden = demoStep === 1;
    if (nextBtn) {
      nextBtn.hidden = false;
      nextBtn.textContent = nextLabel[demoStep];
    }
    const mark = demoStep >= 2;
    if (acct) acct.classList.toggle("is-on", mark);
    if (from) from.classList.toggle("is-on", mark);
    say(hints[demoStep]);
  };
  if (nextBtn) nextBtn.addEventListener("click", () => showDemo(demoStep === 4 ? 1 : demoStep + 1));
  if (backBtn) backBtn.addEventListener("click", () => showDemo(demoStep - 1));
  if (mail) showDemo(1);

  const bar = document.querySelector("[data-progress]");
  const chapters = [...document.querySelectorAll("[data-chapter]")];
  const onScroll = () => {
    const max = Math.max(document.documentElement.scrollHeight - window.innerHeight, 1);
    if (bar) bar.style.width = `${Math.min(100, (window.scrollY / max) * 100)}%`;
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  const wavePin = document.querySelector("[data-wave-pin]");
  const waveLine = document.querySelector("[data-wave-line]");
  const waves = [
    "The email lands.",
    "You look once.",
    "The seal answers.",
    "You keep the record."
  ];
  const onWave = () => {
    if (!wavePin || !waveLine) return;
    const r = wavePin.getBoundingClientRect();
    const span = Math.max(wavePin.offsetHeight - window.innerHeight, 1);
    const gone = Math.min(Math.max(-r.top, 0), span);
    const i = Math.min(waves.length - 1, Math.floor((gone / span) * waves.length));
    if (waveLine.textContent !== waves[i]) waveLine.textContent = waves[i];
  };
  window.addEventListener("scroll", onWave, { passive: true });
  onWave();

  const deskRoot = document.querySelector("[data-desks]");
  if (deskRoot) {
    const copy = {
      law: ["Law office", "Settlement, retainer, or “updated wiring.” Inspect the seal. Keep the record."],
      title: ["Title / closing", "The irreversible detail is the account. Check the seal before you change where money goes."],
      build: ["Construction", "Draws, change orders, sub pay-apps. Ordinary-looking email. That is the trap."],
      pay: ["Payroll", "A “new direct deposit” from someone who looks like staff. Check who it came from. Keep the record."],
      finance: ["Finance / AP", "Invoice plus new routing. Keep Outlook. Watch the money mailbox. Recipients use the live check."],
      bank: ["Bank / credit union ops", "Internal or vendor instructions that move accounts. You still decide. Signet7 is the last look and the record you keep."]
    };
    const title = document.querySelector("[data-desk-title]");
    const body = document.querySelector("[data-desk-body]");
    deskRoot.addEventListener("click", (e) => {
      const btn = e.target.closest("[data-desk]");
      if (!btn) return;
      deskRoot.querySelectorAll("[data-desk]").forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
      const row = copy[btn.getAttribute("data-desk")];
      if (row && title) title.textContent = row[0];
      if (row && body) body.textContent = row[1];
    });
  }
  if (chapters.length && "IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) en.target.classList.add("is-in");
      });
    }, { threshold: 0.35 });
    chapters.forEach((el) => io.observe(el));
  }

  const quest = document.querySelector("[data-quest]");
  if (quest) {
    const answers = {};
    const whoLine = {
      finance: "Finance and AP live on wiring changes.",
      title: "Title and closing live on payoff letters.",
      law: "Law firms live on settlement directions.",
      build: "Construction lives on change-order payments.",
      pay: "Payroll lives on deposit-account changes.",
      me: "If it is just you, one bad wire is the whole company.",
    };
    const showStep = (id) => {
      quest.querySelectorAll("[data-step]").forEach((el) => {
        const on = el.getAttribute("data-step") === String(id);
        el.hidden = !on;
        el.classList.toggle("is-on", on);
      });
      const cards = quest.querySelector("[data-step-cards]");
      if (cards) cards.hidden = id !== "1" && id !== 1;
      const land = quest.querySelector(".quest-land");
      if (land) land.hidden = id === "result";
      const n = id === "result" ? 3 : Number(id);
      const count = quest.querySelector("[data-quest-count]");
      if (count) {
        count.hidden = id === "result";
        count.textContent = `Question ${n} of 3`;
      }
      const fill = quest.querySelector("[data-quest-fill]");
      if (fill) fill.className = `p${n}${id === "result" ? " done" : ""}`;
    };
    const writeResult = () => {
      const title = quest.querySelector("[data-result-title]");
      const body = quest.querySelector("[data-result-body]");
      const kick = quest.querySelector("[data-result-kicker]");
      const money = answers.money;
      const act = answers.act;
      const who = answers.who;
      if (kick) kick.textContent = whoLine[who] || "For you";
      if (money === "no") {
        if (title) title.textContent = "This is for people who move money because an email said so.";
        if (body) body.textContent = "If that is not your world, you can still look. Signet7 inspects a sealed email and keeps a record you can produce.";
      } else if (act === "reply") {
        if (title) title.textContent = "Replying to that email is the trap.";
        if (body) body.textContent = "Signet7 is the check before you change where money goes — who it was tied to, whether the words still match, the record you keep.";
      } else if (act === "call") {
        if (title) title.textContent = "Keep the proof too.";
        if (body) body.textContent = "Signet7 is the file you can show later: who it came from, whether the words still match, a record that is not locked in one company's screen.";
      } else {
        if (title) title.textContent = "Looks ordinary. That's the trap.";
        if (body) body.textContent = "Signet7 is the check: who it was tied to, whether the words still match, the record you keep.";
      }
    };
    quest.addEventListener("click", (e) => {
      const btn = e.target.closest("[data-go]");
      if (!btn || !quest.contains(btn)) return;
      const k = btn.getAttribute("data-k");
      const v = btn.getAttribute("data-v");
      if (k) answers[k] = v;
      const next = btn.getAttribute("data-go");
      if (next === "result") writeResult();
      showStep(next);
    });
  }

  document.querySelectorAll("section.facts").forEach((factsRoot) => {
    const cards = [...factsRoot.querySelectorAll(".fact")];
    const feeds = [
      [
        ["$3.05B", "Business Email Compromise losses reported to FBI IC3 in 2025."],
        ["24,768", "Business Email Compromise complaints reported to FBI IC3 in 2025."],
        ["$20.9B", "Internet-crime losses reported to IC3 in 2025."],
        ["191K+", "Phishing/spoofing complaints reported to FBI IC3 in 2025."],
      ],
      [
        ["1,008,597", "Internet-crime complaints reported to FBI IC3 in 2025."],
        ["26%", "Increase in losses reported to IC3 from 2024 to 2025."],
        ["$20,699", "Average loss reported to FBI IC3 in 2025."],
        ["$17.7B", "Cyber-enabled fraud losses reported to IC3 in 2025."],
      ],
      [
        ["$3.05B", "Business Email Compromise losses reported to FBI IC3 in 2025."],
        ["$275M", "Real estate fraud losses reported to FBI IC3 in 2025."],
        ["12,368", "Real estate fraud complaints reported to FBI IC3 in 2025."],
        ["85%", "Share of 2025 IC3 losses that were cyber-enabled fraud."],
      ],
    ];
    let i = 0;
    const flapCard = (card, pair) => {
      card.classList.add("is-flap");
      window.setTimeout(() => {
        const strong = card.querySelector("strong");
        const span = card.querySelector("span");
        if (strong) strong.textContent = pair[0];
        if (span) span.textContent = pair[1];
      }, 220);
      window.setTimeout(() => card.classList.remove("is-flap"), 560);
    };
    if (!reduce && cards.length === 4) {
      window.setInterval(() => {
        i = (i + 1) % feeds.length;
        const feed = feeds[i];
        cards.forEach((card, n) => {
          window.setTimeout(() => flapCard(card, feed[n]), n * 420);
        });
      }, 8200);
    }
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

  const canvas = document.getElementById("dust");
  if (document.getElementById("mail-flow") || !canvas || reduce || !canvas.getContext) return;
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
