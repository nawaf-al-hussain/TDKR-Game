#!/usr/bin/env python3
"""s47 T2 step A: raw descriptor bytes + engine attribute value-type table.
Dump batch_info descriptors for representative materials of each stride
class, and extract the E_VERTEX_ATTRIBUTE_VALUE_TYPE size table near
0xb8613c from libKRHP.so."""
import struct, io, zipfile
import numpy as np

bi = open('/tmp/my-project/work/zone/GothamCity/batch_info.bin', 'rb').read()
bstride, = struct.unpack_from('<I', bi, 0)
M = (len(bi) - 4) // bstride
recs = np.frombuffer(bi[4:], np.uint8).reshape(M, bstride)
print('batch_info: bstride', bstride, 'records', M)

g = open('/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla', 'rb').read()
_, idxsz, tabsz, n = struct.unpack('>IIII', g[:16])
pool = g[16 + n * 16:idxsz]
Z = None
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
# map material -> (record idx, seg count, raw stride from vb size)
mat_recs = {}
for k in range(len(pairs)):
    off2 = pairs[k][0]
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
    hdr = struct.unpack_from('<17I', ld, off2)
    st = None
    for cand in (20, 24, 28):
        if vb % cand == 0:
            st = cand
            break
    mat_recs.setdefault(hdr[10], []).append((k, hdr, vb, ib, st))

# dump descriptors for a few materials per class
def dump_mat(m):
    r = recs[m]
    N = int(r[33]) if bstride > 33 else 0
    print(f'--- material {m}: record head u16 BE ---')
    ws = struct.unpack(f'>{(bstride//2)}H', r[:bstride//2*2].tobytes())
    print('  ', [hex(x) for x in ws[:24]])
    print('  raw bytes:', bytes(r[:56]).hex(' '))
    if 1 <= N <= 8:
        for j in range(N):
            d = r[40 + j * 12: 40 + (j + 1) * 12]
            print(f"  desc {j}: {bytes(d).hex(chr(32))}")
    return N

seen = set()
for m in range(M):
    r = recs[m]
    key = None
    # class by the u16 at word where stride lives — just bucket by N and first desc
    N = int(r[33])
    if (N) in (3, 4, 5) and N not in seen:
        seen.add(N)
        dump_mat(m)
    if len(seen) >= 3:
        break

# --- engine type table near 0xb8613c ---
so = open('/tmp/my-project/work/apk_lib/lib/armeabi-v7a/libKRHP.so', 'rb').read()
print('--- strings near 0xb8613c ---')
region = so[0xb8613c - 0x200: 0xb8613c + 0x200]
txt = region.decode('latin1')
import re
print([s for s in re.findall(r'[ -~]{2,}', txt)][:24])
# size table candidates: bytes 1,1,2,2,4,4,4 near the names
for probe in range(0xb8613c - 0x80, 0xb8613c + 0x80, 4):
    b = so[probe:probe + 7]
    if b in (bytes([1, 1, 2, 2, 4, 4, 4]), bytes([1, 1, 2, 2, 4, 4, 8])):
        print('size table candidate @', hex(probe), list(b))
