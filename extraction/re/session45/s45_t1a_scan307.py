#!/usr/bin/env python3
"""s45 T1a step 6: scan all 307 effect nodes' setparam blocks for texture values.

Param entry shape (from rec73): {name_ptr, type, a, b, vptr1, vptr2} (24 B).
Sampler value chain: vptr1 -> {u32}, vptr2 -> {u32 or ptr->u32}.
Collect: per record, per param: name, type, value1, value2, resolved.
Validation: dae mat73 = roads_details; count how many records have non-null
sampler values; look for image indices < 176.
"""
import numpy as np, io, zipfile, json

P = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
bres = zipfile.ZipFile(io.BytesIO(open(P, 'rb').read())).read('little_endian_not_quantized.bdae')
u32 = np.frombuffer(bres, '<u4', len(bres) // 4)
BASE, REC, N = 0x23308, 260, 307

def cstr(off):
    if not (0 < off < len(bres)):
        return None
    e = bres.find(b'\0', off)
    if e < 0 or e == off or e - off > 120:
        return None
    try:
        t = bres[off:e].decode('ascii')
    except Exception:
        return None
    return t if all(32 <= ord(c) < 127 for c in t) else None

def deref(w):
    """if w looks like a pointer to a u32, return that u32 else None"""
    if 0x34 < w < len(bres) - 4 and w % 4 == 0:
        return int(u32[w // 4])
    return None

# image name table for reference
IMG_BASE = 0x22a9c
imgs = []
for i in range(176):
    a = IMG_BASE + i * 12
    imgs.append((cstr(int(u32[a // 4])), cstr(int(u32[a // 4 + 2]))))

rows = []
for i in range(N):
    a = BASE + i * REC
    w = [int(x) for x in u32[a // 4:a // 4 + 65]]
    pname = cstr(w[63])
    ent = {}
    for s in (13, 15, 17):
        ptr, cnt = w[s], w[s + 1]
        if not ptr or ptr >= len(bres) - 8:
            continue
        # walk up to 12 param entries from ptr
        k = 0
        p = ptr
        while k < 12:
            nm = cstr(int(u32[p // 4]))
            if nm is None:
                break
            typ = int(u32[p // 4 + 1]); aa = int(u32[p // 4 + 2]); bb = int(u32[p // 4 + 3])
            v1p = int(u32[p // 4 + 4]); v2p = int(u32[p // 4 + 5])
            v1 = deref(v1p); v2 = deref(v2p)
            v1i = int(u32[v1p // 4]) if 0 < v1p < len(bres) else None
            v2i = int(u32[v2p // 4]) if 0 < v2p < len(bres) else None
            ent[nm] = (typ, aa, bb, v1i, v2i)
            k += 1
            p += 24
            if p >= len(bres) - 24:
                break
    rows.append((i, pname, ent))

# census
from collections import Counter
param_names = Counter()
typ_by_name = {}
for i, pn, ent in rows:
    for nm, (typ, aa, bb, v1, v2) in ent.items():
        param_names[nm] += 1
        typ_by_name.setdefault(nm, Counter())[typ] += 1
print('param name census (307 records):')
for nm, c in param_names.most_common(20):
    print(f'  {nm!r}: x{c} types={dict(typ_by_name[nm])}')

# sampler-type (13) value census
vals = Counter()
nonnull = 0
sam_rows = []
for i, pn, ent in rows:
    for nm, (typ, aa, bb, v1, v2) in ent.items():
        if typ == 13:
            vals[(v1, v2)] += 1
            if v2 is not None and v2 != 0xffffffff:
                nonnull += 1
                sam_rows.append((i, pn, nm, v1, v2))
print(f'\ntype-13 (sampler) value pairs (v1,v2): {vals.most_common(8)}')
print(f'non-null v2: {nonnull}')
for r in sam_rows[:15]:
    print('  ', r[0], r[1][:40], r[2], 'v1=', r[3], 'v2=', r[4])

# any value equal to an image index < 176 in v2 position, context check on rec for mat73 order hypothesis
print('\nrecords 70..76 setparams:')
for i in range(70, 77):
    print(' ', i, rows[i][1][:44], list(rows[i][2].items())[:4])
