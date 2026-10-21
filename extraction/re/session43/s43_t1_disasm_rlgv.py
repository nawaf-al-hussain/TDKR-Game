#!/usr/bin/env python3
"""s43 T1a: static disasm of CLuaScriptManager::ResetLuaGlobalVars @0x14b478 (664 B, ARM)
+ xref scan for BL to it across the whole image + data-word references."""
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


TARGET = 0x14b478
SIZE = 664
off = va2off(TARGET)
code = RAW[off:off + SIZE]
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
print(f'=== ResetLuaGlobalVars @0x{TARGET:x} ({SIZE} B) ===')
for ins in md.disasm(code, TARGET):
    tgt = ''
    if ins.mnemonic.startswith('bl') and ins.op_str.startswith('#'):
        try:
            t = int(ins.op_str.lstrip('#'), 0)
            tgt = f'   ; -> 0x{t:x}'
        except ValueError:
            pass
    print(f'0x{ins.address:06x}: {ins.mnemonic:8s} {ins.op_str}{tgt}')

print('\n=== BL/BLX xrefs to 0x%x ===' % TARGET)
hits = []
for (v, o, fs, ms) in SEGS:
    if ms == 0:
        continue
    blob = RAW[o:o + fs]
    for i in range(0, len(blob) - 4, 2):
        w = struct.unpack_from('<I', blob, i)[0]
        if (w & 0x0F000000) == 0x0B000000:  # BL (any cond)
            imm24 = w & 0x00FFFFFF
            if imm24 & 0x800000:
                imm24 -= 1 << 24
            src_va = v + i
            dst = (src_va + 8 + imm24 * 4) & 0xFFFFFFFF
            if dst == TARGET:
                hits.append(src_va)
for h in hits:
    print(f'  BL from 0x{h:06x}')

print('\n=== data word refs ===')
dw = struct.pack('<I', TARGET)
idx = 0
while True:
    idx = RAW.find(dw, idx)
    if idx < 0:
        break
    for (v, o, fs, ms) in SEGS:
        if o <= idx < o + fs:
            print(f'  word at va 0x{v + (idx - o):06x} == 0x{TARGET:x}')
            break
    idx += 1
