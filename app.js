import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

/* ---------------- state ---------------- */
const state = {
  tiers: {},          // tier -> { enabled, glbs:[{file, tris, verts, files, loaded}] }
  groups: new Map(),  // glb file -> THREE.Group
  manager: null,
  wire: false,
  orbit: true,
  loadedBytes: 0,
};

const MANIFEST_URL = 'models/manifest.json';
const $ = (id) => document.getElementById(id);

/* ---------------- renderer ---------------- */
let renderer;
try {
  renderer = new THREE.WebGLRenderer({ canvas: $('view'), antialias: true, powerPreference: 'high-performance' });
} catch (e) {
  $('webgl-fail').classList.remove('hidden');
  $('loader').classList.add('done');
  throw e;
}
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.setSize(innerWidth, innerHeight);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.35;

const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x070b14, 0.00055);

const camera = new THREE.PerspectiveCamera(55, innerWidth / innerHeight, 1, 12000);
camera.position.set(650, 420, 760);

const controls = new OrbitControls(camera, renderer.domElement);
window.__v = { scene, camera, controls, state }; // debug hook
controls.enableDamping = true;
controls.dampingFactor = 0.06;
controls.maxPolarAngle = Math.PI * 0.55;
controls.minDistance = 40;
controls.maxDistance = 4000;
controls.autoRotate = state.orbit;
controls.autoRotateSpeed = 0.35;
controls.target.set(-60, 30, -180);

scene.add(new THREE.HemisphereLight(0x33415e, 0x0a0d16, 0.4));
const moon = new THREE.DirectionalLight(0xbfd4ff, 0.45);
moon.position.set(-600, 900, 400);
scene.add(moon);

/* authentic in-game night panorama as sky */
new THREE.TextureLoader().load('skybox.jpg', (t) => {
  t.mapping = THREE.EquirectangularReflectionMapping;
  t.colorSpace = THREE.SRGBColorSpace;
  scene.background = t;
  scene.backgroundIntensity = 0.25;
  scene.backgroundBlurriness = 0.5;
});

addEventListener('resize', () => {
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
});

/* ---------------- texture cache ---------------- */
const texLoader = new THREE.TextureLoader();
const texCache = new Map(); // name -> Promise<Texture|null>
function getTex(name) {
  if (!texCache.has(name)) {
    texCache.set(name, new Promise((res) => {
      texLoader.load(`models/tex/${name}.jpg`,
        (t) => { t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; res(t); },
        undefined, () => res(null));
    }));
  }
  return texCache.get(name);
}

/* ---------------- GLB loading ---------------- */
const gltfLoader = new GLTFLoader();

async function loadGLB(entry, tierName) {
  const gltf = await new Promise((res, rej) => gltfLoader.load(entry.file, res, undefined, rej));
  const root = gltf.scene;
  const group = new THREE.Group();
  group.name = entry.file;
  group.visible = state.tiers[tierName].enabled;

  // v2 exporter: every PRIMITIVE carries a material NAMED after its texture
  // ('__dark' when untextured). GLTFLoader preserves material names, so we map
  // material.name -> models/tex/<name>.jpg directly. No order/name matching of
  // nodes needed any more.
  root.traverse((obj) => {
    if (!obj.isMesh) return;
    const texName = obj.material?.name && obj.material.name !== '__dark'
      ? obj.material.name : null;
    const texPromise = texName ? getTex(texName) : Promise.resolve(null);
    obj.material = new THREE.MeshLambertMaterial({ color: 0x101623, side: THREE.DoubleSide });
    texPromise.then((tex) => {
      obj.material = tex
        ? new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide })
        : new THREE.MeshLambertMaterial({ color: new THREE.Color().setHSL(0.6, 0.3, 0.10), side: THREE.DoubleSide });
      obj.material.wireframe = state.wire;
    });
  });
  group.add(root);
  group.userData = { tier: tierName, tris: entry.tris, verts: entry.verts };
  scene.add(group);
  state.groups.set(entry.file, group);
  entry.loaded = true;
  addBrowserRow(entry, tierName);
  return group;
}

/* ---------------- UI: tier buttons ---------------- */
const TIER_LABEL = { hero: 'Skyline', fp: 'Footprints', low: 'Low-detail LOD', district: 'District props' };
const TIER_ORDER = ['hero', 'fp', 'district', 'low'];

function buildTierButtons() {
  const nav = $('tiers');
  for (const tier of TIER_ORDER) {
    const list = state.tiers[tier]?.glbs || [];
    if (!list.length) continue;
    const tris = list.reduce((a, g) => a + g.tris, 0);
    const b = document.createElement('button');
    b.className = 'tier-btn' + (state.tiers[tier].enabled ? '' : ' off');
    b.innerHTML = `<span class="dot"></span>${TIER_LABEL[tier] || tier}
      <span class="meta">${list.length} glb · ${(tris / 1000).toFixed(0)}k tris</span>`;
    b.onclick = () => toggleTier(tier, b);
    b.dataset.tier = tier;
    nav.appendChild(b);
  }
}

async function toggleTier(tier, btn) {
  const t = state.tiers[tier];
  t.enabled = !t.enabled;
  btn.classList.toggle('off', !t.enabled);
  if (t.enabled && !t.loaded) {
    t.loaded = true;
    setStatus(`loading ${TIER_LABEL[tier]?.toLowerCase() || tier}…`);
    for (const entry of t.glbs) {
      if (!entry.loaded) await loadGLB(entry, tier);
    }
    clearStatus();
    updateHUDTotals();
  }
  for (const entry of t.glbs) {
    const g = state.groups.get(entry.file);
    if (g) g.visible = t.enabled;
    syncRow(entry.file, t.enabled);
  }
}

/* ---------------- UI: mesh browser ---------------- */
const rowMap = new Map(); // glb file -> row element
function addBrowserRow(entry, tier) {
  const row = document.createElement('label');
  row.className = 'mesh-row';
  row.dataset.file = entry.file;
  row.dataset.name = entry.file.toLowerCase();
  const on = state.tiers[tier].enabled;
  row.innerHTML = `<input type="checkbox" ${on ? 'checked' : ''}>
    <span class="nm" title="${entry.file}">${entry.file.replace('models/', '')}</span>
    <span class="tc">${(entry.tris / 1000).toFixed(1)}k</span>`;
  row.querySelector('input').onchange = (ev) => {
    const g = state.groups.get(entry.file);
    if (g) g.visible = ev.target.checked;
  };
  $('browser-list').appendChild(row);
  rowMap.set(entry.file, row);
}
function syncRow(file, on) {
  const row = rowMap.get(file);
  if (row) row.querySelector('input').checked = on;
}
$('search').addEventListener('input', (e) => {
  const q = e.target.value.toLowerCase();
  for (const row of rowMap.values()) {
    row.classList.toggle('dimmed', q && !row.dataset.name.includes(q));
  }
});
$('btn-browser').onclick = () => $('browser').classList.toggle('hidden');
$('close-browser').onclick = () => $('browser').classList.add('hidden');

/* ---------------- toolbar ---------------- */
$('btn-wire').onclick = () => {
  state.wire = !state.wire;
  $('btn-wire').classList.toggle('on', state.wire);
  for (const g of state.groups.values()) {
    g.traverse((o) => { if (o.isMesh) o.material.wireframe = state.wire; });
  }
};
$('btn-orbit').onclick = () => {
  state.orbit = !state.orbit;
  controls.autoRotate = state.orbit;
  $('btn-orbit').classList.toggle('on', state.orbit);
};
$('btn-reset').onclick = fitCamera;

function fitCamera() {
  const box = new THREE.Box3();
  let any = false;
  for (const g of state.groups.values()) {
    if (g.visible) { box.expandByObject(g); any = true; }
  }
  if (!any) return;
  const c = box.getCenter(new THREE.Vector3());
  const r = box.getSize(new THREE.Vector3()).length() * 0.5;
  camera.position.set(c.x + r * 1.05, c.y + r * 0.62, c.z + r * 1.05);
  controls.target.copy(c);
  controls.maxDistance = r * 6;
}

/* batarang easter egg */
let batarang = null;
const batBtn = document.createElement('button');
batBtn.className = 'tier-btn off';
batBtn.innerHTML = `<span class="dot" style="background:var(--gold);box-shadow:0 0 8px var(--gold)"></span>Batarang
  <span class="meta">easter egg</span>`;
batBtn.onclick = async () => {
  batBtn.classList.toggle('off');
  if (!batarang) {
    const gltf = await new Promise((res, rej) => gltfLoader.load('models/batarang.glb', res, undefined, rej));
    batarang = gltf.scene;
    batarang.scale.setScalar(150);
    batarang.position.set(-60, 190, -180);
    batarang.traverse((o) => {
      if (o.isMesh) {
        const m = o.material;
        o.material = new THREE.MeshBasicMaterial({ map: m.map || null, color: m.map ? 0xffffff : 0x9fb4d8, side: THREE.DoubleSide });
      }
    });
    scene.add(batarang);
  }
  batarang.visible = batBtn.classList.contains('off') === false;
};
$('tiers').appendChild(batBtn);

/* ---------------- loader overlay ---------------- */
function setStatus(s) { $('load-status').textContent = s; }
function clearStatus() { $('load-status').textContent = ''; }

/* ---------------- boot ---------------- */
(async function boot() {
  let manifest;
  try {
    manifest = await (await fetch(MANIFEST_URL)).json();
  } catch (e) {
    setStatus('failed to load manifest.json — is this served over HTTP?');
    return;
  }
  state.tiers = {};
  for (const g of manifest.glbs) {
    const tier = g.tier || 'district';
    (state.tiers[tier] ??= { enabled: false, glbs: [], loaded: false }).glbs.push(g);
  }
  state.tiers.hero.enabled = true;
  buildTierButtons();

  const heroGlbs = state.tiers.hero.glbs;
  let done = 0;
  setStatus(`assembling skyline · 0/${heroGlbs.length}`);
  for (const entry of heroGlbs) {
    await loadGLB(entry, 'hero');
    done++;
    $('load-bar').style.width = `${(done / heroGlbs.length) * 100}%`;
    setStatus(`assembling skyline · ${done}/${heroGlbs.length}`);
  }
  state.tiers.hero.loaded = true;
  fitCamera();
  updateHUDTotals();
  $('loader').classList.add('done');
  clearStatus();
})();

/* ---------------- HUD + render loop ---------------- */
let frames = 0, tPrev = performance.now();
function updateHUDTotals() {
  let v = 0, t = 0;
  for (const g of state.groups.values()) {
    if (g.visible) { v += g.userData.verts; t += g.userData.tris; }
  }
  $('st-verts').textContent = v >= 1000 ? `${(v / 1000).toFixed(0)}k` : v;
  $('st-tris').textContent = t >= 1000 ? `${(t / 1000).toFixed(0)}k` : t;
}

const batarangPrev = { rotate: 0 };
function animate(t) {
  requestAnimationFrame(animate);
  controls.update();
  if (batarang?.visible) {
    batarang.rotation.y += 0.02;
    batarang.rotation.x = Math.sin(t * 0.0006) * 0.35;
    batarang.position.y = 190 + Math.sin(t * 0.0009) * 12;
  }
  renderer.render(scene, camera);
  frames++;
  if (t - tPrev >= 500) {
    $('st-fps').textContent = Math.round(frames * 1000 / (t - tPrev));
    $('st-calls').textContent = renderer.info.render.calls;
    frames = 0;
    tPrev = t;
    updateHUDTotals();
  }
}
requestAnimationFrame(animate);
