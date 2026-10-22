#!/usr/bin/env python3
"""s49 T6: verify the LIVE public URL (gh-pages 16a22ce) still loads cleanly."""
import json, time
from playwright.sync_api import sync_playwright
URL = 'https://nawaf-al-hussain.github.io/TDKR-Game/playable/index.html'
out = {'url': URL}
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
    page = browser.new_page(viewport={'width': 1280, 'height': 900})
    errs = []
    page.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    page.on('pageerror', lambda e: errs.append(str(e)))
    resp = page.goto(URL + '?userfiles=1', wait_until='load', timeout=60000)
    out['status'] = resp.status if resp else None
    out['title'] = page.title()
    out['has_zip_input'] = page.locator('#zipfile').count() > 0
    out['zip_input_note'] = 'appears after ?userfiles=1 init'
    out['walker_note'] = page.locator('#log').inner_text()[:200] if page.locator('#log').count() else ''
    time.sleep(3)
    out['console_errors'] = errs[:5]
    out['three_loaded'] = page.evaluate("typeof window.__P === 'object'")
    page.screenshot(path='/tmp/my-project/work/TDKR-Game/extraction/re/session49/s49_t6_live.png')
    browser.close()
json.dump(out, open('/tmp/my-project/work/TDKR-Game/extraction/re/session49/s49_t6_live.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
