#!/usr/bin/env python3
"""Playable screenshot gate - v21+ release gate (s38 T1d).

Takes a headless-chromium screenshot of gh-pages/playable/index.html#freeze0.5&gate
and FAILS (exit 1) if the rendered character silhouette fails any of:
  - IoU vs the numpy-skinned reference projection < 0.80
  - IoU margin over the ROTATED-reference null < 0.25 (upright discrimination)
  - bbox aspect vs reference off by > 15%
  - feet not near ground (numpy min world-y outside [0, 0.35] m)
  - albedo closer to the untextured grey than to the texture mean
Usage: python3 playable_screenshot_gate.py [--playable-dir DIR] [--json OUT]
"""
import argparse, json, os, struct, subprocess, sys, time
import numpy as np
from PIL import Image, ImageDraw

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir))
TRUTH = '/home/z/my-project/scripts/jsverify/s38_truth/_001_idle_stand.npz'
TEX_MEAN = np.array([31.4, 31.0, 31.0])
GREY = np.array([0.75 * 255] * 3)
PORT = 8898


def look_at(eye, tgt):
    f = tgt - eye; f = f / np.linalg.norm(f)
    up = np.array([0, 1, 0.0])
    s = np.cross(f, up); s = s / np.linalg.norm(s)
    u = np.cross(s, f)
    M = np.eye(4)
    M[0, :3] = s; M[1, :3] = u; M[2, :3] = -f
    M[:3, 3] = np.array([-np.dot(s, eye), -np.dot(u, eye), np.dot(f, eye)])
    return M


def perspective(fov_y, aspect, near, far):
    t = 1 / np.tan(fov_y / 2)
    M = np.zeros((4, 4))
    M[0, 0] = t / aspect; M[1, 1] = t
    M[2, 2] = -(far + near) / (far - near); M[2, 3] = -2 * far * near / (far - near)
    M[3, 2] = -1
    return M


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--playable-dir', default=os.path.join(REPO, 'gh-pages', 'playable'))
    ap.add_argument('--json', default=None)
    args = ap.parse_args()
    PDIR = args.playable_dir
    W, H = 1280, 720

    # ---- numpy reference from the verified truth (idle @ 0.5 s)
    z = np.load(TRUTH)
    Vref = z['t500'].astype(np.float64)
    patch = json.load(open(os.path.join(PDIR, 'patch.json')))
    spawn = patch['spawns'][0]['pos']
    P = np.array([spawn[0], spawn[1], spawn[2] + 0.9])
    R = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]], float)
    Vw = Vref @ R.T + np.array([P[0], P[2] - 0.9, -P[1]])
    CAM_POS = np.array([P[0], P[2] + 0.2, -P[1] + 4.2])
    CAM_TGT = np.array([P[0], P[2] + 0.1, -P[1]])
    VIEW = look_at(CAM_POS, CAM_TGT)
    PROJ = perspective(np.radians(60), W / H, 0.1, 800)

    buf = open(os.path.join(PDIR, 'batman.glb'), 'rb').read()
    jl = struct.unpack('<I', buf[12:16])[0]
    gj = json.loads(buf[20:20 + jl]); bin_off = 20 + jl + 8
    prim = gj['meshes'][0]['primitives'][0]
    def acc(ai):
        a = gj['accessors'][ai]; bv = gj['bufferViews'][a['bufferView']]
        off = bin_off + bv.get('byteOffset', 0) + a.get('byteOffset', 0)
        n = a['count']
        return (np.frombuffer(buf, np.float32, n * 3, off).reshape(n, 3)
                if a['type'] == 'VEC3' else np.frombuffer(buf, np.uint16, n, off))
    verts_g = acc(prim['attributes']['POSITION']).astype(np.float64)
    idx_g = acc(prim['indices']).astype(int).reshape(-1, 3)

    def project(V):
        Vh = np.hstack([V, np.ones((len(V), 1))])
        clip = Vh @ (PROJ @ VIEW).T
        ndc = clip[:, :3] / clip[:, 3:4]
        return ((ndc[:, 0] * .5 + .5) * W, (1 - (ndc[:, 1] * .5 + .5)) * H)

    def silhouette(V):
        px, py = project(V)
        im = Image.new('L', (W, H), 0)
        d = ImageDraw.Draw(im)
        for tri in idx_g:
            pts = [(px[i], py[i]) for i in tri]
            d.polygon(pts, fill=255)
        return np.array(im) > 127

    ref = silhouette(Vw)
    Vwrong = np.load(TRUTH)['t3450'].astype(np.float64)
    Vwrong_w = Vwrong @ R.T + np.array([P[0], P[2] - 0.9, -P[1]])
    # THE regression this gate exists to catch: the model rendered WITHOUT the
    # z-up->y-up rotation (lying on his side, the v20 live bug). Null = the
    # unrotated reference projection.
    Vrot_w = Vref + np.array([P[0], P[2] - 0.9, -P[1]])

    def iou(a, b):
        u = (a | b).sum()
        return float((a & b).sum() / u) if u else 0.0

    # ---- browser screenshot
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT), '-d', PDIR],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ok = False
    try:
        time.sleep(0.8)
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            b = pw.chromium.launch()
            pg = b.new_page(viewport={'width': W, 'height': H})
            pg.goto(f'http://127.0.0.1:{PORT}/index.html#freeze0.5&gate')
            pg.wait_for_function('window.__frozen !== undefined', timeout=20000)
            pg.wait_for_timeout(700)
            pg.screenshot(path='/tmp/gate_playable.png')
            b.close()
        ok = True
    finally:
        srv.terminate()
    if not ok:
        print('GATE FAIL: screenshot could not be taken')
        sys.exit(1)
    shot = np.array(Image.open('/tmp/gate_playable.png').convert('RGB'))
    fg = ~(shot > 240).all(2)
    if fg.mean() < 0.005:
        print('GATE FAIL: character not visible in screenshot (fg %.3f%%)' % (fg.mean() * 100))
        sys.exit(1)

    m_iou = iou(fg, ref)
    n_rot = iou(fg, silhouette(Vrot_w))       # null: LYING (unrotated) reference
    n_wrong = iou(fg, silhouette(Vwrong_w))   # null: wrong idle pose

    def bbox(m):
        rows = np.where(m.any(1))[0]; cols = np.where(m.any(0))[0]
        return rows[0], rows[-1], cols[0], cols[-1]
    rb, fb = bbox(ref), bbox(fg)
    a_ref = (rb[1] - rb[0]) / max(1, rb[3] - rb[2])
    a_br = (fb[1] - fb[0]) / max(1, fb[3] - fb[2])

    min_y = float(Vw[:, 1].min())
    mean_rgb = shot[fg].mean(0)
    d_tex = float(np.abs(mean_rgb - TEX_MEAN).mean())
    d_grey = float(np.abs(mean_rgb - GREY).mean())

    res = {
        'iou': round(m_iou, 4), 'iou_null_unrotated_lying': round(n_rot, 4),
        'iou_null_wrong_pose': round(n_wrong, 4),
        'aspect_reference': round(float(a_ref), 3), 'aspect_browser': round(float(a_br), 3),
        'ground_min_y_m': round(min_y, 4),
        'albedo_dist_to_texture': round(d_tex, 1), 'albedo_dist_to_grey': round(d_grey, 1),
        'thresholds': {'iou_min': 0.80, 'iou_margin_over_rotated_min': 0.25,
                       'aspect_rel_diff_max': 0.15, 'ground_min_y_range': [0.0, 0.35],
                       'albedo_dist_to_texture_max': 40.0, 'albedo_dist_to_grey_min': 60.0},
    }
    fails = []
    if m_iou < 0.80: fails.append(f'IoU {m_iou:.3f} < 0.80')
    if m_iou - n_rot < 0.25: fails.append(f'IoU margin over lying(unrotated) null {m_iou-n_rot:.3f} < 0.25')
    if abs(a_br / a_ref - 1) > 0.15: fails.append(f'aspect off {a_br:.3f} vs {a_ref:.3f} > 15%')
    if not (0.0 <= min_y <= 0.35): fails.append(f'feet off ground: min world-y {min_y:.3f}')
    if d_tex > 40.0: fails.append(f'albedo far from texture: {d_tex:.1f} > 40')
    if d_grey < 60.0: fails.append(f'albedo close to untextured grey: {d_grey:.1f} < 60')
    res['fail'] = fails
    if args.json:
        json.dump(res, open(args.json, 'w'), indent=1)
    print(json.dumps(res, indent=1))
    if fails:
        print('PLAYABLE SCREENSHOT GATE FAIL')
        sys.exit(1)
    print('PLAYABLE SCREENSHOT GATE PASS')


if __name__ == '__main__':
    main()
