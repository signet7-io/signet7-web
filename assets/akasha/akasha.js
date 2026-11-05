(function () {
  var canvas = document.getElementById("petals");
  var oldHash = window.location.hash.replace(/^#/, "");
  var oldRoutes = {
    "/product": "/product.html",
    "/programs": "/programs.html",
    "/about": "/about.html",
    "/scenarios": "/scenarios.html",
    "/security": "/security.html",
    "/faq": "/faq.html",
    "/privacy": "/privacy.html",
    "/contact": "/contact.html"
  };
  if (oldRoutes[oldHash]) window.location.replace(oldRoutes[oldHash]);
  var menu = document.querySelector(".menu");
  var sheet = document.getElementById("site-menu");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var ctx = canvas.getContext("2d", { alpha: true });
  var sprites = [];
  var flakes = [];
  var running = false;
  var last = 0;
  var width = 0;
  var height = 0;
  var dpr = 1;
  var quiet = null;

  function load(src) {
    return new Promise(function (resolve, reject) {
      var img = new Image();
      img.onload = function () {
        resolve(img);
      };
      img.onerror = reject;
      img.src = src;
    });
  }

  function count() {
    var base = width < 760 ? 46 : 110;
    return reduce ? Math.round(base * 0.4) : base;
  }

  function make(existing) {
    var depth = 0.22 + Math.random() * 0.78;
    var kindRoll = Math.random();
    var kind = kindRoll > 0.88 ? 2 : kindRoll > 0.55 ? 1 : 0;
    var size = (kind === 2 ? 34 : 16) + depth * (kind === 2 ? 64 : 44);
    var flake = existing || {};
    flake.kind = kind;
    flake.depth = depth;
    flake.size = size;
    flake.spin = (Math.random() - 0.5) * (0.3 + depth * 0.4);
    flake.phase = Math.random() * Math.PI * 2;
    flake.flip = Math.random() < 0.5 ? -1 : 1;
    flake.sway = 12 + Math.random() * 20;
    flake.vy = 18 + depth * 46;
    flake.x = Math.random() * Math.max(width, 1);
    flake.y = existing ? -size - Math.random() * 180 : Math.random() * (height + size) - size;
    flake.rot = Math.random() * Math.PI * 2;
    return flake;
  }

  function readQuiet() {
    var el = document.querySelector(".hero-copy");
    if (!el) return;
    var r = el.getBoundingClientRect();
    quiet = { l: r.left - 24, t: r.top - 16, r: r.right + 48, b: r.bottom + 20 };
  }

  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = Math.round(width * dpr);
    canvas.height = Math.round(height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    var next = count();
    while (flakes.length < next) flakes.push(make());
    if (flakes.length > next) flakes.length = next;
    readQuiet();
  }

  function draw(now) {
    var dt = Math.min(0.033, (now - last) / 1000 || 0.016);
    last = now;
    ctx.clearRect(0, 0, width, height);
    var i;
    for (i = 0; i < flakes.length; i += 1) {
      var f = flakes[i];
      if (!reduce) {
        f.y += f.vy * dt;
        f.x += Math.sin(now * 0.0005 + f.phase) * f.sway * dt;
        f.rot += f.spin * dt;
        if (f.y > height + f.size) {
          f.y = -f.size - Math.random() * 160;
          f.x = Math.random() * width;
        }
      }
      var img = sprites[f.kind];
      if (!img) continue;
      var fade = 1;
      if (quiet && f.x > quiet.l && f.x < quiet.r && f.y > quiet.t && f.y < quiet.b) fade = 0.12;
      ctx.save();
      ctx.translate(f.x, f.y);
      ctx.rotate(f.rot);
      ctx.scale(f.flip, 1);
      ctx.globalAlpha = (0.34 + f.depth * 0.62) * fade;
      ctx.drawImage(img, -f.size / 2, -f.size / 2, f.size, f.size * (img.height / img.width));
      ctx.restore();
    }
    if (running) requestAnimationFrame(draw);
  }

  function paintOnce() {
    last = performance.now();
    draw(last);
  }

  menu.addEventListener("click", function () {
    var open = sheet.hasAttribute("hidden");
    if (open) sheet.removeAttribute("hidden");
    else sheet.setAttribute("hidden", "");
    menu.setAttribute("aria-expanded", open ? "true" : "false");
    menu.textContent = open ? "Close" : "Menu";
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && !sheet.hasAttribute("hidden")) {
      sheet.setAttribute("hidden", "");
      menu.setAttribute("aria-expanded", "false");
      menu.textContent = "Menu";
      menu.focus();
    }
  });

  window.addEventListener("resize", function () {
    resize();
    if (!running) paintOnce();
  });

  document.addEventListener("visibilitychange", function () {
    if (reduce) return;
    if (document.hidden) {
      running = false;
    } else if (!running) {
      running = true;
      last = performance.now();
      requestAnimationFrame(draw);
    }
  });

  Promise.all([
    load("/assets/akasha/petal-pale.png"),
    load("/assets/akasha/petal-rose.png"),
    load("/assets/akasha/blossom.png"),
  ]).then(function (imgs) {
    sprites = imgs;
    resize();
    document.body.setAttribute("data-petals", "ready");
    if (reduce) {
      paintOnce();
      return;
    }
    running = true;
    last = performance.now();
    requestAnimationFrame(draw);
  });
})();
