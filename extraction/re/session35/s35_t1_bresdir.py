#!/usr/bin/env python3
"""S35 T1a11: parse BRES named-object directory @0xb544 + segment container
head @0xccf4 + string pool; establish the object graph in the file."""
import struct

AD = '/tmp/my-project/work/data/batman_anims.bdae'
ad = open(AD, 'rb').read()
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]
N = len(ad)

def cstr(o):
    e = ad.find(b'\0', o)
    return ad[o:e].decode('latin1') if 0 < e - o < 120 else f'<{e-o}>'

print('=== string pool @0x1e70.. ===')
for o in range(0x1e70, 0x1f60, 16):
    print(f'  0x{o:06x}: {ad[o:o+16]!r}')

print('\n=== named-object directory from 0xb544 ===')
o = 0xb544
for k in range(24):
    so, ty, ptr = u32a(o), u32a(o + 4), u32a(o + 8)
    nm = cstr(0x1e70 + so) if so < 0x2000 else f'so={so}'
    print(f'  [{k:2d}] @0x{o:x}: stroff={so:5d} type={ty} ptr=0x{ptr:6x}  name={nm!r}')
    o += 12
    if ptr == 0 or ptr >= N: break

print('\n=== segment container head 0xcce0..0xcd40 ===')
for k in range(0xcce0, 0xcd40, 16):
    vals = [u32a(k + 4 * j) for j in range(4)]
    print(f'  0x{k:06x}: ' + ' '.join(f'{v:11d}' for v in vals) + '   ' + ' '.join(f'{v:08x}' for v in vals))

print('\n=== zone 0x114c0..0x11590 (after 656 records, before clip list) ===')
for k in range(0x11480, 0x11590, 16):
    vals = [u32a(k + 4 * j) for j in range(4)]
    print(f'  0x{k:06x}: ' + ' '.join(f'{v:11d}' for v in vals) + '   ' + ' '.join(f'{v:08x}' for v in vals))
