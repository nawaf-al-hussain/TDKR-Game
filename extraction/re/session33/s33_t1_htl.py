#!/usr/bin/env python3
"""S33 T1: H-TL global-timeline test.

Scan whole batman_anims.bdae for:
  (a) maximal runs of ascending u32 (tick arrays)
  (b) runs of unit-norm 4-float groups (quat streams)
  (c) smooth 3-float runs (translation streams)
Check (a) against the 921 clip windows [ts, te]: does a tick run's
[min,max] fall inside one clip window? Nulls: shuffled u32 / random f32.
"""
import struct, collections
import numpy as np

D = '/tmp/my-project/work/data/batman_anims.bdae'
d = open(D, 'rb').read()
N = len(d) // 4
u32all = np.frombuffer(d[:N * 4], np.uint32)
f32all = np.frombuffer(d[:N * 4], np.float32)

# ---- clip table ----
u32 = lambda o: struct.unpack_from('<I', d, o)[0]
def cstr(v):
    if 0 < v < len(d):
        e = d.find(b'\0', v)
        if 0 < e - v < 90:
            try: return d[v:e].decode('latin1')
            except Exception: pass
clips = []
o = 0x11580
while True:
    nameOff, ts, te = struct.unpack_from('<3I', d, o + 12 * len(clips))
    nm = cstr(nameOff)
    if not nm or ts > te or te > 10_000_000: break
    clips.append((nm, ts, te))
print(f'{len(clips)} clips')

# ---- (a) ascending u32 runs ----
asc = (u32all[1:] > u32all[:-1]) & (u32all[1:] < 2_000_000) & (u32all[:-1] < 2_000_000)
idx = np.flatnonzero(np.diff(np.concatenate(([0], asc.view(np.int8), [0]))))
runs = []
for k in range(0, len(idx), 2):
    a, b = int(idx[k]), int(idx[k + 1])   # asc[a..b-1] true => run a..b
    if b - a >= 12:                        # >= 13 ticks
        runs.append((a, b))
print(f'ascending u32 runs >=13: {len(runs)}')
stats = collections.Counter()
inwin = 0
for a, b in runs:
    lo, hi = int(u32all[a]), int(u32all[b])
    span = hi - lo
    stats[0 if span < 500 else (1 if span < 3000 else 2)] += 1
    # find clip windows containing [lo,hi]
    wins = [i for i, (nm, ts, te) in enumerate(clips) if ts - 20 <= lo and hi <= te + 20]
    if wins:
        inwin += 1
        if inwin <= 15:
            print(f'  run @0x{a*4:x}: {b-a+1} ticks [{lo}..{hi}] -> clip(s) '
                  f'{[(clips[i][0], clips[i][1], clips[i][2]) for i in wins[:3]]}')
print(f'runs inside a clip window: {inwin}/{len(runs)}; span hist {dict(stats)}')

# null: shuffle the u32 array (same values) -> rerun count
rng = np.random.default_rng(7)
sh = rng.permutation(u32all[:len(d) // 8 * 2])  # shuffle first half for speed
asc2 = (sh[1:] > sh[:-1]) & (sh[1:] < 2_000_000) & (sh[:-1] < 2_000_000)
idx2 = np.flatnonzero(np.diff(np.concatenate(([0], asc2.view(np.int8), [0]))))
n2 = sum(1 for k in range(0, len(idx2), 2) if idx2[k + 1] - idx2[k] >= 12)
print(f'NULL (shuffled u32, half file): ascending runs >=13: {n2}')

# ---- (b) unit-quat runs ----
q = f32all[:len(f32all) // 4 * 4].reshape(-1, 4)
with np.errstate(invalid='ignore'):
    nrm = np.sqrt((q.astype(np.float64) ** 2).sum(1))
ok = np.isfinite(nrm) & (np.abs(nrm - 1) < 2e-3)
idx = np.flatnonzero(np.diff(np.concatenate(([0], ok.view(np.int8), [0]))))
qruns = [(int(idx[k]), int(idx[k + 1])) for k in range(0, len(idx), 2)
         if idx[k + 1] - idx[k] >= 8]
print(f'\nunit-quat runs >=9 groups: {len(qruns)}')
for a, b in qruns[:10]:
    print(f'  @0x{a*16:x}: {b-a} quats')
# null: random floats in quat range
nf = (rng.standard_normal(len(q) * 4) * 0.3).astype(np.float32)
nq = np.sqrt((nf.reshape(-1, 4).astype(np.float64) ** 2).sum(1))
ok2 = np.abs(nq - 1) < 2e-3
idx2 = np.flatnonzero(np.diff(np.concatenate(([0], ok2.view(np.int8), [0]))))
nq2 = sum(1 for k in range(0, len(idx2), 2) if idx2[k + 1] - idx2[k] >= 8)
print(f'NULL (random f32): quat runs >=9: {nq2}')
