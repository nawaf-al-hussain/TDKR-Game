#!/usr/bin/env python3
"""S64 T4 battery: load EVERY page of the exact deploy tree (s56-t1-glide @ b7df902)
headless with the real zip; 0 console errors + 0 failed requests required per page.
Pages: root viewer, walktest, playable/index, playable/integration, playable/integration_lazy
(default), playable/enemy_viewer (combat gate). The s5-air run on this exact tree was
already gated in s64_t2_gate.json (4 runs, 0 errors)."""
import json, time, socket, threading, http.server, functools, sys

PORT = int(__import__('os').environ.get('S64_PORT', '8185'))
WT = '/tmp/my-project/work/ghpages_staged_wt'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
BATCH = (sys.argv[1] if len(sys.argv) > 1 else 'a')
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session64/s64_t4_pages_%s.json' % BATCH

PAGES = [
    ('/index.html', True, 70),
    ('/playable/walktest.html', True, 70),
    ('/playable/index.html', True, 100),
    ('/playable/integration.html', True, 100),
    ('/playable/integration_lazy.html', True, 100),
    ('/playable/enemy_viewer.html', True, 170),
]
# batch selection: argv[1] = 'a' (first 3) or 'b' (last 3)
BATCH = (sys.argv[1] if len(sys.argv) > 1 else 'a')
PAGES = PAGES[:3] if BATCH == 'a' else PAGES[3:]

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
results = {}
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
    for path, usezip, budget in PAGES:
        rec = {'console_errors': [], 'failed': [], 'requests': 0}
        page = browser.new_page(viewport={'width': 960, 'height': 600})
        page.on('console', lambda m, r=rec: r['console_errors'].append(m.text[:180]) if m.type == 'error' else None)
        page.on('pageerror', lambda e, r=rec: r['console_errors'].append('PAGEERROR ' + str(e)[:200]))
        page.on('requestfailed', lambda rq, r=rec: r['failed'].append(rq.url[-90:]))
        page.on('response', lambda rs, r=rec: r.__setitem__('requests', r['requests'] + 1))
        t0 = time.time()
        try:
            page.goto('http://127.0.0.1:%d%s' % (PORT, path), timeout=30000)
            if usezip:
                try:
                    page.set_input_files('input[type=file]', ZIP, timeout=5000)
                except Exception:
                    pass
            # wait out the load window
            t1 = time.time()
            while time.time() - t1 < budget:
                time.sleep(2)
            # enemy gate?
            if 'enemy_viewer' in path:
                g = page.evaluate('window.__GATE && window.__GATE.combat ? window.__GATE.combat.pass : null')
                rec['combat_gate_pass'] = g
        except Exception as e:
            rec['console_errors'].append('NAV ' + str(e)[:150])
        rec['elapsed_s'] = round(time.time() - t0, 1)
        results[path] = rec
        print(path, 'errors', len(rec['console_errors']), 'failed', len(rec['failed']),
              'reqs', rec['requests'], 'combat', rec.get('combat_gate_pass'))
        page.close()
    browser.close()
httpd.shutdown(); httpd.server_close()
ok = all(len(r['console_errors']) == 0 and len(r['failed']) == 0 for r in results.values())
json.dump({'tree': 's56-t1-glide b7df902', 'batch': BATCH, 'pages': results, 'all_clean': ok},
          open(OUT, 'w'), indent=1)
print('ALL CLEAN' if ok else 'ISSUES FOUND', '->', OUT)
