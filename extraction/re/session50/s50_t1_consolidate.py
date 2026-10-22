#!/usr/bin/env python3
"""s50 T1: ONE consolidated, idempotent post-processor for the generated
city_bisect.html. Run AFTER s50_t1_make_bisect.py. Accumulated fixes:
  1. flat-wrap discard -> ' ;' (empty statement, legal GLSL)
  2. corrVsRef/__GLDUMP canvas dims (RW/RH from glz) + RW const
  3. depth window clip_z = -2h/350 + 150/350 (h in [-100,250]; was 1-h/200 which
     clipped all h<0 water/shore = 31% of reference coverage)
  4. remove stale pre-refactor GLDUMP + corr log from the main handler
  5. NOLM / LMONLY shader switches (whole LM term -> vec4(1.0))
  6. HP switch: FS mediump vCoord0/vCoord1 -> highp (regex)
  7. MATONLY (?mat=N) per-material draw filter (batches tagged with mid)
  8. camera bbox override (?bb=x0,z0,x1,z1)
  9. mat-73 CPU array dump (__UV73/__POS73/__SEG73NV) for bake verification
"""
p = '/tmp/my-project/work/city_slice_wt/playable/city_bisect.html'
s = open(p).read()

# 1. flat wrap discard fix
s = s.replace(".replace(/\\s*discard;/g, ' ')", ".replace(/\\s*discard;/g, ' ;')")

# 5+6+7. switches: consts after FLAT_FS line
if "const NOLM" not in s:
    a1 = "const FLAT_FS = `precision mediump float; void main(){ gl_FragColor = vec4(0.5,0.5,0.5,1.0); }`;"
    assert a1 in s
    s = s.replace(a1, a1 + "\nconst NOLM = QS.get('nolm') === '1';\nconst LMONLY = QS.get('lmonly') === '1';\nconst HP = QS.get('hp') === '1';\nconst MATONLY = QS.get('mat') ? parseInt(QS.get('mat')) : null;")
    a2 = ("      fsrc = fsrc0.replace(/void main\\(\\)/g, 'void mainOrig()').replace(/\\s*discard;/g, ' ;') +\n"
          "        '\\nvoid main(){ mainOrig(); gl_FragColor = vec4(0.5,0.5,0.5,1.0); }\\n';\n    }")
    assert a2 in s, 'flat block anchor missing'
    s = s.replace(a2, a2 + "\n    if (MATONLY !== null && b.mid !== MATONLY) continue;"
                          "\n    if (NOLM) { modeKey += '|nolm'; fsrc = fsrc.split('texture2D(LightMap, vCoord1) * 2.0').join('vec4(1.0)'); }"
                          "\n    if (LMONLY) { modeKey += '|lmonly'; fsrc = fsrc.split('texture2D(DiffuseMap, vCoord0, LOD_BIAS)').join('vec4(1.0)'); }"
                          "\n    if (HP) { modeKey += '|hp';"
                          "\n      fsrc = fsrc.replace(/varying\\s+mediump\\s+vec2\\s+vCoord0;/g, 'varying highp vec2 vCoord0;');"
                          "\n      fsrc = fsrc.replace(/varying\\s+mediump\\s+vec2\\s+vCoord1;/g, 'varying highp vec2 vCoord1;'); }")

# 7b+9. tag batches with material id + mat73 dump
if 'batches.push({ fx: fxn, mid,' not in s:
    old_push = "    batches.push({ fx: fxn, bind: bind[mid] || ['', ''],"
    assert old_push in s, 'push anchor missing'
    new_push = ("    if (mid === 73) { window.__UV73 = Array.from(uv0.slice(0, 48));"
                " window.__POS73 = Array.from(pos.slice(0, 32));"
                " window.__SEG73NV = segs.map(q => q.nv); }\n"
                "    batches.push({ fx: fxn, mid, bind: bind[mid] || ['', ''],")
    s = s.replace(old_push, new_push)
    assert 'batches.push({ fx: fxn, mid,' in s, 'push retag failed'

# 2. corrVsRef dims
i0 = s.index('async function corrVsRef(buf) {')
i1 = s.index("document.querySelector('#f').addEventListener('change'", i0)
blk = s[i0:i1]
if 'const RW = glz.width' not in blk:
    blk = blk.replace('async function corrVsRef(buf) {',
        'async function corrVsRef(buf) {\n  const RW = glz.width, RH = glz.height;', 1)
for a, b in [
    ('cc.width = W; cc.height = H;', 'cc.width = RW; cc.height = RH;'),
    ('const ref = cx2.getImageData(0, 0, W, H).data;', 'const ref = cx2.getImageData(0, 0, RW, RH).data;'),
    ('const n = W * H;', 'const n = RW * RH;'),
    ('c.width = W; c.height = H;', 'c.width = RW; c.height = RH;'),
    ('new Uint8ClampedArray(W * H * 4)', 'new Uint8ClampedArray(RW * RH * 4)'),
    ('for (let y = 0; y < H; y++)', 'for (let y = 0; y < RH; y++)'),
    ('buf.subarray(y * W * 4, (y + 1) * W * 4)', 'buf.subarray(y * RW * 4, (y + 1) * RW * 4)'),
    ('(H - 1 - y) * W * 4', '(RH - 1 - y) * RW * 4'),
    ('putImageData(new ImageData(flipped, W, H)', 'putImageData(new ImageData(flipped, RW, RH)'),
]:
    blk = blk.replace(a, b)
s = s[:i0] + blk + s[i1:]

# 8. camera bbox override (before scale computation)
if 'const BBP' not in s:
    old_bb = "    const scale = Math.min(W/(x1-x0), H/(z1-z0));"
    assert old_bb in s, 'scale anchor missing'
    s = s.replace(old_bb,
        "    const BBP = QS.get('bb');\n"
        "    if (BBP) { const bv = BBP.split(',').map(Number); x0 = bv[0]; z0 = bv[1]; x1 = bv[2]; z1 = bv[3]; }\n"
        + old_bb)

# 3. depth window
s = s.replace('0, 0, -1/200, 0,\n      -1, -1, 1, 1,', '0, 0, -2/350, 0,\n      -1, -1, 150/350, 1,')
s = s.replace('new Float32Array([2/W,0,0,0, 0,2/H,0,0, 0,0,-1/200,0, -1,-1,1,1])',
              'new Float32Array([2/W,0,0,0, 0,2/H,0,0, 0,0,-2/350,0, -1,-1,150/350,1])')

# 4. stale block
start_marker = "    window.__GLDUMP = () => { const c = document.createElement('canvas');\n      c.width = W; c.height = H;"
i = s.find(start_marker)
if i >= 0:
    end_marker = "        ' ref_mean ' + (sb/n).toFixed(2));\n"
    j = s.index(end_marker, i) + len(end_marker)
    s = s[:i] + s[j:]
    print('removed stale block')

# 10. ?grad=1 UV-gradient probe (page level)
if "window.__GRAD73 = gt;" not in s:
    a_uv = "if (mid === 73) { window.__UV73"
    assert a_uv in s, 'page uv73 anchor'
    grad_gen = (
        "if (QS.get('grad') === '1' && mid === 73 && !window.__GRAD73) {"
        " const gw = 512, gh = 512; const garr = new Uint8Array(gw * gh * 4);"
        " for (let y = 0; y < gh; y++) for (let x = 0; x < gw; x++) {"
        " const o = (y * gw + x) * 4; garr[o] = Math.min(255, x * 2);"
        " garr[o + 1] = Math.min(255, y * 2); garr[o + 2] = 0; garr[o + 3] = 255; }"
        " const gt = G.createTexture(); G.bindTexture(G.TEXTURE_2D, gt);"
        " G.texImage2D(G.TEXTURE_2D, 0, G.RGBA, gw, gh, 0, G.RGBA, G.UNSIGNED_BYTE, garr);"
        " G.texParameteri(G.TEXTURE_2D, G.TEXTURE_WRAP_S, G.REPEAT);"
        " G.texParameteri(G.TEXTURE_2D, G.TEXTURE_WRAP_T, G.REPEAT);"
        " G.texParameteri(G.TEXTURE_2D, G.TEXTURE_MIN_FILTER, G.NEAREST);"
        " G.texParameteri(G.TEXTURE_2D, G.TEXTURE_MAG_FILTER, G.NEAREST);"
        " window.__GRAD73 = gt; }\n    " + a_uv)
    s = s.replace(a_uv, grad_gen, 1)
    a_bind = "if (dTex && P.uni.DiffuseMap !== undefined && P.uni.DiffuseMap) {\n      G.activeTexture(G.TEXTURE0); G.bindTexture(G.TEXTURE_2D, dTex.tx);"
    assert a_bind in s, 'page diffuse bind anchor'
    s = s.replace(a_bind,
        "if (dTex && P.uni.DiffuseMap !== undefined && P.uni.DiffuseMap) {\n"
        "      G.activeTexture(G.TEXTURE0); G.bindTexture(G.TEXTURE_2D,"
        " (QS.get('grad') === '1' && b.mid === 73 && window.__GRAD73) ? window.__GRAD73 : dTex.tx);")

open(p, 'w').write(s)
assert '-1/200' not in s, 'stale depth window remains'
assert ".replace(/\\s*discard;/g, ' ')" not in s, 'stale discard wrap remains'
assert 'const RW = glz.width' in s, 'RW const missing'
assert 'const NOLM' in s and 'const LMONLY' in s and 'const HP' in s, 'switches missing'
assert 'b.mid !== MATONLY' in s and 'batches.push({ fx: fxn, mid,' in s, 'mat filter missing'
assert 'bind: bind[mid]' in s and 'bindid' not in s, 'bind literal corrupted'
assert 'window.__UV73' in s, 'uv dump missing'
print('city_bisect.html consolidated OK')
