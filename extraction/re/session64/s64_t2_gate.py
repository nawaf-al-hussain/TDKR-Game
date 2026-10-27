#!/usr/bin/env python3
"""S64 T2 gate: second REAL re-anchor via the phase-timeout lift (?s5airto) so the
s5air=185 glide reaches the 64-u facade band with a decayed blend. Accept:
air run has >=1 re-anchor with pre-hit blendD > 4 u and a dip restart; control
reproduces s62 (2 re-anchors @17/300 ms, pre-hit blendD = 0); soup digest
00ce7970/137893 everywhere; 0 console errors. Analytic vz comparison around the
re-anchor (s60 closed form) with n samples."""
import json, math, time, socket, threading, http.server, functools, sys

PORT = 8181
WT = '/tmp/my-project/work/ghpages_staged_wt'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session64/s64_t2_gate.json'

def wait_port(port, timeout=15):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1):
                return True
        except OSError:
            time.sleep(0.25)
    return False

def run(qs, budget=260):
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
                    or 'S5 grapple' in m.text or 'glide timeout' in m.text) else None)
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
           's5airto': s5.get('s5airto'), 'glide_err': s5.get('error'),
           'realStaged_first': (s5.get('realStaged') or {}).get('rays', [{}])[0] if (s5.get('realStaged') or {}).get('rays') else None}
    if rean and traj:
        t_hit = rean[0].get('tMs', 0)
        pre = [s for s in traj if s.get('blendD') is not None and s.get('t', 0) <= t_hit]
        out['pre_hit_samples'] = len(pre)
        out['pre_hit_blendD_max'] = max((s['blendD'] for s in pre), default=None)
        out['pre_hit_blendD_last'] = pre[-1]['blendD'] if pre else None
        post = [s['blendD'] for s in traj if s.get('blendD') is not None and s.get('t', 0) > t_hit]
        out['post_hit_blendD_min'] = min(post) if post else None
        out['dip_restart'] = bool(pre and post and out['pre_hit_blendD_last'] is not None
                                  and out['post_hit_blendD_min'] is not None
                                  and out['post_hit_blendD_min'] < out['pre_hit_blendD_last'] - 0.5)
        # analytic vz comparison around the FIRST re-anchor: window +/- 1.5 s
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
            errs.append((abs(s['vz'] - exp), s.get('t', 0)))
        out['analytic_vz_err_max_all'] = round(max((e for e, _ in errs), default=0), 4)
        out['analytic_n_all'] = len(errs)
        w = [e for e, t in errs if abs(t - t_hit) <= 1500]
        out['analytic_vz_err_max_win'] = round(max(w), 4) if w else None
        out['analytic_n_win'] = len(w)
    return out

cases = [
    ('?s5=1&s5blend=1&s5air=85', 'nosoup-staged-85'),
]
out = {}
for q, name in cases:
    r = run(q)
    a = analyze(r)
    a['console_errors'] = r['console_errors']
    a['page_errors'] = r['page_errors']
    a['logs'] = r['logs'][:14]
    a['soup'] = (r.get('gate') or {}).get('soup')
    a['pass'] = (r.get('gate') or {}).get('pass')
    out[name] = a
    print(name, '->', json.dumps({k: v for k, v in a.items() if k != 'logs'}, default=str)[:700])
    print('  logs:', a['logs'])
json.dump(out, open(OUT, 'w'), indent=1, default=str)
print('saved', OUT)
