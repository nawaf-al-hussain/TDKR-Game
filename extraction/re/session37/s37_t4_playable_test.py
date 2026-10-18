#!/usr/bin/env python3
"""S37 T4.4: drive the pipeline-only playable page in headless Chromium with
the REAL release zip; verify decode + render via WebGL (SwiftShader), capture
frames, drive WASD for a few seconds, save screenshot + report."""
import json, threading, functools, http.server, time, os
from playwright.sync_api import sync_playwright

ROOT = '/tmp/my-project/work/TDKR-Game/gh-pages'
PAGE = 'http://127.0.0.1:8902/playable/pipeline.html'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session37'

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 8902), handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()

os.makedirs(OUT, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader',
                                '--js-flags=--max-old-space-size=2800'])
    pg = b.new_page(viewport={'width': 960, 'height': 640})
    pg.on('console', lambda m: print('[page]', m.text[:160]))
    pg.on('pageerror', lambda e: print('[pageerror]', str(e)[:200]))
    pg.goto(PAGE)
    pg.set_input_files('#f', ZIP)
    t0 = time.time()
    while time.time() - t0 < 420:
        txt = pg.inner_text('#log')
        if 'READY' in txt or 'ERROR' in pg.inner_text('#err'):
            break
        time.sleep(2)
    print('--- page log ---')
    print(pg.inner_text('#log'))
    err = pg.inner_text('#err').strip()
    print('--- err:', err or '(none)')
    # render + drive WASD
    pg.evaluate('window.__frames = 0; (function cnt(){ window.__frames++; requestAnimationFrame(cnt) })();')
    pg.keyboard.down('KeyW'); pg.keyboard.down('ShiftLeft')
    time.sleep(2.0)
    pg.keyboard.up('ShiftLeft')
    time.sleep(1.5)
    pg.keyboard.up('KeyW')
    time.sleep(0.5)
    frames = pg.evaluate('window.__frames')
    cur = pg.evaluate('document.querySelector("#log").textContent.includes("READY")')
    pg.screenshot(path=OUT + '/s37_t4_playable.png')
    rep = {'ready': bool(cur), 'frames_in_4s': frames, 'error': err}
    b.close()
srv.shutdown()
print('REPORT:', json.dumps(rep))
json.dump(rep, open(OUT + '/s37_t4_playable.json', 'w'), indent=1)
print('screenshot:', OUT + '/s37_t4_playable.png')
