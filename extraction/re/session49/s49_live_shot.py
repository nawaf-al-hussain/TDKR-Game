#!/usr/bin/env python3
"""s49 T1d: load the LIVE deployed viewer (?userfiles=1), fly to the road276 block,
screenshot, measure mean luminance over the block area."""
import json, time
from playwright.sync_api import sync_playwright

URL = 'https://nawaf-al-hussain.github.io/TDKR-Game/index.html?userfiles=1'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
OUT = '/home/z/my-project/work/TDKR-Game/extraction/re/session49/s49_t1_live.png'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader'])
    pg = b.new_page(viewport={'width': 1024, 'height': 600})
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:150]))
    pg.on('console', lambda m: errs.append(m.text[:120]) if m.type == 'error' else None)
    pg.goto(URL)
    pg.wait_for_timeout(4000)
    inp = pg.query_selector('input[type=file]')
    if inp:
        inp.set_input_files(ZIP)
    # wait for city streaming to finish: the overlay text 'streaming city' disappears
    for _ in range(180):
        time.sleep(1)
        txt = pg.evaluate("document.body ? document.body.innerText.slice(0, 400) : ''")
        if 'streaming' not in txt and 'GOTHAM' not in txt:
            break
    print('overlay gone after wait; body text head:', pg.evaluate("document.body.innerText.slice(0,80)"))
    pg.wait_for_timeout(6000)
    # camera over the road276 block: zone (x=-88.45, y_zone=-1129.1) -> live (x, y=camH, z=+1129.1)
    pg.evaluate('''() => {
      const v = window.__v;
      if (v && v.camera) {
        v.camera.position.set(-88.45, 25.3, 1129.1);
        v.camera.lookAt(-88.45, 0, 1129.1);
        if (v.controls) { v.controls.target.set(-88.45, 0, 1129.1); v.controls.update(); }
      }
    }''')
    pg.wait_for_timeout(2500)
    pg.screenshot(path=OUT)
    print('errors:', errs[:4], 'n=', len(errs))
    print('saved', OUT)
    b.close()
