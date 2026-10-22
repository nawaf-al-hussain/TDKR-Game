#!/usr/bin/env python3
"""s51 T1: rebuild city_bisect_mip.html with ALL experiment knobs, cleanly.
Knobs: ?mip=0|nml|lml|lmn  ?nolm=1 (robust)  ?bias=<f>  ?nodepth=1  ?uvabs=1  ?texquad=1
Base: committed city_bisect.html @ s41-city-slice."""
import subprocess, re

SRC = subprocess.run(['git', '-C', '/tmp/my-project/work/TDKR-Game', 'show',
                      's41-city-slice:playable/city_bisect.html'],
                     capture_output=True, text=True).stdout
assert len(SRC) > 10000

# --- 1) knobs after QS declaration ---
old = 'const QS = new URLSearchParams(location.search);'
assert old in SRC
SRC = SRC.replace(old, old + '''
const MIPVAR = QS.get("mip") || "0";
window.__LODBIAS = QS.get("bias") === null ? "-1.0" : QS.get("bias");
const NODEPTH = QS.get("nodepth") === "1";
const UVABS = QS.get("uvabs") === "1";
''', 1)

# --- 2) robust NOLM ---
old = "if (NOLM) { modeKey += '|nolm'; fsrc = fsrc.split('texture2D(LightMap, vCoord1) * 2.0').join('vec4(1.0)'); }"
assert old in SRC
SRC = SRC.replace(old, ("if (NOLM) { modeKey += '|nolm'; const __bl = fsrc.length; "
                        "fsrc = fsrc.replace(/texture2D\\s*\\(\\s*LightMap\\s*,[^)]*\\)\\s*\\*\\s*2\\.0/g, 'vec4(1.0)'); "
                        "window.__NOLM_OK = (fsrc.length !== __bl); }"), 1)

# --- 3) depth toggle ---
old = 'G.enable(G.DEPTH_TEST);'
assert old in SRC
SRC = SRC.replace(old, 'if (!NODEPTH) G.enable(G.DEPTH_TEST);', 1)

# --- 4) UV override ---
old = "uv0[(vo+v)*2] = fbuf.getInt16(o + d0.start, true)/32767*0.5 + 0.5;"
assert old in SRC
SRC = SRC.replace(old, "uv0[(vo+v)*2] = UVABS ? 0.5 : (fbuf.getInt16(o + d0.start, true)/32767*0.5 + 0.5);", 1)
old = "uv0[(vo+v)*2+1] = 1.0 - (fbuf.getInt16(o + d0.start + 2, true)/32767*0.5 + 0.5);"
assert old in SRC
SRC = SRC.replace(old, "uv0[(vo+v)*2+1] = UVABS ? 0.5 : 1.0 - (fbuf.getInt16(o + d0.start + 2, true)/32767*0.5 + 0.5);", 1)

# --- 5) LOD_BIAS injection via compileZ ---
old = 'function compileZ(type, src) {'
assert old in SRC
SRC = SRC.replace(old, old + '\n  if (src.indexOf("__LODBIAS__") >= 0) src = src.split("__LODBIAS__").join(window.__LODBIAS);', 1)
old = '#define LOD_BIAS -1.0'
assert old in SRC
SRC = SRC.replace(old, '#define LOD_BIAS __LODBIAS__', 1)

# --- 6) mip chain upload in texZget ---
old = '''  const tx = G.createTexture();
  G.bindTexture(G.TEXTURE_2D, tx);
  G.texImage2D(G.TEXTURE_2D, 0, G.RGBA, t.w, t.h, 0, G.RGBA, G.UNSIGNED_BYTE,
               new Uint8Array(t.data.buffer, t.data.byteOffset, t.data.byteLength));
  G.texParameteri(G.TEXTURE_2D, G.TEXTURE_WRAP_S, G.REPEAT);
  G.texParameteri(G.TEXTURE_2D, G.TEXTURE_WRAP_T, G.REPEAT);
  G.texParameteri(G.TEXTURE_2D, G.TEXTURE_MIN_FILTER, G.NEAREST);
  G.texParameteri(G.TEXTURE_2D, G.TEXTURE_MAG_FILTER, G.NEAREST);
  const o = { tx, alpha: t.alpha, w: t.w, h: t.h };'''
assert old in SRC
new = '''  const tx = G.createTexture();
  G.bindTexture(G.TEXTURE_2D, tx);
  if (MIPVAR !== "0") {
    const tu2 = texMember(texGla, name);
    const parts2 = unwrapSplitParts(tu2);
    const mm = decodePvrMips(parts2['rgb.pvr'] || parts2['rgb']);
    for (let i = 0; i < mm.levels.length; i++) {
      const L = mm.levels[i];
      G.texImage2D(G.TEXTURE_2D, i, G.RGBA, L.w, L.h, 0, G.RGBA, G.UNSIGNED_BYTE,
                   new Uint8Array(L.rgba.buffer, L.rgba.byteOffset, L.rgba.byteLength));
    }
    const MINF = { nml: G.NEAREST_MIPMAP_LINEAR, lml: G.LINEAR_MIPMAP_LINEAR,
                   lmn: G.LINEAR_MIPMAP_NEAREST }[MIPVAR] || G.NEAREST_MIPMAP_LINEAR;
    G.texParameteri(G.TEXTURE_2D, G.TEXTURE_MIN_FILTER, MINF);
    G.texParameteri(G.TEXTURE_2D, G.TEXTURE_MAG_FILTER, G.LINEAR);
  } else {
    G.texImage2D(G.TEXTURE_2D, 0, G.RGBA, t.w, t.h, 0, G.RGBA, G.UNSIGNED_BYTE,
                 new Uint8Array(t.data.buffer, t.data.byteOffset, t.data.byteLength));
    G.texParameteri(G.TEXTURE_2D, G.TEXTURE_MIN_FILTER, G.NEAREST);
    G.texParameteri(G.TEXTURE_2D, G.TEXTURE_MAG_FILTER, G.NEAREST);
  }
  G.texParameteri(G.TEXTURE_2D, G.TEXTURE_WRAP_S, G.REPEAT);
  G.texParameteri(G.TEXTURE_2D, G.TEXTURE_WRAP_T, G.REPEAT);
  const o = { tx, alpha: t.alpha, w: t.w, h: t.h };'''
SRC = SRC.replace(old, new, 1)

# --- 7) decodePvrMips before decodePvr ---
dp = 'function decodePvr(u8) {'
assert dp in SRC
mips_fn = '''function decodePvrMips(u8) {
  const dv = new DataView(u8.buffer, u8.byteOffset, u8.byteLength);
  if (dv.getUint32(0, true) !== 0x34) throw new Error('bad tex tag');
  const h0 = dv.getUint32(4, true), w0 = dv.getUint32(8, true);
  if (String.fromCharCode(u8[44], u8[45], u8[46], u8[47]) !== 'PVR!') throw new Error('bad PVR');
  const levels = [];
  let off = 52, w = w0, h = h0;
  for (let i = 0; i < 16 && w >= 1 && h >= 1; i++) {
    const bw = (w + 3) >> 2, bh = (h + 3) >> 2;
    const sz = bw * bh * 8;
    if (off + sz > u8.length) break;
    const rgba = window.ETC1_TDKR.decodeRGBA(u8.subarray(off, off + sz), w, h);
    levels.push({ w, h, rgba });
    off += sz;
    w = w >> 1; h = h >> 1;
    if (w === 0) w = 1;
    if (h === 0) h = 1;
    if (w0 === 1 && h0 === 1) break;
  }
  return { w: w0, h: h0, levels };
}
'''
SRC = SRC.replace(dp, mips_fn + dp, 1)

# --- 8) texquad function + call at every done site ---
quad_fn = '''
function runQuad() {
  try {
    const tqvs = 'attribute vec2 p; varying vec2 t; void main(){ t = p*0.5+0.5; gl_Position = vec4(p,0.0,1.0); }';
    const tqfs = 'precision mediump float; uniform sampler2D s; varying vec2 t; void main(){ gl_FragColor = texture2D(s, t); }';
    const vs2 = G.createShader(G.VERTEX_SHADER); G.shaderSource(vs2, tqvs); G.compileShader(vs2);
    const fs2 = G.createShader(G.FRAGMENT_SHADER); G.shaderSource(fs2, tqfs); G.compileShader(fs2);
    const pr2 = G.createProgram(); G.attachShader(pr2, vs2); G.attachShader(pr2, fs2); G.linkProgram(pr2);
    G.useProgram(pr2);
    const qb = G.createBuffer(); G.bindBuffer(G.ARRAY_BUFFER, qb);
    G.bufferData(G.ARRAY_BUFFER, new Float32Array([-1,-1, 1,-1, -1,1, 1,-1, 1,1, -1,1]), G.STATIC_DRAW);
    const lp = G.getAttribLocation(pr2, 'p');
    G.enableVertexAttribArray(lp); G.vertexAttribPointer(lp, 2, G.FLOAT, false, 0, 0);
    const texq = texZget('gothamcity_roads_details.tga', false);
    G.activeTexture(G.TEXTURE0); G.bindTexture(G.TEXTURE_2D, texq.tx);
    G.uniform1i(G.getUniformLocation(pr2, 's'), 0);
    G.disable(G.DEPTH_TEST);
    G.viewport(0, 0, W, H);
    G.drawArrays(G.TRIANGLES, 0, 6);
    const qbuf = new Uint8Array(W * H * 4);
    G.readPixels(0, 0, W, H, G.RGBA, G.UNSIGNED_BYTE, qbuf);
    let sr = 0, sg = 0, sb2 = 0, mx = 0;
    for (let i = 0; i < qbuf.length; i += 4) { sr += qbuf[i]; sg += qbuf[i+1]; sb2 += qbuf[i+2]; if (qbuf[i] > mx) mx = qbuf[i]; }
    const n2 = W * H;
    window.__QUAD = { mean: [Math.round(sr/n2*10)/10, Math.round(sg/n2*10)/10, Math.round(sb2/n2*10)/10],
                      maxr: mx, texw: texq.w, texh: texq.h, glerr: G.getError() };
  } catch (e) { window.__QUAD = { error: String(e) }; }
}
'''
anchor = 'document.querySelector(\'#f\').addEventListener'
assert anchor in SRC
SRC = SRC.replace(anchor, quad_fn + '\n' + anchor, 1)
n_done = SRC.count('window.__GATE.done = true;')
SRC = SRC.replace('window.__GATE.done = true;', 'window.__GATE.done = true;\n  if (QS.get("texquad") === "1") runQuad();')
print('done sites patched:', n_done)

out = '/tmp/my-project/work/city_slice_wt/playable/city_bisect_mip.html'
open(out, 'w').write(SRC)
print('written', out, len(SRC))

# extract module js for node --check
i = SRC.find('<script type="module">')
j = SRC.find('</script>', i)
js = SRC[i + len('<script type="module">'):j]
open('/tmp/my-project/work/s51_page_main.js', 'w').write(js)
print('js bytes', len(js))
