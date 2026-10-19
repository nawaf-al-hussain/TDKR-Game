// s38 T1a — ROOT-CAUSE the "162 cm hand-built skinning error".
// Reconstructs the hand-built three.js skinning path (r160) with every
// candidate convention error enumerated, measures each against the numpy
// FK ground truth (s37_fk npz, file-space, world=identity), and identifies
// which single convention produces the observed signature
// ("bone matrixWorld matches, vertices off by ~1.6 m") and its minimal fix.
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import fs from 'fs';
import AdmZip from 'adm-zip';

const buf = fs.readFileSync('/home/z/my-project/scripts/jsverify/s37_myglb.glb');
const ab = buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength);
const gltf = await new Promise((res, rej) => { new GLTFLoader().parse(ab, '', res, rej); });
const scene = gltf.scene;
let sm = null; scene.traverse(o => { if (o.isSkinnedMesh) sm = o; });
const N = sm.geometry.attributes.position.count;

// numpy ground truth
function loadNpz(p) {
  const z = new AdmZip(p);
  const out = {};
  for (const e of z.getEntries()) {
    if (!e.name.endsWith('.npy')) continue;
    const d = e.getData();
    if (e.name === 'ts.npy') {
      out.ts = Array.from(new Float32Array(d.buffer.slice(d.byteOffset + 80, d.byteOffset + d.byteLength)));
    } else {
      out[e.name.slice(1, -4)] = new Float32Array(d.buffer.slice(d.byteOffset + 80, d.byteOffset + d.byteLength));
    }
  }
  out.ts.sort((a, b) => a - b);
  return out;
}
const truth = loadNpz('/home/z/my-project/scripts/jsverify/s37_fk/_001_idle_stand.npz');
const clip = gltf.animations.find(c => c.name === '_001_idle_stand');

function compare(got, exp) {
  let worst = 0, sum = 0;
  for (let i = 0; i < N; i++) {
    const d = Math.hypot(got[i*3]-exp[i*3], got[i*3+1]-exp[i*3+1], got[i*3+2]-exp[i*3+2]);
    sum += d; if (d > worst) worst = d;
  }
  return { worst_m: worst, mean_m: sum / N };
}
const fmt = r => `worst ${(r.worst_m*100).toFixed(2)} cm, mean ${(r.mean_m*100).toFixed(2)} cm`;

// manual skin: SUM w_b * (bone.matrixWorld * boneInverses[b]) * v  (diag convention)
function manualSkin(mesh) {
  mesh.updateMatrixWorld(true);
  const out = new Float32Array(N * 3);
  const v = new THREE.Vector3(), m = new THREE.Matrix4(), p = new THREE.Vector3();
  const pos = mesh.geometry.attributes.position;
  const si = mesh.geometry.attributes.skinIndex, sw = mesh.geometry.attributes.skinWeight;
  for (let i = 0; i < N; i++) {
    v.fromBufferAttribute(pos, i);
    let x = 0, y = 0, z = 0;
    for (let j = 0; j < 4; j++) {
      const w = sw.getComponent(i, j); if (!w) continue;
      const b = si.getComponent(i, j);
      m.multiplyMatrices(mesh.skeleton.bones[b].matrixWorld, mesh.skeleton.boneInverses[b]);
      p.copy(v).applyMatrix4(m);
      x += w * p.x; y += w * p.y; z += w * p.z;
    }
    out[i*3] = x; out[i*3+1] = y; out[i*3+2] = z;
  }
  return out;
}
// manual skin WITH the three.js bind sandwich:
// p' = bindMatrixInverse * SUM w_b (bone.matrixWorld * ibm[b]) * bindMatrix * v
function manualSkinBind(mesh) {
  mesh.updateMatrixWorld(true);
  const out = new Float32Array(N * 3);
  const v = new THREE.Vector3(), m = new THREE.Matrix4(), p = new THREE.Vector3();
  const pos = mesh.geometry.attributes.position;
  const si = mesh.geometry.attributes.skinIndex, sw = mesh.geometry.attributes.skinWeight;
  const BM = mesh.bindMatrix, BMI = mesh.bindMatrixInverse;
  for (let i = 0; i < N; i++) {
    v.fromBufferAttribute(pos, i);
    let x = 0, y = 0, z = 0;
    for (let j = 0; j < 4; j++) {
      const w = sw.getComponent(i, j); if (!w) continue;
      const b = si.getComponent(i, j);
      m.multiplyMatrices(mesh.skeleton.bones[b].matrixWorld, mesh.skeleton.boneInverses[b]);
      m.multiply(BM);                       // bindMatrix on the right of the sum...
      p.copy(v).applyMatrix4(m);
      x += w * p.x; y += w * p.y; z += w * p.z;
    }
    p.set(x, y, z).applyMatrix4(BMI);       // ...then bindMatrixInverse outside
    out[i*3] = p.x; out[i*3+1] = p.y; out[i*3+2] = p.z;
  }
  return out;
}

const report = {};

// ---- C0: unrotated world (GLTFLoader path as-is, no page rotation) + manual skin, bind pose t=0
{
  const mixer = new THREE.AnimationMixer(scene);
  const a = mixer.clipAction(clip); a.play(); mixer.setTime(0);
  const got = manualSkin(sm);
  report.C0_noRotation_bindpose = compare(got, truth['0']);
  a.stop();
}

// ---- C1: THE PAGE ROTATION applied to the armature root (z-up fix, rotation.x=-PI/2),
//          manual skin WITHOUT bind sandwich -> candidate repro of the 162 cm error
{
  const mixer = new THREE.AnimationMixer(scene);
  const a = mixer.clipAction(clip); a.play(); mixer.setTime(0);
  scene.rotation.x = -Math.PI / 2; scene.updateMatrixWorld(true);
  // bone matrixWorld sanity: bones ARE rotated (what "bone matrixWorld matched" meant:
  // each bone matrixWorld == expected * R, consistent — but the SKIN SUM is no longer
  // valid because vertex data is still in unrotated bind space)
  const got = manualSkin(sm);
  report.C1_pageRotation_noBindSandwich = compare(got, truth['0']);
  // and with the sandwich (mesh.bind with bindMatrix = mesh.matrixWorld at bind time)
  const got2 = manualSkinBind(sm);
  report.C1b_pageRotation_withBindSandwich = compare(got2, truth['0']);
  scene.rotation.x = 0; scene.updateMatrixWorld(true);
  a.stop();
}

// ---- C2: skeleton constructed BEFORE scene.updateMatrixWorld (calculateInverses
//          from identity world) -> garbage boneInverses, no rotation involved
{
  // GLTFLoader already built skeleton+inverses; emulate the timing error by
  // recalculating inverses from a FRESH, never-updated bone tree
  const mixer = new THREE.AnimationMixer(scene);
  const a = mixer.clipAction(clip); a.play(); mixer.setTime(0);
  const bones = sm.skeleton.bones;
  const saved = sm.skeleton.boneInverses.map(m => m.clone());
  // simulate: inverses computed before any matrix update
  for (const b of bones) b.matrixWorld.identity();
  sm.skeleton.calculateInverses();
  scene.updateMatrixWorld(true);
  const got = manualSkin(sm);
  report.C2_calculateInverses_beforeUpdate = compare(got, truth['0']);
  sm.skeleton.boneInverses = saved;
  a.stop();
}

// ---- C3: boneInverses ORDER permuted (control — must NOT look like a clean offset)
{
  const mixer = new THREE.AnimationMixer(scene);
  const a = mixer.clipAction(clip); a.play(); mixer.setTime(0);
  const saved = sm.skeleton.boneInverses.map(m => m.clone());
  const B = saved.length;
  const perm = saved.map((_, i) => saved[(i + 1) % B]);
  sm.skeleton.boneInverses = perm;
  const got = manualSkin(sm);
  report.C3_boneInverses_shifted_control = compare(got, truth['0']);
  sm.skeleton.boneInverses = saved;
  a.stop();
}

// ---- C4: unnormalised weights x1.4 (control)
{
  const mixer = new THREE.AnimationMixer(scene);
  const a = mixer.clipAction(clip); a.play(); mixer.setTime(0);
  const sw = sm.geometry.attributes.skinWeight;
  const saved = sw.array.slice();
  for (let i = 0; i < sw.array.length; i++) sw.array[i] *= 1.4;
  sw.needsUpdate = true;
  const got = manualSkin(sm);
  report.C4_weights_x14_control = compare(got, truth['0']);
  sw.array.set(saved); sw.needsUpdate = true;
  a.stop();
}

// ---- C5: the page rotation as a TRANSFORM ON THE MESH NODE + mesh.bind() convention
//          (the hand-built path: SkinnedMesh under rotated root, skin sum in world)
{
  const mixer = new THREE.AnimationMixer(scene);
  const a = mixer.clipAction(clip); a.play(); mixer.setTime(0);
  // rotate only the mesh node, bones stay unrotated under an unrotated root:
  const prevParentRot = sm.rotation.clone();
  sm.rotation.x = -Math.PI / 2;
  sm.updateMatrixWorld(true);
  // emulate hand-built: bindMatrix left IDENTITY (never called bind)
  const got = manualSkin(sm);
  report.C5_meshRotated_bindIdentity = compare(got, truth['0']);
  // fix: bind() AFTER placing the mesh (bindMatrix = mesh.matrixWorld)
  sm.bind(sm.skeleton, new THREE.Matrix4().copy(sm.matrixWorld));
  sm.updateMatrixWorld(true);
  const got2 = manualSkinBind(sm);
  report.C5b_meshRotated_boundAfter = compare(got2, truth['0']);
  sm.rotation.copy(prevParentRot);
  sm.bindMatrix.identity(); sm.bindMatrixInverse.identity();
  a.stop();
}

for (const [k, v] of Object.entries(report)) console.log(k.padEnd(42), fmt(v));
fs.writeFileSync('/home/z/my-project/scripts/jsverify/s38_t1_skin_repro.json',
  JSON.stringify(Object.fromEntries(Object.entries(report).map(([k, v]) =>
    [k, { worst_cm: +(v.worst_m * 100).toFixed(3), mean_cm: +(v.mean_m * 100).toFixed(3) }])), null, 1));
console.log('saved s38_t1_skin_repro.json');
