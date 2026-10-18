#!/usr/bin/env python3
"""S33 T1: dump the 156-entry stream table @0x53200; solve the base offset."""
import struct

D = '/tmp/my-project/work/data/batman_anims.bdae'
d = open(D, 'rb').read()
u32 = lambda o: struct.unpack_from('<I', d, o)[0]

def cstr(v):
    if 0 < v < len(d):
        e = d.find(b'\0', v)
        if 0 < e - v < 90:
            try: return d[v:e].decode('latin1')
            except Exception: pass

# named groups (channel names in order)
names = []
o = 0xb53c
while True:
    w = struct.unpack_from('<8I', d, o)
    if not (w[2] and cstr(w[2]) and w[3] == 1 and w[5] == 1): break
    names.append(cstr(w[2]))
    o += 32
print(f'{len(names)} channel names; first 5: {names[:5]}')

ENT = 0x53200
pairs = [(u32(ENT + 8 * k), u32(ENT + 8 * k + 4)) for k in range(156)]
print('\nall 156 (off, len) entries:')
tot_t = tot_v = 0
for k, (a, b) in enumerate(pairs):
    nm = names[k // 2] if k // 2 < len(names) else '?'
    kind = 'TIME' if k % 2 == 0 else 'VAL '
    print(f'  [{k:3d}] {nm:38s} {kind} off=0x{a:05x} len=0x{b:x} ({b//4} w)')
    if k > 30: break

# tiling check: sort distinct offsets, see if len covers gap to next
offs = sorted({a for a, b in pairs})
print(f'\ndistinct offsets: {len(offs)}; range 0x{offs[0]:x}..0x{offs[-1]:x}')
print('consecutive distinct offsets with the max entry len at that offset:')
len_at = {}
for a, b in pairs:
    len_at[a] = max(len_at.get(a, 0), b)
gaps_ok = gaps_bad = 0
for i in range(len(offs) - 1):
    a, a2 = offs[i], offs[i + 1]
    L = len_at[a]
    if a + L <= a2: gaps_ok += 1
    else: gaps_bad += 1
print(f'  off+len <= next_off: {gaps_ok}, overflow: {gaps_bad}')
print('first 24 distinct offsets + lens:',
      [(hex(a), hex(len_at[a])) for a in offs[:24]])

# hypothesis: base + off = data; try bases so that first TIME entry (0x9c,0xa8)
# hits a 42-tick array [0..1850] and first VAL (0x4dc,0x1f8) hits 42 vec3
# candidate bases from known arrays: 0x536e8 (ticks), quat/vec3 arrays unknown
# scan: for each 4-aligned base in [0x50000..0x60000], check
# base+0x9c: 42 ascending ticks; base+0x4dc: 42 smooth vec3
import numpy as np
N = len(d) // 4
u32all = np.frombuffer(d[:N * 4], np.uint32)
f32all = np.frombuffer(d[:N * 4], np.float32)
best = []
for base in range(0x40000, 0x70000, 4):
    ta = base + 0x9c
    if ta + 168 > len(d): continue
    w = u32all[ta // 4: ta // 4 + 42]
    if not (w[0] == 0 and np.all(np.diff(w.astype(np.int64)) > 0)
            and w[-1] == 1850):
        continue
    va = base + 0x4dc
    v = f32all[va // 4: va // 4 + 126].reshape(42, 3)
    dv = np.abs(np.diff(v.astype(np.float64), axis=0)).max()
    best.append((base, dv))
print(f'\nbase candidates (ticks[0..1850] at base+0x9c): {len(best)}')
for b, dv in best[:10]:
    print(f'  base 0x{b:x} vec3 max|delta|={dv:.4f}')
