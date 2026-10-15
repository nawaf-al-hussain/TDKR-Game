#!/usr/bin/env python3
"""T2: locate the -mesh-skin section: bone palette + inverse-bind matrices."""
import struct

d = open('/home/z/my-project/work/actors/batman.bdae', 'rb').read()
u32 = lambda o: struct.unpack_from('<I', d, o)[0]
f32 = lambda o: struct.unpack_from('<f', d, o)[0]

# section name strings live in a pool; find their offsets & the section table
# the BRES node tree @0x40: walk kind/left/right/name/data
def cstr(off):
    e = d.index(b'\0', off)
    return d[off:e].decode('latin1')

# scan the whole file for section-name strings and their preceding offsets
names = {}
for nm in (b'BATMAN-mesh', b'BATMAN-mesh-skin', b'CAPE-mesh',
           b'CAPE-mesh-skin', b'BATMAN-skeleton', b'Bip01', b'BATMAN',
           b'CAPE'):
    i = d.find(nm)
    if i >= 0:
        names[nm.decode()] = i
        print(f'{nm.decode():22} @ {i:#x}  (prev u32 {u32(i-4):#x})')

# the node entries referencing these names: BRES nodes are 0x20 B:
# [kind][left][right][name(u32)][d1][d2][d3][d4(u16),num(u16)]?
# scan for nodes whose name-pointer resolves to the pool
POOL = 0x868          # string pool base guess
def pool_str(idx):
    o = u32(POOL + idx * 4)
    return cstr(POOL + o) if o < 0x10000 else '?'

# The data pointers: find big float-array regions (candidate -skin blocks)
# heuristic: runs of >= 16 consecutive f32 with |f| in [0, 2] and 4x4 blocks
# whose translation column is in [0, 2]
runs = []
o = 0x4a58 + 0x6c + 0x1c5bc + 0x2aa8   # after batman mesh+indices
print(f'\nscanning from {o:#x} for the CAPE mesh / skin blocks...')
while o < len(d) - 64:
    v = u32(o)
    if v in (0x100, 0xf8):
        w = [u32(o + 4 * k) for k in range(8)]
        if w[1] in (0xf8, 0x100) or w[0] == 0x100:
            print(f'  block-like @ {o:#x}: {w[:8]}')
            o += 0x100
    o += 4

# look at the very end of the file (skins often trail)
print('\nfile tail words:')
for o in range(len(d) - 128, len(d), 16):
    print(f'  {o:#x}: ' + ' '.join(f'{u32(o + k):08x}' for k in range(0, 16, 4)))
