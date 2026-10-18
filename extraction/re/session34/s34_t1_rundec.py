#!/usr/bin/env python3
"""S34 T1: decode _008_run from seg6 (table 0xb2818, data ~0xb2d00) with the
sequential cumsum rule; report keys/channel, loop wrap, tick cadence, and run
the validation battery (with nulls)."""
import struct, json, math
import numpy as np

AD = '/tmp/my-project/work/data/batman_anims.bdae'
ad = open(AD, 'rb').read()
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]
f32a = lambda o: struct.unpack_from('<f', ad, o)[0]
N = len(ad)

T = 0x0b2818
# entries until zero-len terminator
pairs = []
k = 0
while True:
    off, ln = u32a(T + 8*k), u32a(T + 8*k + 4)
    pairs.append((off, ln))
    k += 1
    if ln == 0 or k > 300: break
print(f'{len(pairs)} entries (incl terminator); sum lens 0x{sum(l for _,l in pairs):x}')

def validate(base):
    pos = base; nok = 0
    for kk, (off, ln) in enumerate(pairs):
        if ln == 0: continue
        is_time = (kk % 2 == 0)
        if is_time:
            n = ln // 4
            w = [u32a(pos + 4*j) for j in range(n)]
            if not all(w[i] < w[i+1] for i in range(n-1)) or w[-1] >= 2_000_000:
                return nok, pos, f'entry{kk} time'
        else:
            if ln % 16 == 0 and ln >= 0x20:
                m = ln // 16
                for i in range(m):
                    q = [f32a(pos + 16*i + 4*c) for c in range(4)]
                    nr = math.sqrt(sum(x*x for x in q))
                    if not (0.95 < nr < 1.05): return nok, pos, f'entry{kk} quat{i} n={nr:.3f}'
            elif ln % 12 == 0:
                m = ln // 12
                for i in range(m):
                    v = [f32a(pos + 12*i + 4*c) for c in range(3)]
                    if max(abs(x) for x in v) > 1e5: return nok, pos, f'entry{kk} vec3'
            else:
                return nok, pos, f'entry{kk} len 0x{ln:x}'
        nok += 1; pos += ln
    return nok, pos, 'OK'

for delta in (0x4dc + 8, 0x4e0, 0x4e0 + 4, 0x4e0 + 8, 0x4e0 + 12):
    base = T + delta
    nok, pos, why = validate(base)
    print(f'base 0x{base:06x} (T+0x{delta:x}): {nok}/{len(pairs)} {why}')
    if why == 'OK':
        json.dump(dict(table=T, base=base, end=pos, pairs=pairs),
                  open('/home/z/my-project/scripts/s34_t1_rundec.json', 'w'))
        break
