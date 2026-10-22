#!/usr/bin/env python3
"""Add mat-73 CPU-array dump to s50_t1_consolidate.py (file-based, safe)."""
p = '/tmp/my-project/work/TDKR-Game/extraction/re/session50/s50_t1_consolidate.py'
s = open(p).read()
if '__UV73' not in s:
    old = "    batches.push({ fx: fxn, mid, bind: bind[mid] || ['', ''],"
    new = ("    if (mid === 73) { window.__UV73 = Array.from(uv0.slice(0, 48));"
           " window.__POS73 = Array.from(pos.slice(0, 32));"
           " window.__SEG73NV = segs.map(q => q.nv); }\n"
           "    batches.push({ fx: fxn, mid, bind: bind[mid] || ['', ''],")
    assert old in s, 'push anchor'
    s = s.replace(old, new, 1)
    open(p, 'w').write(s)
    print('uv dump added to consolidate')
else:
    print('already present')
import ast
ast.parse(open(p).read())
print('syntax OK')
