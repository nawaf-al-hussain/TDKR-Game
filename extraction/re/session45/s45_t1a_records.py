#!/usr/bin/env python3
"""s45 T1a step 2: decode the 260-byte per-material records at 0x23308 (307 records).

Validation anchors: mat73 diffuse = image56 (gothamcity_roads_details.tga);
284/307 materials have a LightMap; batch_info M=307.
"""
import struct, io, zipfile
import numpy as np

def load_bres():
    P = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
    raw = open(P, 'rb').read()
    return zipfile.ZipFile(io.BytesIO(raw)).read('little_endian_not_quantized.bdae')

bres = load_bres()
BASE, REC = 0x23308, 260
N = (0x36ac8 - BASE) // REC
print('records:', N, 'stride', REC)

u16 = np.frombuffer(bres, '<u2', len(bres) // 2)
u32 = np.frombuffer(bres, '<u4', len(bres) // 4)
f32 = np.frombuffer(bres, '<f4', len(bres) // 4)

def rec_range(i):
    a = BASE + i * REC
    return a, a + REC

# where do u16==56 hits fall (which record, which u16 slot)?
hits56 = [j for j in range(BASE // 2, (BASE + N * REC) // 2) if u16[j] == 56]
print(f'u16==56 hits in record region: {len(hits56)}')
for j in hits56[:20]:
    off = j * 2
    ri = (off - BASE) // REC
    slot = (off - (BASE + ri * REC)) // 2
    print(f'  off {hex(off)} -> record {ri}, u16 slot {slot} (byte {slot*2})')

# structural map of one record: show u32 words + floats for records 0, 73, 1
def dump_rec(i, label):
    a, b = rec_range(i)
    print(f'\n=== record {i} {label} ({hex(a)}..{hex(b)}) ===')
    w = u32[a // 4:b // 4]
    f = f32[a // 4:b // 4]
    # print words that are small ints or floats in a compact grid
    for k in range(0, 65, 13):
        row = []
        for j in range(k, min(k + 13, 65)):
            v = int(w[j]); fv = float(f[j])
            if abs(fv) < 1e6 and (fv == int(fv) and abs(fv) < 100000 or abs(fv) < 1e4):
                row.append(f'{j}:w{v if v < 10**7 else hex(v)}/{fv:.4g}')
            else:
                row.append(f'{j}:{v if v < 10**7 else hex(v)}')
        print('   ' + ' | '.join(row))

for i, lab in ((0, 'first'), (73, 'mat73?'), (1, 'second')):
    dump_rec(i, lab)

# per-slot census across all 307 records: which u32 slots are constant / small / float-like
print('\n=== per-slot census (307 records, 65 u32 slots) ===')
M = np.array([u32[a // 4:a // 4 + 65] for a, b in (rec_range(i) for i in range(N))], dtype=np.uint32)
for s in range(65):
    col = M[:, s]
    uniq = len(np.unique(col))
    f = f32[BASE // 4 + s::65 * 0]  # unused
    fcol = np.array([f32[(BASE + i * REC) // 4 + s] for i in range(N)])
    fin = np.isfinite(fcol)
    small = int((col < 176).sum())
    if uniq <= 6 or small > N * 0.7:
        fu = np.unique(fcol[np.isfinite(fcol) & (np.abs(fcol) < 1e6)])
        fs = ' floats[' + ','.join(f'{x:.4g}' for x in fu[:5]) + (f'..{len(fu)}u' if len(fu) > 5 else '') + ']' if fin.any() and len(fu) <= 5 else ''
        print(f'  slot {s:2d}: uniq u32 {uniq:4d}  <176: {small:4d}{fs}')
