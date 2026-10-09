#!/usr/bin/env python3
"""Band-containment analysis: for every flat street segment, test which band
atlas page has a band that CONTAINS the segment's v-range. This is the
authoritative page assignment (structural, not score-based)."""
import struct
import numpy as np
from PIL import Image

ZONE = '/home/z/my-project/work/zone'
PNG = '/home/z/my-project/download/TDKR_assets/textures_png'

BAND_PAGES = ['GothamCity_Road_v1_Island_1', 'GothamCity_Road_v2_Island_1',
              'GothamCity_Road_Island_2', 'gothamcity_roads_details',
              'GothamCity_Road_Crossings_Island_1']

def page_img(name):
    for a in ('l_gothamcity_tex', 'commons_tex'):
        try:
            return Image.open(f'{PNG}/{a}/{name}.png').convert('RGB')
        except Exception:
            pass
    return None

def bands_of(name, h=512):
    im = page_img(name)
    if im is None:
        return None
    g = np.asarray(im.convert('L').resize((64, h), Image.BILINEAR), np.float32)
    row = g.mean(1)
    gx = np.abs(np.diff(row))
    thr = gx.mean() * 1.2
    edges = [0] + [i for i in range(len(gx)) if gx[i] > thr] + [h]
    edges = sorted(set(edges))
    out = []
    for a, b in zip(edges[:-1], edges[1:]):
        if b - a > 6:
            out.append((a / h, b / h, float(row[a:b].mean())))
    return out

def parse_flat_segs(name, limit=None):
    lod = open(f'{ZONE}/{name}/lod_data.bin', 'rb').read()
    lt = open(f'{ZONE}/{name}/lod_table.bin', 'rb').read()
    u = struct.unpack(f'<{len(lt)//4}I', lt)
    n = u[0]
    pairs = [(u[1+2*k], u[2+2*k]) for k in range(n)]
    out = []
    for off, sz in pairs[:limit]:
        data_off, four, vb, ib = struct.unpack_from('<4I', lod, off + 68)
        if four != 4:
            continue
        vstart = data_off + 4
        idx = np.frombuffer(lod[vstart+vb:vstart+vb+ib], '<u2').astype(np.int32)
        real = idx[idx != 0xffff]
        mx = int(real.max()) if len(real) else 0
        stride = None
        for s in (24, 20, 32):
            if vb % s == 0 and mx < vb // s:
                t = np.frombuffer(lod[vstart:vstart+vb], '<f4').reshape(-1, s//4)[:, :3]
                if np.isfinite(t).all() and np.abs(t).max() < 6000:
                    stride = s
                    break
        if stride is None:
            continue
        nv = vb // stride
        v = np.frombuffer(lod[vstart:vstart+vb], '<f4').reshape(nv, stride//4)
        words = np.frombuffer(lod[vstart:vstart+vb], '<u4').reshape(nv, stride//4)
        if stride < 20:
            continue
        seg = dict(pos=v[:, :3].copy(), uvw=words[:, 4], idx=real.astype(np.uint32))
        if seg['uvw'] is None or np.all(seg['uvw'] == 0xffffffff):
            continue
        w = seg['uvw']
        uu = (w & 0xffff).astype(np.float32) / 65535.0
        vv = (w >> 16).astype(np.float32) / 65535.0
        p = seg['pos']
        zr = float(np.ptp(p[:, 2]))
        flat = zr < max(2.0, 0.06 * float(np.ptp(p[:, :2])))
        out.append(dict(u=uu, v=vv, flat=flat,
                        uspan=float(uu.max()-uu.min()), vspan=float(vv.max()-vv.min())))
    return out

def main():
    allbands = {n: bands_of(n) for n in BAND_PAGES}
    for n, b in allbands.items():
        print(f'{n}: {len(b) if b else 0} bands', [(round(a,2), round(x,2)) for a, x, _ in (b or [])][:8])
    segs = parse_flat_segs('GothamCity', limit=None)
    print('segments:', len(segs))
    flat_wide = [s for s in segs if s['flat'] and s['uspan'] > 0.25]
    print('flat wide-u:', len(flat_wide))
    from collections import Counter
    cnt = Counter()
    for s in flat_wide:
        vmin, vmax = s['v'].min(), s['v'].max()
        hits = []
        for pn, bl in allbands.items():
            if not bl:
                continue
            for a, b, _ in bl:
                if vmin >= a - 0.012 and vmax <= b + 0.012:
                    hits.append(pn)
                    break
        cnt[tuple(sorted(hits)) or ('NONE',)] += 1
    for k, c in cnt.most_common(12):
        print(f'  {c:>4} {k}')

if __name__ == '__main__':
    main()
