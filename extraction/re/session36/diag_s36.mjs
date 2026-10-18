import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import fs from 'fs';
const buf = fs.readFileSync('/home/z/my-project/download/batman_s36_anims.glb');
const ab = buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength);
const gltf = await new Promise((res, rej) => { new GLTFLoader().parse(ab, '', res, rej); });
const scene = gltf.scene;
let sm = null; scene.traverse(o => { if (o.isSkinnedMesh) sm = o; });
const N = sm.geometry.attributes.position.count;
console.log('skinned verts:', N, 'anims:', gltf.animations.map(a => `${a.name}(${a.tracks.length}t, ${a.duration.toFixed(3)}s)`).join(' '));

function skinned() {
  scene.updateMatrixWorld(true);
  const out = new Float32Array(N * 3);
  const bones = sm.skeleton.bones, ibms = sm.skeleton.bones ? sm.skeleton.boneInverses : null;
  const ib = sm.skeleton.boneInverses;
  const v = new THREE.Vector3(), m = new THREE.Matrix4(), p = new THREE.Vector3();
  const pos = sm.geometry.attributes.position;
  const si = sm.geometry.attributes.skinIndex, sw = sm.geometry.attributes.skinWeight;
  for (let i = 0; i < N; i++) {
    v.fromBufferAttribute(pos, i);
    let x = 0, y = 0, z = 0;
    for (let j = 0; j < 4; j++) {
      const w = sw.getComponent(i, j); if (!w) continue;
      const b = si.getComponent(i, j);
      m.multiplyMatrices(sm.skeleton.bones[b].matrixWorld, ib[b]);
      p.copy(v).applyMatrix4(m);
      x += w * p.x; y += w * p.y; z += w * p.z;
    }
    out[i * 3] = x; out[i * 3 + 1] = y; out[i * 3 + 2] = z;
  }
  return out;
}

const meta = JSON.parse(fs.readFileSync('/home/z/my-project/scripts/jsverify/s35_meta.json'));
const restArr = new Float32Array(meta.rest);
let got = skinned();
let worst = 0;
for (let i = 0; i < N * 3; i++) worst = Math.max(worst, Math.abs(got[i] - restArr[i]));
console.log(`REST: three.js vs numpy worst |d| = ${(worst * 100).toFixed(4)} cm`);

const seams = JSON.parse(fs.readFileSync('/home/z/my-project/scripts/jsverify/s36_seams.json'));
const mixer = new THREE.AnimationMixer(scene);
// 1) r35-style samples (same 4 per clip) + seam-adjacent extras
const extras = [];
for (const [name, info] of Object.entries(seams)) {
  for (const s of info.seams_s) {
    extras.push([name, Math.max(0.001, s - 0.02)]);
    extras.push([name, Math.max(0.001, s + 0.02)]);
    extras.push([name, Math.max(0.001, s)]);
  }
}
for (const [name, file] of meta.samples) {
  const clip = gltf.animations.find(c => c.name === name);
  const action = mixer.clipAction(clip); action.play();
  mixer.setTime(file.t);
  got = skinned();
  const exp = new Float32Array(file.data);
  let worstV = 0, worstI = -1, sum = 0;
  for (let i = 0; i < N; i++) {
    const d = Math.hypot(got[i * 3] - exp[i * 3], got[i * 3 + 1] - exp[i * 3 + 1], got[i * 3 + 2] - exp[i * 3 + 2]);
    sum += d;
    if (d > worstV) { worstV = d; worstI = i; }
  }
  const nearSeam = (seams[name] ? seams[name].seams_s : []).some(s => Math.abs(s - file.t) < 0.05);
  console.log(`${name} @t=${file.t}s${nearSeam ? ' [NEAR-SEAM]' : ''}: worst ${(worstV * 100).toFixed(4)} cm, mean ${(sum / N * 100).toFixed(4)} cm (vert ${worstI})`);
  action.stop();
}
console.log('--- seam-adjacent samples ---');
for (const [name, t] of extras) {
  const clip = gltf.animations.find(c => c.name === name);
  if (!clip) continue;
  const action = mixer.clipAction(clip); action.play();
  mixer.setTime(t);
  got = skinned();
  // compare vs numpy reference at same t? we only have 4 dumps per clip; instead
  // measure the JUMP across the seam: |skinned(t-0.001) - skinned(t+0.001)|
  // as discontinuity evidence (numpy keys have no duplicate ticks at seams).
  mixer.setTime(Math.max(0.0005, t - 0.001));
  const a = skinned();
  mixer.setTime(t + 0.001);
  const b2 = skinned();
  let wJ = 0, wI = -1;
  for (let i = 0; i < N; i++) {
    const d = Math.hypot(a[i * 3] - b2[i * 3], a[i * 3 + 1] - b2[i * 3 + 1], a[i * 3 + 2] - b2[i * 3 + 2]);
    if (d > wJ) { wJ = d; wI = i; }
  }
  console.log(`${name} seam @t=${t}s: 2ms vertex jump worst ${(wJ * 100).toFixed(4)} cm (vert ${wI})`);
  action.stop();
}
