#!/usr/bin/env python3
"""S39 T1: verify the LIVE v21 pages (public URLs, no local copies) quantitatively.

Loads https://nawaf-al-hussain.github.io/TDKR-Game/playable/{index,pipeline}.html
in headless Chromium and reports:
  - silhouette IoU vs numpy-skinned idle truth @0.5 s through the PAGE camera
    (nulls: lying/unrotated, wrong pose, shifted)
  - aspect ratio, feet contact, mean albedo vs the LIVE GLB texture (+ texture
    presence = the embedded PNG must be non-flat)
  - UV seam continuity vs shuffled-UV null (from the LIVE GLB bytes)
  - idle AND run skinned output sampled at two times each vs numpy FK
    (mismatched-time null; advancing = the two times differ)
  - console errors and EVERY network response status on both pages
"""
import json, os, struct, sys, urllib.request
import numpy as np
from PIL import Image, ImageDraw

BASE = 'https://nawaf-al-hussain.github.io/TDKR-Game/playable/'
TRUTH = '/home/z/my-project/scripts/jsverify/s38_truth'
OUTDIR = '/tmp/my-project/work/TDKR-Game/extraction/re/session39'
OUT = OUTDIR + '/s39_t1_live.json'
W, H = 1280, 720
GREY = np.array([0.75 * 255] * 3)
os.makedirs(OUTDIR, exist_ok=True)


def fetch(url):
    req = urllib.request.Request(url, headers={'Cache-Control': 'no-cache'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read(), r.status


print('fetching LIVE assets...')
html_i, st_i = fetch(BASE + 'index.html')
patch_bytes, st_p = fetch(BASE + 'patch.json')
glb, st_g = fetch(BASE + 'batman.glb')
html_pl, st_pl = fetch(BASE + 'pipeline.html')
patch = json.loads(patch_bytes)
print(f'index {st_i} ({len(html_i)}B)  patch {st_p}  glb {st_g} ({len(glb)}B)  pipeline {st_pl}')

# ---- GLB parse (LIVE bytes)
jl = struct.unpack('<I', glb[12:16])[0]
gj = json.loads(glb[20:20 + jl]); bin_off = 20 + jl + 8
prim = gj['meshes'][0]['primitives'][0]


def acc(ai):
    a = gj['accessors'][ai]; bv = gj['bufferViews'][a['bufferView']]
    off = bin_off + bv.get('byteOffset', 0) + a.get('byteOffset', 0)
    n, t = a['count'], a['type']
    if t == 'VEC3': return np.frombuffer(glb, np.float32, n * 3, off).reshape(n, 3)
    if t == 'VEC2': return np.frombuffer(glb, np.float32, n * 2, off).reshape(n, 2)
    return np.frombuffer(glb, np.uint16, n, off)


V = acc(prim['attributes']['POSITION']).astype(np.float64)
UV = acc(prim['attributes']['TEXCOORD_0']).astype(np.float64)
idx_g = acc(prim['indices']).astype(int).reshape(-1, 3)
img = gj['images'][0]; bv = gj['bufferViews'][img['bufferView']]
png = glb[bin_off + bv.get('byteOffset', 0): bin_off + bv.get('byteOffset', 0) + bv['byteLength']]
import io
tex = np.array(Image.open(io.BytesIO(png)).convert('RGB'))
TEX_MEAN = tex.reshape(-1, 3).mean(0)
TEX_STD = tex.reshape(-1, 3).std(0)
print(f'texture {tex.shape[1]}x{tex.shape[0]} mean {TEX_MEAN.round(1)} std {TEX_STD.round(1)}')

# ---- numpy references + camera (identical to playable_screenshot_gate.py)
spawn = patch['spawns'][0]['pos']
P = np.array([spawn[0], spawn[1], spawn[2] + 0.9])
R = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]], float)
OFF = np.array([P[0], P[2] - 0.9, -P[1]])


def world(Vf):
    return Vf @ R.T + OFF


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


CAM_POS = np.array([P[0], P[2] + 0.2, -P[1] + 4.2])
CAM_TGT = np.array([P[0], P[2] + 0.1, -P[1]])
VIEW = look_at(CAM_POS, CAM_TGT)
PROJ = perspective(np.radians(60), W / H, 0.1, 800)


def project(Vv):
    Vh = np.hstack([Vv, np.ones((len(Vv), 1))])
    clip = Vh @ (PROJ @ VIEW).T
    ndc = clip[:, :3] / clip[:, 3:4]
    return ((ndc[:, 0] * .5 + .5) * W, (1 - (ndc[:, 1] * .5 + .5)) * H)


def silhouette(Vv):
    px, py = project(Vv)
    im = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(im)
    for tri in idx_g:
        d.polygon([(px[i], py[i]) for i in tri], fill=255)
    return np.array(im) > 127


def iou(a, b):
    u = (a | b).sum()
    return float((a & b).sum() / u) if u else 0.0


zi = np.load(f'{TRUTH}/_001_idle_stand.npz')
zr = np.load(f'{TRUTH}/_008_run.npz')
ref = world(zi['t500'].astype(np.float64))
ref_lying = zi['t500'].astype(np.float64) + OFF          # unrotated = the v20 regression
ref_wrong = world(zi['t3450'].astype(np.float64))
ref_shift = world(zi['t500'].astype(np.float64)) + np.array([1.2, 0, 0])
sil_ref, sil_lying = silhouette(ref), silhouette(ref_lying)
sil_wrong, sil_shift = silhouette(ref_wrong), silhouette(ref_shift)

# ---- browser over PUBLIC urls
from playwright.sync_api import sync_playwright

console_msgs, responses = [], []


def wire(pg, tag):
    pg.on('console', lambda m: console_msgs.append([tag, m.type, m.text[:300]]))
    pg.on('pageerror', lambda e: console_msgs.append([tag, 'pageerror', str(e)[:300]]))
    pg.on('response', lambda r: responses.append([tag, r.status, r.url[:160]]))


SAMPLE_JS = """([clip, t]) => {
  const f = window.__frozen; if (!f) return null;
  const mixer = f.mixer, A = f.actions, root = f.batman;
  for (const k of Object.keys(A)) { A[k].play(); A[k].setEffectiveWeight(k === clip ? 1 : 0); }
  mixer.setTime(t);
  root.updateMatrixWorld(true);
  let sm = null; root.traverse(o => { if (o.isSkinnedMesh) sm = o; });
  if (!sm) return null;
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
      const M = new Array(16);
      for (let c = 0; c < 4; c++) for (let r = 0; r < 4; r++) {
        let s = 0; for (let q = 0; q < 4; q++) s += m[q*4+r] * b[c*4+q];
        M[c*4+r] = s;
      }
      x += w * (M[0]*px + M[4]*py + M[8]*pz + M[12]);
      y += w * (M[1]*px + M[5]*py + M[9]*pz + M[13]);
      z += w * (M[2]*px + M[6]*py + M[10]*pz + M[14]);
    }
    out[3*i] = x; out[3*i+1] = y; out[3*i+2] = z;
  }
  return Array.from(out);
}"""

res = {'live_url': BASE, 'http_asset_status': {'index.html': st_i, 'patch.json': st_p,
       'batman.glb': st_g, 'pipeline.html': st_pl}}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': W, 'height': H})
    wire(pg, 'index')
    pg.goto(BASE + 'index.html#freeze0.5&gate', wait_until='domcontentloaded', timeout=60000)
    pg.wait_for_function('window.__frozen !== undefined', timeout=45000)
    pg.wait_for_timeout(800)
    pg.screenshot(path='/tmp/s39_live_gate.png')

    # advancing-under-its-own-mixer check (frozen page: drive mixer manually)
    adv = pg.evaluate("""() => {
      const f = window.__frozen, mixer = f.mixer, root = f.batman;
      mixer.setTime(0);
      let sm = null; root.traverse(o => { if (o.isSkinnedMesh) sm = o; });
      const b0 = sm.skeleton.bones[0].position.clone();
      mixer.update(0.25); mixer.update(0.25);
      const b1 = sm.skeleton.bones[0].position.clone();
      return {t_after: mixer.time, moved: b0.distanceTo(b1)};
    }""")
    res['mixer_advancing'] = adv

    samples = {}
    for clip, npz, times in [('_001_idle_stand', zi, [0.5, 2.0]),
                             ('_008_run', zr, [0.1, 0.5])]:
        for t in times:
            arr = pg.evaluate(SAMPLE_JS, [clip, t])
            samples[f'{clip}@{t}'] = np.array(arr, float).reshape(-1, 3)
    b.close()

# ---- FK comparison vs numpy truth (world space)
def cmp_err(Vb, Vt):
    d = np.linalg.norm(Vb - world(Vt.astype(np.float64)), axis=1) * 100.0
    return round(float(d.max()), 3), round(float(d.mean()), 4)


fk = {}
for clip, npz, times in [('_001_idle_stand', zi, [0.5, 2.0]),
                         ('_008_run', zr, [0.1, 0.5])]:
    for t in times:
        key = f'{clip}@{t}'
        k = f't{int(round(t * 1000))}'
        mx, mn = cmp_err(samples[key], npz[k])
        fk[key] = {'max_cm': mx, 'mean_cm': mn}
mx, mn = cmp_err(samples['_001_idle_stand@0.5'], zi['t2000'])
fk['null_idle@0.5_vs_truth@2.0'] = {'max_cm': mx, 'mean_cm': mn}
mx, mn = cmp_err(samples['_008_run@0.1'], zr['t500'])
fk['null_run@0.1_vs_truth@0.5'] = {'max_cm': mx, 'mean_cm': mn}
adv_d = float(np.linalg.norm(samples['_001_idle_stand@0.5'] - samples['_001_idle_stand@2.0'], axis=1).max() * 100)
fk['advancing_idle_0.5_vs_2.0_max_cm'] = round(adv_d, 3)
adv_d2 = float(np.linalg.norm(samples['_008_run@0.1'] - samples['_008_run@0.5'], axis=1).max() * 100)
fk['advancing_run_0.1_vs_0.5_max_cm'] = round(adv_d2, 3)
res['fk_samples_vs_numpy'] = fk

# ---- screenshot metrics
shot = np.array(Image.open('/tmp/s39_live_gate.png').convert('RGB'))
fg = ~(shot > 240).all(2)
res['fg_fraction'] = round(float(fg.mean()), 4)
m_iou = iou(fg, sil_ref)
res['iou'] = round(m_iou, 4)
res['iou_null_lying'] = round(iou(fg, sil_lying), 4)
res['iou_null_wrong_pose'] = round(iou(fg, sil_wrong), 4)
res['iou_null_shifted'] = round(iou(fg, sil_shift), 4)


def bbox(m):
    rows = np.where(m.any(1))[0]; cols = np.where(m.any(0))[0]
    return rows[0], rows[-1], cols[0], cols[-1]


rb, fb = bbox(sil_ref), bbox(fg)
res['aspect_reference'] = round(float(rb[1] - rb[0]) / max(1, rb[3] - rb[2]), 3)
res['aspect_browser'] = round(float(fb[1] - fb[0]) / max(1, fb[3] - fb[2]), 3)
res['feet_min_world_y_m'] = round(float(ref[:, 1].min()), 4)
mean_rgb = shot[fg].mean(0)
res['albedo_mean_rgb'] = [round(float(x), 1) for x in mean_rgb]
res['texture_mean_rgb'] = [round(float(x), 1) for x in TEX_MEAN]
res['texture_std_rgb'] = [round(float(x), 1) for x in TEX_STD]
res['albedo_dist_to_texture'] = round(float(np.abs(mean_rgb - TEX_MEAN).mean()), 1)
res['albedo_dist_to_grey'] = round(float(np.abs(mean_rgb - GREY).mean()), 1)
res['texture_presence_std_min'] = round(float(TEX_STD.min()), 1)

# ---- UV seam check on LIVE GLB (s38 method)
from collections import defaultdict
q = np.round(V / 1e-4).astype(np.int64)
key = q[:, 0] * 2**40 + q[:, 1] * 2**20 + q[:, 2]
groups = defaultdict(list)
for i, k in enumerate(key): groups[int(k)].append(i)
multi = [g for g in groups.values() if len(g) > 1]
pairs = []
for g in multi:
    for i in range(len(g)):
        for j in range(i + 1, len(g)):
            pairs.append((g[i], g[j]))


def sample_t(uv):
    tu = np.mod(uv, 1.0)
    x = np.clip((tu[:, 0] * 1024).astype(int), 0, 1023)
    y = np.clip((tu[:, 1] * 1024).astype(int), 0, 1023)
    return tex[y, x].astype(int)


def match_rate(pa, pb):
    d = np.abs(sample_t(UV[pa]) - sample_t(UV[pb])).max(1)
    return float((d <= 8).mean())


pa = np.array([p[0] for p in pairs]); pb = np.array([p[1] for p in pairs])
duv = np.abs(UV[pa] - UV[pb])
frac_int = (np.abs(duv - np.round(duv)) < 1e-3).all(1)
sel = frac_int if frac_int.any() else np.ones(len(pairs), bool)
res['uv'] = {
    'shared_position_groups': len(multi), 'pairs': len(pairs),
    'integer_offset_pair_pct': round(float(frac_int.mean()), 4),
    'match_rate_integer_offset_pairs': round(match_rate(pa[sel], pb[sel]), 4),
    'match_rate_all_pairs': round(match_rate(pa, pb), 4),
}
rng = np.random.default_rng(39)
uv_sh = UV[rng.permutation(len(UV))]
d = np.abs(sample_t(UV[pa]) - sample_t(uv_sh[pb])).max(1)
res['uv']['null_shuffled_uv_match_rate'] = round(float((d <= 8).mean()), 4)

# ---- console + network
res['console_errors'] = [m for m in console_msgs if m[1] in ('error', 'pageerror')]
res['console_warnings'] = [m for m in console_msgs if m[1] == 'warning'][:20]
bad = [r for r in responses if r[1] >= 400]
res['network_total'] = len(responses)
res['network_non_2xx'] = bad
res['network_all'] = responses

fails = []
if not (0.005 < res['fg_fraction'] < 0.9): fails.append('fg fraction odd')
if m_iou < 0.80: fails.append(f'IoU {m_iou:.3f} < 0.80')
if m_iou - res['iou_null_lying'] < 0.25: fails.append('lying-null margin < 0.25')
if abs(res['aspect_browser'] / res['aspect_reference'] - 1) > 0.15: fails.append('aspect >15% off')
if not (0.0 <= res['feet_min_world_y_m'] <= 0.35): fails.append('feet off ground')
if res['albedo_dist_to_texture'] > 40: fails.append('albedo far from texture')
if res['texture_presence_std_min'] < 5: fails.append('texture flat (std<5)')
for k, v in fk.items():
    if not isinstance(v, dict): continue
    if k.startswith('null'):
        if v['mean_cm'] < 2.0: fails.append(f'{k} too small (insensitive)')
    elif 'max_cm' in v and v['max_cm'] > 2.0:
        fails.append(f'{k} max {v["max_cm"]} cm > 2')
if adv_d < 0.05: fails.append('idle samples identical — not advancing?')
if adv_d2 < 1.0: fails.append('run samples identical — not advancing?')
if res['network_non_2xx']: fails.append(f'{len(res["network_non_2xx"])} non-2xx responses')
if res['console_errors']: fails.append(f'{len(res["console_errors"])} console errors')
res['fail'] = fails
json.dump(res, open(OUT, 'w'), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != 'network_all'}, indent=1)[:4000])
print('NETWORK:', len(responses), 'requests,', len(bad), 'non-2xx')
print('S39 T1 LIVE CHECK:', 'FAIL — ' + '; '.join(fails) if fails else 'PASS')
sys.exit(1 if fails else 0)
