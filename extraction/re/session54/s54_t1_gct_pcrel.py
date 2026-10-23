#!/usr/bin/env python3
"""s54 T1 step 7: find the GenerateComponentTemplate case for CComponentGlide.
Case bodies compute the vtable ptr PC-relatively:  ldr r3, [pc, #imm]; add r3, pc, r3.
So scan for literal L where (add_site + 8 + L) == 0xbd8998 (CComponentGlide stored vptr).
Also: map EVERY case's vtable + Load address to its class id, and identify the class
whose Load == 0x3c0938 (CComponentGlide::Load).
"""
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

GCT, SIZE = 0x368ac0, 11600
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
insns = list(md.disasm(data[v2o(GCT):v2o(GCT) + SIZE], GCT))
print('insns:', len(insns), 'last:', hex(insns[-1].address))

# for each `add rX, pc, rY` preceded by `ldr rY, [pc, #imm]`, compute the target
targets = {}   # computed_addr -> [sites]
for i, ins in enumerate(insns):
    if ins.mnemonic == 'add' and 'pc' in ins.op_str:
        parts = [p.strip() for p in ins.op_str.split(',')]
        if len(parts) >= 3 and parts[1] == 'pc':
            rd, _, rm = parts[0], parts[1], parts[2]
            # find previous ldr rm, [pc, #imm]
            for j in range(i - 1, max(0, i - 12), -1):
                pj = insns[j]
                if pj.mnemonic == 'ldr' and pj.op_str.startswith(rm + ', [pc'):
                    try:
                        imm = int(pj.op_str.split('#')[1].rstrip(']'), 0)
                    except (IndexError, ValueError):
                        break
                    base = (pj.address + 8) & ~3
                    L = struct.unpack_from('<I', data, v2o(base + imm))[0]
                    val = ins.address + 8 + L
                    targets.setdefault(val & 0xffffffff, []).append(
                        (pj.address, ins.address))
                    break

print('\ncomputed pc-rel targets in/near vtable region (0xbbf000-0xbe0000):')
hits = {a: s for a, s in targets.items() if 0xbbf000 <= a < 0xbe0000}
for a in sorted(hits):
    print('  %#x <- sites %s' % (a, [(hex(x), hex(y)) for x, y in hits[a][:2]]))

# the glide vptr = 0xbd8998
for want in (0xbd8998, 0xbd8990):
    if want in targets:
        print('\nGLIDE VTABLE %#x FOUND, sites:' % want, [(hex(x), hex(y)) for x, y in targets[want]])
    else:
        print('\n%#x NOT in computed targets' % want)

# also compute all case targets to build the full class-id -> vtable map:
# walk movw/movt id constants; each is followed (eventually) by a branch to a case;
# simpler: list every id and the nearest following add-site target
print('\nfull id list with nearest pc-rel vtable target after each id:')
ids = []
movw = {}
for i, ins in enumerate(insns):
    if ins.mnemonic == 'movw':
        rd, imm = ins.op_str.split(', ')
        movw[rd] = int(imm.replace('#', ''), 0)
    elif ins.mnemonic == 'movt' and rd in movw:
        rd2, imm2 = ins.op_str.split(', ')
        if rd2 in movw:
            val = (int(imm2.replace('#', ''), 0) << 16) | movw[rd2]
            ids.append((ins.address, val))
for addr, val in ids:
    # find next pc-rel target site after this address
    nxt = None
    for a in sorted(targets):
        for (ldr_s, add_s) in targets[a]:
            if add_s > addr and add_s < addr + 0x60:
                nxt = a
                break
        if nxt:
            break
    print('  id %#010x @%#x -> vt %#x' % (val, addr, nxt if nxt else 0))
