import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import fs from 'fs';
const buf = fs.readFileSync('/home/z/my-project/download/batman_s36_anims.glb');
const ab = buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength);
const gltf = await new Promise((res, rej) => { new GLTFLoader().parse(ab, '', res, rej); });
const scene = gltf.scene;
let sm = null; scene.traverse(o => { if (o.isSkinnedMesh) sm = o; });
const N = sm.geometry.attributes.position.count;
function skinned() {
  scene.updateMatrixWorld(true);
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
    out[i * 3] = x; out[i * 3 + 1] = y; out[i * 3 + 2] = z;
  }
  return out;
}
const ref = JSON.parse(fs.readFileSync('/home/z/my-project/scripts/jsverify/s36_fkref.json'))['_008_run'];
const clip = gltf.animations.find(c => c.name === '_008_run');
const mixer = new THREE.AnimationMixer(scene);
for (const t of [0.079, 0.081, 0.099, 0.101, 0.09, 0.119, 0.121]) {
  const action = mixer.clipAction(clip);
  action.stop(); action.play();
  mixer.setTime(t);
  const got = skinned();
  const exp = new Float32Array(ref[String(t)]);
  let w = 0, wi = -1, sum = 0;
  for (let i = 0; i < N; i++) {
    const d = Math.hypot(got[i*3]-exp[i*3], got[i*3+1]-exp[i*3+1], got[i*3+2]-exp[i*3+2]);
    sum += d; if (d > w) { w = d; wi = i; }
  }
  console.log(`_008_run @t=${t}: fresh-state three.js vs numpy worst ${(w*100).toFixed(4)} cm mean ${(sum/N*100).toFixed(4)} cm (vert ${wi})`);
}
// backward-time probe on a RUNNING action (reproduces the earlier 2.87 cm)
const action = mixer.clipAction(clip); action.stop(); action.play();
mixer.setTime(0.08); skinned();
mixer.setTime(0.079); const a = skinned();
mixer.setTime(0.081); const b = skinned();
let w = 0; for (let i = 0; i < N; i++) w = Math.max(w, Math.hypot(a[i*3]-b[i*3], a[i*3+1]-b[i*3+1], a[i*3+2]-b[i*3+2]));
console.log(`backward-setTime probe: |a-b| = ${(w*100).toFixed(4)} cm`);
