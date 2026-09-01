(() => {
  const pin = document.querySelector("[data-air-pin]");
  const world = document.querySelector("[data-air-land]");
  const copy = document.querySelector("[data-air-copy]");
  const check = document.querySelector("[data-air-check]");
  if (!pin || !world) return;
  const ar = 1920 / 1080;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const layout = () => {
    const vw = window.innerWidth;
    const vh = window.innerHeight;
    let w;
    let h;
    if (vw / vh > ar) {
      w = vw;
      h = vw / ar;
    } else {
      h = vh;
      w = vh * ar;
    }
    world.style.width = w + "px";
    world.style.height = h + "px";
    world.style.left = (vw - w) / 2 + "px";
    world.style.top = (vh - h) / 2 + "px";
  };

  const paint = () => {
    layout();
    if (reduce) {
      world.style.transform = "none";
      if (copy) copy.style.opacity = "1";
      if (check) check.classList.add("is-on");
      return;
    }
    const total = Math.max(1, pin.offsetHeight - window.innerHeight);
    const passed = Math.min(total, Math.max(0, -pin.getBoundingClientRect().top));
    const p = passed / total;
    world.style.transform = "scale(" + (1 + p * 2.85) + ")";
    if (copy) copy.style.opacity = String(Math.max(0, 1 - p * 1.55));
    if (check) {
      if (p > 0.38) check.classList.add("is-on");
      else check.classList.remove("is-on");
    }
  };

  paint();
  window.addEventListener("scroll", paint, { passive: true });
  window.addEventListener("resize", paint);
})();
