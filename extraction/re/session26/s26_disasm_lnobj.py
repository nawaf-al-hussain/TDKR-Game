#!/usr/bin/env python3
"""Disassemble CLevel::LoadNextObject @0x489ecc completely (session 26 T1)."""
import struct, sys, bisect, json

SO = '/home/z/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
SYMS = '/home/z/my-project/work/so_syms.json'

d = open(SO, 'rb').read()
e_phoff = struct.unpack_from('<I', d, 0x1c)[0]
e_phentsize = struct.unpack_from('<H', d, 0x2a)[0]
e_phnum = struct.unpack_from('<H', d, 0x2c)[0]
segs = []
for i in range(e_phnum):
    h = d[e_phoff + i * e_phentsize: e_phoff + (i + 1) * e_phentsize]
    p_type, p_offset, p_vaddr, _, p_filesz = struct.unpack_from('<IIIII', h, 0)
    if p_type == 1:
        segs.append((p_vaddr, p_filesz, p_offset))

def v2f(va):
    for a, s, o in segs:
        if a <= va < a + s:
            return o + (va - a)
    return None

syms = json.load(open(SYMS))['by_name']
items = sorted((int(v, 16), k) for k, v in syms.items())
addrs = [a for a, _ in items]

def fn_of(va):
    i = bisect.bisect_right(addrs, va) - 1
    return items[i][1] if i >= 0 else ('sub_%x' % va)

def sym_at(va):
    i = bisect.bisect_left(addrs, va)
    if i < len(addrs) and addrs[i] == va:
        return items[i][1]
    return None

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
START = 0x489ecc
i0 = bisect.bisect_right(addrs, START) - 1
END = addrs[i0 + 1] if i0 + 1 < len(addrs) else START + 0x4000
print(f'; CLevel::LoadNextObject {START:#x} .. {END:#x}  ({END-START} B)')

md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
md.detail = False
code = d[v2f(START): v2f(START) + (END - START)]
out = []
for ins in md.disasm(code, START):
    line = f'{ins.address:08x}  {ins.mnemonic:<8} {ins.op_str}'
    # symbol annotate branch targets and literal loads
    m = sym_at(ins.op_str.startswith('#') and int(ins.op_str[1:], 0) or -1)
    # literal pool: ldr rX, [pc, #imm]
    out.append(line)
print('\n'.join(out))

# dump literal pool words referenced (pc-relative loads) — annotate manually:
print('\n; literal-pool candidates in range:')
pool_start = END
pool = d[v2f(pool_start): v2f(pool_start) + 0x400]
for j in range(0, len(pool) - 3, 4):
    w = struct.unpack_from('<I', pool, j)[0]
    print(f'  {pool_start + j:08x}: {w:08x}')
