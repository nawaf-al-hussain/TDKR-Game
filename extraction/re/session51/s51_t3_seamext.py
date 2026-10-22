#!/usr/bin/env python3
"""s51 T3: seam check EXTENDED to LightMapDC/AlphaMasking families via relaxed adjacency.
Sign convention (declared BEFORE reading results): z = (real_mean - null_mean)/null_std;
z < 0 supports the real Coord1 binding (real seams lighter-diff than permuted pages).
Adjacency relaxation: vertex keys rounded to eps in {0.1 (s50 baseline), 0.5, 1.0}.
Calibrations per family+eps: wrong chain (Coord0) must move toward 0; shifted page
(+37,0 texels) must also move toward 0. If a family adds no power -> 'weakly supportive', stop.
"""
import json, collections
import numpy as np

SRC = '/tmp/my-project/work/TDKR-Game/extraction/re/session49/s49_t2_checks.py'
ns = {'__name__': 't3mod'}
exec(compile(open(SRC).read(), SRC, 'exec'), ns)
seg_mat = ns['seg_mat']
rows = ns['rows']
seg_pos = ns['seg_pos']
seg_uv0 = ns['seg_uv0']
seg_uv1 = ns['seg_uv1']
tex_member = ns['tex_member']
decode_tex = ns['decode_tex']

# family from the compiled table effect URL (independent parse, same as s50 pyref)
import zipfile, io
BDAE = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
LE = zipfile.ZipFile(io.BytesIO(open(BDAE, 'rb').read())).read('little_endian_not_quantized.bdae')
NB = len(LE)
w32 = np.frombuffer(LE, '<u4', NB // 4)
def cstr(off, maxn=96):
    if not (0 < off < NB): return None
    e = int(LE.find(b'\0', off))
    if e < 0 or e == off or e - off > maxn: return None
    try: t = LE[off:e].decode('ascii')
    except Exception: return None
    return t if all(32 <= ord(c) < 127 for c in t) else None
fam_of = {}
for i in range(307):
    a = 0x5fea0 + i * 36
    ws = [int(w32[(a + k * 4) // 4]) for k in range(9)]
    eff = cstr(ws[3]) or ''
    fam = eff[1:].split('-fx')[0] if eff.startswith('#') else 'none'
    fam_of[i] = fam
print('families:', collections.Counter(fam_of[m] for m in range(307) if rows[m][2] and tex_member(rows[m][2])))

lm_mats = [m for m in range(307) if rows[m][2] and tex_member(rows[m][2])]
_tcache = {}
def page_rgb(p):
    if p not in _tcache:
        _tcache[p] = decode_tex(p)
    return _tcache[p]

def build_pairs(eps):
    q = lambda x: round(x / eps) * eps
    vmap = collections.defaultdict(list)
    lm_segs = [k for k, m in enumerate(seg_mat) if rows[m][2]]
    for k in lm_segs:
        m = seg_mat[k]
        p = seg_pos(k, m)
        for vi in range(len(p)):
            vmap[(q(p[vi][0]), q(p[vi][1]), q(p[vi][2]))].append(k)
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
    return pair_all

def sample_diff(ka, kb, lm_assign, uvfn, shift, eps):
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
    q = lambda x: round(x / eps) * eps
    bmap = {(q(r[0]), q(r[1]), q(r[2])): i for i, r in enumerate(pb_pos)}
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
    for i, rr in enumerate(pa_pos):
        j = bmap.get((q(rr[0]), q(rr[1]), q(rr[2])))
        if j is None:
            continue
        ca = lrgb[int((ta[i, 1]) * LH) % LH, int((ta[i, 0]) * LW) % LW]
        cb = lrgb[int((tb[j, 1]) * LH) % LH, int((tb[j, 0]) * LW) % LW]
        diffs.append(np.abs(ca - cb).mean())
    return float(np.mean(diffs)) if diffs else None

def run_variant(pairs, uvfn, shift=(0, 0), nperm=12, seed=51):
    rng = np.random.default_rng(seed)
    real = [d for p_ in pairs for d in [sample_diff(p_[0], p_[1], {m: rows[m][2] for m in range(307)}, uvfn, shift, EPS) ] if d is not None]
    if len(real) < 10:
        return {'n_real': len(real), 'skip': 'fewer than 10 productive pairs'}
    real = np.array(real)
    nulls = []
    for it in range(nperm):
        perm = rng.permutation(len(lm_mats))
        assign = {m: rows[lm_mats[perm[i]]][2] for i, m in enumerate(lm_mats)}
        ds = [d for p_ in pairs for d in [sample_diff(p_[0], p_[1], assign, uvfn, shift, EPS)] if d is not None]
        if ds:
            nulls.append(float(np.mean(ds)))
    nm = np.array(nulls)
    z = (real.mean() - nm.mean()) / max(nm.std(ddof=1), 1e-9)
    print('  real %.2f (n=%d) | null %.2f +/- %.2f | z %+.2f' %
          (real.mean(), len(real), nm.mean(), nm.std(ddof=1), z))
    return {'real_mean': float(real.mean()), 'n_real': int(len(real)),
            'null_mean': float(nm.mean()), 'null_std': float(nm.std(ddof=1)),
            'n_perm': int(len(nm)), 'z': float(z)}

out = {}
for EPS in (0.1, 0.5, 1.0):
    pairs = build_pairs(EPS)
    fams = collections.Counter()
    for (a, b) in pairs:
        fa, fb = fam_of[seg_mat[a]], fam_of[seg_mat[b]]
        fams[fa if fa == fb else 'mixed'] += 1
    print('eps=%.2f pairs=%d by family: %s' % (EPS, len(pairs), dict(fams)))
    ekey = 'eps_%s' % EPS
    out[ekey] = {'pairs_total': len(pairs), 'by_family': dict(fams)}
    for fam in ('LightMapDC', 'AlphaMasking', 'LightmapVCBlendDC'):
        fpairs = [p_ for p_ in pairs if fam_of[seg_mat[p_[0]]] == fam_of[seg_mat[p_[1]]] == fam]
        if not fpairs:
            continue
        print('  fam %s eps %.2f: %d pairs' % (fam, EPS, len(fpairs)))
        key = '%s__fam_%s' % (ekey, fam)
        out[key] = {
            'REAL_Coord1': run_variant(fpairs, seg_uv1),
            'WRONG_Coord0': run_variant(fpairs, seg_uv0),
            'SHIFTED_37': run_variant(fpairs, seg_uv1, shift=(37, 0)),
        }
json.dump(out, open('/tmp/my-project/work/TDKR-Game/extraction/re/session51/s51_t3_seamext.json', 'w'), indent=1)
print('saved s51_t3_seamext.json')
