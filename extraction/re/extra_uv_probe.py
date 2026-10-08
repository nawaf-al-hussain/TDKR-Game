#!/usr/bin/env python3
"""Extract the stride-28 extra dwords from LongDist footprint meshes and test
them (as 2x u16 packed UV channels) against the bake-record quads + pages."""
import struct, os, json
import numpy as np
from PIL import Image

RAW = '/home/z/my-project/download/TDKR_assets/raw/l_gothamcity'
PAGES = '/home/z/my-project/download/TDKR_assets/pages'
RECS = json.load(open('/home/z/my-project/work/TDKR-Game/extraction/re/bake_regions.json'))
LVC = '/home/z/my-project/download/TDKR_assets/raw/game_config/GothamCity.lvc'

def meshes_raw(path):
    """like parse_meshes but also returns extra1 (+20) and extra2 (+24) dwords"""
    d = open(path, 'rb').read()
    h = struct.unpack_from('<14I', d, 0)
    G = h[10]
    out = []
    g = G
    while g + 0x68 <= len(d):
        # reuse the block finder via parse_meshes internals is complex; quick hack:
        # find footer chain using bdae_extract's parse_first_block
        from bdae_extract import parse_first_block
        blk = parse_first_block(d, g, False)
        if blk is None:
            break
        score, count, ndw, stride, start, footer, maxIdx, numIdx = blk
        s0 = footer + 0x14
        e = d.index(b'\0', s0)
        mat = d[s0:e].decode('ascii', 'replace')
        idx_off = s0 + ((e - s0 + 1 + 3) & ~3)
        recs = []
        for i in range(count):
            o = start + i * stride
            u, v = struct.unpack_from('<2H', d, o + 16)
            e1 = struct.unpack_from('<I', d, o + 20)[0] if stride >= 24 else 0
            e2 = struct.unpack_from('<I', d, o + 24)[0] if stride >= 28 else 0
            recs.append((u / 65535.0, v / 65535.0, e1, e2))
        out.append(dict(offset=g, count=count, stride=stride, mat=mat, recs=recs,
                        numIdx=numIdx, idx_off=idx_off))
        g = (idx_off + numIdx * 2 + 3) & ~3
    return out

def dwords_to_uv(dw, hi_first=False):
    a = dw & 0xFFFF
    b = (dw >> 16) & 0xFFFF
    pair = (b, a) if hi_first else (a, b)
    return (pair[0] / 65535.0, pair[1] / 65535.0)

def main():
    d = open(LVC, 'rb').read()
    tbl_off = struct.unpack_from('>I', d, 4)[0]
    p = tbl_off; cnt = struct.unpack_from('>I', d, p)[0]; p += 4
    for _ in range(cnt):
        ln = struct.unpack_from('>I', d, p)[0]; p += 4; p += ln

    by_mesh = {}
    for r in RECS:
        if r['lvc'] == 'GothamCity' and r.get('mesh'):
            by_mesh.setdefault(r['mesh'], r)

    for stem in ('gc_footprint_vc', 'gc_footprint_ia', 'gc_footprint_cn',
                 'gc_footprint_ac', 'gc_footprint_af'):
        r = by_mesh.get(stem)
        if not r:
            continue
        suffix = stem.rsplit('_', 1)[-1].upper()
        path = os.path.join(RAW, f'GC_Footprint_{suffix}_LongDist.bdae')
        if not os.path.exists(path):
            continue
        o = r['off']
        pre = [struct.unpack_from('>f', d, o - 16 + 4 * k)[0] for k in range(4)]
        post = [struct.unpack_from('>f', d, o + 4 + 4 * k)[0] for k in range(4)]
        ms = meshes_raw(path)
        print(f'\n=== {stem}  page={r["page"]}  pre={[round(x,5) for x in pre]}  post={[round(x,5) for x in post]}')
        for m in ms:
            if m['stride'] < 24:
                print(f'  mesh stride={m["stride"]} mat={m["mat"]!r} (no extra)')
                continue
            for ch, pick in (('e1', lambda t: dwords_to_uv(t[2])), ('e2', lambda t: dwords_to_uv(t[3])),
                             ('e1hi', lambda t: dwords_to_uv(t[2], True)), ('e2hi', lambda t: dwords_to_uv(t[3], True))):
                uvs = np.array([pick(t) for t in m['recs']], dtype=np.float64)
                if not np.isfinite(uvs).all():
                    continue
                print(f'  stride={m["stride"]} mat={m["mat"][:30]!r} {ch}: u[{uvs[:,0].min():.4f},{uvs[:,0].max():.4f}] '
                      f'v[{uvs[:,1].min():.4f},{uvs[:,1].max():.4f}] n={m["count"]}')

if __name__ == '__main__':
    main()
