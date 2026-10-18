#!/usr/bin/env python3
"""S37 T4: run tdkr_pipeline.js in headless Chromium from a File input of the
real 895 MB release zip; report stage timings, JS heap, and 921-clip parity
vs the node reference."""
import json, threading, functools, http.server, time
from playwright.sync_api import sync_playwright

ROOT = '/tmp/my-project/work/TDKR-Game/extraction/re'
PAGE = 'http://127.0.0.1:8901/session37/browser/pipeline_page.html'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 8901), handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()

with sync_playwright() as p:
    b = p.chromium.launch(args=['--js-flags=--max-old-space-size=2800'])
    pg = b.new_page()
    pg.goto(PAGE)
    pg.set_input_files('#f', ZIP)
    t0 = time.time()
    while time.time() - t0 < 420:
        if pg.evaluate('window.REPORT.done'):
            break
        time.sleep(2)
    rep = pg.evaluate('window.REPORT')
    b.close()
srv.shutdown()
print(json.dumps(rep, indent=1)[:2600])
json.dump(rep, open('/tmp/my-project/work/TDKR-Game/extraction/re/session37/s37_t4_browser.json', 'w'), indent=1)
print('saved s37_t4_browser.json')
