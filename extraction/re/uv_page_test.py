#!/usr/bin/env python3
"""Render street segments' UV outlines over candidate pages to identify the
correct page-space binding (roads hypothesis test)."""
import struct
import numpy as np
from PIL import Image, ImageDraw

ZONE = '/home/z/my-project/work/zone'
PNG = '/home/z/my-project/download/TDKR_assets/textures_png'

def find_png(name):
    for a in ('l_gothamcity_tex', 'commons_tex'):
        p = f'{PNG}/{a}/{name}.png'
        try:
            return Image.open(p).convert('RGB')
        except Exception:
            pass
    return None

def parse_island(name, limit=None):
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
        istart = vstart + vb
        idx = np.frombuffer(lod[istart:istart+ib], '<u2').astype(np.int32)
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
        out.append(dict(pos=v[:, :3].copy(), uvw=words[:, 4] if stride >= 20 else None,
                        idx=real.astype(np.uint32), stride=stride))
    return out

def strip_to_tris(idx):
    tris = []
    i, n = 0, len(idx)
    while i < n - 2:
        a, b, c = int(idx[i]), int(idx[i+1]), int(idx[i+2])
        if 0xffff in (a, b, c):
            i += 1
            continue
        if a != b and b != c and a != c:
            tris.append((a, b, c) if i % 2 == 0 else (a, c, b))
        i += 1
    return tris

def uv_of(seg):
    w = seg['uvw']
    return ((w & 0xffff).astype(np.float32) / 65535.0,
            (w >> 16).astype(np.float32) / 65535.0)

def main():
    segs = parse_island('GothamCity', limit=600)
    # road-like: flat, large uv span
    roads = []
    for s in segs:
        if s['uvw'] is None or np.all(s['uvw'] == 0xffffffff):
            continue
        u, v = uv_of(s)
        p = s['pos']
        zr = float(np.ptp(p[:, 2]))
        flat = zr < max(2.0, 0.06 * float(np.ptp(p[:, :2])))
        uspan, vspan = float(u.max() - u.min()), float(v.max() - v.min())
        if flat and uspan > 0.25:
            roads.append((s, u, v, uspan, vspan))
    print(f'flat wide-uv segments: {len(roads)} of {len(segs)}')
    roads.sort(key=lambda r: -r[3])
    picks = roads[:40]

    for page_name in ('GC_LongDist_Island1_Roads', 'GothamCity_Road_v1_Island_1',
                      'BakeGroup_Island1_Roads0', 'GC_LongDist_Island1_FP1'):
        page = find_png(page_name)
        if page is None:
            print('missing page', page_name)
            continue
        W, H = page.size
        im = page.copy()
        dr = ImageDraw.Draw(im)
        for s, u, v, us, vs in picks:
            tris = strip_to_tris(s['idx'])
            for t in tris[:24]:
                pts = [(float(u[i]) * W, (1.0 - float(v[i])) * H) for i in t]
                dr.polygon(pts, outline=(255, 40, 40))
        out = f'/home/z/my-project/work/uvfit_{page_name}.png'
        im.save(out)
        print('saved', out, f'({W}x{H})')

if __name__ == '__main__':
    main()
