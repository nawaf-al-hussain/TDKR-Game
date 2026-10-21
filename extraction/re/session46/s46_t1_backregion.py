#!/usr/bin/env python3
"""s46 T1: hunt the engine-side per-material image bindings in the compiled
bdae back region (0x36ac8..0x6f164). Targeted probe: the TRUE diffuse/lightmap
tga pointers and name pointers (from image table + source.dae binding table)
must appear per-material somewhere. Find where, decode the row structure."""
import io, zipfile, json
import numpy as np

P = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
bres = zipfile.ZipFile(io.BytesIO(open(P, 'rb').read())).read('little_endian_not_quantized.bdae')
NB = len(bres)
u32 = np.frombuffer(bres, '<u4', NB // 4)
u16 = np.frombuffer(bres, '<u2', NB // 2)

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

IMG_BASE, IMG_N = 0x22a9c, 176
images = []
for i in range(IMG_N):
    a = IMG_BASE + i * 12
    w = u32[a // 4: a // 4 + 3]
    images.append({'name_ptr': int(w[0]), 'dup': int(w[1]), 'tga_ptr': int(w[2]),
                   'name': cstr(int(w[0])), 'tga': cstr(int(w[2]))})

# source.dae binding table (s45): list of 307 {i, name, bind{...}}
binds = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session45/s45_t1a_bindings.json'))
tga_to_ord = {}
for idx, im in enumerate(images):
    tga_to_ord[im['tga']] = idx

def bind_ord(b, key):
    v = b.get(key)
    if isinstance(v, dict) and 'ordinal' in v:
        return v['ordinal']
    return None

def bind_tga(b, key):
    v = b.get(key)
    if isinstance(v, dict) and 'tga' in v:
        return v['tga']
    return None

BACK0, BACK1 = 0x36ac8, 0x6f164
mats = []
for b in binds:
    d_ord = bind_ord(b['bind'], 'DiffuseMap')
    l_ord = bind_ord(b['bind'], 'LightMap')
    d_tga = images[d_ord]['tga_ptr'] if d_ord is not None else None
    l_tga = images[l_ord]['tga_ptr'] if l_ord is not None else None
    mats.append({'i': b['i'], 'name': b['name'], 'd_ord': d_ord, 'l_ord': l_ord,
                 'd_tga': d_tga, 'l_tga': l_tga})

# which image ptrs occur in the back region at all (u32 view)?
hits = {}
for im in images:
    for key in ('tga_ptr', 'name_ptr'):
        v = im[key]
        cnt = int(np.count_nonzero(u32[BACK0 // 4: BACK1 // 4] == v))
        if cnt:
            hits[(im['tga'], key)] = cnt
print('image ptr occurrences in back region:', len(hits))
for k, v in sorted(hits.items(), key=lambda kv: -kv[1])[:20]:
    print('   ', k, v)

# offsets of mat73's diffuse tga ptr and lightmap tga ptr in the whole file
probe = []
for m in mats[:80]:
    if m['d_tga']:
        offs = np.where(u32 == m['d_tga'])[0] * 4
        offs = [int(o) for o in offs if BACK0 <= o < BACK1]
        loffs = []
        if m['l_tga']:
            lo = np.where(u32 == m['l_tga'])[0] * 4
            loffs = [int(o) for o in lo if BACK0 <= o < BACK1]
        probe.append((m['i'], m['d_ord'], m['l_ord'], offs, loffs))
print()
print('mat -> back-region offsets of its d_tga (first 40 mats with diffuse):')
for p in probe[:40]:
    print(f"  mat{p[0]:3d} d_ord={p[1]:3d} l_ord={p[2]} d_offs={[hex(x) for x in p[3]][:6]} l_offs={[hex(x) for x in p[4]][:6]}")

# u16 variant: image ordinals 0..175 as u16 in back region rows
print()
print('=== u16 ordinal hunt: rows where u16==d_ord near u16==l_ord ===')
u16back = u16[BACK0 // 2: BACK1 // 2]
hit_rows = 0
for m in mats[:80]:
    if m['d_ord'] is None or m['l_ord'] is None:
        continue
    do = np.where(u16back == m['d_ord'])[0]
    lo = np.where(u16back == m['l_ord'])[0]
    if len(do) == 0 or len(lo) == 0:
        continue
    # same-row pairs within 8 u16 of each other
    ds = set((int(x) // 100) for x in do)
    common = ds & set((int(x) // 100) for x in lo)
    if common:
        hit_rows += 1
        if hit_rows <= 8:
            ex_d = [int(x) for x in do if (int(x) // 100) in common][:4]
            ex_l = [int(x) for x in lo if (int(x) // 100) in common][:4]
            print(f"  mat{m['i']}: d_ord={m['d_ord']} l_ord={m['l_ord']} d@{[hex(BACK0+2*x) for x in ex_d]} l@{[hex(BACK0+2*x) for x in ex_l]}")
print('mats (of first 80) with co-occurring d/l u16 ordinals in a 100-u16 window:', hit_rows)
