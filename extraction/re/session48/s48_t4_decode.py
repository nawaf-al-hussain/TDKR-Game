#!/usr/bin/env python3
"""s48 T4: (1) re-run the s43/s44 strict edge-smoothness criterion on the
3-byte packed normal with the CORRECTED descriptor semantics (normal = declared
attr 16 span, END-offset chain), for GothamCity (1,526 segs) and Island2
(1,020); compare with the OLD fixed-@16 decode (which failed 301 strict on
island1). Unit-ness stats for the failing sets. (2) declaration-driven decoded
VALUE digests (positions/normals/UVs, f64 canonical stream) for both zones —
the JS decoder (city_slice8.html) must reproduce them byte-for-byte."""
import struct, io, zipfile, json, hashlib
import numpy as np

GLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla'
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session48/s48_t4_decode.json'

g = open(GLA, 'rb').read()
_, idxsz, tabsz, n = struct.unpack('>IIII', g[:16])
pool = g[16 + n * 16:idxsz]
zones = {}
for i in range(n):
    o, s, no, _ = struct.unpack('>IIII', g[16 + i * 16:16 + i * 16 + 16])
    nm = pool[no:pool.index(b'\0', no)].decode('ascii', 'replace')
    if nm in ('GothamCity.zip', 'GothamCity_Island2.zip'):
        Z = zipfile.ZipFile(io.BytesIO(g[o:o + s]))
        zones[nm] = (Z.read('lod_data.bin'), Z.read('lod_table.bin'),
                     Z.read('batch_info.bin'))
print('zones:', list(zones.keys()))

VAVT = [1, 1, 2, 2, 4, 4, 4]

def decl_of(recs, mid):
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

def s8trip(raw):
    v = raw.astype(np.int16)
    v = np.where(v >= 128, v - 256, v)
    return v / 127.0

def edge_smooth(nrm, idx):
    tris = idx.reshape(-1, 3)
    tris = tris[(tris != 0xFFFF).all(axis=1)]
    if len(tris) == 0:
        return None
    i0, i1, i2 = tris[:, 0], tris[:, 1], tris[:, 2]
    d = (np.abs(nrm[i0] - nrm[i1]).sum(axis=1) +
         np.abs(nrm[i1] - nrm[i2]).sum(axis=1) +
         np.abs(nrm[i2] - nrm[i0]).sum(axis=1)) / (3 * len(tris))
    return float(d.mean())

def zone_segs(ld, lt, bi):
    bstride, = struct.unpack_from('<I', bi, 0)
    recs = np.frombuffer(bi[4:], np.uint8).reshape((len(bi) - 4) // bstride, bstride)
    u = struct.unpack(f'<{len(lt)//4}I', lt)
    pairs = [(u[1 + 2 * k], u[2 + 2 * k]) for k in range(u[0])]
    segs = []
    for k, (off2, cnt) in enumerate(pairs):
        hdr = struct.unpack_from('<17I', ld, off2)
        mid = hdr[10]
        data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
        ds = decl_of(recs, mid)
        dmap = {d[0]: d for d in ds}
        stride = ds[-1][2]
        nv = vb // stride
        segs.append({'k': k, 'mat': mid, 'stride': stride, 'nv': nv,
                     'off': data_off + 4, 'vb': vb, 'ib': ib,
                     'decl': [(a, s0, e, sz) for (a, s0, e, sz) in ds],
                     'n_start': dmap[16][1] if 16 in dmap else None})
    return segs, recs

rng = np.random.default_rng(410)
out = {'zones': {}}
digests = {}
for zname in ('GothamCity.zip', 'GothamCity_Island2.zip'):
    ld, lt, bi = zones[zname]
    segs, recs = zone_segs(ld, lt, bi)
    print(zname, len(segs), 'segs,', int(sum(s['nv'] for s in segs)), 'verts')
    # ---------- (1) smoothness: EXACT s44 reproduction + corrected decode
    u = struct.unpack(f'<{len(lt)//4}I', lt)
    pairs4 = [u[1 + 2 * k] for k in range(u[0])]
    # s44 protocol: population filter hdr[3]==4 ('four'), probe stride detection
    # cands(24,20,32,28) first-match with mx<vb//s, F@{20:12,24:16,28:20},
    # s8 = first 3 of the 4-B field as signed /127, per-seg RandomState(0x544B+k),
    # 4 paired row-shuffle nulls, pass = real < min(nulls); 301 fail on island1.
    old_fail = []
    new_fail = []
    unit_new_fail = []
    unit_at301 = []
    n_used = 0
    for si, s in enumerate(segs):
        off2 = pairs4[si]
        hdr = struct.unpack_from('<17I', ld, off2)
        data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
        if four != 4:
            continue
        vstart = data_off + 4
        idx = np.frombuffer(ld, '<u2', ib // 2, vstart + vb).astype(np.int64)
        real = idx[idx != 0xFFFF]
        if len(real) == 0:
            continue
        mx = int(real.max())
        cands = [st for st in (24, 20, 32, 28) if vb % st == 0 and mx < vb // st]
        if not cands or cands[0] == 32:
            continue
        st = cands[0]
        foff = {20: 12, 24: 16, 28: 20}[st]
        nv = vb // st
        n_used += 1
        raw = np.frombuffer(ld, np.uint8, vb, vstart).reshape(nv, st)
        F = raw[:, foff:foff + 4]
        s8f = F[:, :3].astype(np.int16)
        s8f = np.where(s8f >= 128, s8f - 256, s8f) / 127.0
        rs = np.random.RandomState(0x544B + si)
        sm = edge_smooth(s8f, idx)
        nulls = [edge_smooth(s8f[rs.permutation(nv)], idx) for _ in range(4)]
        if sm is not None and None not in nulls and sm >= min(nulls):
            old_fail.append(si)
        # corrected decode on the SAME segment: declared stride + attr-16 span
        ds = decl_of(recs, s['mat'])
        dmap = {d[0]: d for d in ds}
        stride_n = ds[-1][2]
        if 16 not in dmap or vb % stride_n != 0:
            continue
        nvn = vb // stride_n
        rawn = np.frombuffer(ld, np.uint8, vb, vstart).reshape(nvn, stride_n)
        ns = dmap[16][1]
        nn = np.zeros((nvn, 3))
        for c in range(3):
            col = rawn[:, ns + c].astype(np.int16)
            nn[:, c] = np.where(col >= 128, col - 256, col) / 127.0
        dev = np.abs(np.linalg.norm(nn, axis=1) - 1.0)
        med_dev = float(np.median(dev))
        smn = edge_smooth(nn, idx)
        nullsn = [edge_smooth(nn[rs.permutation(nvn)], idx) for _ in range(4)]
        if smn is None or None in nullsn or smn >= min(nullsn):
            new_fail.append(si)
            unit_new_fail.append(med_dev)
        if si in set(old_fail):
            unit_at301.append(med_dev)
    print('  s44 population used: %d; EXACT repro fail: %d; corrected-decode fail: %d'
          % (n_used, len(old_fail), len(new_fail)))
    if unit_at301:
        print('  unit |n|-1 median on the s44-301 set (corrected decode): %.4f'
              % float(np.median(unit_at301)))
    if unit_new_fail:
        print('  unit |n|-1 median on the corrected-fail set: %.4f'
              % float(np.median(unit_new_fail)))
    out['zones'][zname] = {'n_segs': len(segs), 'n_used_s44pop': n_used,
                           'old_fail_n': len(old_fail), 'new_fail_n': len(new_fail),
                           'unit_median_s44set': (float(np.median(unit_at301))
                                                  if unit_at301 else None),
                           'unit_median_newfail': (float(np.median(unit_new_fail))
                                                   if unit_new_fail else None),
                           'old_fail': old_fail, 'new_fail': new_fail}
    # ---------- (2) declaration-driven decoded value digests (f64 canonical)
    streams = {'pos': bytearray(), 'nrm': bytearray(), 'uv0': bytearray(), 'uv1': bytearray()}
    for s in segs:
        nv, stride, off = s['nv'], s['stride'], s['off']
        dmap = {d[0]: d for d in s['decl']}
        raw = np.frombuffer(ld, np.uint8, s['vb'], off).reshape(nv, stride) if nv > 0 else None
        streams['pos'] += struct.pack('<I', nv)
        streams['nrm'] += struct.pack('<I', nv)
        streams['uv0'] += struct.pack('<I', nv)
        streams['uv1'] += struct.pack('<I', nv)
        if nv == 0:
            continue
        pos = raw[:, 0:12].copy().view('<f4').reshape(nv, 3).astype(np.float64)
        streams['pos'] += pos.tobytes()
        if 16 in dmap:
            ns = dmap[16][1]
            nrm = np.stack([s8trip(raw[:, ns]), s8trip(raw[:, ns + 1]),
                            s8trip(raw[:, ns + 2])], axis=1).astype(np.float64)
            streams['nrm'] += nrm.tobytes()
        if 1 in dmap:
            d0 = dmap[1]
            uv = raw[:, d0[1]:d0[1] + 4].copy().view('<i2').reshape(nv, 2).astype(np.float64) / 32767.0
            streams['uv0'] += uv.tobytes()
        if 2 in dmap:
            d1 = dmap[2]
            uv = raw[:, d1[1]:d1[1] + 4].copy().view('<i2').reshape(nv, 2).astype(np.float64) / 32767.0
            streams['uv1'] += uv.tobytes()
    dig = {name: hashlib.sha256(bytes(buf)).hexdigest() for name, buf in streams.items()}
    digests[zname] = dig
    print('  digests:', json.dumps(dig, indent=0))

out['digests'] = digests
json.dump(out, open(OUT, 'w'), indent=1)
print('saved', OUT)
