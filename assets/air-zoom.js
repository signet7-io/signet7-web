(() => {
  const pin = document.querySelector("[data-air-pin]");
  const land = document.querySelector("[data-air-land]");
  const copy = document.querySelector("[data-air-copy]");
  const check = document.querySelector("[data-air-check]");
  if (!pin || !land) return;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce) {
    land.style.transform = "none";
    if (copy) copy.style.opacity = "1";
    if (check) check.classList.add("is-on");
    return;
  }

  const paint = () => {
    const total = Math.max(1, pin.offsetHeight - window.innerHeight);
    const passed = Math.min(total, Math.max(0, -pin.getBoundingClientRect().top));
    const p = passed / total;
    land.style.transform = "scale(" + (1 + p * 1.9) + ")";
    if (copy) copy.style.opacity = String(Math.max(0, 1 - p * 1.5));
    if (check) {
      if (p > 0.42) check.classList.add("is-on");
      else check.classList.remove("is-on");
    }
  };

  paint();
  window.addEventListener("scroll", paint, { passive: true });
  window.addEventListener("resize", paint);
})();
