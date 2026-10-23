#!/usr/bin/env python3
"""s53 T4: memory/first-image A/B on integration_lazy.html.
Runs: (1) default baseline, (2) ?poolchunk=1 (chunked capture->decode->GL upload->discard CPU;
the ~100 MB compressed pool + 64 MB decoded LRU are never materialized), (3) ?lrumb=16 (LRU cap
halved+ in default mode, isolates the LRU contribution).
Metrics: renderer RSS peak + timeline (ps poller), JS heap peak, first_image_ms, gate pass,
digest fields (soup/routes), texDecoded/texMiss, texPool mode.
Sign conventions: RSS peak lower = better; first image lower = better; gate pass must stay True;
digests identical to baseline required for acceptance."""
import json, time, socket, threading, http.server, functools, subprocess, sys

PORT = 8146
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

def rss_of_chromium():
    try:
        out2 = subprocess.run(['ps', '-eo', 'rss=,args='], capture_output=True, text=True).stdout
        vals = []
        rend = 0
        for l in out2.splitlines():
            low = l.lower()
            if ('chrome-headless-shell' in low or 'chrome' in low) and 'ps -eo' not in low and '/ps' not in low:
                try:
                    kb = int(l.strip().split()[0])
                    vals.append(kb)
                    if '--type=renderer' in l:
                        rend = max(rend, kb)
                except Exception:
                    pass
        return sum(vals) / 1024.0, rend / 1024.0
    except Exception:
        return 0.0, 0.0

def run_cfg(name, qs, budget=460):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WT)
    httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    wait_port(PORT)
    from playwright.sync_api import sync_playwright
    rec = {'name': name, 'qs': qs, 'console_errors': [], 'page_errors': [],
           'rss_renderer_samples': [], 'rss_tree_samples': [], 't': []}
    stop = [False]
    def poll():
        while not stop[0]:
            tot, rend = rss_of_chromium()
            rec['rss_renderer_samples'].append(round(rend, 1))
            rec['rss_tree_samples'].append(round(tot, 1))
            rec['t'].append(round(time.time(), 1))
            time.sleep(0.3)
    threading.Thread(target=poll, daemon=True).start()
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
        rec['gate'] = {k: gate.get(k) for k in
                       ('done', 'pass', 'soup', 'soupDigestPass', 'routes', 'zone', 'batman',
                        'first_image_ms', 'silhouetteInRange', 'motionDetected', 'cameraFollowed',
                        'nmSelfCheck', 'corruptControl', 'pixelStats', 'camera', 'error')}
        rec['heap_mb_peak'] = gate.get('heap_mb_peak')
        rec['texPool'] = page.evaluate('window.__TEXPOOL || null')
        browser.close()
    stop[0] = True
    time.sleep(0.5)
    rec['rss_renderer_peak'] = max(rec['rss_renderer_samples']) if rec['rss_renderer_samples'] else None
    rec['rss_tree_peak'] = max(rec['rss_tree_samples']) if rec['rss_tree_samples'] else None
    rec['rss_renderer_end'] = rec['rss_renderer_samples'][-1] if rec['rss_renderer_samples'] else None
    httpd.shutdown(); httpd.server_close()
    print('%s: rend_peak=%s MB tree_peak=%s MB first_image=%s pass=%s elapsed=%s' % (
        name, rec['rss_renderer_peak'], rec['rss_tree_peak'],
        rec['gate'].get('first_image_ms'), rec['gate'].get('pass'), rec['elapsed_s']), flush=True)
    return rec

if __name__ == '__main__':
    import os, sys
    os.makedirs(OUTDIR, exist_ok=True)
    OUTJ = OUTDIR + 's53_t4_mem.json'
    CFGS = [('default', ''), ('poolchunk', '?poolchunk=1'), ('lrumb16', '?lrumb=16')]
    if len(sys.argv) > 1:   # single-config mode: s53_t4_mem.py <idx>
        i = int(sys.argv[1]); name, qs = CFGS[i]
        rec = run_cfg(name, qs)
        out = json.load(open(OUTJ)) if os.path.exists(OUTJ) else {'sign_convention': 'renderer RSS peak (ps, MB) lower=better; gate pass must hold; digests vs baseline'}
        out[name] = rec
        json.dump(out, open(OUTJ, 'w'), indent=1)
        print('saved', OUTJ)
    else:
        out = {'sign_convention': 'renderer RSS peak (ps, MB) lower=better; gate pass must hold; digests vs baseline'}
        for name, qs in CFGS:
            out[name] = run_cfg(name, qs)
            json.dump(out, open(OUTJ, 'w'), indent=1)
        print('saved', OUTJ)
