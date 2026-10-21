#!/usr/bin/env python3
"""s45 T1a step 9: does a geometry bdae carry real per-instance texture bindings?

Method on GC_Footprint_AA_BigBuiding.bdae (raw BRES):
1. find tga-name strings; find u32s pointing at them (=> image triples)
2. find u32s pointing at the triples (=> binding sites beyond the table itself)
3. dump the binding-site context (neighborhood words + strings)
"""
import numpy as np, re, struct

P = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla'
g = open(P, 'rb').read()
_, idxsz, tabsz, n = struct.unpack('>IIII', g[:16])
pool = g[16 + n * 16:idxsz]
for i in range(n):
    o, s, no, _ = struct.unpack('>IIII', g[16 + i * 16:16 + i * 16 + 16])
    nm = pool[no:pool.index(b'\0', no)].decode('ascii', 'replace')
    if nm == 'GC_Footprint_AA_BigBuiding.bdae':
        raw = g[o:o + s]
        break

u32 = np.frombuffer(raw, '<u4', len(raw) // 4)
print('size', len(raw))

def cstr(off):
    if not (0 < off < len(raw)):
        return ''
    e = raw.find(b'\0', off)
    if e < 0 or e == off or e - off > 120:
        return ''
    return raw[off:e].decode('ascii', 'replace')

# 1. tga strings -> pointers
tga_hits = {}
for m in re.finditer(rb'[A-Za-z0-9_]{3,40}\.tga', raw):
    s = m.group(0).decode()
    ptrs = np.where(u32 == m.start())[0] * 4
    tga_hits[s] = ptrs
print(f'{len(tga_hits)} tga names; pointer hits per name:')
for k, v in list(tga_hits.items())[:6]:
    print(f'  {k}: {[hex(p) for p in v]}')

# 2. collect triples: a pointer to a tga string is the 3rd word of a triple {img,img,tga}
triples = set()
for s, ptrs in tga_hits.items():
    for p in ptrs:
        base = p - 8
        if base < 0:
            continue
        p1 = int(u32[base // 4]); p2 = int(u32[base // 4 + 1])
        if 0 < p1 < len(raw) and p1 == p2 and cstr(p1):
            triples.add(base)
print(f'image triples found: {len(triples)}')

# 3. references to triples from OUTSIDE the table
if triples:
    lo, hi = min(triples), max(triples) + 12
    refs = {}
    tv = np.array(sorted(triples), dtype=np.uint32)
    for t in sorted(triples)[:60]:
        hits = np.where(u32 == t)[0] * 4
        for h in hits:
            if not (lo <= h < hi):
                refs.setdefault(t, []).append(h)
    ext = {t: r for t, r in refs.items() if r}
    print(f'triples referenced from outside the table: {len(ext)}')
    for t, r in list(ext.items())[:5]:
        for h in r[:2]:
            print(f'  triple {t:#x} referenced at {h:#x}; context:')
            for off in range(h - 32, h + 36, 4):
                v = int(u32[off // 4])
                cs = cstr(v)
                print(f'    {off:#x}: {v:#010x}' + (f' -> {cs!r}' if cs else ''))
