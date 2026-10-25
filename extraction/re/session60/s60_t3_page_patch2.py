#!/usr/bin/env python3
"""s60 T3 page patch v2: move rest-pose IoU capture to loadMerc (pre-animation),
widen one-shot windows, robust finished thresholds."""
P = '/tmp/my-project/work/ghpages_staged_wt/playable/integration_lazy.html'
src = open(P, encoding='utf-8').read()

def rep(old, new, tag, n=1):
    global src
    c = src.count(old)
    assert c == n, 'PATCH %s: %d matches (want %d)' % (tag, c, n)
    src = src.replace(old, new)
    print('patched', tag)

# A) widen windows + report time
rep("  const phase = t < 4 ? 0 : (t < 8 ? 1 : (t < 12 ? 2 : (t < 13 ? 3 : 4)));",
    "  const phase = t < 4 ? 0 : (t < 8 ? 1 : (t < 12 ? 2 : (t < 14 ? 3 : 4)));", 'PHASES2')
rep("  if (t > 18 && !mercSeq.reported && mercSkinProbe) {",
    "  if (t > 20 && !mercSeq.reported && mercSkinProbe) {", 'REPORT-T2')

# B) robust finished thresholds + report raw times
rep("""    const hurtDone = hurtT >= hurtDur - 1e-3;
    const deathDone = deathT >= deathDur - 1e-3;""",
    """    const hurtDone = hurtT >= hurtDur * 0.95;
    const deathDone = deathT >= deathDur * 0.95;""", 'FINISHED')
rep("""      hurtDur: +hurtDur.toFixed(3), deathDur: +deathDur.toFixed(3),
      hurtDone, deathDone, dispCtlWrongClip: dispCtl,""",
    """      hurtDur: +hurtDur.toFixed(3), deathDur: +deathDur.toFixed(3),
      hurtT: +hurtT.toFixed(3), deathT: +deathT.toFixed(3),
      hurtDone, deathDone, dispCtlWrongClip: dispCtl,""", 'GATE3')

# C) cut the IoU block from the report; reference the stored capture
i0 = src.index("    // ---- s60 T3: REST-POSE silhouette capture (raw WebGL1 + readPixels) ----")
i1 = src.index("    if (window.__GATE.pendingFinalize && !window.__GATE.done) {")
block = src[i0:i1]
assert 'enemyIoU' in block and block.count('try {') == 1
src = src[:i0] + "    window.__GATE.enemyIoU = mercSeq.restIoU || { ok: false, error: 'rest capture missing' };\n" + src[i1:]
print('moved IoU block out of report')

# D) insert the capture function before loadMerc + call it in loadMerc after mercSeq init
capfn = """
// s60 T3: rest-pose silhouette capture (raw WebGL1 + readPixels) - runs BEFORE any
// animation so the CPU-skin at rest == bind vertices (bindMaxDev ~ 0 expected).
function captureRestIoU(smIo) {
  try {
    const geo = smIo.geometry;
    const posA = geo.attributes.position;
    const NVi = posA.count;
    const vAll = new Float32Array(NVi * 3);
    const vTmp = new THREE.Vector3();
    for (let i = 0; i < NVi; i++) { smIo.applyBoneTransform(i, vTmp); vAll[i*3] = vTmp.x; vAll[i*3+1] = vTmp.y; vAll[i*3+2] = vTmp.z; }
    const ia = geo.index.array, IN = geo.index.count;
    const SZ = 256, GRID = 64;
    const cv = document.createElement('canvas'); cv.width = SZ; cv.height = SZ;
    const gl = cv.getContext('webgl', { preserveDrawingBuffer: true });
    let mnx = 1e9, mxx = -1e9, mnz = 1e9, mxz = -1e9;
    for (let i = 0; i < NVi; i++) { mnx = Math.min(mnx, vAll[i*3]); mxx = Math.max(mxx, vAll[i*3]); mnz = Math.min(mnz, vAll[i*3+2]); mxz = Math.max(mxz, vAll[i*3+2]); }
    const sx = 2.0 / Math.max(1e-6, mxx - mnx), sz2 = 2.0 / Math.max(1e-6, mxz - mnz);
    const sc = Math.min(sx, sz2) * 0.9;
    const cx = (mnx + mxx) / 2, cz = (mnz + mxz) / 2;
    const xy = new Float32Array(NVi * 2);
    for (let i = 0; i < NVi; i++) { xy[i*2] = (vAll[i*3] - cx) * sc; xy[i*2+1] = (vAll[i*3+2] - cz) * sc; }
    const vb = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, vb); gl.bufferData(gl.ARRAY_BUFFER, xy, gl.STATIC_DRAW);
    const ib = gl.createBuffer(); gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ib); gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, ia, gl.STATIC_DRAW);
    const prog = gl.createProgram();
    const sh = (t, s) => { const o = gl.createShader(t); gl.shaderSource(o, s); gl.compileShader(o); return o; };
    gl.attachShader(prog, sh(gl.VERTEX_SHADER, 'attribute vec2 q; void main(){ gl_Position = vec4(q, 0.0, 1.0); }'));
    gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, 'void main(){ gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0); }'));
    gl.linkProgram(prog); gl.useProgram(prog);
    const loc = gl.getAttribLocation(prog, 'q');
    gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    gl.viewport(0, 0, SZ, SZ); gl.clearColor(0, 0, 0, 1); gl.clear(gl.COLOR_BUFFER_BIT);
    gl.drawElements(gl.TRIANGLES, IN, gl.UNSIGNED_SHORT, 0);
    const px = new Uint8Array(SZ * SZ * 4);
    gl.readPixels(0, 0, SZ, SZ, gl.RGBA, gl.UNSIGNED_BYTE, px);
    let hex = '';
    for (let gy = 0; gy < GRID; gy++) for (let gx = 0; gx < GRID / 8; gx++) {
      let b = 0;
      for (let gy2 = 0; gy2 < 4; gy2++) for (let gx2 = 0; gx2 < 8; gx2++) {
        const X = gx * 8 + gx2, Y = gy * 4 + gy2;
        const o = ((GRID - 1 - Y) * SZ + X) * 4;
        if (px[o] > 32) b |= 1 << (gy2 * 8 + gx2);
      }
      hex += ('0000000' + (b >>> 0).toString(16)).slice(-8);   // 32 bits per group, unsigned
    }
    let bindDev = 0;
    const pa = posA.array;
    for (let i = 0; i < NVi * 3; i++) bindDev = Math.max(bindDev, Math.abs(vAll[i] - pa[i]));
    const res = { ok: true, gridHex: hex, grid: GRID, SZ,
      meshMin: [+mnx.toFixed(4), +mnz.toFixed(4)], meshMax: [+mxx.toFixed(4), +mxz.toFixed(4)],
      height: +(mxz - mnz).toFixed(4), feetZ: +mnz.toFixed(4),
      bindMaxDev: +bindDev.toFixed(6), nVerts: NVi, nIdx: IN };
    log('enemyIoU: height=' + (mxz - mnz).toFixed(3) + ' feetZ=' + mnz.toFixed(3) + ' bindDev=' + bindDev.toFixed(5));
    return res;
  } catch (e4) {
    log('enemyIoU FAILED: ' + (e4 && e4.message || e4));
    return { ok: false, error: String(e4 && e4.message || e4) };
  }
}
"""
rep("async function loadMerc(zipBuf, findM) {",
    capfn + "async function loadMerc(zipBuf, findM) {", 'CAPFN')
rep("""  mercSeq = { t0: performance.now(), phase: 0, wraps: 0, zmin: 1e9, zmax: -1e9, lastT: 0 };""",
    """  mercSeq = { t0: performance.now(), phase: 0, wraps: 0, zmin: 1e9, zmax: -1e9, lastT: 0 };
  { // s60 T3: capture the rest pose BEFORE any animation runs
    const smR = (() => { let s = null; merc.traverse(o => { if (o.isSkinnedMesh) s = o; }); return s; })();
    if (smR) mercSeq.restIoU = captureRestIoU(smR);
    else mercSeq.restIoU = { ok: false, error: 'no skinned mesh' };
  }""", 'CAPCALL')

open(P, 'w', encoding='utf-8').write(src)
print('done, len', len(src))
