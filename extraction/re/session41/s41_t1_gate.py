#!/usr/bin/env python3
"""S41 T1: deployment gate covering EVERY gh-pages page (local tree), plus
syntax-error negative controls for each page.

Pages (gh-pages @582a0d0, served locally from the worktree):
  street  /index.html               street viewer (window.__v hook)
  batman  /playable/index.html#freeze0.5&gate   skinned Batman viewer (IoU vs numpy truth)
  pipe    /playable/pipeline.html   user-zip pipeline (READY + street SHA)

FAIL criteria per page: any console error, pageerror, requestfailed, non-2xx
response, or unmet DOM/canvas expectation.
Negative controls: a copy of each page with an injected SyntaxError script
must be flagged by the SAME monitor.
"""
import functools, hashlib, http.server, io, json, os, struct, threading
import numpy as np
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

ROOT = '/tmp/my-project/work/ghpages_live_wt'
NEG = '/tmp/s41_neg'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
TRUTH = '/home/z/my-project/scripts/jsverify/s38_truth'
OUT = '/home/z/my-project/scripts/s41_t1_gate.json'
STREET_SHA_REF = '52fcbf324bdd24146b6261da45fc74f4dc9a1dd3715a9c1f71c83bc615331736'
W, H = 1280, 720
INJECT = '<script>const __s41gate=(;</script>'  # guaranteed SyntaxError


def serve(root, port):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=root)
    httpd = http.server.ThreadingHTTPServer(('127.0.0.1', port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return port


def monitor(pg, tag, res):
    pg.on('console', lambda m: res[tag]['errors'].append(f'console:{m.text[:200]}') if m.type == 'error' else None)
    pg.on('pageerror', lambda e: res[tag]['errors'].append(f'pageerror:{str(e)[:200]}'))
    pg.on('requestfailed', lambda r: res[tag]['errors'].append(f'reqfail:{r.url[:120]}'))
    pg.on('response', lambda r: res[tag]['non2xx'].append(f'{r.status}:{r.url[:120]}') if r.status >= 400 else None)


def bg_fraction(png_path):
    shot = np.array(Image.open(png_path).convert('RGB'))
    fg = ~(shot > 240).all(2)
    return float(fg.mean())


# ---- batman reference silhouette (local GLB + numpy truth), s39 method ----
def batman_refs():
    glb = open(f'{ROOT}/playable/batman.glb', 'rb').read()
    jl = struct.unpack('<I', glb[12:16])[0]
    gj = json.loads(glb[20:20 + jl]); bin_off = 20 + jl + 8
    prim = gj['meshes'][0]['primitives'][0]

    def acc(ai):
        a = gj['accessors'][ai]; bv = gj['bufferViews'][a['bufferView']]
        off = bin_off + bv.get('byteOffset', 0) + a.get('byteOffset', 0)
        n, t = a['count'], a['type']
        if t == 'VEC3': return np.frombuffer(glb, np.float32, n * 3, off).reshape(n, 3)
        return np.frombuffer(glb, np.uint16, n, off)

    V = acc(prim['attributes']['POSITION']).astype(np.float64)
    idx = acc(prim['indices']).astype(int).reshape(-1, 3)
    patch = json.load(open(f'{ROOT}/playable/patch.json'))
    s = patch['spawns'][0]['pos']
    P = np.array([s[0], s[1], s[2] + 0.9])
    R = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]], float)
    OFF = np.array([P[0], P[2] - 0.9, -P[1]])

    def world(Vf): return Vf @ R.T + OFF

    def look_at(eye, tgt):
        f = tgt - eye; f = f / np.linalg.norm(f)
        up = np.array([0, 1, 0.0]); sx = np.cross(f, up); sx /= np.linalg.norm(sx)
        u = np.cross(sx, f); M = np.eye(4)
        M[0, :3] = sx; M[1, :3] = u; M[2, :3] = -f
        M[:3, 3] = [-np.dot(sx, eye), -np.dot(u, eye), np.dot(f, eye)]
        return M

    def persp(fov, asp, near, far):
        t = 1 / np.tan(fov / 2); M = np.zeros((4, 4))
        M[0, 0] = t / asp; M[1, 1] = t
        M[2, 2] = -(far + near) / (far - near); M[2, 3] = -2 * far * near / (far - near); M[3, 2] = -1
        return M

    CAM = np.array([P[0], P[2] + 0.2, -P[1] + 4.2]); TGT = np.array([P[0], P[2] + 0.1, -P[1]])
    PV = persp(np.radians(60), W / H, 0.1, 800) @ look_at(CAM, TGT)

    def silhouette(Vv):
        Vh = np.hstack([Vv, np.ones((len(Vv), 1))]); clip = Vh @ PV.T
        ndc = clip[:, :3] / clip[:, 3:4]
        px = (ndc[:, 0] * .5 + .5) * W; py = (1 - (ndc[:, 1] * .5 + .5)) * H
        im = Image.new('L', (W, H), 0); d = ImageDraw.Draw(im)
        for tri in idx: d.polygon([(px[i], py[i]) for i in tri], fill=255)
        return np.array(im) > 127

    def iou(a, b):
        u = (a | b).sum()
        return float((a & b).sum() / u) if u else 0.0

    zi = np.load(f'{TRUTH}/_001_idle_stand.npz')
    ref = silhouette(world(zi['t500'].astype(np.float64)))
    lying = silhouette(zi['t500'].astype(np.float64) + OFF)
    wrong = silhouette(world(zi['t3450'].astype(np.float64)))
    shift = silhouette(world(zi['t500'].astype(np.float64)) + np.array([1.2, 0, 0]))
    return iou, ref, lying, wrong, shift


def run_page(b, url, tag, res, timeout_ms=45000):
    pg = b.new_page(viewport={'width': W, 'height': H})
    monitor(pg, tag, res)
    pg.goto(url, wait_until='domcontentloaded', timeout=60000)
    return pg


def main():
    res = {t: {'errors': [], 'non2xx': [], 'ok': None, 'detail': {}} for t in
           ('street', 'batman', 'pipe', 'ctl_street', 'ctl_batman', 'ctl_pipe')}
    iou_fn, ref, lying, wrong, shift = batman_refs()

    # negative-control overlay: REAL dirs + file symlinks only (never a dir
    # symlink that aliases ROOT); corrupted page written behind a ROOT-alias guard
    def build_farm(sub, page_in_playable):
        base = f'{NEG}/{sub}'
        os.makedirs(base, exist_ok=True)
        os.makedirs(f'{base}/playable', exist_ok=True)
        os.makedirs(f'{base}/models', exist_ok=True)
        root_real = os.path.realpath(ROOT)
        for entry in os.listdir(ROOT):
            src = f'{ROOT}/{entry}'
            if entry.startswith('.') or os.path.isdir(src): continue
            os.symlink(src, f'{base}/{entry}')
        for entry in os.listdir(f'{ROOT}/models'):
            src = f'{ROOT}/models/{entry}'
            if entry.startswith('.') or os.path.isdir(src): continue
            os.symlink(src, f'{base}/models/{entry}')
        for entry in os.listdir(f'{ROOT}/playable'):
            src = f'{ROOT}/playable/{entry}'
            if entry.startswith('.') or os.path.isdir(src): continue
            os.symlink(src, f'{base}/playable/{entry}')
        htmlp = f'{base}/playable/{page_in_playable}' if page_in_playable else f'{base}/index.html'
        # the PARENT must be a real dir (not a symlink aliasing ROOT) — then
        # os.remove(htmlp) removes a file symlink we created, never a ROOT file
        assert not os.path.realpath(os.path.dirname(htmlp)).startswith(root_real), 'parent aliases ROOT'
        if os.path.lexists(htmlp): os.remove(htmlp)  # removes the file symlink only
        src_html = f'{ROOT}/playable/{page_in_playable}' if page_in_playable else f'{ROOT}/index.html'
        html = open(src_html).read()
        head = html.find('<head>')
        assert head >= 0
        open(htmlp, 'w').write(html[:head + 6] + INJECT + html[head + 6:])

    os.makedirs(NEG, exist_ok=True)
    build_farm('street', None)
    build_farm('batman', 'index.html')
    build_farm('pipe', 'pipeline.html')

    serve(ROOT, 8131)
    serve(NEG, 8132)

    with sync_playwright() as p:
        b = p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader'])

        # ---- street viewer (local) ----
        pg = run_page(b, 'http://127.0.0.1:8131/index.html', 'street', res)
        try:
            pg.wait_for_function('window.__v && window.__v.scene && window.__v.scene.children.length > 0', timeout=60000)
            pg.wait_for_timeout(8000)
            d = res['street']['detail']
            d['scene_children'] = pg.evaluate('window.__v.scene.children.length')
            d['load_status'] = pg.evaluate("document.querySelector('#load-status') ? document.querySelector('#load-status').textContent : null")
            d['tris_text'] = pg.evaluate("document.querySelector('#st-tris') ? document.querySelector('#st-tris').textContent : null")
            pg.screenshot(path='/home/z/my-project/scripts/s41_gate_street.png')
            d['fg_fraction'] = round(bg_fraction('/home/z/my-project/scripts/s41_gate_street.png'), 4)
            ok = (not res['street']['errors'] and not res['street']['non2xx']
                  and d['scene_children'] > 0 and d['fg_fraction'] > 0.005)
        except Exception as e:
            res['street']['errors'].append(f'gate:{str(e)[:200]}'); ok = False
        res['street']['ok'] = ok
        pg.close()

        # ---- batman viewer (local) ----
        pg = run_page(b, 'http://127.0.0.1:8131/playable/index.html#freeze0.5&gate', 'batman', res)
        try:
            pg.wait_for_function('window.__frozen !== undefined', timeout=45000)
            pg.wait_for_timeout(800)
            pg.screenshot(path='/home/z/my-project/scripts/s41_gate_batman.png')
            shot = np.array(Image.open('/home/z/my-project/scripts/s41_gate_batman.png').convert('RGB'))
            fg = ~(shot > 240).all(2)
            d = res['batman']['detail']
            d['iou'] = round(iou_fn(fg, ref), 4)
            d['iou_null_lying'] = round(iou_fn(fg, lying), 4)
            d['iou_null_wrong'] = round(iou_fn(fg, wrong), 4)
            d['iou_null_shift'] = round(iou_fn(fg, shift), 4)
            d['fg_fraction'] = round(float(fg.mean()), 4)
            ok = (not res['batman']['errors'] and not res['batman']['non2xx']
                  and d['iou'] > 0.80 and d['iou'] - d['iou_null_lying'] > 0.25
                  and 0.005 < d['fg_fraction'] < 0.9)
        except Exception as e:
            res['batman']['errors'].append(f'gate:{str(e)[:200]}'); ok = False
        res['batman']['ok'] = ok
        pg.close()

        # ---- pipeline (local, real zip) ----
        pg = run_page(b, 'http://127.0.0.1:8131/playable/pipeline.html', 'pipe', res)
        try:
            pg.set_input_files('#f', ZIP)
            pg.wait_for_function("document.querySelector('#log').textContent.includes('READY')", timeout=180000)
            pg.wait_for_timeout(2000)
            d = res['pipe']['detail']
            d['street_sha'] = pg.evaluate("""async () => {
                if (!window.__streetRGBA) return null;
                const h = await crypto.subtle.digest('SHA-256', window.__streetRGBA);
                return [...new Uint8Array(h)].map(x => x.toString(16).padStart(2,'0')).join('');
            }""")
            d['err_box'] = pg.evaluate("document.querySelector('#err').textContent")
            d['sha_match'] = (d['street_sha'] == STREET_SHA_REF)
            pg.screenshot(path='/home/z/my-project/scripts/s41_gate_pipe.png')
            ok = (not res['pipe']['errors'] and not res['pipe']['non2xx']
                  and d['sha_match'] and not d['err_box'].strip())
        except Exception as e:
            res['pipe']['errors'].append(f'gate:{str(e)[:200]}'); ok = False
        res['pipe']['ok'] = ok
        pg.close()

        # ---- negative controls: each MUST be flagged ----
        for sub, url, tag in (
                ('street', 'http://127.0.0.1:8132/street/index.html', 'ctl_street'),
                ('batman', 'http://127.0.0.1:8132/batman/playable/index.html', 'ctl_batman'),
                ('pipe', 'http://127.0.0.1:8132/pipe/playable/pipeline.html', 'ctl_pipe')):
            pg = run_page(b, url, tag, res)
            try:
                pg.wait_for_timeout(5000)
            except Exception:
                pass
            flagged = bool(res[tag]['errors'])
            res[tag]['detail']['flagged'] = flagged
            res[tag]['detail']['first_error'] = res[tag]['errors'][0][:160] if res[tag]['errors'] else None
            res[tag]['ok'] = flagged  # ok means the control WORKED (gate failed the page)
            try: pg.close()
            except Exception: pass

        b.close()

    gates = {t: res[t]['ok'] for t in ('street', 'batman', 'pipe')}
    ctrls = {t: res[t]['ok'] for t in ('ctl_street', 'ctl_batman', 'ctl_pipe')}
    print(json.dumps({t: {'ok': res[t]['ok'], 'errors': res[t]['errors'][:4],
                          'detail': res[t]['detail']} for t in res}, indent=1)[:3500])
    print('PAGES:', gates)
    print('CONTROLS (True = correctly flagged):', ctrls)
    verdict = all(gates.values()) and all(ctrls.values())
    print('S41 T1 LOCAL GATE:', 'PASS' if verdict else 'FAIL')
    json.dump(res, open(OUT, 'w'), indent=1)
    return 0 if verdict else 1


if __name__ == '__main__':
    raise SystemExit(main())
