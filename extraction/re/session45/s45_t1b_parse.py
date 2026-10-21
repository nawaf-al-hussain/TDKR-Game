#!/usr/bin/env python3
"""s45 T1b step 1: parse street GLBs, verify seg correspondence, binding agreement census.

- GLB nodes named seg_NNN <-> lod_data segment N (geometric check via AABB)
- GLB material '<dif>|<lm>|<mode>' vs s45 validated engine bindings (DiffuseMap/LightMap
  tga basenames + LightMapDC -> 2x)
"""
import struct, io, zipfile, json, re
import numpy as np

GLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla'
MODEL = '/tmp/my-project/work/ghpages_live_wt/models'

# --- lod segments
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


def seg_hdr(k):
    off2 = pairs[k][0]
    return struct.unpack_from('<17I', ld, off2)


def seg_aabb(k):
    h = seg_hdr(k)
    f = struct.unpack('<17f', struct.pack('<17I', *h))
    mn, mx = f[0:3], f[3:6]
    return mn, mx

# --- GLB parser
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
        t = a['componentType']
        dt = {5126: '<f4', 5123: '<u2', 5125: '<u4', 5121: '<u1'}[t]
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
            pos = read_acc(p['attributes']['POSITION'])
            uv0 = read_acc(p['attributes']['TEXCOORD_0'])
            idx = read_acc(p['indices']).astype(np.int64)
            prims.append({'mat': mat, 'pos': pos, 'uv': uv0, 'idx': idx})
        segs[k] = prims
    return segs

allsegs = {}
for i in range(9):
    P = f'{MODEL}/street_island1_{i:02d}.glb'
    sg = parse_glb(P)
    allsegs.update(sg)
    print(f'street_island1_{i:02d}: {len(sg)} segs')
print('total street segs:', len(allsegs), 'range', min(allsegs), '..', max(allsegs))

# --- geometric correspondence check on 8 random segs
def load_seg_pos(k, stride_hint=None):
    off2 = pairs[k][0]
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
    hdr = struct.unpack_from('<17I', ld, off2)
    stride = stride_hint or 20
    if vb % stride != 0:
        stride = 28 if vb % 28 == 0 else (24 if vb % 24 == 0 else 20)
    vstart = data_off + 4
    nv = vb // stride
    raw = np.frombuffer(ld, np.uint8, vb, vstart).reshape(nv, stride)
    return raw[:, :12].copy().view('<f4').reshape(nv, 3).astype(np.float64)


print('\nAABB correspondence (GLB POSITION bounds vs lod vertex bounds):')
ok = 0
for k in sorted(allsegs)[::max(1, len(allsegs) // 8)][:8]:
    pos = np.vstack([p['pos'] for p in allsegs[k]])
    g_mn, g_mx = pos.min(0), pos.max(0)
    lpos = load_seg_pos(k)
    l_mn, l_mx = lpos.min(0), lpos.max(0)
    d_mn = np.abs(np.array(g_mn) - np.array(l_mn)).max()
    d_mx = np.abs(np.array(g_mx) - np.array(l_mx)).max()
    good = d_mn < 0.5 and d_mx < 0.5
    ok += good
    print(f'  seg {k}: dmin={d_mn:.3f} dmax={d_mx:.3f} {"OK" if good else "MISMATCH"}')
print(f'geometric match {ok}/8')

# --- binding agreement census
bind = json.load(open('/home/z/my-project/scripts/s45_t1a_bindings.json'))


def basename(t):
    return t[:-4] if t and t.endswith('.tga') else t


agree_d = agree_l = agree_m = tot = 0
mismatch = []
for k, prims in allsegs.items():
    mat = seg_hdr(k)[10]
    b = bind[mat] if mat < len(bind) else None
    if b is None:
        continue
    dif = b['bind'].get('DiffuseMap', {}).get('tga')
    lm = b['bind'].get('LightMap', {}).get('tga')
    isLM = (b['effect'] or '').startswith('LightMapDC')
    for p in prims:
        pipe = p['mat'].split('|')
        g_dif = pipe[0] if pipe[0] != '__dark' else None
        g_lm = pipe[1] if len(pipe) >= 3 else None
        g_mode = pipe[2] if len(pipe) >= 3 else (pipe[1] if len(pipe) >= 2 else 'd')
        tot += 1
        # deployed stores diffuse possibly without prefix? compare as-is
        d_ok = (dif and g_dif and basename(dif) == g_dif) or (dif is None and g_dif is None)
        l_ok = (lm and g_lm and basename(lm) == g_lm) or (lm is None and g_lm is None)
        m_ok = (('2x' if isLM else 'd') == g_mode)
        agree_d += d_ok; agree_l += l_ok; agree_m += m_ok
        if not (d_ok and l_ok):
            mismatch.append((k, mat, dif, g_dif, lm, g_lm))
print(f'\nbinding agreement over {tot} primitives: diffuse {agree_d} ({100*agree_d/tot:.1f}%) '
      f'lightmap {agree_l} ({100*agree_l/tot:.1f}%) mode {agree_m} ({100*agree_m/tot:.1f}%)')
for r in mismatch[:10]:
    print('  mismatch seg', r[0], 'mat', r[1], 'mine', r[2], '/', r[4], ' glb', r[3], '/', r[5])
