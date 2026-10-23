#!/usr/bin/env python3
import json, time, socket, threading, http.server, functools, base64
PORT = 8155
WT = '/tmp/my-project/work/city_slice_wt'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
def wait_port(port, timeout=20):
    import time as t
    t0 = t.time()
    while t.time() - t0 < timeout:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1): return True
        except OSError: t.sleep(0.25)
    return False
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WT)
httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
wait_port(PORT)
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
    pg = b.new_page(viewport={'width':1280,'height':900})
    pg.goto('http://127.0.0.1:%d/playable/city_bisect2.html?only=other&upload=1&fix=1' % PORT)
    pg.set_input_files('#f', ZIP)
    for _ in range(120):
        time.sleep(1)
        if (pg.evaluate('window.__GATE || {}')).get('done'): break
    up = pg.evaluate('window.__UPLOAD && window.__UPLOAD()')
    for r in up['batches']:
        print(json.dumps({k: r.get(k) for k in ('mid','fx','bn0','bn1','dMiss','unit0','unit1','noTex','MM','usamp')}))
    b.close()
httpd.shutdown(); httpd.server_close()
