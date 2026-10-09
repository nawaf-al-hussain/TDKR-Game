#!/usr/bin/env python3
"""Zone-tier exporter: streamed street-level geometry from GothamCity*.zip
(lod_data/lod_table) -> street GLBs for the viewer.

v5 binding (session 10, structural — replaces the v4 edge-score heuristics
that produced rainbow smears):

The zone ground uses the LightMapDC technique: DiffuseMap = a horizontal BAND
ATLAS (road cross-sections stacked vertically); a road piece's v-range spans
sidewalk->asphalt->sidewalk = ONE cross-section GROUP of the atlas.  So the
page assignment is a STRUCTURAL test, not a score:

  1. detect each atlas's cross-section groups (dark separator rows)
  2. a flat wide-u segment binds the page whose ONE group contains its
     v-range (hard filter); among candidates the within-group edge score
     only disambiguates (v1 vs v2 vs crossings)
  3. small-UV-box flats tile albedo pages (grass/dirt/sand/asphalt)
  4. props < 15u with decisive score -> Z1 atlases
  5. everything else -> __dark (honest fallback, no more smears)

Geometry layout (proved): segment = [u32 hdr][vBytes verts (stride 20/24)]
[u16 strip indices with 0xffff cuts]; descriptor table in lod_table.bin
maps seg -> (dataOff, vBytes, iBytes) per LOD.
"""
import os, re, struct, sys, json
import numpy as np
from PIL import Image

ZONE = '/home/z/my-project/work/zone'
PNG = '/home/z/my-project/download/TDKR_assets/textures_png'
SITE = '/home/z/my-project/work/ghpages_site'
MODELS = os.path.join(SITE, 'models')
TEXD = os.path.join(MODELS, 'tex')

ISLANDS = {
    'GothamCity': dict(isl='1',
                       roads=['GothamCity_Road_v1_Island_1', 'GothamCity_Road_v2_Island_1'],
                       crossing='GothamCity_Road_Crossings_Island_1',
                       bakes=['BakeGroup_Island1_A0', 'BakeGroup_Island1_B0',
                              'BakeGroup_Island1_Roads0', 'GC_LongDist_Island1_Roads'],
                       props=['GC_Z1_Props_Street', 'GC_Z1_Props_Street_Alpha',
                              'GC_Z1_Props_Rooftop', 'GC_Z1_Props_Rooftop_Alpha']),
    'GothamCity_Island2': dict(isl='2',
                       roads=['GothamCity_Road_v1_Island_2', 'GothamCity_Road_v2_Island_2',
                              'GothamCity_Road_Island_2'],
                       crossing='GothamCity_Road_Crossings_Island_2',
                       bakes=['BakeGroup_Island2_A0', 'BakeGroup_Island2_B0',
                              'BakeGroup_Island2_Roads0', 'GC_LongDist_Island2_Roads'],
                       props=['GC_Z1_Props_Street', 'GC_Z1_Props_Street_Alpha',
                              'GC_Z1_Props_Rooftop', 'GC_Z1_Props_Rooftop_Alpha']),
}
FLAT_TEX = ['GC_Park_grass', 'GC_Park_dirt', 'GothamCity_sand_tile',
            'GothamCity_asphalt_tile']

# v5: band-atlas cross-section groups (computed once per page)
_band_cache = {}

def _gray_rows(name, h=1024):
    if name in _band_cache:
        return _band_cache[name]
    p = find_png(name)
    if p is None:
        _band_cache[name] = None
        return None
    im = Image.open(p).convert('L').resize((32, h), Image.BILINEAR)
    _band_cache[name] = np.asarray(im, np.float32)
    return _band_cache[name]

def cross_sections(name, h=1024):
    g = _gray_rows(name, h)
    if g is None:
        return []
    row = g.mean(1)
    dark = row < row.mean() * 0.62
    edges = [0]
    i = 0
    while i < h:
        if dark[i]:
            j = i
            while j < h and dark[j]:
                j += 1
            if j - i >= 2:
                edges += [i, j]
            i = j
        else:
            i += 1
    edges.append(h)
    edges = sorted(set(edges))
    return [(a / h, b / h) for a, b in zip(edges[:-1], edges[1:]) if b - a > 20]


def find_png(name):
    for a in ('l_gothamcity_tex', 'commons_tex'):
        p = os.path.join(PNG, a, name + '.png')
        if os.path.exists(p):
            return p
    return None


def parse_island(name):
    lod = open(f'{ZONE}/{name}/lod_data.bin', 'rb').read()
    lt = open(f'{ZONE}/{name}/lod_table.bin', 'rb').read()
    u = struct.unpack(f'<{len(lt)//4}I', lt)
    n = u[0]
    pairs = [(u[1+2*k], u[2+2*k]) for k in range(n)]
    out = []
    for off, sz in pairs:
        data_off, four, vb, ib = struct.unpack_from('<4I', lod, off + 68)
        if four != 4:
            continue
        vstart = data_off + 4
        istart = vstart + vb
        idx = np.frombuffer(lod[istart:istart+ib], '<u2').astype(np.int32)
        real = idx[idx != 0xffff]
        mx = int(real.max()) if len(real) else 0
        stride = None
        for s in (24, 20, 32):
            if vb % s == 0 and mx < vb // s:
                t = np.frombuffer(lod[vstart:vstart+vb], '<f4').reshape(-1, s//4)[:, :3]
                if np.isfinite(t).all() and np.abs(t).max() < 6000:
                    stride = s
                    break
        if stride is None:
            continue
        nv = vb // stride
        v = np.frombuffer(lod[vstart:vstart+vb], '<f4').reshape(nv, stride//4)
        words = np.frombuffer(lod[vstart:vstart+vb], '<u4').reshape(nv, stride//4)
        uvw = words[:, 4]
        out.append(dict(pos=v[:, :3].copy(), uvw=uvw, idx=real.astype(np.uint32),
                        vb=vb, ib=ib))
    return out


def strip_to_tris(idx):
    tris = []
    i, n = 0, len(idx)
    while i < n - 2:
        a, b, c = int(idx[i]), int(idx[i+1]), int(idx[i+2])
        if 0xffff in (a, b, c):
            i += 1
            continue
        if a != b and b != c and a != c:
            tris.append((a, b, c) if i % 2 == 0 else (a, c, b))
        i += 1
    return tris


_edge_cache = {}
def edges_of(name, size=512):
    if name in _edge_cache:
        return _edge_cache[name]
    p = find_png(name)
    if p is None:
        _edge_cache[name] = None
        return None
    im = Image.open(p).convert('L')
    im.thumbnail((size, size), Image.BILINEAR)
    a = np.asarray(im, np.float32) / 255.0
    gx = np.zeros_like(a); gy = np.zeros_like(a)
    gx[:, 1:-1] = a[:, 2:] - a[:, :-2]
    gy[1:-1, :] = a[2:, :] - a[:-2, :]
    _edge_cache[name] = np.hypot(gx, gy)
    return _edge_cache[name]


def uv_of(seg):
    w = seg['uvw']
    return ((w & 0xffff).astype(np.float32) / 65535.0,
            (w >> 16).astype(np.float32) / 65535.0)


def score_uv(name, u, v):
    e = edges_of(name)
    if e is None:
        return -1.0
    h, w = e.shape
    uu = np.clip(u * (w - 1), 0, w - 1).astype(np.int32)
    vv = (h - 1) - np.clip(v * (h - 1), 0, h - 1).astype(np.int32)
    return float(e[vv, uu].mean() / (e.mean() + 1e-9))


def band_fit(page, u, v):
    """road pages are horizontal band atlases; a road strip's v lives in one
    band while u spans widely. Returns (fit01, band_v_range)."""
    e = edges_of(page)
    if e is None:
        return 0.0, None
    h = e.shape[0]
    row = e.mean(1)
    # band separators = rows with low edge energy between marking rows
    thr = row.mean() * 0.5
    bands = []
    start = None
    for i in range(h):
        if row[i] > thr and start is None:
            start = i
        elif row[i] <= thr and start is not None:
            if i - start > 8:
                bands.append((start / h, i / h))
            start = None
    if start is not None:
        bands.append((start / h, 1.0))
    vmin, vmax = float(v.min()), float(v.max())
    best = 0.0
    for b0, b1 in bands:
        if vmin >= b0 - 0.02 and vmax <= b1 + 0.02:
            # inside a band: score within-band sampling
            vv = np.clip(v, b0, b1)
            best = max(best, score_uv(page, u, vv))
    return best, bands


def bind_segment(seg, isl, xsecs=None):
    """Returns (tex, mode) or (None, 'dark').

    v5 STRUCTURAL binding — see module docstring.  The band-atlas page for a
    road piece is the one whose cross-section GROUP contains the piece's
    v-range; edge score only disambiguates among containing candidates.
    The v4 global edge-score heuristic bound cross-band pages (rainbow
    smears) — containment now gates everything."""
    if seg['uvw'] is None or np.all(seg['uvw'] == 0xffffffff):
        return None, 'dark'
    u, v = uv_of(seg)
    p = seg['pos']
    zr = float(np.ptp(p[:, 2]))
    flat = zr < max(2.0, 0.06 * float(np.ptp(p[:, :2])))
    uspan, vspan = float(u.max() - u.min()), float(v.max() - v.min())
    if flat:
        if uspan < 0.3 and vspan < 0.3:
            # tiled albedo (grass/dirt/sand/asphalt)
            cands = [(score_uv(t, u, v), t) for t in FLAT_TEX]
            cands.sort(reverse=True)
            top = cands[0]
            if top[0] >= 1.1:
                return top[1], 'd'
            return None, 'dark'
        if vspan > 0.985 and uspan > 0.985:
            return None, 'dark'   # full-page: bake/decals we cannot verify
        # v5: cross-section containment over this island's band atlases
        vmin, vmax = float(v.min()), float(v.max())
        cands = []
        for page, groups in (xsecs or {}).items():
            for a, b in groups:
                if vmin >= a - 0.008 and vmax <= b + 0.008:
                    cands.append(page)
                    break
        if cands:
            scored = sorted(((score_uv(t, u, v), t) for t in cands), reverse=True)
            top = scored[0]
            if top[0] >= 0.9:
                return top[1], 'd'
        return None, 'dark'
    else:
        # vertical pieces: walls belong to the fp tier's complete-map bakes in
        # the viewer; binding them to atlases produces stretched garbage.
        # Only SMALL props (street furniture scale) may take a props atlas,
        # and only on a decisive score; everything else stays dark.
        dim = float(np.ptp(p[:, :2]).max())
        if dim < 15.0:
            cands = [(score_uv(t, u, v), t) for t in isl['props']]
            cands.sort(reverse=True)
            top = cands[0]
            second = cands[1] if len(cands) > 1 else (0, '')
            if top[0] >= 1.2 and top[0] - second[0] > 0.12:
                return top[1], 'd'
        return None, 'dark'


def jpg_from_png(png_path, out_path, max_dim, quality):
    im = Image.open(png_path).convert('RGB')
    if max(im.size) > max_dim:
        im.thumbnail((max_dim, max_dim), Image.LANCZOS)
    im.save(out_path, 'JPEG', quality=quality, optimize=True)
    return os.path.getsize(out_path)


class GlbBuilder:
    def __init__(self):
        self.buf = bytearray()
        self.offset = 0
        self.views, self.accessors, self.meshes, self.nodes, self.materials = [], [], [], [], []
        self._mat_by = {}

    def _add(self, data, align=4):
        pad = (-len(self.buf)) % align
        self.buf.extend(b'\0' * pad)
        self.offset += pad
        start = self.offset
        self.buf.extend(data)
        self.offset += len(data)
        return start, len(data)

    def material_for(self, tex, mode):
        key = (tex, mode)
        if key in self._mat_by:
            return self._mat_by[key]
        if tex is None:
            mat = dict(name='__dark', doubleSided=True,
                       pbrMetallicRoughness=dict(baseColorFactor=[0.055, 0.07, 0.10, 1.0],
                                                 metallicFactor=0.0, roughnessFactor=1.0))
        else:
            mat = dict(name=f'{tex}|{mode}', doubleSided=True,
                       pbrMetallicRoughness=dict(baseColorFactor=[1.0, 1.0, 1.0, 1.0],
                                                 metallicFactor=0.0, roughnessFactor=1.0))
        self.materials.append(mat)
        mid = len(self.materials) - 1
        self._mat_by[key] = mid
        return mid

    def add_segment_mesh(self, name, segs_binds):
        """segs_binds: list of (seg, tex, mode). Segments sharing the same
        (tex, mode) are MERGED into one primitive (draw-call reduction:
        2600 segments -> ~20 primitives per GLB)."""
        by_mat = {}
        order = []
        for seg, tex, mode in segs_binds:
            tris = strip_to_tris(seg['idx'])
            if not tris:
                continue
            key = (tex, mode)
            if key not in by_mat:
                by_mat[key] = dict(pos=[], uv=[], idx=[], base=0)
                order.append(key)
            b = by_mat[key]
            b['base'] = len(b['pos'])
            pos = seg['pos']
            xyz = np.column_stack([pos[:, 0], pos[:, 2], -pos[:, 1]]).astype(np.float32)
            u, v = uv_of(seg)
            uv = np.column_stack([u, 1.0 - v]).astype(np.float32)
            idx = np.asarray(tris, np.uint32).reshape(-1) + b['base']
            b['pos'].append(xyz)
            b['uv'].append(uv)
            b['idx'].append(idx)
        prims = []
        for key in order:
            tex, mode = key
            b = by_mat[key]
            xyz = np.ascontiguousarray(np.concatenate(b['pos']))
            uv = np.ascontiguousarray(np.concatenate(b['uv']))
            idx = np.ascontiguousarray(np.concatenate(b['idx']))
            sp, lp = self._add(xyz.tobytes())
            su, lu = self._add(uv.tobytes())
            si, li = self._add(idx.tobytes())
            base = len(self.views)
            self.views += [dict(buffer=0, byteOffset=sp, byteLength=lp),
                           dict(buffer=0, byteOffset=su, byteLength=lu),
                           dict(buffer=0, byteOffset=si, byteLength=li)]
            mn, mx = xyz.min(0), xyz.max(0)
            a = self.accessors
            a.append(dict(bufferView=base, componentType=5126, count=len(xyz), type='VEC3',
                          min=[float(x) for x in mn], max=[float(x) for x in mx]))
            a.append(dict(bufferView=base + 1, componentType=5126, count=len(uv), type='VEC2'))
            a.append(dict(bufferView=base + 2, componentType=5125, count=len(idx), type='SCALAR'))
            prims.append(dict(attributes=dict(POSITION=len(a) - 3, TEXCOORD_0=len(a) - 2),
                              indices=len(a) - 1, material=self.material_for(tex, mode), mode=4))
        if not prims:
            return False
        mi = len(self.meshes)
        self.meshes.append(dict(name=name, primitives=prims))
        self.nodes.append(dict(mesh=mi, name=name))
        return True

    def write(self, out_path):
        pad = (-len(self.buf)) % 4
        self.buf.extend(b'\0' * pad)
        gltf = dict(
            asset=dict(version='2.0', generator='tdkr-export-zone-v1'),
            scene=0, scenes=[dict(nodes=list(range(len(self.nodes))))],
            nodes=self.nodes, meshes=self.meshes, materials=self.materials,
            accessors=self.accessors, bufferViews=self.views,
            buffers=[dict(byteLength=len(self.buf))])
        js = json.dumps(gltf, separators=(',', ':')).encode()
        js += b' ' * ((-len(js)) % 4)
        total = 12 + 8 + len(js) + 8 + len(self.buf)
        with open(out_path, 'wb') as fo:
            fo.write(struct.pack('<III', 0x46546C67, 2, total))
            fo.write(struct.pack('<II', len(js), 0x4E4F534A))
            fo.write(js)
            fo.write(struct.pack('<II', len(self.buf), 0x004E4942))
            fo.write(self.buf)
        return os.path.getsize(out_path)


def main():
    os.makedirs(MODELS, exist_ok=True)
    os.makedirs(TEXD, exist_ok=True)
    manifest_path = os.path.join(MODELS, 'manifest.json')
    manifest = json.load(open(manifest_path)) if os.path.exists(manifest_path) else dict(
        tiers={}, glbs=[], total_verts=0, total_tris=0, version=9)

    used_tex = set()
    st_glbs = []
    XSECS = {
        'GothamCity_Road_v1_Island_1': cross_sections('GothamCity_Road_v1_Island_1'),
        'GothamCity_Road_v2_Island_1': cross_sections('GothamCity_Road_v2_Island_1'),
        'GothamCity_Road_Island_2': cross_sections('GothamCity_Road_Island_2'),
        'gothamcity_roads_details': cross_sections('gothamcity_roads_details'),
        'GothamCity_Road_Crossings_Island_1': cross_sections('GothamCity_Road_Crossings_Island_1'),
        'GothamCity_Road_Crossings_Island_2': cross_sections('GothamCity_Road_Crossings_Island_2'),
    }
    for islname, isl in ISLANDS.items():
        xs = {k: v for k, v in XSECS.items()
              if (isl['isl'] == '1' and ('Island_1' in k or 'details' in k))
              or (isl['isl'] == '2' and ('Island_2' in k or 'details' in k))}
        segs = parse_island(islname)
        print(f'{islname}: {len(segs)} segments')
        binds = []
        stats = dict(dark=0, road=0, flat=0, prop=0, bake=0)
        for s in segs:
            tex, mode = bind_segment(s, isl, xs)
            if tex is None:
                stats['dark'] += 1
            elif mode == '2x':
                stats['bake' if 'BakeGroup' in tex or 'LongDist' in tex else 'road'] += 1
            else:
                stats['road' if 'Road' in tex else ('prop' if 'Props' in tex else 'flat')] += 1
            binds.append((s, tex, mode))
            if tex:
                used_tex.add(tex)
        print('  binding stats:', stats)

        # pack into spatial chunks: grid binning on (x, y) means
        xs = np.array([s['pos'][:, 0].mean() for s in segs])
        ys = np.array([s['pos'][:, 1].mean() for s in segs])
        gx = ((xs - xs.min()) / max(np.ptp(xs), 1) * 4).clip(0, 3).astype(int)
        gy = ((ys - ys.min()) / max(np.ptp(ys), 1) * 3).clip(0, 2).astype(int)
        buckets = {}
        for i in range(len(segs)):
            buckets.setdefault((int(gx[i]), int(gy[i])), []).append(i)
        chunks = [v for k, v in sorted(buckets.items())]
        for ci, chunk in enumerate(chunks):
            gb = GlbBuilder()
            nv = nt = 0
            for i in chunk:
                s, tex, mode = binds[i]
                tris = strip_to_tris(s['idx'])
                if not gb.add_segment_mesh(f'seg_{i}', [(s, tex, mode)]):
                    continue
                nv += len(s['pos']); nt += len(tris)
            if not nt:
                continue
            name = f'street_{"island1" if isl["isl"]=="1" else "island2"}_{ci:02d}.glb'
            size = gb.write(os.path.join(MODELS, name))
            st_glbs.append(dict(file='models/' + name, bytes=size, verts=nv, tris=nt,
                                tier='street', files=[dict(name=name[:-4], verts=nv, tris=nt,
                                                           meshes=len(chunk))]))
            print(f'  + {name:<32} {size/1024:>7.0f} KB {nt:>8,} tris')

    # export textures used
    for t in sorted(used_tex):
        src = find_png(t)
        if not src:
            print('  !! missing:', t)
            continue
        n = t + '.jpg'
        sz = jpg_from_png(src, os.path.join(TEXD, n), 2048, 88)
        print(f'  tex {n:<44} {sz/1024:>6.0f} KB')

    # merge into manifest (replace existing street tier)
    manifest['glbs'] = [g for g in manifest['glbs'] if g.get('tier') != 'street'] + st_glbs
    manifest['tiers']['street'] = [g['file'] for g in st_glbs]
    manifest['version'] = 11
    tv = sum(g['verts'] for g in manifest['glbs'])
    tt = sum(g['tris'] for g in manifest['glbs'])
    manifest['total_verts'] = tv
    manifest['total_tris'] = tt
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=1)
    print(f"manifest v10: +{len(st_glbs)} street GLBs, totals {tv:,}v {tt:,}t")


if __name__ == '__main__':
    main()
