#!/usr/bin/env python3
"""S62 T4 gate: REAL collision-soup air-collision re-anchor for the glide (?s5blend=1&s5real=1).
- staging: s5Begin rotates the grapple target until the glide direction crosses a real
  facade within 12..160 u (blocked() at takeoff feet - 3); realStaged recorded.
- glide: the walker's capsule-vs-soup query at the destination altitude; on the
  not-blocked -> blocked edge the slide resolver clamps the step and the takeoff anchor
  RE-ANCHORS at the resolved position (ResolveAirCollision analogue, 0x398570) -> the
  blend distance restarts (dip jump in the recorded traj).
Accept: >=1 reanchor kind 'real', wallHit set, landed, 0 console errors, and a blendD DIP
RESTART after some re-anchor (anchor distance resets -> post-reanchor min blendD < pre
max blendD - 0.5; the s60 virtual-wall semantic, measured on the real path). blend jumps
are reported but not required: with a facade AT the glide start (low ledge) blend never
decays before the hit. control ?s5blend=1 (no s5real): reanchors == []; soup digest
00ce7970/137893 in both runs."""
import json, time, socket, threading, http.server, functools

PORT = 8178
WT = '/tmp/my-project/work/ghpages_staged_wt'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t4_gate.json'

def wait_port(port, timeout=15):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1):
                return True
        except OSError:
            time.sleep(0.25)

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
                if ('s5 REAL' in m.text or 'S5 landed' in m.text or 'S5 grapple' in m.text) else None)
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

def blend_jumps(traj):
    jumps, prev = [], None
    for s in traj or []:
        b = s.get('blend')
        if b is None:
            continue
        if prev is not None and b - prev > 0.5:
            jumps.append(round(b - prev, 3))
        prev = b
    return jumps

out = {}
r1 = run('?s5=1&s5blend=1&s5real=1')
out['real_run'] = r1
s5 = r1['gate'].get('s5') or {}
rean = s5.get('reanchors') or []
out['realStaged'] = s5.get('realStaged')
out['reanchors'] = rean
out['wallHit'] = s5.get('wallHit')
out['landed'] = s5.get('landed')
out['n_traj'] = len(s5.get('traj') or [])
out['blend_jumps'] = blend_jumps(s5.get('traj') or [])
kinds_ok = bool(rean) and all(r.get('kind') == 'real' for r in rean)

def dip_restart(traj, rean):
    for r in rean or []:
        pre = [s['blendD'] for s in traj or []
               if s.get('blendD') is not None and s['t'] <= r['tMs'] - 100]
        post = [s['blendD'] for s in traj or []
                if s.get('blendD') is not None and r['tMs'] + 100 <= s['t'] <= r['tMs'] + 700]
        if pre and post and min(post) < max(pre) - 0.5:
            return True, r['tMs']
    return False, None

out['dip_restart'], out['dip_at_tMs'] = dip_restart(s5.get('traj') or [], rean)
out['real_verdict'] = 'PASS' if (kinds_ok and s5.get('wallHit') and s5.get('landed')
                                 and out['dip_restart']
                                 and not r1['console_errors'] and not r1['page_errors']
                                 and r1['gate'].get('soupDigestPass')) else 'FAIL'

r2 = run('?s5=1&s5blend=1')
out['control_run_gate'] = r2['gate'].get('s5') or {}
out['control_reanchors'] = out['control_run_gate'].get('reanchors')
out['control_landed'] = out['control_run_gate'].get('landed')
out['control_verdict'] = 'PASS' if (out['control_reanchors'] == [] and out['control_landed']
                                    and not r2['console_errors'] and not r2['page_errors']
                                    and r2['gate'].get('soupDigestPass')) else 'FAIL'
out['verdict'] = 'PASS' if out['real_verdict'] == 'PASS' and out['control_verdict'] == 'PASS' else 'FAIL'
json.dump(out, open(OUT, 'w'), indent=1)
print('VERDICT:', out['verdict'])
print('real: staged=', out['realStaged'], 'reanchors=', rean, 'landed=', out['landed'],
      'jumps=', out['blend_jumps'], 'dip_restart=', out['dip_restart'], '@', out['dip_at_tMs'],
      'n_traj=', out['n_traj'])
print('control: reanchors=', out['control_reanchors'])
print('errors r1:', r1['console_errors'][:3], r1['page_errors'][:3])
print('errors r2:', r2['console_errors'][:3], r2['page_errors'][:3])
print('logs r1:', r1['logs'][:8])
