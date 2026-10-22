#!/usr/bin/env python3
"""s49 T5 gate: integration.html (staged branch, NOT deployed).
One user zip drives: (1) zone render w/ engine GLSL + follow camera,
(2) navmesh walker + digest-gated soup + route check vs harness,
(3) Batman from user zip. Gates: console errors, route agreement,
silhouette, motion (walk vs idle frame diff), camera travel, pixel stats."""
import json, time, socket, threading, http.server, functools

PORT = 8141
WT = '/tmp/my-project/work/ghpages_staged_wt'
PAGE = '/playable/integration.html'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session49/s49_t5_gate.json'

def wait_port(port, timeout=15):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1):
                return True
        except OSError:
            time.sleep(0.25)
    return False

def run(qs, out_path):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WT)
    httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    wait_port(PORT)
    from playwright.sync_api import sync_playwright
    verdict = {'console_errors': [], 'page_errors': []}
    gate = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
        ctx = browser.new_context(viewport={'width': 1400, 'height': 950})
        page = ctx.new_page()
        page.on('console', lambda m: verdict['console_errors'].append(m.text) if m.type == 'error' else None)
        page.on('pageerror', lambda e: verdict['page_errors'].append(str(e)))
        page.goto('http://127.0.0.1:%d%s%s' % (PORT, PAGE, qs))
        page.set_input_files('#f', ZIP)
        for _ in range(300):
            time.sleep(1)
            gate = page.evaluate('window.__GATE || {}')
            if gate.get('done'):
                break
        pglog = page.evaluate("document.querySelector('#log').textContent")
        shot = out_path.replace('.json', '.png')
        page.screenshot(path=shot)
        browser.close()
    httpd.shutdown()
    print(pglog[-2000:])
    ok = (len(verdict['console_errors']) == 0 and len(verdict['page_errors']) == 0
          and not gate.get('error'))
    checks = {
        'no_errors': ok,
        'nm_self_check': gate.get('nmSelfCheck') is True,
        'soup_digest': gate.get('soupDigestPass') is True,
        'routes_agree': bool(gate.get('routes')) and gate['routes'].get('agree') == gate['routes'].get('run') and gate['routes'].get('run', 0) >= 4,
        'batman_ok': bool(gate.get('batman')) and gate['batman'].get('ok') is True,
        'silhouette_in_range': gate.get('silhouetteInRange') is True,
        'motion_detected': gate.get('motionDetected') is True,
        'camera_followed': gate.get('cameraFollowed') is True,
    }
    gate_pass = all(checks.values())
    out = {'qs': qs, 'gate_pass': gate_pass, 'checks': checks, 'gate': gate,
           'console_errors': verdict['console_errors'][:5], 'page_errors': verdict['page_errors'][:3]}
    json.dump(out, open(out_path, 'w'), indent=1)
    print('CHECKS:', checks)
    print('GATE', 'PASS' if gate_pass else 'FAIL')
    return gate_pass

if __name__ == '__main__':
    import sys
    qs = sys.argv[1] if len(sys.argv) > 1 else ''
    outp = sys.argv[2] if len(sys.argv) > 2 else OUT
    passed = run(qs, outp)
    sys.exit(0 if passed else 1)
