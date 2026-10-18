#!/usr/bin/env python3
"""S35 T1a6: find direct BL/BLX callers of key animation functions.
ARM (bl) and Thumb (bl) encodings scanned across executable segments."""
import capstone, struct, json, sys

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

def v2f(v):
    for vaddr, off, filesz in segs:
        if vaddr <= v < vaddr + filesz:
            return off + (v - vaddr)
    return None

# load symbols for caller naming
syms = json.load(open('/tmp/my-project/work/so_syms.json'))['by_addr']

def fname(va):
    got = syms.get(f'0x{va:x}')
    if got:
        for n in got:
            if not n.startswith('$'):
                return n[:90]
        return got[0][:90]
    return None

def nearest_name(va):
    # find symbol at or before va (walk back up to 0x2000)
    for back in range(0, 0x2000, 4):
        n = fname(va - back)
        if n:
            return f'{n}+0x{back:x}' if back else n
    return f'sub_{va:08x}'

targets = {
    0x7565bc: "getAnimationBlock(key)",
    0x756350: "getAnimationBlock(key,out)",
    0x78fbf8: "getAnimationBlock./",
    0x755834: 'CAnimationBlock::ctor#1(db,clip,int)',
    0x755ba0: 'CAnimationBlock::ctor#2(db,clip,seg)',
    0x7bb770: 'getAnimationSegment(int)',
    0x7badfc: 'getAnimation(name,type,type)',
    0x78e53c: 'SAnimationSegment::getData',
}

# ARM BL: cond(4) 101L(5) imm24 ; imm = signext(imm24)*4 ; target = pc+8+imm
found = []
for vaddr, off, filesz in segs:
    end = filesz - 4
    i = 0
    buf = d[off:off + filesz]
    while i < end:
        w = struct.unpack_from('<I', buf, i)[0]
        if (w & 0x0F000000) == 0x0B000000:  # BL (ARM)
            imm = w & 0x00FFFFFF
            if imm & 0x800000: imm -= 0x1000000
            tgt = vaddr + i + 8 + imm * 4
            if tgt in targets:
                found.append((vaddr + i, tgt, 'ARM'))
        i += 4
# Thumb BL: F000 F800 pairs; scan halfwords
for vaddr, off, filesz in segs:
    buf = d[off:off + filesz]
    for i in range(0, filesz - 4, 2):
        hw1 = struct.unpack_from('<H', buf, i)[0]
        if (hw1 & 0xF800) == 0xF000:
            hw2 = struct.unpack_from('<H', buf, i + 2)[0]
            if (hw2 & 0xF800) == 0xF800:  # BL
                imm = ((hw1 & 0x7FF) << 12) | (hw2 & 0x7FF)
                if imm & 0x400000: imm -= 0x800000
                tgt = vaddr + i + 4 + imm * 2
                if tgt in targets:
                    found.append((vaddr + i, tgt, 'THUMB'))

found.sort()
print(f'{len(found)} direct calls found')
for site, tgt, mode in found:
    # thumb sites have bit0 set on targets; caller address even
    name = nearest_name(site)
    print(f'  0x{site:08x} ({mode}) -> {targets[tgt]}  in {name}')
