#!/usr/bin/env python3
"""s46 T1 final probes: (A) BRES header section directory; (B) material-name
<-> tga-name string co-location in the compiled bdae pools."""
import io, zipfile, json, struct
import numpy as np

P = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
bres = zipfile.ZipFile(io.BytesIO(open(P, 'rb').read())).read('little_endian_not_quantized.bdae')
NB = len(bres)
print('bdae size:', NB, hex(NB))

# --- A: header dump: first 0x120 bytes as u32 with string annotations ---
def cstr(off, maxn=96):
    if not (0 < off < NB):
        return None
    e = bres.find(b'\0', off)
    if e < 0 or e == off or e - off > maxn:
        return None
    s = bres[off:e]
    try:
        t = s.decode('ascii')
    except Exception:
        return None
    return t if all(32 <= ord(c) < 127 for c in t) else None

u32 = np.frombuffer(bres, '<u4', NB // 4)
print('--- header 0x00..0x120 (u32; annotations: as-string / as-off-str) ---')
for i in range(0x120 // 4):
    off = i * 4
    v = int(u32[i])
    note = ''
    s = cstr(v)
    if s:
        note = f' -> {s!r}'
    elif 0 < v < NB:
        s2 = cstr(v)
        if s2:
            note = f' -> @{v:#x} {s2!r}'
    print(f'  {off:#06x}: {v:#010x}{note}')

# --- B: string pool census: material names vs tga names adjacency ---
binds = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session45/s45_t1a_bindings.json'))
mat_names = [b['name'] for b in binds]
# tga names from the image table
IMG_BASE, IMG_N = 0x22a9c, 176
tga_names = []
for i in range(IMG_N):
    a = IMG_BASE + i * 12
    w = u32[a // 4: a // 4 + 3]
    t = cstr(int(w[2]))
    if t:
        tga_names.append(t)

def find_all(needle, cap=400):
    out = []
    start = 0
    while len(out) < cap:
        j = bres.find(needle, start)
        if j < 0:
            break
        out.append(j)
        start = j + 1
    return out

mat_offs = {}
for mn in mat_names[:20]:
    mat_offs[mn] = find_all(mn.encode())
tga_offs = {t: find_all(t.encode()) for t in tga_names}

print()
print('--- co-location test: within +-160 B of a material name occurrence, is there a tga name? ---')
# build sorted list of all tga offsets
tga_flat = []
for t, offs in tga_offs.items():
    for o in offs:
        tga_flat.append((o, t))
tga_flat.sort()
tga_pos = [x[0] for x in tga_flat]
import bisect
hit = 0
tot = 0
examples = []
for mn, offs in mat_offs.items():
    b = binds[[x['name'] for x in binds].index(mn)]
    exp_d = None
    dm = b['bind'].get('DiffuseMap')
    if isinstance(dm, dict):
        exp_d = dm.get('tga')
    for o in offs:
        tot += 1
        lo = bisect.bisect_left(tga_pos, o - 160)
        hi = bisect.bisect_right(tga_pos, o + 160)
        near = [tga_flat[k][1] for k in range(lo, hi)]
        if near:
            hit += 1
            if len(examples) < 10:
                examples.append((mn, hex(o), exp_d, near[:6]))
print(f'material-name occurrences with a tga name within +-160 B: {hit}/{tot}')
for e in examples:
    print('   ', e)
