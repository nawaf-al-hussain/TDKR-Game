#!/usr/bin/env python3
"""s48 T6 gate: headless-load city_zone.html with the USER's release zip; the
in-browser whole-zone render (all 1,526 segs, compiled bindings, LRU ETC1) is
compared pixel-wise against the Python render; report load/decode/render times,
peak heap, texture stats. No deploy."""
import json, time, socket, threading, http.server, functools

PORT = 8113
PAGE = '/playable/city_zone.html'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
WT = '/tmp/my-project/work/city_slice_wt'
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session48/s48_t6_gate.json'


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
            for _ in range(600):
                time.sleep(1)
                gate = page.evaluate('window.__GATE || {}')
                if gate.get('done'):
                    break
            browser.close()
    finally:
        httpd.shutdown()
    print('console errors:', verdict['console_errors'][:5], 'count', len(verdict['console_errors']))
    print('gate error:', gate.get('error'))
    for k in ('t_load_ms', 't_decode_ms', 't_render_ms', 'segs', 'tris_total',
              'tris_drawn', 'tex_binds', 'tex_lru', 'peak_heap_mb', 'corr'):
        print(' ', k, '=', gate.get(k))
    ok = (len(verdict['console_errors']) == 0 and len(verdict['page_errors']) == 0
          and gate.get('corr') is not None and gate['corr'] > 0.95
          and gate.get('segs') == 1526)
    out = dict(gate)
    out['console_errors'] = len(verdict['console_errors'])
    out['page_errors'] = len(verdict['page_errors'])
    out['verdict'] = bool(ok)
    print('VERDICT:', out['verdict'])
    json.dump(out, open(OUT, 'w'), indent=1)


if __name__ == '__main__':
    main()
