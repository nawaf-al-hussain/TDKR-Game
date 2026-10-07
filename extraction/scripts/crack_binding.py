#!/usr/bin/env python3
"""Crack the sampler->texture binding: dump render records + sampler records
with values for key files, and validate small-int-as-texture-index."""
import struct, re, glob, random
from collections import Counter

SAMP_SET = ('DiffuseMap', 'DiffuseMap2', 'DiffuseMap_alpha', 'LightMap', 'NormalMap',
            'NormalMap1', 'NormalMap2', 'ReflectionMap', 'ReflectionMapSampler',
            'DiffuseMaskSampler', 'SpecularLevel', 'Glossiness', 'LightMapAtlas')

def strings(d, limit):
    out = {}
    for m in re.finditer(rb'[\x20-\x7e]{3,}\x00', d[:limit]):
        start, stop = m.start(), m.end() - 1
        L = stop - start
        if start >= 4:
            (Pl,) = struct.unpack_from('<I', d, start - 4)
            if Pl == L:
                out[start - 4] = d[start:stop].decode()   # prefix offset
                out[start] = d[start:stop].decode()       # char offset
    return out

def analyze(path, verbose=True):
    d = open(path, 'rb').read()
    if d[:4] != b'BRES': return None
    h = struct.unpack_from('<14I', d, 0)
    G = h[10]
    strs = strings(d, G)
    texs = [s for off, s in sorted(strs.items()) if s.endswith('.tga')]
    samp_off = {off: s for off, s in strs.items() if s in SAMP_SET}
    n_words = G // 4
    words = struct.unpack_from(f'<{n_words}I', d, 0)
    # records: word[i] == word[i+1] == samp offset; type=word[i+2]
    recs = []
    for i in range(2, n_words - 6):
        v = words[i]
        if v in samp_off and words[i+1] == v:
            recs.append((i*4, samp_off[v], words[i+2], words[i+3], words[i+4], words[i+5], words[i+6]))
    return d, h, G, strs, texs, recs

def show(name):
    p = f'/home/z/my-project/download/TDKR_assets/raw/l_gothamcity/{name}.bdae.bin'
    r = analyze(p)
    if not r: print(name, 'skip'); return
    d, h, G, strs, texs, recs = r
    print(f"\n===== {name}: {len(texs)} textures, {len(recs)} sampler records =====")
    print("  texlist:")
    for i, t in enumerate(texs):
        print(f"    [{i:2}] {t}")
    type_hist = Counter(typ for _, _, typ, *_ in recs)
    print("  record type histogram:", dict(type_hist))
    # for each record show context words
    for off, nm, typ, f3, v1, v2, v3 in recs[:24]:
        ctx = ' | '.join(f"{x:#x}" if x > 64 else str(x) for x in (typ, f3, v1, v2, v3))
        idxnote = ''
        for cand in (v1, v2, v3):
            if isinstance(cand, int) and 0 <= cand < len(texs) and cand > 3:
                idxnote += f"  <== tex[{cand}]={texs[cand]}"
        print(f"    @{off:#07x} {nm:22s} ctx: {ctx}{idxnote}")

for nm in ['GC_Bigbridge', 'GC_island1_LongDist', 'GC_Diner', 'HC_Prop_BillboardRoof_01']:
    show(nm)
