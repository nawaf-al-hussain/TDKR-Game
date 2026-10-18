#!/usr/bin/env python3
"""S33 T1: examine the two 0x14FFFF hit sites."""
import capstone, struct

SO = '/tmp/my-project/work/re29/libKRHP.so'
d = open(SO, 'rb').read()

def disasm_window(va, before=0x60, after=0x80, mode=capstone.CS_MODE_THUMB):
    fo = va - before
    md = capstone.Cs(capstone.CS_ARCH_ARM, mode)
    print(f'===== window around 0x{va:x} ({mode}) =====')
    for ins in md.disasm(d[fo:fo + before + after], fo):
        mark = ' <<<<' if ins.address <= va < ins.address + ins.size else ''
        print(f'  0x{ins.address:08x}: {ins.mnemonic:8s} {ins.op_str}{mark}')

for h in (0x22d576, 0x369ca2):
    print(f'\n########## hit 0x{h:x} ##########')
    print('bytes:', d[h-16:h+16].hex(' '))
    disasm_window(h)
