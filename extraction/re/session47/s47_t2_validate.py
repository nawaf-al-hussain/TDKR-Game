#!/usr/bin/env python3
"""s47 T2 step B: corrected descriptor semantics (off = END offset; size =
B * E_VAVT_size[C]; B==0 -> 3-byte packed normal) applied to all 307
materials; tiling check; 1,526-segment decode vs AABB/UV/normal tests with a
shuffled-descriptor null."""
import struct, io, zipfile, json
import numpy as np
from collections import Counter

bi = open('/tmp/my-project/work/zone/GothamCity/batch_info.bin', 'rb').read()
bstride, = struct.unpack_from('<I', bi, 0)
M = (len(bi) - 4) // bstride
recs = np.frombuffer(bi[4:], np.uint8).reshape(M, bstride)

VAVT = [1, 1, 2, 2, 4, 4, 4]  # Byte UByte Short UShort Int UInt Float @0xb8613c
ATTR = {0: 'Position', 1: 'TexCoord0', 2: 'TexCoord1', 3: 'TexCoord2',
        16: 'Normal', 17: 'Color0', 18: 'Color1'}

def decode_decl(m):
    r = recs[m]
    N = int(r[33])
    if not (1 <= N <= 8):
        return None
    ds = []
    start = 0
    for j in range(N):
        d = bytes(r[40 + j * 12: 40 + (j + 1) * 12])
        A, B, C, st, off, pad = struct.unpack('>6H', d)
        if B == 0:
            size = 3  # packed 3-byte normal (+pad)
        else:
            size = B * VAVT[C] if C < len(VAVT) else None
        if size is None:
            return None
        end = st if off == 0 else off
        ds.append({'attr': A, 'B': B, 'C': C, 'stride': st, 'off': off,
                   'start': start, 'end': end, 'size': size})
        start = end
    return N, ds

tiling_ok = 0
tiling_bad = []
decl_by_mat = {}
classes = Counter()
for m in range(M):
    r = decode_decl(m)
    if r is None:
        tiling_bad.append((m, 'decode'))
        continue
    N, ds = r
    stride = ds[0]['stride']
    end_total = ds[-1]['end']
    ok = end_total == stride and all(
        ds[i]['end'] == ds[i + 1]['start'] for i in range(N - 1))
    ok = ok and all(ds[i]['start'] < ds[i]['end'] or ds[i]['attr'] == 16 for i in range(N))
    if ok:
        tiling_ok += 1
        decl_by_mat[m] = ds
        classes[(stride, tuple(d['attr'] for d in ds))] += 1
    else:
        tiling_bad.append((m, [(d['attr'], d['start'], d['end'], d['stride']) for d in ds]))
print(f'tiling EXACT: {tiling_ok}/{M}; bad: {len(tiling_bad)}')
if tiling_bad[:3]:
    print('  bad samples:', tiling_bad[:3])
print('declaration classes (stride, attrs):')
for kk, v in classes.most_common(8):
    print('  ', v, kk)

# --- segments ---
g = open('/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla', 'rb').read()
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
print('lod table segs:', len(pairs))

segs = []
for k, (off2, cnt) in enumerate(pairs):
    hdr = struct.unpack_from('<17I', ld, off2)
    mat = hdr[10]
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
    segs.append({'k': k, 'mat': mat, 'off': data_off, 'vstart': data_off + 4, 'vb': vb, 'ib': ib,
                 'cnt': cnt})
print('seg count:', len(segs))

# stride agreement: declared stride vs vb-size/vertex-count census
agree = disagree = 0
dis_list = []
for sgm in segs:
    ds = decl_by_mat.get(sgm['mat'])
    if not ds:
        continue
    st = ds[0]['stride']
    nv = sgm['vb'] // st if st else 0
    if sgm['vb'] % st == 0 and nv > 0:
        agree += 1
    else:
        disagree += 1
        dis_list.append((sgm['k'], sgm['mat'], st, sgm['vb']))
print(f'seg stride == declared stride: {agree}/{agree + disagree} '
      f'(s46 was 1507/1526); disagree {disagree}')
if dis_list[:6]:
    print('  disagree samples:', dis_list[:6])

# --- decode vertices per declaration; tests ---
allpos = []
uv_bad = 0
uv_tot = 0
norm_good = 0
norm_tot = 0
pos_samples = []
for sgm in segs:
    ds = decl_by_mat.get(sgm['mat'])
    if not ds:
        continue
    st = ds[0]['stride']
    nv = sgm['vb'] // st
    if nv <= 0 or sgm['vb'] % st:
        continue
    base = sgm['off'] + 4  # vertex data begins after a 4-B record header (s46 vstart)
    vb_bytes = ld[base: base + sgm['vb']]
    arr = np.frombuffer(vb_bytes, np.uint8).reshape(nv, st)
    dmap = {d['attr']: d for d in ds}
    p = dmap.get(0)
    if p and p['size'] == 12:
        px = arr[:, 0:12].copy().view('<f4').reshape(nv, 3)
        allpos.append(px)
        if len(pos_samples) < 2:
            pos_samples.append((sgm['k'], px[:2].tolist()))
    for ua in (1, 2):
        d = dmap.get(ua)
        if d and d['size'] == 4:
            uv = arr[:, d['start']:d['start'] + 4].copy().view('<i2').reshape(nv, 2)
            f = uv.astype(np.float64) / 32767.0
            uv_tot += 1
            if not np.isfinite(f).all() or np.abs(f).max() > 8.0:
                uv_bad += 1
    dn = dmap.get(16)
    if dn and dn['B'] == 0:
        nb = arr[:, dn['start']:dn['start'] + 3].astype(np.float64)
        nrm = (nb - 127.5) / 127.5
        ln = np.sqrt((nrm ** 2).sum(1))
        norm_tot += 1
        if np.median(np.abs(ln - 1.0)) < 0.35:
            norm_good += 1

P = np.concatenate(allpos)
print('decoded positions:', P.shape)
print('pos extent min', P.min(0).tolist(), 'max', P.max(0).tolist())
print('UV: blocks', uv_tot, 'bad(>8 or nonfinite)', uv_bad)
print('packed-normal |n|~1: blocks', norm_tot, 'good', norm_good)
print('pos samples:', pos_samples)

# --- shuffled-descriptor null: permute attr labels per material, redecode
rng = np.random.default_rng(47)
null_inside = []
real_inside = None
# independent AABB: bih_struct root bbox
bh = open('/tmp/my-project/work/zone/GothamCity/bih_struct.bin', 'rb').read()
# take the first floats as a bbox candidate (root node)
bb = np.frombuffer(bh[:64], '<f4')
print('bih head floats:', bb[:12].tolist())
