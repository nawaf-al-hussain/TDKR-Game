#!/usr/bin/env python3
"""S34 T1: validate the ZERO-PAD contiguous layout from 0x536e4 for ALL 156
streams (time ascending, quats unit-norm, vec3 finite). If all pass, the file
rule is data_k = 0x536e4 + cumsum(lens). Also compare off_k vs cumsum and
off_k vs cumsum-of-PREVIOUS-CHANNEL (2-stride) to decode off semantics."""
import struct, json, math
import numpy as np

AD = '/tmp/my-project/work/data/batman_anims.bdae'
ad = open(AD, 'rb').read()
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]
f32a = lambda o: struct.unpack_from('<f', ad, o)[0]
P = json.load(open('/home/z/my-project/scripts/s34_t1_pairs.json'))
names, pairs = P['names'], P['pairs']

BASE = 0x536e4
pos = BASE
fails = []
cum = 0
rows = []
for k, (off, ln) in enumerate(pairs):
    nm = names[k // 2] if k // 2 < len(names) else f'?{k}'
    is_time = (k % 2 == 0)
    p = pos
    ok = True; why = ''
    if ln:
        if is_time:
            n = ln // 4
            w = [u32a(p + 4*j) for j in range(n)]
            if not all(w[i] < w[i+1] for i in range(n-1)) or w[-1] >= 2_000_000:
                ok = False; why = f'ticks not asc (first {w[:3]} last {w[-1]})'
        elif ln % 16 == 0 and ln >= 0x20:
            m = ln // 16
            for i in range(m):
                q = [f32a(p + 16*i + 4*c) for c in range(4)]
                nr = math.sqrt(sum(x*x for x in q))
                if not (0.95 < nr < 1.05) or max(abs(x) for x in q) > 1.05:
                    ok = False; why = f'quat[{i}] norm {nr:.3f}'; break
        elif ln % 12 == 0:
            m = ln // 12
            for i in range(m):
                v = [f32a(p + 12*i + 4*c) for c in range(3)]
                if max(abs(x) for x in v) > 1e5:
                    ok = False; why = f'vec3[{i}] huge {v}'; break
        else:
            ok = False; why = 'bad len'
    rows.append((k, nm, is_time, off, ln, p, ok, why))
    if not ok: fails.append((k, nm, why))
    pos += ln

n_pass = sum(1 for r in rows if r[6])
print(f'contiguous zero-pad layout: {n_pass}/{len(rows)} streams validate')
for k, nm, why in fails[:20]:
    print(f'  FAIL k={k} {nm}: {why}')

print(f'\nfile end: 0x{pos:x} (base 0x{BASE:x} + 0x{pos-BASE:x}; sum lens 0x{sum(l for _,l in pairs):x})')

# off semantics: compare off_k to cumsum before entry k, and channel-level
print('\noff vs cumsum (entry-granularity), first 20:')
for k in range(0, 40, 2):
    _, nm, is_time, off, ln, p, ok, _ = rows[k]
    pre = sum(l for _, l in pairs[:k])
    print(f'  k={k:3d} {nm[:24]:24s} off=0x{off:05x} cum_before=0x{pre:05x} '
          f'diff=0x{off-pre:05x} len=0x{ln:03x}')

# channel granularity: off(2c) - off(2c') relations
print('\nchannel pairs (time off, value off, delta):')
for c in range(12):
    k = 2*c
    t_off, t_ln = pairs[k]; v_off, v_ln = pairs[k+1] if k+1 < 157 else (0, 0)
    print(f'  ch{c:2d} {names[c][:24]:24s} t=0x{t_off:05x}(0x{t_ln:03x}) '
          f'v=0x{v_off:05x}(0x{v_ln:03x}) v-t=0x{v_off-t_off if v_off>=t_off else 0:05x}')
