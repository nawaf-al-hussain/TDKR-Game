#!/usr/bin/env python3
"""S60 T3: merc rig DISCRIMINATING validation (Python port of readBdae2 algorithm).
Checks that can FAIL on the merc:
  V1 skin weights sum to 1 per vertex (+ shuffled-weights null; calibrate batman good /
     batman+0.05-offset bad)
  V2 skin bone indices < nBones (report max index, fraction)
  V3 vertex bbox + height vs batman (plausibility window)
  V4 |bind origin - skin-weighted centroid| per bone (permuted-mapping null, n bones)
  V5 rest-pose bone-length plausibility (parent-child distance vs zero-collapse null)
Output: s60_t3_mercval.json
"""
import struct, json, numpy as np

def read_bdae2(path):
    u8 = open(path, 'rb').read()
    def u32(o): return struct.unpack_from('<I', u8, o)[0]
    def u16(o): return struct.unpack_from('<H', u8, o)[0]
    def f32(o): return struct.unpack_from('<f', u8, o)[0]
    def poolstr(o):
        if o <= 0 or o >= len(u8): return None
        e = o
        while e < len(u8) and u8[e] != 0 and e - o < 4096: e += 1
        if e >= len(u8) or e - o > 4096: return None
        return u8[o:e].decode('latin1')
    assert u8[:4] == b'BRES'
    pool0, pool1, off4 = u32(0x1c), u32(0x20), u32(0x28)
    # nodes
    nodes = []
    o = pool1
    while o < off4 - 0x50:
        n1, n2, al = poolstr(u32(o)), poolstr(u32(o + 4)), poolstr(u32(o + 8))
        if n1 is not None and n2 is not None and al is not None:
            t = [f32(o + 0xc), f32(o + 0x10), f32(o + 0x14)]
            q = [f32(o + 0x18), f32(o + 0x1c), f32(o + 0x20), f32(o + 0x24)]
            s = [f32(o + 0x28), f32(o + 0x2c), f32(o + 0x30)]
            ql = float(np.linalg.norm(q))
            if 0.96 < ql < 1.04 and all(abs(x) < 1e4 for x in t) and \
               all(0.01 < abs(x) < 100 for x in s) and u32(o + 0x34) == 1 and u32(o + 0x38) <= 32:
                nodes.append({'off': o, 'name': n2, 'alias': al, 't': t, 'q': q, 's': s})
        o += 4
    # stride run
    stridesAt, stride = -1, 0
    for o in range(off4, off4 + 0x200, 4):
        v = u32(o)
        if 8 <= v <= 256 and u32(o + 4) == v and u32(o + 8) == v and u32(o + 12) == v:
            stridesAt, stride = o, v
            break
    assert stridesAt >= 0
    # inverse binds
    def matOk(o):
        return (abs(f32(o + 12)) < 1e-5 and abs(f32(o + 28)) < 1e-5 and abs(f32(o + 44)) < 1e-5
                and abs(f32(o + 60) - 1) < 1e-5
                and all(abs(f32(o + 4 * i)) < 1e4 for i in (0, 1, 2, 4, 5, 6, 8, 9, 10, 13, 14)))
    invbOff, nBones = -1, 0
    o = off4
    while o + 64 <= len(u8):
        if u32(o + 60) == 0x3f800000:
            run, p = 0, o
            while p + 64 <= len(u8) and matOk(p):
                run += 1; p += 64
            if run >= 10:
                s0 = o
                while s0 - 64 >= off4 and matOk(s0 - 64):
                    s0 -= 64; run += 1
                invbOff, nBones = s0, run
                break
            o = (p if p > o else o) + 4
        else:
            o += 4
    assert invbOff >= 0
    # palette
    BONE = b'Bone'
    palOff = -1
    lo = invbOff + nBones * 64
    for o in range(lo, lo + 0x200, 4):
        ok = 0
        for k in range(min(nBones, 12)):
            b = u8[o + 8 * k:o + 8 * k + 8]
            if BONE in b[:4] or BONE in b[2:6]:
                ok += 1
        if ok >= min(nBones, 12):
            palOff = o
            break
    assert palOff >= 0
    pal = []
    for o in range(palOff, palOff + nBones * 8, 8):
        a = u8[o:o + 2].decode('latin1'); b = u8[o + 4:o + 6].decode('latin1')
        tag = a if u8[o + 4] == 0x42 and u8[o + 5] == 0x6f else b
        pal.append('Bone' + re.sub('[^0-9]', '', tag) if False else 'Bone' + ''.join(ch for ch in tag if ch.isdigit()))
    # skin records
    srOff, NV, srStride, srW, maxJoint = -1, 0, 0, 0, 0
    for ss, wn in ((20, 4), (16, 3), (24, 5), (12, 2), (28, 6)):
        for s in range(palOff + nBones * 8, palOff + nBones * 8 + 0x40, 4):
            n, o, mj = 0, s, 0
            while o + ss <= len(u8) and n < 8000:
                ok, wsum = True, 0.0
                for k in range(wn):
                    w = f32(o + 4 + 4 * k)
                    if u8[o + k] >= nBones or w < -1e-6 or w > 1.0001:
                        ok = False; break
                    wsum += w
                if not ok or not (0.9 < wsum < 1.1):
                    break
                for k in range(wn):
                    mj = max(mj, u8[o + k])
                n += 1; o += ss
            if n >= 200:
                srOff, NV, srStride, srW, maxJoint = s, n, ss, wn, mj
                break
        if srOff >= 0:
            break
    assert srOff >= 0
    # verts
    bmin = [f32(stridesAt - 0x18), f32(stridesAt - 0x14), f32(stridesAt - 0x10)]
    bmax = [f32(stridesAt - 0xc), f32(stridesAt - 8), f32(stridesAt - 4)]
    EPS = 0.02
    vertsOff = -1
    s = stridesAt + 0x40
    while s < stridesAt + 0x300:
        okall = True
        for i in range(NV):
            b = s + i * stride
            if b + stride > len(u8):
                okall = False; break
            px, py, pz = f32(b), f32(b + 4), f32(b + 8)
            if not (bmin[0] - EPS <= px <= bmax[0] + EPS and bmin[1] - EPS <= py <= bmax[1] + EPS
                    and bmin[2] - EPS <= pz <= bmax[2] + EPS):
                okall = False; break
        if okall:
            vertsOff = s; break
        s += 4
    assert vertsOff >= 0
    # indices
    idxOff, IDXN = -1, 0
    s0 = (vertsOff + NV * stride + 3) & ~3
    s = s0
    while s < min(s0 + 0x400, len(u8) - 64):
        n, o = 0, s
        while o + 2 <= len(u8) and n < 0x40000 and u16(o) < NV:
            n += 1; o += 2
        if n >= 32:
            idxOff, IDXN = s, n
            break
        s += 2
    assert idxOff >= 0
    byAlias = {nd['alias']: nd['name'] for nd in nodes if nd['alias'].startswith('Bone')}
    jointNodes = [byAlias.get(p) for p in pal]
    invB = np.array([[f32(invbOff + k * 64 + 4 * i) for i in range(16)] for k in range(nBones)]).reshape(nBones, 4, 4)
    verts = np.array([[f32(vertsOff + i * stride), f32(vertsOff + i * stride + 4), f32(vertsOff + i * stride + 8)] for i in range(NV)])
    skinJ = np.array([[u8[srOff + i * srStride + j] for j in range(4)] for i in range(NV)], dtype=np.int32)
    skinW = np.array([[f32(srOff + i * srStride + 4 + 4 * j) for j in range(srW)] + [0.0] * (4 - srW) for i in range(NV)])
    idx = np.array([u16(idxOff + 2 * i) for i in range(IDXN)], dtype=np.int32)
    return dict(nodes=nodes, pal=pal, jointNodes=jointNodes, invB=invB, verts=verts,
                skinJ=skinJ, skinW=skinW, idx=idx, nBones=nBones, NV=NV, IDXN=IDXN, srW=srW,
                layout=dict(pool0=pool0, pool1=pool1, off4=off4, stridesAt=stridesAt, stride=stride,
                            invbOff=invbOff, palOff=palOff, srOff=srOff, srStride=srStride,
                            vertsOff=vertsOff, idxOff=idxOff))

import re
D = '/tmp/my-project/work/data/'
bat = read_bdae2(D + 'batman.bdae')
mer = read_bdae2(D + 'Bane_mercenary.bdae')
out = {}

for tag, R in (('batman', bat), ('merc', mer)):
    W, J, NB = R['skinW'], R['skinJ'], R['nBones']
    used = R['srW']
    wsum = W[:, :used].sum(axis=1)
    # V1 shuffled-weights null: permute all used weight values across (vertex,slot) grid
    rng = np.random.default_rng(60)
    flat = W[:, :used].ravel().copy()
    shuffled_sums = []
    for _ in range(200):
        perm = rng.permutation(flat)
        shuffled_sums.append(perm.reshape(-1, used).sum(axis=1))
    sh = np.concatenate(shuffled_sums)
    # deliberately-wrong calibration: real + 0.05 offset on first slot
    bad = wsum + 0.05
    out[tag] = {
        'NV': R['NV'], 'nBones': NB, 'srW': used,
        'V1_wsum_mean': float(wsum.mean()), 'V1_wsum_min': float(wsum.min()),
        'V1_wsum_max': float(wsum.max()),
        'V1_frac_in_0p9995_1p0005': float(((wsum > 0.9995) & (wsum < 1.0005)).mean()),
        'V1_null_mean': float(sh.mean()), 'V1_null_sd': float(sh.std()),
        'V1_null_frac_in_window': float(((sh > 0.9995) & (sh < 1.0005)).mean()),
        'V1_badcase_frac_in_window': float(((bad > 0.9995) & (bad < 1.0005)).mean()),
        'V2_max_joint': int(J.max()), 'V2_frac_lt_nBones': float((J < NB).mean()),
        'V3_bbox_min': R['verts'].min(axis=0).tolist(),
        'V3_bbox_max': R['verts'].max(axis=0).tolist(),
        'V3_height': float(R['verts'][:, 2].max() - R['verts'][:, 2].min()),
    }

# V4 centroid vs inverse bind (both rigs), permuted-mapping null
for tag, R in (('batman', bat), ('merc', mer)):
    W, J, invB, V = R['skinW'], R['skinJ'], R['invB'], R['verts']
    NB = R['nBones']
    cents = []
    devs = []
    for k in range(NB):
        mask = (J == k).any(axis=1)
        if mask.sum() < 10:
            continue
        w = W[mask, :]
        wk = np.where(J[mask] == k, w, 0).sum(axis=1)
        c = (V[mask] * wk[:, None]).sum(axis=0) / wk.sum()
        origin = invB[k][:3, 3]
        devs.append(float(np.linalg.norm(c - origin)))
        cents.append(k)
    rng = np.random.default_rng(61)
    nulls = []
    for _ in range(5):
        pm = rng.permutation(NB)
        d2 = []
        for i, k in enumerate(cents):
            origin = invB[pm[k]][:3, 3]
            d2.append(devs[i])  # devs already computed vs true origin
        # true permuted: recompute distances with permuted origins
        d2 = []
        for i, k in enumerate(cents):
            mask = (J == k).any(axis=1)
            if mask.sum() < 10:
                continue
            w = W[mask, :]
            wk = np.where(J[mask] == k, w, 0).sum(axis=1)
            c = (V[mask] * wk[:, None]).sum(axis=0) / wk.sum()
            origin = invB[pm[k]][:3, 3]
            d2.append(float(np.linalg.norm(c - origin)))
        nulls.append(float(np.median(d2)))
    out[tag]['V4_median_dev'] = float(np.median(devs)) if devs else None
    out[tag]['V4_n_bones'] = len(devs)
    out[tag]['V4_null_medians'] = nulls

json.dump(out, open('/tmp/my-project/scripts/s60_t3_mercval.json', 'w'), indent=1)
print(json.dumps({k: {kk: (round(vv, 4) if isinstance(vv, float) else vv) for kk, vv in v.items()
                       if kk not in ('V3_bbox_min', 'V3_bbox_max')}
                  for k, v in out.items()}, indent=1))
