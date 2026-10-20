// S40 T1c: node parity — decode all packed ETC1 mip0 payloads with the JS
// decoder and compare SHA256 of the RGBA output against the Python reference.
'use strict';
const fs = require('fs');
const crypto = require('crypto');
const E = require('/tmp/my-project/work/ghpages_site_wt/playable/etc1_tdkr.js');

const bin = fs.readFileSync('/home/z/my-project/scripts/s40_t1_mip0.pack');
const man = JSON.parse(fs.readFileSync('/home/z/my-project/scripts/s40_t1_manifest.json', 'utf8'));
const count = bin.readUInt32LE(0);
let off = 4;
let ok = 0, bad = [];
const t0 = Date.now();
for (let i = 0; i < count; i++) {
  const nl = bin.readUInt16LE(off); off += 2;
  const name = bin.toString('latin1', off, off + nl); off += nl;
  const w = bin.readUInt32LE(off), h = bin.readUInt32LE(off + 4);
  const pxLen = bin.readUInt32LE(off + 8); off += 16;
  const px = bin.subarray(off, off + pxLen); off += pxLen;
  const rgba = E.decodeRGBA(px, w, h);
  const sha = crypto.createHash('sha256').update(rgba).digest('hex');
  const e = man[i];
  if (sha === e.sha) ok++;
  else bad.push({ name, w, h, got: sha.slice(0, 12), want: e.sha.slice(0, 12) });
}
console.log(`node parity: ${ok}/${count} SHA256-exact, ${bad.length} mismatches, ${Date.now() - t0} ms`);
if (bad.length) { console.log(bad.slice(0, 8)); process.exit(1); }
