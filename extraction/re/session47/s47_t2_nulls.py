#!/usr/bin/env python3
"""s47 T2 step C: settle the 3-byte field encoding (normal candidates vs
nulls), and the shuffled-descriptor null for the whole decode."""
import struct, io, zipfile, json
import numpy as np

bi = open('/tmp/my-project/work/zone/GothamCity/batch_info.bin', 'rb').read()
bstride, = struct.unpack_from('<I', bi, 0)
M = (len(bi) - 4) // bstride
recs = np.frombuffer(bi[4:], np.uint8).reshape(M, bstride)
VAVT = [1, 1, 2, 2, 4, 4, 4]

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
        size = 3 if B == 0 else B * VAVT[C]
        end = st if off == 0 else off
        ds.append({'attr': A, 'B': B, 'C': C, 'st': st, 'off': off,
                   'start': start, 'end': end, 'size': size})
        start = end
    return N, ds

decl_by_mat = {m: decode_decl(m)[1] for m in range(M) if decode_decl(m)}

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

bb = np.frombuffer(open('/tmp/my-project/work/zone/GothamCity/bih_struct.bin', 'rb').read()[:24], '<f4')
# bih bbox is (x,y,z); the lod stream stores (x,z,y) -> permute to match
BB_MIN = np.array([bb[0], bb[2], bb[1]])
BB_MAX = np.array([bb[3], bb[5], bb[4]])

def decode_positions(decl_map):
    """returns concatenated positions using the decl map (mat -> ds)"""
    out = []
    for k, (off2, cnt) in enumerate(pairs):
        hdr = struct.unpack_from('<17I', ld, off2)
        mat = hdr[10]
        ds = decl_map.get(mat)
        if not ds:
            continue
        data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
        st = ds[0]['st']
        nv = vb // st
        if nv <= 0 or vb % st:
            continue
        arr = np.frombuffer(ld, np.uint8, vb, data_off + 4).reshape(nv, st)
        d0 = [d for d in ds if d['attr'] == 0]
        if not d0 or d0[0]['size'] != 12:
            continue
        px = arr[:, d0[0]['start']:d0[0]['start'] + 12].copy().view('<f4').reshape(nv, 3)
        out.append(px)
    return np.concatenate(out)

P = decode_positions(decl_by_mat)
inside = ((P >= BB_MIN) & (P <= BB_MAX)).all(1).mean()
print(f'REAL decode: {P.shape[0]} verts, inside-bih-bbox fraction = {inside:.4f}')

# normal-encoding tests on the B=0 (3-byte) fields
rng = np.random.default_rng(47)
bias_med, signed_med, rnd_med = [], [], []
tested = 0
for k, (off2, cnt) in enumerate(pairs):
    hdr = struct.unpack_from('<17I', ld, off2)
    mat = hdr[10]
    ds = decl_by_mat.get(mat)
    if not ds:
        continue
    dn = [d for d in ds if d['attr'] == 16 and d['B'] == 0]
    if not dn:
        continue
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
    st = ds[0]['st']
    nv = vb // st
    if nv <= 0 or vb % st:
        continue
    arr = np.frombuffer(ld, np.uint8, vb, data_off + 4).reshape(nv, st)
    nb = arr[:, dn[0]['start']:dn[0]['start'] + 3].astype(np.float64)
    n1 = (nb - 127.5) / 127.5
    n2 = (nb.astype(np.int16).astype(np.float64)) / 127.0
    ln1 = np.sqrt((n1 ** 2).sum(1))
    ln2 = np.sqrt((n2 ** 2).sum(1))
    bias_med.append(np.median(np.abs(ln1 - 1.0)))
    signed_med.append(np.median(np.abs(ln2 - 1.0)))
    rn = rng.integers(0, 256, nb.shape).astype(np.float64)
    rn = (rn - 127.5) / 127.5
    rnd_med.append(np.median(np.abs(np.sqrt((rn ** 2).sum(1)) - 1.0)))
    tested += 1
    if tested >= 400:
        break
print(f'3-byte field |n|-1 median over {tested} blocks: bias127.5 = '
      f'{np.median(bias_med):.3f}, signed/127 = {np.median(signed_med):.3f}, '
      f'random-null = {np.median(rnd_med):.3f}')

# count blocks where EITHER decode gives unit-length
good1 = sum(1 for x in bias_med if x < 0.15)
good2 = sum(1 for x in signed_med if x < 0.15)
print(f'blocks |n|~1: bias {good1}, signed {good2} of {tested}')

# --- shuffled-descriptor null: permute (attr,B,C) triples across materials
perm = rng.permutation(M)
null_decl = {}
for m in range(M):
    src = decl_by_mat[perm[m]]
    st_src = src[0]['st']
    # keep this material's stride but transplant the permuted descriptors
    null_decl[m] = [dict(d) for d in src]
Pn = decode_positions(null_decl)
# NOTE: transplanting whole declarations keeps positions identical; the
# meaningful null permutes the ATTRIBUTE ROLES inside each declaration:
null_decl2 = {}
for m in range(M):
    ds = [dict(d) for d in decl_by_mat[m]]
    attrs = [d['attr'] for d in ds]
    rng.shuffle(attrs)
    for d, a in zip(ds, attrs):
        d['attr'] = a
    null_decl2[m] = ds
def decode_positions_attr(decl_map):
    out = []
    for k, (off2, cnt) in enumerate(pairs):
        hdr = struct.unpack_from('<17I', ld, off2)
        mat = hdr[10]
        ds = decl_map.get(mat)
        if not ds:
            continue
        data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
        st = ds[0]['st']
        nv = vb // st
        if nv <= 0 or vb % st:
            continue
        arr = np.frombuffer(ld, np.uint8, vb, data_off + 4).reshape(nv, st)
        d0 = [d for d in ds if d['attr'] == 0]
        if not d0:
            continue
        d = d0[0]
        if d['end'] - d['start'] != 12:
            continue
        px = arr[:, d['start']:d['end']].copy().view('<f4').reshape(nv, 3)
        out.append(px)
    return np.concatenate(out)
Pn2 = decode_positions_attr(null_decl2)
inside_n = ((Pn2 >= BB_MIN) & (Pn2 <= BB_MAX)).all(1).mean()
print(f'SHUFFLED-ATTR null: {Pn2.shape[0]} verts, inside fraction = {inside_n:.4f}')
json.dump({'real_inside': float(inside), 'null_inside': float(inside_n),
           'verts': int(P.shape[0]),
           'normal_bias_med': float(np.median(bias_med)),
           'normal_signed_med': float(np.median(signed_med)),
           'normal_rand_med': float(np.median(rnd_med))},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session47/s47_t2_nulls.json', 'w'), indent=1)
print('saved s47_t2_nulls.json')
