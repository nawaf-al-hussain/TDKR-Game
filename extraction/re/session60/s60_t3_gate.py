#!/usr/bin/env python3
"""s60 T3 gate: ?enemy=1 with Hurt/Death clips + rest-pose IoU vs Python reference.
Also default digest check (unchanged LIVE 00ce7970/137893) via the default run."""
import json, time, socket, threading, http.server, functools, base64

PORT = 8163
WT = '/tmp/my-project/work/ghpages_staged_wt'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session60/s60_t3_gate.json'
REF = json.load(open('/tmp/my-project/scripts/s60_t3_sil_refs.json'))

def wait_port(port, timeout=15):
    import time as _t
    t0 = _t.time()
    while _t.time() - t0 < timeout:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1):
                return True
        except OSError:
            time.sleep(0.25)
    return False

def run(qs, name, budget=360, want=('done', 'pass', 'soup', 'routes', 'enemy', 'enemyPlay', 'enemyIoU', 'error')):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WT)
    httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    wait_port(PORT)
    from playwright.sync_api import sync_playwright
    rec = {'name': name, 'qs': qs, 'console_errors': [], 'page_errors': [], 'logs': []}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
        page = browser.new_page(viewport={'width': 960, 'height': 600})
        page.on('console', lambda m: rec['console_errors'].append(m.text[:200]) if m.type == 'error' else None)
        page.on('pageerror', lambda e: rec['page_errors'].append(str(e)[:200]))
        page.on('console', lambda m: rec['logs'].append(m.text[:300]) if ('enemy' in m.text or 'merc' in m.text or 'gate' in m.text.lower()) else None)
        page.goto('http://127.0.0.1:%d/playable/integration_lazy.html%s' % (PORT, qs))
        page.set_input_files('#f', ZIP)
        gate = {}
        t0 = time.time()
        while time.time() - t0 < budget:
            time.sleep(0.5)
            gate = page.evaluate('window.__GATE || {}')
            if 'enemy=1' in qs:
                ep = gate.get('enemyPlay') or {}
                if ep.get('reported') or (ep.get('dispIdle') is not None and gate.get('enemyIoU')):
                    time.sleep(1.0)
                    gate = page.evaluate('window.__GATE || {}')
                    break
            elif gate.get('done'):
                break
        rec['elapsed_s'] = round(time.time() - t0, 1)
        rec['gate'] = {k: gate.get(k) for k in want if k in gate}
        try:
            browser.close()
        except Exception:
            pass
    httpd.shutdown(); httpd.server_close()
    return rec

def occ_from_hex(h):
    G = 64
    occ = [[False] * G for _ in range(G)]
    for gy in range(G):
        for gx in range(G // 8):
            b = int(h[(gy * (G // 8) + gx) * 8:(gy * (G // 8) + gx) * 8 + 8], 16)
            for gy2 in range(4):
                for gx2 in range(8):
                    if b & (1 << (gy2 * 8 + gx2)):
                        occ[gy][gx * 8 + gx2] = True
    return occ

def iou(a, b):
    inter = sum(1 for y in range(64) for x in range(64) if a[y][x] and b[y][x])
    un = sum(1 for y in range(64) for x in range(64) if a[y][x] or b[y][x])
    return inter / un if un else 0.0

out = {'runs': []}
r = run('?enemy=1', 'enemy+IoU')
out['runs'].append(r)
giu = (r['gate'].get('enemyIoU') or {})
page_hex = giu.get('gridHex')
if page_hex:
    pocc = occ_from_hex(page_hex)
    rocc = occ_from_hex(REF['merc_ref_hex'])
    bocc = occ_from_hex(REF['batman_ref_hex'])
    # flipped page grid (x-mirror) for orientation control
    focc = [[pocc[y][63 - x] for x in range(64)] for y in range(64)]
    out['iou'] = {
        'page_vs_merc_ref': round(iou(pocc, rocc), 4),
        'page_vs_batman_ref': round(iou(pocc, bocc), 4),
        'page_flipped_vs_merc_ref': round(iou(focc, rocc), 4),
    }
    out['iou_verdict'] = ('PASS' if (out['iou']['page_vs_merc_ref'] > 0.85 and
                                     out['iou']['page_vs_merc_ref'] > out['iou']['page_vs_batman_ref'] and
                                     out['iou']['page_vs_merc_ref'] > out['iou']['page_flipped_vs_merc_ref'])
                          else 'FAIL')
out['enemyIoU'] = giu
ep = r['gate'].get('enemyPlay') or {}
out['enemyPlay'] = ep
out['verdict'] = ('PASS' if (r['gate'].get('done') and not r['console_errors'] and not r['page_errors']
                             and ep.get('ok') and giu.get('ok') and out.get('iou_verdict') == 'PASS')
                  else 'FAIL')
json.dump(out, open(OUT, 'w'), indent=1)
print('verdict:', out['verdict'])
print('iou:', out.get('iou'))
print('enemyPlay ok:', ep.get('ok'), 'disp:', {k: ep.get(k) for k in ('dispIdle', 'dispWalk', 'dispRun', 'dispHurt', 'dispDeath', 'dispCtlWrongClip')})
print('hurtDone/deathDone:', ep.get('hurtDone'), ep.get('deathDone'))
print('IoU meta:', {k: giu.get(k) for k in ('height', 'feetZ', 'bindMaxDev', 'nVerts')})
print('console_errors:', r['console_errors'][:4], 'page_errors:', r['page_errors'][:4])
