#!/usr/bin/env python3
"""s50 T3: calibrate the lightmap seam-continuity check.
Base check (s49 T2c): adjacent segments sharing vertices, both materials bound to
the SAME lightmap page; statistic = mean |LM texel difference| at shared vertices
under the REAL Coord1 chain; null = permuted material->page assignment (12 draws).
SIGN: real mean BELOW the null mean (z<0) supports the Coord1 binding claim.

Calibrations (brief T3):
  (a) wrong Coord1 chain: sample with Coord0 (the diffuse UV) instead of Coord1
      -> must move toward the null;
  (b) wrong page per material: the permuted-page null itself (12 perms) -> that IS
      the null; additionally a fixed (+37,+0)-texel offset variant;
  (c) coverage: distinct materials/pages/families among the pairs; extend to ALL
      adjacent pairs (no 120 cap)."""
import json, sys, collections
import numpy as np

SRC = '/tmp/my-project/work/TDKR-Game/extraction/re/session49/s49_t2_checks.py'
ns = {'__name__': 't2mod'}
exec(compile(open(SRC).read(), SRC, 'exec'), ns)
seg_mat = ns['seg_mat']
rows = ns['rows']
seg_pos = ns['seg_pos']
seg_uv0 = ns['seg_uv0']
seg_uv1 = ns['seg_uv1']
tex_member = ns['tex_member']
decode_tex = ns['decode_tex']

OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session50/s50_t3_seamcal.json'

lm_segs = [k for k, m in enumerate(seg_mat) if rows[m][2]]
vmap = collections.defaultdict(list)
for k in lm_segs:
    m = seg_mat[k]
    p = seg_pos(k, m)
    key = lambda q: (round(q[0], 1), round(q[1], 1), round(q[2], 1))
    for vi in range(len(p)):
        vmap[key(p[vi])].append(k)
pair_all = []
seen = set()
for v, ks in vmap.items():
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            a, b = ks[i], ks[j]
            if a == b or (a, b) in seen:
                continue
            seen.add((a, b))
            if rows[seg_mat[a]][2] == rows[seg_mat[b]][2] and tex_member(rows[seg_mat[a]][2]):
                pair_all.append((a, b))
print('ALL adjacent same-page pairs:', len(pair_all), '(s49 used a 120-pair cap)')

lm_mats = [m for m in range(307) if rows[m][2] and tex_member(rows[m][2])]
_tcache = {}
def page_rgb(p):
    if p not in _tcache:
        _tcache[p] = decode_tex(p)
    return _tcache[p]

def sample_diff(ka, kb, lm_assign, uvfn, shift=(0, 0)):
    ma, mb = seg_mat[ka], seg_mat[kb]
    pa, la = lm_assign[ma], lm_assign[mb]
    if not pa or not la or pa != la:
        return None
    t = page_rgb(pa)
    uva = uvfn(ka, ma)
    uvb = uvfn(kb, mb)
    if uva is None or uvb is None:
        return None
    pa_pos = seg_pos(ka, ma)
    pb_pos = seg_pos(kb, mb)
    key = lambda q: (round(q[0], 1), round(q[1], 1), round(q[2], 1))
    bmap = {key(q): i for i, q in enumerate(pb_pos)}
    LW, LH = t['w'], t['h']
    lrgb = t['rgb'].astype(np.float32)
    def conv(uv):
        tv = uv * 0.5 + 0.5
        tv = tv.copy()
        tv[:, 1] = 1.0 - tv[:, 1]
        tv[:, 0] = tv[:, 0] + shift[0] / LW
        tv[:, 1] = tv[:, 1] + shift[1] / LH
        return tv
    ta, tb = conv(uva), conv(uvb)
    diffs = []
    for i, q in enumerate(pa_pos):
        j = bmap.get(key(q))
        if j is None:
            continue
        ca = lrgb[int((ta[i, 1]) * LH) % LH, int((ta[i, 0]) * LW) % LW]
        cb = lrgb[int((tb[j, 1]) * LH) % LH, int((tb[j, 0]) * LW) % LW]
        diffs.append(np.abs(ca - cb).mean())
    return float(np.mean(diffs)) if diffs else None

def run_variant(label, uvfn, shift=(0, 0), nperm=12, seed=50):
    rng = np.random.default_rng(seed)
    real = []
    for (ka, kb) in pair_all:
        d = sample_diff(ka, kb, {m: rows[m][2] for m in range(307)}, uvfn, shift)
        if d is not None:
            real.append(d)
    real = np.array(real)
    nulls = []
    for it in range(nperm):
        perm = rng.permutation(len(lm_mats))
        assign = {m: rows[lm_mats[perm[i]]][2] for i, m in enumerate(lm_mats)}
        ds = [d for (ka, kb) in pair_all for d in [sample_diff(ka, kb, assign, uvfn, shift)] if d is not None]
        if ds:
            nulls.append(float(np.mean(ds)))
    nm = np.array(nulls)
    z = (real.mean() - nm.mean()) / max(nm.std(ddof=1), 1e-9)
    print('%-22s real %.2f (n=%d) | null %.2f +/- %.2f | z %+.2f' %
          (label, real.mean(), len(real), nm.mean(), nm.std(ddof=1), z))
    return {'label': label, 'real_mean': float(real.mean()), 'n_real': int(len(real)),
            'null_mean': float(nm.mean()), 'null_std': float(nm.std(ddof=1)),
            'n_perm': int(len(nm)), 'z': float(z)}

out = {}
out['all_real_Coord1'] = run_variant('REAL (Coord1)', seg_uv1)
out['wrong_chain_Coord0'] = run_variant('WRONG chain (Coord0)', seg_uv0)
out['shifted_37tex'] = run_variant('SHIFTED (+37,0 tex)', seg_uv1, shift=(37, 0))

# coverage: distinct materials/pages among the pairs that produced real values
mats_in = collections.Counter()
pages_in = collections.Counter()
fam_in = collections.Counter()
for (ka, kb) in pair_all:
    ma, mb = seg_mat[ka], seg_mat[kb]
    pg = rows[ma][2]
    if tex_member(pg):
        mats_in[ma] += 1; mats_in[mb] += 1
        pages_in[pg] += 1
        fam_in[rows[ma][0] if rows[ma][0] in ('LightMapDC', 'AlphaMasking', 'SimpleAdditive', 'StandardDiffuseDC') else 'other'] += 1
out['coverage'] = {
    'pairs_total': len(pair_all),
    'distinct_materials': len(mats_in),
    'distinct_pages': len(pages_in),
    'top_pages': sorted(pages_in.items(), key=lambda kv: -kv[1])[:8],
    'family_pairs': dict(fam_in)}
print('coverage: %d pairs, %d materials, %d pages, families %s' %
      (len(pair_all), len(mats_in), len(pages_in), dict(fam_in)))
json.dump(out, open(OUT, 'w'), indent=1)
print('saved', OUT)
