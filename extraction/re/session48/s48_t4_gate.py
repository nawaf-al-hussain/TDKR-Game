#!/usr/bin/env python3
"""s48 T4 gate: headless-load city_slice8.html with the USER's release zip;
the JS declaration-driven zone decoder must reproduce the Python f64 canonical
digests byte-for-byte on both zones (positions/normals/UVs), and the shuffled-
descriptor null must change the position stream for ~all tried segments."""
import json, time, socket, threading, http.server, functools

REF = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session48/s48_t4_decode.json'))
PORT = 8111
PAGE = '/playable/city_slice8.html'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
WT = '/tmp/my-project/work/city_slice_wt'
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session48/s48_t4_gate.json'


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
            for _ in range(300):
                time.sleep(1)
                gate = page.evaluate('window.__GATE || {}')
                if gate.get('done'):
                    break
            browser.close()
    finally:
        httpd.shutdown()
    print('console errors:', verdict['console_errors'][:5], 'count', len(verdict['console_errors']))
    print('gate error:', gate.get('error'))
    rows = []
    ok = len(verdict['console_errors']) == 0 and len(verdict['page_errors']) == 0
    for zname, ref in REF['digests'].items():
        js = (gate.get('zones') or {}).get(zname)
        if not js:
            ok = False
            print(zname, 'MISSING')
            continue
        match = {k: js['digests'][k] == ref[k] for k in ref}
        nverts_py = None
        print(zname, 'segs', js['nseg'], 'verts', js['nverts'],
              'ms', round(js['ms']), 'digest match', match,
              'null', js['nullInfo'])
        rows.append({'zone': zname, 'segs': js['nseg'], 'verts': js['nverts'],
                     'ms': js['ms'], 'digest_match': match,
                     'digests': js['digests'], 'null': js['nullInfo']})
        ok = ok and all(match.values()) and js['nullInfo']['changed'] > 0.55 * max(1, js['nullInfo']['tried'])
    out = {'console_errors': len(verdict['console_errors']),
           'page_errors': len(verdict['page_errors']),
           'zones': rows, 'verdict': bool(ok)}
    print('VERDICT:', out['verdict'])
    json.dump(out, open(OUT, 'w'), indent=1)


if __name__ == '__main__':
    main()
