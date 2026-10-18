#!/usr/bin/env python3
"""S34 T1: test exact rule data_k = BASE + off_k.
Hypothesis A: base = 0x536e4 (off relative to first anchor, first 0x9c = header).
Validate: time streams ascending-ticks; quat streams unit-norm xyzw;
vec3 streams finite. Count exact-rule hits vs r23's re-anchoring walk."""
import struct, math, json
import numpy as np

AD = '/tmp/my-project/work/data/batman_anims.bdae'
ad = open(AD, 'rb').read()
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]
f32a = lambda o: struct.unpack_from('<f', ad, o)[0]

pairs = json.load(open('/home/z/my-project/scripts/s34_t1_pairs.json'))
names, P = pairs['names'], pairs['pairs']

def dump(o, n=40):
    b = ad[o:o+n]
    return ' '.join(f'{x:02x}' for x in b)

# dump the pre-anchor zone (candidate header/chunk dir)
print('=== zone 0x53648..0x536e4 (0x9c bytes) ===')
for o in range(0x53648, 0x536e4, 16):
    print(f'  0x{o:06x}: {dump(o,16)}')

# hypothesis: pool base = 0x536e4 - 0x9c = 0x53648; data_k = base + off_k
for base in (0x53648, 0x536e4):
    t_ok = t_tot = q_ok = q_tot = v_ok = v_tot = 0
    for k, (off, ln) in enumerate(P):
        if not ln: continue
        p = base + off
        nm = names[k // 2] if k // 2 < len(names) else '?'
        is_time = (k % 2 == 0)
        if is_time:
            t_tot += 1
            n = ln // 4
            w = [u32a(p + 4 * j) for j in range(n)]
            if all(w[i] < w[i+1] for i in range(n-1)) and w[-1] < 2_000_000:
                t_ok += 1
        else:
            if ln % 16 == 0 and ln >= 0x20:  # quat
                q_tot += 1
                m = ln // 16
                q = np.array([f32a(p + 16*i + 4*c) for i in range(m) for c in range(4)])
                q = q.reshape(m, 4)
                nrm = np.linalg.norm(q, axis=1)
                if np.all(np.abs(nrm - 1) < 0.02): q_ok += 1
            elif ln % 12 == 0:  # vec3
                v_tot += 1
                m = ln // 12
                v = np.array([f32a(p + 12*i + 4*c) for i in range(m) for c in range(3)])
                if np.all(np.abs(v) < 1e5): v_ok += 1
    print(f'\nBASE 0x{base:x}: time {t_ok}/{t_tot} asc, quat {q_ok}/{q_tot} unit, '
          f'vec3 {v_ok}/{v_tot} finite')

# also scan a few alternative bases around, maximizing time-ascending hits
best = []
for base in range(0x53200, 0x53800, 4):
    ok = 0
    for k in range(0, len(P), 2):
        off, ln = P[k]
        if not ln: continue
        p = base + off
        if p + ln > len(ad): continue
        n = ln // 4
        w = [u32a(p + 4 * j) for j in range(n)]
        if all(w[i] < w[i+1] for i in range(n-1)) and w[-1] < 2_000_000:
            ok += 1
    best.append((ok, base))
best.sort(reverse=True)
print('\ntop-5 bases by time-asc hits:', [(f'0x{b:x}', n) for n, b in best[:5]])
