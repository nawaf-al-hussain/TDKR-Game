#!/usr/bin/env python3
"""s44 T1: disassemble the ldebug error block + find luaV_arith in libKRHP.so
(symbolized build: luaG_typeerror @0xa53fa0, luaG_ordererror @0xa54114,
luaV_execute @0xa69394, luaV_tonumber nearby, luaS_newlstr @0xa61510)."""
import struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

SO = '/tmp/my-project/work/apk_lib/lib/armeabi-v7a/libKRHP.so'
data = open(SO, 'rb').read()

# symbol map from symtab (12-byte Elf32_Sym)
symoff, symsize, strsym_off = 0xc1e064, 0x158e10, 0xd76e74
SYMS = []
for i in range(symsize // 12):
    o = symoff + i * 12
    nameoff, value, size, info, other, shndx = struct.unpack_from('<IIBBHI', data, o)
    if not value:
        continue
    e = data.find(b'\0', strsym_off + nameoff, strsym_off + nameoff + 200)
    nm = data[strsym_off + nameoff:e].decode('ascii', 'replace')
    SYMS.append((value, size, nm))
SYMS.sort()
NAMED = {}
for v, s, nm in SYMS:
    if nm and not nm.startswith('$'):
        NAMED.setdefault(nm, v)

def v2o(v):
    if v < 0xbbe1ec:
        return v
    return v - 0x1000

md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

def dis(start, size, label, bl_depth=1):
    print(f'===== {label} @ {hex(start)} (size {size}) =====')
    for ins in md.disasm(data[v2o(start):v2o(start) + size], start):
        txt = f'{ins.address:x}: {ins.mnemonic:8s} {ins.op_str}'
        # annotate bl targets
        if ins.mnemonic in ('bl', 'blx'):
            try:
                t = int(ins.op_str.replace('#', ''), 0) if ins.op_str.startswith('#') else int(ins.op_str, 0)
            except ValueError:
                t = None
            if t is not None:
                nm = [n for v, s, n in SYMS if v == t and not n.startswith('$')]
                txt += f'   ; -> {nm[0] if nm else hex(t)}'
        print(txt)

# 1) ldebug block: typeerror .. ordererror (0xa53fa0..0xa54200)
dis(0xa53fa0, 0xa54200 - 0xa53fa0, 'ldebug: typeerror/aritherror/concaterror/indexerror/runerror/ordererror')

# 2) find luaV_arith: scan backwards from luaV_execute for a function that BLs
#    luaV_tonumber and luaG_aritherror
vt = NAMED.get('luaV_tonumber')
ve = NAMED.get('luaV_execute')
print(f'\nluaV_tonumber={hex(vt)} luaV_execute={hex(ve)}')
# locate all BL sites to luaG_aritherror-candidate: first find the aritherror fn:
# it is the unnamed function after luaG_typeerror that references 'perform arithmetic on'
# (0xbb217c) via pc-rel add; scan the ldebug block above printed code for add pc patterns.
