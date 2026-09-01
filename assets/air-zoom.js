(() => {
  const pin = document.querySelector("[data-air-pin]");
  const world = document.querySelector("[data-air-world]");
  const copy = document.querySelector("[data-air-copy]");
  if (!pin || !world) return;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce) return;

  const paint = () => {
    const total = Math.max(1, pin.offsetHeight - window.innerHeight);
    const passed = Math.min(total, Math.max(0, -pin.getBoundingClientRect().top));
    const p = passed / total;
    const scale = 1 + p * 2.6;
    world.style.transform = "translate(-50%, -38%) scale(" + scale + ")";
    if (copy) copy.style.opacity = String(Math.max(0, 1 - p * 1.35));
  };

  paint();
  window.addEventListener("scroll", paint, { passive: true });
  window.addEventListener("resize", paint);
})();
