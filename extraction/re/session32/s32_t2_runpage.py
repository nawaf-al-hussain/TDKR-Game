#!/usr/bin/env python3
"""S32 T2j: page table @0x834280 -> packed streams; decode _008_run root."""
import struct

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

def plausible_pair(off):
    a, b = u32(off), u32(off + 4)
    return (0x1000 < a < 0xb500 and cstr(a) is not None and 0 < b < 0x20000)

for SITE in (0x834280,):
    s = SITE
    while plausible_pair(s - 8):
        s -= 8
    e = SITE
    while plausible_pair(e):
        e += 8
    pairs = [(u32(o), u32(o + 4), cstr(u32(o))) for o in range(s, e, 8)]
    print(f'page table @0x{s:x}..0x{e:x}: {len(pairs)} pairs, '
          f'total {sum(p[1] for p in pairs)} B')
    names = {}
    for a, b, nm in pairs:
        names.setdefault(nm, []).append(b)
    for nm, sizes in list(names.items())[:14]:
        print(f'  {nm!r}: sizes {sizes[:8]}')
    # streams packed after table?
    off = e
    print(f'\nfirst f32s after table @0x{off:x}:',
          [round(f32(off + 4 * j), 4) for j in range(8)])
    # try per-pair stride classification on the first 12 pairs
    ok_counts = {'q+t': 0, 'v3+t': 0, 's+t': 0}
    for a, b, nm in pairs[:12]:
        for lbl, stride in (('q+t', 20), ('v3+t', 16), ('s+t', 8)):
            if b % stride == 0 and b // stride > 0:
                ok_counts[lbl] += 1
    print('stride divisibility (first 12):', ok_counts)
    # locate _008_run pair index
    for k, (a, b, nm) in enumerate(pairs):
        if nm == '_008_run':
            print(f'\n_008_run = pair {k}: size {b}')
            st = e + sum(p[1] for p in pairs[:k])
            print(f'  candidate stream @0x{st:x}')
            n16 = b // 16
            if b % 16 == 0:
                keys = []
                for i in range(n16):
                    v = struct.unpack_from('<3f', d, st + 16 * i)
                    t = u32(st + 16 * i + 12)
                    keys.append((v, t))
                print('  [vec3][tick] keys:', [(tuple(round(x, 3) for x in v), t)
                                               for v, t in keys])
    break
