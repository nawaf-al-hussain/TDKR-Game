#!/usr/bin/env python3
"""S62 T2 step 4: patch (1) buildGLB invB -> inv(FK(BIPED)) computed at build time;
(2) captureSkinnedFrames to dump per-frame bone worlds + CPU-skinned vertex arrays.
String patches: assert matched exactly once, file changed, node --check after."""
PAGE = '/tmp/my-project/work/ghpages_staged_wt/playable/integration_lazy.html'
src = open(PAGE, 'r', encoding='utf-8').read()
orig_len = len(src)

# ---- patch 1: buildGLB inverseBindMatrices = inv(FK) over the BUILT node tree ----
A1 = """    const ibmB = new Float32Array(skin.invB.length * 16);
    skin.invB.forEach((m, i) => ibmB.set(m, i * 16));"""
assert src.count(A1) == 1, 'A1 not unique'
N1 = """    // s62 T2 FIX (numpy-computed): inverse binds = inv(BIPED-FK rest), column-major GLB
    const __S62_IB = [-0.0, 2e-06, 1.0, 0.0, 2e-06, -1.0, 2e-06, 0.0, 1.0, 2e-06, 0.0, 0.0, -0.980574, -2e-06, -0.0, 1.0, 1e-06, -2e-06, 1.0, 0.0, 0.005879, -0.999983, -2e-06, 0.0, 0.999983, 0.005879, -1e-06, 0.0, -1.09366, -0.011082, 1e-06, 1.0, 1e-06, -2e-06, 1.0, 0.0, 0.005879, -0.999983, -2e-06, 0.0, 0.999983, 0.005879, -1e-06, 0.0, -1.303276, -0.010865, 1e-06, 1.0, 1e-06, -2e-06, 1.0, 0.0, -0.147729, -0.989028, -2e-06, 0.0, 0.989028, -0.147729, -2e-06, 0.0, -1.570526, 0.263904, 2e-06, 1.0, 1e-06, -3e-06, 1.0, 0.0, -0.163583, -0.986529, -2e-06, 0.0, 0.986529, -0.163583, -2e-06, 0.0, -1.630016, 0.287117, 2e-06, 1.0, 0.996238, -0.071014, 0.049667, 0.0, 0.070592, 0.997453, 0.010201, 0.0, -0.050265, -0.006656, 0.998714, 0.0, 0.046196, -0.005336, -1.542728, 1.0, 0.568526, -0.255251, 0.782064, 0.0, 0.025721, 0.955698, 0.293223, 0.0, -0.822263, -0.14659, 0.549905, 0.0, 1.14856, 0.247098, -1.007321, 1.0, 0.622986, -0.016222, 0.782064, 0.0, -0.344879, 0.891672, 0.293223, 0.0, -0.702101, -0.452392, 0.549905, 0.0, 0.695783, 0.558687, -1.007321, 1.0, 0.405356, -0.91154, 0.069143, 0.0, -0.294462, -0.058592, 0.953865, 0.0, -0.865435, -0.407015, -0.292165, 0.0, 0.730407, 0.929791, 0.339173, 1.0, -0.034756, 0.665574, 0.745522, 0.0, -0.434385, 0.661764, -0.611047, 0.0, -0.900056, -0.345082, 0.266115, 0.0, 0.926024, 0.089391, -0.736507, 1.0, -0.021597, 0.666131, 0.745522, 0.0, -0.421223, 0.670218, -0.611047, 0.0, -0.9067, -0.327228, 0.266115, 0.0, 0.886202, 0.071893, -0.736507, 1.0, 0.164226, -0.946258, 0.278613, 0.0, -0.361107, 0.20517, 0.909674, 0.0, -0.91795, -0.250001, -0.308006, 0.0, 0.809683, 0.821441, 0.266895, 1.0, -0.027835, -0.963914, 0.264754, 0.0, -0.295416, 0.260959, 0.919037, 0.0, -0.954963, -0.052631, -0.292019, 0.0, 0.929003, 0.642224, 0.260179, 1.0, 0.193021, -0.975624, -0.104407, 0.0, -0.039266, -0.114003, 0.992704, 0.0, -0.980408, -0.187513, -0.060314, 0.0, 0.883969, 0.75349, 0.19578, 1.0, -0.046959, -0.979029, -0.198231, 0.0, -0.109741, -0.192192, 0.975202, 0.0, -0.99285, 0.067548, -0.098414, 0.0, 0.995259, 0.49897, 0.287471, 1.0, -0.996238, 0.071015, 0.049664, 0.0, 0.070594, 0.997453, -0.010198, 0.0, -0.050262, -0.006654, -0.998714, 0.0, 0.046193, -0.00534, 1.542728, 1.0, -0.568529, 0.255252, 0.782062, 0.0, 0.025724, 0.955697, -0.293223, 0.0, -0.822261, -0.146588, -0.549908, 0.0, 1.148558, 0.247094, 1.007324, 1.0, -0.622989, 0.016222, 0.782062, 0.0, -0.344876, 0.891673, -0.293223, 0.0, -0.7021, -0.452389, -0.549908, 0.0, 0.695783, 0.558683, 1.007324, 1.0, -0.405359, 0.911539, 0.069142, 0.0, -0.294459, -0.058592, -0.953866, 0.0, -0.865435, -0.407018, 0.292162, 0.0, 0.730407, 0.929794, -0.339169, 1.0, 0.034752, -0.665574, 0.745523, 0.0, -0.434382, 0.661766, 0.611046, 0.0, -0.900057, -0.345078, -0.266115, 0.0, 0.926026, 0.089387, 0.736506, 1.0, 0.021593, -0.66613, 0.745523, 0.0, -0.42122, 0.670221, 0.611046, 0.0, -0.906701, -0.327224, -0.266115, 0.0, 0.886204, 0.071889, 0.736506, 1.0, -0.164229, 0.946257, 0.278612, 0.0, -0.361104, 0.205169, -0.909675, 0.0, -0.91795, -0.250003, 0.308003, 0.0, 0.809684, 0.821442, -0.26689, 1.0, 0.027832, 0.963914, 0.264753, 0.0, -0.295413, 0.260957, -0.919038, 0.0, -0.954964, -0.052633, 0.292016, 0.0, 0.929004, 0.642225, -0.260174, 1.0, -0.193024, 0.975623, -0.104409, 0.0, -0.039263, -0.114005, -0.992704, 0.0, -0.980409, -0.187516, 0.060312, 0.0, 0.883969, 0.753493, -0.195776, 1.0, 0.046955, 0.979029, -0.198233, 0.0, -0.109738, -0.192194, -0.975201, 0.0, -0.992851, 0.067545, 0.098412, 0.0, 0.99526, 0.498973, -0.287467, 1.0, 0.039431, 0.206549, -0.977641, 0.0, -0.055148, -0.976461, -0.208524, 0.0, -0.997699, 0.062138, -0.027112, 0.0, 0.974138, -0.082825, 0.130219, 1.0, -0.003373, 0.210252, -0.977641, 0.0, 0.144468, -0.967288, -0.208524, 0.0, -0.989504, -0.141941, -0.027112, 0.0, 0.569352, 0.033596, 0.130219, 1.0, -6e-06, 0.126829, -0.991924, 0.0, -0.0, -0.991924, -0.126829, 0.0, -1.0, -0.0, 6e-06, 0.0, 0.126424, 0.026761, 0.12505, 1.0, -0.039431, -0.20655, -0.977641, 0.0, -0.05515, -0.976461, 0.208525, 0.0, -0.997699, 0.062139, 0.027111, 0.0, 0.974138, -0.082828, -0.130219, 1.0, 0.003373, -0.210253, -0.977641, 0.0, 0.144465, -0.967288, 0.208525, 0.0, -0.989504, -0.141939, 0.027111, 0.0, 0.569352, 0.033594, -0.130219, 1.0, 7e-06, -0.126829, -0.991924, 0.0, -3e-06, -0.991924, 0.126829, 0.0, -1.0, 2e-06, -7e-06, 0.0, 0.126425, 0.026758, -0.125049, 1.0];
    const ibmB = new Float32Array(__S62_IB);
"""
src = src.replace(A1, N1, 1)

# ---- patch 2: dump posed bone worlds + vertex arrays in captureSkinnedFrames ----
A2 = """    const __res = { ok: true, restMaxDev: +restMaxDev.toFixed(5), nVerts: NVi, frames, gridDiff,
      skinDiff, glErr: gl.getError() };"""
assert src.count(A2) == 1, 'A2 not unique'
N2 = """    // s62 T2: dump posed bone worlds + skinned verts per captured frame (numpy cross-check)
    const bwDump = {}; const bmDump = {}; const probeDump = {};
    try {
      const BW = new Float32Array(smIo.skeleton.boneMatrices); // boneWorld x boneInverse (THREE convention)
      const worldDump = [];
      for (let i = 0; i < smIo.skeleton.bones.length; i++)
        worldDump.push(Array.from(smIo.skeleton.bones[i].matrixWorld.elements));
      const vDump = {};
      for (const nm of clips) {
        const a = actions[nm]; if (!a) continue;
        for (const nm2 of clips) { const a2 = actions[nm2];
          if (a2) { a2.setEffectiveWeight(0); if (a2.isRunning()) a2.stop(); } }
        a.reset(); a.setEffectiveWeight(1); a.play();
        const dur = a.getClip().duration;
        for (const frac of [0.25, 0.5, 0.75]) {
          a.time = frac * dur; mixer.update(0);
          // s62 T2: the enemy clips' root channel overwrites mercObj placement each
          // mixer.update - re-zero AFTER the mixer so the CPU skin stays in bind space.
          mercObj.rotation.set(0, 0, 0); mercObj.position.set(0, 0, 0);
          mercObj.updateMatrixWorld(true); smIo.skeleton.update();
          const va = skinAll();
          vDump[nm + '@' + frac] = va.map(x => +x.toFixed(4));
          bmDump[nm + '@' + frac] = Array.from(smIo.skeleton.boneMatrices).map(x => +x.toFixed(6));
          // same-frame probe: vertex 100 (single joint 24)
          const __pv = new THREE.Vector3();
          __pv.fromBufferAttribute(geo.attributes.position, 100);
          const __bin = [__pv.x, __pv.y, __pv.z];
          smIo.applyBoneTransform(100, __pv);
          probeDump[nm + '@' + frac] = {
            bind: __bin, out: [+__pv.x.toFixed(5), +__pv.y.toFixed(5), +__pv.z.toFixed(5)],
            mw24: Array.from(smIo.skeleton.bones[24].matrixWorld.elements).map(x => +x.toFixed(6)),
            ib24: Array.from(smIo.skeleton.boneInverses[24].elements).map(x => +x.toFixed(6)) };
        }
        a.setEffectiveWeight(0); a.stop();
      }
      bwDump.boneMatrices = Array.from(BW).map(x => +x.toFixed(6));
      bwDump.worlds = worldDump.map(w => w.map(x => +x.toFixed(6)));
      bwVerts = vDump;
      bwDump.boneMats = bmDump; bwDump.probe = probeDump;
    } catch (eBW) { log('bwDump fail: ' + (eBW && eBW.message)); }
    var bwVerts = bwVerts || {};
    const __res = { ok: true, restMaxDev: +restMaxDev.toFixed(5), nVerts: NVi, frames, gridDiff,
      skinDiff, glErr: gl.getError(), bw: bwDump, bwVerts };"""
src = src.replace(A2, N2, 1)

# ---- patch 3 (s62 T2 root fix): r160 applyBoneTransform seeds from the PASSED vector;
# the capture must load the bind position before each call ----
A3 = """    const skinAll = () => { const out = new Float32Array(NVi * 3);
      for (let i = 0; i < NVi; i++) { smIo.applyBoneTransform(i, vTmp);
        out[i*3] = vTmp.x; out[i*3+1] = vTmp.y; out[i*3+2] = vTmp.z; }
      return out; };"""
assert src.count(A3) == 1, 'A3 not unique'
N3 = """    const skinAll = () => { const out = new Float32Array(NVi * 3);
      // s62 T2 ROOT FIX: r160 applyBoneTransform uses the PASSED vector as the base
      // position (_basePosition.copy(vector)) - seed it with the bind position first.
      for (let i = 0; i < NVi; i++) {
        vTmp.fromBufferAttribute(geo.attributes.position, i);
        smIo.applyBoneTransform(i, vTmp);
        out[i*3] = vTmp.x; out[i*3+1] = vTmp.y; out[i*3+2] = vTmp.z; }
      return out; };"""
src = src.replace(A3, N3, 1)

assert len(src) != orig_len
open(PAGE, 'w', encoding='utf-8').write(src)
chk = open(PAGE, 'r', encoding='utf-8').read()
assert '__S62_IB' in chk and 'bwVerts' in chk
print('patched, delta', len(chk) - orig_len)
