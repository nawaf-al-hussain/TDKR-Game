#!/usr/bin/env python3
"""s50 T1: fetch window.__UV73/__POS73/__SEG73NV from the page and compare against
the Python-side bake for the same material batch (same seg order, same formulas)."""
import json, time, socket, threading, http.server, functools
import struct, io, zipfile
import numpy as np

PORT = 8151
WT = '/tmp/my-project/work/city_slice_wt'
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session50/s50_uv73_cmp.json'

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WT)
httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
time.sleep(0.5)
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
    pg = b.new_page()
    pg.goto('http://127.0.0.1:%d/playable/city_bisect.html?probe=1&skipmiss=1&mat=73' % PORT)
    pg.set_input_files('#f', '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')
    for _ in range(120):
        time.sleep(1)
        g = pg.evaluate('window.__GATE || {}')
        if g.get('done'):
            break
    uv = pg.evaluate('window.__UV73')
    pos = pg.evaluate('window.__POS73')
    nvs = pg.evaluate('window.__SEG73NV')
    b.close()
httpd.shutdown()
print('GL uv73[:24]:', [round(v, 5) for v in uv[:24]])
print('GL pos73[:16]:', [round(v, 3) for v in pos[:16]])
print('GL seg73 nv[:8]:', nvs[:8])

# Python-side bake, same order (byMat insertion = k order)
GLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla'
g = open(GLA, 'rb').read()
_, idxsz, tabsz, n = struct.unpack('>IIII', g[:16])
pool = g[16 + n * 16:idxsz]
for i in range(n):
    o, s, no, _ = struct.unpack('>IIII', g[16 + i * 16:16 + i * 16 + 16])
    nm = pool[no:pool.index(b'\0', no)].decode('ascii', 'replace')
    if nm == 'GothamCity.zip':
        Z = zipfile.ZipFile(io.BytesIO(g[o:o + s]))
        ld = Z.read('lod_data.bin'); lt = Z.read('lod_table.bin'); bi = Z.read('batch_info.bin')
        break
u = struct.unpack(f'<{len(lt)//4}I', lt)
pairs = [(u[1 + 2 * k], u[2 + 2 * k]) for k in range(u[0])]
bstride, = struct.unpack_from('<I', bi, 0)
recs = np.frombuffer(bi[4:], np.uint8).reshape((len(bi) - 4) // bstride, bstride)
VAVT = [1, 1, 2, 2, 4, 4, 4]

def decl_of(mid):
    r = recs[mid]
    N = int(r[33]); ds = []; start = 0
    for j in range(N):
        d = bytes(r[40 + j * 12: 40 + (j + 1) * 12])
        A, B, C, st, off, pad = struct.unpack('>6H', d)
        size = 3 if B == 0 else B * VAVT[C]
        end = st if off == 0 else off
        ds.append((A, start, end, size)); start = end
    return ds

uv73 = []; pos73 = []; nvlist = []
for k, (off2, cnt) in enumerate(pairs):
    hdr = struct.unpack_from('<17I', ld, off2)
    mid = hdr[10]
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2 + 68)
    ds = decl_of(mid)
    stride = ds[-1][2]
    nv = vb // stride
    if mid != 73 or nv <= 0 or vb % stride != 0 or ib < 6:
        continue
    if not any(d[0] == 1 for d in ds):
        continue
    d0 = [d for d in ds if d[0] == 1][0]
    raw = np.frombuffer(ld, np.uint8, vb, data_off + 4).reshape(nv, stride)
    uv = raw[:, d0[1]:d0[1] + 4].copy().view('<i2').reshape(nv, 2).astype(np.float64)
    uvu = uv[:, 0] / 32767.0 * 0.5 + 0.5
    uvv = 1.0 - (uv[:, 1] / 32767.0 * 0.5 + 0.5)
    p3 = raw[:, 0:12].copy().view('<f4').reshape(nv, 3)
    uv73.extend([(a, b2) for a, b2 in zip(uvu[:8], uvv[:8])])
    pos73.extend([(p3[j, 0], p3[j, 1], p3[j, 2]) for j in range(min(4, nv))])
    nvlist.append(nv)
    if len(uv73) >= 24 and len(nvlist) >= 3:
        break
print('PY seg nv[:8]:', nvlist[:8])
print('PY uv73[:24]:', [(round(a, 5), round(b2, 5)) for a, b2 in uv73[:12]])
print('PY pos73[:12]:', [(round(a, 3), round(b2, 3), round(c, 3)) for a, b2, c in pos73[:6]])
out = {'gl_uv': uv, 'gl_pos': pos, 'gl_nvs': nvs, 'py_uv': uv73[:24], 'py_pos': pos73[:12], 'py_nvs': nvlist[:8]}
json.dump(out, open(OUT, 'w'), indent=1)
print('saved', OUT)
