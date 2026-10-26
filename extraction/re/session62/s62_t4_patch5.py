#!/usr/bin/env python3
"""S62 T4 patch5: expose s5 provenance for gate introspection (S5/P are module-scoped,
playwright can only read window.*). Two additions:
1. s5Begin records window.__S5DBG = { from, tgt, wpsN } AFTER staging (live snapshot).
2. the landing/timeout s5 gate objects gain from/tgt/wpsN (provenance of the pick).
No behaviour change."""
PAGE = '/tmp/my-project/work/ghpages_staged_wt/playable/integration_lazy.html'
src = open(PAGE, encoding='utf-8').read()
n0 = len(src)

A1 = "  S5.tgt = tgt; S5.t0 = performance.now();"
assert src.count(A1) == 1
src = src.replace(A1, """  S5.tgt = tgt; S5.t0 = performance.now();
  window.__S5DBG = { from: S5.from.slice(), tgt: tgt.slice(), wpsN: (window.__S5WPS || []).length };   // s62 T4 patch5""", 1)

A2 = "                 realStaged: S5.realStaged || null, real: !!S5REAL };"
assert src.count(A2) == 1
src = src.replace(A2, """                 realStaged: S5.realStaged || null, real: !!S5REAL,
                 from: S5.from.slice(), tgt: S5.tgt.slice(), wpsN: (window.__S5WPS || []).length };""", 1)

A3 = "glideClipActive: S5.clipActive, landed: false, error: 'glide timeout', traj: S5.traj };"
assert src.count(A3) == 1
src = src.replace(A3, "glideClipActive: S5.clipActive, landed: false, error: 'glide timeout', traj: S5.traj,\n               from: S5.from.slice(), tgt: S5.tgt.slice(), wpsN: (window.__S5WPS || []).length };", 1)

assert len(src) != n0
open(PAGE, 'w', encoding='utf-8').write(src)
print('patch5 applied, delta', len(src) - n0)
