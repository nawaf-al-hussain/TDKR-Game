#!/usr/bin/env python3
"""s46 T1: disassemble CColladaDatabase::constructMaterial overloads in
libKRHP.so with symbol + literal-pool annotation. ARM mode."""
import struct, sys, re

SO = '/tmp/my-project/work/apk_lib/lib/armeabi-v7a/libKRHP.so'
SYM = '/tmp/my-project/work/TDKR-Game/extraction/libKRHP_symbols.txt'
DEMANGL = '/tmp/my-project/work/TDKR-Game/extraction/libKRHP_symbols_demangled.txt'

d = open(SO, 'rb').read()
e_phoff = struct.unpack_from('<I', d, 0x1c)[0]
e_phentsize = struct.unpack_from('<H', d, 0x2a)[0]
e_phnum = struct.unpack_from('<H', d, 0x2c)[0]
segs = []
for i in range(e_phnum):
    h = d[e_phoff+i*e_phentsize: e_phoff+(i+1)*e_phentsize]
    p_type, p_offset, p_vaddr, _, p_filesz = struct.unpack_from('<IIIII', h, 0)
    if p_type == 1:
        segs.append((p_vaddr, p_filesz, p_offset))

def v2f(va):
    for a, s, o in segs:
        if a <= va < a + s:
            return o + (va - a)
    return None

syms2 = {}
for line in open(SYM):
    p = line.split()
    if len(p) >= 4 and p[2] == 'FUNC':
        va = int(p[0], 16)
        syms2[va] = (p[3], int(p[1]))
dem = {}
for line in open(DEMANGL):
    p = line.rstrip('\n').split(None, 1)
    if len(p) == 2 and re.match(r'^[0-9a-f]{8}', p[0]):
        dem[int(p[0], 16)] = p[1]

def sym_at(va):
    if va in syms2:
        return dem.get(va, syms2[va][0])
    return None

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_LITTLE_ENDIAN
md = Cs(CS_ARCH_ARM, CS_MODE_ARM | CS_MODE_LITTLE_ENDIAN)

def dis(va, size, label):
    print(f'\n===== {label} @ {va:#x} ({size} B) =====')
    fo = v2f(va)
    code = d[fo:fo+size]
    for ins in md.disasm(code, va):
        line = f'{ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}'
        m = re.search(r'\[pc, #(\d+)\]', ins.op_str)
        if ins.mnemonic.startswith('ldr') and m:
            tgt = (ins.address + 8 + int(m.group(1))) & ~3
            tf = v2f(tgt)
            w = struct.unpack_from('<I', d, tf)[0] if tf is not None else None
            ann = f' ; @{tgt:#x}'
            if w is not None:
                ann += f' = {w:#x}'
                if (w & 1) == 1 and (w & ~1) in syms2:
                    ann += ' -> ' + dem.get(w & ~1, syms2[w & ~1][0])
                elif w in syms2:
                    ann += ' -> ' + dem.get(w, syms2[w][0])
                elif tf is not None:
                    tf3 = v2f(w & ~1)
                    if tf3 is not None:
                        mm = re.match(rb'[ -~]{4,}', d[tf3:tf3+48])
                        if mm:
                            ann += f' "{mm.group().decode()}"'
            line += ann
        if ins.mnemonic in ('bl', 'b', 'blx') and ins.op_str.startswith('#'):
            t = int(ins.op_str.lstrip('#'), 16)
            n = sym_at(t)
            if n:
                line += f'  ; {n}'
        print(line)

if __name__ == '__main__':
    dis(0x7bd0ec, 0x3c, 'constructMaterial(driver, int, scene)')
    dis(0x7bd128, 0x94, 'constructMaterial(driver, const char*, scene)')
    dis(0x7bd1bc, 0x26c, 'constructMaterial(driver, SMaterial*, scene)')
