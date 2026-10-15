#!/usr/bin/env python3
"""Disassemble CWayPointObject::Load @0x2a7e58 and neighbors (session 26 T1)."""
import struct, bisect, json

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

START = 0x2a7e58
i0 = bisect.bisect_right(addrs, START) - 1
END = addrs[i0 + 1]
print(f'; CWayPointObject::Load {START:#x} .. {END:#x} ({END-START} B) next={names.get(END)}')

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
code = d[v2f(START): v2f(START) + (END - START)]
for ins in md.disasm(code, START):
    ann = ''
    if ins.mnemonic.startswith('b'):
        try:
            t = int(ins.op_str.lstrip('#'), 0)
            if t in names:
                ann = f'   ; {names[t]}'
        except ValueError:
            pass
    if ins.mnemonic in ('bl', 'blx'):
        try:
            t = int(ins.op_str.lstrip('#'), 0)
            if t in names:
                ann = f'   ; {names[t]}'
        except ValueError:
            pass
    print(f'{ins.address:08x}  {ins.mnemonic:<8} {ins.op_str}{ann}')
