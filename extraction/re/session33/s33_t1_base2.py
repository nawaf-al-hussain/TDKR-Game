#!/usr/bin/env python3
"""S33 T1: fast base search — candidate bases from entry0 tick arrays, then score."""
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
time_e, valq_e, valv_e = [], [], []
for off, ln in pairs:
    if ln == 0 or ln % 4: continue
    if ln % 16 == 0 and ln >= 0x40: valq_e.append((off, ln))
    elif ln % 12 == 0 and ln >= 0x18: valv_e.append((off, ln))
    elif ln >= 0x20 or ln == 8: time_e.append((off, ln))

OFF0, LEN0 = pairs[0]          # (0x9c, 0xa8) first TIME stream (42 ticks)
K = LEN0 // 4                  # 42

# find all p: u32all[p..p+K) strictly ascending, values < 2e6, last-first>=1000
asc = np.zeros(N, bool)
asc[:-1] = np.diff(u32all.astype(np.int64)) > 0
plaus = u32all < 2_000_000
good = asc & plaus
# sliding window AND over K-1
c = np.cumsum(np.concatenate(([0], good.view(np.int8))))
win_ok = (c[K:] - c[:-K]) == K - 1     # p: run of K-1 asc steps from p to p+K-1
cand_p = np.flatnonzero(win_ok)
span_ok = (u32all[cand_p + K - 1].astype(np.int64) - u32all[cand_p].astype(np.int64)) >= 1000
cand_p = cand_p[span_ok]
bases = (cand_p - OFF0 // 4) * 4
print(f'{len(cand_p)} candidate bases from entry0')

def score_base(B):
    s = n = 0
    for off, ln in time_e:
        a = B + off
        if a < 0 or a + ln > len(d) or a % 4: continue
        w = u32all[a // 4 + 1: (a + ln) // 4 - 1].astype(np.int64)
        if len(w) == 0: continue
        s += bool(np.all(np.diff(w) > 0) and w[-1] < 2_000_000); n += 1
    for off, ln in valq_e:
        a = B + off
        if a < 0 or a + ln > len(d) or a % 16: continue
        q = f32all[a // 4: (a + ln) // 4].reshape(-1, 4).astype(np.float64)
        with np.errstate(invalid='ignore'):
            nr = np.sqrt((q ** 2).sum(1))
        s += bool((np.abs(nr - 1) < 5e-3).mean() > 0.9); n += 1
    for off, ln in valv_e:
        a = B + off
        if a < 0 or a + ln > len(d) or a % 4: continue
        v = f32all[a // 4: (a + ln) // 4].reshape(-1, 3).astype(np.float64)
        s += bool(np.isfinite(v).all() and (np.abs(v) < 100).mean() > 0.95); n += 1
    return s, n

scored = []
for B in bases:
    s, n = score_base(B)
    scored.append((s / max(1, n), s, n, B))
scored.sort(reverse=True)
print('top 12:')
for sc, s, n, B in scored[:12]:
    print(f'  base 0x{B:7x}: {s}/{n} = {sc:.3f}')
