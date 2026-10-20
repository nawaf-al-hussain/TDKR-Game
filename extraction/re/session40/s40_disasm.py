#!/usr/bin/env python3
"""Disassemble CImageLoaderPVR::loadImage (0x80d6f0) and loadTextureHeader
(0x80dc3c) from libKRHP.so to map the header format code -> engine pixel type.
"""
import struct, sys
from capstone import *

SO = '/tmp/my-project/work/re29/libKRHP.so'
d = open(SO, 'rb').read()
phoff = struct.unpack_from('<I', d, 0x1c)[0]
phnum = struct.unpack_from('<H', d, 0x2c)[0]
segs = []
for i in range(phnum):
    o = phoff + i * 32
    p_type, p_offset, p_vaddr, _, p_filesz, _ = struct.unpack_from('<6I', d, o)
    if p_type == 1: segs.append((p_vaddr, p_offset, p_filesz))

def v2o(va):
    for vaddr, off, sz in segs:
        if vaddr <= va < vaddr + sz: return off + (va - vaddr)
    raise ValueError(hex(va))

md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
md.detail = True

def dis(lo, hi):
    o = v2o(lo)
    code = d[o:o + (hi - lo)]
    out = []
    for i in md.disasm(code, lo):
        line = f'{i.address:08x}: {i.mnemonic:8s} {i.op_str}'
        # annotate literal pool loads (ldr rX, [pc, #imm])
        if i.mnemonic.startswith('ldr') and 'pc' in i.op_str:
            # compute target
            ops = i.op_str
            try:
                import re
                m = re.search(r'\[pc, #(-?\d+)\]', ops)
                if m:
                    tgt = i.address + 8 + int(m.group(1))
                    tgt &= ~3
                    wo = v2o(tgt)
                    val = struct.unpack_from('<I', d, wo)[0]
                    line += f'   ; ={tgt:08x} -> 0x{val:08x} ({val})'
            except Exception:
                pass
        out.append(line)
    return '\n'.join(out)

if __name__ == '__main__':
    lo, hi = int(sys.argv[1], 16), int(sys.argv[2], 16)
    print(dis(lo, hi))
