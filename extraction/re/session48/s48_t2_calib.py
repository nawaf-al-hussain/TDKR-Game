#!/usr/bin/env python3
"""s48 T2 calibration: does the enrichment metric have power on a KNOWN-GOOD
binding? seg 695 (roads_details; its UVs are the s46 GLB-bit-exact ones and the
s46 render matched the deployed street at corr 0.97) and seg 1525 (SPLIT alpha)
and one billboard seg. For each: real obs non-empty rate vs the distribution of
its UVs on ~60 OTHER textures (the per-segment shuffled null)."""
import struct, io, zipfile, json
import numpy as np
import importlib.util

spec = importlib.util.spec_from_file_location(
    'cr', '/tmp/my-project/work/TDKR-Game/extraction/re/session42/s42_t2_cleanroom.py')
cr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cr)

GLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla'
TEXGLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/textures/l_gothamcity_tex.gla'
BDAE = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'

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
bi = open('/tmp/my-project/work/zone/GothamCity/batch_info.bin', 'rb').read()
bstride, = struct.unpack_from('<I', bi, 0)
M = (len(bi) - 4) // bstride
recs = np.frombuffer(bi[4:], np.uint8).reshape(M, bstride)
VAVT = [1, 1, 2, 2, 4, 4, 4]

def decl_of(mid):
    r = recs[mid]
    N = int(r[33])
    ds = []
    start = 0
    for j in range(N):
        d = bytes(r[40 + j * 12: 40 + (j + 1) * 12])
        A, B, C, st, off, pad = struct.unpack('>6H', d)
        size = 3 if B == 0 else B * VAVT[C]
        end = st if off == 0 else off
        ds.append((A, start, end, size))
        start = end
    return ds

binds = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session45/s45_t1a_bindings.json'))
diff_of = {r['i']: (r['bind'].get('DiffuseMap') or {}).get('tga', '') for r in binds}

tg = open(TEXGLA, 'rb').read()
_, idxsz2, tabsz2, n2 = struct.unpack('>IIII', tg[:16])
pool2 = tg[16 + n2 * 16:idxsz2]

def tex_member(want):
    for i in range(n2):
        o, s, no, _ = struct.unpack('>IIII', tg[16 + i * 16:16 + i * 16 + 16])
        nm2 = pool2[no:pool2.index(b'\0', no)].decode('ascii', 'replace')
        if nm2.lower() == want.lower():
            return tg[o:o + s]
    return None

def decode_pvr_rgb(u8):
    th_, tw = struct.unpack_from('<II', u8, 4)
    bw, bh = (tw + 3) // 4, (th_ + 3) // 4
    rgba = cr.decode_etc1_cleanroom(
        np.frombuffer(u8, np.uint8, bw * bh * 8, 52), tw, th_)
    return rgba

def unwrap_split(u8):
    if bytes(u8[:4]) != b'PK\x03\x04':
        return {'rgb': u8}
    out = {}
    pos = 0
    while pos + 30 <= len(u8) and bytes(u8[pos:pos + 4]) == b'PK\x03\x04':
        csz = struct.unpack_from('<I', u8, pos + 18)[0]
        nlen = struct.unpack_from('<H', u8, pos + 26)[0]
        elen = struct.unpack_from('<H', u8, pos + 28)[0]
        nm = u8[pos + 30:pos + 30 + nlen].decode('latin1')
        dstart = pos + 30 + nlen + elen
        if nm.strip() != 'SPLIT':
            out[nm] = u8[dstart:dstart + csz]
        pos = dstart + csz
    return out

_cache = {}

def tex_mask(name):
    if name in _cache:
        return _cache[name]
    tu = tex_member(name)
    if tu is None:
        _cache[name] = None
        return None
    try:
        parts = unwrap_split(tu)
        rgb = decode_pvr_rgb(parts['rgb.pvr'] if 'rgb.pvr' in parts else parts['rgb'])
        al = None
        if 'alpha.pvr' in parts:
            al = decode_pvr_rgb(parts['alpha.pvr'])[:, :, 0]
        lum = rgb[:, :, :3].astype(np.float32).mean(axis=2)
        mask = lum < 16.0
        if al is not None:
            fy = max(1, mask.shape[0] // al.shape[0])
            fx = max(1, mask.shape[1] // al.shape[1])
            alup = np.repeat(np.repeat(al, fy, axis=0), fx, axis=1)
            mask = mask | (alup[:mask.shape[0], :mask.shape[1]] < 64)
        _cache[name] = (mask, mask.shape[0], mask.shape[1], 'alpha.pvr' in parts)
    except Exception as exc:
        print('tex_mask FAIL', name, repr(exc))
        _cache[name] = None
    return _cache[name]

def seg_uv(k):
    off2 = pairs[k][0]
    hdr = struct.unpack_from('<17I', ld, off2)
    mid = hdr[10]
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
    ds = decl_of(mid)
    dmap = {d[0]: d for d in ds}
    stride = ds[-1][2]
    nv = vb // stride
    d0 = dmap[1]
    raw = np.frombuffer(ld, np.uint8, vb, data_off + 4).reshape(nv, stride)
    uvr = raw[:, d0[1]:d0[1] + 4].copy().view('<u2').reshape(nv, 2).astype(np.int32)
    uv01 = (np.where(uvr >= 32768, uvr - 65536, uvr) / 32767.0 * 0.5 + 0.5).astype(np.float32)
    return mid, uv01

def rate_on(uv, name):
    e = tex_mask(name)
    if e is None:
        return None
    mask, h, w, split = e
    tx = np.clip((uv[:, 0] * w).astype(np.int64) % w, 0, w - 1)
    ty = np.clip((uv[:, 1] * h).astype(np.int64) % h, 0, h - 1)
    return float((~mask[ty, tx]).mean())

rng = np.random.default_rng(49)
# all candidate textures (for the per-segment null): sample 80 random members
all_names = []
for i in range(n2):
    o, s, no, _ = struct.unpack('>IIII', tg[16 + i * 16:16 + i * 16 + 16])
    nm2 = pool2[no:pool2.index(b'\0', no)].decode('ascii', 'replace')
    all_names.append(nm2)
cand = [t for t in rng.choice(all_names, 90, replace=False)]

CASES = [(695, 'road276 GLB-proven'), (1525, 'stride28 SPLIT'),
         (14, 'cls2017 billboard'), (100, 'cls24nc props')]
out = {}
for k, label in CASES:
    mid, uv = seg_uv(k)
    own = diff_of.get(mid, '')
    r_own = rate_on(uv, own)
    e_own = tex_mask(own)
    rr_own = None
    if e_own is not None:
        mask, h, w, split = e_own
        ru = rng.random(20000); rv = rng.random(20000)
        rr_own = float((~mask[((rv * h).astype(np.int64) % h),
                              ((ru * w).astype(np.int64) % w)]).mean())
    others = []
    for t in cand:
        if t == own:
            continue
        r = rate_on(uv, t)
        if r is not None:
            others.append(r)
    others = np.array(others)
    enr_own = r_own / rr_own if rr_own else None
    enr_others = others / rr_own if rr_own else others
    out[label] = {'k': k, 'mat': mid, 'own_tex': own, 'own_rate': r_own,
                  'own_rand_rate': rr_own, 'own_enrichment': enr_own,
                  'n_others': len(others),
                  'others_rate_mean': float(others.mean()),
                  'others_rate_std': float(others.std()),
                  'others_rate_p90': float(np.percentile(others, 90)),
                  'z_vs_others': float((r_own - others.mean()) / (others.std() + 1e-12))}
    print(label, json.dumps(out[label], default=float))
json.dump(out, open('/tmp/my-project/work/TDKR-Game/extraction/re/session48/s48_t2_calib.json', 'w'), indent=1)
