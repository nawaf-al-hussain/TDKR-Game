#!/usr/bin/env python3
"""s49 T1c: stride-28 segments + per-material/effect census over 1,526 segs."""
import struct, io, zipfile, json, collections
import numpy as np

GLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla'
BI = '/tmp/my-project/work/zone/GothamCity/batch_info.bin'
P = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'

# materials + effects + declared strides
LE = zipfile.ZipFile(io.BytesIO(open(P, 'rb').read())).read('little_endian_not_quantized.bdae')
w32 = np.frombuffer(LE, '<u4', len(LE) // 4); nb = len(LE)
def cs(p):
    if not (0 < p < nb): return None
    e = LE.find(b'\0', p)
    return LE[p:e].decode('ascii', 'replace') if 0 < e - p < 80 else None
mats = {}
for i in range(307):
    a = 0x5fea0 + i * 36
    ws = [int(w32[(a + k * 4) // 4]) for k in range(9)]
    mats[i] = (cs(ws[0]) or '').split('-fx')[0].lstrip('#') if ws[3] else 'None'

# batch_info declarations
bi = open(BI, 'rb').read()
bstride, = struct.unpack_from('<I', bi, 0)
M = (len(bi) - 4) // bstride
recs = np.frombuffer(bi[4:], np.uint8).reshape(M, bstride)
VAVT = [1, 1, 2, 2, 4, 4, 4]
def decl_of(mid):
    r = recs[mid]; N = int(r[33]); ds = []; start = 0
    for j in range(N):
        d = bytes(r[40 + j*12: 40 + (j+1)*12])
        A, B, C, st, off, pad = struct.unpack('>6H', d)
        size = 3 if B == 0 else B * VAVT[C]
        end = st if off == 0 else off
        ds.append((A, start, end, size)); start = end
    return ds
mat_stride = {i: decl_of(i)[-1][2] for i in range(307)}

# segments: lod_table pairs + lod_data headers (+40 = material)
g = open(GLA, 'rb').read()
_, idxsz, tabsz, n = struct.unpack('>IIII', g[:16])
pool = g[16 + n*16: idxsz]
ld = lt = None
for i in range(n):
    o, s, no, _ = struct.unpack('>IIII', g[16 + i*16: 16 + i*16 + 16])
    nm = pool[no:pool.index(b'\0', no)].decode('ascii', 'replace')
    if nm == 'GothamCity.zip':
        Z = zipfile.ZipFile(io.BytesIO(g[o:o+s])); ld = Z.read('lod_data.bin'); lt = Z.read('lod_table.bin'); break
u = struct.unpack(f'<{len(lt)//4}I', lt)
pairs = [(u[1+2*k], u[2+2*k]) for k in range(u[0])]

segs = []
for k, (off2, _) in enumerate(pairs):
    mat, = struct.unpack_from('<I', ld, off2 + 40)
    segs.append({'k': k, 'mat': int(mat), 'stride': mat_stride.get(int(mat))})

# stride census
sc = collections.Counter(s['stride'] for s in segs)
print('stride census over 1,526 segs:', dict(sorted(sc.items(), key=lambda x: -x[1])))
s28 = [s for s in segs if s['stride'] == 28]
print('stride-28 segments:', [(s['k'], s['mat'], mats.get(s['mat'])) for s in s28])
# mat 156 segs (any stride)
m156 = [s for s in segs if s['mat'] == 156]
print('mat 156 segs:', [(s['k'], s['stride']) for s in m156])
# effect census
ec = collections.Counter(mats.get(s['mat'], '?') for s in segs)
print('effect census:', dict(ec.most_common()))
# which AlphaMasking mats carry segs
am = [i for i in range(307) if mats.get(i) == 'AlphaMasking']
use = collections.Counter(s['mat'] for s in segs if s['mat'] in am)
print('AlphaMasking segs by mat:', dict(use), '(mats', am, ')')
# mat 5 usage
print('mat 5 segs:', sum(1 for s in segs if s['mat'] == 5))
# NormalSpecOverbright / NV_Glass mats with segs
for fx in ('NormalSpecOverbright', 'NV_Glass', 'SimpleAdditive'):
    mm = [i for i in range(307) if mats.get(i) == fx]
    print(fx, 'mats:', mm, 'segs:', dict(collections.Counter(s['mat'] for s in segs if s['mat'] in mm)))
# mat 156 uniform recap
print('mat 156 effect:', mats[156], 'stride:', mat_stride[156])
json.dump({'segs': segs, 'mat_fx': {str(k): v for k, v in mats.items()},
           'mat_stride': {str(k): v for k, v in mat_stride.items()}},
          open('s49_t1c_census.json', 'w'))
print('saved')
