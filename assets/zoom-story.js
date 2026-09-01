(() => {
  const pin = document.querySelector("[data-zoom-pin]");
  const scenes = [...document.querySelectorAll("[data-zoom-scene]")];
  if (!pin || scenes.length < 2) return;
  const n = scenes.length;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let current = 0;
  let running = false;

  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const smooth = (t) => t * t * (3 - 2 * t);

  const target = () => {
    const total = Math.max(1, pin.offsetHeight - window.innerHeight);
    const passed = clamp(-pin.getBoundingClientRect().top, 0, total);
    return passed / total;
  };

  const apply = (t) => {
    const x = t * (n - 1);
    const i = Math.min(n - 1, Math.floor(x + 1e-9));
    const u = clamp(x - i, 0, 1);
    const last = i === n - 1;
    const hold = 0.32;
    const z = last || u < hold ? 0 : smooth((u - hold) / (1 - hold));

    scenes.forEach((el, j) => {
      const copy = el.querySelector("[data-zoom-copy]");
      el.style.clipPath = "none";
      if (j < i) {
        el.style.opacity = "0";
        el.style.transform = "scale(1.28)";
        el.style.zIndex = "1";
        if (copy) copy.style.opacity = "0";
      } else if (j === i) {
        el.style.opacity = String(1 - z * 0.35);
        el.style.transform = "scale(" + (1 + z * 0.42) + ")";
        el.style.zIndex = "2";
        if (copy) copy.style.opacity = String(clamp(1 - z * 1.7, 0, 1));
      } else if (j === i + 1) {
        el.style.opacity = String(z);
        el.style.transform = "scale(" + (1.18 - z * 0.18) + ")";
        el.style.zIndex = "3";
        if (copy) copy.style.opacity = String(clamp((z - 0.42) / 0.58, 0, 1));
      } else {
        el.style.opacity = "0";
        el.style.transform = "scale(1.18)";
        el.style.zIndex = "0";
        if (copy) copy.style.opacity = "0";
      }
    });
  };

  const tick = () => {
    const goal = reduce ? 0 : target();
    current += (goal - current) * 0.14;
    if (Math.abs(goal - current) < 0.00035) {
      current = goal;
      running = false;
    } else {
      running = true;
      requestAnimationFrame(tick);
    }
    apply(current);
  };

  const kick = () => {
    if (!running) tick();
  };

  apply(0);
  window.addEventListener("scroll", kick, { passive: true });
  window.addEventListener("resize", kick);
})();
