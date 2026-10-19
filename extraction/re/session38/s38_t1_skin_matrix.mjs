// s38 T1a — DEFINITIVE skinning root-cause matrix (fresh scene per case).
// Ground truth: s38_fk (numpy world@invB — the CORRECTED generator).
// Cases:
//   A  three.js manual world-space skin, unrotated          vs corrected numpy -> expect ~0
//   B  three.js manual world-space skin, page rotation on
//      bone-ancestor (the LIVE page convention)             vs corrected numpy rotated -> expect ~0
//   C  three.js manual skin, rotation on MESH node only
//      (the anti-pattern)                                   vs corrected numpy rotated -> documented error
//   D  bind-sandwich variant of A (bindMatrix=I, GLTFLoader convention) -> expect ~0
// Controls (permutation / scale / wrong-side ibm) for signature separation.
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import fs from 'fs';
import AdmZip from 'adm-zip';

const buf = fs.readFileSync('/home/z/my-project/scripts/jsverify/s37_myglb.glb');
const truthCache = {};
function loadNpz(p) {
  if (truthCache[p]) return truthCache[p];
  const z = new AdmZip(p);
  const out = {};
  for (const e of z.getEntries()) {
    if (!e.name.endsWith('.npy')) continue;
    const d = e.getData();
    if (e.name === 'ts.npy') out.ts = Array.from(new Float32Array(d.buffer.slice(d.byteOffset + 80, d.byteOffset + d.byteLength)));
    else out[e.name.slice(1, -4)] = new Float32Array(d.buffer.slice(d.byteOffset + 80, d.byteOffset + d.byteLength));
  }
  out.ts.sort((a, b) => a - b);
  truthCache[p] = out;
  return out;
}
const truth = loadNpz('/home/z/my-project/scripts/jsverify/s38_fk/_001_idle_stand.npz');
const clipName = '_001_idle_stand';

async function freshScene() {
  const ab2 = buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength);
  const gltf = await new Promise((res, rej) => { new GLTFLoader().parse(ab2, '', res, rej); });
  let sm = null; gltf.scene.traverse(o => { if (o.isSkinnedMesh) sm = o; });
  return { gltf, sm };
}

function manualSkin(mesh, opts = {}) {
  mesh.matrixWorldNeedsUpdate = true; if (mesh.parent) mesh.parent.updateMatrixWorld(true); else mesh.updateMatrixWorld(true);
  const N = mesh.geometry.attributes.position.count;
  const out = new Float32Array(N * 3);
  const v = new THREE.Vector3(), m = new THREE.Matrix4(), p = new THREE.Vector3();
  const pos = mesh.geometry.attributes.position;
  const si = mesh.geometry.attributes.skinIndex, sw = mesh.geometry.attributes.skinWeight;
  const BM = opts.bindMatrix || null, BMI = opts.bindMatrixInverse || null;
  for (let i = 0; i < N; i++) {
    v.fromBufferAttribute(pos, i);
    let x = 0, y = 0, z = 0;
    for (let j = 0; j < 4; j++) {
      const w = sw.getComponent(i, j); if (!w) continue;
      const b = si.getComponent(i, j);
      if (opts.ibmWrongSide) m.multiplyMatrices(mesh.skeleton.boneInverses[b], mesh.skeleton.bones[b].matrixWorld);
      else m.multiplyMatrices(mesh.skeleton.bones[b].matrixWorld, mesh.skeleton.boneInverses[b]);
      if (BM) m.multiply(BM);
      p.copy(v).applyMatrix4(m);
      x += w * p.x; y += w * p.y; z += w * p.z;
    }
    if (BMI) p.set(x, y, z).applyMatrix4(BMI);
    out[i*3] = p.x; out[i*3+1] = p.y; out[i*3+2] = p.z;
  }
  return out;
}

function compare(got, exp) {
  const N = exp.length / 3;
  let worst = 0, sum = 0, wi = 0;
  for (let i = 0; i < N; i++) {
    const d = Math.hypot(got[i*3]-exp[i*3], got[i*3+1]-exp[i*3+1], got[i*3+2]-exp[i*3+2]);
    sum += d; if (d > worst) { worst = d; wi = i; }
  }
  return { worst_cm: +(worst*100).toFixed(3), mean_cm: +(sum/N*100).toFixed(3), worst_vert: wi };
}

// numpy-side rotation for space-matched comparisons (the page applies R to the scene root)
const R = new THREE.Matrix4().makeRotationX(-Math.PI / 2);
function rotRef(exp) {
  const N = exp.length / 3, out = new Float32Array(exp.length);
  const v = new THREE.Vector3();
  for (let i = 0; i < N; i++) {
    v.set(exp[i*3], exp[i*3+1], exp[i*3+2]).applyMatrix4(R);
    out[i*3] = v.x; out[i*3+1] = v.y; out[i*3+2] = v.z;
  }
  return out;
}

const report = {};

// A: unrotated, world@ibm, bind pose t=0 vs corrected numpy
{
  const { gltf, sm } = await freshScene();
  const mixer = new THREE.AnimationMixer(gltf.scene);
  const a = mixer.clipAction(gltf.animations.find(c => c.name === clipName)); a.play(); mixer.setTime(0);
  report.A_worldIbm_unrotated_vs_correctedNumpy = compare(manualSkin(sm), truth['0']);
}

// B: rotation on the bone ANCESTOR (gltfScene), bones carry R, compare to ROTATED numpy ref
{
  const { gltf, sm } = await freshScene();
  gltf.scene.rotation.x = -Math.PI / 2;
  const mixer = new THREE.AnimationMixer(gltf.scene);
  const a = mixer.clipAction(gltf.animations.find(c => c.name === clipName)); a.play(); mixer.setTime(0);
  report.B_rotationOnBoneAncestor_vs_rotatedNumpy = compare(manualSkin(sm), rotRef(truth['0']));
}

// C: rotation on the MESH node ONLY (anti-pattern: skinned verts ignore mesh transform)
{
  const { gltf, sm } = await freshScene();
  const mixer = new THREE.AnimationMixer(gltf.scene);
  const a = mixer.clipAction(gltf.animations.find(c => c.name === clipName)); a.play(); mixer.setTime(0);
  sm.rotation.x = -Math.PI / 2;
  report.C_rotationOnMeshNode_vs_rotatedNumpy = compare(manualSkin(sm), rotRef(truth['0']));
}

// D: bind sandwich with identity bind (GLTFLoader convention) — must equal A
{
  const { gltf, sm } = await freshScene();
  const mixer = new THREE.AnimationMixer(gltf.scene);
  const a = mixer.clipAction(gltf.animations.find(c => c.name === clipName)); a.play(); mixer.setTime(0);
  sm.bindMatrix.identity(); sm.bindMatrixInverse.identity();
  report.D_identityBindSandwich_vs_correctedNumpy = compare(manualSkin(sm, { bindMatrix: sm.bindMatrix, bindMatrixInverse: sm.bindMatrixInverse }), truth['0']);
}

// E: ibm on the wrong side (invB @ world — the s37 numpy bug, three.js side) — the signature
{
  const { gltf, sm } = await freshScene();
  const mixer = new THREE.AnimationMixer(gltf.scene);
  const a = mixer.clipAction(gltf.animations.find(c => c.name === clipName)); a.play(); mixer.setTime(0);
  report.E_ibmWrongSide_signature = compare(manualSkin(sm, { ibmWrongSide: true }), truth['0']);
}

// F: cross-check — CORRECT three.js vs the OLD (buggy) numpy truth, at t=0 (the s37 confusion, quantified)
{
  const old = loadNpz('/home/z/my-project/scripts/jsverify/s37_fk/_001_idle_stand.npz');
  const { gltf, sm } = await freshScene();
  const mixer = new THREE.AnimationMixer(gltf.scene);
  const a = mixer.clipAction(gltf.animations.find(c => c.name === clipName)); a.play(); mixer.setTime(0);
  report.F_correctThree_vs_BUGGYs37Numpy = compare(manualSkin(sm), old['0']);
}

for (const [k, v] of Object.entries(report)) console.log(k.padEnd(46), JSON.stringify(v));
fs.writeFileSync('/home/z/my-project/scripts/jsverify/s38_t1_skin_matrix.json', JSON.stringify(report, null, 1));
console.log('saved s38_t1_skin_matrix.json');
