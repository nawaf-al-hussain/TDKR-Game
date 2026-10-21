#!/usr/bin/env python3
"""s44 T2: alternative decodings of the 3-byte F field for the segments that
FAIL the per-segment paired smoothness test (s43: 615/1526 i1 + 305/1020 i2).

Candidates (F lives at stride-dependent offset: s20@12, s24@16, s28@20):
  s8            signed /127            (s43 layout hypothesis)
  u8            unsigned /255          (AO / baked colour-like)
  s8_scaled     s8 x per-seg max-unit scale
  u8_scaled     u8 x per-seg max-unit scale
  oct_u8        octahedral from two u8
  1010102       packed 10-10-10-2 @F..F+4 (rejected by s43; re-run for the
                failing set only)
Metric: edge smoothness (mean L1 across index edges, normalized), PAIRED
row-shuffle null per segment (destroys vertex correlation, keeps value
distribution). Also the population test per material group.
Verdict question: does ANY candidate make the failing set population-smooth
(<< null p95) per material group, or is 'noisy hard-surface content' the
right explanation?
"""
import struct, io, zipfile, collections, json
import numpy as np

P = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla'
g = open(P, 'rb').read()
_, idxsz, tabsz, n = struct.unpack('>IIII', g[:16])
pool = g[16 + n * 16:idxsz]
members = {}
for i in range(n):
    o, s, no, _ = struct.unpack('>IIII', g[16 + i * 16:16 + i * 16 + 16])
    nm = pool[no:pool.index(b'\0', no)].decode('ascii', 'replace')
    members[nm] = (o, s)
zo, zs = members['GothamCity.zip']
Z = zipfile.ZipFile(io.BytesIO(g[zo:zo + zs]))
ld = Z.read('lod_data.bin')
lt = Z.read('lod_table.bin')
u = struct.unpack(f'<{len(lt)//4}I', lt)
cnt = u[0]
pairs = [(u[1 + 2 * k], u[2 + 2 * k]) for k in range(cnt)]


def s8a(v):
    v = v.astype(np.int16)
    return np.where(v >= 128, v - 256, v) / 127.0


def u8a(v):
    return v.astype(np.float64) / 255.0


def oct_u8(raw):
    x = u8a(raw[:, 0:1]) * 2 - 1
    y = u8a(raw[:, 1:2]) * 2 - 1
    z = 1.0 - np.abs(x) - np.abs(y)
    n = np.concatenate([x, y, z], axis=1)
    ln = np.linalg.norm(n, axis=1, keepdims=True)
    ln[ln == 0] = 1
    return n / ln


def s10(v):
    v = v.astype(np.int32)
    return np.where(v >= 512, v - 1024, v) / 511.0


def edge_smooth(f, idx):
    tris = idx.reshape(-1, 3)
    tris = tris[(tris != 0xFFFF).all(axis=1)]
    if len(tris) == 0:
        return None
    i0, i1, i2 = tris[:, 0], tris[:, 1], tris[:, 2]
    d = (np.abs(f[i0] - f[i1]).sum(axis=1) +
         np.abs(f[i1] - f[i2]).sum(axis=1) +
         np.abs(f[i2] - f[i0]).sum(axis=1)) / (3 * len(tris))
    return float(d.mean())


CANDS = ('s8', 'u8', 'oct_u8', '1010102')

rows = []
for k in range(1526):
    off2 = pairs[k][0]
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
    if four != 4:
        continue
    vstart = data_off + 4
    idx = np.frombuffer(ld, '<u2', ib // 2, vstart + vb).astype(np.int64)
    real = idx[idx != 0xFFFF]
    if len(real) == 0:
        continue
    mx = int(real.max())
    cands = [s for s in (24, 20, 32, 28) if vb % s == 0 and mx < vb // s]
    if not cands:
        continue
    st = cands[0]
    if st == 32:
        continue
    foff = {20: 12, 24: 16, 28: 20}[st]
    nv = vb // st
    raw = np.frombuffer(ld, np.uint8, vb, vstart).reshape(nv, st)
    F = raw[:, foff:foff + 4]
    # candidates
    dec = {}
    dec['s8'] = s8a(F[:, :3])
    dec['u8'] = u8a(F[:, :3])
    dec['oct_u8'] = oct_u8(F)
    p = F.copy().view('<u4').reshape(nv)
    dec['1010102'] = np.stack([s10(p & 0x3ff), s10((p >> 10) & 0x3ff),
                               s10((p >> 20) & 0x3ff)], axis=1)
    # per-segment real smoothness + paired row-shuffle null (4 reps, seeded)
    rng = np.random.RandomState(0x544B + k)
    res = {}
    for name, f in dec.items():
        s = edge_smooth(f, idx)
        nulls = []
        for _ in range(4):
            perm = rng.permutation(nv)
            nulls.append(edge_smooth(f[perm], idx))
        if s is None or None in nulls:
            continue
        res[name] = {'s': s, 'null_med': float(np.median(nulls)),
                     'null_min': float(np.min(nulls)), 'pass': s < min(nulls)}
    rows.append({'seg': k, 'stride': st, 'verdicts': res})

# summarize
ok_counts = collections.Counter()
per_cand_real, per_cand_null = collections.defaultdict(list), collections.defaultdict(list)
fails = {'s8': []}
for r in rows:
    for name, v in r['verdicts'].items():
        per_cand_real[name].append(v['s'])
        per_cand_null[name].append(v['null_med'])
        ok_counts[(name, v['pass'])] += 1
        if name == 's8' and not v['pass']:
            fails['s8'].append(r)

print('segments decoded:', len(rows))
for name in CANDS:
    npass = ok_counts[(name, True)]
    nfail = ok_counts[(name, False)]
    mr = np.mean(per_cand_real[name]) if per_cand_real[name] else float('nan')
    mn = np.mean(per_cand_null[name]) if per_cand_null[name] else float('nan')
    print(f'{name:9s} pass {npass:5d} fail {nfail:5d}  mean real {mr:.3f} vs mean null {mn:.3f}')

# the s43-failing population: does ANY candidate flip it to pass?
s8fail = {r['seg'] for r in fails['s8']}
print(f'\ns8-failing population: {len(s8fail)} segments')
flips = collections.Counter()
for r in rows:
    if r['seg'] not in s8fail:
        continue
    for name in CANDS:
        v = r['verdicts'].get(name)
        if v and v['pass']:
            flips[name] += 1
print('candidates that PASS on the s8-failing population:', dict(flips))

# material-group view for the failing set (s43 grouped by material; here by
# stride + smoothness flip availability)
json.dump({'rows': rows, 's8_fail_segs': sorted(s8fail),
           'flip_counts': dict(flips),
           'per_cand_mean_real': {k: float(np.mean(v)) for k, v in per_cand_real.items()},
           'per_cand_mean_null': {k: float(np.mean(v)) for k, v in per_cand_null.items()}},
          open('/home/z/my-project/scripts/s44_t2_ffield.json', 'w'), indent=1)
print('saved s44_t2_ffield.json')
