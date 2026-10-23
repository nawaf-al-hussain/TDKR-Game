#!/usr/bin/env python3
"""s54 T4 runner: zoomed per-effect correlation for the n-limited families.
Sign conventions (declared before results, same as s53):
  corr  = Pearson r over shared covered px (mean RGB > 8 both), GL flipped top-down
  ratio = GL_covered_mean / CPU_covered_mean (1.0 == agreement)
  calibration: ?wronglm=1 must LOWER corr on LM-using pixels (positive control)
Windows: StandardDiffuseDC concentrated in mid13+mid14 (x[-927,-368] z[-1157,-739]);
AlphaMasking mid144 (x[-922,-1135... ] -> x[-922,-670] z[-1135,-541]).
"""
import json, time, socket, threading, http.server, functools, base64, sys, os
import numpy as np
from PIL import Image

PORT = 8159
WT = '/tmp/my-project/work/city_slice_wt'
PAGE = "/playable/city_bisect2.html"
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
REFDIR = WT + '/playable/'
OUTDIR = '/tmp/my-project/work/TDKR-Game/extraction/re/session54/'
OUTJSON = OUTDIR + 's54_t4_pereffect.json'

WINS = {
    'StandardDiffuseDC': '-700,-1000,-600,-941',
    'AlphaMasking': '-680,-910,-620,-850',
}
LAB = {  # flat-label geometry masks (px >= 128), from s54_t4_cpu.py --flat
    'StandardDiffuseDC': REFDIR + 's54_labSD_final.png',
    'AlphaMasking': REFDIR + 's54_labAM_final.png',
}
FAMILIES = ['StandardDiffuseDC', 'AlphaMasking']

def wait_port(port, timeout=20):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1):
                return True
        except OSError:
            time.sleep(0.25)
    return False

def run_gl(qs, dumpbase, timeout_s=280):
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
            res['pageerrs'] = errs[:3]
            browser.close()
    finally:
        httpd.shutdown()
        httpd.server_close()
    return res

def load_rgb(p):
    return np.asarray(Image.open(p).convert('RGB'), np.float64)

def cmp_pair(glp, refp, labp=None):
    gl = load_rgb(glp)[::-1]
    ref = load_rgb(refp)
    h = min(gl.shape[0], ref.shape[0]); w = min(gl.shape[1], ref.shape[1])
    if gl.shape != ref.shape:
        gl = gl[:h, :w]; ref = ref[:h, :w]
    gm = gl.mean(axis=2); rm = ref.mean(axis=2)
    if labp and os.path.exists(labp):
        lab = np.asarray(Image.open(labp).convert('L'), np.float64)[:h, :w]
        geo = lab >= 128
        both = geo & (gm > 0) & (rm > 0)      # geometry mask, value-free
        mode = 'label_mask'
    else:
        gcm = gm > 8; rcm = rm > 8
        both = gcm & rcm
        mode = 'mean_gt8'
    out = {'mode': mode,
           'gl_cov_pct': round(100 * float((gm > 0).mean()), 3),
           'cpu_cov_pct': round(100 * float((rm > 0).mean()), 3),
           'iou': round(float(both.sum()) / max(1, ((gm > 0) | (rm > 0)).sum()), 4)}
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

def main():
    out = {'sign_convention': 'corr = Pearson r over shared covered px (mean RGB>8 both); '
           'ratio = GL/CPU covered mean; wronglm must LOWER corr (positive control); '
           'windows chosen from s54_t4_cpu.py --matstats concentration analysis',
           'windows': WINS}
    only = sys.argv[1] if len(sys.argv) > 1 else 'all'
    for fx in FAMILIES:
        if only not in ('all', fx):
            continue
        win = WINS[fx]
        rec = {}
        cpupng = REFDIR + 's54_ref_%s_win.png' % fx
        labp = LAB.get(fx)
        # GL fixed
        print('GL %s fix=1 bb=%s ...' % (fx, win), flush=True)
        r1 = run_gl('?only=%s&fix=1&bb=%s' % (fx, win), 's54_gl_%s_win' % fx)
        rec['gl_fixed'] = {'elapsed_s': r1.get('elapsed_s'), 'pageerrs': r1.get('pageerrs'),
                           'dump': r1.get('dump')}
        if os.path.exists(REFDIR + r1['dump']) and os.path.exists(cpupng):
            rec['gl_fixed']['vs_cpu'] = cmp_pair(REFDIR + r1['dump'], cpupng, labp)
        # GL wronglm calibration
        print('GL %s wronglm=1 ...' % fx, flush=True)
        r2 = run_gl('?only=%s&fix=1&wronglm=1&bb=%s' % (fx, win), 's54_gl_%s_win_wronglm' % fx)
        rec['gl_wronglm'] = {'elapsed_s': r2.get('elapsed_s'), 'pageerrs': r2.get('pageerrs')}
        if os.path.exists(REFDIR + r2['dump']) and os.path.exists(cpupng):
            rec['gl_wronglm']['vs_cpu'] = cmp_pair(REFDIR + r2['dump'], cpupng, labp)
        # negative control: GL vs the OTHER family's CPU ref over the same geometry mask
        other = 'AlphaMasking' if fx == 'StandardDiffuseDC' else 'StandardDiffuseDC'
        oref = REFDIR + 's54_ref_%s_win.png' % other
        if os.path.exists(oref) and os.path.exists(REFDIR + r1['dump']):
            rec['negative_control_cross_family'] = cmp_pair(REFDIR + r1['dump'], oref, labp)
        out[fx] = rec
        json.dump(out, open(OUTJSON, 'w'), indent=1)
        print(fx, '->', json.dumps(rec.get('gl_fixed', {}).get('vs_cpu')), flush=True)
    json.dump(out, open(OUTJSON, 'w'), indent=1)
    print('saved', OUTJSON)

if __name__ == '__main__':
    main()
