<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>TDKR integration (s49 T5 — staged, NOT deployed)</title>
<style>
  body { margin: 0; background: #14161c; color: #cdd3e0; font: 13px/1.5 system-ui, sans-serif; }
  #panel { position: fixed; left: 8px; top: 8px; z-index: 9; background: rgba(10,12,18,.85);
           border: 1px solid #334; border-radius: 8px; padding: 10px 12px; max-width: 460px; }
  #log { white-space: pre-wrap; max-height: 46vh; overflow: auto; }
  #zone { position: fixed; right: 8px; top: 8px; border: 1px solid #334; }
  #bman { position: fixed; right: 8px; bottom: 8px; border: 1px solid #334; background: #fff; }
  input[type=file] { color: #cdd3e0; }
  b { color: #9fc3ff; }
</style>
<script src="./etc1_tdkr.js"></script>
<script src="./tdkr_pipeline.js"></script>
<script src="./lvc.js"></script>
<script src="./walktest.js"></script>
<script src="./walktest_routes.js"></script>
<script type="importmap">
{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
"three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}
</script>
</head>
<body>
<div id="panel">
  <b>s49 T5 integration</b> — one page, ONE user zip: (1) zone-scale city render with the
  engine's own GLSL + compiled material/texture bindings (raw WebGL1, capsule-follow camera),
  (2) navmesh walker + collision soup parsed from YOUR files (self-check + sha256 digest),
  (3) Batman from YOUR zip (skin+anims+RGB888 texture, GLB assembled in-browser).
  The capsule replays a harness route on the city; camera follows.<br>
  <code>?corrupt=1</code> = negative control (navmesh bytes corrupted must be caught).<br>
  Pick the release <b>TDKR_v1.1.6b_APK_OBB.zip</b>:<br>
  <input type="file" id="f">
  <div id="log"></div>
</div>
<canvas id="zone" width="1024" height="605"></canvas>
<canvas id="bman" width="320" height="240"></canvas>
<script type="module">
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const log = (s) => { document.querySelector('#log').textContent += s + '\n'; };
window.__GATE = { ready: false, done: false, heapSamples: [] };
window.__consoleErrors = [];
window.addEventListener('error', e => window.__consoleErrors.push('window.onerror: ' + e.message));
const _origErr = console.error;
console.error = function () {
  try { window.__consoleErrors.push(Array.from(arguments).map(String).join(' ').slice(0, 300)); } catch (_) {}
  return _origErr.apply(console, arguments);
};
const heapMB = () => performance.memory ? Math.round(performance.memory.usedJSHeapSize / 1048576) : -1;
setInterval(() => { const h = heapMB(); if (h > 0) window.__GATE.heapSamples.push(h); }, 1000);

function u16le(u8, i) { return u8[i] | (u8[i + 1] << 8); }
function u32le(u8, i) { return (u8[i] | (u8[i + 1] << 8) | (u8[i + 2] << 16) | (u8[i + 3] << 24)) >>> 0; }
function u32be(u8, i) { return ((u8[i] << 24) | (u8[i + 1] << 16) | (u8[i + 2] << 8) | u8[i + 3]) >>> 0; }
const LATIN = new TextDecoder('latin1');

/* ---------------- zip + gla members (city_zone2 path, verified s48/s49) ---------------- */
function zipMembers(buf) {
  let eocd = -1;
  for (let i = buf.length - 22; i >= Math.max(0, buf.length - 66000); i--)
    if (u32le(buf, i) === 0x06054b50) { eocd = i; break; }
  if (eocd < 0) throw new Error('no EOCD');
  const n = u16le(buf, eocd + 10);
  let p = u32le(buf, eocd + 16);
  const members = new Map();
  for (let k = 0; k < n; k++) {
    if (u32le(buf, p) !== 0x02014b50) throw new Error('bad CD');
    const method = u16le(buf, p + 10), csize = u32le(buf, p + 20);
    const nlen = u16le(buf, p + 28), elen = u16le(buf, p + 30), clen = u32le(buf, p + 32);
    const lho = u32le(buf, p + 42);
    members.set(LATIN.decode(buf.subarray(p + 46, p + 46 + nlen)), { method, csize, lho });
    p += 46 + nlen + elen + clen;
  }
  return members;
}
async function zipRead2(buf, m) {
  const lho = m.lho, nlen = u16le(buf, lho + 26), elen = u16le(buf, lho + 28);
  const start = lho + 30 + nlen + elen;
  const raw = buf.subarray(start, start + m.csize);
  if (m.method === 0) return raw;
  if (m.method === 8) {
    const ds = new DecompressionStream('deflate-raw');
    const stream = new Response(new Blob([raw])).body.pipeThrough(ds);
    return new Uint8Array(await new Response(stream).arrayBuffer());
  }
  throw new Error('method ' + m.method);
}
function glaMember(g, want) {
  const idxSize = u32be(g, 4), n = u32be(g, 12);
  const pool = g.subarray(16 + n * 16, idxSize);
  for (let i = 0; i < n; i++) {
    const o = u32be(g, 16 + i * 16), s = u32be(g, 16 + i * 16 + 4),
          no = u32be(g, 16 + i * 16 + 8);
    let e = pool.indexOf(0, no);
    const nm = LATIN.decode(pool.subarray(no, e < 0 ? no + 96 : e));
    if (nm === want) return g.subarray(o, o + s);
  }
  throw new Error('gla member not found: ' + want);
}
function texMember(g, want) {
  if (!g) return null;
  const idxSize = u32be(g, 4), n = u32be(g, 12);
  const pool = g.subarray(16 + n * 16, idxSize);
  const wantL = want.toLowerCase();
  for (let i = 0; i < n; i++) {
    const o = u32be(g, 16 + i * 16), s = u32be(g, 16 + i * 16 + 4),
          no = u32be(g, 16 + i * 16 + 8);
    let e = pool.indexOf(0, no);
    const nm = LATIN.decode(pool.subarray(no, e < 0 ? no + 96 : e));
    if (nm.toLowerCase() === wantL) return g.subarray(o, o + s);
  }
  return null;
}
function cstrAt(u8, off, maxn = 96) {
  if (!(off > 0 && off < u8.length)) return null;
  let e = off;
  const lim = Math.min(u8.length, off + maxn);
  while (e < lim && u8[e] !== 0) e++;
  if (e === off || e === lim) return null;
  const s = LATIN.decode(u8.subarray(off, e));
  for (let i = 0; i < s.length; i++) {
    const c = s.charCodeAt(i);
    if (c < 32 || c > 126) return null;
  }
  return s;
}

/* ---------------- compiled instance table (s48 T3) ---------------- */
function parseCompiledTable(le) {
  const dv = new DataView(le.buffer, le.byteOffset, le.byteLength);
  const IMG_BASE = 0x22a9c, IMG_N = 176;
  const imgs = [];
  for (let i = 0; i < IMG_N; i++) {
    imgs.push([dv.getUint32(IMG_BASE + i * 12, true), dv.getUint32(IMG_BASE + i * 12 + 8, true)]);
  }
  const bind = {}, fx = {};
  for (let i = 0; i < 307; i++) {
    const a = 0x5fea0 + i * 36;
    const w = [];
    for (let k = 0; k < 9; k++) w.push(dv.getUint32(a + k * 4, true));
    const sam = {};
    for (let j = 0; j < w[4]; j++) {
      const pa = w[5] + j * 24;
      const pw = [];
      for (let k = 0; k < 6; k++) pw.push(dv.getUint32(pa + k * 4, true));
      const pname = cstrAt(le, pw[0]);
      if (pw[2] !== 13 || pw[3] !== 1) continue;
      const v1 = pw[4];
      if (dv.getUint32(v1, true) !== 1 || dv.getUint32(v1 + 4, true) !== v1 + 24) continue;
      const idx = dv.getUint32(v1 + 24, true);
      if (idx < IMG_N) sam[pname] = cstrAt(le, imgs[idx][1]) || '';
      else if (idx === 0xffffffff) sam[pname] = '';
    }
    bind[i] = [sam['DiffuseMap'] || '', sam['LightMap'] || ''];
    fx[i] = (cstrAt(le, w[3]) || '').split('-fx')[0].replace('#', '');
  }
  return { bind, fx };
}

const VAVT = [1, 1, 2, 2, 4, 4, 4];
function declOf(bi8, mid) {
  const bstride = u32le(bi8, 0);
  const base = 4 + mid * bstride;
  const N = bi8[base + 33];
  const ds = [];
  let start = 0;
  for (let j = 0; j < N; j++) {
    const d = base + 40 + j * 12;
    const A = (bi8[d] << 8) | bi8[d + 1];
    const B = (bi8[d + 2] << 8) | bi8[d + 3];
    const C = (bi8[d + 4] << 8) | bi8[d + 5];
    const st = (bi8[d + 6] << 8) | bi8[d + 7];
    const off = (bi8[d + 8] << 8) | bi8[d + 9];
    const size = B === 0 ? 3 : B * VAVT[C];
    const end = off === 0 ? st : off;
    ds.push({ attr: A, start, end, size });
    start = end;
  }
  return ds;
}

/* ---------------- SPLIT-aware ETC1 decode with LRU (city_zone2, verified) ---------------- */
const LRU_CAP = 20;
const texLRU = new Map();
const texStats = { miss: 0, hit: 0, evict: 0 };
function unwrapSplitParts(u8) {
  if (!(u8[0] === 0x50 && u8[1] === 0x4b && u8[2] === 0x03 && u8[3] === 0x04)) return { rgb: u8 };
  const out = {};
  let pos = 0;
  while (pos + 30 <= u8.length && u8[pos] === 0x50 && u8[pos + 1] === 0x4b &&
         u8[pos + 2] === 0x03 && u8[pos + 3] === 0x04) {
    const csz = u32le(u8, pos + 18);
    const nlen = u16le(u8, pos + 26), elen = u16le(u8, pos + 28);
    const nm = LATIN.decode(u8.subarray(pos + 30, pos + 30 + nlen));
    const dstart = pos + 30 + nlen + elen;
    if (nm.trim() !== 'SPLIT') out[nm] = u8.subarray(dstart, dstart + csz);
    pos = dstart + csz;
  }
  if (!out['rgb.pvr']) throw new Error('split-zip: no rgb.pvr');
  return out;
}
function decodePvr(u8) {
  const dv = new DataView(u8.buffer, u8.byteOffset, u8.byteLength);
  if (dv.getUint32(0, true) !== 0x34) throw new Error('bad tex tag');
  const h = dv.getUint32(4, true), w = dv.getUint32(8, true);
  if (String.fromCharCode(u8[44], u8[45], u8[46], u8[47]) !== 'PVR!') throw new Error('bad PVR');
  const bw = (w + 3) >> 2, bh = (h + 3) >> 2;
  const rgba = window.ETC1_TDKR.decodeRGBA(u8.subarray(52, 52 + bw * bh * 8), w, h);
  return { w, h, rgba };
}
function getTex(texGla, name, wantAlpha) {
  const key = name + '|' + (wantAlpha ? 'a' : 'r');
  if (texLRU.has(key)) {
    texStats.hit++;
    const v = texLRU.get(key);
    texLRU.delete(key);
    texLRU.set(key, v);
    return v;
  }
  texStats.miss++;
  let t = null;
  // s52 T4: prefer the range-captured pool (l_gothamcity_tex.gla is never materialized whole)
  let tu = (typeof texPool !== 'undefined' && texPool) ? texPool.get(name.toLowerCase()) : null;
  if (!tu) tu = texMember(texGla, name);
  if (tu) {
    try {
      const parts = unwrapSplitParts(tu);
      const rgb = decodePvr(parts['rgb.pvr'] || parts['rgb']);
      let al = null;
      if (wantAlpha && parts['alpha.pvr']) {
        const a = decodePvr(parts['alpha.pvr']);
        al = { w: a.w, h: a.h, data: a.rgba };
      }
      t = { w: rgb.w, h: rgb.h, data: rgb.rgba, alpha: al };
    } catch (e) { t = null; }
  }
  if (t) t.bytes = t.w * t.h * 4 + (t.alpha ? t.alpha.w * t.alpha.h : 0);
  texLRU.set(key, t);
  lruBytes += t ? t.bytes : 0;
  // s52 T4: byte cap in addition to the entry cap
  while (texLRU.size > 1 && (texLRU.size > LRU_CAP || lruBytes > LRU_BYTES)) {
    const old = texLRU.keys().next().value;
    const ov = texLRU.get(old);
    lruBytes -= (ov && ov.bytes) ? ov.bytes : 0;
    texLRU.delete(old);
    texStats.evict++;
  }
  return t;
}

/* ---------------- engine GLSL (verbatim effects.gla extraction, s49 T1 gates) ---------------- */
const CONFIG = `
precision highp float;
#define VERTICAL_FOG_COLOR vec4(0.93, 0.76, 0.47, 0.35)
#define VERTICAL_FOG_HEIGHT 18.0
#define LOD_BIAS -1.0
#define FOG_DECAY 0.5
`;
const LIGHTMAPDC_V = CONFIG + `
attribute       highp   vec3    Normal;
attribute       highp   vec4    Position;
attribute       lowp    vec4    Color;
attribute       highp   vec2    Coord0;
attribute       highp   vec2    Coord1;
uniform         highp   vec4    Coord0_scaleoffset;
uniform         highp   vec4    Coord1_scaleoffset;
uniform         highp   mat4    WorldViewProjection;
uniform     highp       vec4    LightMapAtlas;
varying         highp   vec2    vCoord0;
varying         highp   vec2    vCoord1;
uniform         highp   mat4    WorldViewTransposed;
uniform         highp   vec2    FogStartEnd;
uniform         lowp    vec4    FogColor;
varying         lowp    float   FogFactor;
void main()
{
        vCoord0                                         = Coord0 * Coord0_scaleoffset.xy + Coord0_scaleoffset.zw;
        vCoord1                                         = (Coord1 * Coord1_scaleoffset.xy + Coord1_scaleoffset.zw) * LightMapAtlas.xy + LightMapAtlas.zw;
        highp vec4 pos                          = Position;
        gl_Position                             = WorldViewProjection * pos;
        FogFactor                       = (-dot(WorldViewTransposed[2], Position) - FogStartEnd.x) * FogStartEnd.y;
}
`;
const LIGHTMAPDC_F = CONFIG + `
uniform         lowp    sampler2D               DiffuseMap;
uniform         lowp    sampler2D               LightMap;
varying         mediump vec2    vCoord0;
varying         mediump vec2    vCoord1;
uniform         lowp    vec4    FogColor;
varying         lowp    float   FogFactor;
lowp vec4 ComputeFogFS(lowp vec4 col, lowp vec4 fogCol, lowp float fogF)
{
        lowp    float   GrayScale       = dot(col.xyz, vec3(0.149, 0.293, 0.57));
        lowp    float   fFactor         = fogF * (1.0 - GrayScale);
        return vec4(mix(col.rgb, fogCol.rgb, fFactor * fogCol.a), col.a);
}
void main()
{
        lowp    vec4    LightMapColor   = texture2D(LightMap, vCoord1) * 2.0;
        highp   vec4    DiffuseMapColor = texture2D(DiffuseMap, vCoord0, LOD_BIAS);
        lowp    vec4  Color                             = DiffuseMapColor * LightMapColor;
        Color                                                   = ComputeFogFS(Color, FogColor, clamp(FogFactor, 0.0, 1.0));
        gl_FragColor                                    = Color;
}
`;
const ALPHAMASKING_V = CONFIG + `
attribute       highp   vec4    Position;
attribute       lowp    vec4    Color;
attribute       highp   vec2    TexCoord0;
attribute       highp   vec2    TexCoord1;
uniform         highp   vec4    TexCoord0_scaleoffset;
uniform         highp   vec4    TexCoord1_scaleoffset;
uniform         highp   mat4    WorldViewProjection;
uniform     highp       vec4    LightMapAtlas;
varying         highp   vec2    vCoord0;
varying         highp   vec2    vCoord1;
uniform         highp   mat4    WorldViewTransposed;
uniform         highp   vec2    FogStartEnd;
uniform         lowp    vec4    FogColor;
varying         lowp    float   FogFactor;
void main()
{
        vCoord0                                         = TexCoord0 * TexCoord0_scaleoffset.xy + TexCoord0_scaleoffset.zw;
        vCoord1                                         = (TexCoord1 * TexCoord1_scaleoffset.xy + TexCoord1_scaleoffset.zw) * LightMapAtlas.xy + LightMapAtlas.zw;
        highp vec4 pos                          = Position;
        gl_Position                             = WorldViewProjection * pos;
        FogFactor                       = (-dot(WorldViewTransposed[2], Position) - FogStartEnd.x) * FogStartEnd.y;
}
`;
const ALPHAMASKING_F = CONFIG + `
#ifdef TDKR_SPLIT_ALPHA
uniform         lowp    sampler2D               DiffuseMap_alpha;
#endif
uniform         lowp    sampler2D               DiffuseMap;
uniform         lowp    sampler2D               LightMap;
uniform         lowp    float   Overbright;
varying         mediump vec2    vCoord0;
varying         mediump vec2    vCoord1;
uniform         lowp    vec4    FogColor;
varying         lowp    float   FogFactor;
lowp vec4 ComputeFogFS(lowp vec4 col, lowp vec4 fogCol, lowp float fogF)
{
        lowp    float   GrayScale       = dot(col.xyz, vec3(0.149, 0.293, 0.57));
        lowp    float   fFactor         = fogF * (1.0 - GrayScale);
        return vec4(mix(col.rgb, fogCol.rgb, fFactor * fogCol.a), col.a);
}
void main()
{
#if defined(TDKR_SPLIT_ALPHA) && !defined(NO_ALPHA)
        highp   vec4  DiffuseMapColor   = vec4(texture2D(DiffuseMap, vCoord0).rgb, texture2D(DiffuseMap_alpha, vCoord0, -2.0).r);
#else
        highp   vec4  DiffuseMapColor   = texture2D(DiffuseMap, vCoord0);
#endif
        highp float fAlpha                              = DiffuseMapColor.a ;
        lowp    vec4  LightMapColor             = texture2D(LightMap, vCoord1) * 2.0 + vec4(Overbright);
        lowp    vec4  Color                             = DiffuseMapColor * LightMapColor ;
        Color                                                   = ComputeFogFS(Color, FogColor, clamp(FogFactor, 0.0, 1.0));
        gl_FragColor                                    = vec4(Color.rgb, fAlpha);
#if !defined(MODULATE) && !defined(NO_ALPHA)
        if (fAlpha < 0.3)
                discard;
#endif
}
`;
const NVGLASS_V = `
attribute highp vec4 Position;
attribute highp vec3 Normal;
attribute mediump vec2 TexCoord0;
uniform         highp   vec4    TexCoord0_scaleoffset;
attribute mediump vec2 TexCoord1;
uniform         highp   vec4    TexCoord1_scaleoffset;
attribute lowp vec4 Color0;
uniform mediump vec2 uvOffset;
uniform highp   mat4 WorldViewProjectionMatrix;
#if defined(LIGHTMAP)
        varying mediump vec2 vCoord1;
#endif
varying highp vec2 vCoord0;
varying lowp vec4 vColor0;
uniform         highp   mat4    WorldViewTransposed;
uniform         highp   vec2    FogStartEnd;
uniform         lowp    vec4    FogColor;
varying         lowp    float   FogFactor;
void main()
{
        vCoord0 = TexCoord0 * TexCoord0_scaleoffset.xy + TexCoord0_scaleoffset.zw + uvOffset;
        vColor0 = Color0;
#if defined(LIGHTMAP)
        vCoord1 = TexCoord1 * TexCoord1_scaleoffset.xy + TexCoord1_scaleoffset.zw;
#endif
        gl_Position                     = WorldViewProjectionMatrix * Position;
        FogFactor                       = (-dot(WorldViewTransposed[2], Position) - FogStartEnd.x) * FogStartEnd.y;
}
`;
const NVGLASS_F = `
precision mediump float;
#ifdef TDKR_SPLIT_ALPHA
uniform lowp    sampler2D DiffuseTextureSampler_alpha;
#endif
uniform lowp    sampler2D DiffuseTextureSampler;
#if defined(TEX2)
        uniform lowp    sampler2D Diffuse2TextureSampler;
#endif
#if defined(REFLECTION)
uniform lowp    sampler2D ReflectionMapSampler;
varying mediump   vec3  vViewDir;
varying mediump   vec3  vNormal;
#endif
#if defined(LIGHTMAP)
uniform lowp    sampler2D LightmapTextureSampler;
#endif
#if defined(DIFFUSE_MASK)
uniform lowp    sampler2D DiffuseMaskSampler;
#else
uniform lowp float BlendFactor;
#endif
uniform lowp vec4 Ambient;
varying mediump vec2 vCoord0;
varying lowp vec4 vColor0;
#if defined(LIGHTMAP)
        varying mediump vec2 vCoord1;
#endif
uniform         lowp    vec4    FogColor;
varying         lowp    float   FogFactor;
lowp vec4 ComputeFogFS(lowp vec4 col, lowp vec4 fogCol, lowp float fogF)
{
        lowp    float   GrayScale       = dot(col.xyz, vec3(0.149, 0.293, 0.57));
        lowp    float   fFactor         = fogF * (1.0 - GrayScale);
        return vec4(mix(col.rgb, fogCol.rgb, fFactor * fogCol.a), col.a);
}
void main()
{
#if defined(TDKR_SPLIT_ALPHA) && defined(HAS_ALPHA)
        lowp vec4 Color = vec4(texture2D(DiffuseTextureSampler, vCoord0).rgb, texture2D(DiffuseTextureSampler_alpha, vCoord0).r);
#else
        lowp vec4 Color = texture2D(DiffuseTextureSampler, vCoord0);
#endif
#if !defined(TEX2)
        Color = Color * vColor0;
#endif
#if defined(DIFFUSE_MASK)
        lowp vec4 Mask  = texture2D(DiffuseMaskSampler, vCoord0);
#endif
        lowp vec4 Lighting = vec4(1.0);
#if defined(LIGHTMAP)
        lowp vec4 lmColor = texture2D(LightmapTextureSampler, vCoord1) * 2.0;
        Lighting = lmColor;
#endif
        Color *= Lighting;
#if defined(DIFFUSE_MASK)
        gl_FragColor = vec4(Color.rgb, Mask.g * vColor0.a);
#else
        gl_FragColor = Color;
#endif
        Color                                                   = ComputeFogFS(gl_FragColor, FogColor, clamp(FogFactor, 0.0, 1.0));
        gl_FragColor                                    = Color;
}
`;
const VCBLEND_V = `
attribute highp vec4 Position;
attribute highp vec3 Normal;
attribute lowp  vec4 Color;
attribute highp vec2 Coord0;
attribute highp vec2 Coord1;
uniform         highp   vec4    Coord0_scaleoffset;
uniform         highp   vec4    Coord1_scaleoffset;
uniform         highp   mat4    WorldViewProjection;
uniform     highp       vec4    LightMapAtlas;
varying lowp    vec4    vColor;
varying mediump vec2    vCoord0;
varying mediump vec2    vCoord1;
uniform         highp   mat4    WorldViewTransposed;
uniform         highp   vec2    FogStartEnd;
uniform         lowp    vec4    FogColor;
varying         lowp    float   FogFactor;
void main()
{
        vColor                                          = Color;
        vCoord0                                         = Coord0 * Coord0_scaleoffset.xy + Coord0_scaleoffset.zw;
        vCoord1                                         = (Coord1 * Coord1_scaleoffset.xy + Coord1_scaleoffset.zw) * LightMapAtlas.xy + LightMapAtlas.zw;
        gl_Position                             = WorldViewProjection * Position;
        FogFactor                       = (-dot(WorldViewTransposed[2], Position) - FogStartEnd.x) * FogStartEnd.y;
}
`;
const VCBLEND_F = `
precision mediump float;
uniform lowp    sampler2D LightMapSampler;
uniform lowp    sampler2D Texture1;
uniform lowp    sampler2D Texture2;
varying lowp    vec4    vColor;
varying mediump vec2    vCoord0;
varying mediump vec2    vCoord1;
uniform         lowp    vec4    FogColor;
varying         lowp    float   FogFactor;
lowp vec4 ComputeFogFS(lowp vec4 col, lowp vec4 fogCol, lowp float fogF)
{
        lowp    float   GrayScale       = dot(col.xyz, vec3(0.149, 0.293, 0.57));
        lowp    float   fFactor         = fogF * (1.0 - GrayScale);
        return vec4(mix(col.rgb, fogCol.rgb, fFactor * fogCol.a), col.a);
}
void main()
{
    lowp vec4 _LightMap = texture2D(LightMapSampler, vCoord1, -1.0) * 2.0;
        lowp vec4 _Texture1     = texture2D(Texture1, vCoord0, -1.0);
        lowp vec4 _Texture2     = texture2D(Texture2, vCoord0, -1.0);
        lowp float BlendFactor = vColor.a;
        lowp vec4 Color         = _LightMap * mix(_Texture1, _Texture2, BlendFactor) * vec4(vColor.rgb, 1.0);
        Color                                                   = ComputeFogFS(Color, FogColor, clamp(FogFactor, 0.0, 1.0));
        gl_FragColor                                    = vec4(Color.rgb, 1.0);
}
`;

/* ================= zone GL renderer (s49 T4a, adapted to a follow camera) ================= */
const zcv = document.getElementById('zone');
const G = zcv.getContext('webgl', { preserveDrawingBuffer: true, antialias: false, depth: true });
if (!G) throw new Error('no webgl');
const W = 1024, H = 605;
function compileZ(type, src) {
  const s = G.createShader(type);
  G.shaderSource(s, src);
  G.compileShader(s);
  if (!G.getShaderParameter(s, G.COMPILE_STATUS))
    throw new Error('shader: ' + G.getShaderInfoLog(s).slice(0, 300));
  return s;
}
const progZ = new Map();
function getProgZ(key, vs, fs) {
  if (progZ.has(key)) return progZ.get(key);
  const p = G.createProgram();
  G.attachShader(p, compileZ(G.VERTEX_SHADER, vs));
  G.attachShader(p, compileZ(G.FRAGMENT_SHADER, fs));
  G.linkProgram(p);
  if (!G.getProgramParameter(p, G.LINK_STATUS))
    throw new Error('link: ' + G.getProgramInfoLog(p));
  const o = { p, attr: {}, uni: {} };
  const na = G.getProgramParameter(p, G.ACTIVE_ATTRIBUTES);
  for (let i = 0; i < na; i++) {
    const inf = G.getActiveAttrib(p, i);
    o.attr[inf.name] = G.getAttribLocation(p, inf.name);
  }
  const nu = G.getProgramParameter(p, G.ACTIVE_UNIFORMS);
  for (let i = 0; i < nu; i++) {
    const inf = G.getActiveUniform(p, i);
    o.uni[inf.name.replace('[0]', '')] = G.getUniformLocation(p, inf.name);
  }
  progZ.set(key, o);
  return o;
}
const texZ = new Map();
const texZstats = { decoded: 0 };
window.__TEXMISS = [];
function texZget(name, wantAlpha) {
  const key = name + (wantAlpha ? '|a' : '');
  if (texZ.has(key)) return texZ.get(key);
  // s53 T4 ?poolchunk=1: texture already decoded AND uploaded by the chunked capture;
  // only the GL handle (+alpha for AlphaMasking) is stored - no CPU bytes exist.
  const pk = (preTex && preTex.get(name.toLowerCase())) || null;
  if (pk && pk.uploaded) {
    const o = { tx: pk.tx, alpha: pk.alpha, w: pk.w, h: pk.h, name: name };
    texZ.set(key, o);
    texZstats.decoded++;
    return o;
  }
  const t = pk || getTex(texGla, name, wantAlpha);
  if (!t) { texZ.set(key, null);
    window.__TEXMISS.push(name);
    return null; }
  const tx = G.createTexture();
  G.bindTexture(G.TEXTURE_2D, tx);
  G.texImage2D(G.TEXTURE_2D, 0, G.RGBA, t.w, t.h, 0, G.RGBA, G.UNSIGNED_BYTE,
               new Uint8Array(t.data.buffer, t.data.byteOffset, t.data.byteLength));
  G.texParameteri(G.TEXTURE_2D, G.TEXTURE_WRAP_S, G.REPEAT);
  G.texParameteri(G.TEXTURE_2D, G.TEXTURE_WRAP_T, G.REPEAT);
  G.texParameteri(G.TEXTURE_2D, G.TEXTURE_MIN_FILTER, G.NEAREST);
  G.texParameteri(G.TEXTURE_2D, G.TEXTURE_MAG_FILTER, G.NEAREST);
  const o = { tx, alpha: t.alpha, w: t.w, h: t.h, name: name };  // s53 T1: name for the unit audit
  texZ.set(key, o);
  texZstats.decoded++;
  if (TEXFREE) {          // s58 T4 lever: CPU bytes no longer needed once uploaded
    t.data = null; if (t.alpha) t.alpha.data = null;
    texLRU.delete(key); lruBytes -= (t.bytes || 0);
  }
  return o;
}
const alphaTexCache = new Map();
function alphaTexOf(dTex, name) {
  const key = name + '|alphaTx';
  if (alphaTexCache.has(key)) return alphaTexCache.get(key);
  const n = dTex.alpha.w * dTex.alpha.h;
  const arr = new Uint8Array(n * 4);
  for (let i = 0; i < n; i++) {
    const v = dTex.alpha.data[i * 4];
    arr[i*4] = v; arr[i*4+1] = v; arr[i*4+2] = v; arr[i*4+3] = 255;
  }
  const at = G.createTexture();
  G.bindTexture(G.TEXTURE_2D, at);
  G.texImage2D(G.TEXTURE_2D, 0, G.RGBA, dTex.alpha.w, dTex.alpha.h, 0, G.RGBA, G.UNSIGNED_BYTE, arr);
  G.texParameteri(G.TEXTURE_2D, G.TEXTURE_WRAP_S, G.REPEAT);
  G.texParameteri(G.TEXTURE_2D, G.TEXTURE_WRAP_T, G.REPEAT);
  G.texParameteri(G.TEXTURE_2D, G.TEXTURE_MIN_FILTER, G.NEAREST);
  G.texParameteri(G.TEXTURE_2D, G.TEXTURE_MAG_FILTER, G.NEAREST);
  alphaTexCache.set(key, at);
  return at;
}
const SHADERS_Z = {
  LightMapDC: [LIGHTMAPDC_V, LIGHTMAPDC_F],
  AlphaMasking: [ALPHAMASKING_V, ALPHAMASKING_F],
  SimpleAdditive: [NVGLASS_V, NVGLASS_F],
  StandardDiffuseDC: [NVGLASS_V, NVGLASS_F],
  other: [NVGLASS_V, NVGLASS_F],
};
const DEFS_Z = {
  LightMapDC: '',
  AlphaMasking: '#define TDKR_SPLIT_ALPHA\n',
  SimpleAdditive: '',
  StandardDiffuseDC: '',
  other: '',
};
const IDENT4 = new Float32Array([1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]);
// ---- s52 T5: engine fog + ColorCorrection LUT in the zone path (off by default; gate digests unchanged) ----
const QS2 = new URLSearchParams(location.search);
const FOGENG = QS2.get('fog') === '1';   // ComputeFogFS with shipped values: FogColor RGBA(64,102,119,160), start 0, end 140, y = 1/(start-end)
const LUTON = QS2.get('lut') === '1';    // ColorCorrection 000_default.tga (RGB565 512x16, commons_tex.gla) post pass
const CAMH = 60.0;                        // top-down camera height anchor: view depth = CAMH - h
// s53 T1: draw-time texture-unit audit (?unitaudit=1) — asserts unit0 == diffuse, unit1 == lightmap on EVERY zone draw
const UAUD = QS2.get('unitaudit') === '1';
const UA = { n: 0, mm: 0, noTex: 0, mmFirst: [], u0: null, u1: null };
// ---- s53 T5: minimal glide + grapple slice (?s5=1) — data sources in extraction/re/session53/s53_t5_design.md
// Engine anchors: PlayerComponent::EnterGlideFromGrapnel (state 7 guard), SetActorSpeedGlide,
// clips _089_grapnel_pull / _057_glide_idle / _065_glide_idle_to_run (s35 battery idx 91/55/63).
// s54 T1: parameters DECODED from the engine data (extraction/re/session54/):
//  CComponentGlide (class 0x0110ce1f, Load = ReadInt + 21xReadFloat + ReadInt, ARM) template
//  'Glider' (0x2674, gadget slot 0) gol.bin payload, consumed via CGadgetManager::GetGlide:
//   f0=4, f1=16: AIRSPEED ACCUMULATOR CLAMPS u/s (s57 T1 decision; rate = f0+(f1-f0)*(2/pi)*|p|),
//   f2=14, f3=4 (unread), f4 unattributed (the 0x3836e4 read is the ACTOR pitch), f5=1, f6=6
//   (base vertical sink + slope; f6 ALSO the 6-deg side-slip of the horizontal direction),
//   f7=0, f8=2 (ground-proximity blend target within f9=16 u), f10=-45 (initial glide pitch DEG,
//   SetInitialGlideAngle; engine hard default -30; Glider_Plunge slot 1: -60),
//   f11..f20 = -60,30,35,1.25,0.05,45,0.5,30,30,40 (pitch/roll/yaw clamp+rate family),
//   int2=600 (both templates). Named statics (.data): k_glideWallEvadeDistance 6,
//   k_glideWallEvadeMinDistance 1, k_glideWallEvadeMaxAngle 10, s_fallAheadOffset 0.4.
// Legacy placeholders (?s5legacy=1): fwd 18, gravity -25, bank 0.35 rad fixed.
// s57 T1 DECISION (round 47): the ACCUMULATOR model IS the engine model - default for ?s5=1.
//  Evidence (ARM libKRHP.so, this session):
//   (a) RefreshForcesGlide 0x3836b0..0x383a08: rate s10 = f0+(f1-f0)*(2/pi)*|p| feeds ONLY the
//       guarded integration of [actor+0x53c] (grow p<=0 @0x3839dc vmlagt/vstrgt, decay p>0 @0x383724
//       vmlsmi/vstrmi, both xdt=[actor+0x2a8]); output velocity 0x383858..0x383880:
//       X=-sin(f6deg)*acc*cos(p)*dt, Y=cos(f6deg)*acc*cos(p)*dt, Z=(sin(p)*acc - (f5+(f6-f5)(2/pi)|p|
//       + GetGliderGravityHelper()) - blend)*dt. The f5/f6 formula appears ONLY in Z; the s55 note
//       had the two families swapped (and helper into FORWARD speed - byte-refuted: vadd into Z @0x383784).
//   (b) acc writers census (whole .text, direct+computed bases): StartGlide 0x3806a8 acc=f1=16
//       (ldr ip,[comp+0xc]; str [actor+0x53c]); StartGlideFromGrapnel 0x380b80+0x380c48 acc=f1=16;
//       UpdateNavGlide 0x381bc0 acc=|velocity @actor+0x224| (momentum seed); readers: RefreshForcesGlide
//       (post-update s22 @0x38379c) + UpdateNavGlide 0x381c5c. No other readers/writers exist.
//   (c) plausibility: acc model fwd = acc*cos(p) in [4,15.9] u/s (faster than a run; glide angle
//       52.8 deg at -45); s55-note model predicts CONSTANT fwd 3.5 u/s (slower than a run) and a
//       ~70 deg dive identical for Glider and Plunge - and has no role for the integrated accumulator.
//  ?s5=1        ACCUMULATOR (engine): acc seeded f1=16 (StartGlide byte-proof), pitch held at f10
//               (-45 Glider / -60 Plunge via ?s5plunge=1); per-frame: rate = f0+(f1-f0)*(2/pi)*|p|,
//               acc += rate*dt (p<=0, clamp f1) / acc -= rate*dt (p>0, clamp f0);
//               fwd = acc*cos(p), vz = acc*sin(p) - s56(f5,f6) - blend(f7,f8,f9).
//  ?s5sink=1    s55-note model (MISREAD, kept as control): fwd = f5+(f6-f5)*(2/pi)*|p|,
//               sink = f0+(f1-f0)*(2/pi)*|p|.
//  ?s5acc=1     alias of the default (kept for s56 receipt comparability).
//  ?s5old=1     pre-s56 staged model (const fwd 16, sink 4+12*|p| without 2/pi) - control.
//  ?s5legacy=1  s53 placeholders (unchanged).
//  s58 T1 BLEND PINNED from the engine (RefreshForcesGlide 0x383788..0x383804):
//   the virtual call is [comp+4]->vtable[+0x18] = CGameObject::GetPosition (slot 6; vtable base
//   0xbd8028; GetPosition @0x2d6f1c 'add r0,r0,#0xc' = &obj->pos). NOT a ground raycast/nav query.
//   d = |GetPosition(obj) - [comp+0x1a4..0x1ac]| where the vec3 cache is stored right after every
//   SetActorPosition (Update 0x36e74c, ground-nav updates, TryEdgeGrab, UpdateFloorTesting,
//   ResolveAirCollision) and NEVER by UpdateNavGlide (0x380e94..0x3813bc: 0 stores) -> during a
//   glide it is frozen at the TAKEOFF position: d = distance travelled since glide start.
//   blend_raw = fB + (1 - d/f9)*(f7 - fB); blend = max(blend_raw, fB) [0x3837d4/ec,0x383804];
//   vz -= blend [0x383814]. Gadget floats: fB=[+0x24] floor, f7=[+0x28] start, f9=[+0x2c] range.
//   ?s5=1 keeps the s56/s57 DECLARED PROXY (height over nm) for digest stability;
//   ?s5blend=1 runs the exact engine measure (takeoff-anchor distance, same closed form).
//   GetGliderGravityHelper 0x1e1508 = UpgradesManager::map[0x1f].SUpgrade+0xc (operator[] default
//   insert; base value data-driven from the ResetUpgrades definition tables, no .text constant;
//   in-page 0 = no upgrades, additive into the vertical rate at 0x383784).
// s56 T2 (?s5ctl=1, engine mode only): scripted pitch control + auto-level.
//  PROVENANCE: pitch mapping f10/sink/speed = decoded; pitch CLAMPS and auto-level coefficient are
//  NOT engine-decoded (s_glide* dead, f12/f16/f17/f19 unread, UpdateNavGlide = nav steering only)
//  - the sequence validates the CONTROL MECHANISM against exact analytic outcomes, and the
//  f6=6-deg side-slip (decoded) is exercised. Scripted: ramp -45->-60 by 0.4s, HOLD -60 in
//  [0.4,1.2) (sink 12.0 / fwd 4.333 exact), then pitch(t) = -60*exp(-2.0*(t-1.2)) (placeholder k=2/s).
const S5ON = QS2.get('s5') === '1';
const S5LEG = QS2.get('s5legacy') === '1';
const S5OLD = QS2.get('s5old') === '1';        // s56 T1 control
const S5ACC = QS2.get('s5acc') === '1';        // s57: alias of the default (accumulator)
const S5SINK = QS2.get('s5sink') === '1';      // s57 T1: s55-note model kept as control
const S5PLUNGE = QS2.get('s5plunge') === '1';  // s56 T1: GetGlide(1) 'Glider_Plunge'
const S5CTL = QS2.get('s5ctl') === '1';        // s56 T2: scripted pitch control + auto-level
const S5EARLY = QS2.get('s5ctlEarly') === '1'; // s56 T2b: early release so the decay precedes landing
const S5BLEND = QS2.get('s5blend') === '1';    // s58 T1: exact engine blend (takeoff-anchor distance)
const S5REAN = QS2.get('s5reanchor') === '1';  // s60 T5: ResolveAirCollision re-anchor case (virtual wall)
const S5WALL = parseFloat(QS2.get('s5wall') || '40');
const S5CTLV = S5EARLY
  ? { tRamp: 0.25, tHold: 0.45, diveDeg: -60.0, k: 2.0, slipDeg: 6.0, rampFromDeg: -45.0 }
  : { tRamp: 0.4, tHold: 1.2, diveDeg: -60.0, k: 2.0, slipDeg: 6.0, rampFromDeg: -45.0 };
const S5TWO_PI = 2 / Math.PI;                  // engine pool 0.6366198 @0x3839f8
const S5P = S5LEG
  ? { mode: 'legacy', fwd: 18.0, pitch0Deg: -30.0, sinkMin: 4.0, sinkMax: 16.0, bank: 0.35 }
  : S5OLD
  ? { mode: 'old', fwd: 16.0, pitch0Deg: -45.0, sinkMin: 4.0, sinkMax: 16.0, bank: 0.35 }
  : { mode: S5SINK ? 'sink56' : 'acc', fwd: 16.0,   // s57 T1: accumulator = engine default
      pitch0Deg: S5PLUNGE ? -60.0 : -45.0,     // f10: Glider -45 / Glider_Plunge -60
      sinkMin: 4.0, sinkMax: 16.0,             // f0, f1
      fwdMin: 1.0, fwdMax: 6.0,                // f5, f6
      blendMin: 0.0, blendMax: 2.0, blendDist: 16.0,   // f7, f8, f9
      bank: 0.35 };
function s5Sink56(pitch) {  // f5/f6 family: f5+(f6-f5)*(2/pi)*|pitch| (upgrade helper 0 - no upgrades)
  return S5P.fwdMin + (S5P.fwdMax - S5P.fwdMin) * S5TWO_PI * Math.abs(pitch);
}
function s5Rate(pitch) {    // f0/f1 family: f0+(f1-f0)*(2/pi)*|pitch| (sink in s55 note / accel rate in acc re-read)
  return S5P.sinkMin + (S5P.sinkMax - S5P.sinkMin) * S5TWO_PI * Math.abs(pitch);
}
const S5 = { phase: 'off', t0: 0, tGlide: 0, from: null, tgt: null, dur: 1200, vz: 0,
             reached: false, reachDist: null, clipActive: false, landed: false,
             landMs: null, started: false, done: false, bank: 0.35,
             fwd: 0.0, acc: 0.0, pitch: 0, baseHead: 0 };
function s5PickEdge() {
  // s54 T2: prefer REAL CWayPointObject anchors (decoded from YOUR lvc);
  // the portal-edge BFS below stays as fallback when no waypoint qualifies.
  const WPS = window.__S5WPS;
  if (WPS && WPS.length) {
    let bw = null, bwScore = -1e9;
    for (const w of WPS) {
      const d = Math.hypot(w.x - P.x, w.y - P.y);
      if (d < 14 || d > 80 || Math.abs(w.z - P.z) >= 14) continue;
      if (nm_ground(w.x, w.y, w.z + 2.6) <= -1e8) continue;   // slice keeps walkable-only targets
      const score = (w.z - P.z) * 10 - d;                      // elevated anchor first (engine ledge grapple)
      if (score > bwScore) { bwScore = score; bw = [w.x, w.y, w.z]; }
    }
    if (bw) return bw;
  }
  // find the current cell: nearest cell center within 10 u (2D)
  let cu = -1, cd = 1e9;
  for (let i = 0; i < nmCent.length / 3; i++) {
    const dx = nmCent[i * 3] - P.x, dy = nmCent[i * 3 + 1] - P.y;
    const d2 = dx * dx + dy * dy;
    if (d2 < cd) { cd = d2; cu = i; }
  }
  if (cu < 0 || cd > 100) return null;
  // BFS out to ~80 u: every visited (cell, neighbor) portal edge midpoint is a candidate
  // ("a grapple to a decoded edge" - real CNavMeshNova portals: shared 2-vertex cell edges)
  const seen = new Set([cu]);
  const ring = [cu];
  let best = null, bestD = 1e9, bestScore = -1e9;
  for (let depth = 0; depth < 10 && ring.length; depth++) {
    const nxt = [];
    for (const u of ring) {
      for (let ni = NBS_OFF[u]; ni < NBS_OFF[u + 1]; ni++) {
        const v = NBS_ARR[ni];
        if (!seen.has(v)) { seen.add(v); nxt.push(v); }
        const a = [nmCells[u * 7], nmCells[u * 7 + 1], nmCells[u * 7 + 2]];
        const b = [nmCells[v * 7], nmCells[v * 7 + 1], nmCells[v * 7 + 2]];
        const sh = a.filter(x => b.indexOf(x) >= 0);
        if (sh.length !== 2) continue;
        const mx = (nmV[sh[0] * 3] + nmV[sh[1] * 3]) / 2, my = (nmV[sh[0] * 3 + 1] + nmV[sh[1] * 3 + 1]) / 2,
              mz = (nmV[sh[0] * 3 + 2] + nmV[sh[1] * 3 + 2]) / 2;
        const d = Math.hypot(mx - P.x, my - P.y);
        if (d >= 14 && d <= 80 && Math.abs(mz - P.z) < 14 &&
            nm_ground(mx, my, mz + 2.6) > -1e8) {
          // s54 T1: prefer an ELEVATED anchor (engine grapples UP to a ledge, glides down);
          // score = height above the walker first, distance second
          const score = (mz - P.z) * 10 - d;
          if (best === null || score > bestScore) { bestScore = score; best = [mx, my, mz]; }
        }
      }
    }
    ring.length = 0; for (const w of nxt) ring.push(w);
    if (best && depth >= 2) break;   // near candidates first
  }
  return best;
}
function s5SetClip(name) {
  if (!mixer) return;
  for (const k of ['_001_idle_stand', '_007_walk', '_008_run', '_089_grapnel_pull', '_057_glide_idle', '_065_glide_idle_to_run']) {
    const a = actions[k];
    if (!a) continue;
    a.setEffectiveWeight(k === name ? 1 : 0);
    if (k === name) { a.reset(); a.play(); }
  }
}
function s5Begin() {
  S5.started = true;
  const tgt = s5PickEdge();
  if (!tgt) { S5.phase = 'done'; S5.done = true;
    window.__GATE.s5 = { enabled: true, error: 'no edge in range' };
    startWalkPhase(); return; }
  S5.from = [P.x, P.y, P.z];
  S5.tgt = tgt; S5.t0 = performance.now();
  S5.phase = 'grapnel';
  s5SetClip('_089_grapnel_pull');
  log('S5 grapple: portal-edge midpoint ' + tgt.map(v => v.toFixed(1)).join(',') +
      ' dist ' + Math.hypot(tgt[0] - P.x, tgt[1] - P.y).toFixed(1) + ' u');
}
function s5Tick(now) {
  const g = window.__GATE;
  if (S5.phase === 'grapnel') {
    const t = Math.min(1, (now - S5.t0) / S5.dur);
    const e = t * t;   // ease-in pull (rope-constrained lerp)
    P.x = S5.from[0] + (S5.tgt[0] - S5.from[0]) * e;
    P.y = S5.from[1] + (S5.tgt[1] - S5.from[1]) * e;
    P.z = S5.from[2] + (S5.tgt[2] - S5.from[2]) * e + 1.2 * Math.sin(Math.PI * e);
    if (batman) batman.rotation.y = Math.atan2(-(S5.tgt[0] - S5.from[0]), -(S5.tgt[1] - S5.from[1])) + Math.PI;
    if (t >= 1) {
      S5.reachDist = Math.hypot(P.x - S5.tgt[0], P.y - S5.tgt[1]);
      S5.reached = S5.reachDist <= 2.5;
      S5.phase = 'glide'; S5.t0 = now; S5.tGlide = now;
      // s54 T1: the grapple ends AT the anchor (ledge) - stand on its surface, then glide
      const gz0 = nm_ground(S5.tgt[0], S5.tgt[1], S5.tgt[2] + 2.6);
      if (gz0 > -1e8) { P.z = gz0 + 0.9; }
      S5.pitch = S5P.pitch0Deg * Math.PI / 180;   // engine initial glide pitch (f10, SetInitialGlideAngle)
      S5.acc = S5P.sinkMax;   // s57 T1: engine StartGlide seeds acc = f1 = 16 (0x3806a8)
      if (S5P.mode === 'acc') S5.anchor = [P.x, P.y, P.z];   // s58 T1: engine blend anchor = takeoff pos
      if (S5REAN) { S5.reanchors = []; S5.wallHit = null; }  // s60 T5: collision-case receipt
      S5.baseHead = Math.atan2(S5.tgt[1] - S5.from[1], S5.tgt[0] - S5.from[0]);   // s56 T2 slip reference
      S5.vz = S5P.mode === 'legacy' ? 2.0
            : S5P.mode === 'old' ? -(S5P.sinkMin + (S5P.sinkMax - S5P.sinkMin) * Math.abs(S5.pitch))
            : S5P.mode === 'acc' ? (S5.acc * Math.sin(S5.pitch) - s5Sink56(S5.pitch))
            : -s5Rate(S5.pitch);
      // acc (ENGINE default, s57) at -45 deg, acc=f1=16: vz = 16*(-0.7071) - 3.5 = -14.81 u/s, fwd = 16*cos(-45) = 11.31
      // sink56 (s55-note control) at -45 deg: sink = 4 + 12*(2/pi)*0.7854 = 10.0 u/s, fwd = 1 + 5*(2/pi)*0.7854 = 3.5 u/s
      // legacy model: small rise then gravity -25 u/s^2
      s5SetClip('_057_glide_idle');
    }
  } else if (S5.phase === 'glide') {
    const dt2 = Math.min(0.1, (now - S5.t0) / 1000) || 0.016;
    S5.t0 = now;
    const dx = S5.tgt[0] - S5.from[0], dy = S5.tgt[1] - S5.from[1];
    const dl = Math.hypot(dx, dy) || 1;
    // s56 T2: scripted pitch control (engine mode only) - see header comment for provenance
    if (S5CTL && S5P.mode === 'acc') {
      const tG = (now - S5.tGlide) / 1000;
      let tgtDeg;
      if (tG < S5CTLV.tRamp) {
        tgtDeg = S5CTLV.rampFromDeg + (S5CTLV.diveDeg - S5CTLV.rampFromDeg) * (tG / S5CTLV.tRamp);
        S5.pitch = tgtDeg * Math.PI / 180;                     // linear ramp, exact
      } else if (tG < S5CTLV.tHold) {
        S5.pitch = S5CTLV.diveDeg * Math.PI / 180;             // hard hold, exact
      } else {
        S5.pitch = S5CTLV.diveDeg * Math.PI / 180 * Math.exp(-S5CTLV.k * (tG - S5CTLV.tHold));  // auto-level
      }
    }
    // s56 T1 model switch (see header comment); s54 wall-evade analogue kept for all models
    if (S5P.mode === 'acc') {
      const rate = s5Rate(S5.pitch);
      if (S5.pitch <= 0) { if (S5.acc < S5P.sinkMax) S5.acc = Math.min(S5P.sinkMax, S5.acc + rate * dt2); }
      else if (S5.acc > S5P.sinkMin) { S5.acc = Math.max(S5P.sinkMin, S5.acc - rate * dt2); }
      let blendD;
      if (S5BLEND && S5.anchor) {            // s58 T1: ENGINE measure - dist from takeoff anchor
        blendD = Math.hypot(P.x - S5.anchor[0], P.y - S5.anchor[1], P.z - S5.anchor[2]);
      } else {                               // s56/s57 declared proxy: height over navmesh
        const gzh = nm_ground(P.x, P.y, P.z + 2.6);
        blendD = (gzh > -1e8) ? Math.max(0, P.z - 0.9 - gzh) : 1e9;
      }
      // engine: blend_raw = fB + (1 - d/f9)*(f7 - fB); blend = max(blend_raw, fB) [0x3837d4..0x383804]
      const blend = Math.max(S5P.blendMin,
        S5P.blendMin + (1 - blendD / S5P.blendDist) * (S5P.blendMax - S5P.blendMin));
      S5.blendD = blendD; S5.blendV = blend;
      S5.vz = S5.acc * Math.sin(S5.pitch) - s5Sink56(S5.pitch) - blend;
      S5.fwd = S5.acc * Math.cos(S5.pitch);
    } else if (S5P.mode === 'sink56') {
      S5.fwd = s5Sink56(S5.pitch);
      S5.vz = -s5Rate(S5.pitch);
    } else if (S5P.mode === 'old') {
      S5.fwd = S5P.fwd;
      S5.vz = -(S5P.sinkMin + (S5P.sinkMax - S5P.sinkMin) * Math.abs(S5.pitch));
    } else { S5.vz += -25.0 * dt2; S5.fwd = S5P.fwd; }   // legacy
    // s54 T1: engine k_glideWallEvade analogue - never step forward into void;
    // hold position laterally and keep descending (nm corridor of the decoded region)
    let sdx = dx, sdy = dy;
    if (S5CTL && S5P.mode === 'acc') {   // s56 T2: decoded f6 side-slip (RefreshForcesGlide 0x383824..38)
      const sl = -S5CTLV.slipDeg * Math.PI / 180, cs = Math.cos(sl), sn = Math.sin(sl);
      sdx = dx * cs - dy * sn; sdy = dx * sn + dy * cs;
    }
    let gx = P.x + sdx / dl * S5.fwd * dt2, gy = P.y + sdy / dl * S5.fwd * dt2;
    if (nm_ground(gx, gy, P.z + 2.6) <= -1e8) { gx = P.x; gy = P.y; }
    if (S5REAN && S5.anchor && S5.wallHit === null) {
      // s60 T5: virtual wall at S5WALL u from the TAKEOFF anchor along the heading
      const ax = P.x - S5.anchor[0], ay = P.y - S5.anchor[1];
      const dBefore = Math.hypot(ax, ay);
      const nx = gx - S5.anchor[0], ny = gy - S5.anchor[1];
      const dAfter = Math.hypot(nx, ny);
      if (dAfter >= S5WALL && dBefore < S5WALL) {
        // ResolveAirCollision analogue: clamp the horizontal step at the wall plane,
        // then store the RESOLVED position into the cache (0x398570 -> 0x3987a4/74)
        const f = (S5WALL - dBefore) / Math.max(1e-9, dAfter - dBefore);
        gx = P.x + (gx - P.x) * f; gy = P.y + (gy - P.y) * f;
        S5.anchor = [gx, gy, P.z];            // RE-ANCHOR at the resolved position
        S5.wallHit = { tMs: Math.round(now - S5.tGlide), pos: [+gx.toFixed(3), +gy.toFixed(3)] };
        if (!S5.reanchors) S5.reanchors = [];
        S5.reanchors.push(S5.wallHit);
        log('s5 re-anchor: wall at ' + S5WALL + ' u, anchor reset @' + S5.wallHit.tMs + ' ms');
      }
    }
    const nz = P.z + S5.vz * dt2;
    const gz = nm_ground(gx, gy, nz + 2.6);
    P.x = gx; P.y = gy; P.z = nz;
    // s54 T1: in-page trajectory record (alt-lost-per-metre comparison, gate-visible)
    if (!S5.traj) S5.traj = [];
    if (S5.traj.length === 0 || now - S5.traj[S5.traj.length - 1].t >= 200) {
      S5.traj.push({ t: Math.round(now - S5.tGlide), x: +P.x.toFixed(2), y: +P.y.toFixed(2),
                     z: +P.z.toFixed(2), vz: +S5.vz.toFixed(2), fwd: +(S5.fwd || 0).toFixed(3),
                     acc: S5P.mode === 'acc' ? +S5.acc.toFixed(3) : undefined,
                     pitch: +(S5.pitch * 180 / Math.PI).toFixed(2),
                     head: +((Math.atan2(sdy, sdx) - S5.baseHead) * 180 / Math.PI).toFixed(2),
                     gz: (gz > -1e8) ? +gz.toFixed(2) : null,
                     blendD: S5P.mode === 'acc' ? +(S5.blendD || 0).toFixed(3) : undefined,
                     blend: S5P.mode === 'acc' ? +(S5.blendV || 0).toFixed(3) : undefined });
    }
    window.__GATE.s5live = { phase: S5.phase, model: S5P.mode, vz: +S5.vz.toFixed(2),
                             fwd: +(S5.fwd || 0).toFixed(3), z: +P.z.toFixed(2),
                             gz: (gz > -1e8) ? +gz.toFixed(2) : null, ms: Math.round(now - S5.tGlide),
                             blendD: S5P.mode === 'acc' ? +(S5.blendD || 0).toFixed(3) : undefined,
                             blendV: S5P.mode === 'acc' ? +(S5.blendV || 0).toFixed(3) : undefined };
    if (batman) { batman.rotation.y = Math.atan2(-dx, -dy) + Math.PI; batman.rotation.z = S5.bank; }
    const glA = actions['_057_glide_idle'];
    S5.clipActive = !!(glA && glA.getEffectiveWeight() > 0.5 && glA.time > 0.05);   // clip actually sampled
    if (gz > -1e8 && nz - 0.9 <= gz + 0.05) {
      // ground contact: clamp to the surface; finish the landing after the 400 ms
      // min-airtime window so the glide clip is genuinely sampled (gate fidelity)
      P.z = gz + 0.9;
      if (now - S5.tGlide > 400) {
        S5.landed = true; S5.landMs = Math.round(now - S5.tGlide);
        S5.phase = 'done'; S5.done = true;
        if (batman) batman.rotation.z = 0;
        s5SetClip('_065_glide_idle_to_run');   // s54 T3: state table Grapnel_Horizontal_To_Glide_Idle -> _065 (667 ms), then run
        setTimeout(function () { if (S5.phase === 'done') s5SetClip('_008_run'); }, 450);
        g.s5 = { enabled: true, model: S5P.mode, ctl: !!S5CTL, targetReached: S5.reached, reachDist: S5.reachDist === null ? null : Math.round(S5.reachDist * 100) / 100,
                 glideClipActive: S5.clipActive, landed: true, landMs: S5.landMs, traj: S5.traj,
                 reanchors: S5.reanchors || [], wallHit: S5.wallHit };
        log('S5 landed: ground z ' + gz.toFixed(2) + ', glide lasted ' + S5.landMs + ' ms');
        startWalkPhase();   // hand back to the standard gate walk phase
      }
    }
    if (now - S5.tGlide > 6000 && !S5.landed) {   // safety: never stall the gate
      g.s5 = { enabled: true, model: S5P.mode, targetReached: S5.reached, reachDist: S5.reachDist,
               glideClipActive: S5.clipActive, landed: false, error: 'glide timeout', traj: S5.traj };
      S5.phase = 'done'; S5.done = true;
      startWalkPhase();
    }
  }
}
const FOG_WVT = (() => { const a = new Float32Array([1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]);
  a[8] = 0; a[9] = 0; a[10] = -1; a[11] = CAMH; return a; })();  // col2 -> dot = CAMH - h
let lutTex = null, lutFBO = null, lutSceneTex = null, lutPost = null;

/* follow camera: top-down ortho centered on the capsule, height = depth.
 * Same math family as city_zone2 (pixel-space ortho; s50 T1: depth window [-100,+250], clip_z = -2h/350 + 150/350 — the old 1-h/200 clipped all h<0 water/shore). */
const VIEWW = 240, VIEWH = 240 * H / W;
function camWVP(cx, cz) {
  return new Float32Array([
    2 / VIEWW, 0, 0, 0,
    0, -2 / VIEWH, 0, 0,
    0, 0, -2 / 350, 0,
    -2 * cx / VIEWW, 2 * cz / VIEWH, 150 / 350, 1,
  ]);
}

function drawZone(batches, wvp) {
  const usePost = LUTON && lutTex;   // s52 T5: scene -> FBO -> LUT quad -> screen
  G.viewport(0, 0, W, H);
  G.clearColor(0, 0, 0, 0);
  if (usePost) { ensureLutPost(); G.bindFramebuffer(G.FRAMEBUFFER, lutFBO); }
  G.clear(G.COLOR_BUFFER_BIT | G.DEPTH_BUFFER_BIT);
  G.enable(G.DEPTH_TEST);
  G.depthFunc(G.LEQUAL);
  G.disable(G.CULL_FACE);
  let tris = 0, draws = 0;
  for (const b of batches) {
    const [vsrc, fsrc] = SHADERS_Z[b.fx] || SHADERS_Z.other;
    const P = getProgZ(b.fx + '|' + DEFS_Z[b.fx], DEFS_Z[b.fx] + vsrc, DEFS_Z[b.fx] + fsrc);
    G.useProgram(P.p);
    if (P.uni.WorldViewProjection) G.uniformMatrix4fv(P.uni.WorldViewProjection, false, wvp);
    if (P.uni.WorldViewProjectionMatrix) G.uniformMatrix4fv(P.uni.WorldViewProjectionMatrix, false, wvp);
    const so = [1, 1, 0, 0];
    for (const nm of ['Coord0_scaleoffset', 'Coord1_scaleoffset', 'TexCoord0_scaleoffset',
                      'TexCoord1_scaleoffset'])
      if (P.uni[nm]) G.uniform4fv(P.uni[nm], so);
    if (P.uni.LightMapAtlas) G.uniform4fv(P.uni.LightMapAtlas, [1, 1, 0, 0]);
    if (P.uni.Overbright) G.uniform1f(P.uni.Overbright, 1.0);
    if (P.uni.uvOffset) G.uniform2f(P.uni.uvOffset, 0, 0);
    if (P.uni.Ambient) G.uniform4f(P.uni.Ambient, 0, 0, 0, 1);
    if (P.uni.FogColor) { if (FOGENG) G.uniform4f(P.uni.FogColor, 64/255, 102/255, 119/255, 160/255); else G.uniform4f(P.uni.FogColor, 64/255, 102/255, 119/255, 0); }
    if (P.uni.FogStartEnd) G.uniform2f(P.uni.FogStartEnd, 0, FOGENG ? -1/140 : 1/140);
    if (P.uni.WorldViewTransposed) G.uniformMatrix4fv(P.uni.WorldViewTransposed, false, FOGENG ? FOG_WVT : IDENT4);
    function bindA(name, buf, size) {
      if (P.attr[name] === undefined || P.attr[name] < 0) return;
      G.bindBuffer(G.ARRAY_BUFFER, buf);
      G.enableVertexAttribArray(P.attr[name]);
      G.vertexAttribPointer(P.attr[name], size, G.FLOAT, false, 0, 0);
    }
    bindA('Position', b.posBuf, 4);
    bindA('Normal', b.posBuf, 4);
    bindA('Coord0', b.uv0Buf, 2);
    bindA('TexCoord0', b.uv0Buf, 2);
    if (b.uv1Buf) { bindA('Coord1', b.uv1Buf, 2); bindA('TexCoord1', b.uv1Buf, 2); }
    if (b.c0Buf) { bindA('Color', b.c0Buf, 4); bindA('Color0', b.c0Buf, 4); }
    let unit = 0;
    if (UAUD) { UA.n++; UA.u0 = null; UA.u1 = null; }   // s53 T1 per-draw unit audit
    if (b.dTex && P.uni.DiffuseMap !== undefined && P.uni.DiffuseMap) {
      G.activeTexture(G.TEXTURE0); G.bindTexture(G.TEXTURE_2D, b.dTex.tx);
      if (UAUD) UA.u0 = b.dTex.name || null;
      G.uniform1i(P.uni.DiffuseMap, 0); unit = 1;
    } else if (b.dTex && P.uni.DiffuseTextureSampler) {
      G.activeTexture(G.TEXTURE0); G.bindTexture(G.TEXTURE_2D, b.dTex.tx);
      if (UAUD) UA.u0 = b.dTex.name || null;
      G.uniform1i(P.uni.DiffuseTextureSampler, 0); unit = 1;
    }
    if ((b.fx === 'LightMapDC' || b.fx === 'AlphaMasking') && b.lmTex) {
      if (P.uni.LightMap) { G.activeTexture(G.TEXTURE1); G.bindTexture(G.TEXTURE_2D, b.lmTex.tx); G.uniform1i(P.uni.LightMap, 1); }
      else if (P.uni.LightmapTextureSampler) { G.activeTexture(G.TEXTURE1); G.bindTexture(G.TEXTURE_2D, b.lmTex.tx); G.uniform1i(P.uni.LightmapTextureSampler, 1); }
      if (UAUD) UA.u1 = b.lmTex.name || null;
    }
    if (UAUD) {   // s53 T1: assert unit0 == the batch's diffuse, unit1 == its lightmap
      const exp0 = b.dTex ? (b.dTex.name || null) : null;
      const isLMA = (b.fx === 'LightMapDC' || b.fx === 'AlphaMasking');
      const exp1 = (isLMA && b.lmTex) ? (b.lmTex.name || null) : null;
      if (exp0 === null) { UA.noTex++; }
      else {
        if (UA.u0 !== exp0) { UA.mm++; if (UA.mmFirst.length < 8) UA.mmFirst.push({ mid: b.mid, fx: b.fx, exp0: exp0, u0: UA.u0, exp1: exp1, u1: UA.u1 }); }
        if (exp1 !== null && UA.u1 !== exp1) { UA.mm++; if (UA.mmFirst.length < 8) UA.mmFirst.push({ mid: b.mid, fx: b.fx, exp0: exp0, u0: UA.u0, exp1: exp1, u1: UA.u1 }); }
      }
      window.__GATE.unit_audit = { draws: UA.n, mismatches: UA.mm, noTex: UA.noTex, first: UA.mmFirst };
    }
    if (b.fx === 'AlphaMasking' && b.alphaTx && P.uni.DiffuseMap_alpha) {
      G.activeTexture(G.TEXTURE2); G.bindTexture(G.TEXTURE_2D, b.alphaTx);
      G.uniform1i(P.uni.DiffuseMap_alpha, 2);
    }
    if (!b.c0Buf && (P.attr.Color !== undefined || P.attr.Color0 !== undefined)) {
      const loc = (P.attr.Color !== undefined && P.attr.Color >= 0) ? P.attr.Color : P.attr.Color0;
      if (loc !== undefined && loc >= 0) {
        G.disableVertexAttribArray(loc);
        G.vertexAttrib4f(loc, 1, 1, 1, 1);
      }
    }
    G.bindBuffer(G.ELEMENT_ARRAY_BUFFER, b.idxBuf);
    G.drawElements(G.TRIANGLES, b.nidx, b.use32 ? G.UNSIGNED_INT : G.UNSIGNED_SHORT, 0);
    tris += b.nidx / 3; draws++;
  }
  if (usePost) { G.bindFramebuffer(G.FRAMEBUFFER, null); lutDrawPass(); }
  return { tris, draws, lut: usePost };
}

// s52 T5: ColorCorrection post pass (viewer parity). The scene renders INTO lutFBO (RGBA texture
// + DEPTH_COMPONENT16 renderbuffer), then a fullscreen quad applies the engine CCFS LUT mapping
// (u = r*cell*0.9375 + 0.03125*cell + floor(b*31.9999)*cell, v = g) to the default framebuffer.
function ensureLutPost() {
  if (lutPost) return;
  const vs = 'attribute vec2 p; varying vec2 t; void main(){ t = p*0.5+0.5; gl_Position = vec4(p,0.0,1.0); }';
  const fs = 'precision mediump float; uniform sampler2D sc; uniform sampler2D lut; varying vec2 t;\n' +
    'void main(){ vec4 c = texture2D(sc, t); float cell = 1.0/32.0;\n' +
    ' float u = c.r * cell * 0.9375 + 0.03125 * cell + floor(c.b * 31.9999) * cell; float v = c.g;\n' +
    ' gl_FragColor = vec4(texture2D(lut, vec2(u, v)).rgb, c.a); }';
  const mk = (ty, src) => { const s = G.createShader(ty); G.shaderSource(s, src); G.compileShader(s);
    if (!G.getShaderParameter(s, G.COMPILE_STATUS)) throw new Error('lutpost: ' + G.getShaderInfoLog(s)); return s; };
  const pr = G.createProgram(); G.attachShader(pr, mk(G.VERTEX_SHADER, vs)); G.attachShader(pr, mk(G.FRAGMENT_SHADER, fs));
  G.linkProgram(pr);
  const qb = G.createBuffer(); G.bindBuffer(G.ARRAY_BUFFER, qb);
  G.bufferData(G.ARRAY_BUFFER, new Float32Array([-1,-1, 1,-1, -1,1, 1,-1, 1,1, -1,1]), G.STATIC_DRAW);
  lutPost = { pr, qb, loc_p: G.getAttribLocation(pr, 'p'), loc_sc: G.getUniformLocation(pr, 'sc'), loc_lut: G.getUniformLocation(pr, 'lut') };
  lutSceneTex = G.createTexture(); G.bindTexture(G.TEXTURE_2D, lutSceneTex);
  G.texImage2D(G.TEXTURE_2D, 0, G.RGBA, W, H, 0, G.RGBA, G.UNSIGNED_BYTE, null);
  G.texParameteri(G.TEXTURE_2D, G.TEXTURE_MIN_FILTER, G.NEAREST); G.texParameteri(G.TEXTURE_2D, G.TEXTURE_MAG_FILTER, G.NEAREST);
  G.texParameteri(G.TEXTURE_2D, G.TEXTURE_WRAP_S, G.CLAMP_TO_EDGE); G.texParameteri(G.TEXTURE_2D, G.TEXTURE_WRAP_T, G.CLAMP_TO_EDGE);
  const rb = G.createRenderbuffer(); G.bindRenderbuffer(G.RENDERBUFFER, rb);
  G.renderbufferStorage(G.RENDERBUFFER, G.DEPTH_COMPONENT16, W, H);
  lutFBO = G.createFramebuffer(); G.bindFramebuffer(G.FRAMEBUFFER, lutFBO);
  G.framebufferTexture2D(G.FRAMEBUFFER, G.COLOR_ATTACHMENT0, G.TEXTURE_2D, lutSceneTex, 0);
  G.framebufferRenderbuffer(G.FRAMEBUFFER, G.DEPTH_ATTACHMENT, G.RENDERBUFFER, rb);
  G.bindFramebuffer(G.FRAMEBUFFER, null);
}
function lutDrawPass() {
  G.disable(G.DEPTH_TEST);
  G.useProgram(lutPost.pr);
  G.bindBuffer(G.ARRAY_BUFFER, lutPost.qb);
  G.enableVertexAttribArray(lutPost.loc_p);
  G.vertexAttribPointer(lutPost.loc_p, 2, G.FLOAT, false, 0, 0);
  G.activeTexture(G.TEXTURE0); G.bindTexture(G.TEXTURE_2D, lutSceneTex); G.uniform1i(lutPost.loc_sc, 0);
  G.activeTexture(G.TEXTURE1); G.bindTexture(G.TEXTURE_2D, lutTex); G.uniform1i(lutPost.loc_lut, 1);
  G.viewport(0, 0, W, H);
  G.drawArrays(G.TRIANGLES, 0, 6);
  G.enable(G.DEPTH_TEST);
  G.activeTexture(G.TEXTURE0);
}

/* prepare static GL state per material batch (textures decoded ONCE, not per frame) */
function prepareBatch(b) {
  const bn = b.bind;
  b.dTex = bn[0] ? texZget(bn[0], false) : null;
  b.lmTex = (bn[1] && (b.fx === 'LightMapDC' || b.fx === 'AlphaMasking')) ? texZget(bn[1], false) : null;
  b.alphaTx = (b.fx === 'AlphaMasking' && b.dTex && b.dTex.alpha) ? alphaTexOf(b.dTex, bn[0]) : null;
}

/* batch builder — WORLD-space positions (camera transform lives in the WVP matrix) */
let texGla = null;
// s52 T4: range-captured texture pool + byte-capped LRU accounting
let texPool = null;
let lruBytes = 0;
// s53 T4 knobs: ?poolchunk=1 (chunked capture -> decode -> GL upload -> discard CPU; the ~100 MB
// compressed pool and the 64 MB decoded LRU are never materialized), ?lrumb=N (LRU byte cap override)
let preTex = null;
const POOLCHUNK = QS2.get('poolchunk') === '1';
const LRUMB = QS2.get('lrumb') ? parseInt(QS2.get('lrumb')) : null;
let LRU_BYTES = 64 * 1048576;
if (LRUMB) LRU_BYTES = LRUMB * 1048576;
const TEXFREE = QS2.get('texfree') === '1';   // s58 T4: drop decoded CPU bytes right after GL upload
function buildBatches(lt, ldd, bi8, le) {
  const { bind, fx } = parseCompiledTable(le);
  const fbuf = new DataView(ldd.buffer, ldd.byteOffset, ldd.byteLength);
  const cnt = u32le(lt, 0);
  const pairs = [];
  for (let k = 0; k < cnt; k++) pairs.push([u32le(lt, 4 + 8*k), u32le(lt, 8 + 8*k)]);
  const segInfo = [];
  for (let k = 0; k < cnt; k++) {
    const off2 = pairs[k][0];
    const mid = u32le(ldd, off2 + 40);
    const data_off = u32le(ldd, off2 + 68), vb = u32le(ldd, off2 + 76), ib = u32le(ldd, off2 + 80);
    const ds = declOf(bi8, mid);
    const stride = ds[ds.length-1].end;
    const nv = (vb/stride)|0;
    if (nv <= 0 || vb % stride !== 0 || ib < 6) continue;
    segInfo.push({ k, mid, data_off, vb, ib, nv, stride, ds });
  }
  const byMat = new Map();
  for (const s of segInfo) {
    if (!byMat.has(s.mid)) byMat.set(s.mid, []);
    byMat.get(s.mid).push(s);
  }
  const batches = [];
  for (const [mid, segs] of byMat) {
    if (!segs[0].ds.find(d => d.attr === 1)) continue;
    let nvT = 0, niT = 0;
    for (const s of segs) { nvT += s.nv; niT += (s.ib/2)|0; }
    const pos = new Float32Array(nvT*4);
    const uv0 = new Float32Array(nvT*2);
    const d1 = segs[0].ds.find(d => d.attr === 2);
    const uv1 = d1 ? new Float32Array(nvT*2) : null;
    const d17 = segs[0].ds.find(d => d.attr === 17);
    const c0 = d17 ? new Float32Array(nvT*4) : null;
    const use32 = nvT > 65535;
    const idx = use32 ? new Uint32Array(niT) : new Uint16Array(niT);
    let vo = 0, io = 0;
    for (const s of segs) {
      const dmap = {}; for (const d of s.ds) dmap[d.attr] = d;
      const d0 = dmap[1];
      for (let v = 0; v < s.nv; v++) {
        const o = s.data_off + 4 + v*s.stride;
        const x = fbuf.getFloat32(o, true), zz = fbuf.getFloat32(o + 4, true);
        const h = fbuf.getFloat32(o + 8, true);
        const o4 = (vo+v)*4;
        pos[o4] = x; pos[o4+1] = zz; pos[o4+2] = h; pos[o4+3] = 1;
        uv0[(vo+v)*2] = fbuf.getInt16(o + d0.start, true)/32767*0.5 + 0.5;
        uv0[(vo+v)*2+1] = 1.0 - (fbuf.getInt16(o + d0.start + 2, true)/32767*0.5 + 0.5);
        if (uv1) {
          uv1[(vo+v)*2] = fbuf.getInt16(o + d1.start, true)/32767*0.5 + 0.5;
          uv1[(vo+v)*2+1] = 1.0 - (fbuf.getInt16(o + d1.start + 2, true)/32767*0.5 + 0.5);
        }
        if (c0) {
          for (let c = 0; c < 4; c++) c0[(vo+v)*4+c] = ldd[o + d17.start + c]/255;
        }
      }
      for (let t = 0; t + 2 < (s.ib/2)|0; t += 3) {
        const a = u16le(ldd, s.data_off + 4 + s.vb + t*2);
        const bb2 = u16le(ldd, s.data_off + 4 + s.vb + t*2 + 2);
        const cc = u16le(ldd, s.data_off + 4 + s.vb + t*2 + 4);
        if (a < s.nv && bb2 < s.nv && cc < s.nv) {
          idx[io] = a+vo; idx[io+1] = bb2+vo; idx[io+2] = cc+vo; io += 3;
        }
      }
      vo += s.nv;
    }
    const mk = (arr) => { const b = G.createBuffer(); G.bindBuffer(G.ARRAY_BUFFER, b);
      G.bufferData(G.ARRAY_BUFFER, arr, G.STATIC_DRAW); return b; };
    const bi2 = G.createBuffer();
    G.bindBuffer(G.ELEMENT_ARRAY_BUFFER, bi2);
    G.bufferData(G.ELEMENT_ARRAY_BUFFER, idx, G.STATIC_DRAW);
    const fxn = ['LightMapDC', 'AlphaMasking', 'SimpleAdditive', 'StandardDiffuseDC']
      .includes(fx[mid]) ? fx[mid] : 'other';
    let hsum = 0;
    for (let i = 2; i < pos.length; i += 4) hsum += pos[i];
    batches.push({ fx: fxn, bind: bind[mid] || ['', ''],
      posBuf: mk(pos), uv0Buf: mk(uv0), uv1Buf: uv1 ? mk(uv1) : null,
      c0Buf: (c0 && fxn !== 'other') ? mk(c0) : null, idxBuf: bi2, nidx: io, use32,
      hmean: hsum/(pos.length/4) });
  }
  for (const b of batches) prepareBatch(b);
  batches.sort((a, b) => a.hmean - b.hmean);
  return batches;
}

/* ================= walker runner (s44 T4 functions, verbatim ports) ================= */
function norm3(ax, ay, az, bx, by, bz) {
  const dx = ax - bx, dy = ay - by, dz = az - bz;
  return Math.sqrt(dx * dx + dy * dy + dz * dz);
}
function snap_spawn_nm(pos) {
  const z = nm_ground(pos[0], pos[1], pos[2] + 2.6);
  if (z === -1e9) return [null, 'no_navmesh'];
  const trial = [pos[0], pos[1], z];
  if (!blocked(trial)) return [trial, 'ok'];
  for (let ri = 0; ri < 8; ri++) {
    const r = 0.25 + ri * 0.25;
    const cnt = Math.max(Math.floor(2 * Math.PI * r / 0.25), 8);
    for (let ai = 0; ai < cnt; ai++) {
      const a = ai * (2 * Math.PI / cnt);
      const x = pos[0] + r * Math.cos(a), y = pos[1] + r * Math.sin(a);
      const zz = nm_ground(x, y, pos[2] + 2.6);
      if (zz === -1e9) continue;
      const t2 = [x, y, zz];
      if (!blocked(t2) && Math.abs(zz - pos[2]) < 1.5) return [t2, 'snapped'];
    }
  }
  return [null, 'all_blocked'];
}
function follow_nm(pts) {
  const fails = [];
  const [sp0, why] = snap_spawn_nm(pts[0]);
  if (sp0 === null) return { verdict: why, dist: 0.0, slides: 0, end: null, fails };
  let pos = sp0;
  let s = 0.0, stuck = 0, stall = 0, slides = 0, iters = 0;
  const SUB = 0.2;
  const fail = (w, px, py, pz, extra) => fails.push(Object.assign({ why: w, x: px, y: py, z: pz }, extra || {}));
  for (let wi = 1; wi < pts.length; wi++) {
    const tgt = pts[wi];
    let d = norm3(tgt[0], tgt[1], tgt[2], pos[0], pos[1], pos[2]);
    const n = Math.max(Math.floor(d / 0.5), 1);
    for (let k = 0; k < n; k++) {
      const dl = Math.max(norm3(tgt[0], tgt[1], tgt[2], pos[0], pos[1], pos[2]), 1e-9);
      const dirx = (tgt[0] - pos[0]) / dl, diry = (tgt[1] - pos[1]) / dl, dirz = (tgt[2] - pos[2]) / dl;
      let remaining = Math.min(0.5, d);
      let guard = 0;
      while (remaining > 1e-6 && guard < 6) {
        iters++;
        if (iters > 40000) { fail('stuck_wall_timeout', pos[0], pos[1], pos[2]); return { verdict: 'stuck_wall', dist: s, slides, end: pos.slice(), fails }; }
        guard++;
        const mvlen = Math.min(SUB, remaining);
        const sp = [pos[0] + dirx * mvlen, pos[1] + diry * mvlen, pos[2] + dirz * mvlen];
        const g = nm_ground(sp[0], sp[1], pos[2] + 2.6);
        if (g === -1e9) { fail('fell', sp[0], sp[1], pos[2]); return { verdict: 'fell', dist: s, slides, end: pos.slice(), fails }; }
        const climb = g - pos[2];
        if (climb > 0.9) {
          const sl = try_slide(pos, dirx * mvlen, diry * mvlen, mvlen);
          if (sl !== null) { pos = sl[0]; s += sl[1]; remaining -= sl[1]; slides++; continue; }
          fail('step_too_high', sp[0], sp[1], pos[2], { climb });
          return { verdict: 'step_too_high', dist: s, slides, end: pos.slice(), fails };
        }
        const trial = [sp[0], sp[1], g];
        if (blocked(trial)) {
          const sl = try_slide(pos, dirx * mvlen, diry * mvlen, mvlen);
          if (sl !== null) {
            pos = sl[0]; s += sl[1];
            if (sl[1] < 0.02) stall++; else stall = 0;
            if (stall >= 3) { fail('stuck_wall_stall', pos[0], pos[1], pos[2]); return { verdict: 'stuck_wall', dist: s, slides, end: pos.slice(), fails }; }
            remaining -= Math.max(sl[1], 0.02);
            slides++; stuck = 0;
            continue;
          }
          stuck++;
          if (stuck > 6) { fail('stuck_wall', pos[0], pos[1], pos[2]); return { verdict: 'stuck_wall', dist: s, slides, end: pos.slice(), fails }; }
          remaining = 0;
          break;
        }
        pos = trial;
        s += mvlen;
        remaining -= mvlen;
      }
    }
  }
  return { verdict: 'ok', dist: s, slides, end: pos.slice(), fails };
}

/* route check vs the s44 harness expectations (same comparison as walktest_run) */
function runRouteCheck() {
  const t0 = performance.now();
  const results = [];
  for (const r of WALKTEST_ROUTES) {
    if (results.length >= 10 || performance.now() - t0 > 12000) break;
    const tR = performance.now();
    const p = astar(r.cells[0], r.cells[1]);
    if (p === null) { results.push({ route: r.route, verdict: 'no_path', agree: r.expected === 'no_path', dist: 0 }); continue; }
    const pts = p.map(c => [nmCent[c * 3], nmCent[c * 3 + 1], nmCent[c * 3 + 2]]);
    const out = follow_nm(pts);
    const dd = (r.expected_dist != null) ? Math.abs(out.dist - r.expected_dist) : null;
    results.push({ route: r.route, verdict: out.verdict, dist: +out.dist.toFixed(3),
      expected: r.expected, expected_dist: r.expected_dist,
      agree: out.verdict === r.expected && (dd == null || dd < 0.25),
      dist_delta: dd != null ? +dd.toFixed(3) : null, ms: Math.round(performance.now() - tR) });
  }
  return { run: results.length,
    agree: results.filter(r => r.agree).length,
    results };
}

/* ================= Batman from the USER's zip (s40 T7 pipeline, engine-verified) ================= */
function u16a(arr) { const o = new Uint16Array(arr.length); o.set(arr); return o; }
const buildGLB = function buildGLB(skin, A, byNameC, clipsToEmbed) {
    const f32 = a => new Float32Array(a);
    const BIPED = {
      'Bip01_Pelvis':'Bip01','Bip01_Spine':'Bip01_Pelvis','Bip01_Spine1':'Bip01_Spine',
      'Bip01_Neck':'Bip01_Spine1','Bip01_Head':'Bip01_Neck',
      'Bip01_L_Thigh':'Bip01_Pelvis','Bip01_L_Calf':'Bip01_L_Thigh','Bip01_L_Foot':'Bip01_L_Calf',
      'Bip01_R_Thigh':'Bip01_Pelvis','Bip01_R_Calf':'Bip01_R_Thigh','Bip01_R_Foot':'Bip01_R_Calf',
      'Bip01_L_Clavicle':'Bip01_Neck','Bip01_L_UpperArm':'Bip01_L_Clavicle',
      'Bip01_L_Forearm':'Bip01_L_UpperArm','Bip01_L_Hand':'Bip01_L_Forearm',
      'Bip01_R_Clavicle':'Bip01_Neck','Bip01_R_UpperArm':'Bip01_R_Clavicle',
      'Bip01_R_Forearm':'Bip01_R_UpperArm','Bip01_R_Hand':'Bip01_R_Forearm',
      'Bip01_L_Finger0':'Bip01_L_Hand','Bip01_L_Finger01':'Bip01_L_Finger0',
      'Bip01_L_Finger1':'Bip01_L_Hand','Bip01_L_Finger11':'Bip01_L_Finger1',
      'Bip01_L_Finger2':'Bip01_L_Hand','Bip01_L_Finger21':'Bip01_L_Finger2',
      'Bip01_R_Finger0':'Bip01_R_Hand','Bip01_R_Finger01':'Bip01_R_Finger0',
      'Bip01_R_Finger1':'Bip01_R_Hand','Bip01_R_Finger11':'Bip01_R_Finger1',
      'Bip01_R_Finger2':'Bip01_R_Hand','Bip01_R_Finger21':'Bip01_R_Finger2'
    };
    const parentOf = nm => skin.pnameOf[nm] || BIPED[nm] || null;
    const need = []; const inNeed = new Set();
    for (const jn of skin.jointNodes) {
      let nm = jn;
      while (nm && !inNeed.has(nm)) { need.push(nm); inNeed.add(nm); nm = parentOf(nm); }
    }
    const nodeOf = {}; const gnodes = [];
    for (const nm of need) { nodeOf[nm] = gnodes.length; gnodes.push({ name: nm, children: [] }); }
    for (const nm of need) {
      const pr = parentOf(nm);
      if (pr && nodeOf[pr] !== undefined) gnodes[nodeOf[pr]].children.push(nodeOf[nm]);
    }
    for (const nm of need) {
      const nd = skin.nodes.find(x => x.name === nm);
      const n = gnodes[nodeOf[nm]];
      n.translation = nd.t; n.rotation = nd.q; n.scale = nd.s;
    }
    const NVV = skin.verts.length / 3;
    gnodes.push({ name: 'BATMAN_mesh', mesh: 0, skin: 0 });
    const posB = f32(skin.verts), uvB = f32(skin.uvs), wtB = f32(skin.skinW);
    const jnB = u16a(skin.skinJ), idxB = u16a(skin.idx);
    // s62 T2 FIX (numpy-computed): inverse binds = inv(BIPED-FK rest), column-major GLB
    const __S62_IB = [-0.0, 2e-06, 1.0, 0.0, 2e-06, -1.0, 2e-06, 0.0, 1.0, 2e-06, 0.0, 0.0, -0.980574, -2e-06, -0.0, 1.0, 1e-06, -2e-06, 1.0, 0.0, 0.005879, -0.999983, -2e-06, 0.0, 0.999983, 0.005879, -1e-06, 0.0, -1.09366, -0.011082, 1e-06, 1.0, 1e-06, -2e-06, 1.0, 0.0, 0.005879, -0.999983, -2e-06, 0.0, 0.999983, 0.005879, -1e-06, 0.0, -1.303276, -0.010865, 1e-06, 1.0, 1e-06, -2e-06, 1.0, 0.0, -0.147729, -0.989028, -2e-06, 0.0, 0.989028, -0.147729, -2e-06, 0.0, -1.570526, 0.263904, 2e-06, 1.0, 1e-06, -3e-06, 1.0, 0.0, -0.163583, -0.986529, -2e-06, 0.0, 0.986529, -0.163583, -2e-06, 0.0, -1.630016, 0.287117, 2e-06, 1.0, 0.996238, -0.071014, 0.049667, 0.0, 0.070592, 0.997453, 0.010201, 0.0, -0.050265, -0.006656, 0.998714, 0.0, 0.046196, -0.005336, -1.542728, 1.0, 0.568526, -0.255251, 0.782064, 0.0, 0.025721, 0.955698, 0.293223, 0.0, -0.822263, -0.14659, 0.549905, 0.0, 1.14856, 0.247098, -1.007321, 1.0, 0.622986, -0.016222, 0.782064, 0.0, -0.344879, 0.891672, 0.293223, 0.0, -0.702101, -0.452392, 0.549905, 0.0, 0.695783, 0.558687, -1.007321, 1.0, 0.405356, -0.91154, 0.069143, 0.0, -0.294462, -0.058592, 0.953865, 0.0, -0.865435, -0.407015, -0.292165, 0.0, 0.730407, 0.929791, 0.339173, 1.0, -0.034756, 0.665574, 0.745522, 0.0, -0.434385, 0.661764, -0.611047, 0.0, -0.900056, -0.345082, 0.266115, 0.0, 0.926024, 0.089391, -0.736507, 1.0, -0.021597, 0.666131, 0.745522, 0.0, -0.421223, 0.670218, -0.611047, 0.0, -0.9067, -0.327228, 0.266115, 0.0, 0.886202, 0.071893, -0.736507, 1.0, 0.164226, -0.946258, 0.278613, 0.0, -0.361107, 0.20517, 0.909674, 0.0, -0.91795, -0.250001, -0.308006, 0.0, 0.809683, 0.821441, 0.266895, 1.0, -0.027835, -0.963914, 0.264754, 0.0, -0.295416, 0.260959, 0.919037, 0.0, -0.954963, -0.052631, -0.292019, 0.0, 0.929003, 0.642224, 0.260179, 1.0, 0.193021, -0.975624, -0.104407, 0.0, -0.039266, -0.114003, 0.992704, 0.0, -0.980408, -0.187513, -0.060314, 0.0, 0.883969, 0.75349, 0.19578, 1.0, -0.046959, -0.979029, -0.198231, 0.0, -0.109741, -0.192192, 0.975202, 0.0, -0.99285, 0.067548, -0.098414, 0.0, 0.995259, 0.49897, 0.287471, 1.0, -0.996238, 0.071015, 0.049664, 0.0, 0.070594, 0.997453, -0.010198, 0.0, -0.050262, -0.006654, -0.998714, 0.0, 0.046193, -0.00534, 1.542728, 1.0, -0.568529, 0.255252, 0.782062, 0.0, 0.025724, 0.955697, -0.293223, 0.0, -0.822261, -0.146588, -0.549908, 0.0, 1.148558, 0.247094, 1.007324, 1.0, -0.622989, 0.016222, 0.782062, 0.0, -0.344876, 0.891673, -0.293223, 0.0, -0.7021, -0.452389, -0.549908, 0.0, 0.695783, 0.558683, 1.007324, 1.0, -0.405359, 0.911539, 0.069142, 0.0, -0.294459, -0.058592, -0.953866, 0.0, -0.865435, -0.407018, 0.292162, 0.0, 0.730407, 0.929794, -0.339169, 1.0, 0.034752, -0.665574, 0.745523, 0.0, -0.434382, 0.661766, 0.611046, 0.0, -0.900057, -0.345078, -0.266115, 0.0, 0.926026, 0.089387, 0.736506, 1.0, 0.021593, -0.66613, 0.745523, 0.0, -0.42122, 0.670221, 0.611046, 0.0, -0.906701, -0.327224, -0.266115, 0.0, 0.886204, 0.071889, 0.736506, 1.0, -0.164229, 0.946257, 0.278612, 0.0, -0.361104, 0.205169, -0.909675, 0.0, -0.91795, -0.250003, 0.308003, 0.0, 0.809684, 0.821442, -0.26689, 1.0, 0.027832, 0.963914, 0.264753, 0.0, -0.295413, 0.260957, -0.919038, 0.0, -0.954964, -0.052633, 0.292016, 0.0, 0.929004, 0.642225, -0.260174, 1.0, -0.193024, 0.975623, -0.104409, 0.0, -0.039263, -0.114005, -0.992704, 0.0, -0.980409, -0.187516, 0.060312, 0.0, 0.883969, 0.753493, -0.195776, 1.0, 0.046955, 0.979029, -0.198233, 0.0, -0.109738, -0.192194, -0.975201, 0.0, -0.992851, 0.067545, 0.098412, 0.0, 0.99526, 0.498973, -0.287467, 1.0, 0.039431, 0.206549, -0.977641, 0.0, -0.055148, -0.976461, -0.208524, 0.0, -0.997699, 0.062138, -0.027112, 0.0, 0.974138, -0.082825, 0.130219, 1.0, -0.003373, 0.210252, -0.977641, 0.0, 0.144468, -0.967288, -0.208524, 0.0, -0.989504, -0.141941, -0.027112, 0.0, 0.569352, 0.033596, 0.130219, 1.0, -6e-06, 0.126829, -0.991924, 0.0, -0.0, -0.991924, -0.126829, 0.0, -1.0, -0.0, 6e-06, 0.0, 0.126424, 0.026761, 0.12505, 1.0, -0.039431, -0.20655, -0.977641, 0.0, -0.05515, -0.976461, 0.208525, 0.0, -0.997699, 0.062139, 0.027111, 0.0, 0.974138, -0.082828, -0.130219, 1.0, 0.003373, -0.210253, -0.977641, 0.0, 0.144465, -0.967288, 0.208525, 0.0, -0.989504, -0.141939, 0.027111, 0.0, 0.569352, 0.033594, -0.130219, 1.0, 7e-06, -0.126829, -0.991924, 0.0, -3e-06, -0.991924, 0.126829, 0.0, -1.0, 2e-06, -7e-06, 0.0, 0.126425, 0.026758, -0.125049, 1.0];
    const ibmB = new Float32Array(__S62_IB);

    const order6 = [['pos', posB], ['uv', uvB], ['wt', wtB], ['jn', jnB], ['idx', idxB], ['ibm', ibmB]];
    const offs = {}; let base = 0;
    for (const [k, c] of order6) { while (base % 4) base++; offs[k] = base; base += c.byteLength; }
    const gltf = {
      asset: { version: '2.0', generator: 'tdkr-s37-browser' },
      scene: 0, scenes: [{ nodes: null }],
      nodes: gnodes,
      skins: [{ inverseBindMatrices: null, joints: skin.jointNodes.map(nm => nodeOf[nm]) }],
      meshes: [{ primitives: [{ attributes: { POSITION: 0, TEXCOORD_0: 1, WEIGHTS_0: 2, JOINTS_0: 3 }, indices: 4, material: 0 }] }],
      materials: [{ pbrMetallicRoughness: { baseColorFactor: [0.8, 0.8, 0.85, 1] } }],
      animations: [], accessors: [], bufferViews: [], buffers: [{ byteLength: 0 }]
    };
    function addAcc(off, ln, count, ctype, typ) {
      gltf.bufferViews.push({ buffer: 0, byteOffset: off, byteLength: ln });
      gltf.accessors.push({ bufferView: gltf.bufferViews.length - 1, componentType: ctype, count, type: typ });
      return gltf.accessors.length - 1;
    }
    addAcc(offs.pos, posB.byteLength, NVV, 5126, 'VEC3');
    addAcc(offs.uv, uvB.byteLength, NVV, 5126, 'VEC2');
    addAcc(offs.wt, wtB.byteLength, NVV, 5126, 'VEC4');
    addAcc(offs.jn, jnB.byteLength, NVV, 5123, 'VEC4');
    addAcc(offs.idx, idxB.byteLength, idxB.length, 5123, 'SCALAR');
    gltf.skins[0].inverseBindMatrices = addAcc(offs.ibm, ibmB.byteLength, skin.invB.length, 5126, 'MAT4');
    const animBins = []; let ab = 0;
    for (const nm of (clipsToEmbed || ['_001_idle_stand', '_007_walk', '_008_run', '_057_glide_idle', '_089_grapnel_pull', '_088_grapnel_shoot', '_065_glide_idle_to_run'])) {   // s53 T5 + s54 T3: state-table clips; s59 T2: caller-suppliable list (enemy clips)
      const clip = byNameC[nm]; if (!clip) continue;
      const { chans } = TDKR.assembleClip(A, clip);
      const samplers = []; const chansG = [];
      for (let c = 0; c < 78; c++) {
        const ch = chans[c]; if (!ch) continue;
        const meta = A.CH[c];
        let nmb = meta.name || '';
        nmb = nmb.endsWith('-node') ? nmb.slice(0, -5) : nmb;
        if (nodeOf[nmb] === undefined) continue;
        const ncomp = meta.ty === 1 ? 3 : 4;
        const seen = new Set();
        const tks = [], vks = [];
        for (let i = 0; i < ch.t.length; i++) {
          const t = ch.t[i];
          if (seen.has(t)) continue;
          seen.add(t); tks.push(t); vks.push(ch.v[i]);
        }
        const tb = new Float32Array(tks.length);
        const tb0 = tks[0];
        for (let i = 0; i < tks.length; i++) tb[i] = (tks[i] - tb0) / 1000;
        const ob = new Float32Array(tks.length * ncomp);
        vks.forEach((row, i) => { for (let d = 0; d < ncomp; d++) ob[i * ncomp + d] = row[d]; });
        while (ab % 4) { animBins.push(new Uint8Array(1)); ab++; }
        const tOff = ab; animBins.push(tb); ab += tb.byteLength;
        while (ab % 4) { animBins.push(new Uint8Array(1)); ab++; }
        const oOff = ab; animBins.push(ob); ab += ob.byteLength;
        while (ab % 4) { animBins.push(new Uint8Array(1)); ab++; }
        gltf.bufferViews.push({ buffer: 0, byteOffset: base + tOff, byteLength: tb.byteLength });
        gltf.accessors.push({ bufferView: gltf.bufferViews.length - 1, componentType: 5126, count: tks.length, type: 'SCALAR' });
        const ti = gltf.accessors.length - 1;
        gltf.bufferViews.push({ buffer: 0, byteOffset: base + oOff, byteLength: ob.byteLength });
        gltf.accessors.push({ bufferView: gltf.bufferViews.length - 1, componentType: 5126, count: tks.length, type: ncomp === 4 ? 'VEC4' : 'VEC3' });
        const oi = gltf.accessors.length - 1;
        samplers.push({ input: ti, output: oi, interpolation: 'LINEAR' });
        chansG.push({ sampler: samplers.length - 1, target: { node: nodeOf[nmb], path: meta.ty === 1 ? 'translation' : 'rotation' } });
      }
      gltf.animations.push({ name: nm, samplers, channels: chansG });
    }
    const roots = [];
    for (let i = 0; i < gnodes.length - 1; i++) {
      const pr = parentOf(gnodes[i].name);
      if (!pr || nodeOf[pr] === undefined || nodeOf[pr] === i) roots.push(i);
    }
    roots.push(gnodes.length - 1);
    gltf.scenes[0].nodes = roots;
    gltf.buffers[0].byteLength = base + ab;
    const bin = new Uint8Array(base + ab);
    for (const [k, c] of order6) bin.set(new Uint8Array(c.buffer, c.byteOffset, c.byteLength), offs[k]);
    let o4 = base;
    for (const blk of animBins) {
      if (blk instanceof Float32Array) { while (o4 % 4) o4++; }
      bin.set(new Uint8Array(blk.buffer, blk.byteOffset, blk.byteLength), o4);
      o4 += blk.byteLength;
    }
    let js = new TextEncoder().encode(JSON.stringify(gltf));
    while (js.length % 4) js = new Uint8Array([...js, 32]);
    const total = 12 + 8 + js.length + 8 + bin.length;
    const out = new Uint8Array(total); const dv = new DataView(out.buffer);
    dv.setUint32(0, 0x46546C67, true); dv.setUint32(4, 2, true); dv.setUint32(8, total, true);
    dv.setUint32(12, js.length, true); dv.setUint32(16, 0x4E4F534A, true); out.set(js, 20);
    dv.setUint32(20 + js.length, bin.length, true); dv.setUint32(24 + js.length, 0x004E4942, true);
    out.set(bin, 28 + js.length);
    return out;
};

/* Batman THREE viewport (silhouette-friendly white background) */
const bcv = document.getElementById('bman');
const bRenderer = new THREE.WebGLRenderer({ canvas: bcv, antialias: true, preserveDrawingBuffer: true });
bRenderer.outputColorSpace = THREE.SRGBColorSpace;
bRenderer.setClearColor(0xffffff, 1);
bRenderer.setPixelRatio(1);
bRenderer.setSize(320, 240, false);
const bScene = new THREE.Scene();
const bCam = new THREE.PerspectiveCamera(45, 320 / 240, 0.1, 100);
bScene.add(new THREE.HemisphereLight(0x8899bb, 0x223322, 2.6));
bScene.add(new THREE.AmbientLight(0xffffff, 1.1));
const bSun = new THREE.DirectionalLight(0xffeecc, 3.0); bSun.position.set(3, 6, 2); bScene.add(bSun);
let batman = null, mixer = null; const actions = {};

/* ---- s51 T2: lazy zip reads (file.slice; never hold the whole OBB) ---- */
async function zipReadLazy(file, m) {
  const hh = new Uint8Array(await file.slice(m.lho, m.lho + 30).arrayBuffer());
  if (u32le(hh, 0) !== 0x04034b50) throw new Error('bad local header');
  const nlen = u16le(hh, 26), elen = u16le(hh, 28);
  const start = m.lho + 30 + nlen + elen;
  const blob = file.slice(start, start + m.csize);
  if (m.method === 0) return new Uint8Array(await blob.arrayBuffer());
  const ds2 = new DecompressionStream('deflate-raw');
  const st2 = new Response(blob).body.pipeThrough(ds2);
  return new Uint8Array(await new Response(st2).arrayBuffer());
}
async function streamInflateRanges(file, m, ranges) {
  // ranges: [{o, s, out?}] in the INFLATED stream; returns array of Uint8Array
  const hh = new Uint8Array(await file.slice(m.lho, m.lho + 30).arrayBuffer());
  const nlen = u16le(hh, 26), elen = u16le(hh, 28);
  const start = m.lho + 30 + nlen + elen;
  const ds2 = new DecompressionStream('deflate-raw');
  const src = new Response(file.slice(start, start + m.csize)).body.pipeThrough(ds2);
  const reader = src.getReader();
  const outs = ranges.map(r => new Uint8Array(r.s));
  let pos = 0;
  const endMax = Math.max(...ranges.map(r => r.o + r.s));
  while (pos < endMax) {
    const rd = await reader.read();
    if (rd.done) break;
    const v = rd.value;
    for (let i = 0; i < ranges.length; i++) {
      const c0 = Math.max(ranges[i].o, pos), c1 = Math.min(ranges[i].o + ranges[i].s, pos + v.length);
      if (c1 > c0) outs[i].set(v.subarray(c0 - pos, c1 - pos), c0 - ranges[i].o);
    }
    pos += v.length;
  }
  try { await reader.cancel(); } catch (e) {}
  return outs;
}
async function glaIndexLazy(file, m) {
  // inflate first 1 MB, parse the BE index + name pool; returns {ents: Map name->{o,s}}
  const head = (await streamInflateRanges(file, m, [{ o: 0, s: 1 << 20 }]))[0];
  const dv = new DataView(head.buffer, head.byteOffset, head.byteLength);
  const idxSize = dv.getUint32(4), n = dv.getUint32(12);
  if (idxSize + 4096 > head.length) throw new Error('gla index bigger than probe');
  const pool = head.subarray(16 + n * 16, idxSize);
  const ents = new Map();
  for (let i = 0; i < n; i++) {
    const b = 16 + i * 16;
    const o = dv.getUint32(b), s = dv.getUint32(b + 4), no = dv.getUint32(b + 8);
    let e = pool.indexOf(0, no);
    if (e < 0) e = no + 96;
    ents.set(LATIN.decode(pool.subarray(no, e)), { o, s });
  }
  window.__GLAIDX = window.__GLAIDX || { n, idxSize, headLen: head.length, sample: [...ents.entries()].slice(0, 5).map(e => e[0]), has: ents.has('GothamCity.zip'), entsN: ents.size };
  return ents;
}
async function glaSliceLazy(file, m, want) {
  const ents = await glaIndexLazy(file, m);
  const rs = [];
  const names = [];
  for (const nm of want) {
    const e = ents.get(nm);
    if (!e) throw new Error('lazy gla member missing: ' + nm);
    rs.push({ o: e.o, s: e.s });
    names.push(nm);
  }
  const outs = await streamInflateRanges(file, m, rs.map(r => ({ o: r.o, s: r.s + (1 << 16) })));
  const res = {};
  names.forEach((nm, i) => { res[nm] = outs[i]; });
  return res;
}

async function loadBatman(zipBuf, findM) {
  const aMem = await glaSliceLazy(zipBuf, zmembersGet(findM(/data\/actors\.gla$/i)),
    new Set(['batman.bdae', 'batman_anims.bdae']));
  // s52 T4: actors_tex.gla by index + single-member range (30.7 MB container never materialized)
  const atM = zmembersGet(findM(/textures\/actors_tex\.gla$/i));
  const atIdx = await glaIndexLazy(zipBuf, atM);
  const atWant = 'chara_Batman_DIFFUSE.tga';
  const atEnt = atIdx.get(atWant);
  let atBytes = atEnt ? (await streamInflateRanges(zipBuf, atM, [{ o: atEnt.o, s: atEnt.s }]))[0] : null;
  atIdx.clear();
  const gt = { ents: atBytes ? { [atWant]: { off: 0, size: atBytes.length } } : {} };
  log('LZ batman.bdae bytes=' + (aMem['batman.bdae'] ? aMem['batman.bdae'].length : -1) +
       ' anims=' + (aMem['batman_anims.bdae'] ? aMem['batman_anims.bdae'].length : -1) +
       ' texEnts=' + Object.keys(gt.ents || {}).length);
  const skin = TDKR.readBdae(aMem['batman.bdae']);
  const A = TDKR.decodeAnims(aMem['batman_anims.bdae']);
  log('batman.bdae: ' + skin.verts.length / 3 + ' verts, ' + skin.idx.length + ' idx; anims: ' + A.clips.length + ' clips');
  const texE = gt.ents['chara_Batman_DIFFUSE.tga'];
  let texture = null;
  if (texE && atBytes) {
    const td = atBytes;
    const th = td[4] | (td[5] << 8) | (td[6] << 16) | (td[7] << 24);
    const tw = td[8] | (td[9] << 8) | (td[10] << 16) | (td[11] << 24);
    const px = td.subarray(52, 52 + tw * th * 3);
    const rgba = new Uint8Array(tw * th * 4);
    for (let i = 0; i < tw * th; i++) {
      rgba[i*4] = px[i*3]; rgba[i*4+1] = px[i*3+1]; rgba[i*4+2] = px[i*3+2]; rgba[i*4+3] = 255;
    }
    texture = new THREE.DataTexture(rgba, tw, th, THREE.RGBAFormat);
    texture.colorSpace = THREE.SRGBColorSpace; texture.needsUpdate = true; texture.flipY = false;
    log('chara_Batman_DIFFUSE: ' + tw + 'x' + th + ' RGB888 (s42 T1: R8G8B8 byte0=R) decoded');
  }
  atBytes = null; gt.ents = null;
  const byNameC = Object.fromEntries(A.clips.map(c => [c.name, c]));
  const glbBytes = buildGLB(skin, A, byNameC);
  const g = await new Promise((res, rej) => new GLTFLoader().parse(glbBytes.buffer, '', res, rej));
  batman = g.scene; bScene.add(batman);
  batman.rotation.x = -Math.PI / 2;
  mixer = new THREE.AnimationMixer(batman);
  for (const c of g.animations) actions[c.name] = mixer.clipAction(c);
  const idle = actions['_001_idle_stand'], walk = actions['_007_walk'];
  if (idle) { idle.play(); idle.setEffectiveWeight(1); }
  if (walk) { walk.play(); walk.setEffectiveWeight(0); }
  let sm = null; batman.traverse(o => { if (o.isSkinnedMesh) sm = o; });
  if (texture && sm) { sm.material.map = texture; sm.material.color.set(0xffffff); sm.material.needsUpdate = true; }
  return { verts: skin.verts.length / 3, clips: g.animations.map(a => a.name) };
}
// s58 T3: enemy (Melee_Enemy_Merc) rig via the SAME FK/GLB path as Batman.
// Rig LOCATED: Bane_mercenary.bdae (1,229,264 B; low LOD 750,064 B) in actors.gla.
// Clips: the SHARED anim bank batman_anims.bdae (921 clips; enemy families s55 T6);
// Merc state table Idle/Walk/Run -> _014_idle_enemy_combat / _166_enemy_walk /
// _171_enemy_run (FK-validated node-side, extraction/re/session58/s58_t3_fk.json).
// NOTE: readBdae's SKIN_OFFS is batman-hardwired (the merc probe's '1449 verts' was
// the batman layout misread onto merc bytes) -> in-page merc MESH playback needs a
// merc-specific bdae layout derivation (one focused session). This flag fails
// gracefully with that error; clip FK receipts are node-side.
// Damage = 5.0 HP per decoded GiveDamage(actorId, damage) census (game_config.gla:
// 146 literal calls; 5 x91 = the scripted standard; GiveDamage disasm 0x155e4c).
// s60 T3: Hurt/Death wired (shared bank: _222/_223 hurt, _250/_251 death)
const ENEMY_CLIPS = ['_014_idle_enemy_combat', '_166_enemy_walk', '_171_enemy_run', '_223_enemy_hurtl', '_250_enemy_death1'];
const ENEMY_DMG = 5.0;
let merc = null, mercMixer = null, mercActions = {}, mercSeq = null;
let mercSkinProbe = null, mercDisp = { byClip: {} };
let mercRestIoU = null;

// s60 T3: rest-pose silhouette capture (raw WebGL1 + readPixels) - runs BEFORE any
// animation so the CPU-skin at rest == bind vertices (bindMaxDev ~ 0 expected).
function captureRestIoU(smIo) {
  try {
    // s60 T3 (rev2): silhouette from the STATIC bind geometry - the mesh exactly as
    // parsed and assembled into the GLB (skinning itself is validated by the
    // displacement battery idle/walk/run/hurt/death + wrong-clip control).
    const geo = smIo.geometry;
    const posA = geo.attributes.position;
    const NVi = posA.count;
    const vAll = new Float32Array(NVi * 3);
    vAll.set(posA.array.subarray(0, NVi * 3));
    const ia = geo.index.array, IN = geo.index.count;
    const SZ = 256, GRID = 64;
    const cv = document.createElement('canvas'); cv.width = SZ; cv.height = SZ;
    const gl = cv.getContext('webgl', { preserveDrawingBuffer: true });
    let mnx = 1e9, mxx = -1e9, mnz = 1e9, mxz = -1e9;
    for (let i = 0; i < NVi; i++) { mnx = Math.min(mnx, vAll[i*3]); mxx = Math.max(mxx, vAll[i*3]); mnz = Math.min(mnz, vAll[i*3+2]); mxz = Math.max(mxz, vAll[i*3+2]); }
    const sx = 2.0 / Math.max(1e-6, mxx - mnx), sz2 = 2.0 / Math.max(1e-6, mxz - mnz);
    const sc = Math.min(sx, sz2) * 0.9;
    const cx = (mnx + mxx) / 2, cz = (mnz + mxz) / 2;
    const xy = new Float32Array(NVi * 2);
    for (let i = 0; i < NVi; i++) { xy[i*2] = (vAll[i*3] - cx) * sc; xy[i*2+1] = (vAll[i*3+2] - cz) * sc; }
    const vb = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, vb); gl.bufferData(gl.ARRAY_BUFFER, xy, gl.STATIC_DRAW);
    const ib = gl.createBuffer(); gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ib); gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, ia, gl.STATIC_DRAW);
    const prog = gl.createProgram();
    const sh = (t, s) => { const o = gl.createShader(t); gl.shaderSource(o, s); gl.compileShader(o); return o; };
    gl.attachShader(prog, sh(gl.VERTEX_SHADER, 'attribute vec2 q; void main(){ gl_Position = vec4(q, 0.0, 1.0); }'));
    gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, 'void main(){ gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0); }'));
    gl.linkProgram(prog); gl.useProgram(prog);
    const loc = gl.getAttribLocation(prog, 'q');
    gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    gl.viewport(0, 0, SZ, SZ); gl.clearColor(0, 0, 0, 1); gl.clear(gl.COLOR_BUFFER_BIT);
    gl.drawElements(gl.TRIANGLES, IN, gl.UNSIGNED_SHORT, 0);
    const glErr = gl.getError();
    const linkOk = gl.getProgramParameter(prog, gl.LINK_STATUS);
    const px = new Uint8Array(SZ * SZ * 4);
    gl.readPixels(0, 0, SZ, SZ, gl.RGBA, gl.UNSIGNED_BYTE, px);
    let lit = 0;
    for (let i = 0; i < SZ * SZ; i++) if (px[i * 4] > 32) lit++;
    let hex = '';
    for (let gy = 0; gy < GRID; gy++) for (let gx = 0; gx < GRID / 8; gx++) {
      let b = 0;
      // byte gx covers grid columns [gx*8,(gx+1)*8); bit (gy2,gx2) = cell 4x4 px;
      // buffer row 0 = bottom -> row flip
      for (let gy2 = 0; gy2 < 4; gy2++) for (let gx2 = 0; gx2 < 8; gx2++) {
        for (let sy = 0; sy < 4; sy++) for (let sx = 0; sx < 4; sx++) {
          const X = (gx * 8 + gx2) * 4 + sx, Y = (GRID - 1 - gy) * 4 + gy2;
          const o = (Y * SZ + X) * 4;
          if (px[o] > 32) { b |= 1 << (gy2 * 8 + gx2); sy = 4; sx = 4; }
        }
      }
      hex += ('0000000' + (b >>> 0).toString(16)).slice(-8);   // 32 bits per group, unsigned
    }
    let bindDev = 0;
    const pa = posA.array;
    for (let i = 0; i < NVi * 3; i++) bindDev = Math.max(bindDev, Math.abs(vAll[i] - pa[i]));
    const res = { ok: lit > 1000, gridHex: hex, grid: GRID, SZ,
      meshMin: [+mnx.toFixed(4), +mnz.toFixed(4)], meshMax: [+mxx.toFixed(4), +mxz.toFixed(4)],
      height: +(mxz - mnz).toFixed(4), feetZ: +mnz.toFixed(4),
      nVerts: NVi, nIdx: IN, glErr, linkOk, lit };
    log('enemyIoU: height=' + (mxz - mnz).toFixed(3) + ' feetZ=' + mnz.toFixed(3) + ' bindDev=' + bindDev.toFixed(5));
    return res;
  } catch (e4) {
    log('enemyIoU FAILED: ' + (e4 && e4.message || e4));
    return { ok: false, error: String(e4 && e4.message || e4) };
  }
}

// s61 T3: POSED skinned capture. Root-cause fix proven in-page:
// (a) skinIndex/skinWeight are VEC4 from the GLB (r160 applyBoneTransform reads 4 comps
//     unconditionally - 1-comp attrs made getComponent(i>0) undefined and the weight
//     check `undefined !== 0` pass -> bones[undefined] crash/zeros - the s60 failure);
// (b) bind() must keep the FILE invB (GLTFLoader binds with identity bindMatrix at parse);
// (c) NEVER skeleton.pose() per frame (it overwrites the clip pose from boneInverses).
// Recipe per frame: action.time=t; mixer.update(0); merc.updateMatrixWorld(true);
// skeleton.update(); then applyBoneTransform == numpy convention
// (boneMat = boneWorld x fileInvB, weights x4).

function captureBindBisect(smIo, mercObj) {
    // S62 T2: rest/bind convention gap bisection (task spec a-d)
    const out = { ok: true };
    const skel = smIo.skeleton;
    const NB = skel.bones.length;
    // (a) per-bone boneInverses + bone.matrixWorld (bind/rest pose, mesh transform zeroed)
    const keepR = mercObj.rotation.x, keepP = mercObj.position.clone(), keepS = mercObj.scale.clone();
    mercObj.rotation.set(0, 0, 0); mercObj.position.set(0, 0, 0); mercObj.scale.set(1, 1, 1);
    mercObj.updateMatrixWorld(true); skel.update();
    out.scaleWas = { x: keepS.x, y: keepS.y, z: keepS.z };
    out.rotWas = keepR;
    const inv = [], mw = [], bn = [];
    for (let i = 0; i < NB; i++) {
      inv.push(Array.from(skel.boneInverses[i].elements));
      mw.push(Array.from(skel.bones[i].matrixWorld.elements));
      bn.push(skel.bones[i].name || ('bone' + i));
    }
    out.boneNames = bn;
    out.boneInverses = inv;
    out.boneMatrixWorld = mw;
    // bindMatrix / bindMatrixInverse
    out.bindMatrix = Array.from(smIo.bindMatrix.elements);
    out.bindMatrixInverse = Array.from(smIo.bindMatrixInverse.elements);
    // (b) node TRS as the loader parsed them (same values the GLB carried)
    out.nodeTRS = skel.bones.map(b => ({
      name: b.name || ('bone' + bn.indexOf(b)),
      pos: [b.position.x, b.position.y, b.position.z],
      quat: [b.quaternion.x, b.quaternion.y, b.quaternion.z, b.quaternion.w],
      scl: [b.scale.x, b.scale.y, b.scale.z] }));
    out.meshNode = { pos: [mercObj.position.x, mercObj.position.y, mercObj.position.z],
      quat: [mercObj.quaternion.x, mercObj.quaternion.y, mercObj.quaternion.z, mercObj.quaternion.w],
      scl: [mercObj.scale.x, mercObj.scale.y, mercObj.scale.z] };
    out.skelRoot = skel.bones[0] ? skel.bones[0].name : null;
    // (c) skin attributes as LOADED
    const g = smIo.geometry;
    const si = g.attributes.skinIndex, sw = g.attributes.skinWeight;
    out.skinAttrs = { skinIndex: si ? { itemSize: si.itemSize, count: si.count,
      arrayType: si.array.constructor.name } : null,
      skinWeight: sw ? { itemSize: sw.itemSize, count: sw.count,
        arrayType: sw.array.constructor.name } : null };
    if (sw) {
      let bad = 0, maxDev = 0;
      for (let i = 0; i < sw.count; i++) {
        let s2 = 0;
        for (let k = 0; k < 4; k++) s2 += sw.getComponent(i, k);
        const d = Math.abs(s2 - 1);
        if (d > 1e-3) bad++;
        if (d > maxDev) maxDev = d;
      }
      out.weightSums = { bad: bad, maxDev: +maxDev.toFixed(6), count: sw.count };
    }
    // (d) one-vertex identity test: skin vertex 0 with identity boneMatrices
    const v0 = new THREE.Vector3();
    g.attributes.position.getX(0); // touch
    const px0 = g.attributes.position.getX(0), py0 = g.attributes.position.getY(0),
          pz0 = g.attributes.position.getZ(0);
    // identity skin: set every boneMatrix = I (save first)
    const saved = new Float32Array(skel.boneMatrices);
    for (let i = 0; i < NB * 16; i++) skel.boneMatrices[i] = 0;
    for (let i = 0; i < NB; i++) {
      skel.boneMatrices[i*16+0] = 1; skel.boneMatrices[i*16+5] = 1;
      skel.boneMatrices[i*16+10] = 1; skel.boneMatrices[i*16+15] = 1;
    }
    smIo.applyBoneTransform(0, v0);
    out.oneVertexIdentity = { in: [px0, py0, pz0], out: [v0.x, v0.y, v0.z],
      maxDev: +Math.max(Math.abs(v0.x - px0), Math.abs(v0.y - py0), Math.abs(v0.z - pz0)).toFixed(6) };
    // also vertices through the REAL rest chain (non-degenerate picks)
    out.vertexRest = [];
    for (const idx of [1, 100, 500, 900, 1200]) {
      const v1 = new THREE.Vector3();
      smIo.applyBoneTransform(idx, v1);
      out.vertexRest.push({ idx,
        bind: [g.attributes.position.getX(idx), g.attributes.position.getY(idx), g.attributes.position.getZ(idx)],
        rest: [+v1.x.toFixed(4), +v1.y.toFixed(4), +v1.z.toFixed(4)] });
    }
    out.inv1 = Array.from(skel.boneInverses[1].elements).map(x => +x.toFixed(6));
    // restore
    skel.boneMatrices.set(saved);
    mercObj.rotation.x = keepR; mercObj.position.copy(keepP); mercObj.scale.copy(keepS);
    mercObj.updateMatrixWorld(true); skel.update();
    return out;
  }

function captureSkinnedFrames(smIo, mercObj, mixer, actions, clips) {
  try {
    log('IoU2-start clips=' + clips.length);
    const geo = smIo.geometry;
    const NVi = geo.attributes.position.count;
    const vTmp = new THREE.Vector3();
    const skinAll = () => { const out = new Float32Array(NVi * 3);
      for (let i = 0; i < NVi; i++) { smIo.applyBoneTransform(i, vTmp);
        out[i*3] = vTmp.x; out[i*3+1] = vTmp.y; out[i*3+2] = vTmp.z; }
      return out; };
    // s61 T3 fix: the CPU applyBoneTransform chain = bindMatrixInverse x boneWorld x invB x bindMatrix
    // with bindMatrix = identity (loader bind) -> any mesh transform applied AFTER bind leaks into
    // the CPU result. Zero the mesh transform for the capture (file space = bind verts space).
    const __rot0 = mercObj.rotation.x, __pos0 = mercObj.position.clone();
    mercObj.rotation.set(0, 0, 0); mercObj.position.set(0, 0, 0);
    mercObj.updateMatrixWorld(true); smIo.skeleton.update();
    const rest = skinAll();
    const pa = geo.attributes.position.array;
    let restMaxDev = 0;
    for (let i = 0; i < NVi * 3; i++) restMaxDev = Math.max(restMaxDev, Math.abs(rest[i] - pa[i]));
    const SZ = 256, GRID = 64;
    const cv = document.createElement('canvas'); cv.width = SZ; cv.height = SZ;
    const gl = cv.getContext('webgl', { preserveDrawingBuffer: true });
    const sh = (t, s2) => { const o = gl.createShader(t); gl.shaderSource(o, s2); gl.compileShader(o); return o; };
    const prog = gl.createProgram();
    gl.attachShader(prog, sh(gl.VERTEX_SHADER, 'attribute vec2 q; void main(){ gl_Position = vec4(q, 0.0, 1.0); }'));
    gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, 'void main(){ gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0); }'));
    gl.linkProgram(prog); gl.useProgram(prog);
    const loc = gl.getAttribLocation(prog, 'q');
    gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    gl.viewport(0, 0, SZ, SZ); gl.clearColor(0, 0, 0, 1);
    const vb = gl.createBuffer(), ib = gl.createBuffer();
    const ia = geo.index.array, IN = geo.index.count;
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ib); gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, ia, gl.STATIC_DRAW);
    // fixed projection: scale from the REST cpu-skin bbox; each frame recentred on the
    // PELVIS bone world position (root-relative - the root-motion channel is cm-scale)
    let rmnx = 1e9, rmxx = -1e9, rmnz = 1e9, rmxz = -1e9;
    for (let i = 0; i < NVi; i++) { rmnx = Math.min(rmnx, rest[i*3]); rmxx = Math.max(rmxx, rest[i*3]);
      rmnz = Math.min(rmnz, rest[i*3+2]); rmxz = Math.max(rmxz, rest[i*3+2]); }
    const rsc = Math.min(2.0 / Math.max(1e-6, rmxx - rmnx), 2.0 / Math.max(1e-6, rmxz - rmnz)) * 0.9;
    const pelvis = smIo.skeleton.bones.find(b => /pelvis/i.test(b.name || '')) || smIo.skeleton.bones[0];
    const pv = new THREE.Vector3();
    const raster = (vAll) => {
      pelvis.getWorldPosition(pv);
      const ccx = pv.x, ccz = pv.z;
      let mnx = 1e9, mxx = -1e9, mnz = 1e9, mxz = -1e9;
      for (let i = 0; i < NVi; i++) { mnx = Math.min(mnx, vAll[i*3]); mxx = Math.max(mxx, vAll[i*3]);
        mnz = Math.min(mnz, vAll[i*3+2]); mxz = Math.max(mxz, vAll[i*3+2]); }
      const xy = new Float32Array(NVi * 2);
      for (let i = 0; i < NVi; i++) { xy[i*2] = (vAll[i*3] - ccx) * rsc; xy[i*2+1] = (vAll[i*3+2] - ccz) * rsc; }
      gl.bindBuffer(gl.ARRAY_BUFFER, vb); gl.bufferData(gl.ARRAY_BUFFER, xy, gl.STATIC_DRAW);
      gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
      gl.clear(gl.COLOR_BUFFER_BIT);
      gl.drawElements(gl.TRIANGLES, IN, gl.UNSIGNED_SHORT, 0);
      const px = new Uint8Array(SZ * SZ * 4);
      gl.readPixels(0, 0, SZ, SZ, gl.RGBA, gl.UNSIGNED_BYTE, px);
      let lit = 0;
      for (let i = 0; i < SZ * SZ; i++) if (px[i*4] > 32) lit++;
      let hex = '';
      for (let gy = 0; gy < GRID; gy++) for (let gx = 0; gx < GRID / 8; gx++) {
        let b = 0;
        for (let gy2 = 0; gy2 < 4; gy2++) for (let gx2 = 0; gx2 < 8; gx2++) {
          for (let sy = 0; sy < 4; sy++) for (let sx2 = 0; sx2 < 4; sx2++) {
            const X = (gx * 8 + gx2) * 4 + sx2, Y = (GRID - 1 - gy) * 4 + gy2;
            const o = (Y * SZ + X) * 4;
            if (px[o] > 32) { b |= 1 << (gy2 * 8 + gx2); sy = 4; sx2 = 4; }
          }
        }
        hex += ('0000000' + (b >>> 0).toString(16)).slice(-8);
      }
      return { gridHex: hex, lit, height: +(mxz - mnz).toFixed(4), feetZ: +mnz.toFixed(4) };
    };
    const frames = {};
    for (const nm of clips) {
      const a = actions[nm]; if (!a) continue;
      for (const nm2 of clips) { const a2 = actions[nm2];
        if (a2) { a2.setEffectiveWeight(0); if (a2.isRunning()) a2.stop(); } }
      a.reset(); a.setEffectiveWeight(1); a.play();
      const dur = a.getClip().duration;
      const fr = []; let prev = null;
      for (const frac of [0.25, 0.5, 0.75]) {
        a.time = frac * dur; mixer.update(0);
        mercObj.updateMatrixWorld(true); smIo.skeleton.update();
        const vAll = skinAll();
        const r = raster(vAll);
        let fd = 0;
        if (prev) { let s3 = 0; for (let i = 0; i < vAll.length; i++) s3 += Math.abs(vAll[i] - prev[i]);
          fd = +(s3 / NVi).toFixed(4); }
        prev = vAll;
        fr.push(Object.assign({ frac, frameDisp: fd, nVerts: NVi }, r));
      }
      frames[nm] = fr;
      a.setEffectiveWeight(0); a.stop();
    }
    // wrong-clip control v2: mean |idle_skin - walk_skin| at frac 0.25 (vertex space)
    let skinDiff = -1;
    try {
      const A = actions[clips[0]], B = actions[clips[1]];
      const snap = (act, frac) => {
        for (const nm2 of clips) { const a2 = actions[nm2];
          if (a2) { a2.setEffectiveWeight(0); if (a2.isRunning()) a2.stop(); } }
        act.reset(); act.setEffectiveWeight(1); act.play();
        act.time = frac * act.getClip().duration; mixer.update(0);
        mercObj.updateMatrixWorld(true); smIo.skeleton.update();
        return skinAll();
      };
      const va = snap(A, 0.25), vbw = snap(B, 0.25);
      let sd = 0;
      for (let i = 0; i < va.length; i++) sd += Math.abs(va[i] - vbw[i]);
      skinDiff = +(sd / va.length).toFixed(4);
      A.setEffectiveWeight(0); A.stop(); B.setEffectiveWeight(0); B.stop();
    } catch (eSD) { log('IoU2 skinDiff fail: ' + (eSD && eSD.message)); }
    let gridDiff = -1;
    if (frames[clips[0]] && frames[clips[1]]) {
      const A = frames[clips[0]][0].gridHex, B = frames[clips[1]][0].gridHex;
      let d = 0;
      for (let i = 0; i < A.length; i += 8) {
        const x = (parseInt(A.slice(i, i + 8), 16) ^ parseInt(B.slice(i, i + 8), 16)) >>> 0;
        d += x.toString(2).split('1').length - 1;
      }
      gridDiff = d;
    }
    mercObj.rotation.x = __rot0; mercObj.position.copy(__pos0);
    mercObj.updateMatrixWorld(true); smIo.skeleton.update();
    // s62 T2: dump posed bone worlds + skinned verts per captured frame (numpy cross-check)
    const bwDump = {};
    try {
      const BW = new Float32Array(smIo.skeleton.boneMatrices); // boneWorld x boneInverse (THREE convention)
      const worldDump = [];
      for (let i = 0; i < smIo.skeleton.bones.length; i++)
        worldDump.push(Array.from(smIo.skeleton.bones[i].matrixWorld.elements));
      const vDump = {};
      for (const nm of clips) {
        const a = actions[nm]; if (!a) continue;
        for (const nm2 of clips) { const a2 = actions[nm2];
          if (a2) { a2.setEffectiveWeight(0); if (a2.isRunning()) a2.stop(); } }
        a.reset(); a.setEffectiveWeight(1); a.play();
        const dur = a.getClip().duration;
        a.time = 0.25 * dur; mixer.update(0);
        mercObj.updateMatrixWorld(true); smIo.skeleton.update();
        vDump[nm] = Array.from(skinAll()).map(x => +x.toFixed(4));
        a.setEffectiveWeight(0); a.stop();
      }
      bwDump.boneMatrices = Array.from(BW).map(x => +x.toFixed(6));
      bwDump.worlds = worldDump.map(w => w.map(x => +x.toFixed(6)));
      bwVerts = vDump;
    } catch (eBW) { log('bwDump fail: ' + (eBW && eBW.message)); }
    var bwVerts = bwVerts || {};
    const __res = { ok: true, restMaxDev: +restMaxDev.toFixed(5), nVerts: NVi, frames, gridDiff,
      skinDiff, glErr: gl.getError(), bw: bwDump, bwVerts };
    log('IoU2-done restMaxDev=' + __res.restMaxDev + ' clips=' + Object.keys(frames).length + ' gridDiff=' + gridDiff);
    return __res;
  } catch (e4) {
    log('enemyIoU2 FAILED: ' + (e4 && e4.message || e4));
    return { ok: false, error: String(e4 && e4.message || e4) };
  }
}
async function loadMerc(zipBuf, findM) {
  const aMem = await glaSliceLazy(zipBuf, zmembersGet(findM(/data\/actors\.gla$/i)),
    new Set(['Bane_mercenary.bdae', 'batman_anims.bdae']));
  const atM = zmembersGet(findM(/textures\/actors_tex\.gla$/i));
  const atIdx = await glaIndexLazy(zipBuf, atM);
  const atWant = 'chara_banemercenarya_c.tga';
  const atEnt = atIdx.get(atWant);
  let atBytes = atEnt ? (await streamInflateRanges(zipBuf, atM, [{ o: atEnt.o, s: atEnt.s }]))[0] : null;
  atIdx.clear();
  const skin = TDKR.readBdae2(aMem['Bane_mercenary.bdae']);  // s59 T2: layout from the file's own headers
  const A = TDKR.decodeAnims(aMem['batman_anims.bdae']);
  log('LZ Bane_mercenary.bdae bytes=' + aMem['Bane_mercenary.bdae'].length +
      ' verts=' + skin.verts.length / 3 + ' joints=' + (skin.jointNodes ? skin.jointNodes.length : -1));
  let texture = null;
  if (atBytes) {
    const td = atBytes;
    const th = td[4] | (td[5] << 8) | (td[6] << 16) | (td[7] << 24);
    const tw = td[8] | (td[9] << 8) | (td[10] << 16) | (td[11] << 24);
    const px = td.subarray(52, 52 + tw * th * 3);
    const rgba = new Uint8Array(tw * th * 4);
    for (let i = 0; i < tw * th; i++) {
      rgba[i*4] = px[i*3]; rgba[i*4+1] = px[i*3+1]; rgba[i*4+2] = px[i*3+2]; rgba[i*4+3] = 255;
    }
    texture = new THREE.DataTexture(rgba, tw, th, THREE.RGBAFormat);
    texture.colorSpace = THREE.SRGBColorSpace; texture.needsUpdate = true; texture.flipY = false;
    log('chara_banemercenarya_c: ' + tw + 'x' + th + ' decoded');
  }
  atBytes = null;
  const byNameC = Object.fromEntries(A.clips.map(c => [c.name, c]));
  const missing = ENEMY_CLIPS.filter(nm => !byNameC[nm]);
  if (missing.length) throw new Error('enemy clips missing: ' + missing.join(','));
  const glbBytes = buildGLB(skin, A, byNameC, ENEMY_CLIPS);
  const g = await new Promise((res, rej) => new GLTFLoader().parse(glbBytes.buffer, '', res, rej));
  merc = g.scene;
  { // s60 T3: capture the rest pose BEFORE the root transform (bind = parse-time world)
    const smR = (() => { let s = null; merc.traverse(o => { if (o.isSkinnedMesh) s = o; }); return s; })();
    mercRestIoU = smR ? captureRestIoU(smR) : { ok: false, error: 'no skinned mesh' };
  // s61 T3: posed skinned capture (root-cause fix proof + per-clip posed frames)

  }
  merc.rotation.x = -Math.PI / 2;
  merc.position.set(P.x + 2.0, P.y, P.z);
  bScene.add(merc);
  mercMixer = new THREE.AnimationMixer(merc);
  for (const c of g.animations) mercActions[c.name] = mercMixer.clipAction(c);
  const sm = (() => { let s = null; merc.traverse(o => { if (o.isSkinnedMesh) s = o; }); return s; })();
  if (texture && sm) { sm.material.map = texture; sm.material.color.set(0xffffff); sm.material.needsUpdate = true; }
  mercSeq = { t0: performance.now(), phase: 0, wraps: 0, zmin: 1e9, zmax: -1e9, lastT: 0 };
  mercSeq.restIoU = mercRestIoU;
  // s59 T2: CPU-skin probe (vertex displacement gate). applyBoneTransform on a
  // subset; per-phase mean |delta|; wrong-clip negative control at report time.
  mercSkinProbe = null; mercDisp = { byClip: {} };
  {
    const sm0 = (() => { let s = null; merc.traverse(o => { if (o.isSkinnedMesh) s = o; }); return s; })();
    if (sm0 && sm0.geometry.attributes.position) {
      const nV = sm0.geometry.attributes.position.count;
      const step = Math.max(1, Math.floor(nV / 150));
      const idxs = [];
      for (let i = 0; i < nV && idxs.length < 150; i += step) idxs.push(i);
      mercSkinProbe = { sm: sm0, idxs, v: new THREE.Vector3() };
    }
  }
  const idle = mercActions[ENEMY_CLIPS[0]]; idle.play(); idle.setEffectiveWeight(1);
  // s60 T3: Hurt/Death are one-shot clips (LoopOnce + clamp)
  mercActions['_223_enemy_hurtl'].loop = THREE.LoopOnce;
  mercActions['_223_enemy_hurtl'].clampWhenFinished = true;
  mercActions['_250_enemy_death1'].loop = THREE.LoopOnce;
  mercActions['_250_enemy_death1'].clampWhenFinished = true;
  // s61 T3: posed skinned capture (after mixer + actions exist; root-cause fix proof)
  try {
    const smI2 = (() => { let s5 = null; merc.traverse(o => { if (o.isSkinnedMesh) s5 = o; }); return s5; })();
    if (smI2) {
      log('IoU2-call');
      window.__GATE.enemyIoU2 = captureSkinnedFrames(smI2, merc, mercMixer, mercActions, ENEMY_CLIPS);
      try { window.__GATE.bindBisect = captureBindBisect(smI2, merc); } catch (eBB) {
        window.__GATE.bindBisect = { ok: false, error: String(eBB && eBB.message || eBB) }; }
    } else window.__GATE.enemyIoU2 = { ok: false, error: 'no skinned mesh' };
  } catch (eI2) { log('IoU2-throw: ' + (eI2 && eI2.message)); window.__GATE.enemyIoU2 = { ok: false, error: String(eI2 && eI2.message) }; }
  return { verts: skin.verts.length / 3, joints: skin.jointNodes ? skin.jointNodes.length : -1,
           clips: g.animations.filter(a => ENEMY_CLIPS.indexOf(a.name) >= 0).map(a => a.name) };
}
function mercTick(now) {
  if (!merc || !mercSeq) return;
  const t = (now - mercSeq.t0) / 1000;
  const phase = t < 4 ? 0 : (t < 8 ? 1 : (t < 12 ? 2 : (t < 14 ? 3 : 4)));
  if (phase !== mercSeq.phase) {
    mercSeq.phase = phase;
    for (const nm of ENEMY_CLIPS) mercActions[nm].setEffectiveWeight(0);
    const a = mercActions[ENEMY_CLIPS[phase]]; a.setEffectiveWeight(1); a.play();
  }
  mercMixer.update(1 / 60);
  if (mercActions[ENEMY_CLIPS[mercSeq.phase]].time < mercSeq.lastT - 0.001) mercSeq.wraps++;
  mercSeq.lastT = mercActions[ENEMY_CLIPS[mercSeq.phase]].time;
  let bb = new THREE.Box3().setFromObject(merc);
  if (isFinite(bb.min.z)) { mercSeq.zmin = Math.min(mercSeq.zmin, bb.min.z); mercSeq.zmax = Math.max(mercSeq.zmax, bb.max.z); }
  // s59 T2: per-phase mean vertex displacement (CPU skinning on the subset)
  if (mercSkinProbe) {
    const pr = mercSkinProbe, out = new Float32Array(pr.idxs.length * 3);
    for (let k = 0; k < pr.idxs.length; k++) {
      pr.sm.applyBoneTransform(pr.idxs[k], pr.v);
      out[k*3] = pr.v.x; out[k*3+1] = pr.v.y; out[k*3+2] = pr.v.z;
    }
    if (mercSeq.lastSkin && mercSeq.lastSkin.length === out.length) {
      let s = 0;
      for (let i = 0; i < out.length; i++) s += Math.abs(out[i] - mercSeq.lastSkin[i]);
      const nm = ENEMY_CLIPS[mercSeq.phase];
      if (!mercDisp.byClip[nm]) mercDisp.byClip[nm] = { sum: 0, n: 0 };
      mercDisp.byClip[nm].sum += s / pr.idxs.length; mercDisp.byClip[nm].n++;
    }
    mercSeq.lastSkin = out;
  }
  if (t > 20 && !mercSeq.reported && mercSkinProbe) {
    mercSeq.reported = true;
    // negative control: sample the WRONG clip (walk) labeled as the idle slot;
    // its displacement must differ from the measured enemy idle.
    const ctlClip = ENEMY_CLIPS[1];
    for (const nm of ENEMY_CLIPS) mercActions[nm].setEffectiveWeight(0);
    const ca = mercActions[ctlClip]; ca.setEffectiveWeight(1); ca.play();
    let ctlSum = 0, ctlN = 0, prev = null;
    for (let f = 0; f < 30; f++) {
      mercMixer.update(1 / 60);
      merc.updateMatrixWorld(true);   // no render here: refresh bone world matrices for the probe
      if (mercSkinProbe) {
        const pr = mercSkinProbe, out = new Float32Array(pr.idxs.length * 3);
        for (let k = 0; k < pr.idxs.length; k++) {
          pr.sm.applyBoneTransform(pr.idxs[k], pr.v);
          out[k*3] = pr.v.x; out[k*3+1] = pr.v.y; out[k*3+2] = pr.v.z;
        }
        if (prev) { let s = 0; for (let i = 0; i < out.length; i++) s += Math.abs(out[i] - prev[i]);
          ctlSum += s / pr.idxs.length; ctlN++; }
        prev = out;
      }
    }
    ca.setEffectiveWeight(0);
    const disp = {};
    for (const k of Object.keys(mercDisp.byClip)) disp[k] = +(mercDisp.byClip[k].sum / Math.max(1, mercDisp.byClip[k].n)).toFixed(5);
    const dispCtl = +(ctlSum / Math.max(1, ctlN)).toFixed(5);
    const dIdle = disp[ENEMY_CLIPS[0]], dWalk = disp[ENEMY_CLIPS[1]], dRun = disp[ENEMY_CLIPS[2]];
    const dHurt = disp[ENEMY_CLIPS[3]], dDeath = disp[ENEMY_CLIPS[4]];
    // one-shot finished: action time pinned at (or past) clip duration
    const hurtDur = mercActions[ENEMY_CLIPS[3]].getClip().duration;
    const deathDur = mercActions[ENEMY_CLIPS[4]].getClip().duration;
    const hurtT = mercActions[ENEMY_CLIPS[3]].time;
    const deathT = mercActions[ENEMY_CLIPS[4]].time;
    const hurtDone = hurtT >= hurtDur * 0.95;
    const deathDone = deathT >= deathDur * 0.95;
    const okGate = isFinite(dIdle) && isFinite(dWalk) && isFinite(dRun) && isFinite(dispCtl) &&
      dIdle > 0 && dWalk > 0 && dRun > 0 && Math.abs(dispCtl - dIdle) > 1e-4 &&
      isFinite(dHurt) && dHurt > 0 && isFinite(dDeath) && dDeath > 0 && hurtDone && deathDone;
    window.__GATE.enemyPlay = { ok: okGate, wraps: mercSeq.wraps, phasesSeen: mercSeq.phase + 1,
      bboxZmin: +mercSeq.zmin.toFixed(3), bboxZmax: +mercSeq.zmax.toFixed(3),
      clip: ENEMY_CLIPS[mercSeq.phase], dmg: ENEMY_DMG,
      dispIdle: dIdle, dispWalk: dWalk, dispRun: dRun,
      dispHurt: dHurt, dispDeath: dDeath,
      hurtDur: +hurtDur.toFixed(3), deathDur: +deathDur.toFixed(3),
      hurtT: +hurtT.toFixed(3), deathT: +deathT.toFixed(3),
      hurtDone, deathDone, dispCtlWrongClip: dispCtl,
      ctlClip, probeVerts: mercSkinProbe ? mercSkinProbe.idxs.length : 0 };
    log('enemy playback: wraps=' + mercSeq.wraps + ' disp=' + JSON.stringify(disp) + ' ctlWrong=' + dispCtl +
        ' bboxZ=[' + mercSeq.zmin.toFixed(2) + ',' + mercSeq.zmax.toFixed(2) + ']');
    window.__GATE.enemyIoU = mercSeq.restIoU || { ok: false, error: 'rest capture missing' };
    if (window.__GATE.pendingFinalize && !window.__GATE.done) {
      const extra = window.__GATE.pendingFinalize; window.__GATE.pendingFinalize = null;
      finalizeGate(extra);
    }
  }
}
function zmembersGet(key) {
  if (!key) throw new Error('zip member not found');
  return zipMembersCache.get(key);
}

let zipMembersCache = null;

/* ================= playback state ================= */
const P = { x: 0, y: 0, z: 0.9, speed: 0 };
const cam = { cx: 0, cz: 0 };
const WALK_SPEED = 1.6;
const capsule = { wi: 1, moving: false, lastMoving: null, wpts: [], ping: 1 };
let batches = [];
let readyAt = 0;
const SAMP = { idleA: null, idleB: null, idleDone: false, s: [], plan: [] };

function crop64() {
  const C = 64;
  const buf = new Uint8Array(C * C * 4);
  G.readPixels(W / 2 - C / 2, H / 2 - C / 2, C, C, G.RGBA, G.UNSIGNED_BYTE, buf);
  let sum = 0;
  for (let i = 0; i < buf.length; i++) sum += buf[i];
  return { buf, sum };
}
function diffCrop(a, b) {
  let d = 0;
  for (let i = 0; i < a.buf.length; i++) d += Math.abs(a.buf[i] - b.buf[i]);
  return d;
}
function canvasStats() {
  const buf = new Uint8Array(W * H * 4);
  G.readPixels(0, 0, W, H, G.RGBA, G.UNSIGNED_BYTE, buf);
  let s = 0, s2 = 0;
  const n = W * H;
  for (let i = 0; i < n; i++) {
    const g2 = (buf[i*4] + buf[i*4+1] + buf[i*4+2]) / 3;
    s += g2; s2 += g2 * g2;
  }
  const mean = s / n;
  return { mean: +mean.toFixed(3), std: +Math.sqrt(Math.max(0, s2/n - mean*mean)).toFixed(3) };
}
function silhouetteCount() {
  const gl = bRenderer.getContext();
  const buf = new Uint8Array(320 * 240 * 4);
  gl.readPixels(0, 0, 320, 240, gl.RGBA, gl.UNSIGNED_BYTE, buf);
  let cnt = 0;
  for (let i = 0; i < 320 * 240; i++) {
    const r = buf[i*4], g2 = buf[i*4+1], b = buf[i*4+2];
    if (Math.min(r, g2, b) < 200) cnt++;
  }
  return cnt;
}
function startPlayback(route) {
  const p = astar(route.cells[0], route.cells[1]);
  if (p === null) throw new Error('playback route has no A* path');
  const pts = p.map(c => [nmCent[c * 3], nmCent[c * 3 + 1], nmCent[c * 3 + 2]]);
  capsule.wpts = pts.concat(pts.slice(1, -1).reverse());   // ping-pong loop
  const [sp, why] = snap_spawn_nm([pts[0][0], pts[0][1], 0.9]);
  if (sp === null) throw new Error('playback spawn failed: ' + why);
  P.x = sp[0]; P.y = sp[1]; P.z = sp[2] + 0.9;
  cam.cx = P.x; cam.cz = P.y;
  capsule.wi = 1;
  log('playback: route ' + route.route + ' (' + pts.length + ' cells, expected ' + route.expected +
      ' ' + route.expected_dist + ' m) from ' + P.x.toFixed(1) + ',' + P.y.toFixed(1));
}
function stepCapsule(dt) {
  let remaining = WALK_SPEED * dt;
  capsule.moving = false;
  let guard = 0;
  while (remaining > 1e-4 && guard++ < 10) {
    const tgt = capsule.wpts[capsule.wi];
    if (!tgt) { capsule.wpts.reverse(); capsule.wi = 1; continue; }
    const dx = tgt[0] - P.x, dy = tgt[1] - P.y;
    const d = Math.hypot(dx, dy);
    if (d < 0.05) { capsule.wi++; continue; }
    const step = Math.min(remaining, d);
    const nx = P.x + dx / d * step, ny = P.y + dy / d * step;
    const sp2 = [nx, ny, P.z];
    const gz2 = nm_ground(nx, ny, P.z + 2.6);
    if (gz2 > -1e8 && !blocked(sp2) && gz2 - (P.z - 0.9) < 0.85) {
      P.x = nx; P.y = ny; P.z = gz2 + 0.9;
      remaining -= step;
      capsule.moving = true;
      capsule.dirx = dx / d; capsule.diry = dy / d;
    } else {
      const sl = try_slide(P, dx / d * step, dy / d * step, step);
      if (sl !== null && sl[1] > 0.01) {
        P.x = sl[0][0]; P.y = sl[0][1]; P.z = sl[0][2] + 0.9;
        remaining -= Math.min(remaining, sl[1]);
        capsule.moving = true;
        capsule.dirx = dx / d; capsule.diry = dy / d;
      } else {
        capsule.wi++;   // playback: skip blocked waypoint (harness itself stops; recorded honestly)
      }
    }
  }
}

/* ================= gate finalization ================= */
const T0GLOBAL = performance.now();
function finalizeGate(extra) {
  const g = window.__GATE;
  Object.assign(g, extra || {});
  g.consoleErrors = window.__consoleErrors.slice(0, 10);
  g.heap_mb = heapMB();
  g.heap_mb_peak = Math.max(heapMB(), ...(g.heapSamples.filter(x => x > 0)));
  g.wall_ms = Math.round(performance.now() - T0GLOBAL);
  g.ready = true;
  // s59 T2: in enemy mode, hold `done` until the merc playback report exists
  // (mercTick runs inside the rAF loop, which stops at done), then finish.
  if (QS2.get('enemy') === '1' && !g.enemyPlay) {
    g.pendingFinalize = extra || {};
    return;
  }
  g.done = true;
}

/* ================= main ================= */
document.querySelector('#f').addEventListener('change', async (ev) => {
  try {
    const t0 = performance.now();
    const corrupt = new URLSearchParams(location.search).get('corrupt') === '1';
    window.__GATE.corruptControl = corrupt;
    const zfile = ev.target.files[0];
    const tailBuf = new Uint8Array(await zfile.slice(Math.max(0, zfile.size - 66000)).arrayBuffer());
    let eocd = -1;
    for (let i = tailBuf.length - 22; i >= 0; i--)
      if (u32le(tailBuf, i) === 0x06054b50) { eocd = i; break; }
    if (eocd < 0) throw new Error('no EOCD (lazy)');
    const nEnt = u16le(tailBuf, eocd + 10), cdOff = u32le(tailBuf, eocd + 16), cdSize = u32le(tailBuf, eocd + 12);
    const cdBuf = new Uint8Array(await zfile.slice(cdOff, cdOff + cdSize).arrayBuffer());
    const cdWrap = new Uint8Array(cdSize + 22);
    cdWrap.set(cdBuf, 0);
    const dvE = new DataView(cdWrap.buffer, cdSize, 22);
    dvE.setUint32(0, 0x06054b50, true);
    dvE.setUint16(4, 0, true); dvE.setUint16(6, 0, true);
    dvE.setUint16(8, nEnt, true); dvE.setUint16(10, nEnt, true);
    dvE.setUint32(12, cdSize, true); dvE.setUint32(16, 0, true);
    dvE.setUint16(20, 0, true);
    const zmembers = zipMembers(cdWrap);
    zipMembersCache = zmembers;
    const findM = (re) => { for (const k of zmembers.keys()) if (re.test(k)) return k; return null; };
    log('zip (lazy): ' + (zfile.size / 1e6).toFixed(0) + ' MB, ' + zmembers.size + ' members, heap ' + heapMB() + ' MB');

    /* ---- (2) walker data from the USER's files ---- */
    const gc = await zipReadLazy(zfile, zmembersGet(findM(/data\/game_config\.gla$/i)));
    const nmBytes = TDKR.glaSlice(gc, new Set(['GothamCity_502299_navdata.nm']))['GothamCity_502299_navdata.nm'];
    if (!nmBytes) throw new Error('navdata member GothamCity_502299_navdata.nm not found in game_config.gla');
    if (corrupt) {
      for (let b = 2; b < 14; b++) nmBytes[b] = (b % 2) ? 0xc8 : 0xc9;
      log('NEGATIVE CONTROL: navmesh bytes corrupted (?corrupt=1)');
    }
    const chk = loadNavmesh(nmBytes);
    window.__GATE.nmSelfCheck = chk.ok;
    log('.nm parsed from YOUR zip: vcount=' + chk.vcount + ' ccount=' + chk.ccount +
        ' self-check ' + (chk.ok ? 'PASS' : 'FAIL'));
    if (!chk.ok) { finalizeGate({ failReason: 'nm_self_check_failed' }); return; }
    const lvcBytes = TDKR.glaSlice(gc, new Set(['GothamCity.lvc']))['GothamCity.lvc'];
    if (!lvcBytes) throw new Error('member GothamCity.lvc not found in game_config.gla');
    const [table, gol] = await Promise.all([
      fetch('./lvc_readseq_s30.json').then(r => r.json()),
      fetch('./lvc_gol_templates.json').then(r => r.json())]);
    const built = buildSoupFromLvc(lvcBytes, table, gol);
    const dig = await crypto.subtle.digest('SHA-256', built.buf);
    const soupSha = [...new Uint8Array(dig)].map(b => b.toString(16).padStart(2, '0')).join('');
    const SOUP_SHA = '00ce7970e45adc854ac7cae6d0f97797b602342d101e1ecb5eb1c2c01016beb8';
    const soupDigestPass = (soupSha === SOUP_SHA) && built.nTri === 137893;
    window.__GATE.soupDigestPass = soupDigestPass;
    window.__GATE.soup = { nTri: built.nTri, sha256: soupSha };
    log('soup built from YOUR lvc: ' + built.nTri + ' tris / ' + built.nObj + ' objects, sha256 ' +
        (soupDigestPass ? 'PASS' : 'FAIL'));
    if (!soupDigestPass) { finalizeGate({ failReason: 'soup_digest_mismatch' }); return; }
    loadSoup(built.buf);
    const routes = runRouteCheck();
    window.__GATE.routes = routes;
    log('route check vs harness: ' + routes.agree + '/' + routes.run + ' agree (' +
        Math.round(routes.results.reduce((a, r) => a + r.ms, 0)) + ' ms)');
    for (const r of routes.results) log('  route ' + r.route + ': ' + r.verdict + ' d=' + r.dist +
        ' (expected ' + r.expected + ' ' + r.expected_dist + ') ' + (r.agree ? 'OK' : 'MISMATCH'));

    /* ---- s54 T2: REAL grapple-target anchors (CWayPointObject records) ----
     * Session 53 established the engine's grapple targets are object-anchor
     * virtuals (CWayPointObject::GetGrapnelTargetPosition @0x2a9024), NOT
     * navmesh edge flags. Decode the waypoint records (engine cases 0x798f /
     * 0x2666 / 0x4741) from YOUR lvc and offer them to the ?s5=1 slice. */
    if (S5ON) {
      try {
        const plv2 = (typeof parseLvc !== 'undefined') ? parseLvc
                   : (typeof TDKRLvc !== 'undefined' ? TDKRLvc.parseLvc : null);
        const res2 = plv2(lvcBytes, table, gol, {});
        const dv2 = new DataView(lvcBytes.buffer, lvcBytes.byteOffset, lvcBytes.byteLength);
        const wps = [];
        for (const r of res2.records) {
          if (r.tid === 0x798f || r.tid === 0x2666 || r.tid === 0x4741) {
            const p = r.start + 4;   // tid | i oid | c flag | 3f pos (BE)
            wps.push({ oid: dv2.getInt32(p, false), flag: lvcBytes[p + 4],
                       x: dv2.getFloat32(p + 5, false), y: dv2.getFloat32(p + 9, false),
                       z: dv2.getFloat32(p + 13, false) });
          }
        }
        window.__S5WPS = wps;
        log('S5 grapple anchors: ' + wps.length + ' CWayPointObject records decoded (s54 T2)');
      } catch (e2) { log('S5 waypoint decode failed: ' + e2.message); }
    }

    /* ---- (1) zone data + batches (city_zone2 path) ---- */
    const glaM = zmembersGet(findM(/data\/l_gothamcity\.gla$/i));
    const glaIdx = await glaIndexLazy(zfile, glaM);
    const gczEnt = glaIdx.get('GothamCity.zip');
    if (!gczEnt) throw new Error('GothamCity.zip not in l_gothamcity.gla (lazy)');
    let gcityZip = (await streamInflateRanges(zfile, glaM,
      [{ o: gczEnt.o, s: gczEnt.s }]))[0];
    const gmembers = zipMembers(gcityZip);
    const gget = (nm) => { const m = gmembers.get(nm); if (!m) throw new Error('GothamCity.zip missing ' + nm); return zipRead2(gcityZip, m); };
    let lt = await gget('lod_table.bin');
    let ldd = await gget('lod_data.bin');
    let bi8 = await gget('batch_info.bin');
    let mb = await gget('GothamCity_materials.bdae');
    // s52 T4: detach the method-0 views and release the 41 MB zip shell BEFORE the long build
    ldd = new Uint8Array(ldd); lt = new Uint8Array(lt); bi8 = new Uint8Array(bi8); mb = new Uint8Array(mb);
    gcityZip = null; gmembers.clear();
    let le = await zipRead2(mb, zipMembers(mb).get('little_endian_not_quantized.bdae'));
    // s52 T4: l_gothamcity_tex.gla (199 MB) NEVER materialized: index + per-member ranges
    const bindPre = parseCompiledTable(le);
    const texM = zmembersGet(findM(/textures\/l_gothamcity_tex\.gla$/i));
    const texIdx = await glaIndexLazy(zfile, texM);
    const lowMap = new Map(); for (const nm2 of texIdx.keys()) lowMap.set(nm2.toLowerCase(), nm2);
    const wantSet = new Set(); let wantMiss = [];
    for (let i = 0; i < 307; i++) {
      for (const t of bindPre.bind[i]) {
        if (!t) continue;
        const act = lowMap.get(t.toLowerCase());
        if (act) wantSet.add(act); else wantMiss.push(t);
      }
    }
    if (POOLCHUNK) {
      // s53 T4: chunked capture -> decode -> one-shot pre-upload map; the ~100 MB compressed pool
      // and the decoded LRU are never materialized. Alpha arrays are kept ONLY for the AlphaMasking
      // diffuse names (the sole consumer, alphaTexOf at prepare time).
      preTex = new Map();
      const alphaNeed = new Set();
      for (let i = 0; i < 307; i++) {
        if (bindPre.fx[i] === 'AlphaMasking' && bindPre.bind[i] && bindPre.bind[i][0])
          alphaNeed.add(bindPre.bind[i][0].toLowerCase());
      }
      const names = Array.from(wantSet); const CH = 28; let chB = 0;   // s53 T4: 28-member chunks (4 rounds) - fewer await round-trips, same peak profile
      for (let i = 0; i < names.length; i += CH) {
        const ch = names.slice(i, i + CH);
        const rs = ch.map(n => { const e3 = texIdx.get(n); return { o: e3.o, s: e3.s }; });
        const bs = await streamInflateRanges(zfile, texM, rs);
        for (let j = 0; j < ch.length; j++) {
          chB += bs[j] ? bs[j].length : 0;
          try {
            const parts = unwrapSplitParts(bs[j]);
            const rgb = decodePvr(parts['rgb.pvr'] || parts['rgb']);
            // s53 T4 fix: upload to GL INSIDE the chunk loop; only the GL handle (+alpha for
            // AlphaMasking) survives. Decoded CPU bytes and compressed bytes are dropped here.
            const tx = G.createTexture();
            G.bindTexture(G.TEXTURE_2D, tx);
            G.texImage2D(G.TEXTURE_2D, 0, G.RGBA, rgb.w, rgb.h, 0, G.RGBA, G.UNSIGNED_BYTE,
                         new Uint8Array(rgb.rgba.buffer, rgb.rgba.byteOffset, rgb.rgba.byteLength));
            G.texParameteri(G.TEXTURE_2D, G.TEXTURE_WRAP_S, G.REPEAT);
            G.texParameteri(G.TEXTURE_2D, G.TEXTURE_WRAP_T, G.REPEAT);
            G.texParameteri(G.TEXTURE_2D, G.TEXTURE_MIN_FILTER, G.NEAREST);
            G.texParameteri(G.TEXTURE_2D, G.TEXTURE_MAG_FILTER, G.NEAREST);
            const o = { tx, w: rgb.w, h: rgb.h, alpha: null, uploaded: true };
            if (alphaNeed.has(ch[j].toLowerCase()) && parts['alpha.pvr']) {
              const a = decodePvr(parts['alpha.pvr']);
              o.alpha = { w: a.w, h: a.h, data: a.rgba };
            }
            preTex.set(ch[j].toLowerCase(), o);
          } catch (e4) { /* leave absent -> texMiss (baseline decode-failure semantics) */ }
        }
      }
      window.__TEXPOOL = { members: names.length, bytes: 0, chunkedInflatedMB: Math.round(chB / 1048576), mode: 'chunked', wantMiss: wantMiss.slice(0, 8) };
      log('TEXPOOL: chunked preupload ' + names.length + ' members, ' + Math.round(chB / 1048576) + ' MB inflated in 8-member chunks (pool never held), alphaNeed ' + alphaNeed.size + ' (wantMiss ' + wantMiss.length + ')');
    } else {
      const texRanges = []; const texNames = [];
      for (const nm2 of wantSet) { const e2 = texIdx.get(nm2); texRanges.push({ o: e2.o, s: e2.s }); texNames.push(nm2); }
      const texBytes = await streamInflateRanges(zfile, texM, texRanges);
      texPool = new Map(); let poolB = 0;
      for (let i = 0; i < texNames.length; i++) { texPool.set(texNames[i].toLowerCase(), texBytes[i]); poolB += texBytes[i].length; }
      window.__TEXPOOL = { members: texNames.length, bytes: poolB, wantMiss: wantMiss.slice(0, 8) };
      log('TEXPOOL: ' + texNames.length + ' members, ' + Math.round(poolB / 1048576) + ' MB captured (wantMiss ' + wantMiss.length + ')');
    }
    texIdx.clear(); lowMap.clear();
    // s52 T5: ColorCorrection LUT from the USER zip (commons_tex.gla member 000_default.tga, RGB565 512x16)
    if (LUTON) {
      try {
        const cm = zmembersGet(findM(/textures\/commons_tex\.gla$/i));
        const cidx = await glaIndexLazy(zfile, cm);
        const ce = cidx.get('000_default.tga');
        if (!ce) throw new Error('000_default.tga not in commons_tex.gla');
        const cb = (await streamInflateRanges(zfile, cm, [{ o: ce.o, s: ce.s }]))[0];
        cidx.clear();
        const px = new Uint16Array(cb.buffer, cb.byteOffset + 52, 512 * 16);
        const rgb = new Uint8Array(512 * 16 * 4);
        for (let i = 0; i < 512 * 16; i++) {
          const p = px[i];
          rgb[i * 4] = Math.round(((p >> 11) & 0x1f) * 255 / 31);
          rgb[i * 4 + 1] = Math.round(((p >> 5) & 0x3f) * 255 / 63);
          rgb[i * 4 + 2] = Math.round((p & 0x1f) * 255 / 31);
          rgb[i * 4 + 3] = 255;
        }
        lutTex = G.createTexture(); G.bindTexture(G.TEXTURE_2D, lutTex);
        G.texImage2D(G.TEXTURE_2D, 0, G.RGBA, 512, 16, 0, G.RGBA, G.UNSIGNED_BYTE, rgb);
        G.texParameteri(G.TEXTURE_2D, G.TEXTURE_MIN_FILTER, G.LINEAR);
        G.texParameteri(G.TEXTURE_2D, G.TEXTURE_MAG_FILTER, G.LINEAR);
        G.texParameteri(G.TEXTURE_2D, G.TEXTURE_WRAP_S, G.CLAMP_TO_EDGE);
        G.texParameteri(G.TEXTURE_2D, G.TEXTURE_WRAP_T, G.CLAMP_TO_EDGE);
        window.__LUT_OK = true;
        log('LUT 000_default loaded 512x16 RGB565 (s49 CCFS mapping)');
      } catch (eL) { log('LUT load failed: ' + eL); }
    }
    const tB = performance.now();
    batches = buildBatches(lt, ldd, bi8, le);
    const tZone = performance.now() - tB;
    window.__GATE.zone = { batches: batches.length,
      texDecoded: texZstats.decoded, texMiss: window.__TEXMISS.length, buildMs: Math.round(tZone) };
    gcityZip = null; lt = null; ldd = null; bi8 = null; mb = null; le = null;
    log('zone: ' + batches.length + ' material batches built in ' + Math.round(tZone) +
        ' ms, textures decoded ' + texZstats.decoded + ' (miss ' + window.__TEXMISS.length +
        ': ' + JSON.stringify(window.__TEXMISS.slice(0, 6)) + '), heap ' + heapMB() + ' MB');

    /* ---- (3) Batman from the USER's zip ---- */
    try {
      const bInfo = await loadBatman(zfile, findM);
      window.__GATE.batman = Object.assign({ ok: true }, bInfo);
      log('batman from YOUR zip: ' + bInfo.verts + ' verts, clips ' + bInfo.clips.join(', '));
    } catch (e2) {
      window.__GATE.batman = { ok: false, error: String(e2 && e2.message || e2) };
      log('BATMAN ERROR: ' + (e2 && e2.message || String(e2)) + ' | ' + ((e2 && e2.stack) || '').slice(0, 260));
    }
    /* ---- (3b) s58 T3: enemy rig + enemy clips (?enemy=1) ---- */
    if (QS2.get('enemy') === '1') {
      try {
        const eInfo = await loadMerc(zfile, findM);
        window.__GATE.enemy = Object.assign({ ok: true, dmg: ENEMY_DMG,
          damageProvenance: 'GiveDamage(actorId,damage) 0x155e4c; census 146 literal calls, 5 x91' }, eInfo);
        log('enemy merc: ' + eInfo.verts + ' verts, ' + eInfo.joints + ' joints, clips ' + eInfo.clips.join(', '));
      } catch (e3) {
        window.__GATE.enemy = { ok: false, error: String(e3 && e3.message || e3) };
        log('ENEMY ERROR: ' + (e3 && e3.message || String(e3)));
      }
    }

    /* ---- playback: first harness-'ok' route ---- */
    const okRoute = routes.results.find(r => r.expected === 'ok');
    const playRoute = WALKTEST_ROUTES.find(r => okRoute && r.route === okRoute.route) ||
                      WALKTEST_ROUTES.find(r => r.expected === 'ok');
    startPlayback(playRoute);
    readyAt = performance.now();
    window.__GATE.first_image_ms = Math.round(performance.now() - t0);
    window.__GATE.ready = true;
    log('READY (idle control samples, then walk) — total load ' + window.__GATE.first_image_ms + ' ms, heap ' + heapMB() + ' MB');
  } catch (e) {
    log('ERROR: ' + (e && e.stack || e));
    finalizeGate({ error: String(e && e.stack || e).slice(0, 500) });
  }
});

/* ================= render loop + sampling ================= */
let last = performance.now();
function tick(now) {
  requestAnimationFrame(tick);
  const dt = Math.min(0.5, (now - last) / 1000); last = now;   // clamp 0.5: swiftshader frames are slow; keep sim on wall clock
  const g = window.__GATE;
  if (!g.ready || g.done) return;
  const el = now - readyAt;
  if (!SAMP.idleDone) {
    // idle control: capsule static, camera static -> zone canvas must be static
    const st = drawZone(batches, camWVP(cam.cx, cam.cz));
    if (!SAMP.idleA && el > 300) SAMP.idleA = crop64();
    else if (SAMP.idleA && !SAMP.idleB && el > 800) { SAMP.idleB = crop64(); SAMP.idleDone = true; }
    if (batman) { if (mixer) mixer.update(dt); if (merc) mercTick(now); bRenderer.render(bScene, bCam); }
    return;
  }
  if (SAMP.idleDone && !SAMP.walkStarted) {
    if (S5ON && !S5.started) s5Begin();
    if (S5ON && !S5.done) { s5Tick(now); if (batman && mixer) { mixer.update(dt); bRenderer.render(bScene, bCam); } return; }
    SAMP.walkStarted = true;
    startWalkPhase();
  }
  if (!SAMP.walkStarted) return;
  stepCapsule(dt);
  cam.cx = P.x; cam.cz = P.y;
  const st = drawZone(batches, camWVP(cam.cx, cam.cz));
  g.draws = st.draws; g.tris = Math.round(st.tris);
  if (batman) {
    batman.position.set(P.x, P.z - 0.9, -P.y);
    if (capsule.moving && capsule.dirx !== undefined)
      batman.rotation.y = Math.atan2(-capsule.dirx, -capsule.diry) + Math.PI;
    if (mixer) {
      const walkA = actions['_007_walk'], idleA = actions['_001_idle_stand'];
      if (capsule.moving !== capsule.lastMoving && walkA && idleA) {
        walkA.setEffectiveWeight(capsule.moving ? 1 : 0);
        idleA.setEffectiveWeight(capsule.moving ? 0 : 1);
        capsule.lastMoving = capsule.moving;
      }
      mixer.update(dt);
    }
    bCam.position.set(P.x, P.z + 1.9, -P.y + 3.8);
    bCam.lookAt(P.x, P.z - 0.75, -P.y);
    bRenderer.render(bScene, bCam);
  }
  if (merc) mercTick(now);   // s59 T2: enemy playback continues through the walk phase
  // walk samples at +2s/+4s/+6s after walk phase start
  const wel = now - SAMP.walkT0;
  const plan = [ { at: 2000 }, { at: 4000 }, { at: 6000, final: true } ];
  for (let i = 0; i < plan.length; i++) {
    if (SAMP.s.length === i && wel >= plan[i].at) {
      const smp = { t: Math.round(wel), crop: crop64(), stats: canvasStats(),
        camx: cam.cx, camy: cam.cz };
      if (plan[i].final) {
        smp.silhouette = batman ? silhouetteCount() : -1;
        smp.cameraTravelM = +Math.hypot(cam.cx - SAMP.s[0].camx, cam.cz - SAMP.s[0].camy).toFixed(1);
      }
      SAMP.s.push(smp);
    }
  }
  if (SAMP.s.length === 3 && !SAMP.walkFinished) { SAMP.walkFinished = true; finishWalk(); }
}
function startWalkPhase() {
  SAMP.walkT0 = performance.now();
  SAMP.diffIdle = diffCrop(SAMP.idleA, SAMP.idleB);
}
function finishWalk() {
  const g = window.__GATE;
  const d1 = diffCrop(SAMP.s[0].crop, SAMP.s[1].crop);
  const d2 = diffCrop(SAMP.s[1].crop, SAMP.s[2].crop);
  g.pixelStats = [SAMP.s[0].stats, SAMP.s[1].stats, SAMP.s[2].stats];
  g.camera = {
    frameDiffWalk: [d1, d2],
    frameDiffIdle: SAMP.diffIdle,
    cameraTravelM: SAMP.s[2].cameraTravelM,
    silhouettePx: SAMP.s[2].silhouette,
  };
  const sil = SAMP.s[2].silhouette;
  g.silhouetteInRange = sil >= 300 && sil <= 30000;
  g.motionDetected = d1 > 200 && d2 > 200 && d1 > 10 * Math.max(SAMP.diffIdle, 1);
  g.cameraFollowed = SAMP.s[2].cameraTravelM > 2;
  g.pass = (window.__consoleErrors.length === 0) && g.nmSelfCheck === true &&
    g.soupDigestPass === true && g.routes && g.routes.agree === g.routes.run && g.routes.run >= 4 &&
    g.batman && g.batman.ok === true && g.silhouetteInRange && g.motionDetected &&
    g.cameraFollowed && !g.corruptControl && !g.error;
  log('samples: walkDiff ' + d1 + '/' + d2 + ' vs idleDiff ' + SAMP.diffIdle +
      ', cameraTravel ' + SAMP.s[2].cameraTravelM + ' m, silhouette ' + sil + ' px' +
      ', stats ' + JSON.stringify(g.pixelStats));
  log('GATE ' + (g.pass ? 'PASS' : 'FAIL') + ' — see window.__GATE');
  finalizeGate({});
}
requestAnimationFrame(tick);
</script>
</body>
</html>
