#!/usr/bin/env python3
"""s54 T1 gate runner: staged slice ?s5=1 (decoded engine params) vs ?s5legacy=1
(placeholders) vs default re-gate. Samples the glide trajectory (P + S5.vz) every
500 ms during the glide phase for the altitude-lost-per-metre comparison."""
import json, time, socket, threading, http.server, functools, sys, os

PORT = 8149
WT = '/tmp/my-project/work/ghpages_staged_wt'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
OUTDIR = '/tmp/my-project/work/TDKR-Game/extraction/re/session54/'

def wait_port(port, timeout=15):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1):
                return True
        except OSError:
            time.sleep(0.25)
    return False

def run(qs, name, budget=460, sample_traj=False):
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
        traj = []
        while time.time() - t0 < budget:
            time.sleep(0.5)
            if sample_traj:
                try:
                    st = page.evaluate('(() => { const s = window.__GATE || {};'
                                       ' return { phase: (typeof S5 !== "undefined") ? S5.phase : "off",'
                                       ' px: P.x, py: P.y, pz: P.z,'
                                       ' vz: (typeof S5 !== "undefined") ? S5.vz : null,'
                                       ' pitch: (typeof S5 !== "undefined") ? S5.pitch : null }); })()')
                    if st.get('phase') == 'glide':
                        traj.append(st)
                except Exception:
                    pass
            gate = page.evaluate('window.__GATE || {}')
            if gate.get('done'):
                break
        rec['elapsed_s'] = round(time.time() - t0, 1)
        rec['traj'] = traj
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
    os.makedirs(OUTDIR, exist_ok=True)
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    outp = OUTDIR + 's54_t1_gate.json'
    out = json.load(open(outp)) if os.path.exists(outp) else {}
    if which in ('all', 's5'):
        out['s5_decoded'] = run('?s5=1', 's5_decoded', sample_traj=True)
    if which in ('all', 'legacy'):
        out['s5_legacy'] = run('?s5=1&s5legacy=1', 's5_legacy', sample_traj=True)
    if which in ('all', 'default'):
        out['default'] = run('', 'default')
    json.dump(out, open(outp, 'w'), indent=1)
    print('saved', outp)
