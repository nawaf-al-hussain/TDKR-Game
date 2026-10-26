#!/usr/bin/env python3
"""S62 T4 FIX: relocate the REAL-soup re-anchor block BELOW the `const nz` declaration.
The s62_t4_patch.py block referenced `nz` (feet = nz - 0.9) while `const nz` is declared
LATER IN THE SAME BLOCK -> TDZ ReferenceError every glide frame once S5REAL && S5.anchor.
Relocated semantics: the capsule test now runs at the DESTINATION altitude (nz - 0.9,
the step the glide is about to commit) and still BEFORE P.x/P.y/P.z are updated, so the
re-anchor stores the resolved position and P.z stays pre-move (identical to the s60
virtual-wall block). No other behaviour change; flags unchanged (?s5real=1)."""
PAGE = '/tmp/my-project/work/ghpages_staged_wt/playable/integration_lazy.html'
src = open(PAGE, encoding='utf-8').read()
n0 = len(src)

START = "    if (S5REAL && S5.anchor) {"
END_ANCHOR = "    if (S5REAN && S5.anchor && S5.wallHit === null) {"
assert src.count(START) == 1 and src.count(END_ANCHOR) == 1

i0 = src.index(START)
i1 = src.index(END_ANCHOR)
assert i0 < i1
block = src[i0:i1]
assert "const feet = nz - 0.9;" in block and block.rstrip().endswith("}")
# the misplaced block must currently sit BEFORE the nz declaration
inz = src.index("const nz = P.z + S5.vz * dt2;")
assert i1 < inz, "block already relocated?"

# remove the misplaced block
src = src[:i0] + src[i1:]

# relocate: insert AFTER the gz line, BEFORE the P commit line
A_INS = """    const gz = nm_ground(gx, gy, nz + 2.6);
    P.x = gx; P.y = gy; P.z = nz;"""
assert src.count(A_INS) == 1
fixed = block.replace(
    "// s62 T4: REAL soup air collision (blocked = the walker's capsule-vs-soup query",
    "// s62 T4 (relocated by s62_t4_patch2.py: nz TDZ fix) - REAL soup air collision\n"
    "      // (blocked = the walker's capsule-vs-soup query", 1)
assert "const feet = nz - 0.9;" in fixed
src = src.replace(A_INS, """    const gz = nm_ground(gx, gy, nz + 2.6);
""" + fixed + """    P.x = gx; P.y = gy; P.z = nz;""", 1)

# order sanity: the block must now sit AFTER the nz declaration
assert src.index("const feet = nz - 0.9;") > src.index("const nz = P.z + S5.vz * dt2;")
assert src.count("S5REAL") == 4 and src.count("s5real") == 1
assert len(src) != n0
open(PAGE, 'w', encoding='utf-8').write(src)
print('relocated T4 block, delta', len(src) - n0)
