// S41 T2: node parity — decode ALL 910 chunks (incl. full ETC1 mip chains and
// ZIP_SPLIT members) in JS and compare per-level/chunk SHA256 against the
// Python reference manifest. JS decoders are independent of the Python ones.
'use strict';
const fs = require('fs');
const crypto = require('crypto');
const E = require('/tmp/my-project/work/ghpages_live_wt/playable/etc1_tdkr.js');

const PACK = '/home/z/my-project/scripts/s41_t2_chunks.pack';
const MAN = '/home/z/my-project/scripts/s41_t2_chunks.manifest.json';
const OUT = '/home/z/my-project/scripts/s41_t2_parity.json';

const man = JSON.parse(fs.readFileSync(MAN, 'utf8'));
const ref = new Map(man.chunks.map(c => [c.name, c]));
const bin = fs.readFileSync(PACK);
let off = 4;
const count = bin.readUInt32LE(0);

function sha(b) { return crypto.createHash('sha256').update(b).digest('hex'); }

function decode565(px, w, h) {
  const out = Buffer.allocUnsafe(w * h * 4);
  for (let i = 0, j = 0; i < w * h; i++, j += 4) {
    const v = px.readUInt16LE(i * 2);
    const r5 = (v >> 11) & 31, g6 = (v >> 5) & 63, b5 = v & 31;
    out[j] = (r5 << 3) | (r5 >> 2);
    out[j + 1] = (g6 << 2) | (g6 >> 4);
    out[j + 2] = (b5 << 3) | (b5 >> 2);
    out[j + 3] = 255;
  }
  return out;
}
function decode888(px, w, h) {
  const out = Buffer.allocUnsafe(w * h * 4);
  for (let i = 0, j = 0; i < w * h; i++, j += 4) {
    out[j] = px[i * 3]; out[j + 1] = px[i * 3 + 1]; out[j + 2] = px[i * 3 + 2];
    out[j + 3] = 255;
  }
  return out;
}

const t0 = Date.now();
const stats = { ETC1: [0, 0], RGB565: [0, 0], RGB888: [0, 0], RGBA8888: [0, 0], ZIP_SPLIT: [0, 0] };
const mism = [];
let packChunks = 0;
const chunkSha = [];
for (let c = 0; c < count; c++) {
  const nl = bin.readUInt16LE(off); off += 2;
  const name = bin.toString('latin1', off, off + nl); off += nl;
  const blobLen = bin.readUInt32LE(off); off += 4;
  const blob = bin.subarray(off, off + blobLen); off += blobLen;
  packChunks++;
  const r = ref.get(name);
  if (!r) { mism.push({ name, issue: 'not in reference manifest' }); continue; }
  // iterate levels from our own blob layout
  let p = 0, li = 0;
  const levelShas = [];
  const all = [];
  // flattened expected level sha list (for ZIP_SPLIT: rgb.pvr levels then alpha.pvr)
  const wantLevels = r.kind === 'ZIP_SPLIT'
    ? [...r.members['rgb.pvr'].levels, ...r.members['alpha.pvr'].levels]
    : r.levels;
  while (p + 12 <= blobLen) {
    const w = blob.readUInt32LE(p), h = blob.readUInt32LE(p + 4), n = blob.readUInt32LE(p + 8);
    p += 12;
    const raw = blob.subarray(p, p + n); p += n;
    let rgba;
    if (r.kind === 'ETC1' || r.kind === 'ZIP_SPLIT') {
      const u = E.decodeRGBA(raw, w, h);
      rgba = Buffer.from(u.buffer, u.byteOffset, u.byteLength);
    } else if (r.kind === 'RGB565') rgba = decode565(raw, w, h);
    else if (r.kind === 'RGB888') rgba = decode888(raw, w, h);
    else rgba = Buffer.from(raw); // RGBA8888: memory RGBA
    const s = sha(rgba);
    levelShas.push(s);
    all.push(rgba);
    const want = wantLevels[li] ? wantLevels[li].sha : null;
    if (want && want !== s) {
      mism.push({ name, level: li, w, h, got: s.slice(0, 12), want: want.slice(0, 12) });
    }
    li++;
  }
  const chunkS = sha(Buffer.concat(all));
  chunkSha.push(chunkS === r.sha);
  const kind = r.kind;
  stats[kind][1]++;
  const levelOk = levelShas.every((s, k) => !wantLevels[k] || wantLevels[k].sha === s);
  if (levelOk && chunkS === r.sha) stats[kind][0]++;
  else {
    mism.push({ name, kind, issue: 'chunk sha mismatch', got: chunkS.slice(0, 12), want: r.sha.slice(0, 12) });
  }
}
console.log(`pack chunks walked: ${packChunks}, time ${((Date.now() - t0) / 1000).toFixed(1)} s`);
for (const k of Object.keys(stats)) console.log(`  ${k}: ${stats[k][0]}/${stats[k][1]}`);
console.log('mismatches:', mism.length);
if (mism.length) console.log(mism.slice(0, 10));
const pass = Object.values(stats).every(([o, t]) => o === t) && mism.length === 0;
console.log('S41 T2 NODE PARITY:', pass ? 'PASS (all 910 chunks SHA256-exact)' : 'FAIL');
fs.writeFileSync(OUT, JSON.stringify({ stats, mismatches: mism, pass }, null, 1));
process.exit(pass ? 0 : 1);
