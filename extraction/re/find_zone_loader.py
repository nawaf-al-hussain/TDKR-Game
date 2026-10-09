#!/usr/bin/env python3
"""Disassemble the zone-payload loader function(s) that reference the
stream_info/batch_info/lod_table string block (anchor pool @0xc75d4/0xc75d8).
Goal: exact batch_info.bin record layout (batch -> material index)."""
import struct
import sys

LIB = '/home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
d = open(LIB, 'rb').read()

# ---- read symtab, find FUNC symbols ----
e_shoff = struct.unpack_from('<I', d, 0x20)[0]
e_shentsize, e_shnum = struct.unpack_from('<HH', d, 0x2e)
secs = []
for i in range(e_shnum):
    p = e_shoff + i * e_shentsize
    vals = struct.unpack_from('<10I', d, p)
    secs.append(vals)
# shstrtab
shstr_off = secs[secs_e_shstrndx := e_shnum - 1][4]  # last section is shstrtab
def secname(x):
    end = d.index(b'\x00', shstr_off + x)
    return d[shstr_off + x:end].decode()
symtab = strtab = None
for s in secs:
    if secname(s[0]) == '.symtab':
        symtab = s
    if secname(s[0]) == '.strtab':
        strtab = s
def strname(x):
    end = d.index(b'\x00', strtab[4] + x)
    return d[strtab[4] + x:end].decode('latin1')

funcs = []
nsym = symtab[5] // 16
for i in range(nsym):
    p = symtab[4] + i * 16
    nm, val, sz, info, oth = struct.unpack_from('<IIIBB', d, p)
    if info & 0xf == 2 and sz > 0:  # STT_FUNC
        funcs.append((val, sz, strname(nm)))
funcs.sort()

def containing(addr):
    for val, sz, nm in funcs:
        if val <= addr < val + sz:
            return val, sz, nm
    # nearest below
    best = None
    for val, sz, nm in funcs:
        if val <= addr and (best is None or val > best[0]):
            best = (val, sz, nm)
    return best

for a in (0xc75d4, 0xc75d8):
    print(f'pool 0x{a:x} in:', containing(a))

# also check known zone ctors
for val, sz, nm in funcs:
    if 'LODStreaming' in nm or 'DoubleBufferedDynamic' in nm or ('Zone' in nm and 'Load' in nm):
        print(f'FUNC 0x{val:x} +0x{sz:x} {nm}')
