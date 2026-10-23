#!/usr/bin/env python3
"""s53 T2: A0 anti-signal investigation (page BakeGroup_Island1_A0.tga, z=+1.85 in s52 K_dec1).

SIGN CONVENTION (declared before reading results):
  z = (real_mean - null_mean) / null_std(ddof=1); z < 0 SUPPORTS the real Coord1
  binding (real shared-vertex seams differ LESS than page-permuted nulls).
  z > 0 = anti-signal (real seams differ MORE than nulls).

Questions (from the brief):
  Q1 which materials/segments form the A0 pairs, and their effect families
  Q2 their lightmap chain: Coord1 scale/offset (census says identity; zone corr
     0.9923 vs the identity-chain CPU model is the second signal) and the TC1
     bounding box of each paired segment (atlas-region sanity)
  Q3 are A0 pairs mostly CROSS-effect pairs (different fx URLs)?
  Q4 is the check VALID on A0 (atlas-border discontinuities at NEAREST wrap)?
Subsets:
  same_fx vs cross_fx; sample near the segment's own TC1 bbox edge (<=2 texels)
  vs interior. Corrected page z = same_fx AND interior subset (valid seams).
Calibration (must move): WRONG chain (Coord0) and SHIFTED (+37,0) on each subset.
"""
import json, collections, io, zipfile, struct
import numpy as np

SRC = '/tmp/my-project/work/TDKR-Game/extraction/re/session49/s49_t2_checks.py'
ns = {'__name__': 't3mod'}
exec(compile(open(SRC).read(), SRC, 'exec'), ns)
seg_mat = ns['seg_mat']; rows = ns['rows']; seg_pos = ns['seg_pos']
seg_uv0 = ns['seg_uv0']; seg_uv1 = ns['seg_uv1']
tex_member = ns['tex_member']; decode_tex = ns['decode_tex']

OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session53/s53_t2_a0.json'
PAGE = 'BakeGroup_Island1_A0.tga'

_tcache = {}
def page_rgb(p):
    if p not in _tcache:
        _tcache[p] = decode_tex(p)
    return _tcache[p]

def make_key(kind, eps=0.1):
    if kind == 'dec':
        return lambda q: (round(q[0], 1), round(q[1], 1), round(q[2], 1))
    return lambda q: (round(q[0] / eps) * eps, round(q[1] / eps) * eps, round(q[2] / eps) * eps)

def build_pairs(keyfn):
    vmap = collections.defaultdict(list)
    lm_segs = [k for k, m in enumerate(seg_mat) if rows[m][2] and tex_member(rows[m][2])]
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

# effect family per material (compiled instance table, same decode as s52 T2)
BDAE = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
LE = zipfile.ZipFile(io.BytesIO(open(BDAE, 'rb').read())).read('little_endian_not_quantized.bdae')
NB = len(LE); w32 = np.frombuffer(LE, '<u4', NB // 4)
def cstr(off, maxn=96):
    if not (0 < off < NB): return None
    e = int(LE.find(b'\0', off))
    if e < 0 or e == off or e - off > maxn: return None
    try: t = LE[off:e].decode('ascii')
    except Exception: return None
    return t if all(32 <= ord(c) < 127 for c in t) else None
def fx_of(mid):
    a = 0x5fea0 + mid * 36
    ws = [int(w32[(a + k * 4) // 4]) for k in range(9)]
    eff = cstr(ws[3]) or ''
    return eff[1:].split('-fx')[0] if eff.startswith('#') else 'none'

def sample_diff(ka, kb, lm_assign, uvfn, shift, keyfn, detail=False):
    ma, mb = seg_mat[ka], seg_mat[kb]
    pa, la = lm_assign[ma], lm_assign[mb]
    if not pa or not la or pa != la:
        return None
    t = page_rgb(pa)
    uva = uvfn(ka, ma); uvb = uvfn(kb, mb)
    if uva is None or uvb is None:
        return None
    pa_pos = seg_pos(ka, ma); pb_pos = seg_pos(kb, mb)
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
        xa = int((ta[i, 0]) * LW) % LW; ya = int((ta[i, 1]) * LH) % LH
        xb = int((tb[j, 0]) * LW) % LW; yb = int((tb[j, 1]) * LH) % LH
        diffs.append(np.abs(lrgb[ya, xa] - lrgb[yb, xb]).mean())
    if not diffs:
        return None
    if detail:
        # TC1 bbox in page texels for both segments; flag edge-straddling samples
        def bbox(tuv):
            x = (tuv[:, 0] * 0.5 + 0.5) * LW
            y = ((tuv[:, 1] * 0.5 + 0.5)) * LH
            y = LH - y  # flip like conv
            return (x.min(), x.max(), y.min(), y.max())
        ba, bb = bbox(uva), bbox(uvb)
        return float(np.mean(diffs)), int(len(diffs)), ba, bb
    return float(np.mean(diffs))

def subset_z(pairs, keyfn, uvfn, shift=(0, 0), nperm=16, seed=70):
    rng = np.random.default_rng(seed)
    real_v = []
    for p_ in pairs:
        d = sample_diff(p_[0], p_[1], {m: rows[m][2] for m in range(307)}, uvfn, shift, keyfn)
        if d is not None:
            real_v.append(d)
    if len(real_v) < 8:
        return {'n_real': len(real_v), 'skip': 'fewer than 8 productive pairs'}
    real = np.array(real_v)
    nulls = []
    lm_mats = [m for m in range(307) if rows[m][2] and tex_member(rows[m][2])]
    for it in range(nperm):
        perm = rng.permutation(len(lm_mats))
        assign = {m: rows[lm_mats[perm[i]]][2] for i, m in enumerate(lm_mats)}
        ds = [d for p_ in pairs for d in [sample_diff(p_[0], p_[1], assign, uvfn, shift, keyfn)] if d is not None]
        if ds:
            nulls.append(float(np.mean(ds)))
    nm = np.array(nulls)
    return {'real_mean': float(real.mean()), 'n_real': int(len(real)),
            'null_mean': float(nm.mean()), 'null_std': float(nm.std(ddof=1)),
            'n_perm': int(len(nm)), 'z': float((real.mean() - nm.mean()) / max(nm.std(ddof=1), 1e-9))}

def main():
    out = {'sign_convention': 'z<0 supports real Coord1 binding; z>0 anti-signal'}
    for keyname, keyfn in (('K_dec1', make_key('dec')), ('K_g0.1', make_key('grid', 0.1))):
        pairs = build_pairs(keyfn)
        a0 = [p_ for p_ in pairs if rows[seg_mat[p_[0]]][2] == PAGE]
        ent = {'n_a0_pairs': len(a0)}
        # Q1/Q3: composition
        comp = collections.Counter()
        recs = []
        for (a, b) in a0:
            fa, fb = fx_of(seg_mat[a]), fx_of(seg_mat[b])
            comp['same_fx' if fa == fb else 'cross_fx'] += 1
            comp['fam:%s' % fa] += 1
            recs.append({'mids': [int(seg_mat[a]), int(seg_mat[b])],
                         'fx': [fa, fb], 'same_fx': fa == fb})
        ent['composition'] = dict(comp)
        # Q2: TC1 bbox + per-pair detail with edge flags
        real_assign = {m: rows[m][2] for m in range(307)}
        detail = []
        same_fx, cross_fx = [], []
        for (p_, r) in zip(a0, [None] * len(a0)):
            pass
        for (a, b) in a0:
            d = sample_diff(a, b, real_assign, seg_uv1, (0, 0), keyfn, detail=True)
            if d is None:
                continue
            diff, nsh, ba, bb = d
            fa, fb = fx_of(seg_mat[a]), fx_of(seg_mat[b])
            LW = page_rgb(PAGE)['w']; LH = page_rgb(PAGE)['h']
            def edge_frac(bx):
                x0, x1, y0, y1 = bx
                # fraction of the bbox within 2 texels of the page border
                return ((x0 < 2) + (x1 > LW - 3) + (y0 < 2) + (y1 > LH - 3)) / 4.0
            rec = {'mids': [int(seg_mat[a]), int(seg_mat[b])], 'fx': [fa, fb],
                   'same_fx': fa == fb, 'n_shared': nsh, 'diff': round(diff, 2),
                   'bbox_a': [round(v, 1) for v in ba], 'bbox_b': [round(v, 1) for v in bb],
                   'page_edge_frac_a': round(edge_frac(ba), 2), 'page_edge_frac_b': round(edge_frac(bb), 2)}
            detail.append(rec)
            (same_fx if fa == fb else cross_fx).append((a, b))
        ent['detail'] = detail
        ent['z_same_fx'] = subset_z(same_fx, keyfn, seg_uv1, seed=71)
        ent['z_cross_fx'] = subset_z(cross_fx, keyfn, seg_uv1, seed=72)
        ent['z_all'] = subset_z(a0, keyfn, seg_uv1, seed=73)
        # calibration inside subsets (must move toward 0 / change materially)
        ent['cal_same_fx_wrongchain'] = subset_z(same_fx, keyfn, seg_uv0, seed=74, nperm=10)
        ent['cal_same_fx_shift37'] = subset_z(same_fx, keyfn, seg_uv1, shift=(37, 0), seed=75, nperm=10)
        out[keyname] = ent
        print('%s: A0 pairs=%d same=%d cross=%d z_all=%s z_same=%s z_cross=%s' % (
            keyname, len(a0), len(same_fx), len(cross_fx),
            ent['z_all'].get('z'), ent['z_same_fx'].get('z'), ent['z_cross_fx'].get('z')), flush=True)
    json.dump(out, open(OUT, 'w'), indent=1)
    print('saved', OUT)

if __name__ == '__main__':
    main()
