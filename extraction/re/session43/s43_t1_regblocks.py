#!/usr/bin/env python3
"""s43 T1f: fully resolve the registration blocks in 0x14a8bc — the pc-rel string
lists and the bool argument at each GlobalVarAddToLocalTable call."""
import struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

SO = '/tmp/my-project/work/apk_lib/lib/armeabi-v7a/libKRHP.so'
RAW = open(SO, 'rb').read()
PHOFF = struct.unpack_from('<I', RAW, 0x1c)[0]
PHNUM = struct.unpack_from('<H', RAW, 0x2c)[0]
SEGS = []
for i in range(PHNUM):
    o = PHOFF + i * 32
    t, off, va, pa, fs, ms = struct.unpack_from('<8I', RAW, o)[:6]
    if t == 1 and fs > 0:
        SEGS.append((va, off, fs, ms))


def va2off(va):
    for (v, o, fs, ms) in SEGS:
        if v <= va < v + fs:
            return o + (va - v)
    return None


def cstr_at(va, m=64):
    o = va2off(va)
    if o is None:
        return None
    d = RAW[o:o + m]
    e = d.find(b'\0')
    if e < 0:
        return None
    try:
        s = d[:e].decode('ascii')
        return s if all(32 <= ord(c) < 127 for c in s) else None
    except Exception:
        return None


LO, SZ = 0x14a8bc, 2592
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
code = RAW[va2off(LO):va2off(LO) + SZ]
insns = list(md.disasm(code, LO))

# track register values for ldr-literal + add-pc pairs
lits = {}   # reg -> (w, insn_va)
names = []  # resolved strings in order
for k, ins in enumerate(insns):
    if ins.mnemonic == 'ldr' and '[pc' in ins.op_str and ins.op_str.startswith('r'):
        try:
            reg = ins.op_str.split(',')[0]
            imm = int(ins.op_str.split('#')[1].rstrip(']'), 0)
            la = ((ins.address + 8) & ~3) + imm
            w = struct.unpack('<I', RAW[va2off(la):va2off(la) + 4])[0]
            lits[reg] = (w, ins.address)
        except Exception:
            pass
    elif ins.mnemonic == 'add' and 'pc' in ins.op_str:
        parts = [p.strip() for p in ins.op_str.split(',')]
        if len(parts) == 3 and parts[2] in lits:
            w, _ = lits[parts[2]]
            sva = (ins.address + 8 + w) & 0xFFFFFFFF
            s = cstr_at(sva)
            print(f'0x{ins.address:06x}: add {parts[0]}, pc, {parts[2]}  -> 0x{sva:06x} = {s!r}')
    elif ins.mnemonic.startswith('bl') and ins.op_str == '#0x14966c':
        print(f'0x{ins.address:06x}: *** GlobalVarAddToLocalTable call ***')
