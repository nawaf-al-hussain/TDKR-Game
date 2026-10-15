#!/usr/bin/env python3
"""T2 engine-driven decode of batman.bdae.

Evidence chain:
1. glitch attribute registry (getStringsInternal table): 0 Position,
   1 TexCoord0, 2 TexCoord1, ... 16 Normal, 17 Color0, ... 27 SkinWeights,
   28 SkinIndices, 29 InstanceId.
2. BRES sections: '-mesh' carries interleaved vertex streams with
   descriptors; '-mesh-skin' carries per-bone data; node section carries
   the Bip01 hierarchy.
3. Output: descriptor -> attribute-id mapping candidates, skeleton
   hierarchy, per-bone inverse-bind matrix hypothesis with bind-pose
   consistency check (matrix translation == node position).
"""
import struct
import sys
import json
import numpy as np

BDAE = '/home/z/my-project/work/data/batman.bdae'
d = open(BDAE, 'rb').read()
print(f'batman.bdae: {len(d)} B')

# ---- BRES section table ----
# Session-24: 'BRES' feff then sections with named entries ('BATMAN-mesh' etc.)
assert d[:4] == b'BRES', d[:8]
u16 = lambda o: struct.unpack_from('<H', d, o)[0]
u32 = lambda o: struct.unpack_from('<I', d, o)[0]
ver = u16(4)
print(f'version 0x{ver:x}')

# BRES layout (Nintendo-ish): u16 version, u16 ???, u32 root, u16 ns, u16 ss,
# u16 ds; then string pool / string table / entries
ns, ss, ds = u16(10), u16(12), u16(14)
root = u32(8)
print(f'root=0x{root:x} ns={ns} ss={ss} ds={ds}')


def parse_node(off):
    """BRES node: u32 kind, u32 left/right/child(sibling), u32 name
    (u24 idx,u8 flag), u32 data1, u32 data2, u32 data3, u16 data4, u16
    numChildren... varies. Walk generically."""
    kind = u32(off)
    left = u32(off + 4)
    right = u32(off + 8)
    name = u32(off + 12)
    d1 = u32(off + 16)
    d2 = u32(off + 20)
    d3 = u32(off + 24)
    return dict(kind=kind, left=left, right=right, name=name,
                d1=d1, d2=d2, d3=d3)


# string pool at root+8? try: entries pointed by name -> ss pool
def getstr(idx):
    # string table entries u32 offsets into ss pool
    s = ss  # pool base
    off = u32(0x20 + idx * 4) if idx < 4096 else 0
    end = d.index(b'\0', s + off)
    return d[s + off:end].decode('latin1')


nodes = {}
# walk the root node tree breadth-first with guards
stack = [(root, 0)]
seen = set()
while stack:
    off, depth = stack.pop()
    if off in seen or off < root or off >= len(d) - 32:
        continue
    seen.add(off)
    n = parse_node(off)
    try:
        nm = getstr(n['name'] & 0xFFFFFF)
    except Exception:
        nm = f'<name {n["name"]:#x}>'
    nodes[off] = (nm, n)
    if depth < 3:
        if n['left'] not in seen:
            stack.append((n['left'], depth + 1))
        if n['right'] not in seen:
            stack.append((n['right'], depth + 1))
        if n['d2'] not in seen:
            stack.append((n['d2'], depth + 1))
print(f'walked {len(nodes)} nodes; names sample:')
interesting = []
for off, (nm, n) in sorted(nodes.items()):
    if 'mesh' in nm.lower() or 'skin' in nm.lower() or 'node' in nm.lower():
        interesting.append((off, nm, n))
        print(f'  @0x{off:x} {nm} kind={n["kind"]:#x} d1={n["d1"]:#x} '
              f'd2={n["d2"]:#x} d3={n["d3"]:#x}')
