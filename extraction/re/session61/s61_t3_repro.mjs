// s61 T3 minimal repro (v2): one-bone skinning in THREE r160.
// Root-cause hunt for s60's "applyBoneTransform returns zeros / skeleton.pose() corrupts".
import * as THREE from 'three';

function mat4str(v) {
  return `[${[v.x, v.y, v.z].map(x => +x.toFixed(4)).join(' ')}]`;
}

function mkgeom() {
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute([0, 1, 0], 3));
  g.setAttribute('skinIndex', new THREE.Uint16BufferAttribute([0], 1));
  g.setAttribute('skinWeight', new THREE.Float32BufferAttribute([1.0], 1));
  return g;
}
const invB = new THREE.Matrix4(); // bind pose = identity
const expected = [-1, 0, 0];      // rotZ(90) maps (0,1,0) -> (-1,0,0)

// CASE A: pose set, but NO updateMatrixWorld / skeleton.update before applyBoneTransform
try {
  const mesh = new THREE.SkinnedMesh(mkgeom(), new THREE.MeshBasicMaterial());
  const bone = new THREE.Bone();
  bone.rotation.set(0, 0, Math.PI / 2);
  mesh.add(bone);
  mesh.bind(new THREE.Skeleton([bone], [invB.clone()]));
  const v = new THREE.Vector3(0, 1, 0);
  mesh.applyBoneTransform(0, v);
  const zero = mesh.skeleton.boneMatrices.every(x => x === 0);
  console.log('A (no update):   ', mat4str(v), 'boneMatricesAllZero=', zero, 'expected', expected);
} catch (e) {
  console.log('A threw:', e.message);
}

// CASE B: updateMatrixWorld(true) + skeleton.update() first
try {
  const mesh = new THREE.SkinnedMesh(mkgeom(), new THREE.MeshBasicMaterial());
  const bone = new THREE.Bone();
  bone.rotation.set(0, 0, Math.PI / 2);
  mesh.add(bone);
  mesh.bind(new THREE.Skeleton([bone], [invB.clone()]));
  mesh.updateMatrixWorld(true);
  mesh.skeleton.update();
  const v = new THREE.Vector3(0, 1, 0);
  mesh.applyBoneTransform(0, v);
  console.log('B (update+skel): ', mat4str(v), 'expected', expected);
} catch (e) {
  console.log('B threw:', e.message);
}

// CASE C: manual CPU recipe - boneMat = bone.matrixWorld * boneInverses[i]
try {
  const mesh = new THREE.SkinnedMesh(mkgeom(), new THREE.MeshBasicMaterial());
  const bone = new THREE.Bone();
  bone.rotation.set(0, 0, Math.PI / 2);
  mesh.add(bone);
  mesh.updateMatrixWorld(true);
  const m = new THREE.Matrix4().multiplyMatrices(bone.matrixWorld, invB);
  const v = new THREE.Vector3(0, 1, 0).applyMatrix4(m);
  console.log('C (manual):      ', mat4str(v), 'expected', expected);
} catch (e) {
  console.log('C threw:', e.message);
}

// CASE D: skeleton.pose() AFTER bind with file inverses (the s60 "corrupts state" claim)
try {
  const mesh = new THREE.SkinnedMesh(mkgeom(), new THREE.MeshBasicMaterial());
  const bone = new THREE.Bone();
  bone.rotation.set(0, 0, Math.PI / 2);
  mesh.add(bone);
  const skel = new THREE.Skeleton([bone], [invB.clone()]);
  mesh.bind(skel);
  const before = bone.rotation.z;
  skel.pose(); // copies bone.rest? in r160: pose() sets bones to skeleton.boneInverses^-1
  mesh.updateMatrixWorld(true);
  skel.update();
  const v = new THREE.Vector3(0, 1, 0);
  mesh.applyBoneTransform(0, v);
  console.log('D (after pose()):', mat4str(v), 'rotZ before', before.toFixed(3), 'after', bone.rotation.z.toFixed(3), '(pose() OVERWROTE the clip pose)');
} catch (e) {
  console.log('D threw:', e.message);
}
