#!/usr/bin/env python3
"""s49 T2: three falsifiable UV/binding checks, each calibrated.

(a) atlas-cell containment — segment UV footprints vs atlas cells computed from the
    page content; matched estimator on shuffled bindings (same statistic).
(b) road direction — structure-tensor dominant orientation of the textured render vs
    the mesh long axis; real vs shuffled textures.
(c) lightmap seam continuity — segments sharing vertices sample the LM at the shared
    verts; real vs permuted LM-page assignment.
"""
import struct, io, zipfile, json, collections
import numpy as np
from PIL import Image
import importlib.util

spec = importlib.util.spec_from_file_location(
    'cr', '/tmp/my-project/work/TDKR-Game/extraction/re/session42/s42_t2_cleanroom.py')
cr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cr)

GLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/l_gothamcity.gla'
TEXGLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/textures/l_gothamcity_tex.gla'
BDAE = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
OUT = '/tmp/my-project/work/TDKR-Game/extraction/re/session49/s49_t2_checks.json'

# ---------------- data ----------------
exec(open('/tmp/my-project/work/TDKR-Game/extraction/re/session49/s49_t1_render.py')
     .read().split('FOG_COLOR = ')[0].replace(
         "OUT_JSON = '/tmp/my-project/work/TDKR-Game/extraction/re/session49/s49_t1_render.json'", ''))

# bindings per material: authoring rows (name, diffuse, lm)
NS = {'c': 'http://www.collada.org/2005/11/COLLADASchema'}
import xml.etree.ElementTree as ET
z = zipfile.ZipFile(BDAE)
root = ET.fromstring(z.read('source.dae'))
imgs = {}
for im in root.find('c:library_images', NS).findall('c:image', NS):
    iid = im.get('id')
    init = im.find('c:init_from', NS)
    imgs[iid] = init.text.strip() if init is not None and init.text else ''
rows = []
for md in root.find('c:library_materials', NS).findall('c:material', NS):
    inst = md.find('c:instance_effect', NS)
    sam = {}
    if inst is not None:
        surf = {}
        for sp in inst.findall('c:setparam', NS):
            sf = sp.find('c:surface/c:init_from', NS)
            if sf is not None and sf.text:
                surf[sp.get('ref')] = imgs.get(sf.text.strip(), sf.text.strip())
        for sp in inst.findall('c:setparam', NS):
            s2 = sp.find('c:sampler2D/c:source', NS)
            if s2 is not None and s2.text and s2.text.strip() in surf:
                sam[sp.get('ref')] = surf[s2.text.strip()]
    rows.append((md.get('id'), sam.get('DiffuseMap') or '', sam.get('LightMap') or ''))

# segments: material + uv0 + positions
seg_mat = []
for k in range(len(pairs)):
    m, = struct.unpack_from('<I', ld, pairs[k][0] + 40)
    seg_mat.append(int(m))
segs_uv = {}
def seg_uv0(k, mid):
    if k in segs_uv:
        return segs_uv[k]
    off2 = pairs[k][0]
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2+68)
    ds = decl_of(mid)
    stride = ds[-1][2]
    nv = vb//stride
    raw = np.frombuffer(ld, np.uint8, vb, data_off+4)
    dmap = {d[0]: d for d in ds}
    d0 = dmap[1]
    uv = s16a(raw.reshape(nv, stride)[:, d0[1]:d0[1]+4].copy().view('<u2').reshape(nv, 2).astype(np.int32))
    segs_uv[k] = uv
    return uv

def seg_pos(k, mid):
    off2 = pairs[k][0]
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2+68)
    ds = decl_of(mid)
    stride = ds[-1][2]
    nv = vb//stride
    raw = np.frombuffer(ld, np.uint8, vb, data_off+4)
    return raw.reshape(nv, stride)[:, 0:12].copy().view('<f4').reshape(nv, 3).astype(np.float64)

def seg_uv1(k, mid):
    off2 = pairs[k][0]
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2+68)
    ds = decl_of(mid)
    stride = ds[-1][2]
    nv = vb//stride
    raw = np.frombuffer(ld, np.uint8, vb, data_off+4)
    dmap = {d[0]: d for d in ds}
    if 2 not in dmap:
        return None
    d1 = dmap[2]
    return s16a(raw.reshape(nv, stride)[:, d1[1]:d1[1]+4].copy().view('<u2').reshape(nv, 2).astype(np.int32))
out = {}

# ================= (a) atlas-cell containment =================
# atlas pages: pick billboard/props/rooftop diffuse pages with >=8 segments
page_segs = collections.defaultdict(list)
for k, m in enumerate(seg_mat):
    d = rows[m][1]
    if d:
        page_segs[d].append(k)
ATLAS_KEYS = ('billboard', 'props', 'rooftop', 'signs')
atlas_pages = [p for p in page_segs if len(page_segs[p]) >= 8 and
               any(key in p.lower() for key in ATLAS_KEYS)]
print('atlas pages:', atlas_pages)

def page_mask_nonempty(t):
    rgb = t['rgb'].astype(np.int32)
    near_black = rgb.mean(axis=2) < 16
    return ~near_black

def page_cells(t, grid=8):
    """coarse atlas cells: connected components on a downsampled non-empty mask."""
    from scipy import ndimage
    m = page_mask_nonempty(t)
    # downsample by 8 for speed
    h, w = m.shape
    m8 = m[:h//8*8, :w//8*8].reshape(h//8, 8, w//8, 8).mean(axis=(1, 3)) > 0.5
    lab, n = ndimage.label(m8)
    cells = []
    for i in range(1, n+1):
        ys, xs = np.nonzero(lab == i)
        if len(ys) < 4:
            continue
        cells.append((xs.min()/ (w//8), ys.min()/(h//8),
                      (xs.max()+1)/(w//8), (ys.max()+1)/(h//8)))
    return cells

def best_cell_containment(uv, cells):
    """uv footprint bbox vs best cell (matched estimator for real and null alike)."""
    u0, v0 = uv.min(axis=0)*0.5+0.5
    u1, v1 = uv.max(axis=0)*0.5+0.5
    best = 0.0
    fa = (u1-u0)*(v1-v0)
    if fa <= 0:
        return 0.0
    for (cu0, cv0, cu1, cv1) in cells:
        ix = max(0, min(u1, cu1)-max(u0, cu0))
        iy = max(0, min(v1, cv1)-max(v0, cv0))
        c = ix*iy/fa
        if c > best:
            best = c
    return best

try:
    import scipy
    HAVE_SCIPY = True
except ImportError:
    HAVE_SCIPY = False
print('scipy:', HAVE_SCIPY)

rng = np.random.default_rng(49)
res_a = {'pages': []}
if HAVE_SCIPY and atlas_pages:
    cell_cache = {}
    for page in atlas_pages[:6]:
        t = decode_tex(page)
        cells = page_cells(t)
        segs = page_segs[page][:60]
        real = []
        for k in segs:
            uv = seg_uv0(k, seg_mat[k])
            real.append(best_cell_containment(uv, cells))
        # shuffled null: same segments bound to OTHER atlas pages' cells (label-shuffle
        # of the segment->page assignment within this atlas set)
        others = [p for p in atlas_pages if p != page]
        nulls = []
        for _ in range(16):
            pp = others[rng.integers(len(others))]
            if pp not in cell_cache:
                cell_cache[pp] = page_cells(decode_tex(pp))
            for k in segs:
                uv = seg_uv0(k, seg_mat[k])
                nulls.append(best_cell_containment(uv, cell_cache[pp]))
        real_m = float(np.mean(real)); null_m = float(np.mean(nulls)); null_s = float(np.std(nulls))
        z = (real_m-null_m)/max(null_s, 1e-9)
        res_a['pages'].append({'page': page, 'segs': len(segs), 'cells': len(cells),
                               'real_mean': round(real_m, 4), 'null_mean': round(null_m, 4),
                               'null_std': round(null_s, 4), 'z': round(z, 2)})
        print('A', page[:40], 'real', round(real_m, 3), 'null', round(null_m, 3),
              '+/-', round(null_s, 3), 'z', round(z, 2))
out['a_atlas_containment'] = res_a

# ================= (b) road direction =================
def render_top(p, uv, tex, tris, size=192):
    mn, mx = p.min(0), p.max(0)
    span = max(mx[0]-mn[0], mx[1]-mn[1])*1.04
    cx, cy = (mn[0]+mx[0])/2, (mn[1]+mx[1])/2
    img = np.zeros((size, size, 3), np.float32)
    W, H = tex['w'], tex['h']
    trgb = tex['rgb']
    tuv = uv*0.5+0.5
    tuv = tuv.copy(); tuv[:, 1] = 1.0-tuv[:, 1]
    pxs = (p[:, 0]-cx)/span*size + size/2
    pys = (cy-p[:, 1])/span*size + size/2
    order = np.argsort(p[tris].mean(axis=1)[:, 2])
    for t in order:
        i0, i1, i2 = tris[t]
        if max(i0, i1, i2) >= len(p): continue
        x0, y0, x1, y1, x2, y2 = pxs[i0], pys[i0], pxs[i1], pys[i1], pxs[i2], pys[i2]
        xlo = max(int(min(x0, x1, x2)), 0); xhi = min(int(max(x0, x1, x2))+1, size-1)
        ylo = max(int(min(y0, y1, y2)), 0); yhi = min(int(max(y0, y1, y2))+1, size-1)
        if xlo > xhi or ylo > yhi: continue
        gx, gy = np.meshgrid(np.arange(xlo, xhi+1)+0.5, np.arange(ylo, yhi+1)+0.5)
        d = (y1-y2)*(x0-x2)+(x2-x1)*(y0-y2)
        if abs(d) < 1e-9: continue
        w0 = ((y1-y2)*(gx-x2)+(x2-x1)*(gy-y2))/d
        w1 = ((y2-y0)*(gx-x2)+(x0-x2)*(gy-y2))/d
        w2 = 1-w0-w1
        mask = (w0 >= -0.001) & (w1 >= -0.001) & (w2 >= -0.001)
        if not mask.any(): continue
        uu = w0*tuv[i0, 0]+w1*tuv[i1, 0]+w2*tuv[i2, 0]
        vv = w0*tuv[i0, 1]+w1*tuv[i1, 1]+w2*tuv[i2, 1]
        tx = np.clip((uu*W).astype(np.int64) % W, 0, W-1)
        ty = np.clip((vv*H).astype(np.int64) % H, 0, H-1)
        col = trgb[ty, tx].astype(np.float32)
        region = img[ylo:yhi+1, xlo:xhi+1]
        img[ylo:yhi+1, xlo:xhi+1] = np.where(mask[..., None], col, region)
    return img, span

def long_axis_deg(p):
    """dominant axis of the segment footprint (deg vs +x)."""
    q = p[:, :2] - p[:, :2].mean(axis=0)
    cov = q.T @ q / len(q)
    ev, evec = np.linalg.eigh(cov)
    v = evec[:, -1]
    return float(np.degrees(np.arctan2(v[1], v[0])) % 180.0)

def structure_tensor_ori(img):
    """dominant EDGE orientation via the structure tensor (deg vs +x, mod 180)."""
    g = img.mean(axis=2)
    gx = np.zeros_like(g); gy = np.zeros_like(g)
    gx[:, 1:-1] = g[:, 2:]-g[:, :-2]
    gy[1:-1, :] = g[2:, :]-g[1:-1, :] if gy.shape[0] > 2 else 0
    gy[1:-1, :] = g[2:, :]-g[:-2, :]
    # edge direction = gradient direction; dominant orientation = gradient angle /2 tensor
    Jxx = (gx*gx).sum(); Jyy = (gy*gy).sum(); Jxy = (gx*gy).sum()
    theta = 0.5*np.degrees(np.arctan2(2*Jxy, Jxx-Jyy))
    return float(theta % 180.0)

# calibration set: roads (known good, s46 GLB-proven) + a shuffled-texture null
ROAD_TEX = 'gothamcity_roads_details.tga'
road_segs = [k for k, m in enumerate(seg_mat) if rows[m][1] == ROAD_TEX][:14]
res_b = []
dtex = decode_tex(ROAD_TEX)
pool = [p for p in page_segs if 'road' in p.lower() or 'street' in p.lower()][:12]
for k in road_segs:
    m = seg_mat[k]
    p = seg_pos(k, m)
    uv = seg_uv0(k, m)
    tris = None
    off2 = pairs[k][0]
    data_off, four, vb, ib = struct.unpack_from('<4I', ld, off2+68)
    tris = np.frombuffer(ld, '<u2', ib//2, data_off+4+vb).astype(np.int64).reshape(-1, 3)
    img, span = render_top(p, uv, dtex, tris)
    la = long_axis_deg(p)
    ori = structure_tensor_ori(img)
    # edge orientation should be PARALLEL to the road axis (lane strokes) -> |ori - la| small
    dreal = min(abs(ori-la), 180-abs(ori-la))
    entry = {'k': int(k), 'axis': round(la, 1), 'ori': round(ori, 1), 'd_real': round(dreal, 1)}
    # shuffled-texture null: same geometry, random textures
    ds = []
    for _ in range(6):
        pt = pool[rng.integers(len(pool))]
        try:
            t2 = decode_tex(pt)
        except SystemExit:
            continue
        img2, _ = render_top(p, uv, t2, tris)
        ori2 = structure_tensor_ori(img2)
        d2 = min(abs(ori2-la), 180-abs(ori2-la))
        ds.append(d2)
    entry['d_null_mean'] = round(float(np.mean(ds)), 1) if ds else None
    res_b.append(entry)
d_real_all = [e['d_real'] for e in res_b]
d_null_all = [e['d_null_mean'] for e in res_b if e['d_null_mean'] is not None]
print('B real |ori-axis| mean %.1f vs shuffled-texture %.1f' %
      (np.mean(d_real_all), np.mean(d_null_all)))
out['b_road_direction'] = {'real_mean_deg': round(float(np.mean(d_real_all)), 2),
                           'null_mean_deg': round(float(np.mean(d_null_all)), 2),
                           'per_seg': res_b}

# ================= (c) lightmap seam continuity =================
# pairs of LightMapDC segments sharing >=3 vertex positions
from collections import defaultdict
vmap = defaultdict(list)
lm_segs = [k for k, m in enumerate(seg_mat) if rows[m][2]]
for k in lm_segs:
    m = seg_mat[k]
    p = seg_pos(k, m)
    key = lambda q: (round(q[0], 1), round(q[1], 1), round(q[2], 1))
    for vi in range(0, len(p), max(1, len(p)//24)):
        vmap[key(p[vi])].append(k)
pair_list = []
seen = set()
for v, ks in vmap.items():
    for i in range(len(ks)):
        for j in range(i+1, len(ks)):
            a, b = ks[i], ks[j]
            if a == b:
                continue
            if (a, b) in seen:
                continue
            seen.add((a, b))
            if rows[seg_mat[a]][2] == rows[seg_mat[b]][2]:
                pair_list.append((a, b))
rng.shuffle(pair_list)
pair_list = pair_list[:120]
print('LM seam pairs:', len(pair_list))

def lm_sample_diff(ka, kb, lm_assign):
    """mean |LM color difference| at shared vertices between two segments."""
    ma, mb = seg_mat[ka], seg_mat[kb]
    pa, la = lm_assign[ma], lm_assign[mb]
    if not pa or not la or pa != la:
        return None
    if tex_member(pa) is None:
        return None
    t = decode_tex(pa)
    uva = seg_uv1(ka, ma)
    uvb = seg_uv1(kb, mb)
    if uva is None or uvb is None:
        return None
    pa_pos = seg_pos(ka, ma)
    pb_pos = seg_pos(kb, mb)
    key = lambda q: (round(q[0], 1), round(q[1], 1), round(q[2], 1))
    bmap = {key(q): i for i, q in enumerate(pb_pos)}
    LW, LH = t['w'], t['h']
    lrgb = t['rgb'].astype(np.float32)
    diffs = []
    tuv = uva*0.5+0.5; tuv = tuv.copy(); tuv[:, 1] = 1.0-tuv[:, 1]
    tuvb = uvb*0.5+0.5; tuvb = tuvb.copy(); tuvb[:, 1] = 1.0-tuvb[:, 1]
    for i, q in enumerate(pa_pos):
        j = bmap.get(key(q))
        if j is None:
            continue
        ca = lrgb[int((tuv[i, 1])*LH) % LH, int((tuv[i, 0])*LW) % LW]
        cb = lrgb[int((tuvb[j, 1])*LH) % LH, int((tuvb[j, 0])*LW) % LW]
        diffs.append(np.abs(ca-cb).mean())
    return float(np.mean(diffs)) if diffs else None

real_diffs = []
for (ka, kb) in pair_list:
    d = lm_sample_diff(ka, kb, {m: rows[m][2] for m in range(307)})
    if d is not None:
        real_diffs.append(d)
# null: permute the LM page assignment across LightMapDC materials
lm_mats = [m for m in range(307) if rows[m][2]]
null_diffs = []
for it in range(8):
    perm = rng.permutation(len(lm_mats))
    assign = {m: rows[lm_mats[perm[i]]][2] for i, m in enumerate(lm_mats)}
    for (ka, kb) in pair_list[:40]:
        d = lm_sample_diff(ka, kb, assign)
        if d is not None:
            null_diffs.append(d)
print('C seam |dLM| real %.2f vs permuted-page %.2f (n=%d/%d)' %
      (np.mean(real_diffs), np.mean(null_diffs), len(real_diffs), len(null_diffs)))
out['c_lm_seam'] = {'real_mean': round(float(np.mean(real_diffs)), 3),
                    'null_mean': round(float(np.mean(null_diffs)), 3),
                    'n_real': len(real_diffs), 'n_null': len(null_diffs)}

json.dump(out, open(OUT, 'w'), indent=1)
print('saved', OUT)
