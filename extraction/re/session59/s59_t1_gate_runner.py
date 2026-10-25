#!/usr/bin/env python3
"""s59 T1 gate battery. Runs the staged slice (worktree s56-t1-glide @22b77bc) in the
6 s58 configs; samples per-t state WITH positions at 200 ms for the offline
wrong-model control (frozen-anchor blend vs per-frame-displacement blend)."""
import json, time, socket, threading, http.server, functools, sys, os

PORT = 8159
WT = '/tmp/my-project/work/ghpages_staged_wt'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session59/s59_t1_gate.json'

def wait_port(port, timeout=15):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1):
                return True
        except OSError:
            time.sleep(0.25)
    return False

def run(qs, name, budget=420):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WT)
    httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    wait_port(PORT)
    from playwright.sync_api import sync_playwright
    rec = {'name': name, 'qs': qs, 'console_errors': [], 'page_errors': [], 'outer_traj': []}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
        page = browser.new_page(viewport={'width': 960, 'height': 600})
        page.on('console', lambda m: rec['console_errors'].append(m.text[:150]) if m.type == 'error' else None)
        page.on('pageerror', lambda e: rec['page_errors'].append(str(e)[:150]))
        page.goto('http://127.0.0.1:%d/playable/integration_lazy.html%s' % (PORT, qs))
        page.set_input_files('#f', ZIP)
        gate = {}
        t0 = time.time()
        while time.time() - t0 < budget:
            time.sleep(0.2)
            try:
                st = page.evaluate('(() => ({ t: performance.now(),'
                                   ' phase: (typeof S5 !== "undefined") ? S5.phase : "off",'
                                   ' px: P.x, py: P.y, pz: P.z,'
                                   ' vz: (typeof S5 !== "undefined") ? S5.vz : null,'
                                   ' fwd: (typeof S5 !== "undefined" && S5.fwd != null) ? S5.fwd : null,'
                                   ' acc: (typeof S5 !== "undefined" && S5.acc != null) ? S5.acc : null,'
                                   ' pitch: (typeof S5 !== "undefined" && S5.pitch != null) ? S5.pitch : null,'
                                   ' blendD: (typeof S5 !== "undefined" && S5.blendD != null) ? S5.blendD : null,'
                                   ' blendV: (typeof S5 !== "undefined" && S5.blendV != null) ? S5.blendV : null }))()')
            except Exception:
                st = {}
            if st.get('phase') == 'glide':
                rec['outer_traj'].append(st)
            gate = page.evaluate('window.__GATE || {}')
            if gate.get('done'):
                break
        rec['elapsed_s'] = round(time.time() - t0, 1)
        keep = ('done', 'pass', 'soup', 'routes', 'zone', 'batman', 'first_image_ms',
                'nmSelfCheck', 'corruptControl', 's5', 's5live', 'error')
        rec['gate'] = {k: gate.get(k) for k in keep}
        try:
            browser.close()
        except Exception:
            pass
    httpd.shutdown(); httpd.server_close()
    s5 = rec['gate'].get('s5') or {}
    soup = rec['gate'].get('soup')
    print('%-16s pass=%s s5.model=%s landed=%s landMs=%s errs=%d/%d traj_n=%d soup=%s' % (
        name, rec['gate'].get('pass'), s5.get('model'), s5.get('landed'), s5.get('landMs'),
        len(rec['console_errors']), len(rec['page_errors']), len(rec['outer_traj']),
        (soup.get('digest') if isinstance(soup, dict) else soup)), flush=True)
    return rec

if __name__ == '__main__':
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    out = json.load(open(OUT)) if os.path.exists(OUT) else {}
    plan = [('default', '', 'default'),
            ('s5_acc_glider', '?s5=1', 's5'),
            ('s5blend_exact', '?s5=1&s5blend=1', 's5'),
            ('s5blend_plunge', '?s5=1&s5blend=1&s5plunge=1', 's5'),
            ('s5_sink_control', '?s5=1&s5sink=1', 's5'),
            ('s5_ctl', '?s5=1&s5ctl=1', 's5')]
    for key, qs, tag in plan:
        if which not in ('all', key):
            continue
        out[key] = run(qs, key)
        json.dump(out, open(OUT, 'w'), indent=1)
    print('saved', OUT)
