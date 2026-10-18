#!/usr/bin/env python3
"""S36 T1d2: scan for BL to 0x1d17cc in .text (direct calls)."""
import struct

SO = '/tmp/my-project/work/re29/libKRHP.so'
d = open(SO, 'rb').read()
e_phoff = struct.unpack_from('<I', d, 0x1c)[0]
e_phentsize = struct.unpack_from('<H', d, 0x2a)[0]
e_phnum = struct.unpack_from('<H', d, 0x2c)[0]
segs = []
for i in range(e_phnum):
    o = e_phoff + i * e_phentsize
    p_type, p_offset, p_vaddr, p_paddr, p_filesz, p_memsz = struct.unpack_from('<6I', d, o)
    if p_type == 1 and p_filesz:
        segs.append((p_vaddr, p_offset, p_filesz))

TARGET = 0x1d17cc
callers = []
for vaddr, off, filesz in segs:
    blob = d[off:off + filesz]
    for i in range(0, len(blob) - 4, 4):
        w = struct.unpack_from('<I', blob, i)[0]
        if (w & 0x0F000000) == 0x0B000000:  # BL (any cond)
            imm = w & 0x00FFFFFF
            if imm & 0x800000: imm -= 0x1000000
            tgt = vaddr + i + 8 + imm * 4
            if tgt == TARGET:
                callers.append(vaddr + i)
print(f'BL callers of Create @0x{TARGET:x}:')
import json
syms = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session25/so_syms.json'))['by_addr']
for c in callers:
    # nearest symbol at or before
    print(f'  0x{c:08x}')
