#!/usr/bin/env python3
"""S39 T1b: load the LIVE pipeline.html from the public URL and drive the full
user-file pipeline (real 895 MB APK/OBB zip) through it. Console + network log.
"""
import json, sys
from playwright.sync_api import sync_playwright

URL = 'https://nawaf-al-hussain.github.io/TDKR-Game/playable/pipeline.html'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session39/s39_t1_pipeline_live.json'

console_msgs, responses = [], []
res = {}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': 1280, 'height': 720})
    pg.on('console', lambda m: console_msgs.append([m.type, m.text[:300]]))
    pg.on('pageerror', lambda e: console_msgs.append(['pageerror', str(e)[:300]]))
    pg.on('response', lambda r: responses.append([r.status, r.url[:160]]))
    pg.goto(URL, wait_until='domcontentloaded', timeout=60000)
    pg.wait_for_timeout(1500)
    res['initial_log'] = pg.inner_text('#log')
    pg.set_input_files('#f', ZIP)
    try:
        pg.wait_for_function(
            "document.getElementById('log').textContent.includes('READY')", timeout=120000)
        res['ready'] = True
    except Exception:
        res['ready'] = False
    res['final_log'] = pg.inner_text('#log')[-600:]
    res['err'] = pg.inner_text('#err')
    # let the render loop produce frames
    pg.wait_for_timeout(2000)
    pg.screenshot(path='/tmp/s39_pipeline_live.png')
    b.close()

res['console_errors'] = [m for m in console_msgs if m[0] in ('error', 'pageerror')]
res['console_all_count'] = len(console_msgs)
bad = [r for r in responses if r[0] >= 400]
res['network_total'] = len(responses)
res['network_non_2xx'] = bad
res['network_all'] = responses
json.dump(res, open(OUT, 'w'), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != 'network_all'}, indent=1)[:2500])
print('PIPELINE LIVE:', 'PASS' if res['ready'] and not res['console_errors'] and not bad else 'FAIL')
sys.exit(0 if res['ready'] and not res['console_errors'] and not bad else 1)
