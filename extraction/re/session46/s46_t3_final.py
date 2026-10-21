#!/usr/bin/env python3
"""s46 T3 final: batch_info declarations for all 307 materials (BE u16 fields),
tiling validation, per-seg stride agreement + shuffled null, count reconciliation."""
import struct, io, zipfile, json
import numpy as np
from collections import Counter, defaultdict

bi = open('/tmp/my-project/work/zone/GothamCity/batch_info.bin', 'rb').read()
bstride, = struct.unpack_from('<I', bi, 0)
M = (len(bi) - 4) // bstride
recs = np.frombuffer(bi[4:], np.uint8).reshape(M, bstride)

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
segs = []
for k in range(len(pairs)):
    off2 = pairs[k][0]
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
    hdr = struct.unpack_from('<17I', ld, off2)
    st = 20
    if vb % 28 == 0:
        st = 28
    if vb % 24 == 0:
        st = 24
    segs.append((k, hdr[10], st, vb // st, ib // 6))

TYPE_BYTES = {1: 4, 2: 4, 3: 12, 4: 4, 5: 8, 6: 16, 7: 8}
ATTR = {0: 'Position', 1: 'TexCoord0', 2: 'TexCoord1', 3: 'TexCoord2', 16: 'Normal',
        17: 'Color0', 18: 'Color1', 19: 'Tangent', 20: 'Binormal'}

def decode(m):
    N = int(recs[m, 33])
    if not (1 <= N <= 8):
        return None
    ds = []
    for j in range(N):
        b = recs[m, 40 + j * 12: 52 + j * 12]
        A, B, C, st, off, pad = struct.unpack('>6H', b.tobytes())
        ds.append({'attr': A, 'unit': B, 'type': C, 'stride': st, 'offset': off})
    return N, ds

# --- 307-record validation: tiling + stride
tiling_ok, stride_mats, decl_tab = 0, {}, defaultdict(Counter)
no_lod = []
for m in range(M):
    r = decode(m)
    if r is None:
        continue
    N, ds = r
    sts = set(d['stride'] for d in ds)
    # tiling: sort by offset; coverage [0, stride) with attr sizes
    ok_t = False
    if len(sts) == 1:
        st = sts.pop()
        if st in (20, 24, 28):
            try:
                cov = 0
                tiles = sorted((d['offset'], TYPE_BYTES.get(d['type'], 0)) for d in ds)
                for off, sz in tiles:
                    if off != cov:
                        break
                    cov += sz
                ok_t = (cov == st)
            except Exception:
                pass
            stride_mats[m] = st
            for d in ds:
                decl_tab[st][(d['attr'], d['type'], d['offset'])] += 1
    if ok_t:
        tiling_ok += 1
    else:
        no_lod.append(m)
print(f'records decoded: {M}; stride class known: {len(stride_mats)}; '
      f'tiling-exact: {tiling_ok}; non-tiling/odd: {len(no_lod)} {no_lod[:10]}')

print('\nDECLARATION TABLE per stride class (attr: type @offset -> xN materials):')
for st in sorted(decl_tab):
    parts = []
    for (a, t, off), cnt in sorted(decl_tab[st].items(), key=lambda kv: kv[0][2]):
        parts.append(f'{ATTR.get(a, a)}(t{t})@{off} x{cnt}')
    print(f'  stride {st}: ' + ' | '.join(parts))

# --- per-seg agreement + shuffled null
seg_ok = seg_bad = 0
bad_list = []
rng = np.random.default_rng(4646)
perm = rng.permutation(M)
for (k, mat, st, nv, ntri) in segs:
    r = decode(mat)
    dst = stride_mats.get(mat)
    if dst == st:
        seg_ok += 1
    else:
        seg_bad += 1
        bad_list.append((k, mat, st, dst))
null_ok = null_bad = 0
for (k, mat, st, nv, ntri) in segs:
    pm = int(perm[mat % M])
    dst = stride_mats.get(pm)
    if dst == st:
        null_ok += 1
    else:
        null_bad += 1
print(f'\nper-seg declaration-stride agreement: {seg_ok}/{seg_ok + seg_bad} '
      f'(mismatches: {len(bad_list)}; first: {bad_list[:6]})')
print(f'shuffled-material null: agreement {null_ok}, mismatch {null_bad} '
      f'({null_bad / (null_ok + null_bad):.1%} — real mismatch rate '
      f'{seg_bad / (seg_ok + seg_bad):.2%})')

# --- smoothness count reconciliation (criteria from saved s43/s44 analyses)
rec = {
 'criterion_s43_single_null': 'F-field row-shuffled once; seg fails if real F smoothness (mean |dF| over adjacent-vertex pairs) fails to beat its single shuffled null; on the shared 1,526-island1 population -> 238 fail',
 'criterion_s44_strict': 'min-of-4 nulls (4 independent shuffles); seg must beat ALL 4 -> stricter; 301 fail on the same population',
 'criterion_s43_reported_615': 's43 run reported 615 = its looser single-null pass on a different threshold + island2 305 added; not a population contradiction (s45 reconciliation)',
 'adopted': 's44 strict min-of-4 = 301/1526 island1 (conservative; the other counts are criterion variants, not population disagreements)'
}
print('\ncount reconciliation:', json.dumps(rec, indent=1))

out = {'tiling_exact': tiling_ok, 'stride_class_mats': len(stride_mats),
       'decl_table': {str(k): {f'{ATTR.get(a,a)}(t{t})@{off}': c
                               for (a, t, off), c in sorted(v.items(), key=lambda x: x[0][2])}
                      for k, v in decl_tab.items()},
       'seg_agreement': seg_ok, 'seg_mismatch': len(bad_list), 'bad_list': bad_list[:20],
       'null_mismatch': null_bad, 'reconciliation': rec}
json.dump(out, open('/home/z/my-project/scripts/s46_t3_final.json', 'w'), indent=1)
print('\nsaved s46_t3_final.json')
