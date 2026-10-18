#!/usr/bin/env python3
"""S34 T1: empirically locate every idle_stand time stream (strictly ascending
u32 runs of exact length n), fit off->file transform. Also unit-quat runs for
rotation channels. Reveals whether off is pool-relative and what the base is."""
import struct, json
import numpy as np

AD = '/tmp/my-project/work/data/batman_anims.bdae'
ad = open(AD, 'rb').read()
n_bytes = len(ad)
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]
f32a = lambda o: struct.unpack_from('<f', ad, o)[0]

P = json.load(open('/home/z/my-project/scripts/s34_t1_pairs.json'))
names, pairs = P['names'], P['pairs']

LO, HI = 0x50000, 0x70000
seg = ad  # scan whole buffer but restrict windows

def find_time_runs(n):
    """all p in [LO,HI) where u32[p..p+4n) strictly ascending, end<2e6"""
    out = []
    if n < 2: return out
    win = 4 * n
    for p in range(LO, min(HI, n_bytes - win)):
        ok = True
        prev = u32a(p)
        if prev > 2_000_000: continue
        for j in range(1, n):
            cur = u32a(p + 4 * j)
            if cur <= prev or cur > 2_000_000: ok = False; break
            prev = cur
        if ok: out.append(p)
    return out

def is_quat_zone(p, m):
    for i in range(m):
        q = [f32a(p + 16*i + 4*c) for c in range(4)]
        nr = math.sqrt(sum(x*x for x in q))
        if not (0.97 < nr < 1.03): return False
        if not all(abs(x) <= 1.001 for x in q): return False
    return True

import math
def find_quat_runs(m):
    out = []
    win = 16 * m
    for p in range(LO, min(HI, n_bytes - win)):
        if is_quat_zone(p, m): out.append(p)
    return out

# per-channel candidate collection
report = []
for k, (off, ln) in enumerate(pairs):
    if not ln: continue
    nm = names[k // 2] if k // 2 < len(names) else '?'
    if k % 2 == 0:
        n = ln // 4
        cands = find_time_runs(n)
        report.append(dict(k=k, name=nm, kind='time', n=n, off=off,
                           cands=[hex(c) for c in cands[:8]], ncand=len(cands)))
    else:
        if ln % 16 == 0 and ln >= 0x20:
            m = ln // 16
            cands = find_quat_runs(m)
            report.append(dict(k=k, name=nm, kind='quat', n=m, off=off,
                               cands=[hex(c) for c in cands[:8]], ncand=len(cands)))
        else:
            report.append(dict(k=k, name=nm, kind='vec3', n=ln // 12, off=off,
                               cands=[], ncand=-1))

uniq = [r for r in report if r['ncand'] == 1]
multi = [r for r in report if r['ncand'] > 1]
none = [r for r in report if r['ncand'] == 0]
print(f'time/quat entries: unique {len(uniq)}, multi {len(multi)}, none {len(none)}')

print('\nunique-hit transform (file_pos - off):')
ds = []
for r in uniq:
    d = int(r['cands'][0], 16) - r['off']
    ds.append((r['k'], r['name'], r['kind'], r['n'], r['off'], int(r['cands'][0], 16), d))
for t in ds[:30]:
    print(f'  k={t[0]:3d} {t[1][:26]:26s} {t[2]:4s} n={t[3]:3d} off=0x{t[4]:05x} '
          f'file=0x{t[5]:06x} d=0x{t[6]:06x} ({t[6]})')
dvals = [t[6] for t in ds]
print(f'\nd stats: min 0x{min(dvals):x} max 0x{max(dvals):x} unique {len(set(dvals))}')

# check d vs off relationship
import collections
# maybe two zones: main pool + shared tail -> d piecewise constant?
cv = collections.Counter(dvals)
print('most common d:', [(hex(v), c) for v, c in cv.most_common(6)])

json.dump(report, open('/home/z/my-project/scripts/s34_t1_scan.json', 'w'))
print('wrote s34_t1_scan.json')
