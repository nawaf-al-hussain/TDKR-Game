// s38 T1a — FINAL ARBITER with CORRECT npy header parsing.
// three.js (GLTFLoader, fresh matrices, W@ibm) vs s37_fk truth (invB@world + row einsum).
// These conventions are algebraically identical (numpy side is the transpose with row
// vectors), so the expected error is ~0. Any residual localizes precisely.
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import fs from 'fs';
import AdmZip from 'adm-zip';

function readNpyBuf(d) {
  const hlen = d.readUInt16LE(8);
  const off = 10 + hlen;
  const descr = d.slice(10, 10 + hlen).toString();
  const f32 = descr.includes('<f4') || descr.includes('float32');
  const f64 = descr.includes('<f8') || descr.includes('float64');
  const body = d.slice(off);
  if (f32) return new Float32Array(body.buffer.slice(body.byteOffset, body.byteOffset + body.byteLength));
  if (f64) return new Float64Array(body.buffer.slice(body.byteOffset, body.byteOffset + body.byteLength));
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

function skinAt(t) {
  const mixer = new THREE.AnimationMixer(gltf.scene);
  const a = mixer.clipAction(gltf.animations.find(c => c.name === '_001_idle_stand')); a.play();
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

const truth = loadNpz('/home/z/my-project/scripts/jsverify/s37_fk/_001_idle_stand.npz');
console.log('truth ticks:', truth.ts.length, 'first:', truth.ts.slice(0, 4));

let gWorst = 0, gSum = 0, gN = 0;
for (const t of [0, 0.25, 0.5, 1.0, 1.35, 2.0, 3.0, 4.0, 4.95]) {
  const got = skinAt(t);
  const key = String(Math.round(t * 1000));
  const exp = truth[key];
  if (!exp) { console.log(`t=${t}: no truth key ${key}`); continue; }
  let worst = 0, sum = 0;
  for (let i = 0; i < N; i++) {
    const d = Math.hypot(got[i*3]-exp[i*3], got[i*3+1]-exp[i*3+1], got[i*3+2]-exp[i*3+2]);
    sum += d; if (d > worst) worst = d;
  }
  gWorst = Math.max(gWorst, worst); gSum += sum / N; gN++;
  console.log(`idle t=${t}s: worst ${(worst*100).toFixed(4)} cm, mean ${(sum/N*100).toFixed(4)} cm`);
}
console.log(`OVERALL: worst ${(gWorst*100).toFixed(4)} cm, mean-of-means ${(gSum/gN*100).toFixed(4)} cm over ${gN} times`);

// also the SHUFFLED-REFERENCE null: three.js idle(t=1.0) vs truth at a random other tick
{
  const got = skinAt(1.0);
  const key = '3450';
  const exp = truth[key];
  let worst = 0;
  for (let i = 0; i < N; i++) {
    const d = Math.hypot(got[i*3]-exp[i*3], got[i*3+1]-exp[i*3+1], got[i*3+2]-exp[i*3+2]);
    if (d > worst) worst = d;
  }
  console.log(`NULL (t=1.0 vs truth@3.45s): worst ${(worst*100).toFixed(1)} cm  [should be large]`);
}
