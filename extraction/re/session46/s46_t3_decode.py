#!/usr/bin/env python3
"""s46 T3: decode batch_info per-material vertex declarations; validate the
alignment against the lod seg stride census; tabulate per stride class."""
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
mat2stride = {}
for k in range(len(pairs)):
    off2 = pairs[k][0]
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
    hdr = struct.unpack_from('<17I', ld, off2)
    st = 20
    if vb % 28 == 0:
        st = 28
    if vb % 24 == 0:
        st = 24
    mat2stride.setdefault(hdr[10], Counter())[st] += 1

ATTR = {0: 'Position', 1: 'TexCoord0', 2: 'TexCoord1', 3: 'TexCoord2', 4: 'TexCoord3',
        16: 'Normal', 17: 'Color0', 18: 'Color1', 19: 'Tangent', 20: 'Binormal'}

def decode_record(m, dstart=40, dsize=12):
    N = int(recs[m, 33])
    if not (1 <= N <= 8):
        return None
    if dstart + N * dsize > bstride:
        return None
    ds = []
    for j in range(N):
        d = recs[m, dstart + j * dsize: dstart + (j + 1) * dsize]
        A, B, C, st, off, pad = struct.unpack('<6H', d.tobytes())
        ds.append((A, B, C, st, off, pad))
    return N, ds

ok = tot = 0
for m in range(M):
    r = decode_record(m)
    if r is None:
        continue
    N, ds = r
    tot += 1
    sts = set(d[3] for d in ds if d[3] in (20, 24, 28))
    if m in mat2stride and sts and sts <= set(mat2stride[m]):
        ok += 1
print(f'descriptor decode: stride-consistent {ok}/{tot} (subset of lod census strides)')

# tabulate declarations per stride class
decl = defaultdict(Counter)
bad = []
for m in range(M):
    r = decode_record(m)
    if r is None:
        bad.append(m)
        continue
    N, ds = r
    for (A, B, C, st, off, pad) in ds:
        decl[st][(A, C, off)] += 1
print('\nper-stride (attrId A, type C, offset) census:')
for st in sorted(decl):
    print(f'  stride {st}: ' + ', '.join(f'(A={a}:{ATTR.get(a,"?")},C={c}@{off})x{n}' for (a, c, off), n in sorted(decl[st].items())))
# B field census
Bc = Counter()
for m in range(M):
    r = decode_record(m)
    if r:
        for d in r[1]:
            Bc[d[1]] += 1
print('B census:', Bc.most_common(8))
# records not matching any lod stride (unused materials etc.)
print('records with no/invalid N:', len(bad), bad[:8])

# @16 field per stride class (the task question)
for st in (20, 24, 28):
    entries = [(a, c, off) for (a, c, off), n in decl[st].items() if off == 16]
    print(f'stride {st}: @16 = {[(ATTR.get(a, a), c, n) for a, c, n in entries]}')

json.dump({'adopted': {'dstart': 40, 'dsize': 12, 'consistent': ok},
           'decl': {str(k): {f'A{a}C{c}@{off}': n for (a, c, off), n in sorted(v.items())}
                    for k, v in decl.items()},
           'B_census': {str(k): v for k, v in Bc.items()},
           'bad_records': bad},
          open('/home/z/my-project/scripts/s46_t3_batchinfo_decoded.json', 'w'), indent=1)
