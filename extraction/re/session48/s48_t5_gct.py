#!/usr/bin/env python3
"""s48 T5 (time-boxed): does GenerateComponentTemplate @0x368ac0 inject
component DATA (sizes) for flag-0 template components, or only instantiate?
Also: list the trigger templates' BuiltinBox entries (class id, flag) from
gol.bin and confirm no default-size source exists. Stop rule applies."""
import struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB

SO = '/tmp/my-project/work/re29/libKRHP.so'
import os
if not os.path.exists(SO):
    import glob
    cands = glob.glob('/tmp/my-project/raw/**/libKRHP.so', recursive=True)
    SO = cands[0]
data = open(SO, 'rb').read()
# ELF: find PT_LOAD covering 0x368ac0 (file offset = vaddr for typical GAM-E mappings)
e_phoff = struct.unpack_from('<I', data, 0x1C)[0]
e_phentsize = struct.unpack_from('<H', data, 0x2A)[0]
e_phnum = struct.unpack_from('<H', data, 0x2C)[0]
segs = []
for i in range(e_phnum):
    p = e_phoff + i * e_phentsize
    p_type, p_offset, p_vaddr, _pa, p_filesz = struct.unpack_from('<IIIII', data, p)
    if p_type == 1:
        segs.append((p_vaddr, p_filesz, p_offset))

def v2o(va):
    for vaddr, filesz, off in segs:
        if vaddr <= va < vaddr + filesz:
            return off + (va - vaddr)
    return None

VA = 0x368ac0
o = v2o(VA)
print('v2o(%#x) = %#x' % (VA, o))
md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
md.detail = False
code = data[o:o + 0x400]
bls = []
for ins in md.disasm(code, VA):
    line = '%08x  %-8s %s' % (ins.address, ins.mnemonic, ins.op_str)
    print(line)
    if ins.mnemonic in ('bl', 'blx') or ins.mnemonic == 'pop' and 'pc' in ins.op_str:
        bls.append(line)
    if ins.mnemonic == 'pop' and 'pc' in ins.op_str:
        break
