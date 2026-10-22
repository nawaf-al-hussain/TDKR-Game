#!/usr/bin/env python3
"""s49 T2c z-score: per-pair real |dLM| vs per-perm null means.
Re-uses the checks module by exec-ing it fully (parts a/b rerun; ~2 min)."""
import json
import numpy as np

SRC = '/tmp/my-project/work/TDKR-Game/extraction/re/session49/s49_t2_checks.py'
ns = {'__name__': 't2mod'}
exec(compile(open(SRC).read(), SRC, 'exec'), ns)
seg_mat = ns['seg_mat']
rows = ns['rows']
seg_pos = ns['seg_pos']
tex_member = ns['tex_member']
lm_sample_diff = ns['lm_sample_diff']

import collections
lm_segs = [k for k, m in enumerate(seg_mat) if rows[m][2]]
vmap = collections.defaultdict(list)
for k in lm_segs:
    m = seg_mat[k]
    p = seg_pos(k, m)
    key = lambda q: (round(q[0], 1), round(q[1], 1), round(q[2], 1))
    for vi in range(0, len(p), max(1, len(p)//24)):
        vmap[key(p[vi])].append(k)
pair_list = []
seen = set()
for v, ks in vmap.items():
    for i in range(len(ks)):
        for j in range(i+1, len(ks)):
            a, b = ks[i], ks[j]
            if a == b or (a, b) in seen:
                continue
            seen.add((a, b))
            if rows[seg_mat[a]][2] == rows[seg_mat[b]][2]:
                pair_list.append((a, b))
rng = np.random.default_rng(49)
rng.shuffle(pair_list)
pair_list = pair_list[:120]

lm_mats = [m for m in range(307) if rows[m][2] and tex_member(rows[m][2])]
real = []
for (ka, kb) in pair_list:
    d = lm_sample_diff(ka, kb, {m: rows[m][2] for m in range(307)})
    if d is not None:
        real.append(d)
real = np.array(real)
null_means = []
for it in range(12):
    perm = rng.permutation(len(lm_mats))
    assign = {m: rows[lm_mats[perm[i]]][2] for i, m in enumerate(lm_mats)}
    ds = []
    for (ka, kb) in pair_list:
        d = lm_sample_diff(ka, kb, assign)
        if d is not None:
            ds.append(d)
    null_means.append(float(np.mean(ds)))
nm = np.array(null_means)
z = (real.mean()-nm.mean())/max(nm.std(ddof=1), 1e-9)
print('real mean %.3f (n=%d) | null-perm means %.3f +/- %.3f (n=%d perms) | z = %.2f' %
      (real.mean(), len(real), nm.mean(), nm.std(ddof=1), len(nm), z))
json.dump({'real_mean': float(real.mean()), 'real_vals': real.tolist(),
           'null_means': nm.tolist(), 'z': float(z)},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session49/s49_t2c_z.json', 'w'), indent=1)
print('saved s49_t2c_z.json')
