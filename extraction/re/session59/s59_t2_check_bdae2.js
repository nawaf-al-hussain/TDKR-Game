// s59 T2: node-side validation of readBdae2 — Batman digest equality vs readBdae
// + merc layout vs the python walker + error handling.
const TDKR = require('/tmp/my-project/work/ghpages_staged_wt/playable/tdkr_pipeline.js');
const crypto = require('crypto');
const sha = b => crypto.createHash('sha256').update(b).digest('hex').slice(0, 16);

const bat = new Uint8Array(require('fs').readFileSync('/tmp/my-project/work/data/batman.bdae'));
const merc = new Uint8Array(require('fs').readFileSync('/tmp/my-project/work/data/Bane_mercenary.bdae'));

const a1 = TDKR.readBdae(bat), a2 = TDKR.readBdae2(bat);
const dg = s => {
  const buf = s.verts.buffer.slice(s.verts.byteOffset, s.verts.byteOffset + s.verts.byteLength);
  return { verts: sha(new Uint8Array(buf)), nV: s.verts.length / 3,
           idx: sha(new Uint8Array(s.idx.buffer.slice(s.idx.byteOffset, s.idx.byteOffset + s.idx.byteLength))),
           nIdx: s.idx.length, joints: s.jointNodes.length,
           skinJ: sha(new Uint8Array(s.skinJ.buffer.slice(s.skinJ.byteOffset, s.skinJ.byteOffset + s.skinJ.byteLength))),
           invB0: Array.from(s.invB[0]).slice(0, 4).map(x => +x.toFixed(5)) };
};
const d1 = dg(a1), d2 = dg(a2);
console.log('BATMAN readBdae :', JSON.stringify(d1));
console.log('BATMAN readBdae2:', JSON.stringify(d2));
console.log('BATMAN DIGESTS EQUAL:', JSON.stringify(d1) === JSON.stringify(d2));

const m = TDKR.readBdae2(merc);
console.log('MERC layout:', JSON.stringify(m._layout));
console.log('MERC joints:', m.jointNodes.length, 'first 6:', m.jointNodes.slice(0, 6));
console.log('MERC uv sample:', Array.from(m.uvs.slice(0, 6)).map(x => +x.toFixed(4)));
console.log('MERC vert0:', Array.from(m.verts.slice(0, 3)).map(x => +x.toFixed(4)));
console.log('MERC idx0:', Array.from(m.idx.slice(0, 6)));
