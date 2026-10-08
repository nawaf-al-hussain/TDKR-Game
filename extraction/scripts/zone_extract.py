#!/usr/bin/env python3
"""Extract streamed street-level geometry from TDKR zone ZIPs (GothamCity*.zip
inside l_gothamcity.gla).

Proved layout (RE session 9):
  lod_table.bin : [u32 N][N x (u32 off, u32 sz)]      # segment DESCRIPTOR table
                  [u32 M][M x u32]                    # leaf index stream
  lod_data.bin  : [segment blocks ...][descriptors][bih]
  descriptor    : +0 triCount, +4/+16 3D bounds (2 blocks), +68 dataOff,
                  +72 =4, +76 vBytes, +80 iBytes, [+100/+168... more LOD blocks]
  segment block : [u32 hdr][vBytes vertex data][iBytes u16 strip idx (0xffff cut)]
  vertex (24B)  : [f32 a][f32 b][f32 c][u32 oct-nrm][u32 X][u32 Y]  (wall style)
  vertex (20B)  : [f32 a][f32 b][f32 c][u32 oct-nrm][u32 uv]        (ground style)
Coordinates: game Z-up; (a,b) horizontal, c = up.
"""
import struct, sys, os
import numpy as np

ZONE = '/home/z/my-project/work/zone'

def parse_island(name):
    lod = open(f'{ZONE}/{name}/lod_data.bin', 'rb').read()
    lt = open(f'{ZONE}/{name}/lod_table.bin', 'rb').read()
    u = struct.unpack(f'<{len(lt)//4}I', lt)
    n = u[0]
    pairs = [(u[1+2*k], u[2+2*k]) for k in range(n)]
    out = []
    stats = {'s20': 0, 's24': 0, 's32': 0, 'bad': 0}
    for off, sz in pairs:
        data_off, four, vb, ib = struct.unpack_from('<4I', lod, off + 68)
        if four != 4:
            stats['bad'] += 1
            continue
        vstart = data_off + 4
        istart = vstart + vb
        idx = np.frombuffer(lod[istart:istart+ib], '<u2').astype(np.int32)
        real = idx[idx != 0xffff]
        mx = int(real.max()) if len(real) else 0
        stride = None
        for s, tag in ((24, 's24'), (20, 's20'), (32, 's32')):
            if vb % s == 0 and mx < vb // s:
                # verify: no NaN/garbage first dwords across vertices
                test = np.frombuffer(lod[vstart:vstart+vb], '<f4').reshape(-1, s//4)[:, :3]
                if np.isfinite(test).all() and np.abs(test).max() < 6000:
                    stride = s
                    stats[tag] += 1
                    break
        if stride is None:
            stats['bad'] += 1
            continue
        nv = vb // stride
        v = np.frombuffer(lod[vstart:vstart+vb], '<f4').reshape(nv, stride//4)
        pos = v[:, :3].copy()
        words = np.frombuffer(lod[vstart:vstart+vb], '<u4').reshape(nv, stride//4)
        nrm = words[:, 3]
        uvw = words[:, 4] if stride >= 20 else None
        extra = words[:, 5] if stride == 24 else None
        # decode octahedral normal 2 x snorm16
        nx = (nrm & 0xffff).astype(np.int16).astype(np.float32) / 32767.0
        ny = (nrm >> 16).astype(np.int16).astype(np.float32) / 32767.0
        nz = 1.0 - np.abs(nx) - np.abs(ny)
        # octahedral decode
        nz = np.clip(nz, -1.0, 1.0)
        nn = np.column_stack([nx - np.sign(nx) * nz * 0 if False else nx, ny, nz])
        # standard octahedral: if |x|+|y| > 1 fold; we stored z = 1-|x|-|y| so
        # normal = (x, y, z) directly when not folded; folded case rare here
        out.append(dict(seg=len(out), pos=pos, idx=real.astype(np.uint32),
                        nrm=nn, uvw=uvw, extra=extra, vbytes=vb, ibytes=ib,
                        desc_off=off, data_off=data_off, stride=stride))
    print(f'{name}: {len(out)} segments, stats={stats}')
    return out


def strip_to_tris(idx):
    """u16 strip with 0xffff cuts -> triangle list."""
    tris = []
    i = 0
    n = len(idx)
    while i < n - 2:
        a, b, c = int(idx[i]), int(idx[i+1]), int(idx[i+2])
        if a == 0xffff or b == 0xffff or c == 0xffff:
            i += 1
            continue
        if a != b and b != c and a != c:
            if i % 2 == 0:
                tris.append((a, b, c))
            else:
                tris.append((a, c, b))
        i += 1
    return tris


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--island', default='GothamCity')
    ap.add_argument('--render', action='store_true')
    args = ap.parse_args()
    segs = parse_island(args.island)
    tot_v = sum(len(s['pos']) for s in segs)
    tot_t = sum(len(strip_to_tris(s['idx'])) for s in segs[:40])
    print('verts:', tot_v)
    # position coordinate ranges
    allmin = np.min([s['pos'].min(0) for s in segs], 0)
    allmax = np.max([s['pos'].max(0) for s in segs], 0)
    print('coord mins:', allmin, 'maxs:', allmax)
    # UV dword stats
    uvvals = collections = {}
    import collections
    c = collections.Counter()
    for s in segs[:200]:
        if s['uvw'] is not None:
            u16lo = (s['uvw'] & 0xffff).astype(np.float32) / 65535.0
            u16hi = (s['uvw'] >> 16).astype(np.float32) / 65535.0
            c[(float(np.median(u16lo)), float(np.median(u16hi)))] += 1
    print('median uv (lo,hi) top:', c.most_common(8))

    if args.render:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib.collections import PolyCollection
        fig, axes = plt.subplots(1, 2, figsize=(22, 11), constrained_layout=True)
        for ax, sl in zip(axes, (slice(0, 300), slice(300, 600))):
            polys = []
            zs = []
            for s in segs[sl]:
                tris = strip_to_tris(s['idx'])
                p = s['pos']
                for t in tris[:400]:
                    polys.append(p[list(t)][:, :2])
                    zs.append(p[list(t)][:, 2].mean())
            pc = PolyCollection(polys, array=np.array(zs), cmap='viridis',
                                edgecolors='none')
            ax.add_collection(pc)
            ax.autoscale(); ax.set_aspect('equal')
            ax.set_title(f'segments {sl.start}..{sl.stop} (top view, z-colored)')
        out = f'/home/z/my-project/work/zone/render_{args.island}.png'
        fig.savefig(out, dpi=90)
        print('render ->', out)

if __name__ == '__main__':
    main()
