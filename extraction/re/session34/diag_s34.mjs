import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import fs from 'fs';
const buf = fs.readFileSync('/home/z/my-project/download/batman_s34_anims.glb');
const ab = buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength);
const gltf = await new Promise((res, rej) => { new GLTFLoader().parse(ab, '', res, rej); });
const scene = gltf.scene;
let sm = null; scene.traverse(o => { if (o.isSkinnedMesh) sm = o; });
const N = sm.geometry.attributes.position.count;
function skinned() {
  scene.updateMatrixWorld(true);
  const out = new Float32Array(N * 3);
  const bones = sm.skeleton.bones, ibms = sm.skeleton.boneInverses;
  const v = new THREE.Vector3(), m = new THREE.Matrix4();
  const pos = sm.geometry.attributes.position;
  const si = sm.geometry.attributes.skinIndex, sw = sm.geometry.attributes.skinWeight;
  for (let i = 0; i < N; i++) {
    v.fromBufferAttribute(pos, i);
    let x = 0, y = 0, z = 0;
    for (let j = 0; j < 4; j++) {
      const w = sw.getComponent(i, j); if (!w) continue;
      const b = si.getComponent(i, j);
      m.multiplyMatrices(bones[b].matrixWorld, ibms[b]);
      const p = v.clone().applyMatrix4(m);
      x += w*p.x; y += w*p.y; z += w*p.z;
    }
    out[i*3] = x; out[i*3+1] = y; out[i*3+2] = z;
  }
  return out;
}
const mixer = new THREE.AnimationMixer(scene);
const clip = gltf.animations.find(c => c.name === '_008_run');
const action = mixer.clipAction(clip); action.play();
mixer.setTime(0.801);
const got = skinned();
const eb = fs.readFileSync('/home/z/my-project/scripts/jsverify/s34bin/run_t14700.bin');
const exp = new Float32Array(eb.buffer, eb.byteOffset, eb.length/4);
let worst = [];
for (let i = 0; i < N; i++) {
  const d = Math.hypot(got[i*3]-exp[i*3], got[i*3+1]-exp[i*3+1], got[i*3+2]-exp[i*3+2]);
  worst.push([d, i]);
}
worst.sort((a, b) => b[0] - a[0]);
console.log('top-8 divergent verts (diff cm, vertIdx, weights):');
for (const [d, i] of worst.slice(0, 8)) {
  const jn = [], wt = [];
  for (let j = 0; j < 4; j++) {
    jn.push(sm.skeleton.bones[sm.geometry.attributes.skinIndex.getComponent(i, j)].name);
    wt.push(sm.geometry.attributes.skinWeight.getComponent(i, j).toFixed(3));
  }
  console.log(`  ${d.toFixed(3)} cm  v${i}  ${jn.map((n, k) => n + ':' + wt[k]).join(' ')}`);
}
// bone world positions three vs nothing — print animated quats per bone for the worst bone
console.log('\nclip tracks:', clip.tracks.length);
for (const tr of clip.tracks) {
  if (tr.name.endsWith('.quaternion')) {
    const nm = tr.name.split('.')[0];
    // print values around t=0.801
    const times = tr.times, vals = tr.values;
    let k = 0;
    while (k < times.length && times[k] < 0.801) k++;
    if (k > 0 && k < times.length) {
      const a = [vals[(k-1)*4], vals[(k-1)*4+1], vals[(k-1)*4+2], vals[(k-1)*4+3]];
      const b = [vals[k*4], vals[k*4+1], vals[k*4+2], vals[k*4+3]];
      const na = Math.hypot(...a), nb = Math.hypot(...b);
      if (Math.abs(na-1) > 0.01 || Math.abs(nb-1) > 0.01)
        console.log(`  NON-UNIT ${nm}: norms ${na.toFixed(4)} ${nb.toFixed(4)} at t=${times[k-1].toFixed(3)},${times[k].toFixed(3)}`);
    }
  }
}
console.log('done');
