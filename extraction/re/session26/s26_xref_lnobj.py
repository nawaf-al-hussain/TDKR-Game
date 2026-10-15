#!/usr/bin/env python3
"""Find xrefs to LoadNextObject and disassemble the caller loop."""
import struct, bisect, json, sys

SO = '/home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
SYMS = '/home/z/my-project/work/so_syms.json'

d = open(SO, 'rb').read()
e_phoff = struct.unpack_from('<I', d, 0x1c)[0]
e_phentsize = struct.unpack_from('<H', d, 0x2a)[0]
e_phnum = struct.unpack_from('<H', d, 0x2c)[0]
segs = []
for i in range(e_phnum):
    h = d[e_phoff + i * e_phentsize: e_phoff + (i + 1) * e_phentsize]
    p_type, p_offset, p_vaddr, _, p_filesz = struct.unpack_from('<IIIII', h, 0)
    if p_type == 1:
        segs.append((p_vaddr, p_filesz, p_offset))

def v2f(va):
    for a, s, o in segs:
        if a <= va < a + s:
            return o + (va - a)
    return None

syms = json.load(open(SYMS))['by_name']
items = sorted((int(v, 16), k) for k, v in syms.items())
addrs = [a for a, _ in items]
names = {a: k for a, k in items}

def fn_start(va):
    i = bisect.bisect_right(addrs, va) - 1
    return addrs[i], names[addrs[i]]

TARGET = 0x489ecc  # LoadNextObject
# scan all executable code for 'bl 0x489ecc'
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
# scan segment by segment (code is in the first LOAD)
callers = []
for a, s, o in segs:
    code = d[o: o + s]
    for ins in md.disasm(code, a):
        if ins.mnemonic == 'bl' and ins.op_str.lstrip('#') == hex(TARGET):
            fs, fn = fn_start(ins.address)
            callers.append((ins.address, fs, fn))
print('xrefs (bl) to LoadNextObject:')
for ca, fs, fn in callers:
    print(f'  call @{ca:#x} inside {fn} ({fs:#x})')
