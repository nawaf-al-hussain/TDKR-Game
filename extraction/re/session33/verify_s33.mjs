// S33 T2: three.js verification of batman_s33_full.glb + batman_s33_posed25.glb
import * as THREE from 'three';
import fs from 'fs';

function readGlb(path) {
  const b = fs.readFileSync(path);
  const magic = b.readUInt32LE(0), ver = b.readUInt32LE(4), len = b.readUInt32LE(8);
  if (magic !== 0x46546C67) throw new Error('not glTF');
  let off = 12, json = null, bin = null;
  while (off < len) {
    const clen = b.readUInt32LE(off), ctype = b.readUInt32LE(off + 4);
    const chunk = b.subarray(off + 8, off + 8 + clen);
    if (ctype === 0x4E4F534A) json = JSON.parse(chunk.toString('utf8'));
    else if (ctype === 0x004E4942) bin = chunk;
    off += 8 + clen;
  }
  return { json, bin };
}
function accessorBytes(g, i) {
  const acc = g.json.accessors[i];
  const bv = g.json.bufferViews[acc.bufferView];
  const bo = (bv.byteOffset || 0) + (acc.byteOffset || 0);
  const ncomp = { SCALAR: 1, VEC2: 2, VEC3: 3, VEC4: 4, MAT4: 16 }[acc.type];
  const csize = { 5126: 4, 5123: 2, 5121: 1 }[acc.componentType];
  return { data: g.bin.subarray(bo, bo + acc.count * ncomp * csize), ncomp, csize, acc };
}
function verify(path, expectedSkinnedPath, label) {
  const g = readGlb(path);
  const J = g.json;
  console.log(`\n===== ${label}: ${path.split('/').pop()} =====`);
  console.log(`  nodes ${J.nodes.length}, joints ${J.skins[0].joints.length}, ` +
    `prims ${J.meshes[0].primitives.length}, TEXCOORD_0 ${J.meshes[0].primitives[0].attributes.TEXCOORD_0 !== undefined}`);
  const world = J.nodes.map(() => new THREE.Matrix4());
  const local = J.nodes.map(n => n.matrix ? new THREE.Matrix4().fromArray(n.matrix)
                                          : new THREE.Matrix4());
  const visited = new Set();
  function walk(i, parent) {
    if (visited.has(i)) return; visited.add(i);
    world[i].multiplyMatrices(parent, local[i]);
    (J.nodes[i].children || []).forEach(c => walk(c, world[i]));
  }
  J.scenes[J.scene || 0].nodes.forEach(r => walk(r, new THREE.Matrix4()));
  const skin = J.skins[0];
  const ibmAcc = accessorBytes(g, skin.inverseBindMatrices);
  const ibms = [];
  for (let j = 0; j < skin.joints.length; j++) {
    const fa = new Float32Array(ibmAcc.data.buffer, ibmAcc.data.byteOffset + j * 64, 16);
    ibms.push(new THREE.Matrix4().fromArray(Array.from(fa)));
  }
  const prim = J.meshes[0].primitives[0];
  const posA = accessorBytes(g, prim.attributes.POSITION);
  const uvA = accessorBytes(g, prim.attributes.TEXCOORD_0);
  const jntA = accessorBytes(g, prim.attributes.JOINTS_0);
  const wgtA = accessorBytes(g, prim.attributes.WEIGHTS_0);
  const N = posA.acc.count;
  const pos = new Float32Array(posA.data.buffer, posA.data.byteOffset, N * 3);
  const uvs = new Float32Array(uvA.data.buffer, uvA.data.byteOffset, N * 2);
  const jnt = jntA.csize === 1 ? new Uint8Array(jntA.data.buffer, jntA.data.byteOffset, N * 4)
                            : new Uint16Array(jntA.data.buffer, jntA.data.byteOffset, N * 4);
  const wgt = new Float32Array(wgtA.data.buffer, wgtA.data.byteOffset, N * 4);
  // UV sanity in three.js-side readback
  let uvBad = 0, tiles = new Set();
  for (let i = 0; i < N; i++) {
    const u = uvs[i*2], v = uvs[i*2+1];
    if (!(u >= 0 && u < 16 && v >= 0 && v < 16)) uvBad++;
    tiles.add(Math.floor(u / 4) + ',' + Math.floor(v / 4));
  }
  console.log(`  UVs: out-of-[0,16) ${uvBad}/${N}, tiles ${tiles.size}`);
  const skinned = new Float32Array(N * 3);
  const v = new THREE.Vector4(), m = new THREE.Matrix4(), acc = new THREE.Matrix4();
  for (let i = 0; i < N; i++) {
    acc.set(0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0);
    for (let k = 0; k < 4; k++) {
      const w = wgt[i * 4 + k];
      if (w === 0) continue;
      const j = jnt[i * 4 + k];
      m.multiplyMatrices(world[skin.joints[j]], ibms[j]);
      m.multiplyScalar(w);
      for (let q = 0; q < 16; q++) acc.elements[q] += m.elements[q];
    }
    v.set(pos[i*3], pos[i*3+1], pos[i*3+2], 1).applyMatrix4(acc);
    skinned[i*3] = v.x; skinned[i*3+1] = v.y; skinned[i*3+2] = v.z;
  }
  const exp = fs.readFileSync(expectedSkinnedPath);
  const expF = new Float32Array(exp.buffer, exp.byteOffset, N * 3);
  let eSelf = 0, eSelfMax = 0, eNumpy = 0, eNumpyMax = 0, exact = 0;
  for (let i = 0; i < N; i++) {
    const dx = skinned[i*3]-pos[i*3], dy = skinned[i*3+1]-pos[i*3+1], dz = skinned[i*3+2]-pos[i*3+2];
    const e1 = Math.sqrt(dx*dx + dy*dy + dz*dz);
    eSelf += e1; if (e1 > eSelfMax) eSelfMax = e1; if (e1 < 1e-3) exact++;
    const nx = skinned[i*3]-expF[i*3], ny = skinned[i*3+1]-expF[i*3+1], nz = skinned[i*3+2]-expF[i*3+2];
    const e2 = Math.sqrt(nx*nx + ny*ny + nz*nz);
    eNumpy += e2; if (e2 > eNumpyMax) eNumpyMax = e2;
  }
  console.log(`  three.js skinned vs unskinned: exact<0.1mm ${exact}/${N},` +
    ` mean ${(eSelf/N*100).toFixed(3)} cm, max ${(eSelfMax*100).toFixed(3)} cm`);
  console.log(`  three.js vs numpy: mean ${(eNumpy/N*1000).toFixed(4)} mm,` +
    ` max ${(eNumpyMax*1000).toFixed(4)} mm`);
  return { J, world, skin, ibms, local, jnt, wgt, pos, N };
}
const A = verify('/home/z/my-project/download/batman_s33_full.glb',
  '/home/z/my-project/scripts/jsverify/skinned_s33_full.bin', 'REST (bind-aligned rig)');
const B = verify('/home/z/my-project/download/batman_s33_posed25.glb',
  '/home/z/my-project/scripts/jsverify/skinned_s33_posed25.bin', 'POSED +25deg X on L_Clavicle chain');
// independent pose-change check inside three.js: insert Rx AFTER the
// L_Clavicle local (same construction as the numpy posed25) and re-skin
const ci = A.J.nodes.findIndex(n => n.name === 'Bip01_L_Clavicle');
const Rx = new THREE.Matrix4().makeRotationX(25 * Math.PI / 180);
const worldA = A.J.nodes.map((n, i) => A.world[i].clone());
const localA = A.J.nodes.map((n, i) => A.local[i].clone());
localA[ci].premultiply(Rx.clone().transpose());  // (L_row*Rx_np)^T = Rx_np^T * L^T
const visited2 = new Set();
function walk2(i, parent) {
  if (visited2.has(i)) return; visited2.add(i);
  worldA[i].multiplyMatrices(parent, localA[i]);
  (A.J.nodes[i].children || []).forEach(c => walk2(c, worldA[i]));
}
walk2(0, new THREE.Matrix4());
const sk2 = new Float32Array(A.N * 3);
const v = new THREE.Vector4(), m = new THREE.Matrix4(), acc = new THREE.Matrix4();
for (let i = 0; i < A.N; i++) {
  acc.set(0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0);
  for (let k = 0; k < 4; k++) {
    const w = A.wgt[i*4+k];
    if (w === 0) continue;
    const j = A.jnt[i*4+k];
    m.multiplyMatrices(worldA[A.skin.joints[j]], A.ibms[j]);
    m.multiplyScalar(w);
    for (let q = 0; q < 16; q++) acc.elements[q] += m.elements[q];
  }
  v.set(A.pos[i*3], A.pos[i*3+1], A.pos[i*3+2], 1).applyMatrix4(acc);
  sk2[i*3] = v.x; sk2[i*3+1] = v.y; sk2[i*3+2] = v.z;
}
const expB = fs.readFileSync('/home/z/my-project/scripts/jsverify/skinned_s33_posed25.bin');
const expBF = new Float32Array(expB.buffer, expB.byteOffset, A.N * 3);
let eX = 0, eXMax = 0, moved = 0;
for (let i = 0; i < A.N; i++) {
  const dx = sk2[i*3]-expBF[i*3], dy = sk2[i*3+1]-expBF[i*3+1], dz = sk2[i*3+2]-expBF[i*3+2];
  const e = Math.sqrt(dx*dx+dy*dy+dz*dz);
  eX += e; if (e > eXMax) eXMax = e;
  if (e > 1e-4) moved++;
}
console.log(`\nPOSE-CHANGE cross-check (three.js re-pose vs posed25 numpy): ` +
  `moved ${moved}/${A.N}, mean ${(eX/A.N*100).toFixed(3)} cm, max ${(eXMax*100).toFixed(3)} cm`);
