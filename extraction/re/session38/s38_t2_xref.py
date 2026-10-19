#!/usr/bin/env python3
"""Find callers of PVRTCDecompress (thunk 0x744148 / impl 0x746e34) via bl scan."""
import struct
SO = '/tmp/my-project/work/re29/libKRHP.so'
d = open(SO, 'rb').read()
phoff = struct.unpack_from('<I', d, 0x1c)[0]
phnum = struct.unpack_from('<H', d, 0x2c)[0]
segs = []
for i in range(phnum):
    o = phoff + i * 32
    p_type, p_offset, p_vaddr, _, p_filesz, _ = struct.unpack_from('<6I', d, o)
    if p_type == 1: segs.append((p_vaddr, p_offset, p_filesz))
def v2o(va):
    for vaddr, off, sz in segs:
        if vaddr <= va < vaddr + sz: return off + (va - vaddr)
    raise ValueError(hex(va))
def o2v(o):
    for vaddr, off, sz in segs:
        if off <= o < off + sz: return vaddr + (o - off)
    raise ValueError(hex(o))
targets = {0x744148: 'thunk', 0x746e34: 'impl'}
# scan text segment for bl/blx imm24 (ARM): encoding 0xEB/0xFA-0xFB
text = segs[1] if len(segs) > 1 else segs[0]
vaddr, off, sz = segs[2] if len(segs) > 2 else segs[1]
# scan the EXEC segment (find the one containing 0x746e34)
for vaddr, off, sz in segs:
    if vaddr <= 0x746e34 < vaddr + sz: break
hits = []
for o in range(off, off + sz - 4, 4):
    w = struct.unpack_from('<I', d, o)[0]
    cond = w >> 28
    if (w & 0x0F000000) in (0x0B000000, 0x0F000000 & 0x0F000000):
        if (w & 0x0F000000) == 0x0B000000 and cond != 0xF:
            imm = w & 0x00FFFFFF
            if imm & 0x800000: imm -= 0x1000000
            tgt = o2v(o) + 8 + imm * 4
            if tgt in targets:
                hits.append((o2v(o), targets[tgt]))
for va, t in hits:
    print(f'{va:08x}: bl {t}')
print('total', len(hits))
