#!/usr/bin/env python3
"""s49 T4b: classify the 197 (island1) + 156 (island2) failing-smoothness segments.
Decode-issue test: does the DECODED vertex normal match its triangle's geometric
normal (per-triangle vertex-normal vs face-normal agreement)? Self-consistent
normals = legit hard-edge content; a decode defect would break the agreement.
Census: material/effect/stride of the failing set vs the passing population."""
import json, struct, io, zipfile, collections
import numpy as np

S48 = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session48/s48_t4_decode.json'))
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session49/s49_t4_classify.json'
ZONE_DIR = {'GothamCity.zip': '/tmp/my-project/work/zone/GothamCity',
            'GothamCity_Island2.zip': '/tmp/my-project/work/zone/GothamCity_Island2'}
GLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla'

g = open(GLA, 'rb').read()
_, idxsz, tabsz, n = struct.unpack('>IIII', g[:16])
pool = g[16+n*16: idxsz]
zones = {}
for i in range(n):
    o, s, no, _ = struct.unpack('>IIII', g[16+i*16:16+i*16+16])
    nm = pool[no:pool.index(b'\0', no)].decode('ascii', 'replace')
    if nm in ZONE_DIR:
        Z = zipfile.ZipFile(io.BytesIO(g[o:o+s]))
        zones[nm] = (Z.read('lod_data.bin'), Z.read('lod_table.bin'))
bi_cache = {}
def batch_info(zone):
    if zone not in bi_cache:
        bi_cache[zone] = open(ZONE_DIR[zone]+'/batch_info.bin', 'rb').read()
    return bi_cache[zone]
VAVT = [1, 1, 2, 2, 4, 4, 4]
_decl = {}
def decl_of(bi, mid):
    if (id(bi), mid) in _decl:
        return _decl[(id(bi), mid)]
    bstride, = struct.unpack_from('<I', bi, 0)
    recs = np.frombuffer(bi[4:], np.uint8).reshape(-1, bstride)
    r = recs[mid]; N = int(r[33]); ds = []; start = 0
    for j in range(N):
        dd = bytes(r[40+j*12:40+(j+1)*12])
        A, B, C, st, off, pad = struct.unpack('>6H', dd)
        size = 3 if B == 0 else B*VAVT[C]
        end = st if off == 0 else off
        ds.append((A, start, end, size)); start = end
    _decl[(id(bi), mid)] = ds
    return ds
def s16a(v):
    v = v.astype(np.int32)
    return np.where(v >= 32768, v-65536, v)/32767.0

def seg_data(zone, k, mat):
    ld, lt = zones[zone]
    u = struct.unpack('<%dI' % (len(lt)//4), lt)
    pairs = [(u[1+2*kk], u[2+2*kk]) for kk in range(u[0])]
    off2 = pairs[k][0]
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2+68)
    bi = batch_info(zone)
    ds = decl_of(bi, mat)
    stride = ds[-1][2]
    nv = vb//stride
    raw = np.frombuffer(ld, np.uint8, vb, data_off+4)
    dmap = {d[0]: d for d in ds}
    pos = raw.reshape(nv, stride)[:, 0:12].copy().view('<f4').reshape(nv, 3).astype(np.float64)
    dn = dmap.get(0)   # attr 0 = normal (packed signed byte if size 3, else f3?)
    nrm = None
    if dn is not None:
        blob = raw.reshape(nv, stride)[:, dn[1]:dn[1]+dn[3]].copy()
        if dn[3] == 3:
            nrm = blob.reshape(nv, 3).astype(np.int8)/127.0
        elif dn[3] == 12:
            nrm = blob.view('<f4').reshape(nv, 3).astype(np.float64)
    tris = np.frombuffer(ld, '<u2', ib//2, data_off+4+vb).astype(np.int64).reshape(-1, 3)
    return pos, nrm, tris

# material fx table (island1 only; island2 uses its own compiled table — use stride/mats)
def fx_table(zone):
    try:
        P = ZONE_DIR[zone] + '/GothamCity_materials.bdae'
        if zone == 'GothamCity_Island2.zip':
            P = '/tmp/my-project/work/zone/GothamCity_Island2/GothamCity_Island2_materials.bdae'
        import os
        if not __import__('os').path.exists(P):
            return {}
        LE = zipfile.ZipFile(P).read('little_endian_not_quantized.bdae')
        w32 = np.frombuffer(LE, '<u4', len(LE)//4); nb = len(LE)
        def cs(p):
            if not (0 < p < nb): return None
            e = LE.find(b'\0', p)
            return LE[p:e].decode('ascii', 'replace') if 0 < e-p < 80 else None
        fx = {}
        for i in range(307):
            a = 0x5fea0 + i*36
            ws = [int(w32[(a+kk*4)//4]) for kk in range(9)]
            fx[i] = (cs(ws[3]) or 'NONE').split('-fx')[0].lstrip('#')
        return fx
    except Exception as e:
        print('fx table skip:', e)
        return {}

out = {}
for zone in ('GothamCity.zip', 'GothamCity_Island2.zip'):
    zd = S48['zones'][zone]
    fail = set(zd['new_fail'])
    ld, lt = zones[zone]
    u = struct.unpack('<%dI' % (len(lt)//4), lt)
    pairs = [(u[1+2*kk], u[2+2*kk]) for kk in range(u[0])]
    bi = batch_info(zone)
    bstride, = struct.unpack_from('<I', bi, 0)
    recs = np.frombuffer(bi[4:], np.uint8).reshape(-1, bstride)
    seg_mat = []
    for k in range(len(pairs)):
        m, = struct.unpack_from('<I', ld, pairs[k][0]+40)
        seg_mat.append(int(m))
    fx = fx_table(zone)
    mat_stride = {}
    for m in set(seg_mat):
        ds = decl_of(bi, m)
        mat_stride[m] = ds[-1][2]
    agree_f = []; agree_p = []
    fcen = collections.Counter(); pcen = collections.Counter()
    sc_f = collections.Counter(); sc_p = collections.Counter()
    eff_f = collections.Counter(); eff_p = collections.Counter()
    for k in range(len(pairs)):
        m = seg_mat[k]
        tag = 'F' if k in fail else 'P'
        (fcen if tag == 'F' else pcen)[m] += 1
        (sc_f if tag == 'F' else sc_p)[mat_stride[m]] += 1
        (eff_f if tag == 'F' else eff_p)[fx.get(m, '?')] += 1
        pos, nrm, tris = seg_data(zone, k, m)
        if nrm is None or len(tris) == 0:
            continue
        tri = tris[tris.max(axis=1) < len(pos)]
        if len(tri) == 0:
            continue
        e1 = pos[tri[:, 1]]-pos[tri[:, 0]]
        e2 = pos[tri[:, 2]]-pos[tri[:, 0]]
        fn = np.cross(e1, e2)
        ln = np.linalg.norm(fn, axis=1)
        ok = ln > 1e-9
        fn = fn[ok]/ln[ok][:, None]
        vn = nrm[tri[ok]]
        vn = vn/np.maximum(np.linalg.norm(vn, axis=1, keepdims=True), 1e-9)
        dot = (vn*fn[:, None, :]).sum(axis=2)   # per-triangle verts x face normal
        flat_like = float(np.mean(dot > 0.85))  # verts whose normal ~ face normal
        (agree_f if tag == 'F' else agree_p).append((k, flat_like))
    af = np.array([a for _, a in agree_f]); ap = np.array([a for _, a in agree_p])
    print(zone, 'failing segs with normal data:', len(af), 'passing:', len(ap))
    print('  face-normal agreement (verts with n.v>0.85): failing mean %.3f median %.3f | '
          'passing mean %.3f median %.3f' %
          (af.mean(), np.median(af), ap.mean(), np.median(ap)))
    top_f = [(m, c) for m, c in fcen.most_common(8)]
    print('  failing top materials:', top_f)
    print('  failing strides:', dict(sc_f), 'effects:', dict(eff_f.most_common(5)))
    print('  passing strides:', dict(sc_p.most_common(4)), 'effects:', dict(eff_p.most_common(5)))
    out[zone] = {
        'n_fail': int(len(af)), 'face_agree_fail_mean': float(af.mean()),
        'face_agree_fail_median': float(np.median(af)),
        'n_pass': int(len(ap)), 'face_agree_pass_mean': float(ap.mean()),
        'face_agree_pass_median': float(np.median(ap)),
        'fail_mat_top': [[m, c] for m, c in fcen.most_common(10)],
        'fail_stride': {str(k): v for k, v in sc_f.items()},
        'fail_effect': dict(eff_f),
        'pass_stride': {str(k): v for k, v in sc_p.items()},
        'pass_effect': {k: v for k, v in eff_p.most_common(10)},
        'per_seg_flatlike': {str(k): round(a, 3) for k, a in agree_f},
    }
json.dump(out, open(OUT, 'w'), indent=1)
print('saved', OUT)
