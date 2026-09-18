(() => {
  const canvas = document.getElementById("cad-film");
  const pin = document.getElementById("film-pin");
  const chapters = [...document.querySelectorAll("[data-chapter]")];
  if (!canvas || !pin || typeof THREE === "undefined") return;

  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce) {
    document.documentElement.classList.add("no-film");
    return;
  }
  document.documentElement.classList.add("has-film");

  const CYAN = 0x47b1dc;
  const BRIGHT = 0x5cb9e9;
  const NAVY = 0x010d1d;
  const W = 2.1;
  const H = 1.48;
  const T = 0.05;
  const THICK = 0.028;
  const THICK2 = 0.018;

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(NAVY);
  scene.fog = new THREE.Fog(NAVY, 6, 16);

  const camera = new THREE.PerspectiveCamera(32, 1, 0.05, 40);
  const renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: true,
    alpha: false,
    powerPreference: "high-performance"
  });
  renderer.setClearColor(NAVY, 1);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

  const mat = new THREE.MeshBasicMaterial({ color: BRIGHT });
  const matDim = new THREE.MeshBasicMaterial({ color: CYAN });
  const matSoft = new THREE.MeshBasicMaterial({ color: CYAN, transparent: true, opacity: 0.55 });

  function fat(a, b, thick, material) {
    const dir = new THREE.Vector3().subVectors(b, a);
    const len = dir.length();
    if (len < 1e-6) return null;
    const mesh = new THREE.Mesh(new THREE.BoxGeometry(thick, thick, len), material);
    mesh.position.copy(a).add(b).multiplyScalar(0.5);
    mesh.lookAt(b);
    return mesh;
  }

  function rectLoop(x, y, z, w, h, thick, material, group) {
    const hw = w / 2;
    const hh = h / 2;
    const pts = [
      [new THREE.Vector3(x - hw, y + hh, z), new THREE.Vector3(x + hw, y + hh, z)],
      [new THREE.Vector3(x + hw, y + hh, z), new THREE.Vector3(x + hw, y - hh, z)],
      [new THREE.Vector3(x + hw, y - hh, z), new THREE.Vector3(x - hw, y - hh, z)],
      [new THREE.Vector3(x - hw, y - hh, z), new THREE.Vector3(x - hw, y + hh, z)]
    ];
    pts.forEach(([a, b]) => {
      const m = fat(a, b, thick, material);
      if (m) group.add(m);
    });
  }

  const sheet = new THREE.Group();
  scene.add(sheet);

  const grid = new THREE.Group();
  for (let i = -8; i <= 8; i += 1) {
    grid.add(fat(new THREE.Vector3(-6, -1.35, i * 0.45), new THREE.Vector3(6, -1.35, i * 0.45), 0.008, matSoft));
    grid.add(fat(new THREE.Vector3(i * 0.45, -1.35, -6), new THREE.Vector3(i * 0.45, -1.35, 6), 0.008, matSoft));
  }
  sheet.add(grid);

  const frame = new THREE.Group();
  rectLoop(0, 0.2, 0, 5.6, 3.4, 0.022, matDim, frame);
  rectLoop(0, 0.2, 0, 5.35, 3.15, 0.014, matSoft, frame);
  sheet.add(frame);

  const body = new THREE.Group();
  rectLoop(0, 0.15, 0, W, H, THICK, mat, body);
  body.add(fat(new THREE.Vector3(-W / 2, 0.15 + H / 2, 0), new THREE.Vector3(0, 0.05, 0), THICK2, matDim));
  body.add(fat(new THREE.Vector3(W / 2, 0.15 + H / 2, 0), new THREE.Vector3(0, 0.05, 0), THICK2, matDim));
  body.add(fat(new THREE.Vector3(-W / 2, 0.15 - H / 2, 0), new THREE.Vector3(-0.35, 0.02, 0), THICK2, matSoft));
  body.add(fat(new THREE.Vector3(W / 2, 0.15 - H / 2, 0), new THREE.Vector3(0.35, 0.02, 0), THICK2, matSoft));
  sheet.add(body);

  const flap = new THREE.Group();
  flap.position.set(0, 0.15 + H / 2, 0);
  const flapDraw = new THREE.Group();
  flapDraw.add(fat(new THREE.Vector3(-W / 2, 0, 0), new THREE.Vector3(0, -H * 0.52, 0), THICK, mat));
  flapDraw.add(fat(new THREE.Vector3(W / 2, 0, 0), new THREE.Vector3(0, -H * 0.52, 0), THICK, mat));
  flapDraw.add(fat(new THREE.Vector3(-W / 2, 0, 0), new THREE.Vector3(W / 2, 0, 0), THICK, mat));
  flap.add(flapDraw);
  sheet.add(flap);

  const lock = new THREE.Group();
  const shackle = new THREE.Mesh(new THREE.TorusGeometry(0.09, 0.018, 8, 20, Math.PI), mat);
  shackle.rotation.z = Math.PI;
  shackle.position.y = 0.09;
  lock.add(shackle);
  const box = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.14, 0.05), mat);
  lock.add(box);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(0.22, 0.012, 8, 32), matDim);
  lock.add(ring);
  lock.position.set(0, 0.12, 0.04);
  sheet.add(lock);

  const dims = new THREE.Group();
  dims.add(fat(new THREE.Vector3(-W / 2, 0.15 + H / 2 + 0.22, 0), new THREE.Vector3(W / 2, 0.15 + H / 2 + 0.22, 0), 0.016, matDim));
  dims.add(fat(new THREE.Vector3(W / 2 + 0.22, 0.15 - H / 2, 0), new THREE.Vector3(W / 2 + 0.22, 0.15 + H / 2, 0), 0.016, matDim));
  sheet.add(dims);

  function label(text, x, y, z) {
    const c = document.createElement("canvas");
    c.width = 256;
    c.height = 64;
    const g = c.getContext("2d");
    g.clearRect(0, 0, 256, 64);
    g.fillStyle = "#5cb9e9";
    g.font = "600 32px Consolas, monospace";
    g.textAlign = "center";
    g.textBaseline = "middle";
    g.fillText(text, 128, 32);
    const tex = new THREE.CanvasTexture(c);
    const m = new THREE.MeshBasicMaterial({ map: tex, transparent: true });
    const quad = new THREE.Mesh(new THREE.PlaneGeometry(0.55, 0.14), m);
    quad.position.set(x, y, z);
    return quad;
  }
  dims.add(label("210.0", 0, 0.15 + H / 2 + 0.34, 0.02));
  dims.add(label("148.0", W / 2 + 0.48, 0.15, 0.02));
  dims.add(label("SEAL", 0.55, 0.28, 0.06));

  scene.add(new THREE.AmbientLight(0x7ec4e4, 0.35));

  const camFrom = new THREE.Vector3(0.15, 1.55, 4.6);
  const camTo = new THREE.Vector3(0.55, 0.85, 2.55);
  const look = new THREE.Vector3(0, 0.2, 0);

  function clamp(v, a, b) {
    return Math.max(a, Math.min(b, v));
  }
  function progress() {
    const total = pin.offsetHeight - window.innerHeight;
    if (total <= 1) return 0;
    return clamp(-pin.getBoundingClientRect().top / total, 0, 1);
  }

  function apply(p) {
    const flapT = clamp((p - 0.12) / 0.28, 0, 1);
    const explode = clamp((p - 0.38) / 0.32, 0, 1);
    flap.rotation.x = 1.15 * flapT;
    body.position.z = -0.18 * explode;
    lock.position.z = 0.04 + 0.55 * explode;
    lock.position.y = 0.12 + 0.35 * explode;
    camera.position.lerpVectors(camFrom, camTo, p);
    camera.lookAt(look);
    const idx = Math.min(chapters.length - 1, Math.floor(p * chapters.length * 0.999));
    chapters.forEach((el, i) => el.classList.toggle("is-on", i === idx));
  }

  function resize() {
    const w = canvas.clientWidth || pin.clientWidth;
    const h = canvas.clientHeight || window.innerHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / Math.max(h, 1);
    camera.updateProjectionMatrix();
  }

  let ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      apply(progress());
      ticking = false;
    });
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", () => {
    resize();
    apply(progress());
  });
  resize();
  apply(0);

  function loop() {
    renderer.render(scene, camera);
    requestAnimationFrame(loop);
  }
  loop();
})();
