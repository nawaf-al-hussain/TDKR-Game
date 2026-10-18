#!/usr/bin/env python3
"""S33 T1: locate _008_run / _007_walk tick arrays via clip windows."""
import struct
import numpy as np

d = open('/tmp/my-project/work/data/batman_anims.bdae', 'rb').read()
u32 = lambda o: struct.unpack_from('<I', d, o)[0]

def cstr(v):
    if 0 < v < len(d):
        e = d.find(b'\0', v)
        if 0 < e - v < 90:
            try: return d[v:e].decode('latin1')
            except Exception:
                return None

clips = []
o = 0x11580
while True:
    nameOff, ts, te = struct.unpack_from('<3I', d, o + 12 * len(clips))
    nm = cstr(nameOff)
    if not nm or ts > te or te > 10_000_000:
        break
    clips.append((nm, ts, te))
for i, (nm, ts, te) in enumerate(clips[:12]):
    print(i, nm, ts, te)

N = len(d) // 4
ua = np.frombuffer(d[:N * 4], np.uint32)
asc = np.zeros(N, bool)
asc[:-1] = np.diff(ua.astype(np.int64)) > 0
good = asc & (ua < 2_000_000)
c = np.cumsum(np.concatenate(([0], good.view(np.int8))))
K = 12
win = (c[K:] - c[:-K]) == K - 1
starts = np.flatnonzero(win)
for want in ('_007_walk', '_008_run', '_009_run_r_turn_left', '_010_run_l_turn_left',
             '_011_run_r_turn_right'):
    hit = [(i, nm, ts, te) for i, (nm, ts, te) in enumerate(clips) if nm == want]
    if not hit:
        print(want, 'NOT IN TABLE')
        continue
    i, nm, ts, te = hit[0]
    inside = [s for s in starts if ts <= int(ua[s]) and int(ua[s + K - 1]) <= te]
    print(f'{nm} [{ts}..{te}]: {len(inside)} run-starts inside; first: '
          + ' '.join(hex(int(s) * 4) for s in inside[:12]))
