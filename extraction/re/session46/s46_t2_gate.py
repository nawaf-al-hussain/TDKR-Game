#!/usr/bin/env python3
"""s46 T2 gate: headless-load city_slice_textured.html with the USER's release
zip; assert 0 console errors, geometry+texture digests vs Python, and thumb16
closer to the real-binding Python render than to null-binding renders."""
import json, subprocess, sys, time, socket, threading, http.server, functools
import numpy as np

REF = json.load(open('/home/z/my-project/scripts/s46_t2_reference.json'))
PORT = 8098
PAGE = '/playable/city_slice_textured.html'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'


def wait_port(port, timeout=15):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1):
                return True
        except OSError:
            time.sleep(0.25)
    return False


def tv(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    ha, _ = np.histogram(a, 32, (0, 255))
    hb, _ = np.histogram(b, 32, (0, 255))
    return float(0.5 * np.abs(ha / ha.sum() - hb / hb.sum()).sum())


def main():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler,
                                directory='/tmp/my-project/work/city_slice_wt')
    httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    ok = wait_port(PORT)
    print('server:', ok)
    from playwright.sync_api import sync_playwright
    verdict = {'console_errors': [], 'page_errors': []}
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True,
                                        args=['--enable-unsafe-swiftshader'])
            ctx = browser.new_context(viewport={'width': 1280, 'height': 900})
            page = ctx.new_page()
            page.on('console', lambda m: verdict['console_errors'].append(m.text)
                    if m.type == 'error' else None)
            page.on('pageerror', lambda e: verdict['page_errors'].append(str(e)))
            page.goto(f'http://127.0.0.1:{PORT}{PAGE}', wait_until='load')
            page.set_input_files('#f', ZIP)
            for _ in range(150):  # up to 300 s
                done = page.evaluate('window.__GATE && window.__GATE.done')
                if done:
                    break
                page.wait_for_timeout(2000)
            gate = page.evaluate('window.__GATE')
            verdict['gate'] = gate
            page.screenshot(path='/home/z/my-project/scripts/s46_t2_gate_shot.png')
            browser.close()
    finally:
        httpd.shutdown()

    g = verdict.get('gate', {})
    checks = {}
    checks['no_page_errors'] = not verdict['page_errors']
    checks['no_console_errors'] = not verdict['console_errors']
    checks['no_gate_error'] = not g.get('error')
    checks['geo_digest'] = g.get('geo_digest') == REF['geo_digest']
    checks['_geo_page'] = str(g.get('geo_digest'))[:20]
    checks['_geo_ref'] = str(REF['geo_digest'])[:20]
    checks['tex_digest'] = g.get('tex_digest') == REF['tex_digest']
    th = g.get('thumb16')
    if th:
        t_real = tv(th, REF['thumb_real'])
        t_nulls = {k: tv(th, v) for k, v in REF['thumb_nulls'].items()}
        r_real = float(np.corrcoef(th, REF['thumb_real'])[0, 1])
        checks['corr_page_real'] = round(r_real, 4)
        r_nulls = {k: round(float(np.corrcoef(th, v)[0, 1]), 4) for k, v in REF['thumb_nulls'].items()}
        checks['corr_page_nulls'] = r_nulls
        checks['tv_page_real'] = round(t_real, 4)
        # pixel-level comparison: page PNG vs Python renders (700x700)
        import base64, io as _io
        from PIL import Image as _Image
        pimg = np.asarray(_Image.open(_io.BytesIO(base64.b64decode(g['png'].split(',', 1)[1]))).convert('RGB'), np.float32)
        def pixcorr(path):
            r = np.asarray(_Image.open(path).convert('RGB'), np.float32)
            mask = (pimg.sum(2) > 0) & (r.sum(2) > 0)
            if mask.sum() < 500:
                return 0.0
            a = pimg[mask]; b = r[mask]
            cs = []
            for c in range(3):
                if a[:, c].std() < 1e-6 or b[:, c].std() < 1e-6:
                    cs.append(0.0)
                else:
                    cs.append(float(np.corrcoef(a[:, c], b[:, c])[0, 1]))
            return round(float(np.mean(cs)), 4)
        checks['pixcorr_real'] = pixcorr('/home/z/my-project/scripts/s46_t2_py_real.png')
        checks['pixcorr_nulls'] = {k: pixcorr(f'/home/z/my-project/scripts/s46_t2_py_null_{k}.png')
                                   for k in REF['thumb_nulls']}
        checks['separation'] = (checks['pixcorr_real'] > 0.8 and
                                checks['pixcorr_real'] - max(checks['pixcorr_nulls'].values()) >= 0.2)
        checks['covered'] = g.get('pixels_covered')
    ok = all(checks.get(k, False) for k in
             ('no_page_errors', 'no_console_errors', 'no_gate_error',
              'geo_digest', 'tex_digest', 'separation'))
    print(json.dumps({'verdict': 'PASS' if ok else 'FAIL', 'checks': checks,
                      'page_errors': verdict['page_errors'][:3],
                      'console_errors_head': verdict['console_errors'][:3]}, indent=1))
    return 0 if ok else 2


if __name__ == '__main__':
    sys.exit(main())
