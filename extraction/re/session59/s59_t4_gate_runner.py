#!/usr/bin/env python3
"""s59 T4 gate: enemy_viewer.html behaviour slice — cone geometry, negative control
(outside cone / behind facing), alert transition, hurt->death sequence, health values."""
import json, time, socket, threading, http.server, functools, os

PORT = 8171
WT = '/tmp/my-project/work/ghpages_staged_wt'
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session59/s59_t4_gate.json'

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WT)
httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
t0 = time.time()
while time.time() - t0 < 15:
    try:
        socket.create_connection(('127.0.0.1', PORT), timeout=1).close(); break
    except OSError: time.sleep(0.25)

from playwright.sync_api import sync_playwright
rec = {'console_errors': [], 'page_errors': []}
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
    page = browser.new_page(viewport={'width': 1000, 'height': 640})
    page.on('console', lambda m: rec['console_errors'].append(m.text[:150]) if m.type == 'error' else None)
    page.on('pageerror', lambda e: rec['page_errors'].append(str(e)[:150]))
    page.goto(f'http://127.0.0.1:{PORT}/playable/enemy_viewer.html')
    page.wait_for_timeout(1500)
    gate = page.evaluate('window.__GATE || {}')
    rec['gate'] = gate
    page.screenshot(path='/tmp/my-project/scripts/s59_t4_viewer.png')
    browser.close()
httpd.shutdown(); httpd.server_close()
print('gate pass:', gate.get('pass'))
print(json.dumps(gate, indent=1)[:1500])
print('errs:', len(rec['console_errors']), len(rec['page_errors']))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(rec, open(OUT, 'w'), indent=1)
