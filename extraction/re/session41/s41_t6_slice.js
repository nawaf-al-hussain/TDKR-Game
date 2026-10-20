// S41 T6: JS mirror of the city slice — from the USER's OBB zip:
// OBB -> l_gothamcity.gla -> GothamCity.zip -> lod_table.bin + lod_data.bin
// -> per-segment counts + SHA256(positions). Compares vs s41_t6_pyref.json.
'use strict';
const fs = require('fs');
const zlib = require('zlib');
const crypto = require('crypto');

const OBB = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip';
const REF = JSON.parse(fs.readFileSync('/home/z/my-project/scripts/s41_t6_pyref.json', 'utf8'));
const OUT = '/home/z/my-project/scripts/s41_t6_js.json';

function sha(b) { return crypto.createHash('sha256').update(b).digest('hex'); }

// ---- minimal zip central-directory reader ----
function zipMembers(buf) {
  // find EOCD
  let eocd = -1;
  for (let i = buf.length - 22; i >= Math.max(0, buf.length - 66000); i--) {
    if (buf.readUInt32LE(i) === 0x06054b50) { eocd = i; break; }
  }
  if (eocd < 0) throw new Error('no EOCD');
  const n = buf.readUInt16LE(eocd + 10);
  let p = buf.readUInt32LE(eocd + 16);
  const members = new Map();
  for (let k = 0; k < n; k++) {
    if (buf.readUInt32LE(p) !== 0x02014b50) throw new Error('bad CD sig @' + p);
    const method = buf.readUInt16LE(p + 10);
    const csize = buf.readUInt32LE(p + 20);
    const ulen = buf.readUInt16LE(p + 28);
    const nlen = buf.readUInt16LE(p + 28);
    const elen = buf.readUInt16LE(p + 30);
    const clen = buf.readUInt16LE(p + 32);
    const lho = buf.readUInt32LE(p + 42);
    const name = buf.toString('latin1', p + 46, p + 46 + nlen);
    members.set(name, { method, csize, lho, clen, nlen });
    p += 46 + nlen + elen + clen;
  }
  return members;
}

function zipRead(buf, m) {
  const lho = m.lho;
  if (buf.readUInt32LE(lho) !== 0x04034b50) throw new Error('bad LFH');
  const nlen = buf.readUInt16LE(lho + 26);
  const elen = buf.readUInt16LE(lho + 28);
  const start = lho + 30 + nlen + elen;
  const raw = buf.subarray(start, start + m.csize);
  if (m.method === 0) return raw;
  if (m.method === 8) return zlib.inflateRawSync(raw);
  throw new Error('method ' + m.method);
}

// ---- gla member extraction (BE container) ----
function glaMember(g, want) {
  const idxSize = g.readUInt32BE(4);
  const n = g.readUInt32BE(12);
  const pool = g.subarray(16 + n * 16, idxSize);
  for (let i = 0; i < n; i++) {
    const ro = 16 + i * 16;
    const off = g.readUInt32BE(ro), sz = g.readUInt32BE(ro + 4), no = g.readUInt32BE(ro + 8);
    const e = pool.indexOf(0, no);
    const name = pool.toString('latin1', no, e);
    if (name === want) return g.subarray(off, off + sz);
  }
  return null;
}

console.time('obb');
const obb = fs.readFileSync(OBB);
console.timeEnd('obb');
const members = zipMembers(obb);
const glaName = 'com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla';
if (!members.has(glaName)) throw new Error('gla member missing');
const gla = zipRead(obb, members.get(glaName));
console.log('gla inflated:', (gla.length / 1e6).toFixed(1), 'MB');

const zb = glaMember(gla, 'GothamCity.zip');
if (!zb) throw new Error('GothamCity.zip not in gla');
const Z = zipMembers(zb);
const lt = zipRead(zb, Z.get('lod_table.bin'));
const ld = zipRead(zb, Z.get('lod_data.bin'));
console.log('lod_table', lt.length, 'lod_data', ld.length);

const n = lt.readUInt32LE(0);
const segs = [];
let ok4 = 0;
for (let k = 0; k < n; k++) {
  const off = lt.readUInt32LE(4 + 8 * k), sz = lt.readUInt32LE(8 + 8 * k);
  const dataOff = ld.readUInt32LE(off + 68), four = ld.readUInt32LE(off + 72);
  const vb = ld.readUInt32LE(off + 76), ib = ld.readUInt32LE(off + 80);
  if (four !== 4) { segs.push(null); continue; }
  const vstart = dataOff + 4, istart = vstart + vb;
  // index: u16 strip, drop 0xFFFF
  const ni = ib >> 1;
  let real = 0, mx = 0;
  for (let i = 0; i < ni; i++) {
    const v = ld.readUInt16LE(istart + 2 * i);
    if (v !== 0xFFFF) { real++; if (v > mx) mx = v; }
  }
  let stride = 0;
  for (const s of [24, 20, 32, 28]) {  // +28: s42 T6 - the 9 skipped segs are stride-28
    if (vb % s === 0 && mx < vb / s) {
      // EXACT mirror of the Python probe: every record, xyz only
      const cnt = vb / s;
      let ok = true;
      for (let i = 0; i < cnt; i++) {
        const x = ld.readFloatLE(vstart + i * s), y = ld.readFloatLE(vstart + i * s + 4), z = ld.readFloatLE(vstart + i * s + 8);
        if (!isFinite(x) || !isFinite(y) || !isFinite(z) || Math.max(Math.abs(x), Math.abs(y), Math.abs(z)) >= 6000) { ok = false; break; }
      }
      if (ok) { stride = s; break; }
    }
  }
  if (!stride) { segs.push(null); continue; }
  ok4++;
  const nvb = vb - (vb % stride);
  const posBuf = ld.subarray(vstart, vstart + nvb);
  // positions = first 3 f4 of each stride-record
  const cnt = nvb / stride;
  const pos = Buffer.allocUnsafe(cnt * 12);
  for (let i = 0; i < cnt; i++) {
    pos.copy ? pos.writeFloatLE(posBuf.readFloatLE(i * stride), i * 12) : 0;
    pos.writeFloatLE(posBuf.readFloatLE(i * stride + 4), i * 12 + 4);
    pos.writeFloatLE(posBuf.readFloatLE(i * stride + 8), i * 12 + 8);
  }
  // index real values u32 LE for sha parity with numpy '<u4'
  const idxBuf = Buffer.allocUnsafe(real * 4);
  let w = 0;
  for (let i = 0; i < ni; i++) {
    const v = ld.readUInt16LE(istart + 2 * i);
    if (v !== 0xFFFF) idxBuf.writeUInt32LE(v, 4 * w++);
  }
  segs.push({
    off, m40: ld.readUInt32LE(off + 40), m36: ld.readUInt32LE(off + 36),
    nv: cnt, ni: real, nidx_raw: ni, stride, vb, ib,
    pos_sha: sha(pos), idx_sha: sha(idxBuf),
  });
}
console.log('segments:', n, 'stride-ok:', ok4);

// ---- compare vs Python reference ----
let mism = 0, checked = 0;
for (let k = 0; k < n; k++) {
  const r = REF.segments[k], j = segs[k];
  const rOk = r && r.stride !== undefined;
  if (rOk !== !!j) { mism++; if (mism < 6) console.log('OK-MISMATCH seg', k, 'py_ok=', rOk, 'js_ok=', !!j); continue; }
  if (!j) continue;
  checked++;
  const keys = ['off', 'm40', 'm36', 'nv', 'ni', 'nidx_raw', 'stride', 'vb', 'ib', 'pos_sha', 'idx_sha'];
  for (const key of keys) {
    if (String(r[key]) !== String(j[key])) {
      mism++;
      if (mism < 6) console.log('MISMATCH seg', k, key, 'py=', r[key], 'js=', j[key]);
      break;
    }
  }
}
console.log(`checked ${checked} segments, mismatches ${mism}`);
const refDecoded = REF.segments.filter(x => x && x.stride !== undefined).length;
const pass = mism === 0 && checked === refDecoded;
console.log('ref decoded:', refDecoded);
console.log('S41 T6 JS-vs-PY:', pass ? 'PASS (all decoded segments bit-identical: counts + position/index SHA256)' : 'FAIL');
fs.writeFileSync(OUT, JSON.stringify({ n, ok4, checked, mism, pass }, null, 1));
