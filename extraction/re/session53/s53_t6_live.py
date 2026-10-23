#!/usr/bin/env python3
"""s53 T6: live verification by PUBLIC URL (nothing deployed).
Loads the live gh-pages viewer and the live walktest page; counts requests + console errors."""
import json, time
from playwright.sync_api import sync_playwright

LIVE = 'https://nawaf-al-hussain.github.io/TDKR-Game/'
out = {}
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
    for name, url in (('viewer', LIVE + '?userfiles=1'), ('walktest', LIVE + 'playable/walktest.html')):
        reqs = {'n': 0, 'failed': 0}
        errs = []
        pg = b.new_page(viewport={'width': 960, 'height': 600})
        pg.on('request', lambda r: reqs.__setitem__('n', reqs['n'] + 1))
        pg.on('requestfailed', lambda r: reqs.__setitem__('failed', reqs['failed'] + 1))
        pg.on('console', lambda m: errs.append(m.text[:150]) if m.type == 'error' else None)
        pg.on('pageerror', lambda e: errs.append(str(e)[:150]))
        t0 = time.time()
        try:
            pg.goto(url, wait_until='load', timeout=45000)
            time.sleep(8)   # let the boot settle
            body = pg.evaluate('document.body ? document.body.children.length : -1')
            scene = pg.evaluate('(window.scene && window.scene.children) ? window.scene.children.length : null')
            out[name] = {'url': url, 'load_ok': True, 'elapsed_s': round(time.time() - t0, 1),
                         'requests': reqs['n'], 'failed': reqs['failed'], 'console_errors': errs[:5],
                         'body_children': body, 'scene_children': scene}
        except Exception as e:
            out[name] = {'url': url, 'load_ok': False, 'error': str(e)[:200]}
        pg.close()
    b.close()
print(json.dumps(out, indent=1))
json.dump(out, open('/tmp/my-project/work/TDKR-Game/extraction/re/session53/s53_t6_live.json', 'w'), indent=1)
