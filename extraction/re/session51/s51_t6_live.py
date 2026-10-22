#!/usr/bin/env python3
"""s51 T6: LIVE verification of the deployed pages (public URLs).
Loads root viewer + playable walktest with a user zip; reports console errors,
requests, and (for the viewer) that city GLBs stream. NO deployment."""
import json, time
from playwright.sync_api import sync_playwright

BASE = 'https://nawaf-al-hussain.github.io/TDKR-Game/'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session51/s51_t6_live.json'

results = {}
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader'])

    # 1) root viewer ?userfiles=1
    pg = b.new_page(viewport={'width': 1024, 'height': 600})
    errs, reqs = [], []
    pg.on('pageerror', lambda e: errs.append(str(e)[:150]))
    pg.on('console', lambda m: errs.append(m.text[:120]) if m.type == 'error' else None)
    pg.on('request', lambda r: reqs.append(r.url))
    pg.goto(BASE + 'index.html?userfiles=1')
    pg.wait_for_timeout(4000)
    inp = pg.query_selector('input[type=file]')
    if inp:
        inp.set_input_files(ZIP)
    for _ in range(150):
        time.sleep(1)
        txt = pg.evaluate("document.body ? document.body.innerText.slice(0, 300) : ''")
        if 'streaming' not in txt.lower():
            break
    pg.wait_for_timeout(5000)
    glb_ok = pg.evaluate('''() => {
      try { const v = window.__v; if (!v) return 'no __v';
        return 'scene children ' + (v.scene ? v.scene.children.length : 'n/a'); } catch (e) { return String(e); }
    }''')
    body = pg.evaluate("document.body.innerText.slice(0, 120)")
    results['viewer'] = {'console_errors': errs[:5], 'n_requests': len(reqs),
                         'has_gc_collision': any('gc_collision.bin' in u for u in reqs),
                         'glb_probe': glb_ok, 'body': body}
    print('viewer:', results['viewer'])
    pg.screenshot(path='/tmp/my-project/work/TDKR-Game/extraction/re/session51/s51_t6_live_viewer.png')
    pg.close()

    # 2) playable walktest (no userfiles needed: default mode loads patch.json fallback)
    pg = b.new_page(viewport={'width': 1024, 'height': 600})
    errs, reqs = [], []
    pg.on('pageerror', lambda e: errs.append(str(e)[:150]))
    pg.on('console', lambda m: errs.append(m.text[:120]) if m.type == 'error' else None)
    pg.on('request', lambda r: reqs.append(r.url))
    pg.goto(BASE + 'walktest.html')
    pg.wait_for_timeout(12000)
    body = pg.evaluate("document.body.innerText.slice(0, 150)")
    results['walktest'] = {'console_errors': errs[:5], 'n_requests': len(reqs),
                           'has_gc_collision': any('gc_collision.bin' in u for u in reqs),
                           'body': body}
    print('walktest:', results['walktest'])
    pg.screenshot(path='/tmp/my-project/work/TDKR-Game/extraction/re/session51/s51_t6_live_walktest.png')
    pg.close()
    b.close()

json.dump(results, open(OUT, 'w'), indent=1)
print('saved', OUT)
