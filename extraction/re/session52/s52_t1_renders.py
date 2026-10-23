#!/usr/bin/env python3
"""s52 T1 second-renderer runs: firefox, webkit (if launchable), chromium --use-angle=gl under Xvfb.
Same measures per renderer on two configs: step2 fix0 (bug present) and step4 fix1 (fixed).
Also captures __GATE.error + log tail when __GPUCHECK is missing (debug)."""
import json, time, socket, threading, http.server, functools, base64, sys, os, subprocess
import numpy as np
from PIL import Image

PORT = 8155
WT = '/tmp/my-project/work/city_slice_wt'
PAGE = "/playable/city_bisect2.html"
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
BB = '-448,-713,-248,-513'
REFDIR = WT + '/playable/'
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session52/s52_t1_renders.json'

def wait_port(port, timeout=20):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1):
                return True
        except OSError:
            time.sleep(0.25)
    return False

def load_rgb(p):
    return np.asarray(Image.open(p).convert('RGB'), np.float64)

def cmp_arrays(gl, ref):
    gl = gl[::-1]
    gm = gl.mean(axis=2); rm = ref.mean(axis=2)
    gcm = gm > 8; rcm = rm > 8
    both = gcm & rcm
    if both.sum() <= 20:
        return {'shared': int(both.sum())}
    a = gm[both]; b = rm[both]
    return {'shared': int(both.sum()),
            'gl_mean': round(float(a.mean()), 2), 'cpu_mean': round(float(b.mean()), 2),
            'ratio': round(float(a.mean()) / max(float(b.mean()), 1e-9), 4),
            'corr': round(float(np.corrcoef(a, b)[0, 1]), 4),
            'gl_cov_pct': round(100 * float(gcm.mean()), 3)}

def run_one(browser_kind, qs, dumpbase, extra_args=None, headless=True):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WT)
    httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    wait_port(PORT)
    res = {'browser': browser_kind, 'qs': qs}
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            if browser_kind == 'chromium':
                browser = p.chromium.launch(headless=headless, args=extra_args or ['--enable-unsafe-swiftshader'])
            elif browser_kind == 'firefox':
                browser = p.firefox.launch(headless=headless, args=extra_args or [])
            elif browser_kind == 'webkit':
                browser = p.webkit.launch(headless=headless, args=extra_args or [])
            else:
                raise SystemExit('unknown browser')
            page = browser.new_page(viewport={'width': 1280, 'height': 900})
            errs = []
            page.on('pageerror', lambda e: errs.append(str(e)))
            page.goto('http://127.0.0.1:%d%s%s' % (PORT, PAGE, qs))
            page.set_input_files('#f', ZIP)
            gate = {}
            for _ in range(240):
                time.sleep(1)
                gate = page.evaluate('window.__GATE || {}')
                if gate.get('done'):
                    break
            url = page.evaluate('window.__GLDUMP && window.__GLDUMP()')
            if url:
                png = REFDIR + dumpbase + '.png'
                open(png, 'wb').write(base64.b64decode(url.split(',', 1)[1]))
                res['dump'] = dumpbase + '.png'
            res['gate'] = {k: gate.get(k) for k in ('corr', 'js_mean', 'draws', 'glerr', 'error')}
            gc = page.evaluate('window.__GPUCHECK || null')
            res['gpucheck'] = gc
            if gc is None:
                try:
                    res['logtail'] = page.evaluate("document.querySelector('#log').textContent")[-600:]
                except Exception as e:
                    res['logtail'] = 'log read fail %s' % e
            res['pageerrs'] = errs[:3]
            # renderer identity
            try:
                res['renderer'] = page.evaluate(
                    "(() => { const c=document.createElement('canvas'); const g=c.getContext('webgl');"
                    "const e=g.getExtension('WEBGL_debug_renderer_info');"
                    "return e ? g.getParameter(e.UNMASKED_RENDERER_WEBGL) : 'n/a'; })()")
            except Exception:
                res['renderer'] = 'eval-fail'
            browser.close()
    except Exception as e:
        res['launch_error'] = str(e)[:300]
    finally:
        httpd.shutdown()
        httpd.server_close()
    return res

def main():
    cpu2 = load_rgb(REFDIR + 's52_cpu_step2.png')
    cpu4 = load_rgb(REFDIR + 's52_cpu_step4.png')
    cfgs = [
        ('chromium-swiftshader', 'chromium', ['--enable-unsafe-swiftshader'], True),
        ('firefox', 'firefox', [], True),
        ('chromium-angle-gl', 'chromium', ['--use-angle=gl', '--enable-unsafe-swiftshader'], False),
        ('webkit', 'webkit', [], True),
    ]
    out = {}
    for tag, kind, args, hl in cfgs:
        for step, fix, cpuref in ((2, 0, cpu2), (4, 1, cpu4)):
            qs = '?mat=73&bb=%s&nodepth=1&upload=1&step=%d&fix=%d&gpucheck=%d' % (BB, step, fix, 1 if (step == 4 and fix == 1) else 0)
            key = '%s_step%d_fix%d' % (tag, step, fix)
            print(key, '...', flush=True)
            r = run_one(kind, qs, 's52_glr_' + key, args, hl)
            if 'dump' in r:
                m = cmp_arrays(load_rgb(REFDIR + r['dump']), cpuref)
                r['measure'] = m
                print('  ', m, 'renderer:', r.get('renderer'), flush=True)
            out[key] = r
            json.dump(out, open(OUT, 'w'), indent=1)
    print('saved', OUT)

if __name__ == '__main__':
    main()
