#!/usr/bin/env python3
"""s50 T1: run the painter variant, save window.__GLDUMP() as PNG, diff vs flat ref."""
import json, time, socket, threading, http.server, functools, base64

PORT = 8145
WT = '/tmp/my-project/work/city_slice_wt'
PAGE = '/playable/city_bisect.html'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
QS = '?painter=1&ref=s50_ref_flat.png'
DUMP = '/tmp/my-project/work/city_slice_wt/playable/s50_g3_dump.png'

def wait_port(port, timeout=15):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1):
                return True
        except OSError:
            time.sleep(0.25)
    return False

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WT)
httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
wait_port(PORT)
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
    page = browser.new_page(viewport={'width': 1280, 'height': 900})
    page.goto('http://127.0.0.1:%d%s%s' % (PORT, PAGE, QS))
    page.set_input_files('#f', ZIP)
    for _ in range(200):
        time.sleep(1)
        g = page.evaluate('window.__GATE || {}')
        if g.get('done'):
            break
    print('GATE:', json.dumps(g)[:400])
    print('LOG:', page.evaluate("document.querySelector('#log').textContent")[-500:])
    url = page.evaluate('window.__GLDUMP && window.__GLDUMP()')
    if url:
        b64 = url.split(',', 1)[1]
        open(DUMP, 'wb').write(base64.b64decode(b64))
        print('dump saved', DUMP)
    browser.close()
httpd.shutdown()

import numpy as np
from PIL import Image
gl = np.asarray(Image.open(DUMP).convert('RGB'), np.float64)
ref = np.asarray(Image.open(WT + '/playable/s50_ref_flat.png').convert('RGB'), np.float64)
gcm = gl.mean(axis=2) > 60      # covered (gray 128)
rcm = ref.mean(axis=2) > 60
inter = (gcm & rcm).sum(); union = (gcm | rcm).sum()
print('coverage: GL %.2f%%  ref %.2f%%  IoU %.4f' % (100*gcm.mean(), 100*rcm.mean(), inter/union))
onlygl = gcm & ~rcm; onlyref = rcm & ~gcm
print('GL-only px %d, ref-only px %d' % (onlygl.sum(), onlyref.sum()))
Image.fromarray(((onlyref) * 255).astype(np.uint8)).save(WT + '/playable/s50_diff_refonly.png')
Image.fromarray(((onlygl) * 255).astype(np.uint8)).save(WT + '/playable/s50_diff_glonly.png')
Image.fromarray((np.clip(ref.mean(axis=2)/2,0,127) + gcm*100).astype(np.uint8)).save(WT + '/playable/s50_overlay.png')
# where are ref-only pixels? column/row profiles
rows = onlyref.mean(axis=1); cols = onlyref.mean(axis=0)
print('ref-only row profile (10 bins):', np.round([rows[i*60:(i+1)*60].mean() for i in range(10)], 3))
print('ref-only col profile (10 bins):', np.round([cols[i*102:(i+1)*102].mean() for i in range(10)], 3))
