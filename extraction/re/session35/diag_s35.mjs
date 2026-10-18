import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import fs from 'fs';
const buf = fs.readFileSync('/home/z/my-project/download/batman_s35_anims.glb');
const ab = buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength);
const gltf = await new Promise((res, rej) => { new GLTFLoader().parse(ab, '', res, rej); });
const scene = gltf.scene;
let sm = null; scene.traverse(o => { if (o.isSkinnedMesh) sm = o; });
const N = sm.geometry.attributes.position.count;
console.log('skinned verts:', N, 'anims:', gltf.animations.map(a => `${a.name}(${a.tracks.length} tracks, dur ${a.duration.toFixed(3)}s)`));

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

// REST check: no animation
let got = skinned();
const meta = JSON.parse(fs.readFileSync('/home/z/my-project/scripts/jsverify/s35_meta.json'));
const restExp = new Float32Array(meta.rest.buffer ? meta.rest : Object.values(meta.rest));
// meta.rest is array-of-3N from python; rebuild
const restArr = new Float32Array(meta.rest);
let worst = 0;
for (let i = 0; i < N * 3; i++) worst = Math.max(worst, Math.abs(got[i] - restArr[i]));
console.log(`REST: three.js vs numpy worst |d| = ${(worst*100).toFixed(4)} cm`);

const mixer = new THREE.AnimationMixer(scene);
for (const [name, file] of meta.samples) {
  const clip = gltf.animations.find(c => c.name === name);
  const action = mixer.clipAction(clip); action.play();
  mixer.setTime(file.t);
  got = skinned();
  const exp = new Float32Array(file.data);
  let worstV = 0, worstI = -1, sum = 0;
  for (let i = 0; i < N; i++) {
    const d = Math.hypot(got[i*3]-exp[i*3], got[i*3+1]-exp[i*3+1], got[i*3+2]-exp[i*3+2]);
    sum += d;
    if (d > worstV) { worstV = d; worstI = i; }
  }
  console.log(`${name} @t=${file.t}s: three.js vs numpy FK worst ${ (worstV*100).toFixed(4)} cm, mean ${(sum/N*100).toFixed(4)} cm (vert ${worstI})`);
  action.stop();
}
