#!/usr/bin/env python3
"""Bake-region extractor v2 — code-verified frame (session 6).

CComponentBeastObjectComponent::Load (@0x2e1e8c) reads:
    vec4 so1                (Coord1_scaleoffset: scaleU, scaleV, offU, offV)
    string page1            (runtime bake page -> material 'LightMap' slot)
    vec4 so2                (low/-0 path tile; consumed by the NEXT component)
CBeastObjectComponent::Load (@0x2a1ea4) then binds:
    getTexture(page1), getTexture('LightMapSampler.tga'),
    uniform 'LightMapAtlas', and copies so1 into Coord1_scaleoffset.
Shader (LightMapDC-v.glsl):
    vCoord1 = (Coord1*Coord1_scaleoffset.xy + Coord1_scaleoffset.zw)
              * LightMapAtlas.xy + LightMapAtlas.zw

Stream frame around each record (BE):
    [f32 so1 x4][u32 page1 idx][f32 so2 x4][u32 page2 idx][u32 W][u32 H][s32 -1]
    [u32 hash][u8 1][u32 objectId][...] [u32 mesh bdae idx][4 x u8] ...

v1 (session 5) only scanned page strings starting with 'BakeGroup' — the
GC_LongDist_Island*_FP* pages of the 8 runtime-bake footprints were never
seen. v2 scans every '*.tga' string and decodes the full frame.

Output: extraction/re/bake_regions_v2.json
"""
import struct, json, re, sys
from collections import defaultdict

RAW = '/home/z/my-project/download/TDKR_assets/raw/game_config'
OUT = '/home/z/my-project/work/TDKR-Game/extraction/re/bake_regions_v2.json'
NOISE = re.compile(r'collision|placeholder|batman|reflection|staticmesh|shadow', re.I)

def load(lvcname):
    d = open(f'{RAW}/{lvcname}.lvc', 'rb').read()
    tbl_off = struct.unpack_from('>I', d, 4)[0]
    p = tbl_off; cnt = struct.unpack_from('>I', d, p)[0]; p += 4
    strings = []
    for _ in range(cnt):
        ln = struct.unpack_from('>I', d, p)[0]; p += 4
        strings.append(d[p:p + ln].decode('utf-8', 'replace')); p += ln
    return d, tbl_off, cnt, strings

def f32(d, a): return struct.unpack_from('>f', d, a)[0]
def u32(d, a): return struct.unpack_from('>I', d, a)[0]
def i32(d, a): return struct.unpack_from('>i', d, a)[0]

def valid_so(so):
    s_u, s_v, o_u, o_v = so
    if not (0.0005 <= s_u <= 1.01 and 0.0005 <= s_v <= 1.01):
        return False
    if not (-0.002 <= o_u <= 1.002 and -0.002 <= o_v <= 1.002):
        return False
    if o_u + s_u > 1.01 or o_v + s_v > 1.01:
        return False
    return True

def is_pow2(x): return x > 0 and (x & (x - 1)) == 0

def extract(lvcname):
    d, tbl_off, cnt, strings = load(lvcname)
    # index every .tga page string
    tga_idx = [i for i, s in enumerate(strings) if s.endswith('.tga')]
    recs = []
    for si in tga_idx:
        pat = struct.pack('>I', si)
        o = 9
        while True:
            o = d.find(pat, o, tbl_off)
            if o < 0:
                break
            o += 1
            base = o - 1
            so1 = [f32(d, base - 16 + 4 * k) for k in range(4)]
            so2 = [f32(d, base + 4 + 4 * k) for k in range(4)]
            page2_i = u32(d, base + 20)
            W, H, mip = u32(d, base + 24), u32(d, base + 28), i32(d, base + 32)
            if page2_i >= cnt or not strings[page2_i].endswith('.tga'):
                continue
            if mip != -1 or not is_pow2(W) or not is_pow2(H):
                continue
            if not valid_so(so1) or not valid_so(so2):
                continue
            # mesh component: first plausible bdae string in [base+36, base+220]
            mesh = None
            for dq in range(36, 220, 4):
                v = u32(d, base + dq)
                if v < cnt:
                    cand = strings[v]
                    if cand.endswith('.bdae') and not NOISE.search(cand):
                        mesh = cand
                        break
            recs.append(dict(
                lvc=lvcname, off=base,
                page=strings[si].replace('.tga', ''),
                so1=[round(x, 7) for x in so1],
                page_low=strings[page2_i].replace('.tga', ''),
                so2=[round(x, 7) for x in so2],
                dims=[W, H],
                mesh=mesh.replace('.bdae', '') if mesh else None,
            ))
    return recs

def main():
    allrows = []
    for lv in ('GothamCity', 'GothamCity_Island2'):
        rows = extract(lv)
        n_mesh = sum(1 for r in rows if r['mesh'])
        print(f'=== {lv}: {len(rows)} bake frames ({n_mesh} with mesh)')
        allrows += rows
    json.dump(allrows, open(OUT, 'w'), indent=1)
    print(f'saved {OUT} ({len(allrows)} records)')

if __name__ == '__main__':
    main()
