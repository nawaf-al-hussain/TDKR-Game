// S38 T5.2: skeleton-level parity digests, JS side (via tdkr_pipeline.js).
import fs from 'fs';
import crypto from 'crypto';
const TDKR = await import('/tmp/my-project/work/TDKR-Game/gh-pages/playable/tdkr_pipeline.js');
const api = TDKR.default || TDKR;
const bd = new Uint8Array(fs.readFileSync('/tmp/my-project/work/data/batman.bdae'));
const ad = new Uint8Array(fs.readFileSync('/tmp/my-project/work/data/batman_anims.bdae'));
const skin = api.readBdae(bd);
const A = api.decodeAnims(ad);
const sha = s => crypto.createHash('sha256').update(s).digest('hex').slice(0, 16);
const shaB = b => crypto.createHash('sha256').update(Buffer.from(b.buffer, b.byteOffset, b.byteLength)).digest('hex').slice(0, 16);

const names = skin.nodes.map(n => n.name);
const parentIdx = names.map((nm, i) => {
  const p = skin.pnameOf[nm] || null;
  return p ? names.indexOf(p) : -1;
});
const ibm = new Float32Array(31 * 16);
skin.invB.forEach((m, i) => ibm.set(m, i * 16));
// skin.skinJ / skin.skinW are FLAT packed arrays (NV*4) — use directly
const skinIds = new Uint8Array(skin.skinJ);            // copy (source may be an unaligned view)
const skinW = new Float32Array(skin.skinW);

const digests = {
  node_names_sha: sha(names.join('|')),
  parent_idx_sha: sha(parentIdx.join(',')),
  palette_order_sha: sha(skin.jointNodes.join('|')),
  ibm_sha: shaB(ibm),
  skin_ids_sha: shaB(skinIds),
  skin_w_sha: shaB(skinW),
  n_nodes: names.length, n_palette: skin.jointNodes.length,
  parent_idx: parentIdx.join(','),
  palette: skin.jointNodes.join('|'),
  segs: A.segs.length, clips: A.clips.length,
};
console.log(JSON.stringify(digests, null, 1));
fs.writeFileSync('/home/z/my-project/scripts/s38/s38_t5_digests_js.json', JSON.stringify(digests, null, 1));
