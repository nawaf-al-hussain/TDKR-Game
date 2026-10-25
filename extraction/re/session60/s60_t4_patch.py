#!/usr/bin/env python3
"""s60 T4 patch: enemy_viewer.html gets the REAL merc (FK-skinned point cloud from
Bane_mercenary.bdae + batman_anims.bdae via tdkr_pipeline lazy slices) driven by the
s59 state machine (extended with Run), and the gate gains clip-per-state + wrong-clip
control. Asserts unique matches; byte-diff printed."""
P = '/tmp/my-project/work/ghpages_staged_wt/playable/enemy_viewer.html'
src = open(P, encoding='utf-8').read()
n0 = len(src)

def rep(old, new, tag):
    global src
    assert src.count(old) == 1, 'PATCH %s: %d matches' % (tag, src.count(old))
    src = src.replace(old, new, 1)
    print('patched', tag)

# 1) pipeline include + zip input UI
rep('<canvas id="c" width="960" height="600"></canvas>',
    '<canvas id="c" width="960" height="600"></canvas>\n'
    '<script src="./tdkr_pipeline.js"></script>', 'PIPELINE-INCLUDE')
rep('<div id="gateOut">gate: pending</div>',
    '<div id="gateOut">gate: pending</div>\n'
    ' <h4>s60 T4: real merc in the slice (Bane_mercenary.bdae FK point cloud)</h4>\n'
    ' <input type="file" id="zf"><span id="mercStat">merc: not loaded</span>', 'UI')

# 2) state machine: add Run (alerted chase) — s59 machine + distance rule
rep("""  // alert transition: player inside the visibility cone (any radius <= R_FAR)
  setState(inCone(PL[0], PL[1]) ? 'Walk' : 'Idle');""",
    """  // alert transition: player inside the visibility cone (any radius <= R_FAR)
  // s60 T4: alerted AND player beyond 14 u -> Run (chase approach)
  if (inCone(PL[0], PL[1])) {
    var dNow = Math.hypot(PL[0] - ME[0], PL[1] - ME[1]);
    setState(dNow > 14.0 ? 'Run' : 'Walk');
  } else setState('Idle');""", 'RUN-STATE')
rep("var ST = 'Idle';        // Idle | Walk | Hurt | Death",
    "var ST = 'Idle';        // Idle | Walk | Run | Hurt | Death", 'ST-COMMENT')

# 3) the merc combat module + extended gate, injected before the final draw()
MODULE = r"""
// ================= s60 T4: REAL MERC in the combat slice =================
// Rig: Bane_mercenary.bdae (readBdae2, header-derived); anims: the SHARED bank
// batman_anims.bdae (decodeAnims/assembleClip). FK = node hierarchy (BIPED parents),
// animated rotation channels (nearest key) + root position channel; skin =
// sum_k w_k * M_{J_k} * invB_{J_k} * v  (same pairing the three.js path validated).
var CLIPS5 = { Idle: '_014_idle_enemy_combat', Walk: '_166_enemy_walk', Run: '_171_enemy_run',
               Hurt: '_223_enemy_hurtl', Death: '_250_enemy_death1' };
var u32leL = function (b, o) { return (b[o] | (b[o+1] << 8) | (b[o+2] << 16) | (b[o+3] << 24)) >>> 0; };
var u16leL = function (b, o) { return b[o] | (b[o+1] << 8); };
var LATIN = new TextDecoder('latin1');
async function zipReadLazyL(file, m) {
  var hh = new Uint8Array(await file.slice(m.lho, m.lho + 30).arrayBuffer());
  if (u32leL(hh, 0) !== 0x04034b50) throw new Error('bad local header');
  var nlen = u16leL(hh, 26), elen = u16leL(hh, 28);
  var start = m.lho + 30 + nlen + elen;
  var blob = file.slice(start, start + m.csize);
  if (m.method === 0) return new Uint8Array(await blob.arrayBuffer());
  var ds2 = new DecompressionStream('deflate-raw');
  var st2 = new Response(blob).body.pipeThrough(ds2);
  return new Uint8Array(await new Response(st2).arrayBuffer());
}
async function streamInflateRangesL(file, m, ranges) {
  var hh = new Uint8Array(await file.slice(m.lho, m.lho + 30).arrayBuffer());
  var nlen = u16leL(hh, 26), elen = u16leL(hh, 28);
  var start = m.lho + 30 + nlen + elen;
  var ds2 = new DecompressionStream('deflate-raw');
  var src2 = new Response(file.slice(start, start + m.csize)).body.pipeThrough(ds2);
  var reader = src2.getReader();
  var outs = ranges.map(function (r) { return new Uint8Array(r.s); });
  var pos = 0;
  var endMax = 0; ranges.forEach(function (r) { endMax = Math.max(endMax, r.o + r.s); });
  while (pos < endMax) {
    var rd = await reader.read();
    if (rd.done) break;
    var v = rd.value;
    for (var i = 0; i < ranges.length; i++) {
      var c0 = Math.max(ranges[i].o, pos), c1 = Math.min(ranges[i].o + ranges[i].s, pos + v.length);
      if (c1 > c0) outs[i].set(v.subarray(c0 - pos, c1 - pos), c0 - ranges[i].o);
    }
    pos += v.length;
  }
  try { await reader.cancel(); } catch (e) {}
  return outs;
}
async function glaSliceLazyL(file, m, want) {
  var head = (await streamInflateRangesL(file, m, [{ o: 0, s: 1 << 20 }]))[0];
  var dv = new DataView(head.buffer, head.byteOffset, head.byteLength);
  var idxSize = dv.getUint32(4), n = dv.getUint32(12);
  var pool = head.subarray(16 + n * 16, idxSize);
  var ents = {};
  for (var i = 0; i < n; i++) {
    var b = 16 + i * 16;
    var o = dv.getUint32(b), s = dv.getUint32(b + 4), no = dv.getUint32(b + 8);
    var e = pool.indexOf(0, no); if (e < 0) e = no + 96;
    ents[LATIN.decode(pool.subarray(no, e))] = { o: o, s: s };
  }
  var rs = [], names = [];
  for (var k = 0; k < want.length; k++) {
    var en = ents[want[k]];
    if (!en) throw new Error('gla member missing: ' + want[k]);
    rs.push({ o: en.o, s: en.s }); names.push(want[k]);
  }
  var outs = await streamInflateRangesL(file, m, rs.map(function (r) { return { o: r.o, s: r.s + (1 << 16) }; }));
  var res = {};
  names.forEach(function (nm, i) { res[nm] = outs[i]; });
  return res;
}
function qmulL(a, b) {
  var x1 = a[0], y1 = a[1], z1 = a[2], w1 = a[3], x2 = b[0], y2 = b[1], z2 = b[2], w2 = b[3];
  return [w1*x2 + x1*w2 + y1*z2 - z1*y2, w1*y2 - x1*z2 + y1*w2 + z1*x2,
          w1*z2 + x1*y2 - y1*x2 + z1*w2, w1*w2 - x1*x2 - y1*y2 - z1*z2];
}
function qrotL(q, v) {
  var vv = [v[0], v[1], v[2], 0];
  var qc = [-q[0], -q[1], -q[2], q[3]];
  var o = qmulL(qmulL(q, vv), qc);
  return [o[0], o[1], o[2]];
}
var MC = { ready: false };
async function loadMercCombat(file) {
  var dir = await TDKR.zipDirLazy(file);
  var mActors = null;
  for (var i = 0; i < dir.length; i++) if (/data\/actors\.gla$/i.test(dir[i].name)) mActors = dir[i];
  if (!mActors) throw new Error('actors.gla not in zip');
  var mem = await glaSliceLazyL(file, mActors, ['Bane_mercenary.bdae', 'batman_anims.bdae']);
  var skin = TDKR.readBdae2(mem['Bane_mercenary.bdae']);
  var A = TDKR.decodeAnims(mem['batman_anims.bdae']);
  var byName = {};
  for (var c = 0; c < A.clips.length; c++) byName[A.clips[c].name] = A.clips[c];
  var chans5 = {};
  var durs = {};
  for (var st5 in CLIPS5) {
    var cl = byName[CLIPS5[st5]];
    if (!cl) throw new Error('clip missing: ' + CLIPS5[st5]);
    var as = TDKR.assembleClip(A, cl, 0);
    chans5[st5] = as.chans;
    durs[st5] = (cl.te - cl.ts) / 1000.0;
  }
  // skeleton: palette joint node names + BIPED parents + node locals
  var nodes = {};
  for (var nn = 0; nn < skin.nodes.length; nn++) nodes[skin.nodes[nn].name] = skin.nodes[nn];
  var order = [];
  for (var j = 0; j < skin.jointNodes.length; j++) order.push(skin.jointNodes[j]);
  // topological order (parents first)
  var placed = {}, topo = [];
  function place(nm) {
    if (placed[nm]) return;
    placed[nm] = true;
    var p = skin.parentName(nm);
    if (p && nodes[p] && order.indexOf(p) >= 0) place(p);
    topo.push(nm);
  }
  for (var j2 = 0; j2 < order.length; j2++) place(order[j2]);
  MC = { ready: true, skin: skin, chans: chans5, durs: durs, topo: topo,
         nodes: nodes, NV: skin.NV,
         vert0: skin.verts, idx: skin.idx,
         J: skin.skinJ, W: skin.skinW, invB: skin.invB };
  // point-cloud GL buffers
  MC.prog = sh('attribute vec2 a; uniform vec2 off; uniform float sc; void main(){ vec2 p = (a - off) * sc; gl_Position = vec4(p.x, p.y, 0.0, 1.0); gl_PointSize = 2.2; }',
    'precision mediump float; uniform vec4 col; void main(){ gl_FragColor = col; }');
  MC.uOff = G.getUniformLocation(MC.prog, 'off'); MC.uSc = G.getUniformLocation(MC.prog, 'sc');
  MC.uCol = G.getUniformLocation(MC.prog, 'col'); MC.aA = G.getAttribLocation(MC.prog, 'a');
  MC.vbuf = G.createBuffer();
  document.getElementById('mercStat').textContent = 'merc: ' + skin.NV + ' verts, ' +
    skin.jointNodes.length + ' joints, 5 clips';
}
function chanSample(ch5, tMs) {
  // nearest key at or before tMs (s35 convention); null channel -> null
  if (!ch5) return null;
  var t = ch5.t, v = ch5.v;
  var lo = 0, hi = t.length - 1;
  if (tMs <= t[0]) return v[0];
  if (tMs >= t[hi]) return v[hi];
  while (hi - lo > 1) { var mid = (lo + hi) >> 1; if (t[mid] <= tMs) lo = mid; else hi = mid; }
  return v[lo];
}
function chanSampleRoot(ch5, tMs) {
  if (!ch5) return [0, 0, 0];
  var s = chanSample(ch5, tMs);
  return s ? [s[0], s[1], s[2]] : [0, 0, 0];
}
function fkPose(stateName, tState) {
  // returns worldP/worldQ per joint name (rig space, z-up)
  var chans = MC.chans[stateName];
  var tMs = Math.round(tState * 1000);
  var chanIdx = {};
  for (var c = 0; c < A_CH.length; c++) chanIdx[A_CH[c].name + '|' + A_CH[c].ty] = c;
  var WP = {}, WQ = {};
  for (var i = 0; i < MC.topo.length; i++) {
    var nm = MC.topo[i];
    var nd = MC.nodes[nm];
    var ciR = chanIdx[nm + '|5'];
    var q = (ciR !== undefined && chans[ciR]) ? chanSample(chans[ciR], tMs) : nd.q;
    if (!q) q = nd.q;
    var parent = MC.skin.parentName(nm);
    if (nm === 'Bip01') {
      var ciP = chanIdx[nm + '|1'];
      WP[nm] = chanSampleRoot(ciP !== undefined ? chans[ciP] : null, tMs);
      WQ[nm] = q;
    } else if (parent && WP[parent]) {
      var lt = [nd.t[0] * nd.s[0], nd.t[1] * nd.s[1], nd.t[2] * nd.s[2]];
      var off = qrotL(WQ[parent], lt);
      WP[nm] = [WP[parent][0] + off[0], WP[parent][1] + off[1], WP[parent][2] + off[2]];
      WQ[nm] = qmulL(WQ[parent], q);
    } else {
      WP[nm] = [nd.t[0], nd.t[1], nd.t[2]];
      WQ[nm] = q;
    }
  }
  return { WP: WP, WQ: WQ };
}
var A_CH = null;
function skinFrame(stateName, tState) {
  var pose = fkPose(stateName, tState);
  var NV = MC.NV, out = new Float32Array(NV * 2);
  var hmin = 1e9, hmax = -1e9;
  var J = MC.J, W = MC.W, V = MC.vert0, invB = MC.invB, WP = pose.WP, WQ = pose.WQ;
  var nameToIdx = {};
  for (var k = 0; k < MC.skin.jointNodes.length; k++) nameToIdx[MC.skin.jointNodes[k]] = k;
  for (var v = 0; v < NV; v++) {
    var px = V[3*v], py = V[3*v+1], pz = V[3*v+2];
    var ox = 0, oy = 0, oz = 0;
    for (var s4 = 0; s4 < 4; s4++) {
      var w = W[4*v + s4];
      if (w <= 0) continue;
      var jn = MC.skin.jointNodes[J[4*v + s4]];
      if (!jn || !WQ[jn]) continue;
      var q = WQ[jn], p = WP[jn];
      var ib = invB[J[4*v + s4]];
      // invB (file) * v  (affine, column-major 4x4 rows stored flat)
      var bx = ib[0]*px + ib[4]*py + ib[8]*pz + ib[12];
      var by = ib[1]*px + ib[5]*py + ib[9]*pz + ib[13];
      var bz = ib[2]*px + ib[6]*py + ib[10]*pz + ib[14];
      // rotate by world q, translate by world p
      var r = qrotL(q, [bx, by, bz]);
      ox += w * (r[0] + p[0]); oy += w * (r[1] + p[1]); oz += w * (r[2] + p[2]);
    }
    out[2*v] = ox; out[2*v+1] = oy;
    if (oz < hmin) hmin = oz; if (oz > hmax) hmax = oz;
  }
  return { xy: out, hmin: hmin, hmax: hmax };
}
function drawMerc(stateName, tState) {
  if (!MC.ready) return;
  var f = skinFrame(stateName, tState);
  G.useProgram(MC.prog);
  G.uniform2fv(MC.uOff, CAM); G.uniform1f(MC.uSc, SC);
  G.uniform4fv(MC.uCol, stateName === 'Hurt' ? [1, 0.5, 0.2, 1] :
    (stateName === 'Death' ? [0.5, 0.5, 0.55, 1] : [0.35, 0.9, 1, 1]));
  G.bindBuffer(G.ARRAY_BUFFER, MC.vbuf);
  G.bufferData(G.ARRAY_BUFFER, f.xy, G.DYNAMIC_DRAW);
  G.enableVertexAttribArray(MC.aA);
  G.vertexAttribPointer(MC.aA, 2, G.FLOAT, false, 0, 0);
  G.drawArrays(G.POINTS, 0, MC.NV);
  MC.lastH = [f.hmin, f.hmax];
  return f;
}
// ---- forced wrong-clip control: sample Walk clip while state=Idle ----
function drawMercWrongClip(tState) {
  if (!MC.ready) return skinFrame('Idle', tState);
  var f = skinFrame('Walk', tState);   // WRONG clip for Idle state
  return f;
}
async function runCombatGate() {
  var g = { enabled: true, states: ['Idle', 'Walk', 'Run', 'Hurt', 'Death'],
    clipByState: CLIPS5, fovDeg: FOV_DEG, rNear: R_NEAR, rFar: R_FAR, health0: HP0,
    dmg: [DMG5, DMG10], runRule: 'alerted && dist > 14', hurtHoldSec: 0.4 };
  var rad = faceDeg * Math.PI / 180;
  function st(t) { tick(t); return ST; }
  // controls (s59): far outside cone; inside radius but behind facing
  PL = [0, 60]; st(0.016);
  g.ctlFar = { pos: [0, 60], state: ST, clip: CLIPS5[ST] === CLIPS5.Idle };
  PL = [ME[0] - 15 * Math.cos(rad), ME[1] - 15 * Math.sin(rad)]; st(0.016);
  g.ctlBehind = { state: ST, clip: CLIPS5[ST] === CLIPS5.Idle };
  g.ctlPass = g.ctlFar.state === 'Idle' && g.ctlBehind.state === 'Idle';
  // enter cone near (8 u) -> Walk
  PL = [ME[0] + 8 * Math.cos(rad), ME[1] + 8 * Math.sin(rad)]; st(0.016);
  g.walkState = ST;
  // far-but-in-cone (15.5 u) -> Run
  PL = [ME[0] + 15.5 * Math.cos(rad), ME[1] + 15.5 * Math.sin(rad)]; st(0.016);
  g.runState = ST;
  // back near -> Walk
  PL = [ME[0] + 8 * Math.cos(rad), ME[1] + 8 * Math.sin(rad)]; st(0.016);
  g.walk2State = ST;
  // hits: 5 -> Hurt; expire -> Walk; 10 -> Hurt; drain -> Death
  applyHit(DMG5);  g.hpAfter5 = health; g.stateAfter5 = ST;
  tick(0.5);       g.stateAfterHurt = ST;
  applyHit(DMG10); g.hpAfter10 = health; g.stateAfter10 = ST;
  tick(0.5);
  var guard = 0;
  while (health > 0 && guard < 40) { applyHit(DMG10); tick(0.5); guard++; }
  g.hpFinal = health; g.stateFinal = ST; g.stateSeq = stSeq.slice(0, 24);
  // wrong-clip control: while Idle, a Walk-clip skin must DIFFER from the Idle skin
  PL = [0, 60]; st(0.016);
  var fIdle = skinFrame('Idle', 0.5), fWrong = drawMercWrongClip(0.5);
  var d = 0;
  for (var i = 0; i < fIdle.xy.length; i++) d += Math.abs(fIdle.xy[i] - fWrong.xy[i]);
  g.ctlWrongClipDiff = +(d / MC.NV).toFixed(4);
  g.ctlWrongClipDetected = g.ctlWrongClipDiff > 0.05;
  g.mercLoaded = MC.ready;
  g.mercVerts = MC.NV;
  g.pass = g.mercLoaded && g.ctlPass && g.ctlWrongClipDetected &&
    g.walkState === 'Walk' && g.runState === 'Run' && g.walk2State === 'Walk' &&
    g.stateAfter5 === 'Hurt' && g.hpAfter5 === 115 && g.stateAfterHurt === 'Walk' &&
    g.stateAfter10 === 'Hurt' && g.hpAfter10 === 105 && g.hpFinal === 0 && g.stateFinal === 'Death';
  window.__GATE = window.__GATE || {};
  window.__GATE.combat = g;
  document.getElementById('gateOut').textContent = 'combat gate: ' + JSON.stringify(g);
}
// hook: load + render loop + run gate after load
document.getElementById('zf').addEventListener('change', async function (e) {
  try {
    await loadMercCombat(e.target.files[0]);
    runCombatGate();
  } catch (err) {
    document.getElementById('mercStat').textContent = 'merc: ERROR ' + (err && err.message || err);
  }
});
var mercClock0 = null;
var _draw0 = draw;
draw = function () {
  _draw0();
  if (MC.ready) {
    var dt5 = ST === 'Hurt' ? Math.max(0, 0.4 - Math.max(0, hurtT)) : (performance.now() - (mercClock0 = mercClock0 || performance.now())) / 1000;
    var tS = ST === 'Death' ? (MC.durs.Death || 1) : (ST === 'Hurt' ? (0.4 - Math.max(0, hurtT)) : (performance.now() / 1000) % Math.max(0.05, MC.durs[ST] || 1));
    drawMerc(ST, tS);
  }
};
"""
rep("// ---------- scripted gate: negative control (outside cone) then inside, hits, death ----------",
    MODULE + "\n// ---------- scripted gate: negative control (outside cone) then inside, hits, death ----------",
    'MODULE')
# A_CH assignment: after pipeline load set A_CH from decodeAnims CH (needs A) - define at load
rep("  MC = { ready: true, skin: skin, chans: chans5, durs: durs, topo: topo,",
    "  A_CH = A.CH;\n  MC = { ready: true, skin: skin, chans: chans5, durs: durs, topo: topo,", 'A-CH')
open(P, 'w', encoding='utf-8').write(src)
print('len %d -> %d (+%d)' % (n0, len(src), len(src) - n0))
