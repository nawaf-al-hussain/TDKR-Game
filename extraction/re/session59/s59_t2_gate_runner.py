#!/usr/bin/env python3
"""s59 T2 gate: default digest + ?enemy=1 (merc mesh + 3 enemy clips + displacement
gate + wrong-clip control). Serves the patched worktree (s56-t1-glide + T2 patches)."""
import json, time, socket, threading, http.server, functools, os

PORT = 8163
WT = '/tmp/my-project/work/ghpages_staged_wt'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session59/s59_t2_gate.json'

def wait_port(port, timeout=15):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1):
                return True
        except OSError:
            time.sleep(0.25)
    return False

def run(qs, name, budget=300):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WT)
    httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    wait_port(PORT)
    from playwright.sync_api import sync_playwright
    rec = {'name': name, 'qs': qs, 'console_errors': [], 'page_errors': [], 'logs': []}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
        page = browser.new_page(viewport={'width': 960, 'height': 600})
        page.on('console', lambda m: rec['console_errors'].append(m.text[:200]) if m.type == 'error' else None)
        page.on('pageerror', lambda e: rec['page_errors'].append(str(e)[:200]))
        page.on('console', lambda m: rec['logs'].append(m.text[:300]) if 'enemy' in m.text or 'merc' in m.text else None)
        page.goto('http://127.0.0.1:%d/playable/integration_lazy.html%s' % (PORT, qs))
        page.set_input_files('#f', ZIP)
        gate = {}
        t0 = time.time()
        while time.time() - t0 < budget:
            time.sleep(0.5)
            gate = page.evaluate('window.__GATE || {}')
            if gate.get('enemyPlay') and (gate['enemyPlay'].get('reported') or gate['enemyPlay'].get('dispIdle') is not None):
                break
            if gate.get('done') and 'enemy=1' not in qs:
                break
        rec['elapsed_s'] = round(time.time() - t0, 1)
        keep = ('done', 'pass', 'soup', 'routes', 'zone', 'batman', 'first_image_ms', 'enemy', 'enemyPlay', 'error')
        rec['gate'] = {k: gate.get(k) for k in keep}
        try: browser.close()
        except Exception: pass
    httpd.shutdown(); httpd.server_close()
    print(name, '->', json.dumps(rec['gate'])[:600], 'errs', len(rec['console_errors']), len(rec['page_errors']), flush=True)
    return rec

if __name__ == '__main__':
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    out = {}
    for key, qs in [('default', ''), ('enemy', '?enemy=1')]:
        out[key] = run(qs, key)
        json.dump(out, open(OUT, 'w'), indent=1)
    print('saved', OUT)
