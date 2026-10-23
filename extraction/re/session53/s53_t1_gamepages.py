#!/usr/bin/env python3
"""s53 T1 game-page unit audit runner: integration.html / integration_lazy.html ?unitaudit=1.
Reads window.__GATE.unit_audit after the gate finishes. Also runs ?corrupt=1 NOT needed here.
Sign convention: mismatches > 0 FAILS (expected 0); noTex counted separately."""
import json, time, socket, threading, http.server, functools, sys

PORT = 8154
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

def run_page(pagefile, out_path, budget=520):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WT)
    httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    wait_port(PORT)
    from playwright.sync_api import sync_playwright
    verdict = {'page': pagefile, 'console_errors': [], 'page_errors': []}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
        page = browser.new_page(viewport={'width': 960, 'height': 600})
        page.on('console', lambda m: verdict['console_errors'].append(m.text[:200]) if m.type == 'error' else None)
        page.on('pageerror', lambda e: verdict['page_errors'].append(str(e)[:200]))
        page.goto('http://127.0.0.1:%d/playable/%s?unitaudit=1' % (PORT, pagefile))
        page.set_input_files('#f', ZIP)
        gate = {}
        t0 = time.time()
        for _ in range(budget):
            time.sleep(2)
            gate = page.evaluate('window.__GATE || {}')
            if gate.get('done'):
                break
        verdict['elapsed_s'] = round(time.time() - t0, 1)
        verdict['gate_done'] = bool(gate.get('done'))
        verdict['gate_error'] = gate.get('error')
        verdict['unit_audit'] = gate.get('unit_audit')
        # grab a couple of stable gate fields for context
        verdict['gate_keys'] = [k for k in gate.keys() if k not in ('heapSamples',)]
        browser.close()
    httpd.shutdown(); httpd.server_close()
    json.dump(verdict, open(out_path, 'w'), indent=1)
    print(pagefile, '->', json.dumps(verdict.get('unit_audit')), 'done=', verdict['gate_done'],
          'errs=', len(verdict['console_errors']), len(verdict['page_errors']), flush=True)
    return verdict

if __name__ == '__main__':
    import os
    os.makedirs(OUTDIR, exist_ok=True)
    res = {}
    res['integration'] = run_page('integration.html', OUTDIR + 's53_t1_game_integration.json')
    res['integration_lazy'] = run_page('integration_lazy.html', OUTDIR + 's53_t1_game_integration_lazy.json')
    json.dump(res, open(OUTDIR + 's53_t1_gamepages.json', 'w'), indent=1)
    print('saved', OUTDIR + 's53_t1_gamepages.json')
