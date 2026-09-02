(() => {
  const path = window.location.pathname;
  if (path.endsWith("/index.html")) {
    history.replaceState(null, "", `/${window.location.search}${window.location.hash}`);
  } else if (path.endsWith(".html")) {
    history.replaceState(null, "", `${path.slice(0, -5)}${window.location.search}${window.location.hash}`);
  }

  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (!document.querySelector(".sky")) {
    /* no-op: old sky/dust layers were lag. Keep the hook for older CSS. */
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
    3: "VSN (Verifiable Sender Network): that company's key is not listed as still theirs. Customer companies are not in this lookup yet.",
    4: "You can keep this result as a file. ",
  };
  const nextLabel = {
    1: "Next · Check the seal",
    2: "Next · Verifiable Sender Network (VSN)",
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

  const deskRoot = document.querySelector("[data-desks]");
  if (deskRoot) {
    const copy = {
      law: [
        "Law office",
        "When a settlement, retainer, or “updated wiring” email arrives, the person who got it opens the live check. No account. No install.",
        "If the seal does not match, they keep the record and call a number they already have. Watch belongs on the one office inbox that would send the money, not on every lawyer’s laptop. "
      ],
      title: [
        "Title / closing",
        "The irreversible step is the account number. Whoever received the email checks it on the website before anyone changes where money goes.",
        "Closing staff do not each install Signet7. Recipients use the live check. Watch, if you use it, sits on the one inbox that would wire funds. "
      ],
      build: [
        "Construction",
        "Draws, change orders, and sub pay-apps often look ordinary. That is the trap. The person who got the email opens the live check.",
        "Do not put Watch on every jobsite laptop. One company inbox that pays vendors is enough. Recipients never install. Keep writing in Outlook."
      ],
      pay: [
        "Payroll",
        "A “new direct deposit” that looks like staff still gets checked on the website. No employee app. No account for the recipient.",
        "If you Watch anything, Watch the inbox that would change bank details. Everyone else keeps their mail app.  "
      ],
      finance: [
        "Finance / AP",
        "Invoice plus new routing. The person who must pay opens the live check. They do not download Signet7 to do that.",
        "Watch the one AP inbox on one company PC if you want a quiet alarm when a seal is torn. Recipients still use the website. Stay in Outlook."
      ],
      bank: [
        "Bank / credit union ops",
        "Internal or vendor instructions that move accounts still get a last look on the live check. Staff do not install a new mail app.",
        "Watch is optional and still one inbox.  Signet7 is the check and the record you can produce later."
      ]
    };
    const title = document.querySelector("[data-desk-title]");
    const body = document.querySelector("[data-desk-body]");
    const more = document.querySelector("[data-desk-more]");
    deskRoot.addEventListener("click", (e) => {
      const btn = e.target.closest("[data-desk]");
      if (!btn) return;
      deskRoot.querySelectorAll("[data-desk]").forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
      const row = copy[btn.getAttribute("data-desk")];
      if (row && title) title.textContent = row[0];
      if (row && body) body.textContent = row[1];
      if (row && more) more.textContent = row[2];
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
          window.setTimeout(() => flapCard(card, feed[n]), n * 160);
        });
      }, 2800);
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

  const pitch = document.querySelector("[data-pitch]");
  if (pitch) {
    const acts = [...pitch.querySelectorAll("[data-pitch-act]")];
    const panels = [...pitch.querySelectorAll("[data-pitch-panel]")];
    const art = pitch.querySelector("[data-pitch-art]");
    const arts = [
      "assets/art/pitch-looks.jpg",
      "assets/art/pitch-trick.jpg",
      "assets/art/pitch-intact.jpg",
      "assets/art/pitch-caught.jpg",
      "assets/art/pitch-link.jpg",
      "assets/art/pitch-bill.jpg",
    ];
    const showPitch = (i) => {
      acts.forEach((btn, n) => btn.setAttribute("aria-selected", n === i ? "true" : "false"));
      panels.forEach((panel, n) => {
        panel.hidden = n !== i;
        panel.classList.toggle("is-on", n === i);
      });
      if (art && arts[i]) art.src = arts[i];
    };
    acts.forEach((btn, i) => btn.addEventListener("click", () => showPitch(i)));
    if (!reduce && acts.length) {
      let n = 0;
      window.setInterval(() => {
        if (pitch.matches(":hover") || pitch.matches(":focus-within")) return;
        n = (n + 1) % acts.length;
        showPitch(n);
      }, 4800);
    }
  }

  const canvas = document.getElementById("dust");
  if (true || !canvas || reduce || !canvas.getContext) return;
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
