// tdkr_pipeline.js — dependency-free TDKR asset pipeline (browser + node).
// Round 26 T5 first slice: user-supplied APK/OBB zip -> .gla containers ->
// game_config (lvc/gol.bin/nm) + batman.bdae + batman_anims.bdae + textures.
// Ports the engine-verified decoders: lvc records (lvc.js), animation chunk
// decoder (663-segment directory, stream tables, 921 clips), skeleton/skin
// reader (0x50-B nodes, inverse binds, skin records, stride-80 vertices).
// NO game data is bundled or fetched; every input is a user File/Buffer.
'use strict';

// ---------------------------------------------------------------- zip ----
// Minimal zip (APK/OBB) reader: central directory + STORE and DEFLATE.
// DEFLATE uses DecompressionStream('deflate-raw') (browsers + node >= 17).
async function inflateRaw(u8) {
  if (typeof DecompressionStream === 'undefined')
    throw new Error('DecompressionStream unavailable; cannot inflate');
  const ds = new DecompressionStream('deflate-raw');
  const stream = new Blob([u8]).stream().pipeThrough(ds);
  const ab = await new Response(stream).arrayBuffer();
  return new Uint8Array(ab);
}

function zipEntries(u8) {
  const dv = new DataView(u8.buffer, u8.byteOffset, u8.byteLength);
  // find EOCD
  let eocd = -1;
  for (let i = u8.length - 22; i >= Math.max(0, u8.length - 66000); i--) {
    if (dv.getUint32(i, true) === 0x06054b50) { eocd = i; break; }
  }
  if (eocd < 0) throw new Error('zip: EOCD not found');
  const n = dv.getUint16(eocd + 10, true);
  let cdOff = dv.getUint32(eocd + 16, true);
  const out = new Map();
  for (let i = 0; i < n; i++) {
    if (dv.getUint32(cdOff, true) !== 0x02014b50) break;
    const method = dv.getUint16(cdOff + 10, true);
    const csize = dv.getUint32(cdOff + 20, true);
    const nameLen = dv.getUint16(cdOff + 28, true);
    const extraLen = dv.getUint16(cdOff + 30, true);
    const cmtLen = dv.getUint16(cdOff + 32, true);
    const lho = dv.getUint32(cdOff + 42, true);
    const nameLenL = dv.getUint16(lho + 26, true);
    const extraLenL = dv.getUint16(lho + 28, true);
    const name = new TextDecoder('latin1').decode(u8.subarray(lho + 30, lho + 30 + nameLenL));
    const dataOff = lho + 30 + nameLenL + extraLenL;
    out.set(name, { method, csize, dataOff });
    cdOff += 46 + nameLen + extraLen + cmtLen;
  }
  return out;
}

async function zipRead(u8, name) {
  const ents = zipEntries(u8);
  const e = ents.get(name);
  if (!e) throw new Error('zip: missing entry ' + name);
  const raw = u8.subarray(e.dataOff, e.dataOff + e.csize);
  if (e.method === 0) return raw;
  if (e.method === 8) return inflateRaw(raw);
  throw new Error('zip: unsupported method ' + e.method);
}

// ---------------------------------------------------------------- gla ----
// .gla container: [u32be ?][u32be idx_size][u32be table_bytes][u32be n]
// then n x 16-B entries [off][size][name_off][?] + name pool.
function parseGla(u8) {
  const dv = new DataView(u8.buffer, u8.byteOffset, u8.byteLength);
  const idxSize = dv.getUint32(4);
  const n = dv.getUint32(12);
  const ents = {};
  const poolStart = 16 + n * 16;
  for (let i = 0; i < n; i++) {
    const o = 16 + i * 16;
    const off = dv.getUint32(o), size = dv.getUint32(o + 4), nameOff = dv.getUint32(o + 8);
    const nameBase = poolStart + nameOff;
    let e = nameBase; while (e < u8.length && u8[e] !== 0) e++;
    const name = new TextDecoder('latin1').decode(u8.subarray(nameBase, e));
    ents[name] = { off, size };
  }
  return { idxSize, n, poolStart, ents };
}

// ------------------------------------------------------------ anims ------
// batman_anims.bdae decoder: 663-segment directory, per-segment stream
// tables, 921-clip list. Engine-derived layout (r25/r26):
//   seg dir: {count u32 @0xccf4, array u32 @0xccf8}, records 0x1c-B:
//     [ts][te][0][0][tbl][dist][0]  (u32 LE)
//   clip list @0x11580: 921 x [nameOff][ts][te] u32 LE
//   stream table @tbl: entry0 = (nStreams u32, len0 u32); then nStreams-1
//     x (off u32, len u32); data base = tbl + (nStreams+1)*8 - 4;
//     streams = pairs (times u32[] BE-keyed?, values f32[]) — all LE here.
const ANIM = { CNT_OFF: 0xccf4, CLIPS_OFF: 0x11580, NCLIPS: 921 };

function decodeAnims(u8) {
  const dv = new DataView(u8.buffer, u8.byteOffset, u8.byteLength);
  const nseg = dv.getUint32(ANIM.CNT_OFF, true);
  const segarr = dv.getUint32(ANIM.CNT_OFF + 4, true);
  const segs = [];
  for (let k = 0; k < nseg; k++) {
    const o = segarr + k * 0x1c;
    segs.push({ k, start: dv.getUint32(o, true), end: dv.getUint32(o + 4, true),
                tbl: dv.getUint32(o + 16, true), dist: dv.getUint32(o + 20, true) });
  }
  function cstr(v) {
    if (v <= 0 || v >= u8.length) return null;
    let e = v; while (e < u8.length && u8[e] !== 0 && e - v < 90) e++;
    if (e - v >= 90) return null;
    let s = ''; for (let i = v; i < e; i++) s += String.fromCharCode(u8[i]);
    return s;
  }
  const clips = [];
  for (let i = 0; i < ANIM.NCLIPS; i++) {
    const o = ANIM.CLIPS_OFF + 12 * i;
    clips.push({ i, name: cstr(dv.getUint32(o, true)),
                 ts: dv.getUint32(o + 4, true), te: dv.getUint32(o + 8, true) });
  }
  // channel names table (engine order, 78 entries @0xb544, 0x20-B records)
  const CH = [];
  for (let k = 0; k < 78; k++) {
    const o = 0xb544 + k * 0x20;
    const sub = dv.getUint32(o + 0x10, true);
    CH.push({ name: cstr(dv.getUint32(sub, true)), ty: dv.getUint32(sub + 4, true) });
  }
  const segStreams = {};
  let failSegs = 0;
  for (const s of segs) {
    const st = decodeSegTable(u8, s.tbl);
    if (st) segStreams[s.k] = st; else failSegs++;
  }
  return { nseg, segs, clips, CH, segStreams, failSegs };
}

function decodeSegTable(u8, T) {
  const dv = new DataView(u8.buffer, u8.byteOffset, u8.byteLength);
  const nst = dv.getUint32(T, true);
  if (!(nst >= 100 && nst <= 160)) return null;
  const len0 = dv.getUint32(T + 4, true);
  const ents = [[0, len0]];
  for (let j = 1; j < nst; j++)
    ents.push([dv.getUint32(T + 8 * j, true), dv.getUint32(T + 8 * j + 4, true)]);
  const cands = [T + (nst + 1) * 8 - 4];
  if (ents[1]) cands.push(T + ents[1][0] + 8);
  for (const base of cands) {
    let pos = base, ok = true;
    const streams = [];
    for (const [off, ln] of ents) {
      if (ln % 4 || pos + ln > u8.length) { ok = false; break; }
      streams.push(u8.subarray(pos, pos + ln));
      pos += ln;
    }
    if (!ok) continue;
    // validate: even streams = ascending u32 ticks
    let bad = 0;
    for (let j = 0; j < streams.length; j += 2) {
      const s = streams[j], n = s.length >> 2;
      if (n >= 2) {
        const dv2 = new DataView(u8.buffer, s.byteOffset, s.byteLength);
        let prev = -1;
        for (let i = 0; i < n; i++) {
          const t = dv2.getUint32(i * 4, true);
          if (t < prev) { bad++; break; }
          prev = t;
        }
      }
    }
    if (bad === 0) return streams;
  }
  return null;
}

// clip assembly: gather channel keys in [ts-pad, te+pad] over covering segs
function assembleClip(anims, clip, pad) {
  pad = pad === undefined ? 120 : pad;
  const ts = clip.ts, te = clip.te;
  const cov = anims.segs.filter(s => s.start < te && s.end > ts);
  const chans = new Array(78).fill(null);
  for (const s of cov) {
    const st = anims.segStreams[s.k];
    if (!st) continue;
    for (let c = 0; c < 78; c++) {
      const tw = st[2 * c], vw = st[2 * c + 1];
      const nt = tw.length >> 2;
      if (!nt) continue;
      const vdim = anims.CH[c].ty === 1 ? 3 : 4;
      const nv = (vw.length * 1) / (vdim * 4) | 0;
      const n = Math.min(nt, nv);
      const dvT = new DataView(u8abs(tw).buffer, tw.byteOffset, nt * 4);
      const dvV = new DataView(u8abs(vw).buffer, vw.byteOffset, vw.byteLength);
      let tt = null, vv = null;
      const keyT = [], keyV = [];
      for (let i = 0; i < n; i++) {
        const t = dvT.getUint32(i * 4, true);
        if (t < ts - pad || t > te + pad) continue;
        keyT.push(t);
        const row = new Float32Array(vdim);
        for (let d = 0; d < vdim; d++) row[d] = dvV.getFloat32(i * vdim * 4 + d * 4, true);
        keyV.push(row);
      }
      if (!keyT.length) continue;
      if (chans[c] === null) { chans[c] = { t: keyT, v: keyV }; }
      else {
        const m = chans[c];
        const mg = m.t.concat(keyT);
        const ord = mg.map((x, i) => [x, i]).sort((a, b) => a[0] - b[0] || a[1] - b[1]);
        chans[c] = {
          t: ord.map(p => mg[p[1]]),
          v: ord.map(p => (p[1] < m.t.length ? m.v[p[1]] : keyV[p[1] - m.t.length]))
        };
      }
    }
  }
  return { cov, chans };
}
function u8abs(x) { return x; }

// -------------------------------------------------------------- skin -----
// batman.bdae skeleton/skin reader (r23-r26 verified offsets):
//   node records 0x50-B from 0x2760 (name@0, alias@4, second@8 -> string
//   pool 0x868..0x22d8; t f32x3 @+0xc; q f32x4 @+0x18; s f32x3 @+0x28)
//   palette @0x3167c (8-B entries), 31 joints; PNAME override map;
//   inverse binds 31 x 64-B @0x30e30 (row-major 4x4, engine = inverse);
//   vertices 1449 x 80-B @0x4b5c (pos @0, u16 u/v @+72/+76 fixed 4.12);
//   skin records 1449 x 20-B @0x31774 (4 x u8 joint, 4 x f32 weight);
//   indices @0x210ba (valid run, 5431 u16).
const SKIN_OFFS = { NODE0: 0x2760, NODE_END: 0x4a08, POOL0: 0x868, POOL1: 0x22d8,
  PALETTE: 0x3167c, PALETTE_END: 0x31774, INVB: 0x30e30, VERTS: 0x4b5c, NV: 1449,
  SKINREC: 0x31774, IDX: 0x210ba, IDXN: 5431 };

const PNAME = ['Bip01_R_Calf', 'Bip01_R_Thigh', 'Bip01_Pelvis', 'Bip01_L_Calf',
  'Bip01_L_Thigh', 'Bip01_Pelvis', 'Bip01_R_Hand', 'Bip01_R_Hand', 'Bip01_R_Forearm',
  'Bip01_R_UpperArm', 'Bip01_R_Clavicle', 'Bip01_Neck', 'Bip01_L_Hand', 'Bip01_L_Hand',
  'Bip01_L_Forearm', 'Bip01_L_UpperArm', 'Bip01_L_Clavicle', 'Bip01_Neck', 'Bip01_Neck',
  'Bip01_Spine1', 'Bip01_Spine', 'Bip01_Pelvis', 'Bip01',
  'Bip01_L_Finger0', 'Bip01_L_Finger1', 'Bip01_L_Hand', 'Bip01_L_Finger2',
  'Bip01_R_Finger0', 'Bip01_R_Finger1', 'Bip01_R_Hand', 'Bip01_R_Finger2'];

function readBdae(u8) {
  const dv = new DataView(u8.buffer, u8.byteOffset, u8.byteLength);
  function pool(v) {
    if (v >= SKIN_OFFS.POOL0 && v < SKIN_OFFS.POOL1) {
      let e = v; while (e < u8.length && u8[e] !== 0) e++;
      let s = ''; for (let i = v; i < e; i++) s += String.fromCharCode(u8[i]);
      return s;
    }
    return null;
  }
  const nodes = [];
  for (let o = SKIN_OFFS.NODE0; o < SKIN_OFFS.NODE_END - 0x50; ) {
    // engine node records are 0x50-strided but the start must be scanned at
    // 4-B granularity (python walker steps 4 on mismatch)
    const n1 = pool(dv.getUint32(o, true)), n2 = pool(dv.getUint32(o + 4, true)),
          al = pool(dv.getUint32(o + 8, true));
    if (n1 === null || n2 === null || al === null) { o += 4; continue; }
    const t = [dv.getFloat32(o + 0x0c, true), dv.getFloat32(o + 0x10, true), dv.getFloat32(o + 0x14, true)];
    const q = [dv.getFloat32(o + 0x18, true), dv.getFloat32(o + 0x1c, true), dv.getFloat32(o + 0x20, true), dv.getFloat32(o + 0x24, true)];
    const s = [dv.getFloat32(o + 0x28, true), dv.getFloat32(o + 0x2c, true), dv.getFloat32(o + 0x30, true)];
    const ql = Math.hypot(q[0], q[1], q[2], q[3]);
    if (!(ql > 0.96 && ql < 1.04)) { o += 4; continue; }
    if (Math.abs(t[0]) > 1e4 || Math.abs(t[1]) > 1e4 || Math.abs(t[2]) > 1e4) { o += 4; continue; }
    if (!(Math.abs(s[0]) > 0.01 && Math.abs(s[0]) < 100)) { o += 4; continue; }
    if (!(Math.abs(s[1]) > 0.01 && Math.abs(s[1]) < 100)) { o += 4; continue; }
    if (!(Math.abs(s[2]) > 0.01 && Math.abs(s[2]) < 100)) { o += 4; continue; }
    if (dv.getUint32(o + 0x34, true) !== 1 || dv.getUint32(o + 0x38, true) > 32) { o += 4; continue; }
    nodes.push({ off: o, name: n2, alias: al, t, q, s });
    o += 0x50;
  }
  // palette
  const pal = [];
  for (let o = SKIN_OFFS.PALETTE; o < SKIN_OFFS.PALETTE_END; o += 8) {
    const a = String.fromCharCode(u8[o], u8[o + 1]), b = String.fromCharCode(u8[o + 4], u8[o + 5]);
    const tag = u8[o + 4] === 0x42 && u8[o + 5] === 0x6f ? b : a; // 'Bo'
    pal.push('Bone' + tag.replace(/[^0-9]/g, ''));
  }
  const byAlias = {};
  for (const nd of nodes) if (nd.alias.startsWith('Bone')) byAlias[nd.alias] = nd.name;
  const jointNodes = pal.map(p => byAlias[p]);
  const pnameOf = {};
  PNAME.forEach((p, b) => { if (jointNodes[b]) pnameOf[jointNodes[b]] = p; });
  const BIPED = { Bip01_Pelvis: 'Bip01', Bip01_Spine: 'Bip01_Pelvis', Bip01_Spine1: 'Bip01_Spine',
    Bip01_Neck: 'Bip01_Spine1', Bip01_Head: 'Bip01_Neck', Bip01_L_Thigh: 'Bip01_Pelvis',
    Bip01_L_Calf: 'Bip01_L_Thigh', Bip01_L_Foot: 'Bip01_L_Calf', Bip01_R_Thigh: 'Bip01_Pelvis',
    Bip01_R_Calf: 'Bip01_R_Thigh', Bip01_R_Foot: 'Bip01_R_Calf',
    Bip01_L_Clavicle: 'Bip01_Neck', Bip01_L_UpperArm: 'Bip01_L_Clavicle',
    Bip01_L_Forearm: 'Bip01_L_UpperArm', Bip01_L_Hand: 'Bip01_L_Forearm',
    Bip01_R_Clavicle: 'Bip01_Neck', Bip01_R_UpperArm: 'Bip01_R_Clavicle',
    Bip01_R_Forearm: 'Bip01_R_UpperArm', Bip01_R_Hand: 'Bip01_R_Forearm',
    Bip01_L_Finger0: 'Bip01_L_Hand', Bip01_L_Finger01: 'Bip01_L_Finger0',
    Bip01_L_Finger1: 'Bip01_L_Hand', Bip01_L_Finger11: 'Bip01_L_Finger1',
    Bip01_L_Finger2: 'Bip01_L_Hand', Bip01_L_Finger21: 'Bip01_L_Finger2',
    Bip01_R_Finger0: 'Bip01_R_Hand', Bip01_R_Finger01: 'Bip01_R_Finger0',
    Bip01_R_Finger1: 'Bip01_R_Hand', Bip01_R_Finger11: 'Bip01_R_Finger1',
    Bip01_R_Finger2: 'Bip01_R_Hand', Bip01_R_Finger21: 'Bip01_R_Finger2' };
  const parentName = nm => pnameOf[nm] || BIPED[nm] || null;
  // inverse binds
  const invB = [];
  for (let k = 0; k < 31; k++) {
    const o = SKIN_OFFS.INVB + k * 64, m = new Float64Array(16);
    for (let i = 0; i < 16; i++) m[i] = dv.getFloat32(o + 4 * i, true);
    invB.push(m);
  }
  // verts + uvs + skin records
  const verts = new Float32Array(SKIN_OFFS.NV * 3);
  const uvs = new Float32Array(SKIN_OFFS.NV * 2);
  const skinJ = new Uint8Array(SKIN_OFFS.NV * 4);
  const skinW = new Float32Array(SKIN_OFFS.NV * 4);
  for (let i = 0; i < SKIN_OFFS.NV; i++) {
    const b = SKIN_OFFS.VERTS + i * 80;
    verts[3 * i] = dv.getFloat32(b, true);
    verts[3 * i + 1] = dv.getFloat32(b + 4, true);
    verts[3 * i + 2] = dv.getFloat32(b + 8, true);
    uvs[2 * i] = dv.getUint16(b + 72, true) / 4096.0;
    uvs[2 * i + 1] = dv.getUint16(b + 76, true) / 4096.0;
    const s = SKIN_OFFS.SKINREC + i * 20;
    for (let j = 0; j < 4; j++) {
      skinJ[4 * i + j] = u8[s + j];
      skinW[4 * i + j] = dv.getFloat32(s + 4 + 4 * j, true);
    }
  }
  const idx = new Uint16Array(SKIN_OFFS.IDXN);
  for (let i = 0; i < SKIN_OFFS.IDXN; i++) idx[i] = dv.getUint16(SKIN_OFFS.IDX + 2 * i, true);
  return { nodes, jointNodes, pnameOf, parentName, invB, verts, uvs, skinJ, skinW, idx };
}

// ------------------------------------------------------------ texture ----
// identify a texture chunk header (common TDKR formats) — extraction only.
function identifyTexture(u8) {
  const dv = new DataView(u8.buffer, u8.byteOffset, Math.min(64, u8.byteLength));
  return { size: u8.length, head: Array.from(u8.subarray(0, 16)).map(x => x.toString(16).padStart(2, '0')).join(' ') };
}

// ---------------------------------------------------------------- export -
const api = { zipEntries, zipRead, parseGla, decodeAnims, assembleClip, readBdae, identifyTexture, inflateRaw };
if (typeof module !== 'undefined' && module.exports) module.exports = api;
if (typeof globalThis !== 'undefined') globalThis.TDKR = api;
