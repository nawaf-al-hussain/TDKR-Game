#!/usr/bin/env python3
"""S41 T1: verify the LIVE public pages (no local copies) with the new gate
criteria, incl. quantified street-patch colour statistics vs the Python
reference decode (null: a different reference texture).

Pages (https://nawaf-al-hussain.github.io/TDKR-Game/):
  playable/index.html   full s39 battery: IoU(+3 nulls), aspect, feet, albedo,
                        UV seams, FK samples vs numpy truth, console, network
  playable/pipeline.html  real zip -> READY, street SHA, preview-canvas colour
                        stats vs reference decode (null = BakeGroup_Island1_A0)
  index.html            street viewer: window.__v scene state, network, screenshot
"""
import io, json, struct, urllib.request, zipfile
import numpy as np
from PIL import Image
import sys
sys.path.insert(0, '/home/z/my-project/scripts')
from s41_refdec_lib import decode_blocks, read_archive  # extracted s40 reference decoder

BASE = 'https://nawaf-al-hussain.github.io/TDKR-Game/'
ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
TRUTH = '/home/z/my-project/scripts/jsverify/s38_truth'
OUT = '/home/z/my-project/scripts/s41_t1_live.json'
STREET_SHA_REF = '52fcbf324bdd24146b6261da45fc74f4dc9a1dd3715a9c1f71c83bc615331736'
W, H = 1280, 720
res = {}


def fetch(url):
    req = urllib.request.Request(url, headers={'Cache-Control': 'no-cache'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read(), r.status


# ---- Python reference decodes (street patch + null texture) ----
z = zipfile.ZipFile(ZIP)
d, ents = read_archive(z, 'l_gothamcity_tex.gla')
stats = {}
for want in ('BakeGroup_Island1_Roads0.tga', 'BakeGroup_Island1_A0.tga'):
    for (name, off, size) in ents:
        if name != want: continue
        hdr = d[off:off + 52]
        hs, hgt, wid, mips, flags, dsz, bpp = struct.unpack_from('<7I', hdr, 0)
        base = ((wid + 3) // 4) * ((hgt + 3) // 4) * 8
        img = decode_blocks(d[off + 52: off + 52 + base], wid, hgt)
        # the page preview draws the TOP-LEFT 512x512 CROP of the texture
        # (pipeline.html: drawImage(full, 0,0,512,512, 0,0,256,256))
        small = Image.fromarray(img[:, :, :3]).crop((0, 0, 512, 512)).resize((256, 256), Image.BOX)
        a = np.asarray(small, float).reshape(-1, 3)
        stats[want] = {'mean': a.mean(0).round(2).tolist(), 'std': a.std(0).round(2).tolist(),
                       'w': wid, 'h': hgt}
res['reference_stats'] = stats
REF, NULLT = stats['BakeGroup_Island1_Roads0.tga'], stats['BakeGroup_Island1_A0.tga']

# ---- batman references (LIVE glb) ----
glb, st_g = fetch(BASE + 'playable/batman.glb')
patch_bytes, st_p = fetch(BASE + 'playable/patch.json')
html_i, st_i = fetch(BASE + 'index.html')
html_pl, st_pl = fetch(BASE + 'playable/pipeline.html')
res['http_asset_status'] = {'index.html': st_i, 'patch.json': st_p,
                            'batman.glb': st_g, 'pipeline.html': st_pl}
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
tex = np.array(Image.open(io.BytesIO(png)).convert('RGB'))
TEX_MEAN = tex.reshape(-1, 3).mean(0); TEX_STD = tex.reshape(-1, 3).std(0)

patch = json.loads(patch_bytes)
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

PV = persp(np.radians(60), W / H, 0.1, 800) @ look_at(
    np.array([P[0], P[2] + 0.2, -P[1] + 4.2]), np.array([P[0], P[2] + 0.1, -P[1]]))

def silhouette(Vv):
    Vh = np.hstack([Vv, np.ones((len(Vv), 1))]); clip = Vh @ PV.T
    ndc = clip[:, :3] / clip[:, 3:4]
    px = (ndc[:, 0] * .5 + .5) * W; py = (1 - (ndc[:, 1] * .5 + .5)) * H
    from PIL import ImageDraw
    im = Image.new('L', (W, H), 0); dd = ImageDraw.Draw(im)
    for tri in idx_g: dd.polygon([(px[i], py[i]) for i in tri], fill=255)
    return np.array(im) > 127

def iou(a, b):
    u = (a | b).sum()
    return float((a & b).sum() / u) if u else 0.0

zi = np.load(f'{TRUTH}/_001_idle_stand.npz')
zr = np.load(f'{TRUTH}/_008_run.npz')
sil_ref = silhouette(world(zi['t500'].astype(np.float64)))
sil_lying = silhouette(zi['t500'].astype(np.float64) + OFF)
sil_wrong = silhouette(world(zi['t3450'].astype(np.float64)))
sil_shift = silhouette(world(zi['t500'].astype(np.float64)) + np.array([1.2, 0, 0]))

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

from playwright.sync_api import sync_playwright
console_msgs, responses = [], []

def wire(pg, tag):
    pg.on('console', lambda mm: console_msgs.append([tag, mm.type, mm.text[:300]]))
    pg.on('pageerror', lambda e: console_msgs.append([tag, 'pageerror', str(e)[:300]]))
    pg.on('response', lambda r: responses.append([tag, r.status, r.url[:160]]))
    pg.on('requestfailed', lambda r: responses.append([tag, 0, 'FAILED:' + r.url[:160]]))

with sync_playwright() as pw:
    b = pw.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader'])

    # ---- A. playable (live) ----
    pg = b.new_page(viewport={'width': W, 'height': H}); wire(pg, 'playable')
    pg.goto(BASE + 'playable/index.html#freeze0.5&gate', wait_until='domcontentloaded', timeout=60000)
    pg.wait_for_function('window.__frozen !== undefined', timeout=45000)
    pg.wait_for_timeout(800)
    pg.screenshot(path='/home/z/my-project/scripts/s41_live_batman.png')
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
    for clip, npz, times in [('_001_idle_stand', zi, [0.5, 2.0]), ('_008_run', zr, [0.1, 0.5])]:
        for t in times:
            arr = pg.evaluate(SAMPLE_JS, [clip, t])
            samples[f'{clip}@{t}'] = np.array(arr, float).reshape(-1, 3)
    pg.close()

    def cmp_err(Vb, Vt):
        dd = np.linalg.norm(Vb - world(Vt.astype(np.float64)), axis=1) * 100.0
        return round(float(dd.max()), 3), round(float(dd.mean()), 4)

    fk = {}
    for clip, npz, times in [('_001_idle_stand', zi, [0.5, 2.0]), ('_008_run', zr, [0.1, 0.5])]:
        for t in times:
            key = f'{clip}@{t}'; k = f't{int(round(t * 1000))}'
            mx, mn = cmp_err(samples[key], npz[k]); fk[key] = {'max_cm': mx, 'mean_cm': mn}
    mx, mn = cmp_err(samples['_001_idle_stand@0.5'], zi['t2000'])
    fk['null_idle_wrongtime'] = {'max_cm': mx, 'mean_cm': mn}
    res['fk_samples_vs_numpy'] = fk

    shot = np.array(Image.open('/home/z/my-project/scripts/s41_live_batman.png').convert('RGB'))
    fg = ~(shot > 240).all(2)
    res['batman'] = {
        'fg_fraction': round(float(fg.mean()), 4),
        'iou': round(iou(fg, sil_ref), 4),
        'iou_null_lying': round(iou(fg, sil_lying), 4),
        'iou_null_wrong': round(iou(fg, sil_wrong), 4),
        'iou_null_shift': round(iou(fg, sil_shift), 4),
        'albedo_mean_rgb': [round(float(x), 1) for x in shot[fg].mean(0)],
        'texture_mean_rgb': [round(float(x), 1) for x in TEX_MEAN],
        'albedo_dist_to_texture': round(float(np.abs(shot[fg].mean(0) - TEX_MEAN).mean()), 1),
    }

    # ---- B. pipeline (live, real zip) ----
    pg = b.new_page(viewport={'width': 1100, 'height': 800}); wire(pg, 'pipe')
    pg.goto(BASE + 'playable/pipeline.html', wait_until='domcontentloaded', timeout=60000)
    pg.set_input_files('#f', ZIP)
    pg.wait_for_function("document.querySelector('#log').textContent.includes('READY')", timeout=240000)
    pg.wait_for_timeout(2000)
    res['pipe'] = {
        'street_sha': pg.evaluate("""async () => {
            if (!window.__streetRGBA) return null;
            const h = await crypto.subtle.digest('SHA-256', window.__streetRGBA);
            return [...new Uint8Array(h)].map(x => x.toString(16).padStart(2,'0')).join('');
        }"""),
        'err_box': pg.evaluate("document.querySelector('#err').textContent"),
        'log_tail': pg.evaluate("document.querySelector('#log').textContent").splitlines()[-6:],
        'canvas_stats': pg.evaluate("""() => {
            let cv = null;
            for (const c of document.querySelectorAll('canvas')) {
                if (c.width === 256 && c.height === 256) { cv = c; break; }
            }
            if (!cv) return null;
            const d = cv.getContext('2d').getImageData(0, 0, cv.width, cv.height).data;
            let n = d.length / 4, mean = [0,0,0], sq = [0,0,0];
            for (let i = 0; i < d.length; i += 4) {
              mean[0]+=d[i]; mean[1]+=d[i+1]; mean[2]+=d[i+2];
              sq[0]+=d[i]*d[i]; sq[1]+=d[i+1]*d[i+1]; sq[2]+=d[i+2]*d[i+2];
            }
            mean = mean.map(v => v/n);
            const std = sq.map((v,k) => Math.sqrt(Math.max(0, v/n - mean[k]*mean[k])));
            return {mean: mean.map(v=>Math.round(v*100)/100), std: std.map(v=>Math.round(v*100)/100),
                    w: cv.width, h: cv.height};
        }"""),
    }
    pg.screenshot(path='/home/z/my-project/scripts/s41_live_pipe.png')
    pg.close()

    # ---- C. street viewer (live) ----
    pg = b.new_page(viewport={'width': W, 'height': H}); wire(pg, 'street')
    pg.goto(BASE + 'index.html', wait_until='domcontentloaded', timeout=60000)
    try:
        pg.wait_for_function('window.__v && window.__v.scene && window.__v.scene.children.length > 0', timeout=300000)
        pg.wait_for_timeout(10000)
        res['street'] = {
            'scene_children': pg.evaluate('window.__v.scene.children.length'),
            'load_status': pg.evaluate("document.querySelector('#load-status') ? document.querySelector('#load-status').textContent : null"),
            'tris_text': pg.evaluate("document.querySelector('#st-tris') ? document.querySelector('#st-tris').textContent : null"),
        }
        pg.screenshot(path='/home/z/my-project/scripts/s41_live_street.png')
    except Exception as e:
        res['street'] = {'error': str(e)[:200]}
    pg.close()
    b.close()

# ---- comparisons + verdicts ----
c = res['pipe'].get('canvas_stats')
if c:
    m = np.array(c['mean']); sd = np.array(c['std'])
    dref = float(np.abs(m - np.array(REF['mean'])).mean())
    dnull = float(np.abs(m - np.array(NULLT['mean'])).mean())
    res['pipe']['canvas_vs_ref_meandist'] = round(dref, 2)
    res['pipe']['canvas_vs_null_meandist'] = round(dnull, 2)
    res['pipe']['canvas_std'] = c['std']; res['pipe']['ref_std'] = REF['std']
    res['pipe']['std_meandist_vs_ref'] = round(float(np.abs(sd - np.array(REF['std'])).mean()), 2)

res['console_errors'] = [mm for mm in console_msgs if mm[1] in ('error', 'pageerror')]
res['network_non2xx'] = [r for r in responses if r[1] >= 400 or r[1] == 0]
res['network_total'] = len(responses)

fails = []
if res['batman']['iou'] < 0.80: fails.append('iou<0.8')
if res['batman']['iou'] - res['batman']['iou_null_lying'] < 0.25: fails.append('lying margin')
if res['pipe']['street_sha'] != STREET_SHA_REF: fails.append('street sha')
if res['pipe']['err_box'].strip(): fails.append('err box')
if not res['pipe'].get('canvas_stats'): fails.append('no canvas')
else:
    if dref >= 2.0: fails.append(f'colour dist {dref}')
    if dnull - dref < 8.0: fails.append('null margin < 8')
if res['street'].get('error'): fails.append('street: ' + res['street']['error'][:80])
elif res['street']['scene_children'] < 1: fails.append('street empty scene')
if res['console_errors']: fails.append(f'{len(res["console_errors"])} console errors')
if res['network_non2xx']: fails.append(f'{len(res["network_non2xx"])} bad responses')
for k, v in fk.items():
    if 'null' in k:
        if v['mean_cm'] < 2.0: fails.append(f'{k} insensitive (mean {v["mean_cm"]})')
    elif v['max_cm'] > 2.0: fails.append(f'{k} {v["max_cm"]}cm')
res['fail'] = fails
json.dump(res, open(OUT, 'w'), indent=1, default=str)
print(json.dumps({k: v for k, v in res.items() if k not in ('network_non2xx',)}, indent=1, default=str)[:3200])
print('NETWORK:', res['network_total'], 'requests,', len(res['network_non2xx']), 'bad')
print('S41 T1 LIVE:', 'FAIL - ' + '; '.join(fails) if fails else 'PASS')
