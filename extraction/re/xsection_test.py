#!/usr/bin/env python3
"""Cross-section group containment: road pieces span sidewalk+asphalt+sidewalk
= one cross-section group in the band atlas. Detect groups via dark separator
rows, test segment v-range containment per page."""
import struct
import numpy as np
from PIL import Image
from collections import Counter

PNG = '/home/z/my-project/download/TDKR_assets/textures_png'

def page_gray(name, h=1024):
    for a in ('l_gothamcity_tex', 'commons_tex'):
        try:
            im = Image.open(f'{PNG}/{a}/{name}.png').convert('L')
            break
        except Exception:
            return None
    im = im.resize((32, h), Image.BILINEAR)
    return np.asarray(im, np.float32)

def cross_sections(name, h=1024):
    g = page_gray(name, h)
    if g is None:
        return None, None
    row = g.mean(1)
    dark = row < row.mean() * 0.62
    # separators = dark runs >= 2 rows
    seps = []
    i = 0
    while i < h:
        if dark[i]:
            j = i
            while j < h and dark[j]:
                j += 1
            if j - i >= 2:
                seps.append((i, j))
            i = j
        else:
            i += 1
    # groups between separators
    bounds = [0] + [a for a, b in seps] + [b for a, b in seps[-1:]] + [h]
    edges = sorted(set([0] + [x for a, b in seps for x in (a, b)] + [h]))
    groups = [(a / h, b / h) for a, b in zip(edges[:-1], edges[1:]) if b - a > 20]
    return groups, row

def segment_vr(path_isl='GothamCity', limit=None):
    lod = open(f'/home/z/my-project/work/zone/{path_isl}/lod_data.bin', 'rb').read()
    lt = open(f'/home/z/my-project/work/zone/{path_isl}/lod_table.bin', 'rb').read()
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
        if stride is None or stride < 20:
            continue
        nv = vb // stride
        v = np.frombuffer(lod[vstart:vstart+vb], '<f4').reshape(nv, stride//4)
        words = np.frombuffer(lod[vstart:vstart+vb], '<u4').reshape(nv, stride//4)
        p = v[:, :3]
        zr = float(np.ptp(p[:, 2]))
        if zr >= max(2.0, 0.06 * float(np.ptp(p[:, :2]))):
            continue
        w = words[:, 4]
        if np.all(w == 0xffffffff):
            continue
        uu = (w & 0xffff).astype(np.float32) / 65535.0
        vv = (w >> 16).astype(np.float32) / 65535.0
        out.append(dict(u=uu, v=vv, uspan=float(uu.max()-uu.min()),
                        vspan=float(vv.max()-vv.min())))
    return out

def main():
    PAGES = ['GothamCity_Road_v1_Island_1', 'GothamCity_Road_v2_Island_1',
             'gothamcity_roads_details', 'GothamCity_Road_Crossings_Island_1']
    groups = {}
    for p in PAGES:
        g, row = cross_sections(p)
        groups[p] = g
        print(f'{p}: {len(g) if g else 0} cross-sections',
              [(round(a, 2), round(b, 2)) for a, b in (g or [])])
    segs = segment_vr()
    wide = [s for s in segs if s['uspan'] > 0.25]
    print('wide flats:', len(wide))
    cnt = Counter()
    for s in wide:
        vmin, vmax = s['v'].min(), s['v'].max()
        hits = []
        for p, gs in groups.items():
            for a, b in gs:
                if vmin >= a - 0.008 and vmax <= b + 0.008:
                    hits.append(p)
                    break
        cnt[tuple(sorted(hits)) or ('NONE',)] += 1
    for k, c in cnt.most_common(10):
        print(f'  {c:>4} {k}')

if __name__ == '__main__':
    main()
