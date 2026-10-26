#!/usr/bin/env python3
"""S62 T3 gate: run enemy_viewer.html (skinned-mesh combat slice) with the user zip."""
import json, time, socket, threading, http.server, functools

PORT = 8177
WT = '/tmp/my-project/work/ghpages_staged_wt'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t3_gate.json'

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
rec = {'console_errors': []}
with sync_playwright() as p:
    b = p.chromium.launch(args=['--enable-unsafe-swiftshader', '--use-gl=swiftshader',
                                '--enable-webgl', '--ignore-gpu-blocklist'])
    pg = b.new_page(viewport={'width': 1100, 'height': 800})
    pg.on('console', lambda m: rec['console_errors'].append(m.text[:200]) if m.type == 'error' else None)
    pg.on('pageerror', lambda e: rec['console_errors'].append('PAGEERROR ' + str(e)[:300]))
    pg.goto('http://127.0.0.1:%d/playable/enemy_viewer.html' % PORT)
    pg.set_input_files('#zf', ZIP)
    gate = None
    t0 = time.time()
    while time.time() - t0 < 180:
        time.sleep(2)
        gate = pg.evaluate('window.__GATE && window.__GATE.combat ? window.__GATE.combat : null')
        if gate and gate.get('hpFinal') is not None:
            break
    rec['gate'] = gate
    b.close()
httpd.shutdown()
json.dump(rec, open(OUT, 'w'), indent=1)
g = gate or {}
print('errors:', len(rec['console_errors']), rec['console_errors'][:2])
print('pass:', g.get('pass'))
print('stateSeq:', g.get('stateSeq'))
print('hp:', g.get('hpAfter5'), g.get('hpAfter10'), '->', g.get('hpFinal'), g.get('stateFinal'))
print('ctl:', g.get('ctlPass'), 'wrongClip(point):', g.get('ctlWrongClipDiff'))
print('meshSil lit:', json.dumps(g.get('meshSil')))
print('meshSilDiff:', json.dumps(g.get('meshSilDiff')))
print('meshSilPass:', g.get('meshSilPass'), 'meshWrongClip:', g.get('meshWrongClipDiff'), g.get('meshWrongClipDetected'))
print('saved', OUT)
