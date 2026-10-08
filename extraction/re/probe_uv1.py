#!/usr/bin/env python3
"""Probe: which UV channel carries the Beast bake coords — UV0 (+16) or the
discarded +20 dword in 24B-stride meshes?  For each bake_regions_v2 record we
rasterize the mesh's candidate UV (transformed by so1) into the assigned page
and measure Sobel-edge alignment inside the mask.  The channel that aligns
with the page's content edges is the engine's Coord1 (lightmap UV)."""
import json, os, re, struct, sys
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, '/home/z/my-project/work/TDKR-Game/extraction/re')
from gla_pull import entries, pull

GLA = '/home/z/my-project/download/TDKR_assets/raw/l_gothamcity.gla'
RECS = '/home/z/my-project/work/TDKR-Game/extraction/re/bake_regions_v2.json'
PAGES = '/home/z/my-project/download/TDKR_assets/pages'
TMP = '/tmp/uv1_probe'
PAGE_PX = 2048


def parse_meshes_uv1(path):
    """bdae_extract.parse_meshes + candidate UV1 from +20 (24B meshes only)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        'bdae_extract', '/home/z/my-project/work/TDKR-Game/extraction/scripts/bdae_extract.py')
    be = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(be)
    d = open(path, 'rb').read()
    h = struct.unpack_from('<14I', d, 0)
    g = h[10]
    out = []
    while g + 0x68 <= len(d):
        blk = be.parse_first_block(d, g, verbose=False)
        if blk is None:
            break
        score, count, ndw, stride, start, footer, maxIdx, numIdx = blk
        s0 = footer + 0x14
        e = d.index(b'\0', s0)
        idx_off = s0 + ((e - s0 + 1 + 3) & ~3)
        uv0 = np.zeros((count, 2), np.float32)
        uv1 = np.zeros((count, 2), np.float32)
        has1 = stride >= 24
        for i in range(count):
            o = start + i * stride
            u, v = struct.unpack_from('<2H', d, o + 16)
            uv0[i] = (u / 65535.0, v / 65535.0)
            if has1:
                u1, v1 = struct.unpack_from('<2H', d, o + 20)
                uv1[i] = (u1 / 65535.0, v1 / 65535.0)
        idx = np.frombuffer(d, np.uint16, numIdx, idx_off).astype(np.uint32)
        if idx.max() >= count:
            break  # misparsed block — stop chain like the base parser does
        out.append(dict(offset=g, count=count, stride=stride, uv0=uv0, uv1=uv1,
                        idx=idx, has1=has1, numIdx=numIdx))
        g = (idx_off + numIdx * 2 + 3) & ~3
    return out


def sobel(gray):
    gx = np.zeros_like(gray); gy = np.zeros_like(gray)
    gx[:, 1:-1] = gray[:, 2:] - gray[:, :-2]
    gy[1:-1, :] = gray[2:, :] - gray[:-2, :]
    return np.hypot(gx, gy)


def raster_mask(uv, idx, shape=(PAGE_PX, PAGE_PX)):
    im = Image.new('L', (shape[1], shape[0]), 0)
    dr = ImageDraw.Draw(im)
    tri = uv[idx].reshape(-1, 3, 2) * PAGE_PX
    for t in tri:
        dr.polygon([tuple(p) for p in t], fill=255)
    return np.asarray(im) > 0


def score(page_edges, mask):
    inside = page_edges[mask].mean() if mask.any() else 0.0
    return inside / (page_edges.mean() + 1e-9)


def main():
    os.makedirs(TMP, exist_ok=True)
    recs = json.load(open(RECS))
    pages = {}
    for r in recs:
        p = (r.get('page') or '').replace('.tga', '')
        if p and p not in pages:
            fp = os.path.join(PAGES, p + '.png')
            if os.path.exists(fp):
                g = np.asarray(Image.open(fp).convert('L'), np.float32) / 255.0
                pages[p] = sobel(g)
    print('pages loaded:', list(pages))

    f, ents = entries(GLA)
    # map record mesh -> bdae chunk (case-insensitive, LongDist suffix variants)
    lowers = {n.lower(): n for n in ents}
    tested = 0
    for r in recs:
        mesh = r.get('mesh') or ''
        page = (r.get('page') or '').replace('.tga', '')
        so1 = r.get('so1')
        if not mesh or page not in pages or not so1:
            continue
        cands = [mesh + '.bdae', mesh + '_longdist.bdae']
        chunk = None
        for c in cands:
            if c in lowers:
                chunk = lowers[c]; break
        if chunk is None:
            # substring pass
            hits = [n for n in lowers if n.startswith(mesh.lower()) and 'longdist' in n and 'collision' not in n and 'reflect' not in n]
            if hits:
                chunk = sorted(hits)[0]
        if chunk is None:
            continue
        path = os.path.join(TMP, chunk)
        if not os.path.exists(path):
            f.seek(ents[chunk][0]); open(path, 'wb').write(f.read(ents[chunk][1]))
        meshes = parse_meshes_uv1(path)
        if not meshes:
            print(f'{mesh}: no meshes parsed'); continue
        su, sv, ou, ov = so1
        edges = pages[page]
        for mi, m in enumerate(meshes):
            if m['numIdx'] < 9 or m['count'] < 3:
                continue
            res = {}
            for tag, uv in (('uv0', m['uv0']), ('uv1', m['uv1'])):
                if tag == 'uv1' and not m['has1']:
                    continue
                t = np.column_stack([uv[:, 0] * su + ou, uv[:, 1] * sv + ov])
                mask = raster_mask(t, m['idx'])
                res[tag] = score(edges, mask)
                # flipV control: page content flipped
                res[tag + '_flipV'] = score(sobel(np.asarray(
                    Image.open(os.path.join(PAGES, page + '.png')).convert('L'), np.float32) / 255.0)[::-1, :], mask)
            print(f"{mesh:34s} p={page:26s} m{mi} v={m['count']:5d} st={m['stride']} "
                  + ' '.join(f'{k}={v:5.2f}' for k, v in res.items()))
            tested += 1
        if tested > 40:
            break


if __name__ == '__main__':
    main()
