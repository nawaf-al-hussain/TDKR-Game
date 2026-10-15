#!/usr/bin/env python3
"""T2: BRES node tree — the Bip01 bone hierarchy with parent indices."""
import struct

d = open('/home/z/my-project/work/actors/batman.bdae', 'rb').read()
u16 = lambda o: struct.unpack_from('<H', d, o)[0]
u32 = lambda o: struct.unpack_from('<I', d, o)[0]
f32 = lambda o: struct.unpack_from('<f', d, o)[0]

def cstrz(off):
    e = d.index(b'\0', off)
    return d[off:e].decode('latin1')

# NitroBRES-style: header 'BRES' bom ver root(ns) ns ss ds; nodes at +0x18?
# header: root=0x3c @+8; nodes likely start @0x40 with 0x1C-byte stride?
# Try the standard nnsbmb layout: nodes 32 B: [kind][left][right][name]...
# strings pool @0x868 (after the node array 0x40..0x868 = 2088 B / 32 = 65.25)
# try 0x1C stride: 2088/28 = 74.6; try nodes = 0x18: 87 — hmm.
# The 'BATMAN' string @0x882 (pool) and nodes before it.
# Let's decode node records assuming 0x1C stride from 0x40:
print('candidate node arrays:')
for stride in (0x18, 0x1C, 0x20, 0x24):
    n = (0x868 - 0x40) // stride
    print(f'  stride {stride:#x}: {n} nodes')

# dump words at 0x40 with 0x1C stride and try name resolution:
# name = u32 whose low 24 bits = index into a string table; the table
# entries at 0x22d8? (from the header word @0x20 = 0x22d8)
ST = 0x22d8
def name_at(idx):
    # try: name idx -> u32 offset at ST + idx*4 -> offset from POOL
    POOL = 0x868
    try:
        o = u32(ST + (idx & 0xFFFFFF) * 4)
        if o < 0x20000:
            return cstrz(POOL + o)
    except Exception:
        pass
    return None

# Scan 0x40..0x868 as 28-B nodes: [kind][left][right][name][d1][d2][d3][fl]
N = (0x868 - 0x40) // 0x1C
print(f'\ntrying {N} nodes @0x40 stride 0x1C:')
for i in range(min(N, 80)):
    o = 0x40 + i * 0x1C
    kind = u32(o)
    a = u32(o + 4)
    b = u32(o + 8)
    nmw = u32(o + 12)
    nm = name_at(nmw & 0xFFFFFF)
    if nm:
        print(f'  node {i:3} @{o:#x} kind={kind:5x} ptr=({a:5},{b:5}) '
              f'nmw={nmw:8x} name={nm[:36]!r}')
