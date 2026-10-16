#!/usr/bin/env python3
"""Disassemble a function from lib_libKRHP.so (ARM) with symbol annotation.
Usage: s27_disasm.py <vaddr> [<max_bytes>]"""
import bisect
import json
import re
import struct
import sys

SO = '/home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
SYMS = '/home/z/my-project/work/so_syms.json'

d = open(SO, 'rb').read()
e_phoff = struct.unpack_from('<I', d, 0x1c)[0]
e_phentsize = struct.unpack_from('<H', d, 0x2a)[0]
e_phnum = struct.unpack_from('<H', d, 0x2c)[0]
segs = []
for i in range(e_phnum):
    h = d[e_phoff + i * e_phentsize: e_phoff + (i + 1) * e_phentsize]
    p_type, p_off, p_va, _, p_sz = struct.unpack_from('<IIIII', h, 0)
    if p_type == 1:
        segs.append((p_va, p_sz, p_off))


def v2f(va):
    for a, s, o in segs:
        if a <= va < a + s:
            return o + (va - a)
    return None


syms = json.load(open(SYMS))['by_name']
items = sorted((int(v, 16), k) for k, v in syms.items())
addrs = [a for a, _ in items]

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM  # noqa: E402

md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
md.detail = False

va = int(sys.argv[1], 16)
nbytes = int(sys.argv[2], 0) if len(sys.argv) > 2 else 0x300
code = d[v2f(va):v2f(va) + nbytes]
for ins in md.disasm(code, va):
    tgt = ''
    m = re.search(r'#(0x[0-9a-f]+)', ins.op_str)
    if ins.mnemonic[0] == 'b' and m:
        t = int(m.group(1), 16)
        i = bisect.bisect_right(addrs, t) - 1
        if i >= 0 and items[i][0] == t:
            tgt = f'   ; {items[i][1]}'
    bl = re.search(r'bl\s+#(0x[0-9a-f]+)', f'{ins.mnemonic} {ins.op_str}')
    if ins.mnemonic == 'bl' and m:
        t = int(m.group(1), 16)
        i = bisect.bisect_right(addrs, t) - 1
        if i >= 0 and items[i][0] == t:
            tgt = f'   ; {items[i][1]}'
    print(f'{ins.address:08x}  {ins.mnemonic:8s} {ins.op_str}{tgt}')
