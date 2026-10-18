#!/usr/bin/env python3
"""S34 T1: re-run r23's contiguous walk (strict time validation), record where
each time stream landed, fit off->file transform per channel."""
import struct, json, math
import numpy as np

AD = '/tmp/my-project/work/data/batman_anims.bdae'
ad = open(AD, 'rb').read()
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]
f32a = lambda o: struct.unpack_from('<f', ad, o)[0]

P = json.load(open('/home/z/my-project/scripts/s34_t1_pairs.json'))
names, pairs = P['names'], P['pairs']

def ticks_asc(p, n):
    w = [u32a(p + 4 * j) for j in range(n)]
    return all(w[i] < w[i + 1] for i in range(n - 1)) and w[-1] < 2_000_000

# r23 walk
pos = 0x536e4
walk = []
for k, (off, ln) in enumerate(pairs):
    nm = names[k // 2] if k // 2 < len(names) else f'?{k}'
    is_time = (k % 2 == 0)
    if ln == 0:
        walk.append((k, nm, off, ln, None)); continue
    n_iter = ln // 4 if is_time else (ln // 16 if (ln % 16 == 0 and ln >= 0x20)
                                      else ln // 12)
    found = None
    if is_time:
        for pad in range(0, 40, 4):
            p = pos + pad
            if p + ln <= len(ad) and ticks_asc(p, n_iter):
                found = p; break
    else:
        if ln % 16 == 0 and ln >= 0x20:
            found = pos          # accepted without validation (r23)
        elif ln % 12 == 0:
            found = pos
    walk.append((k, nm, off, ln, found))
    pos = (found if found is not None else pos) + ln

# fit d = found - off for time streams that validated
rows = []
for k, nm, off, ln, found in walk:
    if ln and k % 2 == 0 and found is not None:
        rows.append((k, nm, off, ln, found, found - off))
print(f'time streams validated in walk: {len(rows)}/78')
print('\nk name off found d(=found-off):')
for t in rows:
    print(f'  {t[0]:3d} {t[1][:24]:24s} off=0x{t[2]:05x} found=0x{t[4]:06x} '
          f'd=0x{t[5]:06x}')

dvals = [t[5] for t in rows]
print(f'\nd: min 0x{min(dvals):x} max 0x{max(dvals):x} n_unique {len(set(dvals))}')
import collections
print('top d:', [(hex(v), c) for v, c in collections.Counter(dvals).most_common(8)])

# correlation: d as function of off? fit linear
offs = np.array([t[2] for t in rows], float)
ds = np.array(dvals, float)
A = np.vstack([offs, np.ones_like(offs)]).T
coef, res, *_ = np.linalg.lstsq(A, ds, rcond=None)
pred = A @ coef
err = np.abs(pred - ds)
print(f'\nlinear fit d = {coef[0]:.4f}*off + {coef[1]:.1f}: max resid {err.max():.1f}, '
      f'median {np.median(err):.1f}')

# maybe d constant for most, outliers = pad-bytes channels
med_d = float(np.median(ds))
inl = [t for t in rows if abs(t[5] - med_d) < 64]
outl = [t for t in rows if abs(t[5] - med_d) >= 64]
print(f'\nmedian d = 0x{int(med_d):x} ({int(med_d)}); inliers {len(inl)}, outliers {len(outl)}')
print('outliers:', [(t[0], t[1][:20], hex(t[2]), hex(t[5])) for t in outl[:20]])

# what about the last found end?
print(f"\nwalk end: 0x{pos:x}")
json.dump([list(t) for t in rows], open('/home/z/my-project/scripts/s34_t1_fit.json', 'w'))
