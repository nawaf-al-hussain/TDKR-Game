#!/usr/bin/env python3
"""S29 T1: resolve small component ids: movw(+no movt) + cmp; also 32-bit pool ldr+cmp."""
import struct, json
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
SO = '/tmp/my-project/work/re29/libKRHP.so'
d = open(SO, 'rb').read()
SYMS = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session25/so_syms.json'))
by_addr = SYMS['by_addr']
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
TEXT = (0xa5d80, 0xac2490)

TARGETS = {0x295: 'l_menu', 0x433: 'shop', 0x2056: 'Stadion', 0x4E52B: 'Police_Station',
           0x4A2B: 'StockExchange', 0x2A953: 'Underground', 0xBC0: 'Military2',
           0x10FF796: 'Dummy', 0x7F8ED4E: 'autofit40B', 0x288AE7DA: 'WorldBox6'}

def sym(a):
    s = by_addr.get(hex(a))
    return s[1] if s and len(s) > 1 else None

def vread(v):
    if v >= 0xbbf930: return struct.unpack_from('<I', d, 0xbbe930 + (v - 0xbbf930))[0]
    return struct.unpack_from('<I', d, v)[0]

# full ARM-mode linear disasm of .text is too slow; instead scan windows around every
# `bl 0x368ac0`(GCT)/`bl 0x223e3c`(factory) and around known case bodies? Simpler:
# brute-force decode: for each candidate id, search .text for cmp-with-reg patterns by
# disasming 0x100-byte windows centered on every `cmp r0, rX`-looking raw word is heavy.
# Faster: single linear disasm of the two switch regions with register tracking.
REGIONS = [('factory', 0x223e3c, 0x2259c4), ('generic_GCT', 0x368ac0, 0x36b4c0),
           ('lnobj_tree', 0x489ecc, 0x48d400), ('createobj', 0x36774c, 0x368ac0)]
found = {}
for rname, start, end in REGIONS:
    ins = list(md.disasm(d[start:end], start))
    movw = {}
    for idx, i in enumerate(ins):
        if i.mnemonic == 'movw' and '#0x' in i.op_str:
            reg, imm = i.op_str.split(', #')
            if ',' not in reg: movw[reg] = int(imm, 16)
        elif i.mnemonic == 'movt' and '#0x' in i.op_str:
            reg, imm = i.op_str.split(', #')
            if reg in movw: movw[reg] = (movw[reg] & 0xFFFF) | (int(imm, 16) << 16)
        elif i.mnemonic == 'cmp' and ', ' in i.op_str:
            parts = i.op_str.split(', ')
            if len(parts) >= 2:
                b = parts[1]
                if b in movw and movw[b] in TARGETS:
                    found.setdefault(movw[b], []).append((rname, i.address, 'regcmp'))
                elif len(parts) >= 2 and b.startswith('#'):
                    try:
                        v = int(b[1:], 16)
                        if v in TARGETS: found.setdefault(v, []).append((rname, i.address, 'immcmp'))
                    except ValueError: pass
for tid, tag in TARGETS.items():
    hits = found.get(tid, [])
    print(f'{tid:#010x} {tag:16s}: {[(r, hex(a), k) for r, a, k in hits[:6]] if hits else "NOT in switch regions"}')
