#!/usr/bin/env python3
"""s48 T3 gate: headless-load city_slice7.html with the USER's release zip;
assert 0 console errors, compiled-table digest == Python digest (1d0f1930...),
source.dae digest == 4f6e2d07..., in-page parity 307/307 names + 305/307 rows
with only the 2 FX_Coronas diffs, and report the time/memory cost vs XML."""
import json, time, socket, threading, http.server, functools

PORT = 8109
PAGE = '/playable/city_slice7.html'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
WT = '/tmp/my-project/work/city_slice_wt'
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session48/s48_t3_gate.json'


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
            for _ in range(120):
                time.sleep(1)
                gate = page.evaluate('window.__GATE || {}')
                if gate.get('done'):
                    break
            browser.close()
    finally:
        httpd.shutdown()
    print('console errors:', verdict['console_errors'][:5], 'count', len(verdict['console_errors']))
    print('page errors:', verdict['page_errors'][:3])
    print('gate error:', gate.get('error'))
    for k in ('n_compiled', 'n_xml', 't_compiled_ms', 't_xml_ms', 'speedup',
              'mem_compiled_mb', 'mem_xml_mb', 'digest_compiled_match',
              'digest_xml_match', 'name_match', 'row_ok', 'no_scene_n'):
        print(' ', k, '=', gate.get(k))
    print('  diffs =', json.dumps(gate.get('diffs'))[:400])
    ok = (len(verdict['console_errors']) == 0 and len(verdict['page_errors']) == 0
          and gate.get('digest_compiled_match') and gate.get('digest_xml_match')
          and gate.get('name_match') == 307 and gate.get('row_ok') == 305
          and gate.get('no_scene_n') == 0 and len(gate.get('diffs') or []) == 2)
    out = dict(gate)
    out['console_errors'] = len(verdict['console_errors'])
    out['page_errors'] = len(verdict['page_errors'])
    out['verdict'] = bool(ok)
    print('VERDICT:', out['verdict'])
    json.dump(out, open(OUT, 'w'), indent=1)


if __name__ == '__main__':
    main()
