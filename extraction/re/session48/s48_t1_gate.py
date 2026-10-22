#!/usr/bin/env python3
"""s48 T1 gate: headless-load city_slice6.html (engine lightmap/additive math)
with the USER's release zip; assert 0 console errors, JS source.dae digest parity,
per-block pixel corr vs the Python engine-math renders (>=0.99 on 5/5), and the
JS TC1 bbox agreement with the Python region check on the LightMapDC blocks."""
import json, time, socket, threading, http.server, functools
import numpy as np

REF = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session48/s48_t1_render.json'))
PORT = 8107
PAGE = '/playable/city_slice6.html'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
WT = '/tmp/my-project/work/city_slice_wt'
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session48/s48_t1_gate.json'


def wait_port(port, timeout=15):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1):
                return True
        except OSError:
            time.sleep(0.25)
    return False


def main():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WT)
    httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    print('server:', wait_port(PORT))
    from playwright.sync_api import sync_playwright
    verdict = {'console_errors': [], 'page_errors': []}
    gate = {}
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
            ctx = browser.new_context(viewport={'width': 1280, 'height': 900})
            page = ctx.new_page()
            page.on('console', lambda m: verdict['console_errors'].append(m.text)
                    if m.type == 'error' else None)
            page.on('pageerror', lambda e: verdict['page_errors'].append(str(e)))
            page.goto(f'http://127.0.0.1:{PORT}{PAGE}')
            page.set_input_files('#f', ZIP)
            for _ in range(240):
                time.sleep(1)
                gate = page.evaluate('window.__GATE || {}')
                if gate.get('done'):
                    break
            browser.close()
    finally:
        httpd.shutdown()
    print('console errors:', verdict['console_errors'][:6], 'count', len(verdict['console_errors']))
    print('page errors:', verdict['page_errors'][:3])
    print('gate error:', gate.get('error'))
    pyblocks = {b['tag']: b for b in REF['blocks']}
    rows = []
    for jb in gate.get('blocks', []):
        pb = pyblocks.get(jb['tag'])
        row = {'tag': jb['tag'], 'mode': jb['mode'], 'corr': jb['corr']}
        if pb and 'tc1_bbox' in jb and 'tc1_bbox' in pb:
            dmax = float(np.max(np.abs(np.array(jb['tc1_bbox'][:4]) - np.array(pb['tc1_bbox']))))
            darea = abs(jb['tc1_bbox'][4] - pb['tc1_area'])
            row['tc1_bbox_maxdiff'] = dmax
            row['tc1_area_diff'] = darea
        if pb and 'color0_mean' in pb and 'color0_mean' in jb:
            row['color0_mean_py'] = pb['color0_mean'][0]
            row['color0_mean_js'] = jb['color0_mean']
        ok = jb['corr'] > 0.99
        if 'tc1_bbox_maxdiff' in row:
            ok = ok and row['tc1_bbox_maxdiff'] < 0.01
        row['ok'] = bool(ok)
        rows.append(row)
        print(' ', row)
    out = {'console_errors': len(verdict['console_errors']),
           'page_errors': len(verdict['page_errors']),
           'digest_match': gate.get('dae_digest_match'),
           'blocks': rows,
           'verdict': bool(len(verdict['console_errors']) == 0
                           and len(verdict['page_errors']) == 0
                           and gate.get('dae_digest_match')
                           and len(rows) == 5 and all(r['ok'] for r in rows))}
    print('VERDICT:', out['verdict'])
    json.dump(out, open(OUT, 'w'), indent=1)


if __name__ == '__main__':
    main()
