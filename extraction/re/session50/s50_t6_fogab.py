#!/usr/bin/env python3
"""s50 T6: engine fog (ComputeFogFS, end=140) vs the deployed viewer's TEXTURE_FOG
path (end=154 incl GPU_5 1.1) — 3 street blocks, mean luminance + Jensen-Shannon
histogram distance. Report only; NOTHING is deployed."""
import os, shutil, json, time, socket, threading, http.server, functools, base64
import numpy as np
from PIL import Image

SRC = '/tmp/my-project/work/ghpages_live_wt'
SITE = '/tmp/my-project/work/t6_fog_site'
PORT = 8157
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session50/s50_t6_fog.json'

if not os.path.isdir(SITE):
    shutil.copytree(SRC, SITE, ignore=shutil.ignore_patterns('.git'))
    print('site copied')

ap = os.path.join(SITE, 'app.js')
s = open(ap).read()
if 'ENGFOG' not in s:
    # 1. readback flag
    old_r = "renderer = new THREE.WebGLRenderer({ canvas: $('view'), antialias: true, powerPreference: 'high-performance' });"
    assert old_r in s, 'renderer anchor'
    s = s.replace(old_r, "renderer = new THREE.WebGLRenderer({ canvas: $('view'), antialias: true, powerPreference: 'high-performance', preserveDrawingBuffer: true });")
    # 2. runtime switch + end override
    old_f = "const FOG = {\n  start: 0.0,                    // GI +0x0c  (fogStart)\n  end: 154.0,"
    assert old_f in s, 'fog anchor'
    s = s.replace(old_f, "const ENGFOG = new URLSearchParams(location.search).has('engfog');\nconst FOG = {\n  start: 0.0,\n  end: (typeof ENGFOG !== 'undefined' && ENGFOG) ? 140.0 : 154.0,")
    # 3. fragment fog mix -> ComputeFogFS when ENGFOG (all variants share the mix line)
    old_m = "  col = mix(col, fogCol2.rgb, clamp(vFogFactor, 0.0, 1.0) * fogCol2.a);"
    n = s.count(old_m)
    assert n >= 1, 'fog mix anchor missing'
    eng = ("  float gsCF = dot(col, vec3(0.149, 0.293, 0.57));\n"
           "  col = mix(col, uFogColor, clamp(vFogFactor, 0.0, 1.0) * (1.0 - gsCF) * uFogAlpha);"
           "  // s50 T6 ENGINE path (ComputeFogFS)")
    s = s.replace(old_m, "${ENGFOG ? (" + json.dumps(eng) + ") : (\n  \"" + old_m.replace('\n', '\\n') + "\")}", n)
    # uniforms uVFogHeight/uFogDecay referenced in engine path? no; uFogColor/uFogAlpha exist in all fog materials
    open(ap, 'w').write(s)
    print('app.js patched: renderer flag, ENGFOG switch, %d fog-mix sites' % n)

def wait_port(port, timeout=15):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1):
                return True
        except OSError:
            time.sleep(0.25)
    return False

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=SITE)
httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
wait_port(PORT)

from playwright.sync_api import sync_playwright
BLOCKS = [(-462, -768), (-900, -600), (-300, -1100)]

def grab(engfog, tag):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
        page = browser.new_page(viewport={'width': 1280, 'height': 800})
        page.goto('http://127.0.0.1:%d/?%s' % (PORT, 'engfog=1' if engfog else ''))
        # wait for scene ready: GOTHAM overlay gone
        for _ in range(180):
            time.sleep(1)
            try:
                gone = page.evaluate("!!window.__v && !!window.__v.scene && document.querySelector('#overlay') === null")
            except Exception:
                gone = False
            ready = page.evaluate("(function(){ try { return !!window.__v && window.__v.scene.children.length > 3; } catch(e){ return false; } })()")
            if ready:
                break
        time.sleep(3)
        shots = []
        for (bx, bz) in BLOCKS:
            page.evaluate("""(function([bx, bz]){
                const c = window.__v.camera;
                c.position.set(bx + 40, 70, bz + 130);
                c.lookAt(bx, 8, bz);
            })([%f, %f])""" % (bx, bz))
            time.sleep(1.2)
            url = page.evaluate("document.querySelector('canvas#view').toDataURL('image/png')")
            shots.append(url.split(',', 1)[1])
        browser.close()
    for (bx, bz), b64 in zip(BLOCKS, shots):
        fp = '/tmp/my-project/work/TDKR-Game/extraction/re/session50/s50_t6_%s_%d_%d.png' % (tag, bx, bz)
        open(fp, 'wb').write(base64.b64decode(b64))
    print('grabbed', tag)

grab(False, 'deployed')
grab(True, 'engfog')
httpd.shutdown()

def jsd(p, q):
    p = np.asarray(p, np.float64); q = np.asarray(q, np.float64)
    p = p / p.sum(); q = q / q.sum()
    m = 0.5 * (p + q)
    def kl(a, b):
        mask = a > 0
        return float(np.sum(a[mask] * np.log(a[mask] / b[mask])))
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)

res = {'blocks': []}
for (bx, bz) in BLOCKS:
    a = np.asarray(Image.open('/tmp/my-project/work/TDKR-Game/extraction/re/session50/s50_t6_deployed_%d_%d.png' % (bx, bz)).convert('L'), np.float64)
    b = np.asarray(Image.open('/tmp/my-project/work/TDKR-Game/extraction/re/session50/s50_t6_engfog_%d_%d.png' % (bx, bz)).convert('L'), np.float64)
    ha, _ = np.histogram(a, bins=64, range=(0, 255))
    hb, _ = np.histogram(b, bins=64, range=(0, 255))
    ent = {'block': [bx, bz],
           'mean_deployed': float(a.mean()), 'mean_engine': float(b.mean()),
           'ratio_engine_over_deployed': float(b.mean() / max(a.mean(), 1e-9)),
           'js_hist64': jsd(ha, hb)}
    res['blocks'].append(ent)
    print('block (%d,%d): deployed mean %.2f | engine mean %.2f (ratio %.2f) | JSD %.4f'
          % (bx, bz, ent['mean_deployed'], ent['mean_engine'], ent['ratio_engine_over_deployed'], ent['js_hist64']))
json.dump(res, open(OUT, 'w'), indent=1)
print('saved', OUT)
