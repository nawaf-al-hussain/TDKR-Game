#!/usr/bin/env python3
"""Properly scan .rel.dyn for R_ARM_RELATIVE slots whose addend points into
the zone-string block; then find code referencing those slots."""
import struct

LIB = '/home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
d = open(LIB, 'rb').read()

# segments
phoff = struct.unpack_from('<I', d, 0x1c)[0]
phentsize, phnum = struct.unpack_from('<HH', d, 0x2a)
segs = []
for i in range(phnum):
    p = phoff + i * phentsize
    ptype, = struct.unpack_from('<I', d, p)
    off, vaddr, paddr, filesz, memsz = struct.unpack_from('<5I', d, p + 8)
    if ptype == 1:
        segs.append((off, vaddr, filesz))

def v2f(v):
    for off, va, sz in segs:
        if va <= v < va + sz:
            return off + (v - va)
    return None

rel_off, rel_size = 0x351fc, 0x6f118
n = rel_size // 8
strs = {0xb4070c: 'stream_info', 0xb4071c: 'bih_data', 0xb4072c: 'bih_struct',
        0xb4073c: 'batch_info', 0xb4074c: '_materials.bdae', 0xb4075c: 'lod_table',
        0xb4076c: 'lod_data', 0xb4077c: 'lod_selector', 0xb406fc: '_inorm',
        0xb40704: '.zip', 0xb40788: '.bin'}
slots = {}
for i in range(n):
    off, info = struct.unpack_from('<II', d, rel_off + i * 8)
    if (info & 0xff) != 23:
        continue
    fo = v2f(off)
    if fo is None:
        continue
    addend = struct.unpack_from('<I', d, fo)[0]
    if addend in strs:
        slots.setdefault(strs[addend], []).append((off, addend))
for k, v in slots.items():
    print(k, [f'slot 0x{o:x}' for o, a in v])
