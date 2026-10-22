#!/usr/bin/env python3
"""s51 T1k: locate mat73 segments (bbox + density) to pick a zoom window."""
import struct, io, zipfile, sys
import numpy as np

GLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla'
BDAE = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
LE = zipfile.ZipFile(io.BytesIO(open(BDAE, 'rb').read())).read('little_endian_not_quantized.bdae')
NB = len(LE)
w32 = np.frombuffer(LE, '<u4', NB // 4)

def cstr(off, maxn=96):
    if not (0 < off < NB): return None
    e = int(LE.find(b'\0', off))
    if e < 0 or e == off or e - off > maxn: return None
    try: t = LE[off:e].decode('ascii')
    except Exception: return None
    return t if all(32 <= ord(c) < 127 for c in t) else None

g = open(GLA, 'rb').read()
_, idxsz, tabsz, n = struct.unpack('>IIII', g[:16])
pool = g[16 + n * 16:idxsz]
for i in range(n):
    o, s, no, _ = struct.unpack('>IIII', g[16 + i * 16:16 + i * 16 + 16])
    nm = pool[no:pool.index(b'\0', no)].decode('ascii', 'replace')
    if nm == 'GothamCity.zip':
        Zz = zipfile.ZipFile(io.BytesIO(g[o:o + s]))
        ld = Zz.read('lod_data.bin')
        lt = Zz.read('lod_table.bin')
        break
u = struct.unpack('<%dI' % (len(lt) // 4), lt)
pairs = [(u[1 + 2 * k], u[2 + 2 * k]) for k in range(u[0])]

# decl_of from pyref
src = open('/tmp/my-project/work/TDKR-Game/extraction/re/session50/s50_t1_pyref.py').read()
out = []
for ln in src.splitlines(True):
    if ln.startswith('ap = argparse.ArgumentParser()'):
        out.append('class _A: flat=False; only=None; noLM=False; lmonly=False; zbuf=False; mat=73; bbox=None; grad=False; snap=False; out="x"\nargs=_A()\n')
    elif ln.startswith('ap.add_argument') or ln.startswith('args = ap.parse_args()'):
        continue
    else:
        out.append(ln)
code = ''.join(out)
cut = code.index('segdata = []')
ns = {'__name__': 't1k'}
exec(compile(code[:cut], 'pyref_head', 'exec'), ns)
ld2 = ns['ld']; pairs2 = ns['pairs']; decl_of2 = ns['decl_of']

pts = []
for k, (off2, cnt) in enumerate(pairs2):
    hdr = struct.unpack_from('<17I', ld2, off2)
    mid = hdr[10]
    if mid != 73:
        continue
    data_off, four, vb, ib = struct.unpack_from('<4I', ld2, off2 + 68)
    ds = decl_of2(mid)
    stride = ds[-1][2]
    nvv = vb // stride
    raw = np.frombuffer(ld2, np.uint8, vb, data_off + 4).reshape(nvv, stride)
    pos = raw[:, 0:12].copy().view('<f4').reshape(-1, 3)
    pts.append(pos)
P = np.concatenate(pts)
print('mat73 segs: %d  verts %d' % (len(pts), len(P)))
print('bbox x [%.1f .. %.1f]  z(y) [%.1f .. %.1f]  h [%.2f .. %.2f]' % (
    P[:, 0].min(), P[:, 0].max(), P[:, 1].min(), P[:, 1].max(), P[:, 2].min(), P[:, 2].max()))
# density: 200m grid
gx = np.clip(((P[:, 0] - P[:, 0].min()) / 200).astype(int), 0, 99)
gz = np.clip(((P[:, 1] - P[:, 1].min()) / 200).astype(int), 0, 99)
from collections import Counter
c = Counter(zip(gx.tolist(), gz.tolist()))
top = c.most_common(8)
x0 = P[:, 0].min(); z0 = P[:, 1].min()
for (a, b), ntr in top:
    print('dense cell x[%.0f..%.0f] z[%.0f..%.0f]: %d verts' % (
        x0 + a * 200, x0 + a * 200 + 200, z0 + b * 200, z0 + b * 200 + 200, ntr))
