#!/usr/bin/env python3
"""s42 T1: headless verify the fixed branch page (s40-user-zip-slice playable).
Loads the page with the REAL user zip, freezes the pose, screenshots, and measures
the rendered belt/chest band colour of the Batman silhouette. Null control: the
same page with the old BGR line re-applied (texture R/B swapped) in a temp root.
PASS = 0 console/page errors AND fixed-belt R>B (warm) while null-belt B>R (cool).
"""
import functools, http.server, json, os, shutil, threading
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

WT = '/tmp/my-project/work/ghpages_site_wt'
NULLROOT = '/tmp/s42_t1_null'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
OUT = '/home/z/my-project/scripts/s42_t1_gate.json'
W, H = 1024, 640


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def serve(root, port):
    handler = functools.partial(QuietHandler, directory=root)
    httpd = http.server.ThreadingHTTPServer(('127.0.0.1', port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return port


def build_null():
    if os.path.exists(NULLROOT):
        shutil.rmtree(NULLROOT)
    os.makedirs(f'{NULLROOT}/playable', exist_ok=True)
    # copy the whole worktree minimal set: playable dir + any top-level assets referenced
    for entry in os.listdir(f'{WT}/playable'):
        src = f'{WT}/playable/{entry}'
        dst = f'{NULLROOT}/playable/{entry}'
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    p = f'{NULLROOT}/playable/index.html'
    s = open(p, encoding='utf-8').read()
    new_line = "      rgba[i*4] = px[i*3]; rgba[i*4+1] = px[i*3+1]; rgba[i*4+2] = px[i*3+2]; rgba[i*4+3] = 255;"
    bgr_line = "      rgba[i*4] = px[i*3+2]; rgba[i*4+1] = px[i*3+1]; rgba[i*4+2] = px[i*3]; rgba[i*4+3] = 255;"
    assert s.count(new_line) == 1
    s = s.replace(new_line, bgr_line)
    open(p, 'w', encoding='utf-8').write(s)
    return NULLROOT


def belt_stats(png_path):
    im_full = np.asarray(Image.open(png_path).convert('RGB'), np.int32)
    # exclude UI panels: top-left debug box and bottom log panel -> canvas mid strip
    im = im_full[110:545, :, :]
    # background = median of left/right border columns of the strip (scene clear colour)
    border = np.concatenate([im[:, :12].reshape(-1, 3), im[:, -12:].reshape(-1, 3)])
    bg = np.median(border, 0)
    dist = np.abs(im - bg).sum(2)
    sil = dist > 18
    if sil.sum() < 200:
        return {'error': 'no silhouette', 'bg': bg.tolist(), 'px': int(sil.sum())}
    ys, xs = np.nonzero(sil)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    hh = y1 - y0
    out = {'bbox': [int(x0), int(y0), int(x1), int(y1)], 'px': int(sil.sum()),
           'bbox_h': int(hh), 'bg': bg.tolist()}
    for name, flo, fhi in (('belt', 0.44, 0.58), ('chest', 0.62, 0.78)):
        band = sil[int(y0 + flo * hh):int(y0 + fhi * hh), x0:x1 + 1]
        bandim = im[int(y0 + flo * hh):int(y0 + fhi * hh), x0:x1 + 1]
        sel = bandim[band]
        if len(sel) < 30:
            out[name] = None
            continue
        m = sel.mean(0)
        out[name] = {'n': int(len(sel)), 'meanRGB': [round(float(v), 2) for v in m],
                     'warmth': round(float(m[0] - m[2]), 2)}
    return out


def run(b, port, tag):
    res = {'errors': []}
    pg = b.new_page(viewport={'width': W, 'height': H})
    pg.on('console', lambda m: res['errors'].append(f'console:{m.text[:160]}') if m.type == 'error' else None)
    pg.on('pageerror', lambda e: res['errors'].append(f'pageerror:{str(e)[:160]}'))
    pg.on('requestfailed', lambda r: res['errors'].append(f'reqfail:{r.url[:120]}'))
    pg.goto(f'http://127.0.0.1:{port}/playable/index.html#freeze0.5', wait_until='load', timeout=60000)
    pg.set_input_files('#zf', ZIP)
    pg.wait_for_function('() => window.__glb && window.__glb.length > 100000', timeout=120000)
    pg.wait_for_timeout(4000)  # let the renderer settle + freeze pose apply
    png = f'/home/z/my-project/scripts/s42_t1_{tag}.png'
    pg.screenshot(path=png)
    res['stats'] = belt_stats(png)
    pg.close()
    return res


def main():
    p1 = serve(WT, 8461)
    p2 = serve(build_null(), 8462)
    out = {}
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        out['fixed_rgb'] = run(b, p1, 'fixed')
        out['null_bgr'] = run(b, p2, 'null')
        b.close()
    json.dump(out, open(OUT, 'w'), indent=1)
    print(json.dumps(out, indent=1))
    f = out['fixed_rgb']['stats'].get('belt')
    n = out['null_bgr']['stats'].get('belt')
    ok = (not out['fixed_rgb']['errors'] and not out['null_bgr']['errors']
          and f and n and f['warmth'] > 0 > n['warmth'])
    print('\nVERDICT:', 'PASS (fixed belt warm >0, null belt cool <0, 0 errors)' if ok else 'CHECK MANUALLY')


main()
