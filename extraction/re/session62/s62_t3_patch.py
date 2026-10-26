#!/usr/bin/env python3
"""S62 T3: replace the s60 FK point cloud with the SKINNED MERC MESH (triangle raster)
in enemy_viewer.html's combat slice + per-state skinned-silhouette gates.
String patches: assert unique match, file changed, node --check after."""
PAGE = '/tmp/my-project/work/ghpages_staged_wt/playable/enemy_viewer.html'
src = open(PAGE, encoding='utf-8').read()
n0 = len(src)

# ---- 1) index buffer after MC.vbuf creation ----
A1 = """  MC.vbuf = G.createBuffer();"""
assert src.count(A1) == 1
N1 = """  MC.vbuf = G.createBuffer();
  // s62 T3: skinned MESH (triangle raster) instead of the FK point cloud
  MC.idx = skin.idx; MC.IDXN = skin.IDXN != null ? skin.IDXN : skin.idx.length;
  MC.ibuf = G.createBuffer();
  G.bindBuffer(G.ELEMENT_ARRAY_BUFFER, MC.ibuf);
  G.bufferData(G.ELEMENT_ARRAY_BUFFER, new Uint16Array(MC.idx), G.STATIC_DRAW);
  // offscreen raster for per-state silhouettes
  MC.rc = document.createElement('canvas'); MC.rc.width = 128; MC.rc.height = 128;
  MC.rg = MC.rc.getContext('webgl', { preserveDrawingBuffer: true });
  // raster program + buffers MUST live on the raster context rg (no GL object sharing)
  var rc = function (t, s3) { var o = MC.rg.createShader(t); MC.rg.shaderSource(o, s3); MC.rg.compileShader(o); return o; };
  MC.rprog = MC.rg.createProgram();
  MC.rg.attachShader(MC.rprog, rc(MC.rg.VERTEX_SHADER, 'attribute vec2 a; uniform vec2 off; uniform float sc; void main(){ vec2 p = (a - off) * sc; gl_Position = vec4(p.x, p.y, 0.0, 1.0); }'));
  MC.rg.attachShader(MC.rprog, rc(MC.rg.FRAGMENT_SHADER, 'precision mediump float; void main(){ gl_FragColor = vec4(1.0); }'));
  MC.rg.linkProgram(MC.rprog);
  MC.raA = MC.rg.getAttribLocation(MC.rprog, 'a');
  MC.ruOff = MC.rg.getUniformLocation(MC.rprog, 'off'); MC.ruSc = MC.rg.getUniformLocation(MC.rprog, 'sc');
  MC.rvbuf = MC.rg.createBuffer(); MC.ribuf = MC.rg.createBuffer();
  MC.rg.bindBuffer(MC.rg.ARRAY_BUFFER, MC.rvbuf);
  MC.rg.bufferData(MC.rg.ARRAY_BUFFER, new Float32Array(skin.NV * 2), MC.rg.DYNAMIC_DRAW);
  MC.rg.bindBuffer(MC.rg.ELEMENT_ARRAY_BUFFER, MC.ribuf);
  MC.rg.bufferData(MC.rg.ELEMENT_ARRAY_BUFFER, new Uint16Array(skin.idx), MC.rg.STATIC_DRAW);"""
src = src.replace(A1, N1, 1)

# ---- 2) drawMerc: TRIANGLES via drawElements ----
A2 = """  G.drawArrays(G.POINTS, 0, MC.NV);
  MC.lastH = [f.hmin, f.hmax];"""
assert src.count(A2) == 1
N2 = """  G.bindBuffer(G.ELEMENT_ARRAY_BUFFER, MC.ibuf);
  G.drawElements(G.TRIANGLES, MC.IDXN - (MC.IDXN % 3), G.UNSIGNED_SHORT, 0);
  MC.lastH = [f.hmin, f.hmax];"""
src = src.replace(A2, N2, 1)

# ---- 3) per-state skinned silhouettes + mesh gates in runCombatGate ----
A3 = """  g.mercLoaded = MC.ready;
  g.mercVerts = MC.NV;   // skin._layout.NV"""
assert src.count(A3) == 1
N3 = """  g.mercLoaded = MC.ready;
  g.mercVerts = MC.NV;   // skin._layout.NV
  // ---- s62 T3: SKINNED MESH silhouettes per state (triangle raster, 128x128 -> 32x32) ----
  function meshSil(stateName, tS) {
    var f = skinFrame(stateName, tS);
    var rg = MC.rg, SZ = 128;
    var cx = 0, cz = 0;
    var sc2 = 1.8 / Math.max(1e-6, (MC.lastH ? (MC.lastH[1] - MC.lastH[0]) : 1.8));
    MC.rg.useProgram(MC.rprog);
    MC.rg.bindBuffer(MC.rg.ARRAY_BUFFER, MC.rvbuf);
    MC.rg.bufferData(MC.rg.ARRAY_BUFFER, f.xy, MC.rg.DYNAMIC_DRAW);
    MC.rg.enableVertexAttribArray(MC.raA);
    MC.rg.vertexAttribPointer(MC.raA, 2, MC.rg.FLOAT, false, 0, 0);
    MC.rg.bindBuffer(MC.rg.ELEMENT_ARRAY_BUFFER, MC.ribuf);
    MC.rg.uniform2fv(MC.ruOff, CAM); MC.rg.uniform1f(MC.ruSc, sc2);
    MC.rg.viewport(0, 0, SZ, SZ); MC.rg.clearColor(0, 0, 0, 1);
    MC.rg.clear(MC.rg.COLOR_BUFFER_BIT);
    MC.rg.drawElements(MC.rg.TRIANGLES, MC.IDXN - (MC.IDXN % 3), MC.rg.UNSIGNED_SHORT, 0);
    var px = new Uint8Array(SZ * SZ * 4);
    MC.rg.readPixels(0, 0, SZ, SZ, MC.rg.RGBA, MC.rg.UNSIGNED_BYTE, px);
    var occ = new Uint8Array(32 * 32), lit = 0;
    for (var y = 0; y < SZ; y++) for (var x = 0; x < SZ; x++) {
      if (px[(y * SZ + x) * 4] > 32) { lit++; occ[((31 - Math.floor(y / 4)) * 32) + Math.floor(x / 4)] = 1; }
    }
    return { occ: occ, lit: lit };
  }
  var sils = {};
  ['Idle', 'Walk', 'Run', 'Hurt', 'Death'].forEach(function (s5) {
    sils[s5] = meshSil(s5, s5 === 'Death' ? (MC.durs.Death || 1) * 0.5 : 0.5);
  });
  g.meshSil = {};
  ['Idle', 'Walk', 'Run', 'Hurt', 'Death'].forEach(function (s5) {
    g.meshSil[s5] = { lit: sils[s5].lit };
  });
  function occDiff(a, b) { var d = 0; for (var i = 0; i < a.occ.length; i++) d += (a.occ[i] ^ b.occ[i]); return d; }
  g.meshSilDiff = {
    idleWalk: occDiff(sils.Idle, sils.Walk), walkRun: occDiff(sils.Walk, sils.Run),
    idleDeath: occDiff(sils.Idle, sils.Death), idleHurt: occDiff(sils.Idle, sils.Hurt)
  };
  g.meshSilPass = sils.Idle.lit > 800 && sils.Walk.lit > 800 && g.meshSilDiff.idleWalk > 40 &&
    g.meshSilDiff.walkRun > 20 && g.meshSilDiff.idleDeath > 25;
  // wrong-clip mesh control: Walk-clip skin sampled while state=Idle vs Idle skin
  var mI = sils.Idle, mW = meshSil('Walk', 0.5);
  g.meshWrongClipDiff = occDiff(mI, mW);
  g.meshWrongClipDetected = g.meshWrongClipDiff > 40;"""
src = src.replace(A3, N3, 1)

# ---- 4) gate pass includes the mesh checks ----
A4 = """  g.pass = g.mercLoaded && g.ctlPass && g.ctlWrongClipDetected &&
    g.walkState === 'Walk' && g.runState === 'Run' && g.walk2State === 'Walk' &&
    g.stateAfter5 === 'Hurt' && g.hpAfter5 === 115 && g.stateAfterHurt === 'Walk' &&
    g.stateAfter10 === 'Hurt' && g.hpAfter10 === 105 && g.hpFinal === 0 && g.stateFinal === 'Death';"""
assert src.count(A4) == 1
N4 = """  g.pass = g.mercLoaded && g.ctlPass && g.ctlWrongClipDetected &&
    g.walkState === 'Walk' && g.runState === 'Run' && g.walk2State === 'Walk' &&
    g.stateAfter5 === 'Hurt' && g.hpAfter5 === 115 && g.stateAfterHurt === 'Walk' &&
    g.stateAfter10 === 'Hurt' && g.hpAfter10 === 105 && g.hpFinal === 0 && g.stateFinal === 'Death' &&
    g.meshSilPass && g.meshWrongClipDetected;"""
src = src.replace(A4, N4, 1)

assert len(src) != n0
open(PAGE, 'w', encoding='utf-8').write(src)
print('patched enemy_viewer.html, delta', len(src) - n0)
