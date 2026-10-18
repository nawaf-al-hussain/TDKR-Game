#!/usr/bin/env python3
"""S35 T1a10: dump root structure zone around 0xb494 + BRES header,
find the segment container and the 0x20-stride clip entry array."""
import struct

AD = '/tmp/my-project/work/data/batman_anims.bdae'
ad = open(AD, 'rb').read()
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]
N = len(ad)

def dump(o, n, label):
    print(f'--- {label} @0x{o:x} ---')
    for k in range(0, n, 16):
        vals = [u32a(o + k + 4 * j) for j in range(4)]
        print(f'  0x{o+k:06x}: ' + ' '.join(f'{v:10d}' for v in vals) + '   ' + ' '.join(f'{v:08x}' for v in vals))

dump(0xb400, 0x200, 'root zone around clip container 0xb494')
dump(0, 0x100, 'file header')

# search for any u32 == 0xcd00 in first 0x10000
hits = []
for o in range(0, 0x10000, 4):
    if u32a(o) == 0xcd00:
        hits.append(o)
print('u32==0xcd00 hits in 0..0x10000:', [f'0x{x:x}' for x in hits])
for h in hits[:8]:
    dump(h - 0x20, 0x60, f'context around 0x{h:x}')
