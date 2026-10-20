#!/usr/bin/env python3
"""s42 T1: LIVE belt-region colour check on the deployed playable page (public URL).
The LIVE page renders Batman large and lit with the embedded PNG (built straight-RGB).
If the RGB order were wrong, the belt band would read cool (B>R). Also a null:
we simulate the wrong order by swapping R/B on the same measured pixels.
"""
import json
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

OUT = '/home/z/my-project/scripts/s42_t1_live.json'
W, H = 1280, 720
URL = 'https://nawaf-al-hussain.github.io/TDKR-Game/playable/index.html#freeze0.5'

errors = []
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': W, 'height': H})
    pg.on('console', lambda m: errors.append(f'console:{m.text[:160]}') if m.type == 'error' else None)
    pg.on('pageerror', lambda e: errors.append(f'pageerror:{str(e)[:160]}'))
    pg.on('requestfailed', lambda r: errors.append(f'reqfail:{r.url[:120]}'))
    pg.goto(URL, wait_until='load', timeout=90000)
    # wait for the skinned mesh + freeze: the page sets a ready marker when booted
    try:
        pg.wait_for_function(
            "() => { const c = document.querySelector('canvas'); return c && c.width > 300; }",
            timeout=90000)
        pg.wait_for_timeout(15000)  # let boot + pose settle (live boot ~10-20 s)
        png = '/home/z/my-project/scripts/s42_t1_live.png'
        pg.screenshot(path=png)
        ok = True
    except Exception as e:
        ok = False
        png = None
        print('NAV/WAIT FAIL:', str(e)[:200])
    b.close()

res = {'url': URL, 'console_errors': errors[:10], 'screenshot': bool(png)}
if png:
    im = np.asarray(Image.open(png).convert('RGB'), np.int32)
    # night-scene background: use the top rows (sky) median
    bg = np.median(im[:20].reshape(-1, 3), 0)
    dist = np.abs(im - bg).sum(2)
    sil = dist > 30
    ys, xs = np.nonzero(sil)
    # restrict to the largest central blob: keep rows 15-90% height of the sil bbox
    y0, y1 = ys.min(), ys.max()
    x0, x1 = xs.min(), xs.max()
    hh = y1 - y0
    res['bg'] = bg.tolist(); res['sil_px'] = int(sil.sum())
    res['bbox'] = [int(x0), int(y0), int(x1), int(y1)]
    out = {}
    for name, flo, fhi in (('belt', 0.42, 0.56), ('chest', 0.60, 0.78), ('legs', 0.20, 0.40)):
        band = sil[int(y0 + flo * hh):int(y0 + fhi * hh), x0:x1 + 1]
        bandim = im[int(y0 + flo * hh):int(y0 + fhi * hh), x0:x1 + 1]
        sel = bandim[band]
        if len(sel) < 100:
            out[name] = None
            continue
        m = sel.mean(0)
        out[name] = {'n': int(len(sel)),
                     'meanRGB': [round(float(v), 2) for v in m],
                     'warmth': round(float(m[0] - m[2]), 2),
                     'warmth_if_BGR': round(float(m[2] - m[0]), 2)}
    res['regions'] = out
    # verdict: belt warmth (R-B) must be positive (warm/gold) under the correct order
    belt = out.get('belt')
    res['verdict'] = ('PASS: LIVE belt band reads warm (R>B) — embedded PNG carries R,G,B'
                      if belt and belt['warmth'] > 0 else
                      'CHECK: belt not warm — inspect')
json.dump(res, open(OUT, 'w'), indent=1)
print(json.dumps(res, indent=1))
