#!/usr/bin/env python3
"""s45 T1a step 3: follow the 307-record pointer structure.

Records @0x23308, stride 260 B. Observed: {ptr,cnt} pairs at slots 13/14, 15/16,
17/18; name-pool offsets at slots 63/64. If slot 63 -> dae material name for
record i, record index == material index confirmed. Then dump the pointer
targets of record 73 looking for sampler values (image 56 = roads_details).
"""
import struct, io, zipfile
import numpy as np

def load_bres():
    P = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
    raw = open(P, 'rb').read()
    return zipfile.ZipFile(io.BytesIO(raw)).read('little_endian_not_quantized.bdae')

bres = load_bres()
BASE, REC, N = 0x23308, 260, 307
u32 = np.frombuffer(bres, '<u4', len(bres) // 4)

def cstr(off):
    e = bres.index(b'\0', off)
    return bres[off:e].decode('ascii', 'replace')

# name-pointer check: slot 63 for records 0..5 and 70..76
print('=== slot63/64 name strings ===')
for i in list(range(6)) + list(range(70, 77)):
    a = BASE + i * REC
    w63 = int(u32[a // 4 + 63]); w64 = int(u32[a // 4 + 64])
    try:
        s63 = cstr(w63)
    except Exception:
        s63 = '<bad>'
    print(f'  rec {i:3d}: w63 {w63:#x} -> {s63[:48]!r}   w64 {w64:#x}')

# record header shape: diff slot12 (1 for all?) and slot37/50 constants
s12 = [int(u32[(BASE + i * REC) // 4 + 12]) for i in range(N)]
print('slot12 values:', sorted(set(s12)), 'count', len(s12))

# dump pointer-target blocks of record 73 and record 0
def dump_block(off, nbytes, label):
    print(f'\n--- {label} @ {off:#x} ({nbytes} B) ---')
    w = u32[off // 4:off // 4 + nbytes // 4]
    f = np.frombuffer(bres, '<f4', len(bres) // 4)[off // 4:off // 4 + nbytes // 4]
    for j in range(0, len(w), 6):
        row = []
        for k in range(j, min(j + 6, len(w))):
            v = int(w[k]); fv = float(f[k])
            txt = f'{v:#x}' if (v > 0x10000 and abs(fv) < 1e-30) else (f'{fv:.4g}' if abs(fv) < 1e7 and abs(fv) > 1e-30 or fv == 0 else f'{v}')
            row.append(f'{k*4:#05x}:{txt}')
        print('   ' + ' | '.join(row))

for i in (73, 0):
    a = BASE + i * REC
    w = u32[a // 4:a // 4 + 65]
    for s in (13, 15, 17):
        ptr = int(w[s]); cnt = int(w[s + 1])
        if ptr and ptr < len(bres) and cnt:
            dump_block(ptr, min(cnt * 4 + 16, 256), f'rec{i} slot{s} target (cnt={cnt})')
        elif ptr and ptr < len(bres):
            dump_block(ptr, 64, f'rec{i} slot{s} target (cnt={cnt})')
