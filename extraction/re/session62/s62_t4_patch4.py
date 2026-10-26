#!/usr/bin/env python3
"""S62 T4 fix 2 (exposed by staging v2's first live run): s5Begin declared
`const tgt = s5PickEdge();` but the S5REAL staging retargets tgt -> TypeError
'Assignment to constant variable' the moment staging actually fires (v1 never
hit it because its underground probe never fired). const -> let; nothing else."""
PAGE = '/tmp/my-project/work/ghpages_staged_wt/playable/integration_lazy.html'
src = open(PAGE, encoding='utf-8').read()
A = "  const tgt = s5PickEdge();"
assert src.count(A) == 1
src = src.replace(A, "  let tgt = s5PickEdge();   // s62 T4 (patch4): let - REAL staging retargets tgt", 1)
assert src.count("let tgt = s5PickEdge();") == 1
open(PAGE, 'w', encoding='utf-8').write(src)
print('const tgt -> let tgt (s5Begin)')
