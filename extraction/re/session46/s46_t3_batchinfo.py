#!/usr/bin/env python3
"""s46 T3: decode batch_info.bin (307 x 197 B) into per-material vertex
declarations; tabulate (stride, attribute id, offset, type) per stride class
against the lod seg census; identify the @16 field."""
import struct, io, zipfile, json
import numpy as np

bi = open('/tmp/my-project/work/zone/GothamCity/batch_info.bin', 'rb').read()
stride, = struct.unpack_from('<I', bi, 0)
M = (len(bi) - 4) // stride
recs = np.frombuffer(bi[4:], np.uint8).reshape(M, stride)
print(f'batch_info: stride {stride}, M {M}, leftover {(len(bi)-4) % stride}')

def hexrow(b, start=0, n=None):
    n = n or len(b)
    return ' '.join(f'{x:02x}' for x in b[start:start+n])

for m in (0, 2, 73, 4, 156, 145, 302):
    print(f'\nmat {m}: {hexrow(recs[m])}')

# census: material -> lod seg strides
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
mat2strides = {}
for k in range(len(pairs)):
    off2 = pairs[k][0]
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
    hdr = struct.unpack_from('<17I', ld, off2)
    mat = hdr[10]
    st = 20
    if vb % 28 == 0:
        st = 28
    if vb % 24 == 0:
        st = 24
    mat2strides.setdefault(mat, set()).add(st)
mixed = {m: v for m, v in mat2strides.items() if len(v) > 1}
print(f'\nmats seen in lod: {len(mat2strides)}; mixed-stride mats: {len(mixed)} {list(mixed.items())[:4]}')
