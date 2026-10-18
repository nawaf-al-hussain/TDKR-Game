#!/usr/bin/env python3
"""S33 T1: disassemble CAnimationBlock ctor @0x755ba0 + callees."""
import capstone, struct, sys

SO = '/tmp/my-project/work/re29/libKRHP.so'
d = open(SO, 'rb').read()
# ELF32
ei_class = d[4]
e_phoff = struct.unpack_from('<I', d, 0x1c)[0]
e_phentsize = struct.unpack_from('<H', d, 0x2a)[0]
e_phnum = struct.unpack_from('<H', d, 0x2c)[0]
print(f'ELF class {ei_class} phoff 0x{e_phoff:x} phnum {e_phnum}')
segs = []
for i in range(e_phnum):
    o = e_phoff + i * e_phentsize
    p_type, p_offset, p_vaddr, p_paddr, p_filesz, p_memsz = struct.unpack_from('<6I', d, o)
    if p_type == 1:
        segs.append((p_vaddr, p_offset, p_filesz, p_memsz))
        print(f'LOAD vaddr 0x{p_vaddr:x} off 0x{p_offset:x} filesz 0x{p_filesz:x} memsz 0x{p_memsz:x}')

def v2f(v):
    for vaddr, off, filesz, memsz in segs:
        if vaddr <= v < vaddr + filesz:
            return off + (v - vaddr)
    return None

def disasm(va, n_bytes, label, mode=capstone.CS_MODE_ARM):
    fo = v2f(va)
    if fo is None:
        print(f'{label}: vaddr 0x{va:x} not mapped'); return
    md = capstone.Cs(capstone.CS_ARCH_ARM, mode)
    md.detail = False
    print(f'\n===== {label} @0x{va:x} (file 0x{fo:x}) =====')
    n = 0
    for ins in md.disasm(d[fo:fo + n_bytes], va):
        print(f'  0x{ins.address:08x}: {ins.mnemonic:8s} {ins.op_str}')
        n += 1
        if n > 400: break

# Thumb bit check: symbol addresses from so_syms.json if available
import json, os
syms = {}
for p in ('/tmp/my-project/work/TDKR-Game/extraction/re/session25/so_syms.json',
          '/tmp/my-project/work/re29/clsid_names.json'):
    if os.path.exists(p):
        print('symfile:', p)
try:
    syms = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session25/so_syms.json'))
except Exception as e:
    print('no so_syms:', e)
for key in ('0x755ba0', '755ba0'):
    if key in syms:
        print('sym 0x755ba0:', syms[key])

disasm(0x755ba0, 0x800, 'CAnimationBlock ctor @0x755ba0 (ARM)')
