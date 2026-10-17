#!/usr/bin/env python3
"""S32 T2b: find the key pool + per-clip channel pointer arrays."""
import struct, re

D = '/tmp/my-project/work/data/batman_anims.bdae'
d = open(D, 'rb').read()
u32 = lambda o: struct.unpack_from('<I', d, o)[0]
f32 = lambda o: struct.unpack_from('<f', d, o)[0]

def cstr(v):
    if 0 < v < len(d):
        e = d.find(b'\0', v)
        if 0 < e - v < 80:
            try:
                return d[v:e].decode('latin1')
            except Exception:
                pass
    return None

clips = []
o = 0x11580
while True:
    nameOff, ts, te = struct.unpack_from('<3I', d, o + 12 * len(clips))
    nm = cstr(nameOff)
    if not nm or ts > te or te > 10_000_000:
        break
    clips.append((nm, ts, te, o + 12 * len(clips)))
print(f'{len(clips)} clips; table ends 0x{clips[-1][3]+12:x}')

# key-run scan (r16 census): 8-B pairs (f32 plausible, u32 tick plausible)
import numpy as np
f32all = np.frombuffer(d[:len(d) & ~7], np.float32)
u32all = np.frombuffer(d[:len(d) & ~7], np.uint32)
# pair i: f32 at 8i, u32 at 8i+1 (word indices 2i, 2i+1)
wf = f32all[0::2]
wu = u32all[1::2]
plausible = (np.abs(wf) < 100) & (wu < 200000)
# runs of plausible pairs
runs = []
start = None
n = len(wf)
pl = plausible
# find long runs efficiently
idx = np.flatnonzero(np.diff(np.concatenate(([0], pl.view(np.int8), [0]))))
for k in range(0, len(idx), 2):
    a, b2 = int(idx[k]), int(idx[k + 1])
    if b2 - a >= 24:      # >= 24 pairs
        runs.append((a * 8, b2 - a))
print(f'key-like runs (>=24 pairs): {len(runs)}')
for off, ln in runs[:12]:
    print(f'  @0x{off:x}: {ln} pairs; first f32={f32(off):.4f} tick={u32(off+4)}')
if len(runs) > 12:
    print('  ...')
    for off, ln in runs[-4:]:
        print(f'  @0x{off:x}: {ln} pairs')

# region map 0x1000..0xb53c: what structures?
print('\nstructure peek:')
for off in (0x0, 0x10, 0x20, 0x1ea0, 0x2000, 0x4000, 0x8000, 0xb000):
    print(f'  @0x{off:x}:', ' '.join(f'{u32(off+4*j):08x}' for j in range(8)))

# pointer-array dialect: after clip table, look for arrays of u32 pointing
# into the descriptor/record zone (0xbf04..0x11000?) or key pool
print('\nscan 0x11e54..0x14000 as u32 arrays:')
for off in range(0x11e54, 0x12400, 32):
    vals = [u32(off + 4 * j) for j in range(8)]
    print(f'  @0x{off:x}:', ' '.join(f'{v:08x}' for v in vals))
