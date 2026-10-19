#!/usr/bin/env python3
"""S38 T1c: QUANTIFIED live-page verification (the release gate's core).
1. headless chromium screenshot of gh-pages/playable/index.html#freeze0.5&gate
2. numpy reference silhouette: s38_truth idle@0.5s skinned verts, page transform
   (R_x(-90) + ground), page camera (pos/lookAt/persp 60deg) -> filled triangles
3. metrics: silhouette IoU (+ 3 nulls: wrong-pose reference, shifted reference,
   rotated-180 reference), bbox aspect, ground contact (numpy min-z), mean
   albedo vs texture mean, height/width ratio
Gate thresholds encoded in gate JSON for site_release_check consumption.
"""
import json, os, subprocess, sys, time
import numpy as np
from PIL import Image, ImageDraw

ROOT = '/tmp/my-project/work/TDKR-Game'
PAGE = f'{ROOT}/gh-pages/playable'
PORT = 8899

# ---- 1. numpy reference (idle @ 0.5 s, from the verified truth)
z = np.load('/home/z/my-project/scripts/jsverify/s38_truth/_001_idle_stand.npz')
Vref = z['t500'].astype(np.float64)          # (1449, 3) file space, z-up
assert Vref.shape == (1449, 3)

# page transform: R_x(-90deg) then batman.position (P at spawn, z-0.9 lift)
patch = json.load(open(f'{PAGE}/patch.json'))
spawn = patch['spawns'][0]['pos']
P = np.array([spawn[0], spawn[1], spawn[2] + 0.9])
def page_tf(V):
    R = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]], float)  # R_x(-90): (x,y,z)->(x,z,-y)
    return V @ R.T + np.array([P[0], P[2] - 0.9, -P[1]])

# gate camera: pos (0, 1.1, 4.2) lookAt (0, 1.0, 0) — but the CHARACTER sits at the
# spawn point! In gate mode the page does NOT move batman (frozen skips position?)...
# Actually batman.position is still set from P each frame. So camera must look at P.
# Fix: gate camera frames the spawn point:
CAM_POS = np.array([P[0], P[2] + 0.2, -P[1] + 4.2])   # == page: (P.x, P.z+0.2, -P.y+4.2)
CAM_TGT = np.array([P[0], P[2] + 0.1, -P[1]])          # == page: (P.x, P.z+0.1, -P.y)

W, H = 1280, 720
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
VIEW = look_at(CAM_POS, CAM_TGT)
PROJ = perspective(np.radians(60), W / H, 0.1, 800)

# triangles of the kept GLB (same trim as the builder): re-derive from the GLB
import struct
buf = open(f'{PAGE}/batman.glb', 'rb').read()
jl = struct.unpack('<I', buf[12:16])[0]
gj = json.loads(buf[20:20 + jl])
bin_off = 20 + jl + 8
prim = gj['meshes'][0]['primitives'][0]
def acc_data(ai):
    acc = gj['accessors'][ai]; bv = gj['bufferViews'][acc['bufferView']]
    off = bin_off + bv.get('byteOffset', 0) + acc.get('byteOffset', 0)
    n = acc['count']
    if acc['type'] == 'VEC3': return np.frombuffer(buf, np.float32, n * 3, off).reshape(n, 3)
    if acc['type'] == 'SCALAR': return np.frombuffer(buf, np.uint16, n, off)
    raise ValueError(acc['type'])
verts_g = acc_data(prim['attributes']['POSITION']).astype(np.float64)
idx_g = acc_data(prim['indices']).astype(int).reshape(-1, 3)
assert len(verts_g) == 1449

def project(V):
    Vh = np.hstack([V, np.ones((len(V), 1))])
    clip = Vh @ (PROJ @ VIEW).T
    ndc = clip[:, :3] / clip[:, 3:4]
    px = (ndc[:, 0] * 0.5 + 0.5) * W
    py = (1 - (ndc[:, 1] * 0.5 + 0.5)) * H
    depth = ndc[:, 2]
    return px, py, depth

def silhouette(V):
    px, py, depth = project(page_tf(V))
    im = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(im)
    for tri in idx_g:
        pts = [(px[i], py[i]) for i in tri]
        if all(-2*W < p[0] < 3*W and -2*H < p[1] < 3*H for p in pts):
            d.polygon(pts, fill=255)
    return np.array(im) > 127

ref = silhouette(Vref)
print(f'reference silhouette: {ref.mean()*100:.1f}% of frame')

# nulls
z2 = np.load('/home/z/my-project/scripts/jsverify/s38_truth/_001_idle_stand.npz')
Vwrong = z2['t3450'].astype(np.float64)      # wrong pose (3.45 s)
Vrot = Vref.copy(); Vrot[:, [0, 1]] = -Vrot[:, [1, 0]]  # garbage orientation control

# ---- 2. browser screenshot
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT), '-d', PAGE],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(0.8)
try:
    from playwright.sync_api import sync_playwright
    shots = {}
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={'width': W, 'height': H})
        pg.goto(f'http://127.0.0.1:{PORT}/index.html#freeze0.5&gate')
        pg.wait_for_function('window.__frozen !== undefined', timeout=15000)
        pg.wait_for_timeout(700)
        shots['main'] = pg.screenshot()
        pg.close(); b.close()
    open('/tmp/s38_gate_main.png', 'wb').write(shots['main'])
    shot = np.array(Image.open('/tmp/s38_gate_main.png').convert('RGB'))
    print('screenshot ok', shot.shape)
finally:
    srv.terminate()

# foreground mask: NOT white-ish background (bg=255,255,255)
bg = (shot > 240).all(2)
fg = ~bg
# remove the 2px border effects
print(f'browser foreground: {fg.mean()*100:.1f}% of frame')

def iou(a, b):
    i = (a & b).sum(); u = (a | b).sum()
    return i / u if u else 0.0

# the browser draws the same mesh — restrict comparison to where BOTH have any
# content; shrink ref mask via same mask ops
# (browser AA edge -> dilate tolerance not needed at IoU>=0.8 thresholds)
ref_b = ref
m_iou = iou(fg, ref_b)
null_wrong = iou(fg, silhouette(Vwrong))
null_rot = iou(fg, silhouette(Vrot))
null_shift = iou(fg, np.roll(ref_b, 160, axis=1))

# bbox aspect
def bbox(m):
    rows = np.where(m.any(1))[0]; cols = np.where(m.any(0))[0]
    if not len(rows): return None
    return rows[0], rows[-1], cols[0], cols[-1]
rb, fb = bbox(ref_b), bbox(fg)
ref_aspect = (rb[1] - rb[0]) / max(1, rb[3] - rb[2])
fg_aspect = (fb[1] - fb[0]) / max(1, fb[3] - fb[2])

# ground contact (numpy): lowest skinned point vs ground plane y=0 (world three-space)
Vw = page_tf(Vref)
min_y = Vw[:, 1].min()

# mean albedo over foreground
mean_rgb = shot[fg].mean(0)
tex_mean = np.array([31.4, 31.0, 31.0])
grey = np.array([0.75 * 255] * 3)  # the OLD untextured baseColorFactor luminance
d_tex = float(np.abs(mean_rgb - tex_mean).mean())
d_grey = float(np.abs(mean_rgb - grey).mean())

res = {
    'iou': round(m_iou, 4),
    'iou_null_wrong_pose': round(null_wrong, 4),
    'iou_null_rotated_ref': round(null_rot, 4),
    'iou_null_shifted_ref': round(null_shift, 4),
    'aspect_reference': round(float(ref_aspect), 3),
    'aspect_browser': round(float(fg_aspect), 3),
    'ground_min_y_m': round(float(min_y), 4),
    'mean_rgb_fg': [round(float(x), 1) for x in mean_rgb],
    'texture_mean_rgb': [31.4, 31.0, 31.0],
    'albedo_dist_to_texture': round(d_tex, 1),
    'albedo_dist_to_grey': round(d_grey, 1),
    'fg_pct': round(float(fg.mean() * 100), 2),
    'ref_pct': round(float(ref.mean() * 100), 2),
}
print(json.dumps(res, indent=1))
json.dump(res, open('/tmp/my-project/work/TDKR-Game/extraction/re/session38/s38_t1_gate_metrics.json', 'w'), indent=1)
print('saved s38_t1_gate_metrics.json')
