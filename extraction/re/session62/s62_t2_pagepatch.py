#!/usr/bin/env python3
"""S62 T2 step 1: patch captureBindBisect() into the staged worktree page.
Bisection dumps (task spec):
 (a) per-bone: skeleton.boneInverses[i] (16 floats) + bone.matrixWorld (16) at bind
 (b) GLB node TRS per bone node + mesh node transform + skin.skeleton root name
 (c) skinIndex/skinWeight itemSize + per-vertex weight sums (loaded geometry)
 (d) one-vertex identity test: known bind-pose vertex through identity skinning
String patch: assert matched exactly once, file changed. Byte-verified."""
import sys

PAGE = '/tmp/my-project/work/ghpages_staged_wt/playable/integration_lazy.html'
src = open(PAGE, 'r', encoding='utf-8').read()

ANCHOR = "      window.__GATE.enemyIoU2 = captureSkinnedFrames(smI2, merc, mercMixer, mercActions, ENEMY_CLIPS);"
assert src.count(ANCHOR) == 1, 'anchor not unique'

INJECT = '''      window.__GATE.enemyIoU2 = captureSkinnedFrames(smI2, merc, mercMixer, mercActions, ENEMY_CLIPS);
      try { window.__GATE.bindBisect = captureBindBisect(smI2, merc); } catch (eBB) {
        window.__GATE.bindBisect = { ok: false, error: String(eBB && eBB.message || eBB) }; }'''

FN = '''
  function captureBindBisect(smIo, mercObj) {
    // S62 T2: rest/bind convention gap bisection (task spec a-d)
    const out = { ok: true };
    const skel = smIo.skeleton;
    const NB = skel.bones.length;
    // (a) per-bone boneInverses + bone.matrixWorld (bind/rest pose, mesh transform zeroed)
    const keepR = mercObj.rotation.x, keepP = mercObj.position.clone(), keepS = mercObj.scale.clone();
    mercObj.rotation.set(0, 0, 0); mercObj.position.set(0, 0, 0); mercObj.scale.set(1, 1, 1);
    mercObj.updateMatrixWorld(true); skel.update();
    out.scaleWas = { x: keepS.x, y: keepS.y, z: keepS.z };
    out.rotWas = keepR;
    const inv = [], mw = [], bn = [];
    for (let i = 0; i < NB; i++) {
      inv.push(Array.from(skel.boneInverses[i].elements));
      mw.push(Array.from(skel.bones[i].matrixWorld.elements));
      bn.push(skel.bones[i].name || ('bone' + i));
    }
    out.boneNames = bn;
    out.boneInverses = inv;
    out.boneMatrixWorld = mw;
    // bindMatrix / bindMatrixInverse
    out.bindMatrix = Array.from(smIo.bindMatrix.elements);
    out.bindMatrixInverse = Array.from(smIo.bindMatrixInverse.elements);
    // (b) node TRS as the loader parsed them (same values the GLB carried)
    out.nodeTRS = skel.bones.map(b => ({
      name: b.name || ('bone' + bn.indexOf(b)),
      pos: [b.position.x, b.position.y, b.position.z],
      quat: [b.quaternion.x, b.quaternion.y, b.quaternion.z, b.quaternion.w],
      scl: [b.scale.x, b.scale.y, b.scale.z] }));
    out.meshNode = { pos: [mercObj.position.x, mercObj.position.y, mercObj.position.z],
      quat: [mercObj.quaternion.x, mercObj.quaternion.y, mercObj.quaternion.z, mercObj.quaternion.w],
      scl: [mercObj.scale.x, mercObj.scale.y, mercObj.scale.z] };
    out.skelRoot = skel.bones[0] ? skel.bones[0].name : null;
    // (c) skin attributes as LOADED
    const g = smIo.geometry;
    const si = g.attributes.skinIndex, sw = g.attributes.skinWeight;
    out.skinAttrs = { skinIndex: si ? { itemSize: si.itemSize, count: si.count,
      arrayType: si.array.constructor.name } : null,
      skinWeight: sw ? { itemSize: sw.itemSize, count: sw.count,
        arrayType: sw.array.constructor.name } : null };
    if (sw) {
      let bad = 0, maxDev = 0;
      for (let i = 0; i < sw.count; i++) {
        let s2 = 0;
        for (let k = 0; k < 4; k++) s2 += sw.getComponent(i, k);
        const d = Math.abs(s2 - 1);
        if (d > 1e-3) bad++;
        if (d > maxDev) maxDev = d;
      }
      out.weightSums = { bad: bad, maxDev: +maxDev.toFixed(6), count: sw.count };
    }
    // (d) one-vertex identity test: skin vertex 0 with identity boneMatrices
    const v0 = new THREE.Vector3();
    g.attributes.position.getX(0); // touch
    const px0 = g.attributes.position.getX(0), py0 = g.attributes.position.getY(0),
          pz0 = g.attributes.position.getZ(0);
    // identity skin: set every boneMatrix = I (save first)
    const saved = new Float32Array(skel.boneMatrices);
    for (let i = 0; i < NB * 16; i++) skel.boneMatrices[i] = 0;
    for (let i = 0; i < NB; i++) {
      skel.boneMatrices[i*16+0] = 1; skel.boneMatrices[i*16+5] = 1;
      skel.boneMatrices[i*16+10] = 1; skel.boneMatrices[i*16+15] = 1;
    }
    smIo.applyBoneTransform(0, v0);
    out.oneVertexIdentity = { in: [px0, py0, pz0], out: [v0.x, v0.y, v0.z],
      maxDev: +Math.max(Math.abs(v0.x - px0), Math.abs(v0.y - py0), Math.abs(v0.z - pz0)).toFixed(6) };
    // s62 T2: non-degenerate vertex probes through the REAL rest chain
    out.vertexRest = [];
    for (const idx of [1, 100, 500, 900, 1200]) {
      const v1 = new THREE.Vector3();
      v1.fromBufferAttribute(g.attributes.position, idx);  // s62: r160 seeds from the PASSED vector
      smIo.applyBoneTransform(idx, v1);
      out.vertexRest.push({ idx,
        bind: [g.attributes.position.getX(idx), g.attributes.position.getY(idx), g.attributes.position.getZ(idx)],
        rest: [+v1.x.toFixed(4), +v1.y.toFixed(4), +v1.z.toFixed(4)] });
    }
    out.inv1 = Array.from(skel.boneInverses[1].elements).map(x => +x.toFixed(6));
    // restore
    skel.boneMatrices.set(saved);
    mercObj.rotation.x = keepR; mercObj.position.copy(keepP); mercObj.scale.copy(keepS);
    mercObj.updateMatrixWorld(true); skel.update();
    return out;
  }
'''

src2 = src.replace(ANCHOR, INJECT, 1)
# insert the function before captureSkinnedFrames definition (top-level, no indent)
MARK = 'function captureSkinnedFrames(smIo, mercObj, mixer, actions, clips) {'
assert src2.count(MARK) == 1, 'fn mark not unique'
FN = FN.replace('  function captureBindBisect', 'function captureBindBisect')
src2 = src2.replace(MARK, FN + '\n' + MARK, 1)
assert src2 != src
open(PAGE, 'w', encoding='utf-8').write(src2)

# byte-verify
chk = open(PAGE, 'r', encoding='utf-8').read()
assert 'captureBindBisect' in chk and chk.count('captureBindBisect') == 2
assert ANCHOR not in chk or INJECT.split('\n')[0] in chk
print('patched OK; length delta:', len(chk) - len(src))
