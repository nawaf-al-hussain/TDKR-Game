#!/usr/bin/env python3
"""S61 T3 debug: dump __GATE keys + captureSkinnedFrames presence + manual invocation."""
import json, time, socket, threading, http.server, functools

PORT = 8175
WT = '/tmp/my-project/work/ghpages_staged_wt'
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

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WT)
httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
wait_port(PORT)
from playwright.sync_api import sync_playwright
rec = {'logs': [], 'errors': []}
with sync_playwright() as p:
    b = p.chromium.launch(args=['--enable-unsafe-swiftshader', '--use-gl=swiftshader',
                                '--enable-webgl', '--ignore-gpu-blocklist'])
    pg = b.new_page(viewport={'width': 960, 'height': 600})
    pg.on('console', lambda m: rec['logs'].append(m.type + ': ' + m.text[:220]))
    pg.on('pageerror', lambda e: rec['errors'].append(str(e)[:300]))
    pg.goto('http://127.0.0.1:%d/playable/integration_lazy.html?enemy=1' % PORT)
    t0 = time.time()
    keys = None
    while time.time() - t0 < 240:
        st = pg.evaluate('''() => ({
            gateKeys: window.__GATE ? Object.keys(window.__GATE) : null,
            hasFn: typeof captureSkinnedFrames,
            hasMerc: !!window.__GATE && !!window.__GATE.enemyPlay,
            iou2: window.__GATE ? (window.__GATE.enemyIoU2 ? 'present' : 'absent') : 'no-gate'
        })''')
        keys = st
        if st['iou2'] != 'absent' or (st['gateKeys'] and 'enemyPlay' in st['gateKeys']):
            break
        time.sleep(3)
    print('state:', json.dumps(keys))
    print('gate:', json.dumps(pg.evaluate('() => window.__GATE ? Object.keys(window.__GATE) : null')))
    i2 = pg.evaluate('() => window.__GATE ? window.__GATE.enemyIoU2 || null : null')
    if i2:
        print('iou2:', json.dumps({k: v for k, v in i2.items() if k != 'frames'})[:400])
        fr = i2.get('frames') or {}
        for nm, f in fr.items():
            print(' ', nm, [(x['frac'], x['lit'], x['height'], x['frameDisp']) for x in f])
    print('errors:', rec['errors'][:5])
    print('logs:', rec['logs'][:14])
    b.close()
httpd.shutdown()
