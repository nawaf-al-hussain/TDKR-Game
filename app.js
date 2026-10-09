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
//
// v7: LIGHTNING + HURT — also extracted, not tuned:
// · BLightning() in the GothamCity Lua bootstrap (lvc string #0) fires THREE
//   one-shot ColorCorrection pulses of 023_lighting.tga plus a smart light:
//     flash 1  fade_in 30ms, run 30ms, fade_out 30ms   light on  75ms off  45ms
//     flash 2  fade_in 60ms, run 30ms, fade_out 150ms  light on 135ms off 135ms
//     flash 3  fade_in 30ms, run 30ms, fade_out  90ms  light on 105ms off  75ms
//   (PostProcessingEffectAdd('ColorCorrection', {extra_texture=
//    '023_lighting.tga', time_to_fade_in=X, time_to_run=30, time_to_fade_out=Y})
//   — CPostProcessEffect_ColorCorrection::Update @0x45ac88 state machine:
//   fade-in -> run -> fade-out, then effect removed.)
// · 023_lighting.tga mean (220,229,234) = near-white flash grade.
// · Health blend (CPostProcessManager::BuildColorGradingTexture @0x458e18):
//     t = (20 - GetHealth()) * (1/60) + 1.0        [DAT_004590c0 = 0.0166667]
//     t = min(t, 1 - CHUDDisplay::GetHurtAlpha())
//     t = clamp(t, 0.0, 1.0)                        [DAT_004590c4 = 0.0]
//     draw LUT_normal(+0x50) blended toward LUT_hurt(+0x54) by 1-t at intensity
//   LUT_hurt comes from the effect's second texture string; when absent the
//   code falls back to '000_default.tga' (getHackTex @0x45a8d8) — so for the
//   shipped night city the hurt LUT == normal LUT and the blend is a no-op
//   unless a gameplay script supplies one. We keep the exact mechanism and
//   drive uHurt from the effective hurtAlpha (keys [ and ]).
const LUT = {
  tex: 'models/tex/LUT_000_default.png',
  flashTex: 'models/tex/LUT_023_lighting.png',   // lightning flash grade (BLightning)
  cells: 32.0,
};

/* ---- BLightning: verbatim port of the Lua bootstrap sequence ------------- */
// one-shot ColorCorrection pulse: state machine @0x45ac88 —
//   fade-in over time_to_fade_in, hold time_to_run, fade-out over
//   time_to_fade_out, then removed. Blend weight w(t) ramps 0->1->0.
const LIGHTNING = {
  pulses: [                        // [fade_in, run, fade_out] ms — from BLightning
    [30, 30, 30],
    [60, 30, 150],
    [30, 30, 90],
  ],
  light: [75, 45, 135, 135, 105, 75],   // smart-light on/off ms, same source
  minInterval: 5000, maxInterval: 15000, // --Wait(Random(5000, 15000)) in bootstrap
};

const lightningState = {
  active: false,      // a 3-pulse strike is playing
  pulse: -1,
  t0: 0,
  phase: 'idle',
  nextStrike: performance.now() + 4000,
  enabled: true,      // c_LightningEnable = true (bootstrap)
  flash: 0.0,         // current grade blend 0..1 -> uFlash uniform
  lightBoost: 0.0,    // current smart-light boost 0..1
};

function stepLightning(now) {
  const L = lightningState;
  if (!L.enabled) { L.flash = 0; L.lightBoost = 0; L.active = false; L.phase = 'idle'; return; }
  if (!L.active && now >= L.nextStrike) {
    L.active = true; L.pulse = -1; L.phase = 'gap'; L.t0 = now;
  }
  if (!L.active) { L.flash *= 0.0; return; }
  if (L.phase === 'gap') {
    L.pulse++;
    if (L.pulse >= LIGHTNING.pulses.length) {
      L.active = false;
      L.flash = 0; L.lightBoost = 0;
      L.nextStrike = now + LIGHTNING.minInterval +
        Math.random() * (LIGHTNING.maxInterval - LIGHTNING.minInterval);
      L.phase = 'idle';
      return;
    }
    L.phase = 'pulse';
    L.t0 = now;
  }
  if (L.phase === 'pulse') {
    const [fi, run, fo] = LIGHTNING.pulses[L.pulse];
    const t = now - L.t0;
    const total = fi + run + fo;
    let w;
    if (t < fi) w = t / Math.max(fi, 1);            // fade in
    else if (t < fi + run) w = 1.0;                 // run
    else if (t < total) w = 1.0 - (t - fi - run) / Math.max(fo, 1);  // fade out
    else { L.phase = 'gap'; L.t0 = now; w = 0.0; }
    L.flash = Math.max(0, Math.min(1, w));
    // smart light windows: pulses start at 0 / 120 / 390 ms (75+45, +135+135)
    const starts = [0, LIGHTNING.light[0] + LIGHTNING.light[1],
      LIGHTNING.light[0] + LIGHTNING.light[1] + LIGHTNING.light[2] + LIGHTNING.light[3]];
    const s = starts[L.pulse];
    const on = LIGHTNING.light[L.pulse * 2], off = LIGHTNING.light[L.pulse * 2 + 1];
    const tl = now - (L.t0 - (now - L.t0)); // pulse start reference
    const dt = t;                            // time since pulse start
    L.lightBoost = dt >= s && dt < s + on ? 1.0 : 0.0;
  }
}

function triggerLightning() {
  lightningState.active = true;
  lightningState.pulse = -1;
  lightningState.phase = 'gap';
  lightningState.t0 = performance.now();
  lightningState.enabled = true;
}

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
// v7: the pass now carries the full effect stack:
//   base grade 000_default (always on, fade_in=0)
// + lightning flash: lerp toward CCFS(023_lighting) by uFlash (BLightning)
// + hurt blend: lerp toward CCFS(uLUTHurt) by uHurt (BuildColorGradingTexture)
const lutShader = {
  uniforms: {
    tDiffuse:   { value: null },
    uLUT:       { value: null },
    uLUTFlash:  { value: null },
    uLUTHurt:   { value: null },
    uCells:     { value: LUT.cells },
    uLutOn:     { value: 0.0 },   // flips to 1 once the LUT texture is loaded
    uFlash:     { value: 0.0 },   // BLightning grade blend 0..1
    uHurt:      { value: 0.0 },   // health/hurt blend 0..1 (1-t from the game)
  },
  vertexShader: /* glsl */`
    varying vec2 vUv;
    void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
  fragmentShader: /* glsl */`
    precision mediump float;
    uniform sampler2D tDiffuse;
    uniform sampler2D uLUT;
    uniform sampler2D uLUTFlash;
    uniform sampler2D uLUTHurt;
    uniform float uCells;
    uniform float uLutOn;
    uniform float uFlash;
    uniform float uHurt;
    varying vec2 vUv;
    // CCFS.glsl (verbatim constants from effects.gla)
    vec3 ccfs(sampler2D lut, vec4 color) {
      float cellsize = 1.0 / uCells;
      float r = color.r * cellsize;
      float b = floor(color.b * (uCells - 0.0001)) * cellsize;
      float u = r * 0.9375 + 0.03125 * cellsize + b;
      float v = color.g;
      return texture2D(lut, vec2(u, v)).rgb;
    }
    void main() {
      vec4 color = texture2D(tDiffuse, vUv);
      vec3 graded   = ccfs(uLUT, color);
      vec3 gradedFl = ccfs(uLUTFlash, color);   // 023_lighting lightning grade
      vec3 gradedHu = ccfs(uLUTHurt, color);    // hurt LUT (== normal for shipped Gotham)
      vec3 out3 = mix(graded, gradedFl, uFlash);
      out3 = mix(out3, gradedHu, uHurt);
      gl_FragColor = mix(color, vec4(out3, color.a), uLutOn);
    }`,
};
const lutPass = new ShaderPass(lutShader);
lutPass.renderToScreen = true;
function lutTexture(url) {
  // the game binds NEAREST + CLAMP for ColorGradingSampler (CPostProcessManager)
  return new Promise((res) => {
    new THREE.TextureLoader().load(url, (t) => {
      t.flipY = false;                      // PVR top-first rows
      t.magFilter = THREE.NearestFilter;
      t.minFilter = THREE.NearestFilter;
      t.wrapS = t.wrapT = THREE.ClampToEdgeWrapping;
      t.colorSpace = THREE.NoColorSpace;    // gamma-space pipeline parity
      res(t);
    }, undefined, () => res(null));
  });
}
Promise.all([lutTexture(LUT.tex), lutTexture(LUT.flashTex)]).then(([t, tf]) => {
  // NOTE: ShaderPass clones the shader uniforms -> mutate lutPass.uniforms
  lutPass.uniforms.uLUT.value = t;
  lutPass.uniforms.uLUTHurt.value = t;   // hurt fallback = 000_default.tga (getHackTex)
  lutPass.uniforms.uLUTFlash.value = tf || t;
  if (t) lutPass.uniforms.uLutOn.value = 1.0;
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
// start at street level over island1 (GLB axes: x = game x, y = game z)
camera.position.set(200, 260, 1500);

const controls = new OrbitControls(camera, renderer.domElement);
window.__v = { scene, camera, controls, state, FOG, lutPass, lightningState, triggerLightning }; // debug hook
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

// v11: LightMapDC two-channel variant — TEXCOORD_0 feeds the DiffuseMap,
// TEXCOORD_1 (game Coord1 * so1) feeds the shared island bake page.
const cityVertLM = /* glsl */`
attribute vec2 uv1;
varying vec2 vUv;
varying vec2 vUv1;
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
  vUv1 = uv1;
  vec4 wp = modelMatrix * vec4(position, 1.0);
  vWorld = wp.xyz;
  vec4 mv = modelViewMatrix * vec4(position, 1.0);
  vDepth = -mv.z;
  vFogFactor = (vDepth - uFogStart) * uFogScale;
  vFogY = vWorld.y * uVFogHeight + vFogFactor * uFogDecay;
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

// v11 engine parity: LightMapDC = DiffuseMap(Coord0) * LightMap(Coord1) * 2.
// The bake pages are the game's own per-object Beast tiles — multiplying the
// albedo back in restores the building structure the bake-only render lost.
function makeCityMaterialLM(tex, lmTex, uMult) {
  return new THREE.ShaderMaterial({
    uniforms: {
      map: { value: tex },
      lmap: { value: lmTex },
      uMult: { value: uMult },
      ...fogUniforms,
    },
    vertexShader: cityVertLM,
    fragmentShader: /* glsl */`precision mediump float;
      uniform sampler2D map;
      uniform sampler2D lmap;
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
      varying vec2 vUv1;
      varying float vDepth;
      varying vec3 vWorld;
      varying float vFogFactor;
      varying float vFogY;
      varying vec2  vFogUV;
      void main() {
        // LightMapDC-FS exact: DiffuseMapColor * texture2D(LightMap, vCoord1) * 2.0
        vec3 col = texture2D(map, vUv).rgb * texture2D(lmap, vUv1).rgb * uMult;
        vec4 FogMapColor = vec4(texture2D(uFogTex, vFogUV).rgb, uVFogAlpha);
        vec4 fogCol2 = mix(FogMapColor, vec4(uFogColor, uFogAlpha), clamp(vFogY, 0.0, 1.0));
        col = mix(col, fogCol2.rgb, clamp(vFogFactor, 0.0, 1.0) * fogCol2.a);
        gl_FragColor = vec4(col, 1.0);
      }`,
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

function makeAdditiveMaterial(tex) {
  // SimpleAdditive-fx port: glow planes / coronas / logos / volumetrics.
  // out = src + dst (gl.ONE, gl.ONE); the atlas IS the glow shape.
  // No fog chain — these are local light sources (fog would gray them out).
  return new THREE.ShaderMaterial({
    uniforms: { map: { value: tex } },
    vertexShader: cityVert,
    fragmentShader: /* glsl */`precision mediump float;
      uniform sampler2D map;
      varying vec2 vUv;
      void main() {
        vec3 col = texture2D(map, vUv).rgb;
        gl_FragColor = vec4(col, 1.0);
      }`,
    side: THREE.DoubleSide,
    blending: THREE.AdditiveBlending,
    transparent: true,
    depthWrite: false,
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
    // v11 contract: '<dif>|<lm>|<mode>' (lightmapped) or '<tex>|<mode>'
    let texName = null, lmName = null, modeStr = 'd';
    if (!isDark) {
      if (pipe.length >= 3) {
        texName = pipe[0] || null;
        lmName = pipe[1] || null;
        modeStr = pipe[2] || 'd';
      } else {
        texName = pipe[0] || null;
        modeStr = pipe[1] || 'd';
      }
    }
    const isAdd = !isDark && modeStr === 'add';
    const mode = !isDark && modeStr === '2x' ? 2.0 : 1.0;
    const texPromise = texName ? getTex(texName) : Promise.resolve(null);
    const lmPromise = lmName ? getTex(lmName) : Promise.resolve(null);
    obj.material = new THREE.MeshLambertMaterial({ color: 0x101623, side: THREE.DoubleSide });
    Promise.all([texPromise, lmPromise]).then(([tex, lm]) => {
      if (isAdd && tex) {
        obj.material = makeAdditiveMaterial(tex);
      } else if (tex && lm) {
        obj.material = makeCityMaterialLM(tex, lm, mode);
      } else if (lm && !tex) {
        // bake page alone (x2) — object whose DiffuseMap is a runtime bake
        obj.material = makeCityMaterial(lm, 2.0);
      } else if (tex) {
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
const TIER_LABEL = { street: 'Street level', skyline: 'Skyline (baked city)', hero: 'Hero units', fp: 'Footprints', low: 'Low-detail LOD', district: 'District props' };
const TIER_ORDER = ['street', 'skyline', 'hero', 'fp', 'district', 'low'];

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

/* ---- BLightning / hurt controls (exact game data, keys) ------------------ */
// L          = trigger a BLightning strike now (3 pulses + smart light)
// Shift+L    = toggle c_LightningEnable (auto strikes, Random(5000,15000) ms)
// [ / ]      = hurtAlpha down/up (health blend; the game computes it from
//              GetHealth via CHUDDisplay::GetHurtAlpha — see notes above)
addEventListener('keydown', (ev) => {
  if (ev.key === 'l' || ev.key === 'L') {
    if (ev.shiftKey) {
      lightningState.enabled = !lightningState.enabled;
      setStatus(lightningState.enabled ? 'lightning: auto (c_LightningEnable)'
                                       : 'lightning: disabled');
      setTimeout(clearStatus, 1600);
    } else {
      triggerLightning();
    }
  } else if (ev.key === '[' || ev.key === ']') {
    const h = lutPass.uniforms.uHurt.value + (ev.key === ']' ? 0.1 : -0.1);
    lutPass.uniforms.uHurt.value = Math.max(0, Math.min(1, h));
    setStatus(`hurtAlpha = ${lutPass.uniforms.uHurt.value.toFixed(2)}  ` +
              `(t = clamp((20-hp)/60+1,0,1), hurt = 1-t)`);
    setTimeout(clearStatus, 2200);
  }
});

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
  // v13 boot policy (session 12): STREET + SKYLINE boot together — the
  // island LongDist bake units now carry their real world transforms,
  // decoded from the lvc CTemplateObject records (session 12:
  // island1 = (-141.69,-681.15,0.114); island2 authored origin-relative).
  // Hero bridges/monorail/railway stay research toggles until their own
  // lvc placement records are decoded.
  if (state.tiers.street) state.tiers.street.enabled = true;
  if (state.tiers.skyline) state.tiers.skyline.enabled = true;
  // district props: several are authored in LOCAL space (unplaced) — keep
  // off by default to avoid floating geometry over the city
  buildTierButtons();

  // stream the real city first: world-correct streets with the game's own
  // road/grass/prop materials
  const streetGlbs = (state.tiers.street?.glbs || []);
  let done = 0;
  setStatus(`streaming city · 0/${streetGlbs.length}`);
  for (const entry of streetGlbs) {
    if (!entry.loaded) {
      try { await loadGLB(entry, 'street'); } catch (e) { console.warn('street glb failed', entry.file, e); }
    }
    done++;
    $('load-bar').style.width = `${(done / Math.max(streetGlbs.length,1)) * 100}%`;
    setStatus(`streaming city · ${done}/${streetGlbs.length}`);
  }
  if (state.tiers.street) state.tiers.street.loaded = true;
  // district props (world-authored landmarks) in the background
  if (state.tiers.district && state.tiers.district.enabled && !state.tiers.district.loaded) {
    state.tiers.district.loaded = true;
    (async () => {
      for (const entry of state.tiers.district.glbs) {
        if (!entry.loaded) {
          try { await loadGLB(entry, 'district'); } catch (e) { console.warn('district glb failed', entry.file, e); }
        }
      }
      updateHUDTotals();
    })();
  }
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
const MOON_BASE = 0.45;
function animate(t) {
  requestAnimationFrame(animate);
  controls.update();
  // BLightning: grade + smart-light windows (CWeatherManager-driven in-game;
  // here the moon light plays the smartLightId role)
  stepLightning(t);
  lutPass.uniforms.uFlash.value = lightningState.flash;
  moon.intensity = MOON_BASE + lightningState.lightBoost * 2.2;
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
