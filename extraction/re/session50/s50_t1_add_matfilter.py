#!/usr/bin/env python3
"""Add ?mat= filter capability to s50_t1_consolidate.py: new page-level replacements."""
p = '/tmp/my-project/work/TDKR-Game/extraction/re/session50/s50_t1_consolidate.py'
s = open(p).read()

if 'MATONLY' not in s:
    old = "const NOLM = QS.get('nolm') === '1';"
    new = ("const NOLM = QS.get('nolm') === '1';\n"
           "const MATONLY = QS.get('mat') ? parseInt(QS.get('mat')) : null;")
    assert old in s, 'nolm const anchor'
    s = s.replace(old, new, 1)

    old2 = "    if (NOLM) { modeKey += '|nolm';"
    new2 = ("    if (MATONLY !== null && b.mid !== MATONLY) continue;\n"
            "    if (NOLM) { modeKey += '|nolm';")
    assert old2 in s, 'nolm use anchor'
    s = s.replace(old2, new2, 1)

    # page-level: tag batches with mid (insert as a new step after depth-window fix)
    anchor = "# 4. stale block"
    assert anchor in s, 'step-4 anchor'
    s = s.replace(anchor, """# 3b. tag batches with material id + per-material draw filter
s = s.replace("    batches.push({ fx: fxn, bind: bind[mid] || ['', ''],",
              "    batches.push({ fx: fxn, mid, bind: bind[mid] || ['', ''],")

# 4. stale block""", 1)

    old4 = "assert 'const NOLM' in s and 'const LMONLY' in s and 'const HP' in s, 'switches missing'"
    new4 = old4 + "\nassert 'MATONLY' in s and 'b.mid !== MATONLY' in s, 'mat filter missing'"
    assert old4 in s, 'assert anchor'
    s = s.replace(old4, new4, 1)
    open(p, 'w').write(s)
    print('consolidate.py updated with mat filter')
else:
    print('already present')
import ast
ast.parse(open(p).read())
print('syntax OK')
