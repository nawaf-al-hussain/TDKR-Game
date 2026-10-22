#!/usr/bin/env python3
"""s48 T2: independent UV-binding correctness check via the non-empty-texel
enrichment metric over ALL 1,526 GothamCity segments.

metric(per segment) = observed non-empty rate of the segment's vertex TC0 samples
    on the bound diffuse texture  /  the uniform-random-UV non-empty rate on the
    SAME texture.  empty mask = alpha<64 (SPLIT alpha.pvr) or near-black
    (mean rgb < 16).  Family aggregates are vertex-weighted; the null permutes
    the material->diffuse binding across materials (label shuffle, B=64), and
    per-family z = (real - null_mean) / null_std, plus log2 ratio.

Two independent readings: (a) enrichment > 1 with z >> 3 against the shuffled
binding null = the engine UVs land on non-empty texels far more than chance;
(b) families whose textures are fully opaque/full-bleed are SILENT by
construction (empty rate ~ 0 everywhere -> enrichment ~ 1 for any binding).
"""
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
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session48/s48_t2_enrich.json'
NPERM = 64
NRND = 20000

# ---------- geometry ----------
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

# ---------- bindings ----------
binds = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session45/s45_t1a_bindings.json'))
diff_of = {}
for r in binds:
    tga = (r['bind'].get('DiffuseMap') or {}).get('tga', '')
    diff_of[r['i']] = tga

# ---------- textures: empty mask per diffuse tga ----------
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
    need = bw * bh * 8
    rgba = cr.decode_etc1_cleanroom(np.frombuffer(u8, np.uint8, need, 52), tw, th_)
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

_mask_cache = {}
_rand_rate = {}

def tex_mask(name):
    """-> (mask_empty (h,w) bool, h, w, split) or None if member missing/bad."""
    if name in _mask_cache:
        return _mask_cache[name]
    tu = tex_member(name)
    if tu is None:
        _mask_cache[name] = None
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
        h, w = mask.shape
        _mask_cache[name] = (mask, h, w, 'alpha.pvr' in parts)
    except Exception:
        _mask_cache[name] = None
    return _mask_cache[name]

def rand_rate(name, rng):
    if name in _rand_rate:
        return _rand_rate[name]
    e = tex_mask(name)
    if e is None:
        r = None
    else:
        mask, h, w, split = e
        ru = rng.random(NRND); rv = rng.random(NRND)
        tx = (ru * w).astype(np.int64) % w
        ty = (rv * h).astype(np.int64) % h
        r = float((~mask[ty, tx]).mean())
    _rand_rate[name] = r
    return r

# ---------- per-segment vertex UVs ----------
segs = []
for k, (off2, cnt) in enumerate(pairs):
    hdr = struct.unpack_from('<17I', ld, off2)
    mid = hdr[10]
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
    dmap = {d[0]: d for d in decl_of(mid)}
    if 1 not in dmap or vb == 0 or ib < 6:
        continue
    stride = dmap[1][2] if False else decl_of(mid)[-1][2]
    nv = vb // stride
    if nv <= 0 or vb % stride != 0:
        continue
    d0 = dmap[1]
    raw = np.frombuffer(ld, np.uint8, vb, data_off + 4).reshape(nv, stride)
    uvr = raw[:, d0[1]:d0[1] + 4].copy().view('<u2').reshape(nv, 2).astype(np.int32)
    uv01 = np.where(uvr >= 32768, uvr - 65536, uvr) / 32767.0 * 0.5 + 0.5
    segs.append({'k': k, 'mat': mid, 'nv': nv, 'uv': uv01.astype(np.float32)})
print('segments used:', len(segs), 'of', len(pairs))

used_tex = sorted({diff_of.get(sg['mat'], '') for sg in segs} - {''})
print('distinct diffuse textures:', len(used_tex))
rng = np.random.default_rng(48)
rates = {}
for t in used_tex:
    rates[t] = rand_rate(t, rng)
bad = [t for t in used_tex if rates[t] is None]
print('textures missing/bad:', bad)

def seg_rate(sg, texname):
    e = tex_mask(texname)
    if e is None:
        return None
    mask, h, w, split = e
    uv = sg['uv']
    tx = np.clip((uv[:, 0] * w).astype(np.int64) % w, 0, w - 1)
    ty = np.clip((uv[:, 1] * h).astype(np.int64) % h, 0, h - 1)
    return float((~mask[ty, tx]).mean())

# real pass (grouped by texture; masks built once, cache holds all)
real_rate = np.full(len(segs), np.nan)
mats_arr = np.array([sg['mat'] for sg in segs])
diff_arr = np.array([diff_of.get(midx, '') for midx in mats_arr])
for t in used_tex:
    idxs = np.where(diff_arr == t)[0]
    if len(idxs) == 0 or rates[t] in (None, 0.0):
        continue
    e = tex_mask(t)
    mask, h, w, split = e
    uvs = np.concatenate([segs[i]['uv'] for i in idxs])
    tx = np.clip((uvs[:, 0] * w).astype(np.int64) % w, 0, w - 1)
    ty = np.clip((uvs[:, 1] * h).astype(np.int64) % h, 0, h - 1)
    ok = (~mask[ty, tx]).astype(np.float32)
    pos = 0
    for i in idxs:
        nvi = segs[i]['nv']
        real_rate[i] = ok[pos:pos + nvi].mean()
        pos += nvi

# ---------- families ----------
def family_of(t):
    tl = t.lower()
    if 'billboard' in tl:
        return 'billboard'
    if 'rooftop' in tl:
        return 'rooftop'
    if 'road' in tl:
        return 'road'
    if any(s in tl for s in ('_bd_', 'residential', 'footprint', 'commercial',
                             'facade', 'wall', 'building', 'cinema', 'bank_',
                             'church', 'hospital', 'hotel')):
        return 'facade'
    if 'props' in tl:
        return 'props'
    return 'other'

fam_of_tex = {t: family_of(t) for t in used_tex}
fams = sorted({fam_of_tex[t] for t in used_tex})

def family_stats(per_seg_rate, weight=None):
    out = {}
    for f in fams:
        idxs = [i for i, sg in enumerate(segs)
                if fam_of_tex.get(diff_arr[i]) == f and not np.isnan(per_seg_rate[i])
                and rates.get(diff_arr[i]) not in (None, 0.0)]
        if not idxs:
            out[f] = None
            continue
        r = np.array([per_seg_rate[i] for i in idxs])
        rr = np.array([rates[diff_arr[i]] for i in idxs])
        w = np.array([segs[i]['nv'] for i in idxs], float)
        enr = np.where(rr > 0, r / np.maximum(rr, 1e-9), np.nan)
        out[f] = {
            'segs': len(idxs),
            'verts': int(w.sum()),
            'rate_vertw': float((r * w).sum() / w.sum()),
            'enrichment_vertw': float((enr * w).sum() / w.sum()),
            'enrichment_median': float(np.nanmedian(enr)),
            'tex_rand_rate_mean': float(rr.mean()),
        }
    return out

real_fam = family_stats(real_rate)
print('REAL:', json.dumps(real_fam, indent=1))

# ---------- shuffled-binding null ----------
tex_of_mat = {midx: diff_of.get(midx, '') for midx in np.unique(mats_arr)}
perm_mats = np.unique(mats_arr)
null_fam = {f: [] for f in fams}
for p in range(NPERM):
    perm = rng.permutation(len(perm_mats))
    mapping = {perm_mats[i]: diff_of.get(perm_mats[perm[i]], '') for i in range(len(perm_mats))}
    nr = np.full(len(segs), np.nan)
    by_tex = {}
    for i, sg in enumerate(segs):
        by_tex.setdefault(mapping[sg['mat']], []).append(i)
    for t, idxs in by_tex.items():
        if rates.get(t) in (None, 0.0) or tex_mask(t) is None:
            continue
        mask, h, w, split = tex_mask(t)
        uvs = np.concatenate([segs[i]['uv'] for i in idxs])
        tx = np.clip((uvs[:, 0] * w).astype(np.int64) % w, 0, w - 1)
        ty = np.clip((uvs[:, 1] * h).astype(np.int64) % h, 0, h - 1)
        ok = (~mask[ty, tx]).astype(np.float32)
        pos = 0
        for i in idxs:
            nvi = segs[i]['nv']
            nr[i] = ok[pos:pos + nvi].mean()
            pos += nvi
    st = family_stats(nr)
    for f in fams:
        if st.get(f):
            null_fam[f].append(st[f]['enrichment_vertw'])
    print('perm', p, 'done', flush=True)

out = {'n_segs': len(segs), 'n_tex': len(used_tex), 'nperm': NPERM,
       'families': {}, 'tex_census': []}
for f in fams:
    e = real_fam.get(f)
    nl = np.array(null_fam[f]) if null_fam[f] else np.array([])
    entry = dict(e or {})
    if e and len(nl) >= 8:
        mu, sd = float(nl.mean()), float(nl.std()) + 1e-12
        entry['null_mean'] = mu
        entry['null_std'] = float(nl.std())
        entry['z'] = float((e['enrichment_vertw'] - mu) / sd)
        entry['log2_ratio'] = float(np.log2(max(e['enrichment_vertw'], 1e-9) / max(mu, 1e-9)))
        entry['decisive'] = bool(entry['z'] > 3.0 and entry['log2_ratio'] > 0.3)
        entry['silent'] = bool(entry['rate_vertw'] > 0.995)
    elif e:
        entry['silent'] = bool(e['rate_vertw'] > 0.995)
        entry['decisive'] = False
    out['families'][f] = entry
for t in used_tex:
    e = tex_mask(t)
    out['tex_census'].append({'tex': t, 'family': fam_of_tex[t],
                              'rand_rate': rates[t],
                              'size': [e[2], e[1]] if e else None,
                              'split': bool(e[3]) if e else None})
json.dump(out, open(OUT, 'w'), indent=1)
print('saved', OUT)
