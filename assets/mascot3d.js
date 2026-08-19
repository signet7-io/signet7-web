(() => {
  const mount = document.getElementById("mascot3d");
  if (!mount || typeof THREE === "undefined") return;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setClearColor(0x000000, 0);
  mount.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(32, 1, 0.1, 40);
  camera.position.set(0, 0.35, 6.2);

  const key = new THREE.PointLight(0x58def8, 40, 20);
  key.position.set(3, 4, 5);
  const fill = new THREE.PointLight(0xff5a6a, 22, 18);
  fill.position.set(-3, 1, 4);
  const gold = new THREE.PointLight(0xffd16d, 16, 16);
  gold.position.set(0, -2, 3);
  scene.add(key, fill, gold, new THREE.AmbientLight(0x1a2430, 0.7));

  const hero = new THREE.Group();
  scene.add(hero);

  const sCurve = new THREE.CatmullRomCurve3([
    new THREE.Vector3(0.85, 1.55, 0),
    new THREE.Vector3(0.15, 1.72, 0),
    new THREE.Vector3(-0.85, 1.35, 0),
    new THREE.Vector3(-0.55, 0.85, 0),
    new THREE.Vector3(0.15, 0.55, 0),
    new THREE.Vector3(0.75, 0.15, 0),
    new THREE.Vector3(0.35, -0.45, 0),
    new THREE.Vector3(-0.75, -0.75, 0),
    new THREE.Vector3(-0.25, -1.35, 0),
    new THREE.Vector3(0.8, -1.45, 0)
  ]);
  const sGeo = new THREE.TubeGeometry(sCurve, 120, 0.28, 18, false);
  const sMat = new THREE.MeshStandardMaterial({
    color: 0x3ad7ea,
    emissive: 0x0a5c6c,
    metalness: 0.35,
    roughness: 0.28
  });
  const ess = new THREE.Mesh(sGeo, sMat);
  hero.add(ess);

  const eyeMat = new THREE.MeshStandardMaterial({ color: 0x0b1118, roughness: 0.4 });
  const eye = (x, y) => {
    const m = new THREE.Mesh(new THREE.SphereGeometry(0.09, 16, 16), eyeMat);
    m.position.set(x, y, 0.28);
    return m;
  };
  hero.add(eye(-0.15, 1.22), eye(0.18, 1.22));

  const sword = new THREE.Group();
  const sevenMat = new THREE.MeshStandardMaterial({
    color: 0xff3b4d,
    emissive: 0xaa1024,
    metalness: 0.2,
    roughness: 0.35
  });
  const bar = (w, h, d, x, y, z, rz) => {
    const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), sevenMat);
    m.position.set(x, y, z);
    if (rz) m.rotation.z = rz;
    sword.add(m);
  };
  bar(1.15, 0.16, 0.16, 0.05, 0.85, 0, -0.12);
  bar(0.16, 1.35, 0.16, 0.42, 0.12, 0, -0.42);
  const hilt = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.07, 0.35, 12), sevenMat);
  hilt.position.set(0.62, -0.62, 0);
  sword.add(hilt);
  sword.position.set(1.15, 0.15, 0.15);
  sword.rotation.z = -0.35;
  hero.add(sword);

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
    mx = ((e.clientX - r.left) / r.width - 0.5) * 0.6;
    my = ((e.clientY - r.top) / r.height - 0.5) * 0.3;
  }, { passive: true });
  mount.addEventListener("click", () => { slash = 1; });

  const tick = () => {
    const t = performance.now() * 0.001;
    if (!reduce) {
      hero.rotation.y = mx + Math.sin(t * 0.6) * 0.18;
      hero.rotation.x = -my + Math.sin(t * 0.9) * 0.04;
      hero.position.y = Math.sin(t * 1.2) * 0.06;
      if (slash > 0) {
        sword.rotation.z = -0.35 - Math.sin(slash * Math.PI) * 1.1;
        slash = Math.max(0, slash - 0.045);
      }
    }
    renderer.render(scene, camera);
    requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
})();
