#!/usr/bin/env python3
"""S40 T1c: headless-Chromium end-to-end test of the fixed pipeline.html:
- loads the page from the gh-pages worktree over http
- feeds the REAL release zip
- expects READY + street texture decode + no console errors
- checks window.__streetRGBA SHA256 == Python reference
- screenshots the scene with the textured street patch
"""
import sys, threading, http.server, functools, hashlib, json
from playwright.sync_api import sync_playwright

ROOT = '/tmp/my-project/work/ghpages_site_wt'
PORT = 8123
OUT = '/home/z/my-project/scripts/s40_t1_page.json'
SHOT = '/home/z/my-project/scripts/s40_t1_street_patch.png'

def serve():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
    httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()

def main():
    serve()
    res = {'console_errors': [], 'logs': [], 'page_errors': []}
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader'])
        pg = b.new_page(viewport={'width': 1100, 'height': 800})
        pg.on('console', lambda m: res['console_errors'].append(m.text) if m.type == 'error' else None)
        pg.on('pageerror', lambda e: res['page_errors'].append(str(e)))
        pg.goto(f'http://127.0.0.1:{PORT}/playable/pipeline.html')
        pg.set_input_files('#f', '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')
        try:
            pg.wait_for_function("document.querySelector('#log').textContent.includes('READY')",
                                 timeout=180000)
            pg.wait_for_timeout(2500)
            res['logs'] = pg.evaluate("document.querySelector('#log').textContent")
            res['street_sha'] = pg.evaluate("""async () => {
                if (!window.__streetRGBA) return null;
                const h = await crypto.subtle.digest('SHA-256', window.__streetRGBA);
                return [...new Uint8Array(h)].map(x => x.toString(16).padStart(2,'0')).join('');
            }""")
            res['err_box'] = pg.evaluate("document.querySelector('#err').textContent")
            res['preview_pixels'] = pg.evaluate("""() => {
                const cv = document.querySelector('canvas[style*="right:8px"]');
                if (!cv) return null;
                const d = cv.getContext('2d').getImageData(0, 0, 256, 256).data;
                let mean = [0, 0, 0], n = d.length / 4;
                for (let i = 0; i < d.length; i += 4) { mean[0]+=d[i]; mean[1]+=d[i+1]; mean[2]+=d[i+2]; }
                return { mean: mean.map(v => Math.round(v / n)), };
            }""")
            pg.screenshot(path=SHOT)
        except Exception as e:
            res['timeout'] = str(e)
            res['logs'] = pg.evaluate("document.querySelector('#log').textContent")
        b.close()
    REF = '52fcbf324bdd24146b6261da45fc74f4dc9a1dd3715a9c1f71c83bc615331736'
    res['street_sha_match'] = (res.get('street_sha') == REF)
    json.dump(res, open(OUT, 'w'), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != 'logs'}, indent=1))
    print('--- page log tail ---')
    print('\n'.join(res['logs'].splitlines()[-14:]))

if __name__ == '__main__':
    main()
