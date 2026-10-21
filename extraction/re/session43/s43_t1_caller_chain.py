#!/usr/bin/env python3
"""s43 T1c: identify the function containing 0x3f379c (production caller of the
chunk-runner 0x1495b4), disassemble a window around the call site, resolve the
getfield literal in 0x1495b4, and identify 0x14b2dc / 0x1493b0 / 0x14bf7c."""
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


SYM = {}
for line in open('/tmp/my-project/work/TDKR-Game/extraction/libKRHP_symbols.txt'):
    p = line.split()
    if len(p) >= 4 and p[3] == 'FUNC':
        SYM[int(p[0], 16)] = int(p[1])


def find_fn(va):
    best = None
    for a, s in SYM.items():
        if a <= va < a + s:
            best = (a, s)
    return best


CALLER = 0x3f379c
fa, fsz = find_fn(CALLER) or (None, None)
if fa is None:
    # scan backwards for an ARM function prologue: push {..., lr} = e92d xxxx
    o = va2off(CALLER)
    for back in range(0, 0x800, 4):
        w = struct.unpack_from('<I', RAW, o - back)[0]
        if (w & 0xFFFF0000) == 0xE92D0000:
            fa = CALLER - back
            break
    # scan forward for next prologue to bound the function
    for fwd in range(0x40, 0x3000, 4):
        w = struct.unpack_from('<I', RAW, va2off(fa) + fwd)[0]
        if (w & 0xFFFF0000) == 0xE92D0000:
            fsz = fwd
            break
    else:
        fsz = 0x800
    print(f'=== caller fn of 0x1495b4 (no export sym): estimated 0x{fa:06x}..0x{fa + fsz:06x} ===')
else:
    print(f'=== caller function of 0x1495b4: 0x{fa:06x} size {fsz} ===')

# demangled name?
import subprocess
name = subprocess.run(['grep', '-F', hex(fa) if fa else 'none', '/tmp/my-project/work/TDKR-Game/extraction/libKRHP_symbols.txt'],
                      capture_output=True, text=True).stdout.strip()
print('symbol line:', name[:200])

# disasm window around the call site: whole function if small else +/-0x120
lo = fa
hi = fa + (fsz or 0x400)
code = RAW[va2off(lo):va2off(hi)]
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
prev_lit = {}
print(f'\n--- disasm 0x{lo:06x}..0x{hi:06x} (window around 0x{CALLER:06x}) ---')
for ins in md.disasm(code, lo):
    mark = '>>>' if abs(ins.address - CALLER) <= 0x10 else '   '
    tgt = ''
    if ins.mnemonic.startswith('bl') and ins.op_str.startswith('#'):
        try:
            t = int(ins.op_str.lstrip('#'), 0)
            fsz2 = SYM.get(t)
            tgt = f'   ; -> 0x{t:x}' + (f' (fn size {fsz2})' if fsz2 else '')
        except ValueError:
            pass
    if ins.mnemonic in ('ldr',) and '[pc' in ins.op_str:
        try:
            imm = int(ins.op_str.split('#')[1].rstrip(']'), 0)
            la = ((ins.address + 8) & ~3) + imm
            w = struct.unpack('<I', RAW[va2off(la):va2off(la) + 4])[0]
            tgt += f'   ; lit@0x{la:06x}=0x{w:08x}'
            if 0x1000 < w < 0xc40000:
                s = cstr_at(w)
                if s:
                    tgt += f' str={s!r}'
                else:
                    # add pc-relative later — record
                    prev_lit[ins.address] = (la, w)
        except Exception:
            pass
    if ins.mnemonic == 'add' and 'pc' in ins.op_str:
        # add rX, pc, rY -> resolve pending literal
        tgt += '   ; pc-rel add'
    print(f'{mark} 0x{ins.address:06x}: {ins.mnemonic:8s} {ins.op_str}{tgt}')

# getfield literal in 0x1495b4
print('\n=== 0x1495b4 getfield literal ===')
la = ((0x1495d8 + 8) & ~3) + 0x88
w = struct.unpack('<I', RAW[va2off(la):va2off(la) + 4])[0]
sva = (0x1495ec + 8 + w) & 0xFFFFFFFF
print(f'  lit@0x{la:06x}=0x{w:08x} -> str@0x{sva:06x} = {cstr_at(sva)!r}')

# identify helper functions
for h in (0x14b2dc, 0x1493b0, 0x14bf7c, 0x3395d8, 0x339914, 0x1493b0):
    fa2, fsz2 = find_fn(h)
    print(f'  helper 0x{h:06x}: fn@0x{fa2:06x} size {fsz2}')
