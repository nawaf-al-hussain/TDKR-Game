#!/usr/bin/env python3
"""s43 T2e FINAL: attribute-aware decode of all streamed zone segments (both islands)
with engine-justified checks, plus the row-shuffle null.

LAYOUT TABLE (recovered):
  stride 20 = Position(3xf32) | F(snorm8x3+pad)@12 | Color0(u8x4)@16
  stride 24 = Position(3xf32) | Coord0(2xsnorm16)@12 | F(snorm8x3+pad)@16 | Color0(u8x4)@20
  stride 28 = Position(3xf32) | Coord0@12 | Coord1@16 | F@20 | Color0@24
  stride 32 = (family +4B; zero segments shipped — unverified)
  F = per-vertex normal field; unit-normalized ONLY in the lit material subset;
      zone VS/FS call normalize(Normal) so storage magnitude is unconstrained.
Checks: positions finite+in-bbox(+pad); Coord ranges [-1,1]; F finite non-degenerate;
F smoothness via index edges (the discriminator); max index < nv.
NULL: per-segment row-shuffle of F -> edge smoothness must collapse.
"""
import struct, io, zipfile, collections, json
import numpy as np

P = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla'
g = open(P, 'rb').read()
_, idxsz, tabsz, n = struct.unpack('>IIII', g[:16])
pool = g[16 + n * 16:idxsz]
members = {}
for i in range(n):
    o, s, no, _ = struct.unpack('>IIII', g[16 + i * 16:16 + i * 16 + 16])
    nm = pool[no:pool.index(b'\0', no)].decode('ascii', 'replace')
    members[nm] = (o, s)


def s8a(v):
    v = v.astype(np.int16)
    return np.where(v >= 128, v - 256, v) / 127.0


def s16a(v):
    v = v.astype(np.int32)
    return np.where(v >= 32768, v - 65536, v) / 32767.0


def edge_smooth(nrm, tris):
    i0, i1, i2 = tris[:, 0], tris[:, 1], tris[:, 2]
    d = (np.abs(nrm[i0] - nrm[i1]).sum(axis=1) +
         np.abs(nrm[i1] - nrm[i2]).sum(axis=1) +
         np.abs(nrm[i2] - nrm[i0]).sum(axis=1)) / 3.0
    return float(d.mean())


def decode_zone(zname, rng):
    zo, zs = members[zname]
    Z = zipfile.ZipFile(io.BytesIO(g[zo:zo + zs]))
    si = Z.read('stream_info.bin')
    bbox = struct.unpack('<6f', si[:24])
    ld = Z.read('lod_data.bin')
    lt = Z.read('lod_table.bin')
    u = struct.unpack(f'<{len(lt)//4}I', lt)
    cnt = u[0]
    pairs = [(u[1 + 2 * k], u[2 + 2 * k]) for k in range(cnt)]
    stats = collections.Counter()
    per_stride = collections.Counter()
    unit_normals = 0
    smooth_real, smooth_null = [], []
    fails = []
    pad = 30.0
    for k in range(cnt):
        off2 = pairs[k][0]
        data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
        hdr = struct.unpack_from('<17I', ld, off2)
        mat = hdr[10]
        if four != 4:
            stats['skip_four'] += 1
            continue
        vstart = data_off + 4
        idx = np.frombuffer(ld, '<u2', ib // 2, vstart + vb).astype(np.int64)
        real = idx[idx != 0xFFFF]
        if len(real) == 0:
            stats['skip_empty'] += 1
            continue
        mx = int(real.max())
        cands = [s for s in (24, 20, 32, 28) if vb % s == 0 and mx < vb // s]
        if not cands:
            stats['skip_nostride'] += 1
            fails.append((k, 'nostride'))
            continue
        st = cands[0]
        nv = vb // st
        raw = np.frombuffer(ld, np.uint8, vb, vstart).reshape(nv, st)
        pos = raw[:, :12].copy().view('<f4').reshape(nv, 3).astype(np.float64)
        if not (np.isfinite(pos).all() and np.abs(pos).max() < 8000):
            stats['fail_pos'] += 1
            fails.append((k, 'pos'))
            continue
        inb = ((pos[:, 0] >= bbox[0] - pad) & (pos[:, 0] <= bbox[3] + pad) &
               (pos[:, 1] >= bbox[1] - pad) & (pos[:, 1] <= bbox[4] + pad) &
               (pos[:, 2] >= bbox[2] - pad) & (pos[:, 2] <= bbox[5] + pad)).all()
        if not inb:
            stats['fail_bbox'] += 1
            fails.append((k, 'bbox'))
            continue
        if st == 20:
            foff, cuv = 12, []
        elif st == 24:
            foff, cuv = 16, [12]
        elif st == 28:
            foff, cuv = 20, [12, 16]
        else:
            foff, cuv = 20, [12, 16]
        uv_ok = True
        for uoff in cuv:
            uv = s16a(raw[:, uoff:uoff + 4].copy().view('<u2').reshape(nv, 2))
            if not (np.isfinite(uv).all() and np.abs(uv).max() <= 1.0 + 1e-6):
                uv_ok = False
        if not uv_ok:
            stats['fail_uv'] += 1
            fails.append((k, 'uv'))
            continue
        F = s8a(raw[:, foff:foff + 3])
        fn = np.linalg.norm(F, axis=1)
        if not (np.isfinite(fn).all() and fn.min() > 0.02):
            stats['fail_F'] += 1
            fails.append((k, 'F'))
            continue
        tris = idx.reshape(-1, 3)
        tris = tris[(tris != 0xFFFF).all(axis=1)]
        if len(tris) == 0:
            stats['skip_notris'] += 1
            continue
        sm = edge_smooth(F, tris)
        # paired null: row-shuffle F, self-calibrated per segment (hard edges OK)
        nulls = [edge_smooth(F[rng.permutation(nv)], tris) for _ in range(4)]
        sm_null = float(np.mean(nulls))
        fnmag = float(fn.mean())
        if fnmag < 0.06 or sm_null < 0.12:
            stats['indeterminate'] += 1   # field too small to discriminate
            stats['ok'] += 1
            per_stride[st] += 1
            smooth_real.append(sm)
            smooth_null.append(sm_null)
            if np.abs(fn - 1.0).max() < 0.03:
                unit_normals += 1
            continue
        elif sm > 0.6 * sm_null:
            stats['fail_smooth'] += 1
            fails.append((k, 'smooth'))
            continue
        # unit-normal subset detection
        if np.abs(fn - 1.0).max() < 0.03:
            unit_normals += 1
        stats['ok'] += 1
        per_stride[st] += 1
        smooth_real.append(sm)
        smooth_null.append(sm_null)
    return {'zone': zname, 'segments': cnt, 'stats': dict(stats), 'per_stride': dict(per_stride),
            'unit_normal_segs': unit_normals,
            'smooth_real_mean': float(np.mean(smooth_real)), 'smooth_real_p95': float(np.percentile(smooth_real, 95)),
            'smooth_null_mean': float(np.mean(smooth_null)), 'smooth_null_p05': float(np.percentile(smooth_null, 5)),
            'first_fails': fails[:8]}


rng = np.random.default_rng(42)
r1 = decode_zone('GothamCity.zip', rng)
print(json.dumps(r1, indent=1))
r2 = decode_zone('GothamCity_Island2.zip', rng)
print(json.dumps(r2, indent=1))
json.dump({'island1': r1, 'island2': r2}, open('/home/z/my-project/scripts/s43_t2_result.json', 'w'), indent=1)
