#!/usr/bin/env python3
"""S33 T1: find tick runs fully inside _007_walk/_008_run windows (maximal runs)."""
import struct
import numpy as np

d = open('/tmp/my-project/work/data/batman_anims.bdae', 'rb').read()
u32 = lambda o: struct.unpack_from('<I', d, o)[0]
N = len(d) // 4
ua = np.frombuffer(d[:N * 4], np.uint32)

asc = np.zeros(N, bool)
asc[:-1] = (np.diff(ua.astype(np.int64)) > 0) & (ua[1:] < 2_000_000) & (ua[:-1] < 2_000_000)
idx = np.flatnonzero(np.diff(np.concatenate(([0], asc.view(np.int8), [0]))))
runs = [(int(idx[k]), int(idx[k + 1])) for k in range(0, len(idx), 2)
        if idx[k + 1] - idx[k] >= 20]          # >=21 ticks
print(f'{len(runs)} maximal runs >=21 ticks')

def cstr(v):
    if 0 < v < len(d):
        e = d.find(b'\0', v)
        if 0 < e - v < 90:
            try: return d[v:e].decode('latin1')
            except Exception: return None
clips = []
o = 0x11580
while True:
    nameOff, ts, te = struct.unpack_from('<3I', d, o + 12 * len(clips))
    nm = cstr(nameOff)
    if not nm or ts > te or te > 10_000_000: break
    clips.append((nm, ts, te))

for want in ('_007_walk', '_008_run'):
    ts, te = [(a, b) for nm, a, b in clips if nm == want][0]
    inside = [(a, b) for a, b in runs
              if ts <= int(ua[a]) and int(ua[b]) <= te]
    print(f'\n{want} [{ts}..{te}]: {len(inside)} runs fully inside')
    for a, b in inside[:16]:
        print(f'  @0x{a*4:x}: n={b-a+1} [{int(ua[a])}..{int(ua[b])}]')
