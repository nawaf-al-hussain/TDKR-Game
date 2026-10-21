#!/usr/bin/env python3
"""s46 T2: per-vertex comparison GLB vs lod on the equal-count subset — the
comparison that can fail. Nulls: row-shuffle, wrong-seg. Plus UV affine test."""
import struct, io, zipfile, json, re
import numpy as np

GLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla'
MODEL = '/tmp/my-project/work/ghpages_live_wt/models'
rng = np.random.default_rng(4646)

g = open(GLA, 'rb').read()
_, idxsz, tabsz, n = struct.unpack('>IIII', g[:16])
pool = g[16 + n * 16:idxsz]
Z = None
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

def seg_hdr(k):
    return struct.unpack_from('<17I', ld, pairs[k][0])

def load_seg(k):
    off2 = pairs[k][0]
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
    stride = 20
    if vb % stride != 0:
        stride = 28 if vb % 28 == 0 else (24 if vb % 24 == 0 else 20)
    nv = vb // stride
    vstart = data_off + 4
    raw = np.frombuffer(ld, np.uint8, vb, vstart).reshape(nv, stride)
    pos = raw[:, :12].copy().view('<f4').reshape(nv, 3).astype(np.float64)
    uv0 = raw[:, 12:16].copy().view('<i2').reshape(nv, 2).astype(np.float64) / 32767.0
    uv1 = None
    if stride == 28:
        uv1 = raw[:, 16:20].copy().view('<i2').reshape(nv, 2).astype(np.float64) / 32767.0
    return {'pos': pos, 'uv0': uv0, 'uv1': uv1, 'stride': stride, 'nv': nv}

def parse_glb(path):
    raw = open(path, 'rb').read()
    clen, = struct.unpack_from('<I', raw, 12)
    js = json.loads(raw[20:20 + clen])
    boff = 20 + clen
    blen, = struct.unpack_from('<I', raw, boff)
    bin_ = raw[boff + 8:boff + 8 + blen]
    acc = js['accessors']
    bv = js['bufferViews']

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
        if m is None or 'mesh' not in node:
            continue
        k = int(m.group(1))
        mesh = js['meshes'][node['mesh']]
        prims = []
        for p in mesh['primitives']:
            mat = js['materials'][p['material']]['name']
            prims.append({'mat': mat,
                          'pos': read_acc(p['attributes']['POSITION']).astype(np.float64),
                          'uv0': read_acc(p['attributes']['TEXCOORD_0']).astype(np.float64),
                          'uv1': (read_acc(p['attributes']['TEXCOORD_1']).astype(np.float64)
                                  if 'TEXCOORD_1' in p['attributes'] else None),
                          'idx': read_acc(p['indices']).astype(np.int64)})
        segs[k] = prims
    return segs

allsegs = {}
for i in range(9):
    allsegs.update(parse_glb(f'{MODEL}/street_island1_{i:02d}.glb'))
print('GLB segs:', len(allsegs))

# ---- census ----
eq, ne = [], []
for k, prims in allsegs.items():
    if k >= cnt:
        continue
    L = load_seg(k)
    nv_g = sum(len(p['pos']) for p in prims)
    (eq if nv_g == L['nv'] else ne).append((k, nv_g, L['nv']))
print(f'equal-count segs: {len(eq)}, differ: {len(ne)} (of {len(allsegs)} matched)')

# ---- per-vertex compare on equal-count segs ----
def to_glb_frame(p):
    # s45: lod = (glb_x, -glb_z, glb_y)  =>  inverse: glb = (lod_x, lod_z, -lod_y)
    return np.column_stack([p[:, 0], p[:, 2], -p[:, 1]])

res = {'exact': 0, 'near': 0, 'fail': 0, 'maxd': [], 'null_shuffle_hit': 0,
       'null_wrongseg_hit': 0, 'n': 0, 'uv_fit': 0, 'uv_n': 0, 'uv_null_fit': 0,
       'uv1_fit': 0, 'uv1_n': 0}
detail = []
for k, nv_g, _ in eq[:4000]:
    prims = allsegs[k]
    if len(prims) != 1:
        continue  # single-prim only for clean order comparison
    gp = prims[0]['pos']
    L = load_seg(k)
    lp = to_glb_frame(L['pos'])
    d = np.abs(gp - lp).max()
    res['n'] += 1
    res['maxd'].append(float(d))
    if d < 1e-4:
        res['exact'] += 1
    elif d < 0.5:
        res['near'] += 1
    else:
        res['fail'] += 1
    detail.append({'k': k, 'maxd': float(d), 'nv': int(nv_g), 'stride': L['stride']})
    # row-shuffle null (same seg, permuted lod rows)
    if res['n'] <= 300:
        perm = rng.permutation(L['nv'])
        d_null = np.abs(gp - lp[perm]).max()
        if d_null < 0.5:
            res['null_shuffle_hit'] += 1
        # wrong-seg null
        k2 = k + 1 if k + 1 < cnt else k - 1
        L2 = load_seg(k2)
        if L2['nv'] == L['nv']:
            d_wrong = np.abs(gp - to_glb_frame(L2['pos'])).max()
            if d_wrong < 0.5:
                res['null_wrongseg_hit'] += 1
    # UV affine fit (uv0 vs lod uv0) on matched segs
    if res['n'] <= 1500:
        gu = prims[0]['uv0']
        lu = L['uv0']
        A = np.column_stack([lu, np.ones(len(lu))])
        ok_axes = True
        r2s = []
        for ax in range(2):
            sol, *_ = np.linalg.lstsq(A, gu[:, ax], rcond=None)
            r = gu[:, ax] - A @ sol
            r2s.append(float(np.abs(r).max()))
        res['uv_n'] += 1
        if max(r2s) < 0.01:
            res['uv_fit'] += 1
        if res['uv_n'] <= 200:
            perm = rng.permutation(len(lu))
            r_null = []
            for ax in range(2):
                sol, *_ = np.linalg.lstsq(A, gu[perm][:, ax], rcond=None)
                r_null.append(float(np.abs(gu[perm][:, ax] - A @ sol[perm] if False else gu[:, ax] - A @ sol).max()))
            if max(r_null) < 0.01:
                res['uv_null_fit'] += 1
        if L['stride'] == 28 and prims[0]['uv1'] is not None and L['uv1'] is not None:
            gu1 = prims[0]['uv1']
            lu1 = L['uv1']
            A1 = np.column_stack([lu1, np.ones(len(lu1))])
            r1s = []
            for ax in range(2):
                sol, *_ = np.linalg.lstsq(A1, gu1[:, ax], rcond=None)
                r1s.append(float(np.abs(gu1[:, ax] - A1 @ sol).max()))
            res['uv1_n'] += 1
            if max(r1s) < 0.01:
                res['uv1_fit'] += 1

mx = res.pop('maxd')
print('per-vertex (single-prim, equal-count):', json.dumps(res, default=float))
print('maxd quantiles (m):', {q: round(float(np.quantile(mx, q)), 6) for q in (0.5, 0.9, 0.99, 1.0)} if mx else {})
print('nulls: row-shuffle hits', res['null_shuffle_hit'], '/', min(res['n'], 300),
      '; wrong-seg hits', res['null_wrongseg_hit'])
json.dump({'res': {k: v for k, v in res.items()}, 'detail_head': detail[:60]},
          open('/home/z/my-project/scripts/s46_t2_vertexmatch.json', 'w'), indent=1)
