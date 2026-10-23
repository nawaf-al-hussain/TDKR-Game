#!/usr/bin/env python3
"""s52 T2: seam-check estimator, fully written out and swept.

SIGN CONVENTION (declared before reading results):
  z = (real_mean - null_mean) / null_std(ddof=1). z < 0 SUPPORTS the real Coord1
  binding (real shared-vertex lightmap seams differ LESS than permuted pages).

Estimator (exact):
  pair construction: for every segment pair of materials whose LightMap resolves to
  an existing texture page: IF the two segments share a vertex position under the
  given key AND their real pages are equal -> pair. Statistic per pair: mean over
  shared (key-matched) vertex pairs of |page_rgb[a] - page_rgb[b]| (RGB mean),
  sampled with the Coord1 chain uv*0.5+0.5, v flipped, REPEAT wrap, NEAREST texel.
  real: assignment = compiled table. null: permutation of material->page over all
  resolvable-page materials (rng(seed).permutation), nperm draws; z from perm mean/std.

Variants swept:
  K_dec1   vertex key = round(q, 1) decimals            (s50 exact pairing, seed 50)
  K_g0.1   vertex key = grid round(x/eps)*eps, eps=0.1  (s51 exact pairing, seed 51)
  K_g0.5   grid eps=0.5                                 (tolerance variant)
  K_g1.0   grid eps=1.0                                 (tolerance variant)
  K_exact  exact float32 key (no tolerance)
Calibrations per variant (must move toward 0 for the variant to count):
  WRONG chain (Coord0 instead of Coord1), SHIFTED (+37,0 texels).
Per-family + per-page (real mean, per-page z) + leave-nothing/global; range verdict.
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

OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session52/s52_t2_estimator.json'

lm_mats = [m for m in range(307) if rows[m][2] and tex_member(rows[m][2])]
_tcache = {}
def page_rgb(p):
    if p not in _tcache:
        _tcache[p] = decode_tex(p)
    return _tcache[p]

def make_key(kind, eps=0.1):
    if kind == 'dec':
        return lambda q: (round(q[0], 1), round(q[1], 1), round(q[2], 1))
    if kind == 'grid':
        return lambda q: (round(q[0] / eps) * eps, round(q[1] / eps) * eps, round(q[2] / eps) * eps)
    return lambda q: (float(q[0]), float(q[1]), float(q[2]))

def build_pairs(keyfn):
    vmap = collections.defaultdict(list)
    lm_segs = [k for k, m in enumerate(seg_mat) if rows[m][2]]
    for k in lm_segs:
        m = seg_mat[k]
        p = seg_pos(k, m)
        for vi in range(len(p)):
            vmap[keyfn(p[vi])].append(k)
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

def sample_diff(ka, kb, lm_assign, uvfn, shift, keyfn):
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
    bmap = {keyfn(q): i for i, q in enumerate(pb_pos)}
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
        j = bmap.get(keyfn(q))
        if j is None:
            continue
        ca = lrgb[int((ta[i, 1]) * LH) % LH, int((ta[i, 0]) * LW) % LW]
        cb = lrgb[int((tb[j, 1]) * LH) % LH, int((tb[j, 0]) * LW) % LW]
        diffs.append(np.abs(ca - cb).mean())
    return float(np.mean(diffs)) if diffs else None

def run_variant(pairs, keyfn, uvfn, shift=(0, 0), nperm=16, seed=50):
    rng = np.random.default_rng(seed)
    real_v = []
    for p_ in pairs:
        d = sample_diff(p_[0], p_[1], {m: rows[m][2] for m in range(307)}, uvfn, shift, keyfn)
        if d is not None:
            real_v.append(d)
    if len(real_v) < 10:
        return {'n_real': len(real_v), 'skip': 'fewer than 10 productive pairs'}
    real = np.array(real_v)
    nulls = []
    for it in range(nperm):
        perm = rng.permutation(len(lm_mats))
        assign = {m: rows[lm_mats[perm[i]]][2] for i, m in enumerate(lm_mats)}
        ds = [d for p_ in pairs for d in [sample_diff(p_[0], p_[1], assign, uvfn, shift, keyfn)] if d is not None]
        if ds:
            nulls.append(float(np.mean(ds))
                         )
    nm = np.array(nulls)
    z = (real.mean() - nm.mean()) / max(nm.std(ddof=1), 1e-9)
    return {'real_mean': float(real.mean()), 'n_real': int(len(real)),
            'null_mean': float(nm.mean()), 'null_std': float(nm.std(ddof=1)),
            'n_perm': int(len(nm)), 'z': float(z)}

# per-page z: for pairs whose REAL page is p, mean real vs per-perm mean (perm-assigned)
def page_stats(pairs, keyfn, uvfn, nperm=12, seed=50):
    rng = np.random.default_rng(seed)
    by_page = collections.defaultdict(list)
    real_assign = {m: rows[m][2] for m in range(307)}
    for p_ in pairs:
        d = sample_diff(p_[0], p_[1], real_assign, uvfn, (0, 0), keyfn)
        if d is not None:
            pg = rows[seg_mat[p_[0]]][2]
            by_page[pg].append((p_, d))
    outp = {}
    perms = []
    for it in range(nperm):
        perm = rng.permutation(len(lm_mats))
        perms.append({m: rows[lm_mats[perm[i]]][2] for i, m in enumerate(lm_mats)})
    for pg, pds in by_page.items():
        pr = [d for _, d in pds]
        nulls = []
        for assign in perms:
            ds = [d for p_ in (x[0] for x in pds)
                  for d in [sample_diff(p_[0], p_[1], assign, uvfn, (0, 0), keyfn)] if d is not None]
            if ds:
                nulls.append(float(np.mean(ds)))
        if len(nulls) >= 4:
            nm = np.array(nulls)
            outp[pg] = {'n_pairs': len(pr), 'real_mean': float(np.mean(pr)),
                        'null_mean': float(nm.mean()), 'null_std': float(nm.std(ddof=1)),
                        'z': float((np.mean(pr) - nm.mean()) / max(nm.std(ddof=1), 1e-9))}
    return outp

VARIANTS = [('K_dec1', make_key('dec'), 50), ('K_g0.1', make_key('grid', 0.1), 51),
            ('K_g0.5', make_key('grid', 0.5), 52), ('K_g1.0', make_key('grid', 1.0), 53),
            ('K_exact', make_key('exact'), 54)]
out = {}
for name, keyfn, seed in VARIANTS:
    pairs = build_pairs(keyfn)
    print('%s: %d pairs' % (name, len(pairs)), flush=True)
    ent = {'pairs': len(pairs)}
    ent['REAL_Coord1'] = run_variant(pairs, keyfn, seg_uv1, nperm=16, seed=seed)
    ent['WRONG_Coord0'] = run_variant(pairs, keyfn, seg_uv0, nperm=12, seed=seed + 100)
    ent['SHIFTED_37'] = run_variant(pairs, keyfn, seg_uv1, shift=(37, 0), nperm=12, seed=seed + 200)
    ent['REAL_Coord1_seed2'] = run_variant(pairs, keyfn, seg_uv1, nperm=16, seed=seed + 7)
    out[name] = ent
    print('  real z=%s | wrong z=%s | shift z=%s' %
          (ent['REAL_Coord1'].get('z'), ent['WRONG_Coord0'].get('z'), ent['SHIFTED_37'].get('z')), flush=True)

# per-family for the two historical pairings + per-page for grid0.1 and dec1
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
    fam_of[i] = eff[1:].split('-fx')[0] if eff.startswith('#') else 'none'

KEYLOOK = {n: k for n, k, _ in VARIANTS}
for name in ('K_dec1', 'K_g0.1', 'K_g0.5', 'K_g1.0'):
    keyfn = KEYLOOK[name]
    pairs = build_pairs(keyfn)
    for fam in ('LightMapDC', 'AlphaMasking', 'LightmapVCBlendDC'):
        fp = [p_ for p_ in pairs if fam_of[seg_mat[p_[0]]] == fam_of[seg_mat[p_[1]]] == fam]
        if len(fp) < 10:
            continue
        r = run_variant(fp, keyfn, seg_uv1, nperm=12, seed=60)
        out.setdefault(name, {})['fam_%s' % fam] = r
        print('%s fam %s: n=%s z=%s' % (name, fam, r.get('n_real'), r.get('z')), flush=True)
    if name in ('K_dec1', 'K_g0.1'):
        ps = page_stats(pairs, keyfn, seg_uv1, nperm=12, seed=61)
        out[name]['per_page'] = ps
        print('%s per-page z: %s' % (name, {k: round(v['z'], 2) for k, v in sorted(ps.items())}), flush=True)

json.dump(out, open(OUT, 'w'), indent=1)
print('saved', OUT)
