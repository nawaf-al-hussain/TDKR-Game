#!/usr/bin/env python3
"""s59 T2 part 2: integration_lazy.html — enemy gate enhancements:
CPU-skin vertex-displacement sampler per clip phase + wrong-clip negative control."""
import sys

WT = '/tmp/my-project/work/ghpages_staged_wt/playable'
H = f'{WT}/integration_lazy.html'

def patch(old, new, tag):
    src = open(H, encoding='utf-8').read()
    assert src.count(old) == 1, f'{tag}: count={src.count(old)}'
    out = src.replace(old, new)
    assert out != src, f'{tag}: no change'
    open(H, 'wb').write(out.encode('utf-8'))
    print(f'patched {tag}')

# 1) probe state after mercSeq init in loadMerc
patch("""  mercSeq = { t0: performance.now(), phase: 0, wraps: 0, zmin: 1e9, zmax: -1e9, lastT: 0 };""",
      """  mercSeq = { t0: performance.now(), phase: 0, wraps: 0, zmin: 1e9, zmax: -1e9, lastT: 0 };
  // s59 T2: CPU-skin probe (vertex displacement gate). applyBoneTransform on a
  // subset; per-phase mean |delta|; wrong-clip negative control at report time.
  mercSkinProbe = null; mercDisp = { byClip: {} };
  {
    const sm0 = (() => { let s = null; merc.traverse(o => { if (o.isSkinnedMesh) s = o; }); return s; })();
    if (sm0 && sm0.geometry.attributes.position) {
      const nV = sm0.geometry.attributes.position.count;
      const step = Math.max(1, Math.floor(nV / 150));
      const idxs = [];
      for (let i = 0; i < nV && idxs.length < 150; i += step) idxs.push(i);
      mercSkinProbe = { sm: sm0, idxs, v: new THREE.Vector3() };
    }
  }""",
      'probe init')

# 2) declarations near the merc globals
patch("let merc = null, mercMixer = null, mercActions = {}, mercSeq = null;",
      "let merc = null, mercMixer = null, mercActions = {}, mercSeq = null;\nlet mercSkinProbe = null, mercDisp = { byClip: {} };",
      'globals')

# 3) sampler + accumulation in mercTick (after mixer update)
patch("""  let bb = new THREE.Box3().setFromObject(merc);
  if (isFinite(bb.min.z)) { mercSeq.zmin = Math.min(mercSeq.zmin, bb.min.z); mercSeq.zmax = Math.max(mercSeq.zmax, bb.max.z); }
  if (t > 12 && !mercSeq.reported) {
    mercSeq.reported = true;
    window.__GATE.enemyPlay = { ok: true, wraps: mercSeq.wraps, phasesSeen: mercSeq.phase + 1,
      bboxZmin: +mercSeq.zmin.toFixed(3), bboxZmax: +mercSeq.zmax.toFixed(3),
      clip: ENEMY_CLIPS[mercSeq.phase], dmg: ENEMY_DMG };
    log('enemy playback: wraps=' + mercSeq.wraps + ' bboxZ=[' + mercSeq.zmin.toFixed(2) + ',' + mercSeq.zmax.toFixed(2) + ']');
  }
}""",
      """  let bb = new THREE.Box3().setFromObject(merc);
  if (isFinite(bb.min.z)) { mercSeq.zmin = Math.min(mercSeq.zmin, bb.min.z); mercSeq.zmax = Math.max(mercSeq.zmax, bb.max.z); }
  // s59 T2: per-phase mean vertex displacement (CPU skinning on the subset)
  if (mercSkinProbe) {
    const pr = mercSkinProbe, out = new Float32Array(pr.idxs.length * 3);
    for (let k = 0; k < pr.idxs.length; k++) {
      pr.sm.applyBoneTransform(pr.idxs[k], pr.v);
      out[k*3] = pr.v.x; out[k*3+1] = pr.v.y; out[k*3+2] = pr.v.z;
    }
    if (mercSeq.lastSkin && mercSeq.lastSkin.length === out.length) {
      let s = 0;
      for (let i = 0; i < out.length; i++) s += Math.abs(out[i] - mercSeq.lastSkin[i]);
      const nm = ENEMY_CLIPS[mercSeq.phase];
      if (!mercDisp.byClip[nm]) mercDisp.byClip[nm] = { sum: 0, n: 0 };
      mercDisp.byClip[nm].sum += s / pr.idxs.length; mercDisp.byClip[nm].n++;
    }
    mercSeq.lastSkin = out;
  }
  if (t > 12 && !mercSeq.reported) {
    mercSeq.reported = true;
    // negative control: sample the WRONG clip (walk) labeled as the idle slot;
    // its displacement must differ from the measured enemy idle.
    const ctlClip = ENEMY_CLIPS[1];
    for (const nm of ENEMY_CLIPS) mercActions[nm].setEffectiveWeight(0);
    const ca = mercActions[ctlClip]; ca.setEffectiveWeight(1); ca.play();
    let ctlSum = 0, ctlN = 0, prev = null;
    for (let f = 0; f < 30; f++) {
      mercMixer.update(1 / 60);
      if (mercSkinProbe) {
        const pr = mercSkinProbe, out = new Float32Array(pr.idxs.length * 3);
        for (let k = 0; k < pr.idxs.length; k++) {
          pr.sm.applyBoneTransform(pr.idxs[k], pr.v);
          out[k*3] = pr.v.x; out[k*3+1] = pr.v.y; out[k*3+2] = pr.v.z;
        }
        if (prev) { let s = 0; for (let i = 0; i < out.length; i++) s += Math.abs(out[i] - prev[i]);
          ctlSum += s / pr.idxs.length; ctlN++; }
        prev = out;
      }
    }
    ca.setEffectiveWeight(0);
    const disp = {};
    for (const k of Object.keys(mercDisp.byClip)) disp[k] = +(mercDisp.byClip[k].sum / Math.max(1, mercDisp.byClip[k].n)).toFixed(5);
    const dispCtl = +(ctlSum / Math.max(1, ctlN)).toFixed(5);
    const dIdle = disp[ENEMY_CLIPS[0]], dWalk = disp[ENEMY_CLIPS[1]], dRun = disp[ENEMY_CLIPS[2]];
    const okGate = isFinite(dIdle) && isFinite(dWalk) && isFinite(dRun) && isFinite(dispCtl) &&
      dIdle > 0 && dWalk > 0 && dRun > 0 && Math.abs(dispCtl - dIdle) > 1e-4;
    window.__GATE.enemyPlay = { ok: okGate, wraps: mercSeq.wraps, phasesSeen: mercSeq.phase + 1,
      bboxZmin: +mercSeq.zmin.toFixed(3), bboxZmax: +mercSeq.zmax.toFixed(3),
      clip: ENEMY_CLIPS[mercSeq.phase], dmg: ENEMY_DMG,
      dispIdle: dIdle, dispWalk: dWalk, dispRun: dRun, dispCtlWrongClip: dispCtl,
      ctlClip, probeVerts: mercSkinProbe ? mercSkinProbe.idxs.length : 0 };
    log('enemy playback: wraps=' + mercSeq.wraps + ' disp=' + JSON.stringify(disp) + ' ctlWrong=' + dispCtl +
        ' bboxZ=[' + mercSeq.zmin.toFixed(2) + ',' + mercSeq.zmax.toFixed(2) + ']');
  }
}""",
      'mercTick displacement + control')
print('OK')
