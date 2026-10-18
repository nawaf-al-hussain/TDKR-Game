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

// forward-only fresh-state: times visited in ASCENDING order across all anims,
// a brand-new mixer/action per evaluation (no backward setTime anywhere)
const report = {};
for (const label of ['_001_idle_stand', '_007_walk', '_008_run', '_010_run_jump_start', '_461_batman_jab_countre_front_attack']) {
  const npz = fs.readFileSync(`/home/z/my-project/scripts/jsverify/s37_fk/${label}.npz`);
  // npz parse: minimal - we saved via numpy.savez (zip). Read via a plain zip walk.
  const Adm = await import('adm-zip').catch(() => null);
  let entries;
  if (Adm) { entries = new Adm.default(npz).getEntries(); }
  else {
    // fall back: use bun's zip? implement minimal stored/deflate reader via zlib
    const zlib = await import('zlib');
    entries = [];
    // parse zip central directory
    const eocd = npz.lastIndexOf(Buffer.from([0x50, 0x4b, 0x05, 0x06]));
    const cdOff = npz.readUInt32LE(eocd + 16), n = npz.readUInt16LE(eocd + 10);
    let off = cdOff;
    for (let i = 0; i < n; i++) {
      const method = npz.readUInt16LE(off + 10), csize = npz.readUInt32LE(off + 20),
            nameLen = npz.readUInt16LE(off + 28), extraLen = npz.readUInt16LE(off + 30),
            commLen = npz.readUInt16LE(off + 32), lho = npz.readUInt32LE(off + 42);
      const name = npz.slice(off + 46, off + 46 + nameLen).toString();
      const lhn = npz.readUInt16LE(lho + 26), lhe = npz.readUInt16LE(lho + 28);
      const dataOff = lho + 30 + lhn + lhe;
      const raw = npz.slice(dataOff, dataOff + csize);
      const data = method === 0 ? raw : zlib.inflateRawSync(raw);
      entries.push({ name, data });
      off += 46 + nameLen + extraLen + commLen;
    }
  }
  const ts = [];
  const dumps = {};
  for (const e of entries) {
    if (e.name === 'ts.npy') {
      // numpy .npy: skip 80-byte header
      const f32 = new Float32Array(e.data.buffer, e.data.byteOffset + 80, (e.data.length - 80) / 4);
      for (let i = 0; i < f32.length; i++) ts.push(f32[i]);
    } else if (e.name.endsWith('.npy')) {
      dumps[e.name.slice(1, -4)] = new Float32Array(
        e.data.buffer.slice(e.data.byteOffset + 80, e.data.byteOffset + e.data.length));
    }
  }
  ts.sort((a, b) => a - b);
  const clip = gltf.animations.find(c => c.name === label);
  let worst = 0, worstT = 0, sum = 0, cnt = 0;
  for (const t of ts) {
    const mixer = new THREE.AnimationMixer(scene);
    const action = mixer.clipAction(clip);
    action.play();
    mixer.setTime(t);                       // forward-only: ts ascending, fresh mixer
    const got = skinned();
    const exp = dumps[`t${Math.round(t * 1000)}`];
    if (!exp) continue;
    for (let i = 0; i < N; i++) {
      const d = Math.hypot(got[i*3]-exp[i*3], got[i*3+1]-exp[i*3+1], got[i*3+2]-exp[i*3+2]) * 100;
      sum += d; cnt++;
      if (d > worst) { worst = d; worstT = t; }
    }
  }
  report[label] = { worst_cm: +worst.toFixed(4), worst_t_s: +worstT.toFixed(3),
                    mean_cm: +(sum / Math.max(cnt, 1)).toFixed(5), n_times: ts.length };
  console.log(label, JSON.stringify(report[label]));
}
fs.writeFileSync('/home/z/my-project/scripts/jsverify/s37_threews_report.json', JSON.stringify(report, null, 1));
console.log('saved s37_threews_report.json');
