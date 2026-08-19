(() => {
  const mount = document.getElementById("mascot3d");
  if (!mount || typeof THREE === "undefined") return;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setClearColor(0x000000, 0);
  mount.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(28, 1, 0.1, 40);
  camera.position.set(0, 0, 4.2);
  scene.add(new THREE.AmbientLight(0xffffff, 1.15));

  const card = new THREE.Group();
  scene.add(card);

  const loader = new THREE.TextureLoader();
  loader.load("assets/mascot-s7-fill.png?v=pet", (tex) => {
    tex.colorSpace = THREE.SRGBColorSpace;
    const aspect = (tex.image && tex.image.width && tex.image.height)
      ? tex.image.width / tex.image.height
      : 16 / 9;
    const h = 2.35;
    const w = h * aspect;
    const mat = new THREE.MeshBasicMaterial({ map: tex, transparent: true });
    const mesh = new THREE.Mesh(new THREE.PlaneGeometry(w, h), mat);
    card.add(mesh);
  });

  const resize = () => {
    const w = mount.clientWidth || 1;
    const h = mount.clientHeight || 1;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  };
  resize();
  window.addEventListener("resize", resize, { passive: true });

  let mx = 0;
  let my = 0;
  let slash = 0;
  mount.addEventListener("pointermove", (e) => {
    const r = mount.getBoundingClientRect();
    mx = ((e.clientX - r.left) / r.width - 0.5) * 0.8;
    my = ((e.clientY - r.top) / r.height - 0.5) * 0.35;
  }, { passive: true });
  mount.addEventListener("click", () => { slash = 1; });

  const tick = () => {
    const t = performance.now() * 0.001;
    if (!reduce) {
      card.rotation.y = mx + Math.sin(t * 0.7) * 0.12;
      card.rotation.x = -my;
      card.position.y = Math.sin(t * 1.1) * 0.05;
      if (slash > 0) {
        card.rotation.z = Math.sin(slash * Math.PI) * 0.35;
        slash = Math.max(0, slash - 0.05);
      } else {
        card.rotation.z = 0;
      }
    }
    renderer.render(scene, camera);
    requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
})();
