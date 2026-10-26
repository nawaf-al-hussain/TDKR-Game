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
N1 = """    // s62 T2 FIX: file invB convention != BIPED-FK frame (restMaxDev 1.87 root cause).
    // Compute inverse binds from the BUILT node tree (BIPED parents + file TRS) so that
    // boneWorld x invB = I at rest exactly. Vertices are in the same bind space.
    const __q2m = (q) => { const [x, y, z, w] = q;
      return [1-2*(y*y+z*z), 2*(x*y+z*w), 2*(x*z-y*w), 0,
              2*(x*y-z*w), 1-2*(x*x+z*z), 2*(y*z+x*w), 0,
              2*(x*z+y*w), 2*(y*z-x*w), 1-2*(x*x+y*y), 0, 0, 0, 0, 1]; };
    const __wmat = {};
    const __fw = (nm) => { if (__wmat[nm]) return __wmat[nm];
      const nd = skin.nodes.find(x => x.name === nm);
      const L = new Float32Array(16);
      { const m = __q2m(nd.q);
        for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) L[r*4+c] = m[r*4+c] * nd.s[c];
        L[12] = nd.t[0]; L[13] = nd.t[1]; L[14] = nd.t[2]; L[15] = 1; }
      const pr = parentOf(nm);
      let W2 = L;
      if (pr && nodeOf[pr] !== undefined) {
        const P = __fw(pr), O = new Float32Array(16);
        for (let r = 0; r < 4; r++) for (let c = 0; c < 4; c++) {
          let s3 = 0; for (let k = 0; k < 4; k++) s3 += P[r*4+k] * L[k*4+c];
          O[r*4+c] = s3; }
        W2 = O; }
      __wmat[nm] = W2; return W2; };
    const ibmB = new Float32Array(skin.invB.length * 16);
    skin.jointNodes.forEach((nm, i) => {
      const W2 = __fw(nm);
      // invert 4x4 (general, column-major storage as THREE expects via GLB: GLB ibm is
      // column-major; our W2 is row-major math -> store TRANSPOSE(W2)^-1 = column-major inv)
      const m = W2, im = new Float32Array(16);
      const a00=m[0],a01=m[1],a02=m[2],a03=m[3],a10=m[4],a11=m[5],a12=m[6],a13=m[7],
            a20=m[8],a21=m[9],a22=m[10],a23=m[11],a30=m[12],a31=m[13],a32=m[14],a33=m[15];
      const b00=a00*a11-a01*a10, b01=a00*a12-a02*a10, b02=a00*a13-a03*a10,
            b03=a01*a12-a02*a11, b04=a01*a13-a03*a11, b05=a02*a13-a03*a12,
            b06=a20*a31-a21*a30, b07=a20*a32-a22*a30, b08=a20*a33-a23*a30,
            b09=a21*a32-a22*a31, b10=a21*a33-a23*a31, b11=a22*a33-a23*a32;
      let det = b00*b11 - b01*b10 + b02*b09 + b03*b08 - b04*b07 + b05*b06;
      det = 1.0 / det;
      im[0]=(a11*b11-a12*b10+a13*b09)*det; im[1]=(a02*b10-a01*b11-a03*b09)*det;
      im[2]=(a31*b05-a32*b04+a33*b03)*det; im[3]=(a22*b04-a21*b05-a23*b03)*det;
      im[4]=(a12*b08-a10*b11-a13*b07)*det; im[5]=(a00*b11-a02*b08+a03*b07)*det;
      im[6]=(a32*b02-a30*b05-a33*b01)*det; im[7]=(a20*b05-a22*b02+a23*b01)*det;
      im[8]=(a10*b10-a11*b08+a13*b06)*det; im[9]=(a01*b08-a00*b10-a03*b06)*det;
      im[10]=(a30*b04-a31*b02+a33*b00)*det; im[11]=(a21*b02-a20*b04-a23*b00)*det;
      im[12]=(a11*b07-a10*b09-a12*b06)*det; im[13]=(a00*b09-a01*b07+a02*b06)*det;
      im[14]=(a31*b01-a30*b03-a32*b00)*det; im[15]=(a20*b03-a21*b01+a22*b00)*det;
      // GLB ibm is COLUMN-major; im is row-major -> transpose on write
      for (let r = 0; r < 4; r++) for (let c = 0; c < 4; c++) ibmB[i*16 + c*4 + r] = im[r*4+c];
    });"""
src = src.replace(A1, N1, 1)

# ---- patch 2: dump posed bone worlds + vertex arrays in captureSkinnedFrames ----
A2 = """    const __res = { ok: true, restMaxDev: +restMaxDev.toFixed(5), nVerts: NVi, frames, gridDiff,
      skinDiff, glErr: gl.getError() };"""
assert src.count(A2) == 1, 'A2 not unique'
N2 = """    // s62 T2: dump posed bone worlds + skinned verts per captured frame (numpy cross-check)
    const bwDump = {};
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
        a.time = 0.25 * dur; mixer.update(0);
        mercObj.updateMatrixWorld(true); smIo.skeleton.update();
        vDump[nm] = Array.from(skinAll()).map(x => +x.toFixed(4));
        a.setEffectiveWeight(0); a.stop();
      }
      bwDump.boneMatrices = Array.from(BW).map(x => +x.toFixed(6));
      bwDump.worlds = worldDump.map(w => w.map(x => +x.toFixed(6)));
      bwVerts = vDump;
    } catch (eBW) { log('bwDump fail: ' + (eBW && eBW.message)); }
    var bwVerts = bwVerts || {};
    const __res = { ok: true, restMaxDev: +restMaxDev.toFixed(5), nVerts: NVi, frames, gridDiff,
      skinDiff, glErr: gl.getError(), bw: bwDump, bwVerts };"""
src = src.replace(A2, N2, 1)

assert len(src) != orig_len
open(PAGE, 'w', encoding='utf-8').write(src)
chk = open(PAGE, 'r', encoding='utf-8').read()
assert '__fw' in chk and 'bwVerts' in chk
print('patched, delta', len(chk) - orig_len)
