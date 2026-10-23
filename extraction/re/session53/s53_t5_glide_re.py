#!/usr/bin/env python3
"""s53 T5: static RE of CComponentGlide::Load (0x3c0938, THUMB) - glide parameters."""
import struct
from capstone import *

data = open('/tmp/my-project/work/re29/libKRHP.so', 'rb').read()
e_phoff = struct.unpack_from('<I', data, 28)[0]
e_phentsize = struct.unpack_from('<H', data, 42)[0]
e_phnum = struct.unpack_from('<H', data, 44)[0]

def v2o(v):
    for i in range(e_phnum):
        p = e_phoff + i * e_phentsize
        p_type, p_offset, p_vaddr, _, p_filesz = struct.unpack_from('<5I', data, p)
        if p_type == 1 and p_vaddr <= v < p_vaddr + p_filesz:
            return p_offset + (v - p_vaddr)
    return None

md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
md.detail = False

def dis(vaddr, n=140, stop_bl=True):
    off = v2o(vaddr)
    code = data[off:off + n * 4]
    out = []
    for ins in md.disasm(code, vaddr):
        out.append('%08x %-8s %s' % (ins.address, ins.mnemonic, ins.op_str))
        if stop_bl and ins.mnemonic in ('bl', 'blx') and len(out) > 8:
            break
        if ins.mnemonic in ('bx', 'pop') and 'pc' in ins.op_str:
            break
    return out

print('=== CComponentGlide::Load @0x3c0938 ===')
for l in dis(0x3c0938 + 1, 150):
    print(l)
