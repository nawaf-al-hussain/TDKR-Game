#!/usr/bin/env python3
"""s43 T1e: walk UP the BL graph from 0x3f36c8 to a named export (depth 3),
to identify which file format carries the serialized globals table."""
import struct

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

SYM = {}
DEM = {}
for line in open('/tmp/my-project/work/TDKR-Game/extraction/libKRHP_symbols.txt'):
    p = line.split()
    if len(p) >= 4 and p[3] == 'FUNC':
        SYM[int(p[0], 16)] = int(p[1])
        DEM[int(p[0], 16)] = p[-1]

# build BL site index: src -> dst (coarse, for targeted lookups only)
def bls_to(target):
    out = []
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
                if (src + 8 + imm24 * 4) & 0xFFFFFFFF == target:
                    out.append(src)
    return out


def prologue_start(va):
    o = va2off(va) if False else None
    # local va2off
    for (v, o, fs, ms) in SEGS:
        if v <= va < v + fs:
            o = o + (va - v)
            break
    for back in range(0, 0x1000, 4):
        w = struct.unpack_from('<I', RAW, o - back)[0]
        if (w & 0xFFFF0000) == 0xE92D0000:
            return va - back
    return None


def va2off_local(va):
    for (v, o, fs, ms) in SEGS:
        if v <= va < v + fs:
            return o + (va - v)
    return None


frontier = [0x3f36c8]
seen = set()
for depth in range(3):
    nxt = []
    print(f'--- depth {depth + 1} callers ---')
    for f in frontier:
        if f in seen:
            continue
        seen.add(f)
        for src in bls_to(f):
            fn = [a for a, s in SYM.items() if a <= src < a + s]
            if fn:
                a = fn[0]
                print(f'  0x{src:06x} -> inside NAMED fn 0x{a:06x} {DEM[a]}')
            else:
                st = prologue_start(src)
                print(f'  0x{src:06x} -> inside static fn ~0x{st:06x}' if st else f'  0x{src:06x} -> ?')
                if st and st not in seen:
                    nxt.append(st)
    frontier = nxt
    if not frontier:
        break
