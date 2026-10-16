#!/usr/bin/env python3
"""S29 T1: disassemble CLevel::LoadNextObject @0x489ecc, find switch + default branch."""
import struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB, CS_MODE_ARM
SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()
START = 0x489ecc
SIZE = 0x3000
code = data[START:START + SIZE]
md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
md.detail = True
insns = list(md.disasm(code, START))
print(f'{len(insns)} insns')
import json
lines = []
for ins in insns:
    lines.append(f'{ins.address:#x}: {ins.mnemonic} {ins.op_str}')
open('/tmp/my-project/work/re29/lnobj_thumb.asm', 'w').write('\n'.join(lines))
# find cmp with big immediates / switch structure: BL, BX, MOVW
import re
for i, ins in enumerate(insns):
    if ins.mnemonic in ('cmp', 'movw') and any(str(x.imm if x.type == 2 else 0) for x in []):
        pass
# print a window around known id literals: search for immediates matching known tids
KNOWN = {0x2657, 0x2b, 0x798f, 0xc69a6a7, 0x2ad64f3d, 0x3377f0e, 0x17ac851f}
for i, ins in enumerate(insns):
    if ins.mnemonic in ('cmp', 'movw', 'ldr'):
        s = ins.op_str
        for k in KNOWN:
            if f'#{k}' in s or f'{k:#x}' in s:
                ctx = lines[max(0, i-3):i+4]
                print(f'--- {ins.address:#x} {ins.mnemonic} {s} (match {k:#x})')
                for c in ctx: print('   ', c)
                break
