#!/usr/bin/env python3
"""s52 T1 runner: differential bisect GL vs CPU model, mat73 zoom window.
Sign conventions (declared before reading results):
  covered  = pixel mean RGB > 8
  ratio    = GL_covered_mean / CPU_covered_mean   (1.0 == agreement)
  corr     = Pearson r of per-pixel mean RGB over shared covered pixels
  diverge  = |ratio-1| > 0.05 OR corr < 0.99      (acceptance: within 5%)
  step ladder: 1 UV field, 2 diffuse, 3 D*LM, 4 D*LM*2, 5 +fog (==4, fog inert)
  fix      = 0 keeps the original bind order (defect reproducible), 1 = fixed
"""
import json, time, socket, threading, http.server, functools, base64, sys, subprocess, os
import numpy as np
from PIL import Image

PORT = 8152
WT = '/tmp/my-project/work/city_slice_wt'
PAGE = "/playable/city_bisect2.html"
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
CPU = '/home/z/my-project/scripts/s52_t1_cpu.py'
BB = '-448,-713,-248,-513'
REFDIR = WT + '/playable/'
OUTJSON = '/tmp/my-project/work/TDKR-Game/extraction/re/session52/s52_t1_bisect.json'

def wait_port(port, timeout=20):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1):
                return True
        except OSError:
            time.sleep(0.25)
    return False

def gen_cpu(step):
    out = 's52_cpu_step%d' % step
    png = REFDIR + out + '.png'
    if os.path.exists(png):
        return png
    cmd = [sys.executable, CPU, '--mat', '73', '--bbox=' + BB, '--snap',
           '--step', str(step), '--out', out]
    print('CPU step %d ...' % step, flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-2000:]); print(r.stderr[-2000:])
        raise SystemExit('cpu step %d failed' % step)
    print(r.stdout.strip().splitlines()[-1], flush=True)
    return png

def load_rgb(p):
    return np.asarray(Image.open(p).convert('RGB'), np.float64)

def cmp_pair(glp, refp):
    gl = load_rgb(glp)[::-1]          # GL dumps are bottom-up; refs are top-down
    ref = load_rgb(refp)
    gm = gl.mean(axis=2); rm = ref.mean(axis=2)
    gcm = gm > 8; rcm = rm > 8
    both = gcm & rcm
    out = {'gl_cov_pct': round(100 * float(gcm.mean()), 3),
           'cpu_cov_pct': round(100 * float(rcm.mean()), 3),
           'iou': round(float(both.sum()) / max(1, (gcm | rcm).sum()), 4)}
    if both.sum() > 20:
        a = gm[both]; b = rm[both]
        out['shared'] = int(both.sum())
        out['gl_mean'] = round(float(a.mean()), 2)
        out['cpu_mean'] = round(float(b.mean()), 2)
        out['ratio'] = round(float(a.mean()) / max(float(b.mean()), 1e-9), 4)
        out['corr'] = round(float(np.corrcoef(a, b)[0, 1]), 4)
    else:
        out['shared'] = int(both.sum())
        out['ratio'] = None; out['corr'] = None
    return out

def run_gl(qs, dumpbase):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WT)
    httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    wait_port(PORT)
    from playwright.sync_api import sync_playwright
    res = {'qs': qs}
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--enable-unsafe-swiftshader'])
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
                open(REFDIR + dumpbase + '.png', 'wb').write(base64.b64decode(url.split(',', 1)[1]))
                res['dump'] = dumpbase + '.png'
            else:
                res['no_dump'] = True
            res['gate'] = {k: gate.get(k) for k in ('corr', 'js_mean', 'ref_mean', 'draws', 'glerr')}
            up = page.evaluate('window.__UPLOAD && window.__UPLOAD()')
            if up:
                res['upload'] = up
            gc = page.evaluate('window.__GPUCHECK || null')
            if gc:
                res['gpucheck'] = gc
            res['pageerrs'] = errs[:3]
            browser.close()
    finally:
        httpd.shutdown()
        httpd.server_close()
    return res

def main():
    steps = [1, 2, 3, 4]
    table = []
    audit = None
    gpucheck = None
    # CPU refs first
    cpu_png = {s: gen_cpu(s) for s in steps}
    for fix in (0, 1):
        for s in steps:
            glstep = s if s < 4 else 4       # step5 run mapped below
            qs = ('?mat=73&bb=%s&nodepth=1&upload=1&step=%d&fix=%d' % (BB, s, fix)) if s != 5 else \
                 ('?mat=73&bb=%s&nodepth=1&upload=1&step=5&fix=%d' % (BB, fix))
            dump = 's52_gl_fix%d_step%d' % (fix, s)
            print('GL fix=%d step=%d ...' % (fix, s), flush=True)
            r = run_gl(qs, dump)
            if 'dump' in r:
                cpupng = cpu_png[4] if s == 5 else cpu_png[s]
                m = cmp_pair(REFDIR + r['dump'], cpupng)
                m.update({'step': s, 'fix': fix, 'pageerrs': r.get('pageerrs')})
                table.append(m)
                print('  step %d fix %d: %s' % (s, fix, m), flush=True)
            if fix == 0 and 'upload' in r:
                audit = r['upload']
            if fix == 1 and s == 4 and 'gpucheck' in r:
                gpucheck = r['gpucheck']
    # whole-zone sanity (no step knob): original vs fixed, vs s50 zbuf ref
    zref = REFDIR + 's50_ref_zbuf_snap.png'
    zone = []
    if os.path.exists(zref):
        for fix in (0, 1):
            dump = 's52_gl_zone_fix%d' % fix
            print('GL zone fix=%d ...' % fix, flush=True)
            r = run_gl('?upload=1&fix=%d' % fix, dump)
            if 'dump' in r:
                m = cmp_pair(REFDIR + r['dump'], zref)
                m['fix'] = fix
                zone.append(m)
                print('  zone fix=%d: %s' % (fix, m), flush=True)
    out = {'sign_convention': {'covered': 'mean RGB > 8', 'ratio': 'GL/CPU covered-mean',
                               'diverge': '|ratio-1|>0.05 or corr<0.99',
                               'steps': '1 UV, 2 diffuse, 3 D*LM, 4 D*LM*2, 5 +fog(inert)'},
           'bisect_table': table, 'zone': zone, 'gpucheck': gpucheck}
    if audit:
        m73 = [b for b in audit.get('batches', []) if b.get('mid') == 73]
        clob = [b for b in audit.get('batches', []) if b.get('CLOBBER')]
        out['mat73_audit'] = m73
        out['clobbered_mids'] = [b['mid'] for b in clob]
        out['n_lmfx_batches'] = len(audit.get('batches', []))
    json.dump(out, open(OUTJSON, 'w'), indent=1)
    print('saved', OUTJSON)

if __name__ == '__main__':
    main()
