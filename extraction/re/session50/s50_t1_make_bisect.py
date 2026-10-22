#!/usr/bin/env python3
"""s50 T1: generate playable/city_bisect.html from city_zone2.html with
controlled-variant switches + GL error probe + OES_element_index_uint fix.
Variants (URL params):
  ?probe=1     per-draw getError() into window.__GLERR
  ?noext=1     do NOT enable OES_element_index_uint (failure-mode probe)
  ?skipmiss=1  skip batches whose DiffuseMap decode failed (Python ref semantics)
  ?flat=1      flat gray output, discard stripped (pure geometry/coverage)
  ?painter=1   global painter order (height, seg, tri), flat color, depth OFF
  ?only=Fx     draw only batches of that mapped effect family
  ?ref=png     correlation target (default s48_ref_zone.png)"""
import re

SRC = '/tmp/my-project/work/city_slice_wt/playable/city_zone2.html'
DST = '/tmp/my-project/work/city_slice_wt/playable/city_bisect.html'
s = open(SRC).read()

# 1. query params + extension + probe state (after GL context creation)
anchor = "const G = glz.getContext('webgl', { preserveDrawingBuffer: true, antialias: false, depth: true });\nif (!G) throw new Error('no webgl');"
assert anchor in s, 'ctx anchor missing'
s = s.replace(anchor, anchor + """
const QS = new URLSearchParams(location.search);
window.__GLERR = [];
if (QS.get('noext') !== '1') G.getExtension('OES_element_index_uint');
const PROBE = QS.get('probe') === '1';
const SKIPMISS = QS.get('skipmiss') === '1';
const FLAT = QS.get('flat') === '1';
const ONLY_FX = QS.get('only');
const FLAT_FS = `precision mediump float; void main(){ gl_FragColor = vec4(0.5,0.5,0.5,1.0); }`;
const FLAT_VS = `attribute vec4 Position; uniform mat4 WVP; void main(){ gl_Position = WVP * Position; }`;""")

# 2. draw loop: only-fx filter, skipmiss, per-draw error probe
old_loop = """  let tris = 0, draws = 0;
  for (const b of batches) {
    const [vsrc, fsrc] = SHADERS_Z[b.fx] || SHADERS_Z.other;
    const P = getProgZ(b.fx + '|' + DEFS_Z[b.fx], DEFS_Z[b.fx] + vsrc, DEFS_Z[b.fx] + fsrc);"""
assert old_loop in s, 'loop anchor missing'
s = s.replace(old_loop, """  let tris = 0, draws = 0;
  for (const b of batches) {
    if (ONLY_FX && b.fx !== ONLY_FX) continue;
    const [vsrc, fsrc0] = SHADERS_Z[b.fx] || SHADERS_Z.other;
    let fsrc = fsrc0, modeKey = '';
    if (FLAT) {
      modeKey = '|flat';
      fsrc = fsrc0.replace(/void main\\(\\)/g, 'void mainOrig()').replace(/\\s*discard;/g, ' ') +
        '\\nvoid main(){ mainOrig(); gl_FragColor = vec4(0.5,0.5,0.5,1.0); }\\n';
    }
    const P = getProgZ(b.fx + '|' + DEFS_Z[b.fx] + modeKey, DEFS_Z[b.fx] + vsrc, DEFS_Z[b.fx] + fsrc);""")

# 3. after texZget(bn[0]) -> skipmiss
old_tex = "    let unit = 0;\n    const bn = b.bind;\n    const dTex = texZget(bn[0], false);"
assert old_tex in s, 'tex anchor missing'
s = s.replace(old_tex, """    let unit = 0;
    const bn = b.bind;
    const dTex = texZget(bn[0], false);
    if (SKIPMISS && !dTex) { if (PROBE) window.__GLERR.push(['skipmiss:' + b.fx, b.nidx, 0]); continue; }""")

# 4. per-draw probe after drawElements
old_de = """    G.bindBuffer(G.ELEMENT_ARRAY_BUFFER, b.idxBuf);
    G.drawElements(G.TRIANGLES, b.nidx, b.use32 ? G.UNSIGNED_INT : G.UNSIGNED_SHORT, 0);
    tris += b.nidx / 3; draws++;"""
assert old_de in s, 'draw anchor missing'
s = s.replace(old_de, """    G.bindBuffer(G.ELEMENT_ARRAY_BUFFER, b.idxBuf);
    G.drawElements(G.TRIANGLES, b.nidx, b.use32 ? G.UNSIGNED_INT : G.UNSIGNED_SHORT, 0);
    if (PROBE) { const e = G.getError(); if (e) window.__GLERR.push([b.fx, b.nidx, e]); }
    tris += b.nidx / 3; draws++;""")

# 5. painter-mode draw path (inserted just before batches.sort in main)
old_sort = "    batches.sort((a, b) => a.hmean - b.hmean);   // painter-order semantics (s48 ref)"
assert old_sort in s, 'sort anchor missing'
s = s.replace(old_sort, """    if (QS.get('painter') === '1') {
      // global painter order over (triangle mean height, seg, tri), flat color, depth OFF
      const tP0 = performance.now();
      let nvAll = 0, triAll = 0;
      for (const s2 of segInfo) { nvAll += s2.nv; triAll += ((s2.ib / 2) / 3) | 0; }
      const ppos = new Float32Array(nvAll * 4);
      const keys = new Float64Array(triAll);
      const tsi = new Int32Array(triAll);
      const tti = new Int32Array(triAll);
      let vbase = 0, tbase = 0;
      const segIds = [];
      for (let si2 = 0; si2 < segInfo.length; si2++) segIds.push(si2);
      for (const s2 of segInfo) {
        const si2 = segIds.shift();
        for (let v = 0; v < s2.nv; v++) {
          const o = s2.data_off + 4 + v * s2.stride;
          const x = fbuf.getFloat32(o, true), zz = fbuf.getFloat32(o + 4, true);
          const h = fbuf.getFloat32(o + 8, true);
          const o4 = (vbase + v) * 4;
          ppos[o4] = (x - xm) * scale + W / 2;
          ppos[o4 + 1] = (zm - zz) * scale + H / 2;
          ppos[o4 + 2] = h; ppos[o4 + 3] = 1;
        }
        const nidx2 = (s2.ib / 2) | 0;
        for (let t = 0; t + 2 < nidx2; t += 3) {
          const a = u16le(ldd, s2.data_off + 4 + s2.vb + t * 2);
          const bb = u16le(ldd, s2.data_off + 4 + s2.vb + t * 2 + 2);
          const cc = u16le(ldd, s2.data_off + 4 + s2.vb + t * 2 + 4);
          if (a >= s2.nv || bb >= s2.nv || cc >= s2.nv) continue;
          const hmean = (ppos[(vbase + a) * 4 + 2] + ppos[(vbase + bb) * 4 + 2] + ppos[(vbase + cc) * 4 + 2]) / 3;
          keys[tbase] = hmean; tsi[tbase] = si2; tti[tbase] = t; tbase++;
        }
        s2.vbase = vbase; vbase += s2.nv;
      }
      const order2 = Array.from({ length: tbase }, (_, i) => i);
      order2.sort((p, q) => keys[p] - keys[q] || tsi[p] - tsi[q] || tti[p] - tti[q]);
      const pidx = new Uint32Array(tbase * 3);
      for (let i = 0; i < tbase; i++) {
        const gi = order2[i];
        const s2 = segInfo[tsi[gi]];
        const t = tti[gi];
        pidx[i * 3] = s2.vbase + u16le(ldd, s2.data_off + 4 + s2.vb + t * 2);
        pidx[i * 3 + 1] = s2.vbase + u16le(ldd, s2.data_off + 4 + s2.vb + t * 2 + 2);
        pidx[i * 3 + 2] = s2.vbase + u16le(ldd, s2.data_off + 4 + s2.vb + t * 2 + 4);
      }
      const pb = G.createBuffer();
      G.bindBuffer(G.ARRAY_BUFFER, pb);
      G.bufferData(G.ARRAY_BUFFER, ppos, G.STATIC_DRAW);
      const pib = G.createBuffer();
      G.bindBuffer(G.ELEMENT_ARRAY_BUFFER, pib);
      G.bufferData(G.ELEMENT_ARRAY_BUFFER, pidx, G.STATIC_DRAW);
      G.viewport(0, 0, W, H);
      G.clearColor(0, 0, 0, 0);
      G.clear(G.COLOR_BUFFER_BIT);
      G.disable(G.DEPTH_TEST);
      const PP = getProgZ('flat|painter', FLAT_VS, FLAT_FS);
      G.useProgram(PP.p);
      G.uniformMatrix4fv(PP.uni.WVP, false, new Float32Array([2/W,0,0,0, 0,2/H,0,0, 0,0,-1/200,0, -1,-1,1,1]));
      const aLoc = PP.attr.Position;
      G.bindBuffer(G.ARRAY_BUFFER, pb);
      G.enableVertexAttribArray(aLoc);
      G.vertexAttribPointer(aLoc, 4, G.FLOAT, false, 0, 0);
      G.bindBuffer(G.ELEMENT_ARRAY_BUFFER, pib);
      G.drawElements(G.TRIANGLES, tbase * 3, G.UNSIGNED_INT, 0);
      const perr = G.getError();
      window.__GLERR.push(['painter', tbase, perr]);
      const buf2 = new Uint8Array(W * H * 4);
      G.readPixels(0, 0, W, H, G.RGBA, G.UNSIGNED_BYTE, buf2);
      window.__GATE.first_image_ms = t_load + (performance.now() - tP0);
      window.__GATE.painter = { tris: tbase, ms: Math.round(performance.now() - tP0) };
      await corrVsRef(buf2);
      window.__GATE.done = true;
      log('PAINTER done: ' + tbase + ' tris in ' + Math.round(performance.now() - tP0) + ' ms, glerr ' + perr);
      return;
    }
""" + old_sort)

# 6. refactor corr into corrVsRef(buf) callable from painter path; replace inline block
old_corr_start = "    // corr vs the s48 reference (flip: GL row0 = bottom)\n    const resp = await fetch('./s48_ref_zone.png');"
assert old_corr_start in s, 'corr anchor missing'
old_corr_block = s[s.index(old_corr_start):s.index("    window.__GLDUMP")]
new_corr_block = """    await corrVsRef(buf);
"""
s = s.replace(old_corr_block, new_corr_block)
# insert corrVsRef function before the change handler
anchor2 = "document.querySelector('#f').addEventListener('change', async (ev) => {"
assert anchor2 in s
s = s.replace(anchor2, """async function corrVsRef(buf) {
  const REFPNG = QS.get('ref') || 's48_ref_zone.png';
  const resp = await fetch('./' + REFPNG);
  const bmp = await createImageBitmap(await resp.blob());
  const cc = document.createElement('canvas');
  cc.width = W; cc.height = H;
  const cx2 = cc.getContext('2d', { willReadFrequently: true });
  cx2.drawImage(bmp, 0, 0);
  const ref = cx2.getImageData(0, 0, W, H).data;
  let sa = 0, sb = 0, saa = 0, sbb = 0, sab = 0;
  const n = W * H;
  for (let i = 0; i < n; i++) {
    const j = i * 4;
    const a = (buf[j] + buf[j + 1] + buf[j + 2]) / 3;
    const bb2 = (ref[i * 4] + ref[i * 4 + 1] + ref[i * 4 + 2]) / 3;
    sa += a; sb += bb2; saa += a * a; sbb += bb2 * bb2; sab += a * bb2;
  }
  const covv = sab / n - (sa / n) * (sb / n);
  const va = saa / n - (sa / n) ** 2, vb2 = sbb / n - (sb / n) ** 2;
  const corr = covv / Math.sqrt(va * vb2);
  window.__GATE.corr = corr;
  window.__GATE.js_mean = sa / n;
  window.__GATE.ref_mean = sb / n;
  window.__GLDUMP = () => { const c = document.createElement('canvas');
    c.width = W; c.height = H;
    const cx3 = c.getContext('2d');
    const flipped = new Uint8ClampedArray(W * H * 4);
    for (let y = 0; y < H; y++)
      flipped.set(buf.subarray(y * W * 4, (y + 1) * W * 4), (H - 1 - y) * W * 4);
    cx3.putImageData(new ImageData(flipped, W, H), 0, 0);
    return c.toDataURL('image/png'); };
  log('corr vs ' + REFPNG + ': ' + corr.toFixed(4) + '  js_mean ' + (sa / n).toFixed(2) + ' ref_mean ' + (sb / n).toFixed(2));
}
""" + anchor2)

# 7. GATE additions at done
old_done = "    window.__GATE.done = true;\n    log('DONE');"
assert old_done in s, 'done anchor'
s = s.replace(old_done, """    window.__GATE.glerr = window.__GLERR;
    window.__GATE.mode = { flat: FLAT, only: ONLY_FX, skipmiss: SKIPMISS,
      ext: QS.get('noext') !== '1', painter: QS.get('painter') === '1' };
    window.__GATE.done = true;
    log('DONE');""")

open(DST, 'w').write(s)
print('written', DST, len(s), 'bytes')
