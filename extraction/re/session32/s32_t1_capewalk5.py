#!/usr/bin/env python3
"""S32 T1j: test per-bone sparse-matrix hypothesis for the 32-chunk block;
also scan OBB for a cape mesh file."""
import struct, os, re
import numpy as np

D = '/tmp/my-project/work/data/batman.bdae'
d = open(D, 'rb').read()
u32 = lambda o: struct.unpack_from('<I', d, o)[0]
f32 = lambda o: struct.unpack_from('<f', d, o)[0]

BASE, N, SKIN = 0x4b5c, 1449, 0x31774
b4s = np.array([struct.unpack_from('<4B', d, SKIN + i * 20)
                for i in range(N)], np.int64)
w4s = np.array([struct.unpack_from('<4f', d, SKIN + i * 20 + 4)
                for i in range(N)], np.float64)

BLK, LN = 0x54d78, 21552
tab = [(u32(BLK + 8 * g), u32(BLK + 8 * g + 4)) for g in range(32)]

# dense per-bone slot lists (w>0): bone -> [(vert, w)]
dense = {b: [] for b in range(31)}
for i in range(N):
    for j in range(4):
        b, w = int(b4s[i, j]), float(w4s[i, j])
        if b < 31 and w > 0:
            dense[b].append((i, w))
slotcnt = {b: len(v) for b, v in dense.items()}
print('dense slot counts per bone:', [slotcnt[b] for b in range(31)])
print('chunk counts              :', [c for c, _ in tab])

# walk chunks in offset order and compare each with a bone's dense list
order = sorted(range(32), key=lambda g: tab[g][1])
print('\nchunk walk (offset order): count, offset, first (w,idx), '
      'match-bone?')
for g in order[:12]:
    c, off = tab[g]
    ws, iis = [], []
    ok = True
    for k in range(c - 1 if False else c):
        if off + 8 * k + 8 > LN:
            ok = False
            break
        w, i = f32(BLK + off + 8 * k), u32(BLK + off + 8 * k + 4)
        ws.append(w)
        iis.append(i)
    # find dense bone with same vertex SET
    match = None
    if ok and iis:
        S = set(iis)
        for b in range(31):
            if {v for v, _ in dense[b]} == S:
                match = b
                break
    print(f'  chunk {g:2d} count {c:4d} off {off:6d} '
          f'first ({ws[0] if ws else 0:.3f},{iis[0] if iis else -1}) '
          f'exact-set-match bone {match}')
    if match is not None:
        # compare weights in order
        dw = dict(dense[match])
        werr = max(abs(dw[i] - w) for i, w in zip(iis, ws)) if iis else 0
        print(f'      weights match max err {werr:.2e}')

# OBB scan for cape files
print('\n=== OBB file scan for cape/batman ===')
for root, _, files in os.walk('/tmp/my-project/work/apk_obb'):
    for fn in files:
        if re.search(r'(?i)cape|batman|bdae$', fn):
            p = os.path.join(root, fn)
            print(f'  {p}  {os.path.getsize(p)}')
for root, _, files in os.walk('/tmp/my-project/work/TDKR_data'):
    for fn in files:
        if re.search(r'(?i)cape|batman', fn):
            p = os.path.join(root, fn)
            print(f'  {p}  {os.path.getsize(p)}')
