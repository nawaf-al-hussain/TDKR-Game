#!/usr/bin/env python3
"""S35 T1a18: dump the 78 channel entries (0x20-stride @0xb544) and the
channel objects (0xbf04+) with their strings; plus clip-entry name strings."""
import struct

AD = '/tmp/my-project/work/data/batman_anims.bdae'
ad = open(AD, 'rb').read()
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]
N = len(ad)

def cstr(v):
    if 0 < v < N:
        e = ad.find(b'\0', v)
        if 0 < e - v < 90:
            return ad[v:e].decode('latin1')
    return None

print('=== 78 channel entries @0xb544 (0x20 stride) ===')
for k in range(78):
    o = 0xb544 + k * 0x20
    vals = [u32a(o + 4 * j) for j in range(8)]
    s1 = cstr(vals[0])
    sub = vals[4]
    if sub and sub < N:
        n1, ty, n2 = u32a(sub), u32a(sub + 4), u32a(sub + 8)
        print(f'  [{k:2d}] @0x{o:x}: name0={s1!r:32} sub=0x{sub:x} [sub+0]={cstr(n1)!r} type={ty} [sub+8]={cstr(n2)!r}')
    else:
        print(f'  [{k:2d}] @0x{o:x}: ' + ' '.join(f'{v:9d}' for v in vals))

print('\n=== clip name strings @0x2ff8 area ===')
for off in (0x2ff8, 0x300c, 0x3028, 0x3044):
    print(f'  0x{off:x}: {cstr(off)!r}')

print('\n=== string zone head 0x1e00..0x1e70 ===')
print(' ', ad[0x1e00:0x1e78])
