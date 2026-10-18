#!/usr/bin/env python3
"""S33 T1: brute-force the stream-table base by scoring all 156 entries."""
import struct
import numpy as np

D = '/tmp/my-project/work/data/batman_anims.bdae'
d = open(D, 'rb').read()
u32 = lambda o: struct.unpack_from('<I', d, o)[0]
N = len(d) // 4
u32all = np.frombuffer(d[:N * 4], np.uint32)
f32all = np.frombuffer(d[:N * 4], np.float32)

ENT = 0x53200
pairs = [(u32(ENT + 8 * k), u32(ENT + 8 * k + 4)) for k in range(156)]

# pre-classify entries
time_e = []   # (off, len, nkeys)
valq_e = []   # quat value streams
valv_e = []   # vec3 value streams
for off, ln in pairs:
    if ln == 0: continue
    if ln % 4:  continue
    if ln % 16 == 0 and ln >= 0x40:
        valq_e.append((off, ln))
    elif ln % 12 == 0 and ln >= 0x18:
        valv_e.append((off, ln))
    elif ln >= 0x20:
        time_e.append((off, ln))
    elif ln == 8:
        time_e.append((off, ln))
print(f'time-like {len(time_e)}, quat-val {len(valq_e)}, vec3-val {len(valv_e)}')

def score_base(B):
    s_t = s_q = s_v = 0.0
    n_t = n_q = n_v = 0
    for off, ln in time_e:
        a = B + off
        if a < 0 or a + ln > len(d): return -1
        w = u32all[a // 4 + 1: (a + ln) // 4 - 1].astype(np.int64)
        if len(w) == 0: continue
        ok = np.all(np.diff(w) > 0) and w[-1] < 2_000_000
        n_t += 1; s_t += ok
    for off, ln in valq_e:
        a = B + off
        if a % 16: continue
        if a + ln > len(d): return -1
        q = f32all[a // 4: (a + ln) // 4].reshape(-1, 4).astype(np.float64)
        with np.errstate(invalid='ignore'):
            nr = np.sqrt((q ** 2).sum(1))
        ok = bool(np.isfinite(nr).all()) and bool((np.abs(nr - 1) < 5e-3).mean() > 0.9)
        n_q += 1; s_q += ok
    for off, ln in valv_e:
        a = B + off
        if a % 4: continue
        if a + ln > len(d): return -1
        v = f32all[a // 4: (a + ln) // 4].reshape(-1, 3).astype(np.float64)
        ok = np.isfinite(v).all() and (np.abs(v) < 100).mean() > 0.95
        n_v += 1; s_v += ok
    tot = (s_t + s_q + s_v) / max(1, n_t + n_q + n_v)
    return tot

best = []
for B in range(0, 0x100000, 4):
    sc = score_base(B)
    if sc > 0.5:
        best.append((sc, B))
best.sort(reverse=True)
print('top bases:')
for sc, B in best[:12]:
    print(f'  base 0x{B:x} score {sc:.3f}')
