#!/usr/bin/env python3
"""S62 T2 step 2: run the page, capture bindBisect dump -> s62_t2_bisect.json.
Reuses the s61 gate harness pattern (playwright + user zip)."""
import json, time, socket, threading, http.server, functools

PORT = 8174
WT = '/tmp/my-project/work/ghpages_staged_wt'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t2_capture2.json'

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
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    assert wait_port(PORT)
    from playwright.sync_api import sync_playwright
    rec = {'console_errors': [], 'logs': []}
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--enable-unsafe-swiftshader', '--use-gl=swiftshader',
                                    '--enable-webgl', '--ignore-gpu-blocklist'])
        pg = b.new_page(viewport={'width': 960, 'height': 600})
        pg.on('console', lambda m: rec['console_errors'].append(m.text[:200])
              if m.type == 'error' else
              (rec['logs'].append(m.text[:200]) if ('enemy' in m.text or 'bind' in m.text.lower()) else None))
        pg.on('pageerror', lambda e: rec['console_errors'].append('PAGEERROR ' + str(e)[:200]))
        pg.goto('http://127.0.0.1:%d/playable/integration_lazy.html?enemy=1&s62bisect=1' % PORT)
        if pg.query_selector('input[type=file]'):
            pg.set_input_files('input[type=file]', ZIP)
        # wait for the bisect dump
        for _ in range(120):
            time.sleep(1)
            v = pg.evaluate('window.__GATE && window.__GATE.bindBisect ? 1 : 0')
            if v:
                break
        else:
            rec['error'] = 'bisect never appeared'
        bb = pg.evaluate('window.__GATE ? window.__GATE.bindBisect : null')
        rec['bindBisect'] = bb
        # also keep the enemyIoU2 restMaxDev from the same load for cross-check
        rec['restMaxDev'] = pg.evaluate(
            'window.__GATE && window.__GATE.enemyIoU2 ? window.__GATE.enemyIoU2.restMaxDev : null')
        rec['bw'] = pg.evaluate('window.__GATE && window.__GATE.enemyIoU2 ? window.__GATE.enemyIoU2.bw : null')
        rec['bwVerts'] = pg.evaluate('window.__GATE && window.__GATE.enemyIoU2 ? window.__GATE.enemyIoU2.bwVerts : null')
        rec['framesMeta'] = pg.evaluate('window.__GATE && window.__GATE.enemyIoU2 ? window.__GATE.enemyIoU2.frames : null')
        b.close()
    httpd.shutdown()
    json.dump(rec, open(OUT, 'w'), indent=1)
    print('console errors:', len(rec['console_errors']))
    print('restMaxDev (fixed invB):', rec.get('restMaxDev'))
    bw = rec.get('bw') or {}
    print('bw keys:', list(bw.keys()) if bw else None)
    bv = rec.get('bwVerts') or {}
    print('bwVerts clips:', list(bv.keys()) if bv else None)
    print('saved', OUT)

if __name__ == '__main__':
    main()
