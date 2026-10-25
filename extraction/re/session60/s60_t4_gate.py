#!/usr/bin/env python3
"""s60 T4 gate: enemy_viewer.html with the REAL merc loaded from the user zip.
Waits for window.__GATE.combat; validates pass + controls; screenshot receipt."""
import json, time, socket, threading, http.server, functools

PORT = 8165
WT = '/tmp/my-project/work/ghpages_staged_wt'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session60/s60_t4_gate.json'
PNG = '/tmp/my-project/work/TDKR-Game/extraction/re/session60/s60_t4_viewer.png'

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
rec = {'console_errors': [], 'page_errors': [], 'logs': []}
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
    page = browser.new_page(viewport={'width': 1000, 'height': 720})
    page.on('console', lambda m: rec['console_errors'].append(m.text[:200]) if m.type == 'error' else None)
    page.on('pageerror', lambda e: rec['page_errors'].append(str(e)[:300]))
    page.on('console', lambda m: rec['logs'].append(m.text[:200]) if ('merc' in m.text or 'IoU' in m.text) else None)
    page.goto('http://127.0.0.1:%d/playable/enemy_viewer.html' % PORT)
    page.set_input_files('#zf', ZIP)
    combat = {}
    t0 = time.time()
    while time.time() - t0 < 240:
        time.sleep(0.5)
        combat = page.evaluate('(window.__GATE||{}).combat || {}')
        if combat.get('enabled'):
            break
    rec['elapsed_s'] = round(time.time() - t0, 1)
    rec['combat'] = combat
    rec['mercStat'] = page.evaluate("document.getElementById('mercStat').textContent")
    try:
        page.screenshot(path=PNG)
        rec['screenshot'] = PNG
    except Exception as e:
        rec['screenshot'] = 'failed: %s' % e
    browser.close()
httpd.shutdown(); httpd.server_close()

c = rec['combat']
rec['verdict'] = 'PASS' if (c.get('pass') and not rec['console_errors'] and not rec['page_errors']) else 'FAIL'
json.dump(rec, open(OUT, 'w'), indent=1)
print('verdict:', rec['verdict'])
print('mercStat:', rec['mercStat'])
print('combat pass:', c.get('pass'), 'ctlFar:', (c.get('ctlFar') or {}).get('state'),
      'ctlBehind:', (c.get('ctlBehind') or {}).get('state'),
      'walk/run/walk2:', c.get('walkState'), c.get('runState'), c.get('walk2State'))
print('hp:', c.get('hpAfter5'), c.get('hpAfter10'), c.get('hpFinal'),
      'states:', c.get('stateAfter5'), c.get('stateAfterHurt'), c.get('stateAfter10'), c.get('stateFinal'))
print('wrongClipDiff:', c.get('ctlWrongClipDiff'), 'seq:', c.get('stateSeq'))
print('errors:', rec['console_errors'][:3], rec['page_errors'][:3])
