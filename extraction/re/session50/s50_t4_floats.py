#!/usr/bin/env python3
"""s50 T4: locate and identify the per-material 10-float runs in the compiled BRES.
Approach: scan for a 307-entry pointer table whose targets are value blocks with
the {1, ptr+24} header followed by 10 f32 (64 B each). Then: which parameters
(order), per-material variation, and correlation with effect families."""
import zipfile, io, json, struct
import numpy as np

P = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
LE = zipfile.ZipFile(io.BytesIO(open(P, 'rb').read())).read('little_endian_not_quantized.bdae')
w32 = np.frombuffer(LE, '<u4', len(LE) // 4)
nb = len(LE)
f32 = np.frombuffer(LE, '<f4', len(LE) // 4)

def cs(p, maxn=80):
    if not (0 < p < nb):
        return None
    e = LE.find(b'\0', p)
    if e < 0 or e == p or e - p > maxn:
        return None
    try:
        t = LE[p:e].decode('ascii')
    except Exception:
        return None
    return t if all(32 <= ord(c) < 127 for c in t) else None

# effects per material from the instance table
fx_of = {}
for i in range(307):
    a = 0x5fea0 + i * 36
    ws = [int(w32[(a + k * 4) // 4]) for k in range(9)]
    s = cs(ws[3]) or ''
    fx_of[i] = s.split('-fx')[0].lstrip('#')

N = 307
found = []
for p in range(0x40, nb - N * 4, 4):
    w0 = w32[p // 4]
    if not (0x40 < w0 < nb - 64):
        continue
    # quick reject: check first two entries
    ok = True
    for i in range(min(3, N)):
        t = int(w32[p // 4 + i])
        if not (0x40 < t < nb - 64):
            ok = False
            break
        if int(w32[t // 4]) != 1 or int(w32[t // 4 + 1]) != t + 24:
            ok = False
            break
    if not ok:
        continue
    # full check
    good = 0
    for i in range(N):
        t = int(w32[p // 4 + i])
        if 0x40 < t < nb - 64 and int(w32[t // 4]) == 1 and int(w32[t // 4 + 1]) == t + 24:
            good += 1
    if good >= N - 2:
        found.append((p, good))
        if len(found) > 8:
            break
print('candidate 307-entry value-block tables:', [(hex(p), g) for p, g in found])

out = {}
for p, good in found[:3]:
    floats = np.zeros((N, 10), np.float64)
    bad = []
    for i in range(N):
        t = int(w32[p // 4 + i])
        try:
            floats[i] = f32[(t + 24) // 4:(t + 24) // 4 + 10]
        except Exception:
            bad.append(i)
    # column stats
    colinfo = []
    for c in range(10):
        col = floats[:, c]
        uvals = np.unique(col)
        colinfo.append({'col': c, 'min': float(col.min()), 'max': float(col.max()),
                        'n_unique': int(len(uvals)),
                        'most_common': float(uvals[np.argmax(np.array([np.sum(col == v) for v in uvals]))]) if len(uvals) else None})
    # variation per column and effect correlation
    var_cols = [c for c in range(10) if len(np.unique(floats[:, c])) > 3]
    # group signature: columns with variation, most common values
    sig = collections = {}
    import collections as _c
    sigc = _c.Counter(tuple(np.round(r, 4)) for r in floats)
    print('table @%s: %d valid blocks; varying cols %s' % (hex(p), good, var_cols))
    for c in range(10):
        ci = colinfo[c]
        print('  col %d: min %.4g max %.4g unique %d common %.4g' % (c, ci['min'], ci['max'], ci['n_unique'], ci['most_common']))
    # per-effect mean signature
    byfx = {}
    for i in range(N):
        byfx.setdefault(fx_of[i], []).append(floats[i])
    print('  per-effect means (top families):')
    for fx, arr in sorted(byfx.items(), key=lambda kv: -len(kv[1]))[:6]:
        m = np.mean(arr, axis=0)
        print('    %-22s n=%3d  %s' % (fx, len(arr), np.round(m, 3).tolist()))
    out['table_%x' % p] = {'good': good, 'colinfo': colinfo,
                           'floats_sample': {str(i): floats[i].tolist() for i in range(0, N, 40)},
                           'per_effect_mean': {fx: np.mean(arr, axis=0).tolist() for fx, arr in byfx.items()}}
json.dump(out, open('/tmp/my-project/work/TDKR-Game/extraction/re/session50/s50_t4_floats.json', 'w'), indent=1)
print('saved s50_t4_floats.json')
