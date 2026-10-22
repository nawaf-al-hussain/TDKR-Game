#!/usr/bin/env python3
"""s51 T1c: run GL mat73 probes (nolm / grad), save dumps, deep-compare.
Usage: s51_t1_vdiff.py <qs> <refpng> <dumpbase> <tag>
"""
import json, time, socket, threading, http.server, functools, base64, sys
import numpy as np
from PIL import Image

PORT = 8149
WT = '/tmp/my-project/work/city_slice_wt'
PAGE = "/playable/city_bisect_mip.html"
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

def run(qs, refpng, dumpbase, tag):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WT)
    httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    wait_port(PORT)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
        page = browser.new_page(viewport={'width': 1280, 'height': 900})
        errs = []
        page.on('pageerror', lambda e: errs.append(str(e)))
        page.goto('http://127.0.0.1:%d%s%s' % (PORT, PAGE, qs))
        page.set_input_files('#f', ZIP)
        gate = {}
        for _ in range(200):
            time.sleep(1)
            gate = page.evaluate('window.__GATE || {}')
            if gate.get('done'):
                break
        url = page.evaluate('window.__GLDUMP && window.__GLDUMP()')
        if url:
            open(WT + '/playable/' + dumpbase, 'wb').write(base64.b64decode(url.split(',', 1)[1]))
        else:
            print('NO DUMP. gate:', {k: gate.get(k) for k in ('done', 'error')})
            try:
                print('log:', page.evaluate("document.querySelector('#log').textContent")[-800:])
            except Exception as e:
                print('log read fail', e)
        browser.close()
    httpd.shutdown()
    gl = np.asarray(Image.open(WT + '/playable/' + dumpbase).convert('RGB'), np.float64)[::-1]
    ref = np.asarray(Image.open(WT + '/playable/' + refpng).convert('RGB'), np.float64)

    def corr(a, b):
        a = a.mean(axis=2).ravel(); b = b.mean(axis=2).ravel()
        return float(np.corrcoef(a, b)[0, 1])
    print('%s: corr %.4f  gl_mean %.3f ref_mean %.3f  pageerrs %s' % (tag, corr(gl, ref), gl.mean(), ref.mean(), errs[:2]))
    gcm = gl.mean(axis=2) > 8; rcm = ref.mean(axis=2) > 8
    both = gcm & rcm
    print('  cov GL %.2f%% ref %.2f%% IoU %.4f shared %d' % (100*gcm.mean(), 100*rcm.mean(),
          both.sum() / max(1, (gcm | rcm).sum()), both.sum()))
    if both.sum():
        a = gl.mean(axis=2)[both]; b = ref.mean(axis=2)[both]
        print('  shared: corr %.4f gl %.2f ref %.2f ratio %.2f' % (np.corrcoef(a, b)[0,1], a.mean(), b.mean(), b.mean()/max(a.mean(),1e-9)))
    np.save(WT + '/playable/' + dumpbase.replace('.png', '.npy'), gl)
    return gl, ref

if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
