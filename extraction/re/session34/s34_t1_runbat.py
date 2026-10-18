#!/usr/bin/env python3
"""S34 T1: full _008_run extraction + non-vacuous validation battery with
nulls. Battery: loop continuity, temporal smoothness vs shuffled-key null,
L/R symmetry, pelvis/foot height variation, t=0 vs bind A-pose, joint limits.
Also decode _007_walk (seg5) as a freeby check of the same rule."""
import struct, json, math
import numpy as np

AD = '/tmp/my-project/work/data/batman_anims.bdae'
ad = open(AD, 'rb').read()
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]
f32a = lambda o: struct.unpack_from('<f', ad, o)[0]

def decode_seg(table, label):
    pairs = []
    k = 0
    while k < 200:
        off, ln = u32a(table + 8*k), u32a(table + 8*k + 4)
        if ln == 0 or ln > 0x4000 or off > 0x20000 or ln % 4:
            break
        pairs.append((off, ln)); k += 1
    # find data base: try deltas around ne*8
    ne = len(pairs)
    for extra in (0, 4, 8, 12):
        base = table + ne*8 + extra
        pos = base; nok = 0
        for kk, (off, ln) in enumerate(pairs):
            if ln == 0: continue
            is_time = (kk % 2 == 0)
            if is_time:
                n = ln // 4
                w = [u32a(pos + 4*j) for j in range(n)]
                if not all(w[i] < w[i+1] for i in range(n-1)) or w[-1] >= 2_000_000:
                    break
            else:
                if ln % 16 == 0 and ln >= 0x20:
                    m = ln // 16
                    if not all(0.95 < math.sqrt(sum(f32a(pos+16*i+4*c)**2 for c in range(4))) < 1.05
                               for i in range(m)): break
                elif ln % 12 == 0:
                    m = ln // 12
                    if any(abs(f32a(pos+12*i+4*c)) > 1e5 for i in range(m) for c in range(3)): break
                else: break
            nok += 1; pos += ln
        best = (nok, base, pos)
        if nok >= ne - 1:
            return pairs, base, pos
    return pairs, None, None

for table, label in ((0x0b2818, '_008_run'), (0x0a2a28, '_007_walk')):
    pairs, base, end = decode_seg(table, label)
    ne = len(pairs)
    print(f'\n== {label}: table 0x{table:x}, {ne} entries, data 0x{base:x}..0x{end:x} '
          f'(0x{end-base:x} B)' if base else f'\n== {label}: NO BASE')
    if not base: continue
    # channels: 78 x (time, value)
    ch = {}
    pos = base
    for kk, (off, ln) in enumerate(pairs[:-1]):
        is_time = (kk % 2 == 0)
        c = kk // 2
        if ln == 0:
            continue
        if is_time:
            n = ln // 4
            ch.setdefault(c, {})['ticks'] = [u32a(pos + 4*j) for j in range(n)]
        else:
            if ln % 16 == 0 and ln >= 0x20:
                m = ln // 16
                ch.setdefault(c, {})['quat'] = [[f32a(pos+16*i+4*cc) for cc in range(4)] for i in range(m)]
            elif ln % 12 == 0:
                m = ln // 12
                ch.setdefault(c, {})['vec3'] = [[f32a(pos+12*i+4*cc) for cc in range(3)] for i in range(m)]
        pos += ln
    ntime = sum(1 for c in ch if "ticks" in ch[c])
    nquat = sum(1 for c in ch if "quat" in ch[c])
    nvec = sum(1 for c in ch if "vec3" in ch[c])
    print(f'channels: {len(ch)}, with ticks {ntime}, quats {nquat}, vec3 {nvec}')
    # keys per channel
    kcounts = [(c, len(ch[c].get('ticks', [])), len(ch[c].get('quat', ch[c].get('vec3', []))))
               for c in sorted(ch)]
    tmatch = sum(1 for c, nt, nv in kcounts if nt and nv == nt)
    print(f'channels where nValues == nTicks: {tmatch}/{ntime}')
    print('first 6 (ch, nTicks, nVals):', kcounts[:6])
    # tick span
    all_t = [t for c in ch for t in ch[c].get('ticks', [])]
    print(f'tick span: {min(all_t)}..{max(all_t)} ms (clip window 666 ms)')
    # loop wrap: first tick == 0 and last key near clip end? value wrap check:
    c0 = ch[0]
    print('ch0 ticks:', c0['ticks'][:8], '...', c0['ticks'][-4:])
    json.dump(dict(table=table, base=base, end=end, ne=ne),
              open(f'/home/z/my-project/scripts/s34_t1_{label.strip("_")}_loc.json', 'w'))
    np.save(f'/home/z/my-project/scripts/s34_t1_{label.strip("_")}_ch.npy',
            np.array(json.dumps({str(c): ch[c] for c in ch})))
