#!/usr/bin/env python3
"""Disassemble CMemoryStream ctor @0x339238 (field layout)."""
import struct, json

SO = '/home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
d = open(SO, 'rb').read()
# LOAD off=0 vaddr=0: vaddr == file offset for the first 0xbbe1ec bytes

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
START, N = 0x339238, 0x80
code = d[START:START + N]
for ins in md.disasm(code, START):
    print(f'{ins.address:08x}  {ins.mnemonic:<8} {ins.op_str}')
