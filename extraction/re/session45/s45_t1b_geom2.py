#!/usr/bin/env python3
"""s45 T1b step 2: geometric correspondence, proper stride inference + frame fit.

For sample segs present in the street GLBs: decode lod vertices with the
s42-validated stride inference ({20,24,28} + finite + idx<vcount), then fit the
GLB frame to the lod frame over the 6 axis permutations, report residual.
"""
import struct, io, zipfile, json, re
import numpy as np

GLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla'
MODEL = '/tmp/my-project/work/ghpages_live_wt/models'

g = open(GLA, 'rb').read()
_, idxsz, tabsz, n = struct.unpack('>IIII', g[:16])
pool = g[16 + n * 16:idxsz]
for i in range(n):
    o, s, no, _ = struct.unpack('>IIII', g[16 + i * 16:16 + i * 16 + 16])
    nm = pool[no:pool.index(b'\0', no)].decode('ascii', 'replace')
    if nm == 'GothamCity.zip':
        Z = zipfile.ZipFile(io.BytesIO(g[o:o + s]))
        ld = Z.read('lod_data.bin')
        lt = Z.read('lod_table.bin')
        break
u = struct.unpack(f'<{len(lt)//4}I', lt)
cnt = u[0]
pairs = [(u[1 + 2 * k], u[2 + 2 * k]) for k in range(cnt)]


def load_seg(k):
    off2 = pairs[k][0]
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
    hdr = struct.unpack_from('<17I', ld, off2)
    vstart = data_off + 4
    idx = np.frombuffer(ld, '<u2', ib // 2, vstart + vb).astype(np.int64)
    best = None
    for stride in (20, 24, 28):
        if vb % stride:
            continue
        nv = vb // stride
        if idx.size and idx.max() >= nv:
            continue
        raw = np.frombuffer(ld, np.uint8, vb, vstart).reshape(nv, stride)
        pos = raw[:, :12].copy().view('<f4').reshape(nv, 3).astype(np.float64)
        if not np.isfinite(pos).all():
            continue
        span = pos.max(0) - pos.min(0)
        if best is None or span.max() < best[1].max():
            best = (pos, span, stride)
    return best


def parse_glb(path):
    raw = open(path, 'rb').read()
    clen, = struct.unpack_from('<I', raw, 12)
    js = json.loads(raw[20:20 + clen])
    boff = 20 + clen
    blen, = struct.unpack_from('<I', raw, boff)
    bin_ = raw[boff + 8:boff + 8 + blen]
    acc, bv = js['accessors'], js['bufferViews']

    def read_acc(ai):
        a = acc[ai]
        v = bv[a['bufferView']]
        off = v.get('byteOffset', 0) + a.get('byteOffset', 0)
        ct = {'VEC3': 3, 'VEC2': 2, 'SCALAR': 1}[a['type']]
        dt = {5126: '<f4', 5123: '<u2', 5125: '<u4', 5121: '<u1'}[a['componentType']]
        arr = np.frombuffer(bin_, dt, a['count'] * ct, off)
        return arr.reshape(a['count'], ct) if ct > 1 else arr

    segs = {}
    for node in js['nodes']:
        m = re.fullmatch(r'seg_(\d+)', node.get('name', ''))
        if m and 'mesh' in node:
            prims = []
            for p in js['meshes'][node['mesh']]['primitives']:
                prims.append({'mat': js['materials'][p['material']]['name'],
                              'pos': read_acc(p['attributes']['POSITION']).astype(np.float64),
                              'uv': read_acc(p['attributes']['TEXCOORD_0']).astype(np.float64),
                              'idx': read_acc(p['indices']).astype(np.int64)})
            segs[int(m.group(1))] = prims
    return segs


allsegs = {}
for i in range(9):
    allsegs.update(parse_glb(f'{MODEL}/street_island1_{i:02d}.glb'))
print('GLB segs:', len(allsegs))

import itertools
print('\nframe fit on 10 sample segs (best axis permutation + translation):')
for k in list(sorted(allsegs))[::max(1, len(allsegs) // 10)][:10]:
    gp = np.vstack([p['pos'] for p in allsegs[k]])
    r = load_seg(k)
    if r is None:
        print(f'  seg {k}: lod decode failed')
        continue
    lp, span, stride = r
    g_mn, g_mx = gp.min(0), gp.max(0)
    l_mn, l_mx = lp.min(0), lp.max(0)
    best = None
    for perm in itertools.permutations(range(3)):
        gm = g_mn[list(perm)]
        gx = g_mx[list(perm)]
        # allow sign flip on the permuted axes (try all 8 sign combos)
        for signs in itertools.product((1, -1), repeat=3):
            mn2 = gm * np.array(signs)
            mx2 = gx * np.array(signs)
            lo2 = np.minimum(mn2, mx2)
            hi2 = np.maximum(mn2, mx2)
            res = max(np.abs(lo2 - l_mn).max(), np.abs(hi2 - l_mx).max())
            if best is None or res < best[0]:
                best = (res, perm, signs)
    res, perm, signs = best
    print(f'  seg {k}: stride {stride} nv {len(lp)} best-perm {perm} signs {signs} residual {res:.4f}')
