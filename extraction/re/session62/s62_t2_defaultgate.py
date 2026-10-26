#!/usr/bin/env python3
"""S62 T2 gate: default page (no ?enemy=1) — soup digest unchanged + 0 errors.
Proves the s62 skinning patches did not touch the default/Batman path."""
import json, time, socket, threading, http.server, functools

PORT = 8176
WT = '/tmp/my-project/work/ghpages_staged_wt'
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t2_defaultgate.json'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WT)
httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
t0 = time.time()
while time.time() - t0 < 15:
    try:
        with socket.create_connection(('127.0.0.1', PORT), timeout=1):
            break
    except OSError:
        time.sleep(0.25)
from playwright.sync_api import sync_playwright
rec = {'console_errors': [], 'logs': []}
with sync_playwright() as p:
    b = p.chromium.launch(args=['--enable-unsafe-swiftshader', '--use-gl=swiftshader',
                                '--enable-webgl', '--ignore-gpu-blocklist'])
    pg = b.new_page(viewport={'width': 960, 'height': 600})
    pg.on('console', lambda m: rec['console_errors'].append(m.text[:200]) if m.type == 'error' else
          (rec['logs'].append(m.text[:200]) if 'soup' in m.text.lower() or 'digest' in m.text.lower() else None))
    pg.on('pageerror', lambda e: rec['console_errors'].append('PAGEERROR ' + str(e)[:200]))
    pg.goto('http://127.0.0.1:%d/playable/integration_lazy.html' % PORT)
    if pg.query_selector('input[type=file]'):
        pg.set_input_files('input[type=file]', ZIP)
    # wait for the walker/soup digest
    digest = None
    t0 = time.time()
    while time.time() - t0 < 90:
        time.sleep(1)
        s = pg.evaluate('window.__GATE && window.__GATE.soup ? 1 : 0')
        if s:
            digest = pg.evaluate('window.__GATE.soup')
            break
    rec['digest'] = digest
    b.close()
httpd.shutdown()
json.dump(rec, open(OUT, 'w'), indent=1)
print('errors:', len(rec['console_errors']))
print('digest:', rec['digest'])
print('expected: 00ce7970e45adc85.../137893')
