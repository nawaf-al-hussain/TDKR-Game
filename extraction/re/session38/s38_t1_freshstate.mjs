// s38 T1a — FULL three.js fresh-state check vs DEFINITIVE truth (s38_truth).
// Forward-only: brand-new mixer per time, ascending t, all 5 anims.
// Expected: ~0 everywhere (conventions proven identical this session).
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import fs from 'fs';
import AdmZip from 'adm-zip';

function readNpyBuf(d) {
  const hlen = d.readUInt16LE(8);
  const off = 10 + hlen;
  const descr = d.slice(10, 10 + hlen).toString();
  if (descr.includes('<f4')) return new Float32Array(d.buffer.slice(d.byteOffset + off, d.byteOffset + d.byteLength));
  if (descr.includes('<f8')) return new Float64Array(d.buffer.slice(d.byteOffset + off, d.byteOffset + d.byteLength));
  throw new Error('dtype? ' + descr);
}
function loadNpz(p) {
  const z = new AdmZip(p);
  const out = {};
  for (const e of z.getEntries()) {
    if (!e.name.endsWith('.npy')) continue;
    const d = e.getData();
    if (e.name === 'ts.npy') out.ts = Array.from(readNpyBuf(d));
    else out[e.name.slice(1, -4)] = readNpyBuf(d);
  }
  out.ts.sort((a, b) => a - b);
  return out;
}

const buf = fs.readFileSync('/home/z/my-project/scripts/jsverify/s37_myglb.glb');
const ab = buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength);
const gltf = await new Promise((r, j) => new GLTFLoader().parse(ab, '', r, j));
let sm = null; gltf.scene.traverse(o => { if (o.isSkinnedMesh) sm = o; });
const N = sm.geometry.attributes.position.count;

function skinAt(clip, t) {
  const mixer = new THREE.AnimationMixer(gltf.scene);
  const a = mixer.clipAction(clip); a.play();
  mixer.setTime(t);
  gltf.scene.updateMatrixWorld(true);
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

const report = {};
const labels = ['_001_idle_stand', '_007_walk', '_008_run', '_010_run_jump_start', '_461_batman_jab_countre_front_attack'];
let gWorst = 0;
for (const label of labels) {
  const truth = loadNpz(`/home/z/my-project/scripts/jsverify/s38_truth/${label}.npz`);
  const clip = gltf.animations.find(c => c.name === label);
  let worst = 0, worstT = 0, sum = 0, cnt = 0;
  for (const t of truth.ts) {
    const got = skinAt(clip, t);   // ascending t, fresh mixer
    const exp = truth[String(Math.round(t * 1000))];
    if (!exp) continue;
    for (let i = 0; i < N; i++) {
      const d = Math.hypot(got[i*3]-exp[i*3], got[i*3+1]-exp[i*3+1], got[i*3+2]-exp[i*3+2]) * 100;
      sum += d; cnt++;
      if (d > worst) { worst = d; worstT = t; }
    }
  }
  gWorst = Math.max(gWorst, worst);
  report[label] = { worst_cm: +worst.toFixed(4), worst_t_s: +worstT.toFixed(3), mean_cm: +(sum / Math.max(cnt,1)).toFixed(5), n_evals: cnt };
  console.log(label, JSON.stringify(report[label]));
}
// null: idle(1.0s) vs truth@3.45s (wrong-time pairing must be large)
{
  const truth = loadNpz('/home/z/my-project/scripts/jsverify/s38_truth/_001_idle_stand.npz');
  const clip = gltf.animations.find(c => c.name === '_001_idle_stand');
  const got = skinAt(clip, 1.0);
  const exp = truth['3450'];
  let worst = 0;
  for (let i = 0; i < N; i++) {
    const d = Math.hypot(got[i*3]-exp[i*3], got[i*3+1]-exp[i*3+1], got[i*3+2]-exp[i*3+2]) * 100;
    if (d > worst) worst = d;
  }
  report.null_wrong_time = { worst_cm: +worst.toFixed(1) };
  console.log('NULL wrong-time idle(1.0) vs truth(3.45):', worst.toFixed(1), 'cm [must be large]');
}
fs.writeFileSync('/home/z/my-project/scripts/jsverify/s38_t1_freshstate.json', JSON.stringify(report, null, 1));
console.log('GLOBAL worst:', (gWorst * 100).toFixed(4), 'cm — saved s38_t1_freshstate.json');
