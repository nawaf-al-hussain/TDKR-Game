import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';

/* ============================================================================
   v6 RENDERER — exact port of the game's LightmapVCBlendDC TEXTURE_FOG chain
   + CCFS ColorCorrection grade (LUT decoded from commons_tex.gla).

   Everything below is RECOVERED DATA, not tuning:

   · GothamCity.lvc.bin 'DICT' container (big-endian, CMemoryStream::BeginRead
     @0x3ae97c) -> CTemplateLevelProperties 0x2657 ->
     CComponentBaseGlobalIllum::Load @0x212000, field-for-field:

       fogColor RGBA = (64, 102, 119, 160)      -> glitch global param FogColor
       fogStart/fogEnd = 0.0 / 140.0            -> FogStartEnd = (s*start, 1/(s*(end-start)))
       fog texture   = "gc_verticalfog.tga"      (CLAMP-wrapped, decoded from
                                                  l_gothamcity_tex, ETC2 RGB)
       FogMap vec4   = (-1210, -220, 1/1520, -1/1130)  world-space projection
       VerticalFogHeight = 0.013,  VerticalFogAlpha = 0.65

   · Shipped GLSL (effects/LightmapVCBlendDC-v/-f.glsl + glsl.config.bin):

       FogFactor   = (-viewZ - FogStartEnd.x) * FogStartEnd.y;
       fY          = worldZ * VerticalFogHeight + FogFactor * FOG_DECAY;  // FOG_DECAY 0.5
       FogUV       = ((World*Position).xy - FogMap.xy) * FogMap.zw;
       FogMapColor = vec4(texture2D(FogTexture, FogUV).rgb, VerticalFogAlpha);
       fogCol2     = mix(FogMapColor, FogColor, clamp(fY, 0, 1));
       Color       = mix(Color, fogCol2, clamp(FogFactor, 0, 1) * fogCol2.a);

   The fog texture is a top-down atlas of Gotham's district glow — distant
   geometry melts into THAT (city-lit haze), which is the TDKR night look.

   Game world is Z-up; viewer is Y-up (export maps game(x,y,z)->view(x,z,-y)),
   so in-shader: gameY = -world.z, height = world.y.

   City bakes bind LightMap = UNBOUND (0xFFFFFFFF) -> engine supplies white ->
   Color = bake * 2.0.  Bakes are authored dark (mean ~0.11) for exactly this.
   The 2012 GLES2 pipeline did ALL of this in gamma space (no sRGB decode), so
   we sample textures raw (NoColorSpace) and write gl_FragColor raw.

   Material names from the v4 exporter carry the shading mode:
       '<tex>|2x'  LightMapDC  -> uMult = 2.0
       '<tex>|d'   StandardDiffuseDC etc -> uMult = 1.0
       '__dark'    untextured
   ========================================================================== */

/* ------- engine constants — extracted, with pinned runtime scale --------- */
// v6: fog scale pinned via DeviceOptions::Singleton (GOT 0xc07f18 -> BSS
// 0xc22ce4; C2 ctor default 1.0f @0x4a91f0; DeviceOptions::LoadOptions key
// "Fog distance factor" -> +0x1c). Shipped GPU_5.xml (top profile) = 1.1.
// SetFogDistance: start' = start*s, end' = end*s -> FogStartEnd=(0, 1/154).
const FOG = {
  start: 0.0,                    // GI +0x0c  (fogStart)
  end: 154.0,                    // GI +0x10 140.0 x GPU_5 "Fog distance factor" 1.1
  color: [64 / 255, 102 / 255, 119 / 255],  // GI +0x14 RGBA(64,102,119,160)
  colorA: 160 / 255,
  vfogHeight: 0.013,             // GI +0x58 -> global param (VerticalFogHeight)
  vfogAlpha: 0.65,               // GI +0x54 -> global param (VerticalFogAlpha)
  fogDecay: 0.5,                 // glsl.config.bin #define FOG_DECAY 0.5
  map: [-1210, -220, 1 / 1520, -1 / 1130],   // GI +0x40..+0x4c world projection
  mapTex: 'models/tex/GC_VerticalFOG.png',
};
FOG.scale = 1 / (FOG.end - FOG.start);

/* ---- ColorGrading LUT (game's ColorCorrection post effect) -------------- */
// Lua bootstrap: PostProcessingEffectAdd("ColorCorrection",
//   {extra_texture="000_default.tga", time_to_fade_in=0})
// LUT texture decoded from commons_tex.gla: 000_default.tga = PVR v1 wrapper
// {h=16,w=512,mips=0,fmt=19(RGB565),bpp=16} -> 512x16 atlas, 16^3 LUT.
// Shipped fragment shader CCFS.glsl (effects.gla), verbatim math:
//   r = color.r * cellsize;  b = floor(color.b*31.9999) * cellsize;
//   u = r * 0.9375 + 0.03125*cellsize + b;   v = color.g;
// (the 512x16 atlas stores 32 blue slices x 16 green rows; u,v are
//  normalized so CCFS works on it directly at half resolution)
const LUT = {
  tex: 'models/tex/LUT_000_default.png',
  cells: 32.0,
};

/* ---------------- state ---------------- */
const state = {
  tiers: {},
  groups: new Map(),
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
// gamma-space engine parity: no tonemap, raw output from our shader
renderer.toneMapping = THREE.NoToneMapping;

const scene = new THREE.Scene();
scene.fog = new THREE.Fog(
  new THREE.Color(...FOG.color), FOG.start, FOG.end); // exact GI fog, fallback mats

/* ---- ColorCorrection post pass (CCFS.glsl port, NEAREST like the game) -- */
const lutShader = {
  uniforms: {
    tDiffuse:   { value: null },
    uLUT:       { value: null },
    uCells:     { value: LUT.cells },
    uLutOn:     { value: 0.0 },   // flips to 1 once the LUT texture is loaded
  },
  vertexShader: /* glsl */`
    varying vec2 vUv;
    void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
  fragmentShader: /* glsl */`
    precision mediump float;
    uniform sampler2D tDiffuse;
    uniform sampler2D uLUT;
    uniform float uCells;
    uniform float uLutOn;
    varying vec2 vUv;
    void main() {
      vec4 color = texture2D(tDiffuse, vUv);
      // CCFS.glsl (verbatim constants from effects.gla)
      float cellsize = 1.0 / uCells;
      float r = color.r * cellsize;
      float b = floor(color.b * (uCells - 0.0001)) * cellsize;
      float u = r * 0.9375 + 0.03125 * cellsize + b;
      float v = color.g;
      vec4 graded = texture2D(uLUT, vec2(u, v));
      gl_FragColor = mix(color, vec4(graded.rgb, color.a), uLutOn);
    }`,
};
const lutPass = new ShaderPass(lutShader);
lutPass.renderToScreen = true;
new THREE.TextureLoader().load(LUT.tex, (t) => {
  t.flipY = false;                      // PVR top-first rows
  t.magFilter = THREE.NearestFilter;    // game binds NEAREST for ColorGradingSampler
  t.minFilter = THREE.NearestFilter;
  t.wrapS = t.wrapT = THREE.ClampToEdgeWrapping;
  t.colorSpace = THREE.NoColorSpace;    // gamma-space pipeline parity
  // NOTE: ShaderPass clones the shader uniforms -> mutate lutPass.uniforms
  lutPass.uniforms.uLUT.value = t;
  lutPass.uniforms.uLutOn.value = 1.0;
});

/* the game's world-projected fog/glow map (gc_verticalfog.tga, ETC2-decoded) */
const fogTexLoader = new THREE.TextureLoader();
fogTexLoader.load(FOG.mapTex, (t) => {
  t.flipY = false;                                  // PVR-style top-first upload
  t.wrapS = t.wrapT = THREE.ClampToEdgeWrapping;    // setWrap(0..2, CLAMPE) in native
  t.colorSpace = THREE.NoColorSpace;                // gamma-space pipeline
  fogUniforms.uFogTex.value = t;
});

const camera = new THREE.PerspectiveCamera(55, innerWidth / innerHeight, 1, 12000);
camera.position.set(650, 420, 760);

const controls = new OrbitControls(camera, renderer.domElement);
window.__v = { scene, camera, controls, state, FOG, lutPass }; // debug hook
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
  scene.backgroundIntensity = 0.5;
  scene.backgroundBlurriness = 0.08;
});

addEventListener('resize', () => {
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
  composer.setSize(innerWidth, innerHeight);
});

/* composer: scene -> RTT -> CCFS color grade -> screen (game's post chain).
   The 2012 GLES2 engine graded into a plain RGBA8 RTT (ColorGradingRTT) —
   UnsignedByteType parity; HalfFloat RTTs are also 10x slower on software GL. */
const composer = new EffectComposer(renderer, new THREE.WebGLRenderTarget(
  innerWidth * renderer.getPixelRatio(), innerHeight * renderer.getPixelRatio(),
  { type: THREE.UnsignedByteType, colorSpace: THREE.NoColorSpace }));
composer.addPass(new RenderPass(scene, camera));
composer.addPass(lutPass);
window.__v.composer = composer;

/* ---------------- the engine's shader (exact LightmapVCBlendDC port) ------ */
const cityVert = /* glsl */`
varying vec2 vUv;
varying float vDepth;
varying vec3 vWorld;
varying float vFogFactor;
varying float vFogY;
varying vec2  vFogUV;
uniform float uFogStart;
uniform float uFogScale;
uniform float uVFogHeight;
uniform float uFogDecay;
uniform vec4  uFogMap;
void main() {
  vUv = uv;
  vec4 wp = modelMatrix * vec4(position, 1.0);
  vWorld = wp.xyz;
  vec4 mv = modelViewMatrix * vec4(position, 1.0);
  vDepth = -mv.z;
  // FogFactor = (-viewZ - FogStartEnd.x) * FogStartEnd.y   (start=0)
  vFogFactor = (vDepth - uFogStart) * uFogScale;
  // fY = worldZ(up) * VerticalFogHeight + FogFactor * FOG_DECAY
  vFogY = vWorld.y * uVFogHeight + vFogFactor * uFogDecay;
  // FogUV = ((World*Position).xy - FogMap.xy) * FogMap.zw ; game Y = -view Z
  vFogUV = (vec2(vWorld.x, -vWorld.z) - uFogMap.xy) * uFogMap.zw;
  gl_Position = projectionMatrix * mv;
}`;

const cityFrag = /* glsl */`
precision mediump float;
uniform sampler2D map;
uniform float uMult;
uniform sampler2D uFogTex;
uniform vec3  uFogColor;
uniform float uFogAlpha;
uniform float uVFogHeight;
uniform float uVFogAlpha;
uniform float uFogStart;
uniform float uFogScale;
uniform float uFogDecay;
uniform vec4  uFogMap;
varying vec2 vUv;
varying float vDepth;
varying vec3 vWorld;
varying float vFogFactor;
varying float vFogY;
varying vec2  vFogUV;
void main() {
  // LightMapDC-FS: DiffuseMapColor * (texture2D(LightMap, vCoord1) * 2.0)
  vec3 col = texture2D(map, vUv).rgb * uMult;
  // exact TEXTURE_FOG path (LightmapVCBlendDC-f.glsl):
  vec4 FogMapColor = vec4(texture2D(uFogTex, vFogUV).rgb, uVFogAlpha);
  vec4 fogCol2 = mix(FogMapColor, vec4(uFogColor, uFogAlpha), clamp(vFogY, 0.0, 1.0));
  col = mix(col, fogCol2.rgb, clamp(vFogFactor, 0.0, 1.0) * fogCol2.a);
  gl_FragColor = vec4(col, 1.0);
}`;

/* shared fog uniform OBJECTS (mutated live -> every material follows) */
const fogUniforms = {
  uFogTex:     { value: null },                 // filled when GC_VerticalFOG loads
  uFogColor:   { value: new THREE.Color(...FOG.color) },
  uFogAlpha:   { value: FOG.colorA },
  uVFogHeight: { value: FOG.vfogHeight },
  uVFogAlpha:  { value: FOG.vfogAlpha },
  uFogStart:   { value: FOG.start },
  uFogScale:   { value: FOG.scale },
  uFogDecay:   { value: FOG.fogDecay },
  uFogMap:     { value: new THREE.Vector4(...FOG.map) },
};

function makeCityMaterial(tex, uMult) {
  return new THREE.ShaderMaterial({
    uniforms: {
      map: { value: tex },
      uMult: { value: uMult },
      ...fogUniforms,
    },
    vertexShader: cityVert,
    fragmentShader: cityFrag,
    side: THREE.DoubleSide,
  });
}

function makeTexlessCityMaterial() {
  // untextured geometry — same fog chain, flat engine fallback albedo
  return new THREE.ShaderMaterial({
    uniforms: { ...fogUniforms },
    vertexShader: cityVert,
    fragmentShader: /* glsl */`precision mediump float;
      uniform vec3 uFogColor; uniform float uFogAlpha; uniform sampler2D uFogTex;
      uniform float uVFogAlpha; uniform vec4 uFogMap;
      varying vec3 vWorld; varying float vFogFactor; varying float vFogY; varying vec2 vFogUV;
      void main() {
        vec3 col = vec3(0.063, 0.086, 0.137);   // Lambert fallback 0x101623
        vec4 FogMapColor = vec4(texture2D(uFogTex, vFogUV).rgb, uVFogAlpha);
        vec4 fogCol2 = mix(FogMapColor, vec4(uFogColor, uFogAlpha), clamp(vFogY,0.0,1.0));
        col = mix(col, fogCol2.rgb, clamp(vFogFactor,0.0,1.0) * fogCol2.a);
        gl_FragColor = vec4(col, 1.0);
      }`,
    side: THREE.DoubleSide,
  });
}

/* ---------------- texture cache ---------------- */
const texLoader = new THREE.TextureLoader();
const texCache = new Map(); // name -> Promise<Texture|null>
function getTex(name) {
  if (!texCache.has(name)) {
    texCache.set(name, new Promise((res) => {
      texLoader.load(`models/tex/${name}.jpg`,
        (t) => {
          // game samples PVR data top-down (v=0 = first memory row); three.js
          // defaults to flipY=true which would vertically flip every mapping.
          t.flipY = false;
          // 2012 GLES2: no sRGB decode — sample raw, shade in gamma space.
          t.colorSpace = THREE.NoColorSpace;
          t.anisotropy = 8;
          res(t);
        },
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

  root.traverse((obj) => {
    if (!obj.isMesh) return;
    const raw = obj.material?.name || '';
    const isDark = raw === '__dark';
    const pipe = raw.split('|');
    const texName = !isDark && pipe[0] ? pipe[0] : null;
    const mode = !isDark && pipe[1] === '2x' ? 2.0 : 1.0;
    const texPromise = texName ? getTex(texName) : Promise.resolve(null);
    obj.material = new THREE.MeshLambertMaterial({ color: 0x101623, side: THREE.DoubleSide });
    texPromise.then((tex) => {
      if (tex) {
        obj.material = makeCityMaterial(tex, mode);
      } else {
        obj.material = makeTexlessCityMaterial();
      }
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
  state.tiers.fp.enabled = true;   // street-level detail (per-building FP meshes)
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
  composer.render();
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
