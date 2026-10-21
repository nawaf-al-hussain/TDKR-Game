#!/usr/bin/env python3
"""s43 T2a: disasm CDoubleBufferedLODStreaming::process @0x469d94 — find the
vertex-size computation (constants 20/24/28/32, format table refs, calls)."""
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


def cstr_at(va, m=48):
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


SYM = {}
for line in open('/tmp/my-project/work/TDKR-Game/extraction/libKRHP_symbols.txt'):
    p = line.split()
    if len(p) >= 4 and p[3] == 'FUNC':
        SYM[int(p[0], 16)] = int(p[1])

LO, SZ = 0x469d94, 2164
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
code = RAW[va2off(LO):va2off(LO) + SZ]
INTEREST_CONST = {20, 24, 28, 32, 12, 8, 4, 36, 68}
for ins in md.disasm(code, LO):
    note = ''
    # movw/movt immediates
    if ins.mnemonic in ('movw', 'mov', 'cmp', 'sub', 'mul') and '#' in ins.op_str:
        try:
            imm = int(ins.op_str.split('#')[-1].rstrip(']'), 0)
            if imm in INTEREST_CONST:
                note += f'   ; <<< {imm}'
        except ValueError:
            pass
    if ins.mnemonic.startswith('bl') and ins.op_str.startswith('#'):
        t = int(ins.op_str.lstrip('#'), 0)
        note += f'   ; -> 0x{t:x}' + (f' (sz{SYM[t]})' if t in SYM else '')
    if ins.mnemonic == 'ldr' and '[pc' in ins.op_str:
        try:
            imm = int(ins.op_str.split('#')[1].rstrip(']'), 0)
            la = ((ins.address + 8) & ~3) + imm
            w = struct.unpack('<I', RAW[va2off(la):va2off(la) + 4])[0]
            note += f'   ; lit=0x{w:08x}'
            if 0x1000 < w < 0xc40000:
                s = cstr_at(w)
                if s:
                    note += f' {s!r}'
        except Exception:
            pass
    if note or ins.mnemonic in ('mul', 'mla'):
        print(f'0x{ins.address:06x}: {ins.mnemonic:8s} {ins.op_str}{note}')
