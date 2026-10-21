#!/usr/bin/env python3
"""s47 T1 step A: BRES directory + fixup-list hunt.
Question: are the 651 empty sampler value slots (0xffffffff terminals in the
compiled setparam value blocks) targets of load-time fixups? If yes, the
per-material image binding is IN the file (encoded via fixups) and can be
extracted directly; if no, the engine must synthesize bindings at scene
construction (XML path) and the compiled slots stay empty.
Also: dump the 224 B unidentified section @0x229b4.
"""
import io, zipfile, struct, json
import numpy as np

P = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
z = zipfile.ZipFile(io.BytesIO(open(P, 'rb').read()))
LE = z.read('little_endian_not_quantized.bdae')
NB = len(LE)
print('LE variant size', hex(NB))

u32 = np.frombuffer(LE, '<u4', NB // 4)
u16 = np.frombuffer(LE, '<u2', NB // 2)

# ---- header dump ----
print('--- header first 0x60 bytes ---')
for off in range(0, 0x60, 4):
    print(f'  {off:#07x}: {int(u32[off//4]):#010x}  {LE[off:off+4].hex()}')

print('magic ascii:', LE[:4], LE[4:8])

# ---- BRES directory parse (0x3c..0x168a8 per s46) ----
DIR_A, DIR_B = 0x3c, 0x168a8
n = (DIR_B - DIR_A)
for stride in (8, 12, 16, 20, 24):
    print(f'dir stride {stride}: count {n//stride}')

print('--- dir head words ---')
for k in range(0, 24):
    off = DIR_A + k * 4
    print(f'  {off:#07x}: {int(u32[off//4]):#010x}')

# ---- node 73 + 302 sampler value blocks ----
BASE, REC = 0x23308, 260
def node_words(i):
    a = BASE + i * REC
    return [int(u32[(a + k * 4) // 4]) for k in range(REC // 4)]

for i in (73, 302):
    ws = node_words(i)
    print(f'node {i}: tech=({ws[13]:#x},{ws[14]}) setparam=({ws[15]:#x},{ws[16]}) '
          f'rstate=({ws[17]:#x},{ws[18]})')

EMPTY_SLOTS = []
SP_DESCS = []
for i in range(307):
    ws = node_words(i)
    sp_ptr, sp_n = ws[15], ws[16]
    if not (0 < sp_ptr < NB) or sp_n == 0 or sp_n > 64:
        continue
    a = sp_ptr
    for k in range(sp_n):
        w0, w1 = int(u32[a // 4]), int(u32[a // 4 + 1])
        SP_DESCS.append((i, a, w0, w1))
        if w0 == 13:
            va = a + 0x14
            for e in range(4):
                slot = va + e * 20 + 12
                v = int(u32[slot // 4])
                EMPTY_SLOTS.append((i, a, slot, v))
        a += 20
print('setparam descs:', len(SP_DESCS), 'sampler slots walked:', len(EMPTY_SLOTS))
vals = sorted(set(v for (_, _, _, v) in EMPTY_SLOTS))
print('distinct value words:', [hex(v) for v in vals][:8])
empty_terminal = sum(1 for (_, _, _, v) in EMPTY_SLOTS if v == 0xffffffff)
print('slots holding 0xffffffff:', empty_terminal, '/', len(EMPTY_SLOTS))

# ---- fixup hunt ----
slotset = set(s for (_, _, s, _) in EMPTY_SLOTS)
hits = []
for stride in (4, 8, 12, 16):
    cnt = (DIR_B - 0x3c) // stride
    for k in range(cnt):
        off = 0x3c + k * stride
        v = int(u32[off // 4])
        if v in slotset:
            hits.append((stride, hex(off), hex(v)))
print('dir-region fixup hits:', len(hits), hits[:10] if hits else '')

whole_hits = []
for k in range(NB // 4):
    v = int(u32[k])
    if v in slotset:
        off = k * 4
        if off not in slotset:
            whole_hits.append((hex(off), hex(v)))
print('whole-file u32 == slot-address occurrences:', len(whole_hits),
      whole_hits[:12] if whole_hits else '')

# ---- 224 B section ----
print('--- 224 B section 0x229b4..0x22a94 ---')
for off in range(0x229b4, 0x22a94, 4):
    v = int(u32[off // 4])
    print(f'  {off:#07x}: {v:#010x}  {LE[off:off+4].hex()}')
