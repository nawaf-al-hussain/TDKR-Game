#!/usr/bin/env python3
"""Add ?grad=1 UV-gradient probe to consolidate.py (page-level transforms only)."""
p = '/tmp/my-project/work/TDKR-Game/extraction/re/session50/s50_t1_consolidate.py'
s = open(p).read()
import ast
if '__GRAD73' not in s:
    anchor = "    open(p, 'w').write(s)\n    assert 'b.mid !== MATONLY' in s"
    # insert two new page-level steps just before the final write block
    old = "# 8. camera bbox override (before scale computation)"
    new = """# 7c. ?grad=1: synthetic UV-gradient texture for the mat-73 batch
if 'const BBP' not in s:
    pass
s = s.replace("OPENPAREN_GRAD", "OPENPAREN_GRAD")  # no-op keeps structure

# 8. camera bbox override (before scale computation)"""
    assert old in s, 'step8 anchor'
    # We add the grad steps at the END (before final write) to run after step 9 inserted __UV73 text.
    tail_anchor = "open(p, 'w').write(s)\nassert '-1/200' not in s"
    assert tail_anchor in s, 'tail anchor'
    grad_code = '''# 10. ?grad=1 UV-gradient probe (page level)
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
        " window.__GRAD73 = gt; }\\n    " + a_uv)
    s = s.replace(a_uv, grad_gen, 1)
    a_bind = "if (dTex && P.uni.DiffuseMap !== undefined && P.uni.DiffuseMap) {\\n      G.activeTexture(G.TEXTURE0); G.bindTexture(G.TEXTURE_2D, dTex.tx);"
    assert a_bind in s, 'page diffuse bind anchor'
    s = s.replace(a_bind,
        "if (dTex && P.uni.DiffuseMap !== undefined && P.uni.DiffuseMap) {\\n"
        "      G.activeTexture(G.TEXTURE0); G.bindTexture(G.TEXTURE_2D,"
        " (QS.get('grad') === '1' && b.mid === 73 && window.__GRAD73) ? window.__GRAD73 : dTex.tx);")

'''
    s = s.replace(tail_anchor, grad_code + tail_anchor, 1)
    open(p, 'w').write(s)
    print('grad probe added to consolidate')
else:
    print('already present')
ast.parse(open(p).read())
print('syntax OK')
