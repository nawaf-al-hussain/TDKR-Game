#!/usr/bin/env python3
"""s54 T1 step 18: parse ELF sections + .rel.dyn to find how the .bss glide
statics are referenced (GOT entries / ABS32 pool relocs), and locate the
initializing code."""
import struct

SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()
e_shoff = struct.unpack_from('<I', data, 32)[0]
e_shentsize = struct.unpack_from('<H', data, 46)[0]
e_shnum = struct.unpack_from('<H', data, 48)[0]
e_shstrndx = struct.unpack_from('<H', data, 50)[0]

def sh(i):
    p = e_shoff + i * e_shentsize
    name, typ, flags, addr, off, size = struct.unpack_from('<6I', data, p)
    return name, typ, flags, addr, off, size

strtab_off = sh(e_shstrndx)[4]
def nm(x):
    e = data.index(b'\0', strtab_off + x)
    return data[strtab_off + x:e].decode()

sections = {}
for i in range(e_shnum):
    name, typ, flags, addr, off, size = sh(i)
    sections[nm(name)] = (typ, addr, off, size)
    if typ != 8:  # not NOBITS
        print('%-18s type=%2d addr=%#x off=%#x size=%#x' % (nm(name), typ, addr, off, size))
    else:
        print('%-18s type= 8(BSS) addr=%#x size=%#x' % (nm(name), addr, size))

# .rel.dyn parse
rel = sections.get('.rel.dyn')
if rel:
    _, addr, off, size = rel
    n = size // 8
    abs32 = []
    relative = []
    for k in range(n):
        r_offset, r_info = struct.unpack_from('<II', data, off + 8 * k)
        typ = r_info & 0xff
        if typ == 2:  # R_ARM_ABS32
            addend = struct.unpack_from('<I', data, v2of(r_offset))[0] if (v2of := (lambda v: next((o + (v - va) for va, o, sz in [(s[0], s[1], s[2]) for s in [(0, 0, 0xbbe1ec), (0xbbf930, 0xbbe930, 0x52f04)] if s[0] <= v < s[0] + s[2]]), None)))() else None
            abs32.append((r_offset, addend))
        elif typ == 23:
            relative.append(r_offset)
    print('\nABS32 relocs:', len(abs32), 'RELATIVE:', len(relative))
    TARGETS = {0xc17d5c: 's_glidePitchMin', 0xc17d60: 's_glidePitchMax',
               0xc17d64: 's_glideRollMax', 0xc17d68: 's_glideDeltaYawMax',
               0xc17d6c: 's_glideYawCoef', 0xc17d70: 's_glidePitchCoef',
               0xc17d74: 's_glideRollCoef', 0xc17d78: 's_glidePitchAutoLevelingCoef',
               0xc17d7c: 's_glideRollAutoLevelingCoef', 0xc17d80: 's_glideDeadAngle',
               0xc0abc0: 'k_glideWallEvadeDistance', 0xc0abc4: 'k_glideWallEvadeMinDistance',
               0xc0abc8: 'k_glideWallEvadeMaxAngle'}
    print('\nABS32 relocs whose addend is a glide static:')
    for ro, ad in abs32:
        if ad in TARGETS:
            print('  reloc @%#x -> %s (%#x)' % (ro, TARGETS[ad], ad))
    # also check .got contents
    got = sections.get('.got')
    if got:
        _, gaddr, goff, gsize = got
        print('\n.got entries holding glide statics:')
        for k in range(0, gsize, 4):
            v = struct.unpack_from('<I', data, goff + k)[0]
            if v in TARGETS:
                print('  got %#x = %s' % (gaddr + k, TARGETS[v]))
