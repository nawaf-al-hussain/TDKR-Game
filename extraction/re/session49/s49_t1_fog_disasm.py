#!/usr/bin/env python3
"""s49 T1d: static-read CWeatherManager fog defaults + SetLevelProperties field use."""
import struct
d = open('/tmp/my-project/work/re29/libKRHP.so', 'rb').read()

# parse ELF section headers to map vaddr
import struct as st
e_shoff, = st.unpack_from('<I', d, 0x20)
e_shentsize, e_shnum, e_shstrndx = st.unpack_from('<HHH', d, 0x2e)
secs = []
for i in range(e_shnum):
    o = e_shoff + i * e_shentsize
    name, typ, flags, addr, off, size = st.unpack_from('<IIIIII', d, o)
    secs.append((addr, off, size, typ))
def v2o(v):
    for addr, off, size, typ in secs:
        if typ and addr <= v < addr + size:
            return off + (v - addr)
    return None
def o2v(o):
    for addr, off, size, typ in secs:
        if typ and off <= o < off + size:
            return addr + (o - off)
    return None

# find symbol addresses from .symtab
symtab = None; strtab = None
for i, (addr, off, size, typ) in enumerate(secs):
    pass
# easier: use the existing elf_syms helper
import json, os
sy = json.load(open('/tmp/my-project/work/so_syms.json')) if os.path.exists('/tmp/my-project/work/so_syms.json') else None
print('so_syms type:', type(sy), (list(sy.keys())[:5] if isinstance(sy, dict) else len(sy)) if sy else None)
