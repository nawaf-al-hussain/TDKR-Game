#!/usr/bin/env python3
"""s47 T6: load the LIVE pages (gh-pages 16a22ce) and record console errors,
network requests (does anything still read gc_collision.bin?), and the staged
RC (62b4ffd) deploy delta. Read-only — no deploy."""
import json, time
from playwright.sync_api import sync_playwright

LIVE = 'https://nawaf-al-hussain.github.io/TDKR-Game/playable/'
PAGES = [('walktest.html', {}), ('index.html', {'userfiles': '1'})]

out = {}
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
    for name, params in PAGES:
        url = LIVE + name + ('?' + '&'.join(f'{k}={v}' for k, v in params.items()) if params else '')
        ctx = browser.new_context(viewport={'width': 1280, 'height': 900})
        page = ctx.new_page()
        errs, reqs = [], []
        page.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        page.on('pageerror', lambda e: errs.append(str(e)))
        page.on('request', lambda r: reqs.append(r.url))
        t0 = time.time()
        try:
            page.goto(url, timeout=60000)
            page.wait_for_timeout(12000)
        except Exception as e:
            errs.append('nav: ' + str(e))
        files = sorted({u.split('/')[-1].split('?')[0] for u in reqs})
        out[name + ('?userfiles=1' if params else '')] = {
            'url': url, 'status': 'loaded', 'console_errors': errs[:8],
            'n_errors': len(errs), 'n_requests': len(reqs),
            'gc_collision_bin_requested': any('gc_collision.bin' in u for u in reqs),
            'patch_json_requested': any('patch.json' in u for u in reqs),
            'files': files[:24]}
        print(name, params, 'errors:', len(errs), 'reqs:', len(reqs),
              'gc_collision.bin:', out[name + ('?userfiles=1' if params else '')]['gc_collision_bin_requested'],
              'patch.json:', out[name + ('?userfiles=1' if params else '')]['patch_json_requested'])
        ctx.close()
    browser.close()

json.dump(out, open('/tmp/my-project/work/TDKR-Game/extraction/re/session48/s48_t7_live.json', 'w'), indent=1)
print('saved s47_t6_live.json')
