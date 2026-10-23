#!/usr/bin/env python3
"""s54 T1 step 9: robust linear sweep of GenerateComponentTemplate with restart-on-invalid.
Dumps to s54_gct_full_disasm.txt. Then locates the case computing vptr 0xbd8998
and the class id guarding it."""
import struct
from capstone import *

SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()
e_phoff = struct.unpack_from('<I', data, 28)[0]
e_phentsize = struct.unpack_from('<H', data, 42)[0]
e_phnum = struct.unpack_from('<H', data, 44)[0]
segs = []
for i in range(e_phnum):
    p = e_phoff + i * e_phentsize
    p_type, p_offset, p_vaddr, _, p_filesz = struct.unpack_from('<5I', data, p)
    if p_type == 1:
        segs.append((p_vaddr, p_offset, p_filesz))

def v2o(v):
    for va, off, sz in segs:
        if va <= v < va + sz:
            return off + (v - va)
    return None

GCT, SIZE = 0x368ac0, 0x36b7c0 - 0x368ac0
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

out = []
pos = GCT
end = GCT + SIZE
while pos < end:
    chunk = md.disasm(data[v2o(pos):v2o(end)], pos)
    last = pos
    n = 0
    for ins in chunk:
        note = ''
        if ins.mnemonic == 'add' and ' pc' in ins.op_str:
            note = '   ; <== PC-REL ADD'
        out.append('%08x %-8s %s%s' % (ins.address, ins.mnemonic, ins.op_str, note))
        last = ins.address + ins.size
        n += 1
    if n == 0 or last <= pos:
        # skip 4 bytes and continue
        pos = last + 4 if last > pos else pos + 4
        out.append('%08x .word  (skip)' % pos)
    else:
        pos = last

open('/home/z/my-project/scripts/s54_gct_full_disasm.txt', 'w').write('\n'.join(out))
print('wrote %d lines, swept to %#x' % (len(out), pos))

# find pc-rel add sites and their computed targets
sites = []
for ln in out:
    if 'PC-REL ADD' in ln:
        sites.append(int(ln.split()[0], 16))
print('pc-rel add sites:', [hex(s) for s in sites])
