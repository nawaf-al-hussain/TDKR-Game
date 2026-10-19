// s38 T1a — ARBITER: python-built GLB (r36, verified) vs browser-built GLB (s37).
// For each GLB: three.js posed skin (idle t=0, t=1.0) vs BOTH numpy orders
// (invB@world and world@invB) computed from the python pipeline context.
// Plus: element-wise comparison of the two GLBs' inverseBindMatrices.
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import fs from 'fs';
import AdmZip from 'adm-zip';
import { execSync } from 'child_process';

function loadGlb(p) {
  const buf = fs.readFileSync(p);
  return new Promise(async (res) => {
    const ab = buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength);
    const gltf = await new Promise((r, j) => new GLTFLoader().parse(ab, '', r, j));
    let sm = null; gltf.scene.traverse(o => { if (o.isSkinnedMesh) sm = o; });
    res({ buf, gltf, sm });
  });
}
function readIbmFromGlb(buf) {
  const jslen = buf.readUInt32LE(12);
  const js = JSON.parse(buf.slice(20, 20 + jslen).toString());
  const binOff = 20 + jslen + 8;
  const skin = js.skins[0];
  const acc = js.accessors[skin.inverseBindMatrices];
  const bv = js.bufferViews[acc.bufferView];
  const off = binOff + (bv.byteOffset || 0) + acc.byteOffset;
  const out = [];
  for (let i = 0; i < 31; i++) {
    out.push(Array.from(new Float32Array(buf.slice(off + i * 64, off + i * 64 + 64).slice().buffer)));
  }
  return out;
}
function skinAt(gltf, sm, clipName, t) {
  const mixer = new THREE.AnimationMixer(gltf.scene);
  const a = mixer.clipAction(gltf.animations.find(c => c.name === clipName)); a.play();
  mixer.setTime(t);
  gltf.scene.updateMatrixWorld(true);
  const N = sm.geometry.attributes.position.count;
  const out = new Float32Array(N * 3);
  const v = new THREE.Vector3(), m = new THREE.Matrix4(), p = new THREE.Vector3();
  const pos = sm.geometry.attributes.position;
  const si = sm.geometry.attributes.skinIndex, sw = sm.geometry.attributes.skinWeight;
  for (let i = 0; i < N; i++) {
    v.fromBufferAttribute(pos, i);
    let x = 0, y = 0, z = 0;
    for (let j = 0; j < 4; j++) {
      const w = sw.getComponent(i, j); if (!w) continue;
      const b = si.getComponent(i, j);
      m.multiplyMatrices(sm.skeleton.bones[b].matrixWorld, sm.skeleton.boneInverses[b]);
      p.copy(v).applyMatrix4(m);
      x += w * p.x; y += w * p.y; z += w * p.z;
    }
    out[i*3] = x; out[i*3+1] = y; out[i*3+2] = z;
  }
  return out;
}
function cmp(got, exp) {
  const N = exp.length / 3;
  let worst = 0, sum = 0, nan = 0;
  for (let i = 0; i < N; i++) {
    const d = Math.hypot(got[i*3]-exp[i*3], got[i*3+1]-exp[i*3+1], got[i*3+2]-exp[i*3+2]);
    if (Number.isNaN(d)) { nan++; continue; }
    sum += d; if (d > worst) worst = d;
  }
  return `worst ${(worst*100).toFixed(2)} cm, mean ${Number.isNaN(sum/N*100) ? 'NaN' : (sum/N*100).toFixed(2)} cm${nan ? `, NaN verts ${nan}` : ''}`;
}
function zrange(a) { let mn = 1e9, mx = -1e9; for (let i = 2; i < a.length; i += 3) { if (a[i] < mn) mn = a[i]; if (a[i] > mx) mx = a[i]; } return [mn.toFixed(3), mx.toFixed(3)].join(' .. '); }

// numpy references from the python pipeline context (exec the verified export head)
execSync(`cd /home/z/my-project/scripts && python3 - <<'EOF'
import numpy as np, json, struct
src = open('s36_t3_export.py').read()
head = src.split('# ---------- GLB assembly ----------')[0]
g = {'__name__': 'ctx'}
exec(head, g)
import sys
fkA = []  # invB @ world  (s36 order)
fkB = []  # world @ invB
clips = dict(g['anims'])
for label, t in [('_001_idle_stand', 0.0), ('_001_idle_stand', 1.0)]:
    channels = clips[label]
    cmap = {}
    for cd in channels: cmap.setdefault(cd['node'], {})[cd['path']] = cd
    W = {}
    parent_name = g['parent_name']; node_trs = g['node_trs']; order = g['order']
    def world(nm):
        if nm in W: return W[nm]
        p = parent_name(nm); t_, q_, s_ = node_trs[nm]; t_s = t
        cd = cmap.get(nm, {}).get('rotation'); q = g['sample_track'](cd['times'], cd['out'], t_s) if cd else q_
        tr = t_
        cdt = cmap.get(nm, {}).get('translation')
        if cdt: tr = g['sample_track'](cdt['times'], cdt['out'], t_s)
        M = np.eye(4); M[:3,:3] = g['colR'](q) @ np.diag(s_); M[3,:3] = tr
        M = M @ (world(p) if p else np.eye(4)); W[nm] = M; return M
    for nm in order: world(nm)
    verts = g['verts']; NV = g['NV']; invB = g['invB']; joint_nodes = g['joint_nodes']
    b4s = g['b4s']; w4s = g['w4s']
    V = np.hstack([verts, np.ones((NV,1))])
    Ma = np.stack([invB[b] @ world(joint_nodes[b]) for b in range(31)])
    Mb = np.stack([world(joint_nodes[b]) @ invB[b] for b in range(31)])
    for M_all, store in [(Ma,'A'), (Mb,'B')]:
        out = np.zeros((NV,3))
        for k in range(4):
            bk = np.clip(b4s[:,k],0,30); wk = w4s[:,k:k+1]; Mb2 = M_all[bk]
            out += wk * np.einsum('ni,nij->nj', V, Mb2)[:,:3]
        store = out
        np.save(f'/tmp/s38_ref_{store if False else ("A" if M_all is Ma else "B")}_{int(t*1000)}.npy', out.astype(np.float32))
print('numpy refs written')
EOF`, { stdio: 'inherit' });

const refA0 = null;
function loadNpy(p) {
  const b = fs.readFileSync(p);
  return new Float32Array(b.buffer.slice(b.byteOffset + 80, b.byteOffset + b.byteLength));
}

const glb36 = await loadGlb('/home/z/my-project/download/batman_s36_anims.glb');
const glb37 = await loadGlb('/home/z/my-project/scripts/jsverify/s37_myglb.glb');
const ibm36 = readIbmFromGlb(glb36.buf);
const ibm37 = readIbmFromGlb(glb37.buf);

// ibm comparison: elementwise, transpose, and transpose-per-bone
let elDiff = 0, trDiff = 0, maxEl = 0, maxTr = 0;
for (let b = 0; b < 31; b++) for (let r = 0; r < 4; r++) for (let c = 0; c < 4; c++) {
  const a = ibm36[b][r*4+c], x = ibm37[b][r*4+c];
  const d = Math.abs(a - x); if (d > maxEl) maxEl = d; if (d > 1e-5) elDiff++;
  const t = ibm36[b][c*4+r]; const dt = Math.abs(t - x); if (dt > maxTr) maxTr = dt; if (dt > 1e-5) trDiff++;
}
console.log(`ibm elementwise mismatches: ${elDiff}/496 (max ${maxEl.toExponential(2)})`);
console.log(`ibm vs TRANSPOSE of the other: mismatches ${trDiff}/496 (max ${maxTr.toExponential(2)})`);

for (const [label, glb] of [['r36(py-built)', glb36], ['s37(browser-built)', glb37]]) {
  for (const t of [0, 1000]) {
    const got = skinAt(glb.gltf, glb.sm, '_001_idle_stand', t / 1000);
    const A = loadNpy(`/tmp/s38_ref_A_${t}.npy`), B = loadNpy(`/tmp/s38_ref_B_${t}.npy`);
    console.log(`${label} idle t=${t/1000}s  vs numpy invB@world: ${cmp(got, A)}   vs numpy world@invB: ${cmp(got, B)}`);
    if (t === 0) console.log(`   three.js z-range: ${zrange(got)} | numpyA z: ${zrange(A)} | numpyB z: ${zrange(B)}`);
  }
}
