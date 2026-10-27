#!/usr/bin/env python3
"""S64 T2 patch: add ?s5airto=<ms> glide phase-timeout override (default 6000 unchanged).
Three edits, each with a single-match assert + file-changed assert."""
import re, sys

P = '/tmp/my-project/work/ghpages_staged_wt/playable/integration_lazy.html'
src = open(P, 'r', encoding='utf-8').read()
orig = src

# 1. const next to S5AIR
old1 = "const S5AIR = parseFloat(QS2.get('s5air') || '0') || 0;   // s63 T3: mid-air glide start (elevated grapple anchor)"
new1 = old1 + "\nconst S5AIRTO = parseFloat(QS2.get('s5airto') || '0') || 0;   // s64 T2: glide phase timeout override (0 = engine-default 6000)"
assert src.count(old1) == 1, 'anchor1 count %d' % src.count(old1)
src = src.replace(old1, new1)

# 2. timeout use
old2 = "if (now - S5.tGlide > 6000 && !S5.landed) {   // safety: never stall the gate"
new2 = "if (now - S5.tGlide > (S5AIRTO || 6000) && !S5.landed) {   // safety: never stall the gate (s64 T2: ?s5airto override)"
assert src.count(old2) == 1, 'anchor2 count %d' % src.count(old2)
src = src.replace(old2, new2)

# 3. provenance on the timeout receipt
old3 = "realStaged: S5.realStaged || null, s5air: S5AIR };"
new3 = "realStaged: S5.realStaged || null, s5air: S5AIR, s5airto: S5AIRTO || 0 };"
assert src.count(old3) == 1, 'anchor3 count %d' % src.count(old3)
src = src.replace(old3, new3)

assert src != orig
open(P, 'w', encoding='utf-8').write(src)
print('patched: 3 edits applied')
