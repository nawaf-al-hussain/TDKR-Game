#!/usr/bin/env python3
"""s45 T1b diag: which lod vertex field produced the GLB TEXCOORD_0/1?

For sample stride-24 and stride-28 segs, least-squares fit GLB uv vs candidate
lod fields (uv@12 snorm16, packed@16 as u8 trio, colour@20), per axis, report
a, b, residual. Also try snorm8 variants of @16.
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
pairs = [(u[1 + 2 * k], u[2 + 2 * k]) for k in range(u[0])]


def s16a(v):
    v = v.astype(np.int32)
    return np.where(v >= 32768, v - 65536, v) / 32767.0


def s8a(v):
    v = v.astype(np.int32)
    return np.where(v >= 128, v - 256, v) / 127.0


def load_seg_raw(k, stride):
    off2 = pairs[k][0]
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
    if vb % stride:
        return None
    vstart = data_off + 4
    nv = vb // stride
    return np.frombuffer(ld, np.uint8, vb, vstart).reshape(nv, stride)


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
                              'uv0': read_acc(p['attributes']['TEXCOORD_0']).astype(np.float64),
                              'uv1': read_acc(p['attributes']['TEXCOORD_1']).astype(np.float64)})
            segs[int(m.group(1))] = prims
    return segs


allsegs = {}
for i in range(9):
    allsegs.update(parse_glb(f'{MODEL}/street_island1_{i:02d}.glb'))


def fit(y, x):
    """y = a*x + b per column; return a, b, max_resid"""
    out = []
    for c in range(y.shape[1]):
        X = np.column_stack([x, np.ones_like(x)])
        sol, res, *_ = np.linalg.lstsq(X, y[:, c], rcond=None)
        pred = X @ sol
        out.append((sol[0], sol[1], np.abs(pred - y[:, c]).max()))
    return out


cands24 = {}
for k in (673, 604, 151, 1381, 1496):
    prims = allsegs.get(k)
    if not prims:
        continue
    raw = load_seg_raw(k, 24)
    if raw is None:
        print(f'seg {k}: not stride 24')
        continue
    nv = raw.shape[0]
    uv12 = s16a(raw[:, 12:16].copy().view('<u2').reshape(nv, 2)) * 0.5 + 0.5
    uv12r = (raw[:, 12:16].copy().view('<u2').reshape(nv, 2).astype(np.float64)) / 65535.0
    F16 = raw[:, 16:19].astype(np.float64) / 255.0
    col20 = raw[:, 20:24].astype(np.float64) / 255.0
    guv0 = prims[0]['uv0']
    guv1 = prims[0]['uv1']
    nv2 = min(nv, guv0.shape[0])
    print(f'\n=== seg {k} (stride 24, nv {nv}, glb nv {guv0.shape[0]}) ===')
    print(' GLBuv0 vs uv@12 snorm*0.5+0.5:', [(round(a, 3), round(b, 3), round(r, 4)) for a, b, r in fit(guv0[:nv2], uv12[:nv2])])
    print(' GLBuv0 vs uv@12 raw/65535  :', [(round(a, 3), round(b, 3), round(r, 4)) for a, b, r in fit(guv0[:nv2], uv12r[:nv2])])
    print(' GLBuv1 vs uv@12 snorm*0.5+0.5:', [(round(a, 3), round(b, 3), round(r, 4)) for a, b, r in fit(guv1[:nv2], uv12[:nv2])])
    print(' GLBuv1 vs F@16/255          :', [(round(a, 3), round(b, 3), round(r, 4)) for a, b, r in fit(guv1[:nv2], F16[:nv2])])
    print(' GLBuv1 vs col@20/255        :', [(round(a, 3), round(b, 3), round(r, 4)) for a, b, r in fit(guv1[:nv2], col20[:nv2])])
    print(' GLBuv0 vs F@16/255          :', [(round(a, 3), round(b, 3), round(r, 4)) for a, b, r in fit(guv0[:nv2], F16[:nv2])])

for k in (1486, 1525):
    prims = allsegs.get(k)
    raw = load_seg_raw(k, 28)
    if raw is None or prims is None:
        print(f'seg {k}: stride28 raw={raw is None} glb={prims is not None}')
        continue
    nv = raw.shape[0]
    uv0 = s16a(raw[:, 12:16].copy().view('<u2').reshape(nv, 2)) * 0.5 + 0.5
    uv1 = s16a(raw[:, 16:20].copy().view('<u2').reshape(nv, 2)) * 0.5 + 0.5
    guv0, guv1 = prims[0]['uv0'], prims[0]['uv1']
    nv2 = min(nv, guv0.shape[0])
    print(f'\n=== seg {k} (stride 28, nv {nv}, glb nv {guv0.shape[0]}) ===')
    print(' GLBuv0 vs lod uv0:', [(round(a, 3), round(b, 3), round(r, 4)) for a, b, r in fit(guv0[:nv2], uv0[:nv2])])
    print(' GLBuv1 vs lod uv1:', [(round(a, 3), round(b, 3), round(r, 4)) for a, b, r in fit(guv1[:nv2], uv1[:nv2])])
