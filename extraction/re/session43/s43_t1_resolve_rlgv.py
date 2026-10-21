#!/usr/bin/env python3
"""s43 T1b: resolve ResetLuaGlobalVars literal pool (string A + 10 whitelist names),
identify + disassemble the caller function @0x1495b4, find ITS callers, and inspect
the vtable word @0xa67e2c."""
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


FN = 0x14b478
END = FN + 664

# --- literal pool: words after the code (capstone stopped at data) ---
pool_off = va2off(0x14b6e4)
pool = [struct.unpack_from('<I', RAW, pool_off + i * 4)[0] for i in range(16)]
print('=== literal pool @0x14b6e4 (as words) ===')
for i, w in enumerate(pool):
    va = 0x14b6e4 + i * 4
    print(f'  0x{va:06x}: 0x{w:08x}' + (f'  -> str {cstr_at(w)!r}' if 0x1000 < w < 0xc40000 and cstr_at(w) else ''))

# --- resolve the pc-relative loads manually ---
print('\n=== pc-relative string resolutions ===')
# (insn va, literal va, note)
loads = [
    (0x14b494, 0x14b6e4 + (0x248 - 0x8) // 4 * 4, None),  # placeholder, fix below
]
# compute literal address: for ARM, literal va = (insn_va + 8) + imm rounded
# ldr rX, [pc, #imm] -> literal at align(insn+8,4) + imm
def litaddr(insn_va, imm):
    return ((insn_va + 8) & ~3) + imm

resolutions = [
    ('getfield string A', 0x14b494, 0x248),
    ('whitelist sp+0', 0x14b4b4, 0x22c),
    ('whitelist sp+4', 0x14b4c0, 0x224),
    ('whitelist sp+8', 0x14b4cc, 0x21c),
    ('wl4', 0x14b588, 0x164),
    ('wl5', 0x14b5a0, 0x150),
    ('wl6', 0x14b5b8, 0x13c),
    ('wl7', 0x14b5d0, 0x128),
    ('wl8', 0x14b5e8, 0x114),
    ('wl9', 0x14b600, 0x100),
    ('wl10', 0x14b618, 0xec),
]
for label, insn_va, imm in resolutions:
    la = litaddr(insn_va, imm)
    w = struct.unpack('<I', RAW[va2off(la):va2off(la) + 4])[0]
    # these are add rX, pc, rX style: string = (insn_after + 8) + w for the add
    # for the three sp stores: add r3, pc, r3 at insn_va+0xc
    add_va = insn_va + 0xc
    sva = (add_va + 8 + w) & 0xFFFFFFFF
    s = cstr_at(sva)
    print(f'  {label:18s} lit@0x{la:06x}=0x{w:08x} -> str@0x{sva:06x} = {s!r}')

# --- caller function 0x1495b4 ---
print('\n=== caller function @0x1495b4 (184 B) ===')
SYM = {}
for line in open('/tmp/my-project/work/TDKR-Game/extraction/libKRHP_symbols.txt'):
    p = line.split()
    if len(p) >= 4 and p[3] == 'FUNC':
        SYM[int(p[0], 16)] = (int(p[1]), p[2] if len(p) > 4 else p[-1])
DEM = {}
for line in open('/tmp/my-project/work/TDKR-Game/extraction/libKRHP_symbols_demangled.txt'):
    if '::' in line:
        DEM[line.strip()] = None
size, _ = SYM.get(0x1495b4, (184, '?'))
code = RAW[va2off(0x1495b4):va2off(0x1495b4) + size]
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
for ins in md.disasm(code, 0x1495b4):
    tgt = ''
    if ins.mnemonic.startswith('bl') and ins.op_str.startswith('#'):
        try:
            t = int(ins.op_str.lstrip('#'), 0)
            nm = ''
            if t in SYM:
                nm = ' <0x%x sz%d>' % (t, SYM[t][0])
            tgt = f'   ; -> 0x{t:x}{nm}'
        except ValueError:
            pass
    print(f'0x{ins.address:06x}: {ins.mnemonic:8s} {ins.op_str}{tgt}')

# callers of 0x1495b4
print('\n=== BL xrefs to 0x1495b4 ===')
for (v, o, fs, ms) in SEGS:
    if ms == 0:
        continue
    blob = RAW[o:o + fs]
    for i in range(0, len(blob) - 4, 2):
        w = struct.unpack_from('<I', blob, i)[0]
        if (w & 0x0F000000) == 0x0B000000:
            imm24 = w & 0x00FFFFFF
            if imm24 & 0x800000:
                imm24 -= 1 << 24
            src = v + i
            if (src + 8 + imm24 * 4) & 0xFFFFFFFF == 0x1495b4:
                print(f'  BL from 0x{src:06x}')

# vtable context at 0xa67e2c
print('\n=== words around vtable slot 0xa67e2c ===')
for k in range(-8, 9, 4):
    va = 0xa67e2c + k
    w = struct.unpack('<I', RAW[va2off(va):va2off(va) + 4])[0]
    sym = ''
    if w in SYM:
        sym = f' <FUNC sz{SYM[w][0]}>'
    print(f'  0x{va:06x}: 0x{w:08x}{sym}')
