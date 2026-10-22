#!/usr/bin/env python3
"""s50 T1 gate/runner: city_bisect.html variant runs.
usage: s50_t1_gate.py "<qs>" <out.json> [timeout_s]"""
import json, time, socket, threading, http.server, functools, sys

PORT = 8143
WT = '/tmp/my-project/work/city_slice_wt'
PAGE = '/playable/city_bisect.html'
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

def run(qs, out_path, budget=300):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WT)
    httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    wait_port(PORT)
    from playwright.sync_api import sync_playwright
    verdict = {'console_errors': [], 'page_errors': []}
    gate = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
        ctx = browser.new_context(viewport={'width': 1280, 'height': 900})
        page = ctx.new_page()
        page.on('console', lambda m: verdict['console_errors'].append(m.text) if m.type == 'error' else None)
        page.on('pageerror', lambda e: verdict['page_errors'].append(str(e)))
        page.goto('http://127.0.0.1:%d%s%s' % (PORT, PAGE, qs))
        page.set_input_files('#f', ZIP)
        t0 = time.time()
        while time.time() - t0 < budget:
            time.sleep(1)
            gate = page.evaluate('window.__GATE || {}')
            if gate.get('done'):
                break
        pglog = page.evaluate("document.querySelector('#log').textContent")
        glerr = page.evaluate('window.__GLERR || []')
        shot = out_path.replace('.json', '.png')
        try:
            page.screenshot(path=shot)
        except Exception:
            pass
        browser.close()
    httpd.shutdown()
    print(pglog[-1500:])
    ok = (len(verdict['console_errors']) == 0 and len(verdict['page_errors']) == 0
          and not gate.get('error'))
    out = {'qs': qs, 'no_errors': ok, 'gate': gate, 'glerr': glerr[:20],
           'console_errors': verdict['console_errors'][:5], 'page_errors': verdict['page_errors'][:3]}
    json.dump(out, open(out_path, 'w'), indent=1)
    print('corr:', gate.get('corr'), 'glerr:', glerr[:10] if glerr else 'none',
          'no_errors:', ok, 'first_image_ms:', gate.get('first_image_ms'))
    return out

if __name__ == '__main__':
    run(sys.argv[1] if len(sys.argv) > 1 else '',
        sys.argv[2] if len(sys.argv) > 2 else '/tmp/my-project/work/TDKR-Game/extraction/re/session50/s50_t1_gate.json',
        int(sys.argv[3]) if len(sys.argv) > 3 else 300)
