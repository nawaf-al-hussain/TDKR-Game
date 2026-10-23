#!/usr/bin/env python3
"""s53 T5 gate runner: integration_lazy.html ?s5=1 (glide+grapple slice) and default re-gate.
Acceptance: s5.targetReached true (reachDist <= 2.5 u), s5.glideClipActive true, s5.landed true
(landMs < 6000), 0 console/page errors, AND the full default gate still passes with the same
digests (soup/routes) as the s52 baseline."""
import json, time, socket, threading, http.server, functools, sys

PORT = 8147
WT = '/tmp/my-project/work/ghpages_staged_wt'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
OUTDIR = '/tmp/my-project/work/TDKR-Game/extraction/re/session53/'

def wait_port(port, timeout=15):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1):
                return True
        except OSError:
            time.sleep(0.25)
    return False

def run(qs, name, budget=460):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WT)
    httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    wait_port(PORT)
    from playwright.sync_api import sync_playwright
    rec = {'name': name, 'qs': qs, 'console_errors': [], 'page_errors': []}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
        page = browser.new_page(viewport={'width': 960, 'height': 600})
        page.on('console', lambda m: rec['console_errors'].append(m.text[:150]) if m.type == 'error' else None)
        page.on('pageerror', lambda e: rec['page_errors'].append(str(e)[:150]))
        page.goto('http://127.0.0.1:%d/playable/integration_lazy.html%s' % (PORT, qs))
        page.set_input_files('#f', ZIP)
        gate = {}
        t0 = time.time()
        for _ in range(budget // 2):
            time.sleep(2)
            gate = page.evaluate('window.__GATE || {}')
            if gate.get('done'):
                break
        rec['elapsed_s'] = round(time.time() - t0, 1)
        keep = ('done', 'pass', 'soup', 'soupDigestPass', 'routes', 'zone', 'batman',
                'first_image_ms', 'silhouetteInRange', 'motionDetected', 'cameraFollowed',
                'nmSelfCheck', 'corruptControl', 's5', 'error')
        rec['gate'] = {k: gate.get(k) for k in keep}
        browser.close()
    httpd.shutdown(); httpd.server_close()
    print(name, '-> pass:', rec['gate'].get('pass'), 's5:', json.dumps(rec['gate'].get('s5')),
          'errs:', len(rec['console_errors']), len(rec['page_errors']), flush=True)
    return rec

if __name__ == '__main__':
    import os
    os.makedirs(OUTDIR, exist_ok=True)
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    outp = OUTDIR + 's53_t5_gate.json'
    out = json.load(open(outp)) if os.path.exists(outp) else {}
    if which in ('all', 's5'):
        out['s5'] = run('?s5=1', 's5')
    if which in ('all', 'default'):
        out['default'] = run('', 'default')
    json.dump(out, open(outp, 'w'), indent=1)
    print('saved', outp)
