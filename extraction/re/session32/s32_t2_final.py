#!/usr/bin/env python3
"""S32 T2 final: consolidate animation decode results -> JSON + verdict."""
import struct, json, math
import numpy as np

D = '/tmp/my-project/work/data/batman_anims.bdae'
d = open(D, 'rb').read()
u32 = lambda o: struct.unpack_from('<I', d, o)[0]
f32 = lambda o: struct.unpack_from('<f', d, o)[0]

def cstr(v):
    if 0 < v < len(d):
        e = d.find(b'\0', v)
        if 0 < e - v < 90:
            try:
                return d[v:e].decode('latin1')
            except Exception:
                pass
    return None

# 1. clip table
clips = []
o = 0x11580
while True:
    nameOff, ts, te = struct.unpack_from('<3I', d, o + 12 * len(clips))
    nm = cstr(nameOff)
    if not nm or ts > te or te > 10_000_000:
        break
    clips.append((nm, ts, te))

# 2. named groups + records
groups = []
o = 0xb53c
while True:
    w = struct.unpack_from('<8I', d, o)
    if not (w[2] and cstr(w[2]) and w[3] == 1 and w[5] == 1):
        break
    groups.append(w)
    o += 32
recs = []
for w in groups:
    rw = [u32(w[4] + 4 * j) for j in range(11)]
    recs.append(rw)
stride_ok = sum(1 for w, r in zip(groups, recs)
                if r[7] >> 16 == (r[5] * 4))
comps_track_ok = sum(1 for w, r in zip(groups, recs)
                     if (('translation' in cstr(w[2])) == (r[5] == 3)))
print(f'stride==comps*4: {stride_ok}/{len(recs)}')
print(f'comps matches track name: {comps_track_ok}/{len(recs)}')

# quat unit-norm check on _187/_193 value zones
o = 0x11e54
rec_by_name = {}
for k in range(734):
    A, B, C = u32(o + 12 * k), u32(o + 12 * k + 4), u32(o + 12 * k + 8)
    rec_by_name[cstr(C)] = (A, B)
qn = []
for nm in ('_187_enemy_idle_aim_to_run_aim', '_193_back_spin_kick2',
           '_184_fly_h_to_gargoyle'):
    A, B = rec_by_name[nm]
    for j in range(12):
        q = struct.unpack_from('<4f', d, A + 16 * j)
        qn.append(math.sqrt(sum(x * x for x in q)))
qn = sorted(qn)
print(f'quat norms (36 samples from 3 clips): median {qn[18]:.4f}, '
      f'min {qn[0]:.4f}, max {qn[-1]:.4f}')

# tick cadence: deltas of _187 ticks
A, B = rec_by_name['_187_enemy_idle_aim_to_run_aim']
# find tick start: first ascending u32 run after values
tk = None
for off in range(A, B - 160, 4):
    vs = [u32(off + 4 * j) for j in range(12)]
    if all(vs[i] < vs[i + 1] for i in range(11)) and vs[0] > 1000:
        tk = off
        break
deltas = [u32(tk + 4 * (j + 1)) - u32(tk + 4 * j) for j in range(39)]
import collections
print(f'_187 ticks @0x{tk:x}: n=40, first={u32(tk)}, last={u32(tk+156)}, '
      f'delta histogram {dict(collections.Counter(deltas))}')

# channel targets
bones = sorted({cstr(w[2]).split('-node-')[0] for w in groups})
tracks = sorted({cstr(w[2]).split('-node-')[1] for w in groups})

out = dict(
    n_clips=len(clips),
    clip0='_001_idle_stand', clip0_duration_ms=clips[0][2] - clips[0][1],
    run_duration_ms=dict(walk=clips[5][2] - clips[5][1],
                         run=clips[6][2] - clips[6][1]),
    named_groups=len(groups),
    stride_consistency=f'{stride_ok}/{len(recs)}',
    comps_track_consistency=f'{comps_track_ok}/{len(recs)}',
    record_layout='[u32 1][u32 4][u32 1][u32 timeIdx=2k][u32 6]'
                  '[u32 comps 3|4][u32 valIdx=2k+1][u32 strideB<<16]'
                  '[u32 nodeNamePtr][u32 X 1|5][u32 0x14FFFF]',
    key_layout='value stream (f32 x comps per key) then shared u32 ms '
               'tick stream; tick deltas ~30 fps (16/33/50 ms)',
    quat_norm_median=qn[18],
    tick_cadence=dict(n=40, first_ms=u32(tk), last_ms=u32(tk + 156),
                      delta_hist={str(k): v for k, v in
                                  collections.Counter(deltas).items()}),
    channel_targets=dict(n_bones=len(bones), bones=bones[:80], tracks=tracks),
    per_clip_blocks=733,
    page_table_0x18c14=[[u32(0x18c14 + 8 * j), u32(0x18c14 + 8 * j + 4)]
                        for j in range(6)],
    run_sites=[[0x834348, 0x80], [0xbbf73c, 0x170], [0x18cb024, 0x20],
               [0x22c6d68, 0x164], [0x23a5584, 0x230]],
    resisting_block=('per-clip stream-table resolution: mapping channel k -> '
                     '(tickRange, valueRange) for both dialects '
                     '(named-group records use paired indices 2k/2k+1 into '
                     'an unresolved stream table; 184+ blocks have '
                     'concatenated multi-channel value streams whose '
                     'per-channel segmentation is unresolved)'),
)
json.dump(out, open('/home/z/my-project/download/s32_t2_result.json', 'w'),
          indent=1)
print('wrote s32_t2_result.json')
print('VERDICT T2: PARTIAL — descriptor layout + key/tick semantics decoded '
      'and cross-validated; pose test blocked on stream-table resolution')
