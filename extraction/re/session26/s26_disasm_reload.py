#!/usr/bin/env python3
"""Disassemble CGameObjectManager::Reload @0x366104 (map offset hunt)."""
import struct, bisect, json

SO = '/home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
SYMS = '/home/z/my-project/work/so_syms.json'

d = open(SO, 'rb').read()
syms = json.load(open(SYMS))['by_name']
items = sorted((int(v, 16), k) for k, v in syms.items())
addrs = [a for a, _ in items]
names = {a: k for a, k in items}

START = 0x366104
i0 = bisect.bisect_right(addrs, START) - 1
END = addrs[i0 + 1]
print(f'; Reload {START:#x} .. {END:#x} ({END-START} B)')

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
code = d[START:START + (END - START)]
for ins in md.disasm(code, START):
    ann = ''
    if ins.mnemonic in ('bl', 'blx') or ins.mnemonic.startswith('b'):
        try:
            t = int(ins.op_str.lstrip('#'), 0)
            if t in names:
                ann = f'   ; {names[t]}'
        except ValueError:
            pass
    print(f'{ins.address:08x}  {ins.mnemonic:<8} {ins.op_str}{ann}')
