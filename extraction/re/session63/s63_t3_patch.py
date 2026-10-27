#!/usr/bin/env python3
"""S63 T3 patch: ?s5air=N - mid-air glide start (the grapple anchor is ELEVATED by N u).
The s62 real re-anchor case starts ON the ledge (blend never decays before the hit);
?s5air=N starts the glide N u ABOVE the anchor so the glide crosses facades/ground at a
DECAYED blend (non-zero blend travel before the hit) - the second real re-anchor case.
Generator edits playable/integration_lazy.html on the staged worktree (s56-t1-glide).
Asserts single-match per replacement (project discipline)."""
P = '/tmp/my-project/work/ghpages_staged_wt/playable/integration_lazy.html'
src = open(P, encoding='utf-8').read()

def rep1(old, new):
    global src
    n = src.count(old)
    assert n == 1, 'expected 1 match, got %d for: %r' % (n, old[:80])
    src = src.replace(old, new)

# 1. flag
rep1("const S5REAL = QS2.get('s5real') === '1';   // s62 T4: REAL soup air-collision re-anchor",
     "const S5REAL = QS2.get('s5real') === '1';   // s62 T4: REAL soup air-collision re-anchor\n"
     "const S5AIR = parseFloat(QS2.get('s5air') || '0') || 0;   // s63 T3: mid-air glide start (elevated grapple anchor)")

# 2. elevated takeoff (after the ledge ground-snap, BEFORE the anchor is taken)
rep1("      const gz0 = nm_ground(S5.tgt[0], S5.tgt[1], S5.tgt[2] + 2.6);\n"
     "      if (gz0 > -1e8) { P.z = gz0 + 0.9; }",
     "      const gz0 = nm_ground(S5.tgt[0], S5.tgt[1], S5.tgt[2] + 2.6);\n"
     "      if (gz0 > -1e8) { P.z = gz0 + 0.9; }\n"
     "      if (S5AIR > 0) { P.z += S5AIR; }   // s63 T3: grapple-elevated anchor - glide starts N u mid-air")

# 3. provenance on both finalize paths
rep1("realStaged: S5.realStaged || null, real: !!S5REAL,",
     "realStaged: S5.realStaged || null, real: !!S5REAL, s5air: S5AIR,")
rep1("realStaged: S5.realStaged || null };",
     "realStaged: S5.realStaged || null, s5air: S5AIR };")

open(P, 'w', encoding='utf-8').write(src)
print('patched OK')
