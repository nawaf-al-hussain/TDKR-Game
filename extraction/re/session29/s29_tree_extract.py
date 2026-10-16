#!/usr/bin/env python3
"""S29 T1: complete dedicated-dispatcher tree extraction (all cmp forms) + case bodies."""
import struct, json
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
SO = '/tmp/my-project/work/re29/libKRHP.so'
d = open(SO, 'rb').read()
SYMS = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session25/so_syms.json'))
by_addr = SYMS['by_addr']
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

def sym(a):
    s = by_addr.get(hex(a)); return s[1] if s and len(s) > 1 else None
def vread(v):
    if v >= 0xbbf930: return struct.unpack_from('<I', d, 0xbbe930 + (v - 0xbbf930))[0]
    return struct.unpack_from('<I', d, v)[0]

START, END = 0x489ecc, 0x48f000
ins = list(md.disasm(d[START:END], START))
print(f'{len(ins)} insns in dispatcher')
movw = {}
cases = {}   # tid -> (cmp_addr, branch_tgt)
for idx, i in enumerate(ins):
    m = i.mnemonic
    if m == 'movw' and '#0x' in i.op_str:
        reg, imm = i.op_str.split(', #')
        if ',' not in reg: movw[reg] = int(imm, 16)
    elif m == 'movt' and '#0x' in i.op_str:
        reg, imm = i.op_str.split(', #')
        if reg in movw: movw[reg] = (movw[reg] & 0xFFFF) | (int(imm, 16) << 16)
    elif m == 'ldr' and '[pc, #' in i.op_str and i.op_str.endswith(']'):
        reg = i.op_str.split(',')[0]
        off = int(i.op_str.split('#')[1].rstrip(']'), 16)
        pa = ((i.address + 8) & ~3) + off
        movw[reg] = struct.unpack_from('<I', d, pa)[0] | 0x100000000  # mark as pool
    elif m == 'cmp' and ', ' in i.op_str:
        parts = i.op_str.split(', ')
        if len(parts) >= 2:
            b = parts[1]
            val = None
            if b in movw: val = movw[b] & 0xFFFFFFFF
            elif b.startswith('#'):
                try: val = int(b[1:], 16)
                except ValueError: pass
            if val is not None and val > 0:
                # find branch
                for j in range(idx + 1, min(idx + 4, len(ins))):
                    if ins[j].mnemonic in ('beq',) and ins[j].op_str.startswith('#'):
                        cases[val] = (i.address, int(ins[j].op_str[1:], 16), parts[0])
                        break
                    if ins[j].mnemonic in ('cmp', 'b'): break
print('distinct compared constants:', len(cases))
FAM = [t for t in sorted(cases) if 0x16F00 <= t <= 0x16FFF]
print('0x16Fxx family in tree:', [hex(t) for t in FAM])
for t in FAM[:8]:
    ca, tgt, reg = cases[t]
    print(f'  {t:#x}: cmp@{ca:#x} -> case@{tgt:#x}')
json.dump({hex(t): {'cmp': hex(a), 'case': hex(b)} for t, (a, b, r) in cases.items()},
          open('/tmp/my-project/work/re29/dispatcher_tree.json', 'w'), indent=0)
