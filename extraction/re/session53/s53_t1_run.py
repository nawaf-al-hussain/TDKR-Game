#!/usr/bin/env python3
"""s53 T1 runner: full-zone unit audit (every draw), wrongLM calibration, per-effect GL renders.
Sign conventions (declared BEFORE reading results):
  unit audit : per draw, assert unit0 == batch diffuse (bn0) and, for LM effects, unit1 == bn1.
               mismatch count > 0 FAILS. noTex draws (unresolvable texture) counted separately.
  corr       = Pearson r over ALL pixels (page) or over shared-covered px (offline, mean RGB > 8 both)
  ratio      = GL_covered_mean / CPU_covered_mean (1.0 == agreement)
  calibration: wronglm=1 (bake-page rotation A0->B0->Roads0) must (a) drop whole-zone corr vs the
               fixed run and (b) make the unit audit report mismatches > 0 (positive control).
"""
import json, time, socket, threading, http.server, functools, base64, sys, os
import numpy as np
from PIL import Image

PORT = 8153
WT = '/tmp/my-project/work/city_slice_wt'
PAGE = "/playable/city_bisect2.html"
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
REFDIR = WT + '/playable/'
OUTDIR = '/tmp/my-project/work/TDKR-Game/extraction/re/session53/'
OUTJSON = OUTDIR + 's53_t1_audit.json'
FAMILIES = ['LightMapDC', 'AlphaMasking', 'SimpleAdditive', 'StandardDiffuseDC', 'other']

def wait_port(port, timeout=20):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1):
                return True
        except OSError:
            time.sleep(0.25)
    return False

def run_gl(qs, dumpbase, timeout_s=300):
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
            t0 = time.time()
            for _ in range(int(timeout_s)):
                time.sleep(1)
                gate = page.evaluate('window.__GATE || {}')
                if gate.get('done'):
                    break
            res['elapsed_s'] = round(time.time() - t0, 1)
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

def audit_summary(up):
    if not up:
        return None
    bs = up.get('batches', [])
    mm = [b for b in bs if b.get('MM')]
    return {'draws': len(bs),
            'lmfx': sum(1 for b in bs if b.get('bn1')),
            'mismatches': len(mm),
            'noTex': sum(1 for b in bs if b.get('noTex')),
            'lmMissing': sum(1 for b in bs if b.get('lmMissing')),
            'first_mm': mm[:5],
            'fx_breakdown': {f: sum(1 for b in bs if b.get('fx') == f) for f in FAMILIES}}

def wait_cpu_ref(fx, timeout_s=2400):
    p = REFDIR + 's53_ref_%s.png' % fx
    t0 = time.time()
    while not os.path.exists(p) and time.time() - t0 < timeout_s:
        time.sleep(10)
    return os.path.exists(p)

def main():
    os.makedirs(OUTDIR, exist_ok=True)
    out = {'sign_convention': {
        'unit_audit': 'per draw: unit0==diffuse(bn0), LM effects unit1==bn1; mismatches>0 FAILS',
        'corr': 'Pearson r, offline over shared covered px (mean RGB>8 both), GL flipped to top-down',
        'ratio': 'GL/CPU covered-mean',
        'wronglm_calibration': 'wrong page rotation must LOWER corr and RAISE audit mismatches'}}

    # R1: fixed whole-zone run with the full every-draw audit
    print('R1 zone fix=1 upload=1 ...', flush=True)
    r1 = run_gl('?upload=1&fix=1&gpucheck=1', 's53_gl_zone_fix1')
    out['zone_fix1'] = {'gate': r1['gate'], 'elapsed_s': r1.get('elapsed_s'),
                        'pageerrs': r1.get('pageerrs'),
                        'audit': audit_summary(r1.get('upload')),
                        'gpucheck_lines': (r1.get('gpucheck') or '').splitlines()}
    if os.path.exists(REFDIR + 's50_ref_zbuf_snap.png'):
        out['zone_fix1']['vs_s50_cpu_ref'] = cmp_pair(REFDIR + 's53_gl_zone_fix1.png',
                                                      REFDIR + 's50_ref_zbuf_snap.png')

    # R2: wrongLM calibration (audit positive control + corr must move)
    print('R2 zone fix=1 wronglm=1 ...', flush=True)
    r2 = run_gl('?upload=1&fix=1&wronglm=1&gpucheck=1', 's53_gl_zone_wronglm')
    out['zone_wronglm'] = {'gate': r2['gate'], 'pageerrs': r2.get('pageerrs'),
                           'audit': audit_summary(r2.get('upload')),
                           'gpucheck_lines': (r2.get('gpucheck') or '').splitlines()}
    if os.path.exists(REFDIR + 's50_ref_zbuf_snap.png'):
        out['zone_wronglm']['vs_s50_cpu_ref'] = cmp_pair(REFDIR + 's53_gl_zone_wronglm.png',
                                                         REFDIR + 's50_ref_zbuf_snap.png')

    # R3: per-effect GL renders (fixed)
    out['per_effect'] = {}
    for fx in FAMILIES:
        print('R3 GL only=%s ...' % fx, flush=True)
        r = run_gl('?only=%s&fix=1&upload=1' % fx, 's53_gl_fx_%s' % fx)
        rec = {'gate': r['gate'], 'pageerrs': r.get('pageerrs'),
               'audit': audit_summary(r.get('upload'))}
        cpupng = REFDIR + 's53_ref_%s.png' % fx
        if os.path.exists(cpupng) and os.path.exists(REFDIR + r['dump']):
            rec['vs_cpu_ref'] = cmp_pair(REFDIR + r['dump'], cpupng)
        else:
            rec['missing_ref'] = True   # offline comparison in s53_t1_gap.py once CPU refs finish
        out['per_effect'][fx] = rec
        print('  %s: %s' % (fx, rec.get('vs_cpu_ref')), flush=True)
        json.dump(out, open(OUTJSON, 'w'), indent=1)   # incremental save

    json.dump(out, open(OUTJSON, 'w'), indent=1)
    print('saved', OUTJSON)

if __name__ == '__main__':
    main()
