#!/usr/bin/env python3
"""s47 T3 gate: headless-load city_slice5.html with the USER's release zip;
assert 0 console errors, JS source.dae table digest == Python digest, per-block
pixel corr vs the Python real render (>=0.9), and JS real thumbs closer to the
Python real thumbs than to the shuffled/random nulls (TV)."""
import json, subprocess, sys, time, socket, threading, http.server, functools
import numpy as np

REF = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session47/s47_t3_reference.json'))
PORT = 8103
PAGE = '/playable/city_slice5.html'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
WT = '/tmp/my-project/work/city_slice_wt'


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
    # a, b are 32-bin thumb16 histograms already — direct TV on the vectors
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    return float(0.5 * np.abs(a / a.sum() - b / b.sum()).sum())


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
    out = {'console_errors': len(verdict['console_errors']),
           'page_errors': len(verdict['page_errors']),
           'digest_match': gate.get('digest_match'),
           'digest': gate.get('dae_table_digest')}
    if gate.get('blocks'):
        pyblocks = {b['tag']: b for b in REF['blocks']}
        rows = []
        for jb in gate['blocks']:
            pb = pyblocks.get(jb['tag'])
            if not pb:
                continue
            t_real = tv(jb['thumb'], pb['thumb_real'])
            t_sh = tv(jb['thumb'], pb['thumb_shuffle'])
            t_rnd = tv(jb['thumb'], pb['thumb_random'])
            print('   dbg', jb['tag'], jb.get('dbg'))
            rows.append({'tag': jb['tag'], 'corr': jb['corr'], 'tv_real': t_real,
                         'tv_shuffle': t_sh, 'tv_random': t_rnd,
                         'sep_ok': bool(t_real < t_sh and t_real < t_rnd and jb['corr'] > 0.9)})
            print(f"  {jb['tag']}: corr={jb['corr']:.4f} tv_real={t_real:.4f} "
                  f"tv_shuffle={t_sh:.4f} tv_random={t_rnd:.4f} sep={rows[-1]['sep_ok']}")
        out['blocks'] = rows
    out['verdict'] = bool(out['console_errors'] == 0 and out['page_errors'] == 0
                          and out['digest_match']
                          and out.get('blocks') and all(b['sep_ok'] for b in out['blocks']))
    print('VERDICT:', out['verdict'])
    json.dump(out, open('/tmp/my-project/work/TDKR-Game/extraction/re/session47/s47_t3_gate.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
