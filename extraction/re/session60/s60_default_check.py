import json, time, socket, threading, http.server, functools
PORT = 8167
WT = '/tmp/my-project/work/ghpages_staged_wt'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WT)
httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
t0 = time.time()
while time.time() - t0 < 15:
    try:
        with socket.create_connection(('127.0.0.1', PORT), timeout=1): break
    except OSError: time.sleep(0.25)
from playwright.sync_api import sync_playwright
rec = {'console_errors': [], 'page_errors': []}
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
    pg = b.new_page(viewport={'width': 960, 'height': 600})
    pg.on('console', lambda m: rec['console_errors'].append(m.text[:150]) if m.type == 'error' else None)
    pg.on('pageerror', lambda e: rec['page_errors'].append(str(e)[:150]))
    pg.goto('http://127.0.0.1:%d/playable/integration_lazy.html' % PORT)
    pg.set_input_files('#f', ZIP)
    gate = {}
    t0 = time.time()
    while time.time() - t0 < 300:
        time.sleep(0.5)
        gate = pg.evaluate('window.__GATE || {}')
        if gate.get('done'): break
    rec['gate'] = {k: gate.get(k) for k in ('done', 'pass', 'soup', 'routes')}
    b.close()
httpd.shutdown(); httpd.server_close()
rec['verdict'] = 'PASS' if (rec['gate'].get('done') and '00ce7970' in json.dumps(rec['gate'].get('soup'))
                            and not rec['console_errors'] and not rec['page_errors']) else 'FAIL'
json.dump(rec, open('/tmp/my-project/work/TDKR-Game/extraction/re/session60/s60_default_gate.json', 'w'), indent=1)
print('default:', rec['verdict'], json.dumps(rec['gate'].get('soup'))[:60], 'routes:', rec['gate'].get('routes'))
print('errors:', rec['console_errors'][:2], rec['page_errors'][:2])
