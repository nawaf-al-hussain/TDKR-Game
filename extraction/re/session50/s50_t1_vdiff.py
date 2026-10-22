#!/usr/bin/env python3
"""s50 T1: run a bisect variant, save __GLDUMP, diff vs its ref PNG."""
import json, time, socket, threading, http.server, functools, base64, sys
import numpy as np
from PIL import Image

PORT = 8147
WT = '/tmp/my-project/work/city_slice_wt'
PAGE = '/playable/city_bisect.html'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'

def wait_port(port, timeout=15):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1):
                return True
        except OSError:
            time.sleep(0.25)
    return False

def run_and_diff(qs, refpng, dumppng, tag):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WT)
    httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    wait_port(PORT)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
        page = browser.new_page(viewport={'width': 1280, 'height': 900})
        page.goto('http://127.0.0.1:%d%s%s' % (PORT, PAGE, qs))
        page.set_input_files('#f', ZIP)
        for _ in range(200):
            time.sleep(1)
            g = page.evaluate('window.__GATE || {}')
            if g.get('done'):
                break
        url = page.evaluate('window.__GLDUMP && window.__GLDUMP()')
        if url:
            open(dumppng, 'wb').write(base64.b64decode(url.split(',', 1)[1]))
        browser.close()
    httpd.shutdown()
    gl = np.asarray(Image.open(dumppng).convert('RGB'), np.float64)[::-1]  # undo display flip
    ref = np.asarray(Image.open(WT + '/playable/' + refpng).convert('RGB'), np.float64)
    def corr(a, b):
        a = a.mean(axis=2).ravel(); b = b.mean(axis=2).ravel()
        return float(np.corrcoef(a, b)[0, 1])
    print('%s: corr %.4f  gl_mean %.3f ref_mean %.3f' % (tag, corr(gl, ref), gl.mean(), ref.mean()))
    gcm = gl.mean(axis=2) > 8; rcm = ref.mean(axis=2) > 8
    onlyref = rcm & ~gcm; onlygl = gcm & ~rcm
    print('  cov GL %.2f%% ref %.2f%% IoU %.4f  gl-only %d ref-only %d' % (
        100*gcm.mean(), 100*rcm.mean(), (gcm & rcm).sum() / max(1,(gcm | rcm).sum()), onlygl.sum(), onlyref.sum()))
    Image.fromarray((onlyref * 255).astype(np.uint8)).save(WT + '/playable/s50_x_refonly_' + tag + '.png')
    Image.fromarray((onlygl * 255).astype(np.uint8)).save(WT + '/playable/s50_x_glonly_' + tag + '.png')
    d = np.abs(gl.mean(axis=2) - ref.mean(axis=2))
    Image.fromarray(np.clip(d * 4, 0, 255).astype(np.uint8)).save(WT + '/playable/s50_x_absdiff_' + tag + '.png')
    rows = onlyref.mean(axis=1); cols = onlyref.mean(axis=0)
    print('  ref-only rows:', np.round([rows[i*60:(i+1)*60].mean() for i in range(10)], 3))
    print('  ref-only cols:', np.round([cols[i*102:(i+1)*102].mean() for i in range(10)], 3))

if __name__ == '__main__':
    run_and_diff(sys.argv[1], sys.argv[2], WT + '/playable/' + sys.argv[3], sys.argv[4])
