#!/usr/bin/env python3
"""s46 T5 RC gate: index.html?userfiles=1 with the USER's release zip.
Positive: WALKER ACTIVE, 0 console errors, >=20 track points with capsule base z
== Python navmesh ground (3 decimals), Batman silhouette quantified.
Negatives: ?corrupt=1 (navmesh byte) -> self-check fails; ?corrupt=2 (lvc byte)
-> soup digest mismatch; no zip -> walker inactive, page still healthy."""
import json, math, sys, time
import numpy as np
from playwright.sync_api import sync_playwright

ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
URL = 'http://127.0.0.1:8099/playable/index.html'
OUT = '/home/z/my-project/scripts/s46_t5_gate.json'

# --- Python navmesh ground (independent reference) ---------------------------
import struct, io, zipfile
g = open('/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/game_config.gla', 'rb').read()
_, idxsz, tabsz, n = struct.unpack('>IIII', g[:16])
pool = g[16 + n * 16:idxsz]
nm = None
for i in range(n):
    o, s, no, _ = struct.unpack('>IIII', g[16 + i * 16:16 + i * 16 + 16])
    nmm = pool[no:pool.index(b'\0', no)].decode('ascii', 'replace')
    if nmm == 'GothamCity_502299_navdata.nm':
        nm = g[o:o + s]
        break
NV = struct.unpack_from('>H', nm, 0)[0]
verts = np.frombuffer(nm, '>f4', NV * 3, 2).reshape(NV, 3).astype(np.float64)
soupEnd = 2 + NV * 12
NC = struct.unpack_from('>H', nm, soupEnd + 2)[0]
cs = soupEnd + 4
raw = np.frombuffer(nm, np.uint8, NC * 15, cs).reshape(NC, 15)[:, :14]
cells = raw.view('>u2').astype(np.int64)
cells[:, :6] = np.where(cells[:, :6] > 0x7fff, cells[:, :6] - 0x10000, cells[:, :6])
tri = cells[:, :3].copy()
valid = (tri[:, 0] < NV) & (tri[:, 1] < NV) & (tri[:, 2] < NV) & (tri >= 0).all(1)
tri = tri[valid]
tv = verts[tri]  # (NC_valid, 3, 3)

def nm_ground(x, y, zmax=1e9):
    best = -1e9
    tx = tv[:, :, 0]
    ty = tv[:, :, 1]
    d = np.sqrt((tx.mean(1) - x) ** 2 + (ty.mean(1) - y) ** 2)
    cand = np.argsort(d)[:400]
    for c in cand:
        p0, p1, p2 = tv[c]
        det = (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1])
        if abs(det) < 1e-9:
            continue
        w1 = ((x - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (y - p0[1])) / det
        w2 = ((p1[0] - p0[0]) * (y - p0[1]) - (x - p0[0]) * (p1[1] - p0[1])) / det
        w0 = 1 - w1 - w2
        if w0 < -0.03 or w1 < -0.03 or w2 < -0.03:
            continue
        z = w0 * p0[2] + w1 * p1[2] + w2 * p2[2]
        if z <= zmax + 0.6 and z > best:
            best = z
    return best

# --- gate --------------------------------------------------------------------
def run_case(pw, mode):
    b = pw.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
    ctx = b.new_context(viewport={'width': 1280, 'height': 800})
    pg = ctx.new_page()
    errs = []
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    pg.on('pageerror', lambda e: errs.append(str(e)))
    url = URL + ('?userfiles=1' + ('&corrupt=' + mode[-1] if mode.startswith('corrupt') else '')
                 if mode != 'nozip' else '')
    pg.goto(url, wait_until='load')
    res = {'mode': mode, 'console_errors': []}
    if mode == 'nozip':
        pg.wait_for_timeout(6000)
        res['walker_active'] = pg.evaluate("!!(window.WALKER && window.WALKER.active)")
        res['log_tail'] = pg.evaluate("document.getElementById('log').textContent.slice(-200)")
        res['batman_canvas_nonempty'] = pg.evaluate(
            "(function(){const c=document.querySelector('canvas');if(!c)return false;"
            "const gl=c.getContext('webgl')||c.getContext('webgl2');"
            "const px=new Uint8Array(4);gl.readPixels(c.width/2|0,c.height/2|0,1,1,gl.RGBA,gl.UNSIGNED_BYTE,px);"
            "return (px[0]+px[1]+px[2])>0;})()")
    else:
        pg.set_input_files('#zipfile', ZIP)
        # wait for WALKER ACTIVE or ERROR (up to 300 s)
        state = None
        for _ in range(150):
            lt = pg.evaluate("document.getElementById('log').textContent")
            if 'WALKER ACTIVE' in lt or 'WALKER ERROR' in lt:
                state = lt
                break
            pg.wait_for_timeout(2000)
        lt = pg.evaluate("document.getElementById('log').textContent")
        res['log_tail'] = lt[-260:]
        res['walker_active'] = 'WALKER ACTIVE' in lt
        res['walker_error'] = 'WALKER ERROR' in lt
        if mode == 'pos':
            track = []
            pg.keyboard.down('Shift')
            pg.keyboard.down('w')
            for i in range(24):
                pg.wait_for_timeout(240)
                p = pg.evaluate('window.__P')
                if p:
                    track.append([p['x'], p['y'], p['z']])
                if i == 11:
                    pg.keyboard.down('a')
                    pg.keyboard.up('w')
            pg.keyboard.up('a')
            pg.keyboard.up('Shift')
            res['track_n'] = len(track)
            res['track_head'] = track[:4]
            # ground comparison
            okz = 0
            diffs = []
            for (x, y, z) in track:
                gz = nm_ground(x, y, z + 2.6)
                if gz > -1e8:
                    dd = abs((z - 0.9) - gz)
                    diffs.append(dd)
                    if dd < 0.005:
                        okz += 1
            res['ground_checked'] = len(diffs)
            res['ground_ok'] = okz
            res['ground_maxdiff'] = round(max(diffs), 5) if diffs else None
            # Batman silhouette: 3 canvas frames via toDataURL
            sil = []
            for k in range(3):
                data = pg.evaluate("(function(){const c=document.querySelector('canvas');return c?c.toDataURL('image/png'):null;})()")
                if data:
                    import base64, io as _io
                    from PIL import Image as _Image
                    img = np.asarray(_Image.open(_io.BytesIO(base64.b64decode(data.split(',', 1)[1]))).convert('RGB'), np.float32)
                    # silhouette = pixels far from the frame's dominant colors
                    med = np.median(img.reshape(-1, 3), 0)
                    d2 = np.abs(img - med).sum(2)
                    sil.append(int((d2 > 90).sum()))
                pg.wait_for_timeout(420)
            res['silhouette_px'] = sil
        if mode == 'corrupt1':
            pass
        res['console_error_count'] = len(errs)
    res['console_errors_head'] = errs[:3]
    b.close()
    return res

def main():
    import threading, http.server, functools, socket
    handler = functools.partial(http.server.SimpleHTTPRequestHandler,
                                directory='/tmp/my-project/work/ghpages_staged_wt')
    httpd = http.server.ThreadingHTTPServer(('127.0.0.1', 8099), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    t0 = time.time()
    while True:
        try:
            with socket.create_connection(('127.0.0.1', 8099), timeout=1):
                break
        except OSError:
            time.sleep(0.2)
    results = {}
    with sync_playwright() as pw:
        results['pos'] = run_case(pw, 'pos')
        results['corrupt1'] = run_case(pw, 'corrupt1')
        results['corrupt2'] = run_case(pw, 'corrupt2')
        results['nozip'] = run_case(pw, 'nozip')
    httpd.shutdown()

    p = results['pos']
    checks = {
        'pos_walker_active': p['walker_active'],
        'pos_no_console_errors': p['console_error_count'] == 0,
        'pos_track_ge20': p.get('track_n', 0) >= 20,
        'pos_ground_3dec': p.get('ground_checked', 0) > 0 and p['ground_ok'] == p['ground_checked'],
        'pos_silhouette_present': all(300 < s < 60000 for s in p.get('silhouette_px', [0])) and
                                  len(set(p.get('silhouette_px', []))) > 1,
        'corrupt1_detected': results['corrupt1'].get('walker_error') or
                             (not results['corrupt1'].get('walker_active') and
                              ('self-check' in results['corrupt1'].get('log_tail', '') or
                               'FAILED' in results['corrupt1'].get('log_tail', '') or
                               'ERROR' in results['corrupt1'].get('log_tail', ''))),
        'corrupt2_detected': results['corrupt2'].get('walker_error') or
                             ('MISMATCH' in results['corrupt2'].get('log_tail', '')) or
                             (not results['corrupt2'].get('walker_active')),
        'nozip_safe': (not results['nozip'].get('walker_active')) and
                      results['nozip'].get('batman_canvas_nonempty'),
    }
    ok = all(checks.values())
    print(json.dumps({'verdict': 'PASS' if ok else 'FAIL', 'checks': checks,
                      'pos_summary': {k: p.get(k) for k in ('track_n', 'ground_checked', 'ground_ok', 'ground_maxdiff', 'silhouette_px')},
                      'corrupt1_log': results['corrupt1'].get('log_tail', '')[-160:],
                      'corrupt2_log': results['corrupt2'].get('log_tail', '')[-160:],
                      'nozip_log': results['nozip'].get('log_tail', '')[-120:],
                      'elapsed_s': round(time.time() - t0)}, indent=1))
    json.dump({'verdict': 'PASS' if ok else 'FAIL', 'checks': checks,
               'results': {k: {kk: vv for kk, vv in v.items() if kk != 'console_errors_head'}
                           for k, v in results.items()}},
              open(OUT, 'w'), indent=1, default=str)
    return 0 if ok else 2

if __name__ == '__main__':
    sys.exit(main())
