#!/usr/bin/env python3
"""s50 T1: compare the decoded gothamcity_roads_details.tga between the page
(JS ETC1 path, as uploaded to GL) and Python (cleanroom). Fetch via __TEX73DUMP."""
import json, time, socket, threading, http.server, functools
import struct, io, zipfile
import numpy as np
import importlib.util

spec = importlib.util.spec_from_file_location(
    'cr', '/tmp/my-project/work/TDKR-Game/extraction/re/session42/s42_t2_cleanroom.py')
cr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cr)

PORT = 8153
WT = '/tmp/my-project/work/city_slice_wt'

# inject the texture dump into the page (one-off, direct page patch)
pgp = WT + '/playable/city_bisect.html'
s = open(pgp).read()
if '__TEX73DUMP' not in s:
    old = "    if (mid === 73) { window.__UV73"
    new = ("    if (mid === 73) { const __t73 = texZget(bind[73][0], false);"
           " if (__t73) { const __n = Math.min(64, __t73.w * __t73.h) * 4;"
           " window.__TEX73DUMP = { w: __t73.w, h: __t73.h, name: bind[73][0],"
           " px: Array.from(new Uint8Array(__t73.tx ? [0] : [0])) };"
           " const __gl = G.createTexture(); }  window.__UV73")
    # simpler: capture from the decoded cache (getTex returns rgba data)
    new = ("    if (mid === 73) { const __t73 = getTex(texGla, bind[73][0], false);"
           " if (__t73) { window.__TEX73DUMP = { w: __t73.w, h: __t73.h, name: bind[73][0],"
           " first: Array.from(__t73.data.slice(0, 64)),"
           " midpx: Array.from(__t73.data.slice((__t73.h >> 1) * __t73.w * 4, (__t73.h >> 1) * __t73.w * 4 + 64)) }; } }"
           "\n    if (mid === 73) { window.__UV73")
    assert old in s, 'uv73 anchor'
    s = s.replace(old, new, 1)
    open(pgp, 'w').write(s)
    print('page patched with __TEX73DUMP')

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
    tex = pg.evaluate('window.__TEX73DUMP')
    b.close()
httpd.shutdown()
print('GL-side texture:', tex['name'], tex['w'], 'x', tex['h'])
print('GL first px:', tex['first'][:16])
print('GL midrow px:', tex['midpx'][:16])

# Python side
TEXGLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/textures/l_gothamcity_tex.gla'
tg = open(TEXGLA, 'rb').read()
_, idxsz2, tabsz2, n2 = struct.unpack('>IIII', tg[:16])
pool2 = tg[16 + n2 * 16:idxsz2]

def tex_member(want):
    for i in range(n2):
        o, s2, no, _ = struct.unpack('>IIII', tg[16 + i * 16:16 + i * 16 + 16])
        nm2 = pool2[no:pool2.index(b'\0', no)].decode('ascii', 'replace')
        if nm2.lower() == want.lower():
            return tg[o:o + s2]
    return None

def unwrap_split(u8):
    if bytes(u8[:4]) != b'PK\x03\x04':
        return {'rgb': u8}
    out = {}; pos = 0
    while pos + 30 <= len(u8) and bytes(u8[pos:pos + 4]) == b'PK\x03\x04':
        csz = struct.unpack_from('<I', u8, pos + 18)[0]
        nlen = struct.unpack_from('<H', u8, pos + 26)[0]
        elen = struct.unpack_from('<H', u8, pos + 28)[0]
        nm = u8[pos + 30:pos + 30 + nlen].decode('latin1')
        dstart = pos + 30 + nlen + elen
        if nm.strip() != 'SPLIT':
            out[nm] = u8[dstart:dstart + csz]
        pos = dstart + csz
    return out

tu = tex_member(tex['name'])
parts = unwrap_split(tu)
pvr = parts['rgb.pvr'] if 'rgb.pvr' in parts else parts['rgb']
th_, tw = struct.unpack_from('<II', pvr, 4)
print('PY-side tex %dx%d, container magic %r, fmt bytes %r' % (
    tw, th_, bytes(pvr[44:48]), bytes(pvr[48:52]).hex()))
bw, bh = (tw + 3) // 4, (th_ + 3) // 4
rgb = cr.decode_etc1_cleanroom(np.frombuffer(pvr, np.uint8, bw * bh * 8, 52), tw, th_)
flat = rgb.reshape(-1, rgb.shape[-1])
print('PY first px:', [int(v) for v in flat[:16, :4].ravel()[:16]])
midrow = (th_ // 2) * tw
print('PY midrow px:', [int(v) for v in flat[midrow:midrow + 16, :4].ravel()[:16]])
json.dump({'gl': tex, 'py_wh': [int(tw), int(th_)]},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session50/s50_tex73_cmp.json', 'w'), indent=1)
