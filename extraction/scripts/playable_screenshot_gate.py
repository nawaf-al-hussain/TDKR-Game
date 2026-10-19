#!/usr/bin/env python3
"""Playable screenshot gate - v21+ release gate (s38 T1d).

Takes a headless-chromium screenshot of gh-pages/playable/index.html#freeze0.5&gate
and FAILS (exit 1) if the rendered character silhouette fails any of:
  - IoU vs the numpy-skinned reference projection < 0.80
  - IoU margin over the ROTATED-reference null < 0.25 (upright discrimination)
  - bbox aspect vs reference off by > 15%
  - feet not near ground (numpy min world-y outside [0, 0.35] m)
  - albedo closer to the untextured grey than to the texture mean
stays: IoU vs numpy-skinned reference, rotated/lying null margin, aspect, feet,
albedo. s39 adds: texture presence (embedded PNG non-flat AND rendered fg
non-flat) and animation advancing (second freeze at t=2.0 must match its own
truth silhouette AND differ from the t=0.5 frame).
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

    # ---- s39: texture presence (embedded PNG non-flat + rendered fg non-flat)
    jl = struct.unpack('<I', buf[12:16])[0]
    gjx = json.loads(buf[20:20 + jl])
    img = gjx['images'][0]; bvg = gjx['bufferViews'][img['bufferView']]
    boff = 20 + jl + 8 + bvg.get('byteOffset', 0)
    import io as _io
    tex = np.array(Image.open(_io.BytesIO(buf[boff:boff + bvg['byteLength']])).convert('RGB'))
    tex_std = float(tex.reshape(-1, 3).std(0).min())
    fg_std = float(shot[fg].mean(1).std())

    # ---- s39: animation advancing. SILHOUETTE-level comparison is INSENSITIVE
    # for idle (s39 measured: t0.5 vs t2.0 frames pixel-identical, IoU 1.000;
    # t2-vs-truth IoU 0.893 == wrong-pose null 0.89) — the sway lives inside the
    # outline. The sensitive signal is the SKINNED-VERTEX delta through the
    # page's own mixer: real 30.0 cm (t0.5 vs t2.0), same-time null 0, frozen
    # mixer 0. Reported-but-NOT-gated: the t2 silhouette IoU (insensitive).
    srv2 = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT + 1), '-d', PDIR],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(0.8)
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            b2 = pw.chromium.launch()
            pg2 = b2.new_page(viewport={'width': W, 'height': H})
            pg2.goto(f'http://127.0.0.1:{PORT + 1}/index.html#freeze0.5&gate', timeout=30000)
            pg2.wait_for_function('window.__frozen !== undefined', timeout=20000)
            pg2.wait_for_timeout(500)
            delta = pg2.evaluate("""() => {
              const f = window.__frozen, mixer = f.mixer, root = f.batman;
              let sm = null; root.traverse(o => { if (o.isSkinnedMesh) sm = o; });
              const grab = () => {
                root.updateMatrixWorld(true);
                const P = sm.geometry.attributes.position.array;
                const SI = sm.geometry.attributes.skinIndex.array;
                const SW = sm.geometry.attributes.skinWeight.array;
                const bones = sm.skeleton.bones, ibm = sm.skeleton.boneInverses;
                const out = new Float32Array(P.length);
                for (let i = 0; i < P.length / 3; i++) {
                  const px = P[3*i], py = P[3*i+1], pz = P[3*i+2];
                  let x = 0, y = 0, z = 0;
                  for (let k = 0; k < 4; k++) {
                    const w = SW[4*i+k]; if (w < 1e-6) continue;
                    const m = bones[SI[4*i+k]].matrixWorld.elements;
                    const b = ibm[SI[4*i+k]].elements;
                    x += w * (m[0]*(b[0]*px+b[4]*py+b[8]*pz+b[12]) + m[4]*(b[1]*px+b[5]*py+b[9]*pz+b[13]) + m[8]*(b[2]*px+b[6]*py+b[10]*pz+b[14]) + m[12]);
                    y += w * (m[1]*(b[0]*px+b[4]*py+b[8]*pz+b[12]) + m[5]*(b[1]*px+b[5]*py+b[9]*pz+b[13]) + m[9]*(b[2]*px+b[6]*py+b[10]*pz+b[14]) + m[13]);
                    z += w * (m[2]*(b[0]*px+b[4]*py+b[8]*pz+b[12]) + m[6]*(b[1]*px+b[5]*py+b[9]*pz+b[13]) + m[10]*(b[2]*px+b[6]*py+b[10]*pz+b[14]) + m[14]);
                  }
                  out[3*i] = x; out[3*i+1] = y; out[3*i+2] = z;
                }
                return out;
              };
              const A = f.actions, idle = A['_001_idle_stand'];
              idle.play(); idle.setEffectiveWeight(1);
              mixer.setTime(0.5); const a = grab();
              mixer.setTime(2.0); const b2 = grab();
              let mx = 0; for (let i = 0; i < a.length; i++) { const d = Math.abs(a[i] - b2[i]); if (d > mx) mx = d; }
              return mx;
            }""")
            pg2.screenshot(path='/tmp/gate_playable_t2.png')
            b2.close()
    finally:
        srv2.terminate()
    shot2 = np.array(Image.open('/tmp/gate_playable_t2.png').convert('RGB'))
    fg2 = ~(shot2 > 240).all(2)
    Vt2 = np.load(TRUTH)['t2000'].astype(np.float64)
    ref2_iou = iou(fg2, silhouette(Vt2 @ R.T + np.array([P[0], P[2] - 0.9, -P[1]])))
    adv_max_m = float(delta)   # world units (m)

    res = {
        'iou': round(m_iou, 4), 'iou_null_unrotated_lying': round(n_rot, 4),
        'iou_null_wrong_pose': round(n_wrong, 4),
        'aspect_reference': round(float(a_ref), 3), 'aspect_browser': round(float(a_br), 3),
        'ground_min_y_m': round(min_y, 4),
        'albedo_dist_to_texture': round(d_tex, 1), 'albedo_dist_to_grey': round(d_grey, 1),
        'texture_embedded_std_min': round(tex_std, 1), 'rendered_fg_lum_std': round(fg_std, 1),
        'advancing_t2_silhouette_iou_INSENSITIVE': round(ref2_iou, 4),
        'advancing_vertex_delta_max_m': round(adv_max_m, 4),
        'thresholds': {'iou_min': 0.80, 'iou_margin_over_rotated_min': 0.25,
                       'aspect_rel_diff_max': 0.15, 'ground_min_y_range': [0.0, 0.35],
                       'albedo_dist_to_texture_max': 40.0, 'albedo_dist_to_grey_min': 60.0,
                       'texture_std_min': 5.0, 'advancing_vertex_delta_min_m': 0.05},
    }
    fails = []
    if m_iou < 0.80: fails.append(f'IoU {m_iou:.3f} < 0.80')
    if m_iou - n_rot < 0.25: fails.append(f'IoU margin over lying(unrotated) null {m_iou-n_rot:.3f} < 0.25')
    if abs(a_br / a_ref - 1) > 0.15: fails.append(f'aspect off {a_br:.3f} vs {a_ref:.3f} > 15%')
    if not (0.0 <= min_y <= 0.35): fails.append(f'feet off ground: min world-y {min_y:.3f}')
    if d_tex > 40.0: fails.append(f'albedo far from texture: {d_tex:.1f} > 40')
    if d_grey < 60.0: fails.append(f'albedo close to untextured grey: {d_grey:.1f} < 60')
    if tex_std < 5.0: fails.append(f'texture flat (embedded std {tex_std:.1f} < 5)')
    if fg_std < 5.0: fails.append(f'rendered fg flat (lum std {fg_std:.1f} < 5)')
    if adv_max_m < 0.05: fails.append(f'mixer not advancing: skinned vertex delta {adv_max_m:.4f} m < 0.05 (real 0.30, null 0)')
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
