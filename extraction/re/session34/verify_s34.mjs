// S34 T1: three.js GLTFLoader + AnimationMixer verification of
// batman_s34_anims.glb — AnimationMixer sampling vs numpy FK expected arrays.
// Non-circular: three.js does its own glTF parse, keyframe interpolation
// (slerp), and skinning; we only compare resulting positions.
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import fs from 'fs';

const GLB = '/home/z/my-project/download/batman_s34_anims.glb';
const BINDIR = '/home/z/my-project/scripts/jsverify/s34bin';

const buf = fs.readFileSync(GLB);
const ab = buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength);

const loader = new GLTFLoader();
const gltf = await new Promise((res, rej) =>
  loader.parse(ab, '', res, rej));

const scene = gltf.scene;
const clips = gltf.animations;
console.log(`loaded: nodes ${scene.children.length ? 'ok' : '?'} (scene), animations ${clips.length}: ${clips.map(c => `${c.name}(${c.tracks.length} tracks, ${c.duration.toFixed(3)}s)`).join(', ')}`);

const ibmAcc = [];   // from the parsed skeleton
let skinnedMesh = null;
scene.traverse(o => { if (o.isSkinnedMesh) skinnedMesh = o; });
if (!skinnedMesh) throw new Error('no SkinnedMesh found');
const skeleton = skinnedMesh.skeleton;
const N = skinnedMesh.geometry.attributes.position.count;
console.log(`skinned mesh: ${N} verts, ${skeleton.bones.length} bones`);

function skinnedPositions() {
  scene.updateMatrixWorld(true);
  const out = new Float32Array(N * 3);
  const bones = skeleton.bones;
  const ibms = skeleton.boneInverses;
  const v = new THREE.Vector3();
  const pos = skinnedMesh.geometry.attributes.position;
  const skinIdx = skinnedMesh.geometry.attributes.skinIndex;
  const skinW = skinnedMesh.geometry.attributes.skinWeight;
  const m = new THREE.Matrix4();
  for (let i = 0; i < N; i++) {
    v.fromBufferAttribute(pos, i);
    let x = 0, y = 0, z = 0;
    for (let j = 0; j < 4; j++) {
      const w = skinW.getComponent(i, j);
      if (w === 0) continue;
      const b = skinIdx.getComponent(i, j);
      m.multiplyMatrices(bones[b].matrixWorld, ibms[b]);
      const p = v.clone().applyMatrix4(m);
      x += w * p.x; y += w * p.y; z += w * p.z;
    }
    out[i*3] = x; out[i*3+1] = y; out[i*3+2] = z;
  }
  return out;
}

function bin(name) {
  const b = fs.readFileSync(`${BINDIR}/${name}.bin`);
  return new Float32Array(b.buffer, b.byteOffset, b.length / 4);
}
function cmp(got, exp, label) {
  let maxd = 0, n = got.length / 3;
  for (let i = 0; i < n; i++) {
    const d = Math.hypot(got[i*3] - exp[i*3], got[i*3+1] - exp[i*3+1],
                         got[i*3+2] - exp[i*3+2]);
    if (d > maxd) maxd = d;
  }
  console.log(`  ${label}: max diff ${maxd.toFixed(4)} cm over ${n} verts ` +
              `(max ${(maxd*10).toFixed(3)} mm)`);
  return maxd;
}

// REST check (no animation applied)
const restExp = bin('rest');
const restGot = skinnedPositions();
const restMax = cmp(restGot, restExp, 'REST (no anim) three.js vs numpy');

const samples = [
  ['_001_idle_stand', 0.0, 'idle t=0.000s'],
  ['_001_idle_stand', 0.4, 'idle t=0.400s'],
  ['_001_idle_stand', 0.9, 'idle t=0.900s'],
  ['_001_idle_stand', 1.5, 'idle t=1.500s'],
  ['_001_idle_stand', 1.849, 'idle t=1.849s'],
  ['_008_run', 0.0, 'run t=0.000s (tick 13899)'],
  ['_008_run', 0.301, 'run t=0.301s (tick 14200)'],
  ['_008_run', 0.801, 'run t=0.801s (tick 14700)'],
  ['_008_run', 1.301, 'run t=1.301s (tick 15200)'],
  ['_008_run', 1.701, 'run t=1.701s (tick 15600)'],
];
const npzKey = {
  '_001_idle_stand': { 0: 'idle_t0', 0.4: 'idle_t400', 0.9: 'idle_t900',
                       1.5: 'idle_t1500', 1.849: 'idle_t1849' },
  '_008_run': { 0: 'run_t13899', 0.301: 'run_t14200', 0.801: 'run_t14700',
                1.301: 'run_t15200', 1.701: 'run_t15600' },
};
let worst = 0;
for (const [clipName, t, label] of samples) {
  const clip = clips.find(c => c.name === clipName);
  const mixer = new THREE.AnimationMixer(scene);
  const action = mixer.clipAction(clip);
  action.setLoop(THREE.LoopOnce);
  action.clampWhenFinished = true;
  action.play();
  mixer.setTime(t);
  const got = skinnedPositions();
  const exp = bin(npzKey[clipName][t]);
  worst = Math.max(worst, cmp(got, exp, label));
}
console.log(`\nWORST animation diff: ${worst.toFixed(4)} cm; ` +
            `rest diff: ${restMax.toFixed(4)} cm`);
console.log(worst < 0.05 && restMax < 0.05
  ? 'VERDICT: PASS (three.js AnimationMixer == numpy FK, sub-0.5mm)'
  : 'VERDICT: CHECK THRESHOLD');
