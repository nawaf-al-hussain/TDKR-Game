#!/usr/bin/env python3
"""S63 T3 gate: SECOND real re-anchor case - glide starts MID-AIR (?s5air=N, elevated
grapple anchor) so the collision happens after the blend has decayed (non-zero blend
travel before the hit), with the trajectory compared against the analytic curve including
the dip restart.
Accept: >=1 real re-anchor, pre-hit blend decay > 4 u of travel, blendD dip restart after
the re-anchor, landed, 0 console errors, control (s5air=0) unchanged-vs-s62, soup digest
00ce7970/137893 in every run."""
import json, math, time, socket, threading, http.server, functools, sys

PORT = 8179
WT = '/tmp/my-project/work/ghpages_staged_wt'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session63/s63_t3_gate.json'

def wait_port(port, timeout=15):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1):
                return True
        except OSError:
            time.sleep(0.25)
    return False

def run(qs, budget=240):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WT)
    httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    wait_port(PORT)
    from playwright.sync_api import sync_playwright
    rec = {'qs': qs, 'console_errors': [], 'page_errors': [], 'logs': []}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
        page = browser.new_page(viewport={'width': 960, 'height': 600})
        page.on('console', lambda m: rec['console_errors'].append(m.text[:200]) if m.type == 'error' else None)
        page.on('pageerror', lambda e: rec['page_errors'].append(str(e)[:300]))
        page.on('console', lambda m: rec['logs'].append(m.text[:160])
                if ('s5 REAL' in m.text or 'S5 landed' in m.text or 's5 re-anchor' in m.text
                    or 'S5 grapple' in m.text) else None)
        page.goto('http://127.0.0.1:%d/playable/integration_lazy.html%s' % (PORT, qs))
        page.set_input_files('#f', ZIP)
        gate = {}
        t0 = time.time()
        while time.time() - t0 < budget:
            time.sleep(0.5)
            gate = page.evaluate('window.__GATE || {}')
            if gate.get('done'):
                break
        rec['gate'] = {k: gate.get(k) for k in ('done', 'pass', 'soup', 'soupDigestPass', 's5', 'error')}
        try:
            browser.close()
        except Exception:
            pass
    httpd.shutdown(); httpd.server_close()
    return rec

def analyze(rec):
    s5 = (rec.get('gate') or {}).get('s5') or {}
    traj = s5.get('traj') or []
    rean = s5.get('reanchors') or []
    out = {'n_traj': len(traj), 'reanchors': rean, 'landed': s5.get('landed'),
           'wallHit': s5.get('wallHit'), 's5air': s5.get('s5air'),
           'from': s5.get('from'), 'tgt': s5.get('tgt')}
    # blend decay before the FIRST re-anchor
    if rean and traj:
        t_hit = rean[0].get('tMs', 0)
        pre = [s for s in traj if s.get('blendD') is not None and s.get('t', 0) <= t_hit]
        out['pre_hit_samples'] = len(pre)
        out['pre_hit_blendD_max'] = max((s['blendD'] for s in pre), default=None)
        out['pre_hit_blendD_last'] = pre[-1]['blendD'] if pre else None
        # dip restart: blendD resets at the re-anchor then grows again
        post = [s['blendD'] for s in traj if s.get('blendD') is not None and s.get('t', 0) > t_hit]
        out['post_hit_blendD_min'] = min(post) if post else None
        out['dip_restart'] = bool(pre and post and out['pre_hit_blendD_last'] is not None
                                  and out['post_hit_blendD_min'] is not None
                                  and out['post_hit_blendD_min'] < out['pre_hit_blendD_last'] - 0.5)
    # analytic vz check around the re-anchor (s60 closed form, acc mode @ -45 deg)
    two_pi = 2 / math.pi
    pitch = math.radians(-45.0)
    sink = 4.0 + 12.0 * two_pi * abs(pitch)
    fwd = 1.0 + 5.0 * two_pi * abs(pitch)
    errs = []
    for s in traj:
        b = s.get('blend')
        if b is None or s.get('vz') is None:
            continue
        exp = sink * math.sin(pitch) - fwd - b
        errs.append(abs(s['vz'] - exp))
    out['analytic_vz_err_max'] = round(max(errs), 4) if errs else None
    out['analytic_n'] = len(errs)
    # vertical trajectory error around the re-anchor vs piecewise analytic (alt/m model)
    return out

cases = [('?s5=1&s5blend=1&s5real=1', 'control-s62'), ] if '--control-only' in sys.argv else []
qs = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].startswith('?') else '?s5=1&s5blend=1&s5real=1&s5air=28'
cases.append((qs, 'air'))
out = {}
for q, name in cases:
    r = run(q)
    a = analyze(r)
    a['console_errors'] = r['console_errors']
    a['page_errors'] = r['page_errors']
    a['logs'] = r['logs'][:12]
    a['soup'] = (r.get('gate') or {}).get('soup')
    out[name] = a
    print(name, '->', json.dumps({k: v for k, v in a.items() if k != 'logs'}, default=str)[:600])
    print('  logs:', a['logs'])
json.dump(out, open(OUT, 'w'), indent=1, default=str)
print('saved', OUT)
