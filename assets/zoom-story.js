(() => {
  const pin = document.querySelector("[data-zoom-pin]");
  const scenes = [...document.querySelectorAll("[data-zoom-scene]")];
  if (!pin || scenes.length < 2) return;
  const n = scenes.length;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const paint = () => {
    const total = Math.max(1, pin.offsetHeight - window.innerHeight);
    const passed = Math.min(total, Math.max(0, -pin.getBoundingClientRect().top));
    const t = reduce ? 0 : passed / total;
    const x = t * (n - 1);
    const i = Math.min(n - 1, Math.floor(x + 1e-9));
    const u = Math.min(1, x - i);
    const last = i === n - 1;
    const hold = 0.24;
    const z = last || u < hold ? 0 : (u - hold) / (1 - hold);

    scenes.forEach((el, j) => {
      const copy = el.querySelector("[data-zoom-copy]");
      if (j < i) {
        el.style.opacity = "0";
        el.style.transform = "scale(2.05)";
        el.style.clipPath = "none";
        el.style.zIndex = "1";
        if (copy) copy.style.opacity = "0";
      } else if (j === i) {
        el.style.opacity = "1";
        el.style.transform = "scale(" + (1 + z * 1.7) + ")";
        el.style.clipPath = "none";
        el.style.zIndex = "2";
        if (copy) copy.style.opacity = String(Math.max(0, 1 - z * 1.45));
      } else if (j === i + 1) {
        const r = Math.max(0, z * 82);
        el.style.opacity = z > 0.03 ? "1" : "0";
        el.style.transform = "scale(1)";
        el.style.clipPath = "circle(" + r + "% at 50% 52%)";
        el.style.zIndex = "4";
        if (copy) copy.style.opacity = String(Math.max(0, (z - 0.58) * 2.6));
      } else {
        el.style.opacity = "0";
        el.style.transform = "scale(1)";
        el.style.clipPath = "circle(0% at 50% 52%)";
        el.style.zIndex = "0";
        if (copy) copy.style.opacity = "0";
      }
    });
  };

  paint();
  window.addEventListener("scroll", paint, { passive: true });
  window.addEventListener("resize", paint);
})();
