#!/usr/bin/env python3
"""s49 T4a gate: city_zone2.html (per-material batched WebGL1 zone render).
Targets: first image < 10 s, peak heap < 400 MB, corr >= 0.99 vs the s48
Python reference render on the same camera."""
import json, time, socket, threading, http.server, functools

PORT = 8139
PAGE = '/playable/city_zone2.html'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
WT = '/tmp/my-project/work/city_slice_wt'
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session49/s49_t4_gate.json'

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
print('server:', wait_port(PORT), flush=True)
from playwright.sync_api import sync_playwright
verdict = {'console_errors': [], 'page_errors': []}
gate = {}
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
    ctx = browser.new_context(viewport={'width': 1280, 'height': 900})
    page = ctx.new_page()
    page.on('console', lambda m: verdict['console_errors'].append(m.text) if m.type == 'error' else None)
    page.on('pageerror', lambda e: verdict['page_errors'].append(str(e)))
    page.goto('http://127.0.0.1:%d%s' % (PORT, PAGE))
    page.set_input_files('#f', ZIP)
    for _ in range(300):
        time.sleep(1)
        gate = page.evaluate('window.__GATE || {}')
        if gate.get('done'):
            break
    pglog = page.evaluate("document.querySelector('#log').textContent")
    browser.close()
print(pglog[-1200:])
ok = (len(verdict['console_errors']) == 0 and len(verdict['page_errors']) == 0
      and not gate.get('error'))
checks = {
    'corr>=0.99': gate.get('corr', 0) >= 0.99,
    'corr_recorded': gate.get('corr', 0),
    'first_image<10s': gate.get('first_image_ms', 1e9) < 10000,
    'heap<400MB': gate.get('heap_mb', 1e9) < 400,
    'no_errors': ok,
}
gate_pass = all(checks.values())
out = {'gate_pass': gate_pass, 'checks': checks, 'gate': gate,
       'console_errors': verdict['console_errors'][:5], 'page_errors': verdict['page_errors'][:3]}
json.dump(out, open(OUT, 'w'), indent=1)
print('CHECKS:', checks)
print('GATE', 'PASS' if gate_pass else 'FAIL')
