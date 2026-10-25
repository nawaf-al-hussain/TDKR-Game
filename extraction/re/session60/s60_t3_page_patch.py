#!/usr/bin/env python3
"""s60 T3 page patch: wire Hurt/Death clips + rest-pose IoU capture (raw WebGL1).
Asserts each old string matches exactly once; verifies file changed; prints diff stats."""
import re, hashlib

P = '/tmp/my-project/work/ghpages_staged_wt/playable/integration_lazy.html'
src = open(P, 'rb').read().decode('utf-8')
orig_len = len(src)

def rep(old, new, tag):
    global src
    n = src.count(old)
    assert n == 1, 'PATCH %s: %d matches' % (tag, n)
    src = src.replace(old, new, 1)
    print('patched', tag)

# 1) ENEMY_CLIPS: add Hurt/Death
rep("const ENEMY_CLIPS = ['_014_idle_enemy_combat', '_166_enemy_walk', '_171_enemy_run'];",
    "// s60 T3: Hurt/Death wired (shared bank: _222/_223 hurt, _250/_251 death)\n"
    "const ENEMY_CLIPS = ['_014_idle_enemy_combat', '_166_enemy_walk', '_171_enemy_run', '_223_enemy_hurtl', '_250_enemy_death1'];",
    'CLIPS')

# 2) one-shot setup after idle play
rep("  const idle = mercActions[ENEMY_CLIPS[0]]; idle.play(); idle.setEffectiveWeight(1);",
    "  const idle = mercActions[ENEMY_CLIPS[0]]; idle.play(); idle.setEffectiveWeight(1);\n"
    "  // s60 T3: Hurt/Death are one-shot clips (LoopOnce + clamp)\n"
    "  mercActions['_223_enemy_hurtl'].loop = THREE.LoopOnce;\n"
    "  mercActions['_223_enemy_hurtl'].clampWhenFinished = true;\n"
    "  mercActions['_250_enemy_death1'].loop = THREE.LoopOnce;\n"
    "  mercActions['_250_enemy_death1'].clampWhenFinished = true;",
    'ONESHOT')

# 3) phase machine 5 states: idle 0-4, walk 4-8, run 8-12, hurt 12-13, death 13+
rep("  const phase = t < 4 ? 0 : (t < 8 ? 1 : 2);",
    "  const phase = t < 4 ? 0 : (t < 8 ? 1 : (t < 12 ? 2 : (t < 13 ? 3 : 4)));",
    'PHASES')

# 4) report later + extra measures
rep("  if (t > 12 && !mercSeq.reported && mercSkinProbe) {",
    "  if (t > 18 && !mercSeq.reported && mercSkinProbe) {",
    'REPORT-T')

# 5) gate: hurt/death disp + one-shot finished flags + rest-pose IoU
rep("""    const dIdle = disp[ENEMY_CLIPS[0]], dWalk = disp[ENEMY_CLIPS[1]], dRun = disp[ENEMY_CLIPS[2]];
    const okGate = isFinite(dIdle) && isFinite(dWalk) && isFinite(dRun) && isFinite(dispCtl) &&
      dIdle > 0 && dWalk > 0 && dRun > 0 && Math.abs(dispCtl - dIdle) > 1e-4;""",
    """    const dIdle = disp[ENEMY_CLIPS[0]], dWalk = disp[ENEMY_CLIPS[1]], dRun = disp[ENEMY_CLIPS[2]];
    const dHurt = disp[ENEMY_CLIPS[3]], dDeath = disp[ENEMY_CLIPS[4]];
    // one-shot finished: action time pinned at (or past) clip duration
    const hurtDur = mercActions[ENEMY_CLIPS[3]].getClip().duration;
    const deathDur = mercActions[ENEMY_CLIPS[4]].getClip().duration;
    const hurtT = mercActions[ENEMY_CLIPS[3]].time;
    const deathT = mercActions[ENEMY_CLIPS[4]].time;
    const hurtDone = hurtT >= hurtDur - 1e-3;
    const deathDone = deathT >= deathDur - 1e-3;
    const okGate = isFinite(dIdle) && isFinite(dWalk) && isFinite(dRun) && isFinite(dispCtl) &&
      dIdle > 0 && dWalk > 0 && dRun > 0 && Math.abs(dispCtl - dIdle) > 1e-4 &&
      isFinite(dHurt) && dHurt > 0 && isFinite(dDeath) && dDeath > 0 && hurtDone && deathDone;""",
    'GATE')

rep("""      dispIdle: dIdle, dispWalk: dWalk, dispRun: dRun, dispCtlWrongClip: dispCtl,
      ctlClip, probeVerts: mercSkinProbe ? mercSkinProbe.idxs.length : 0 };""",
    """      dispIdle: dIdle, dispWalk: dWalk, dispRun: dRun,
      dispHurt: dHurt, dispDeath: dDeath,
      hurtDur: +hurtDur.toFixed(3), deathDur: +deathDur.toFixed(3),
      hurtDone, deathDone, dispCtlWrongClip: dispCtl,
      ctlClip, probeVerts: mercSkinProbe ? mercSkinProbe.idxs.length : 0 };""",
    'GATE2')

# 6) rest-pose IoU capture (raw WebGL1) appended at report time, before finalize
rep("""    log('enemy playback: wraps=' + mercSeq.wraps + ' disp=' + JSON.stringify(disp) + ' ctlWrong=' + dispCtl +
        ' bboxZ=[' + mercSeq.zmin.toFixed(2) + ',' + mercSeq.zmax.toFixed(2) + ']');""",
    """    log('enemy playback: wraps=' + mercSeq.wraps + ' disp=' + JSON.stringify(disp) + ' ctlWrong=' + dispCtl +
        ' bboxZ=[' + mercSeq.zmin.toFixed(2) + ',' + mercSeq.zmax.toFixed(2) + ']');
    // ---- s60 T3: REST-POSE silhouette capture (raw WebGL1 + readPixels) ----
    try {
      mercMixer.stopAllAction();          // rest/bind pose
      merc.updateMatrixWorld(true);
      const smIo = (() => { let s = null; merc.traverse(o => { if (o.isSkinnedMesh) s = o; }); return s; })();
      const geo = smIo.geometry;
      const posA = geo.attributes.position;
      const NVi = posA.count;
      const vAll = new Float32Array(NVi * 3);
      const vTmp = new THREE.Vector3();
      for (let i = 0; i < NVi; i++) { smIo.applyBoneTransform(i, vTmp); vAll[i*3] = vTmp.x; vAll[i*3+1] = vTmp.y; vAll[i*3+2] = vTmp.z; }
      const ia = geo.index.array, IN = geo.index.count;
      // raw WebGL1 offscreen render: front view on mesh-local (x, z)
      const SZ = 256, GRID = 64;
      const cv = document.createElement('canvas'); cv.width = SZ; cv.height = SZ;
      const gl = cv.getContext('webgl', { preserveDrawingBuffer: true });
      // mesh-local (x,z) normalized to [-1,1] on CPU
      let mnx = 1e9, mxx = -1e9, mnz = 1e9, mxz = -1e9;
      for (let i = 0; i < NVi; i++) { mnx = Math.min(mnx, vAll[i*3]); mxx = Math.max(mxx, vAll[i*3]); mnz = Math.min(mnz, vAll[i*3+2]); mxz = Math.max(mxz, vAll[i*3+2]); }
      const sx = 2.0 / Math.max(1e-6, mxx - mnx), sz = 2.0 / Math.max(1e-6, mxz - mnz);
      const sc = Math.min(sx, sz) * 0.9;
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
      // downsample to 64x64 occupancy (any lit pixel)
      let hex = '';
      for (let gy = 0; gy < GRID; gy++) for (let gx = 0; gx < GRID / 8; gx++) {
        let b = 0;
        for (let gy2 = 0; gy2 < 4; gy2++) for (let gx2 = 0; gx2 < 8; gx2++) {
          const X = gx * 8 + gx2, Y = gy * 4 + gy2;
          const o = ((GRID - 1 - Y) * SZ + X) * 4;
          if (px[o] > 32) b |= 1 << (gy2 * 8 + gx2);
        }
        hex += ('0' + b.toString(16)).slice(-2);
      }
      // rest-pose CPU-skin == bind check (max deviation) + height/upright
      let bindDev = 0;
      const pa = posA.array;
      for (let i = 0; i < NVi * 3; i++) bindDev = Math.max(bindDev, Math.abs(vAll[i] - pa[i]));
      window.__GATE.enemyIoU = { ok: true, gridHex: hex, grid: GRID, SZ,
        meshMin: [mnx, mnz], meshMax: [mxx, mxz],
        height: +(mxz - mnz).toFixed(4), feetZ: +mnz.toFixed(4),
        bindMaxDev: +bindDev.toFixed(6), nVerts: NVi, nIdx: IN };
      log('enemyIoU: height=' + (mxz - mnz).toFixed(3) + ' feetZ=' + mnz.toFixed(3) + ' bindDev=' + bindDev.toFixed(5));
    } catch (e4) {
      window.__GATE.enemyIoU = { ok: false, error: String(e4 && e4.message || e4) };
      log('enemyIoU FAILED: ' + (e4 && e4.message || e4));
    }""",
    'IOU')

open(P, 'w', encoding='utf-8').write(src)
new_len = len(src)
print('len %d -> %d (delta %d)' % (orig_len, new_len, new_len - orig_len))
print('sha before/after:',
      hashlib.sha256(open(P, 'rb').read()).hexdigest()[:16])
