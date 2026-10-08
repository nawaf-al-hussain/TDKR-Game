#!/usr/bin/env python3
"""BDAE mesh extractor — parses chained mesh blocks in the BRES geometry section
and exports glTF-Binary (GLB) + stats.

Verified vertex format (static geometry):
  stride = 8 + ndw*4 where ndw = geo_header[12]
  +0  pos     3 x f32
  +12 normal  packed 11-11-10 snorm (x:y:z = 11:11:10 bits, scale 1023/1023/511)
  +16 uv      2 x u16 unorm (/65535)
  +20 extra   (24B meshes: packed lightmap-uv or tangent dword)
mesh block chain: geo header (26 u32, signature fields[2..9] == 5C 4C A8 40 34 28 1C 10)
  stream_end = G + fields[1]; verts = COUNT=fields[11] entries ending at stream_end
  footer = G + fields[0]: [maxIdx][numIdx][stride][0][0]['bdae'][pad0]
  indices = numIdx x u16 at footer+0x1C; next header = footer+0x1C+numIdx*2
"""
import struct, sys, os, json
import numpy as np

BASE = '/home/z/my-project/download/TDKR_assets/raw'
PNG = '/home/z/my-project/download/TDKR_assets/textures_png'
SIG = (0x5C, 0x4C, 0xA8, 0x40, 0x34, 0x28, 0x1C, 0x10)

def decode_normal(dw):
    x = (dw & 0x7FF)
    if x >= 1024: x -= 2048
    y = ((dw >> 11) & 0x7FF)
    if y >= 1024: y -= 2048
    z = ((dw >> 22) & 0x3FF)
    if z >= 512: z -= 1024
    n = np.array([x / 1023.0, y / 1023.0, z / 511.0], np.float32)
    ln = np.linalg.norm(n)
    return n / ln if ln > 1e-6 else np.array([0, 0, 1], np.float32)

def plausible(x):
    return abs(x) < 1e5 and (x == 0.0 or 1e-7 < abs(x) < 1e7)

def parse_first_block(d, G, verbose=False):
    """Robustly locate (COUNT, ndw, start) for the mesh block at geo header G.
    Header layout varies: [f0, f1, <k pairs>, 0x10, 1, COUNT, ndw, ...].
    Anchors: fields f0/f1 = footer/stream-end offsets; footer triple (maxIdx, numIdx, _)."""
    f = struct.unpack_from('<40I', d, G)
    cands = []
    for i in range(2, 36):
        if f[i] == 0x10 and f[i + 1] == 1:
            for COUNT, ndw in ((f[i + 2], f[i + 3]), (f[i + 3], f[i + 2])):
                if not (0 < COUNT < 2_000_000 and 1 <= ndw <= 12):
                    continue
                stride = 8 + ndw * 4
                end = G + f[1]
                start = end - COUNT * stride
                footer = G + f[0] - 8
                if not (start > G + 0x40 and footer + 0x1C <= len(d) and start < end):
                    continue
                maxIdx, numIdx, _ = struct.unpack_from('<3I', d, footer)
                if numIdx == 0 or numIdx % 3 or numIdx > 12 * COUNT or maxIdx >= COUNT:
                    continue
                if footer + 0x1C + numIdx * 2 > len(d):
                    continue
                # score position plausibility over all entries
                ok = 0
                step = max(1, COUNT // 500)
                n = 0
                for vi in range(0, COUNT, step):
                    x, y, z = struct.unpack_from('<3f', d, start + vi * stride)
                    ok += plausible(x) and plausible(y) and plausible(z)
                    n += 1
                score = ok / n
                cands.append((score, COUNT, ndw, stride, start, footer, maxIdx, numIdx))
    if not cands:
        return None
    cands.sort(key=lambda c: -c[0])
    best = cands[0]
    if best[0] < 0.98:
        if verbose:
            print(f'    low plausibility {best[0]:.2f} at G={G:#x}')
        return None
    return best  # (score, COUNT, ndw, stride, start, footer, maxIdx, numIdx)

def parse_meshes(path, verbose=True):
    d = open(path, 'rb').read()
    h = struct.unpack_from('<14I', d, 0)
    G = h[10]
    meshes = []
    g = G
    while g + 0x68 <= len(d):
        blk = parse_first_block(d, g, verbose)
        if blk is None:
            break
        score, count, ndw, stride, start, footer, maxIdx, numIdx = blk
        # footer: [maxIdx][numIdx][X][0][0][matname NUL-padded to 4][indices...]
        s0 = footer + 0x14
        e = d.index(b'\0', s0)
        mat = d[s0:e].decode('ascii', 'replace')
        idx_off = s0 + ((e - s0 + 1 + 3) & ~3)
        pos = np.zeros((count, 3), np.float32)
        nrm = np.zeros((count, 3), np.float32)
        uv = np.zeros((count, 2), np.float32)
        for i in range(count):
            o = start + i * stride
            pos[i] = struct.unpack_from('<3f', d, o)
            nrm[i] = decode_normal(struct.unpack_from('<I', d, o + 12)[0])
            u, v = struct.unpack_from('<2H', d, o + 16)
            uv[i] = (u / 65535.0, v / 65535.0)
        idx = np.frombuffer(d, np.uint16, numIdx, idx_off).astype(np.uint32)
        if not np.isfinite(pos).all() or not np.isfinite(pos[idx]).all():
            if verbose:
                print(f'  mesh@{g:#x}: rejected (non-finite positions)')
            break
        meshes.append(dict(offset=g, count=count, stride=stride, numIdx=numIdx,
                           maxIdx=int(maxIdx), ndw=ndw, material=mat,
                           pos=pos, nrm=nrm, uv=uv, idx=idx,
                           mn=pos.min(0), mx=pos.max(0)))
        if verbose:
            print(f'  mesh@{g:#x}: verts={count:6d} stride={stride} tris={numIdx//3:6d} '
                  f'maxIdx={maxIdx:6d} mat={mat!r} min={np.round(pos.min(0), 3)} max={np.round(pos.max(0), 3)}')
        g = (idx_off + numIdx * 2 + 3) & ~3  # next geo header is 4-aligned
    return meshes

def write_glb(meshes, tex_path, out_path, name='mesh', yup=True, max_tex=2048):
    """minimal GLB writer: one PRIMITIVE per mesh, shared material+texture.
    yup=True converts game coords (Z-up, Max-style) to glTF Y-up: (x, y, z)_g -> (x, z, -y)_gl."""
    import PIL.Image as Image
    io = __import__('io')
    bin_chunks, nodes, prims, offset = [], [], [], 0
    total_v = sum(m['count'] for m in meshes)
    total_i = sum(m['numIdx'] for m in meshes)
    buf = bytearray()
    # interleave accessors separately (simple: one buffer view per mesh stream)
    def add(data, align=4):
        nonlocal offset
        pad = (-len(buf)) % align
        buf.extend(b'\0' * pad)
        offset += pad
        start = offset
        buf.extend(data)
        offset += len(data)
        return start, len(data)
    views = {}
    for mi, m in enumerate(meshes):
        if yup:
            pos = m['pos'][:, [0, 2, 1]].copy()
            pos[:, 2] = -m['pos'][:, 1]
            nrm = m['nrm'][:, [0, 2, 1]].copy()
            nrm[:, 2] = -m['nrm'][:, 1]
        else:
            pos, nrm = m['pos'], m['nrm']
        for key, arr, comp in (('pos', pos, 3), ('nrm', nrm, 3), ('uv', m['uv'], 2)):
            a = arr.astype(np.float32)
            if key == 'uv' and a is not None and len(a):
                # v10: game UVs are bottom-origin; glTF samples v=0 at top row
                a = a.copy()
                a[:, 1] = 1.0 - a[:, 1]
            s, l = add(a.tobytes())
            views[(mi, key)] = (s, l, len(a))
        idx = m['idx'].astype(np.uint32)
        s, l = add(idx.tobytes())
        views[(mi, 'idx')] = (s, l, len(idx))
    # texture
    img_data, img_mime = None, None
    if tex_path and os.path.exists(tex_path):
        im = Image.open(tex_path).convert('RGBA')
        if max(im.size) > max_tex:
            im.thumbnail((max_tex, max_tex), Image.LANCZOS)
        b = io.BytesIO(); im.save(b, 'PNG')
        img_data, img_mime = b.getvalue(), 'image/png'
    img_view = None
    if img_data:
        s, l = add(img_data)
        img_view = (s, l)
    pad_end = (-len(buf)) % 4
    buf.extend(b'\0' * pad_end)

    accessors, prims = [], []
    def acc(view, comp_type, count, amin, amax, vtype):
        accessors.append(dict(bufferView=view, componentType=comp_type, count=count,
                              type=vtype, **({'min': list(amin), 'max': list(amax)} if amin is not None else {})))
        return len(accessors) - 1
    VIEWS = []
    for (mi, key), (s, l, n) in sorted(views.items()):
        VIEWS.append(dict(buffer=0, byteOffset=s, byteLength=l))
    view_id = {k: i for i, k in enumerate(sorted(views.keys()))}
    for mi, m in enumerate(meshes):
        pos = m['pos'][:, [0, 2, 1]].copy() if yup else m['pos']
        if yup:
            pos[:, 2] = -m['pos'][:, 1]
        assert np.isfinite(pos).all(), f'mesh {mi} has non-finite positions'
        mn, mx = pos.min(0), pos.max(0)
        a_pos = acc(view_id[(mi, 'pos')], 5126, m['count'], [float(v) for v in mn], [float(v) for v in mx], 'VEC3')
        a_nrm = acc(view_id[(mi, 'nrm')], 5126, m['count'], None, None, 'VEC3')
        a_uv = acc(view_id[(mi, 'uv')], 5126, m['count'], None, None, 'VEC2')
        a_idx = acc(view_id[(mi, 'idx')], 5125, m['numIdx'], None, None, 'SCALAR')
        prims.append(dict(attributes=dict(POSITION=a_pos, NORMAL=a_nrm, TEXCOORD_0=a_uv),
                          indices=a_idx, material=0, mode=4))
    gltf = dict(
        asset=dict(version='2.0', generator='tdkr-bdae-extract'),
        scene=0, scenes=[dict(nodes=[0], name=name)],
        nodes=[dict(mesh=0, name=name)],
        meshes=[dict(primitives=prims, name=name)],
        materials=[dict(pbrMetallicRoughness=dict(baseColorTexture=dict(index=0),
                                                  metallicFactor=0.0, roughnessFactor=0.9),
                        doubleSided=True)],
        textures=[dict(source=0, sampler=0)],
        images=[dict(bufferView=len(VIEWS), mimeType=img_mime)] if img_view else [],
        samplers=[dict(magFilter=9729, minFilter=9987, wrapS=33071, wrapT=33071)],
        accessors=accessors, bufferViews=VIEWS,
        buffers=[dict(byteLength=len(buf))])
    if img_view:
        gltf['bufferViews'].append(dict(buffer=0, byteOffset=img_view[0], byteLength=img_view[1]))
    js = json.dumps(gltf, separators=(',', ':')).encode()
    js += b' ' * ((-len(js)) % 4)
    total = 12 + 8 + len(js) + 8 + len(buf)
    with open(out_path, 'wb') as fo:
        fo.write(struct.pack('<III', 0x46546C67, 2, total))
        fo.write(struct.pack('<II', len(js), 0x4E4F534A)); fo.write(js)
        fo.write(struct.pack('<II', len(buf), 0x004E4942)); fo.write(buf)
    return len(buf)

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('files', nargs='+')
    ap.add_argument('--outdir', default='/home/z/my-project/download/TDKR_assets/meshes_glb')
    ap.add_argument('--no-glb', action='store_true')
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    for p in args.files:
        base = os.path.basename(p).replace('.bdae.bin', '')
        print(f'== {base}')
        meshes = parse_meshes(p)
        print(f'   total: {len(meshes)} meshes, {sum(m["count"] for m in meshes)} verts, '
              f'{sum(m["numIdx"]//3 for m in meshes)} tris')
        if not args.no_glb and meshes:
            # heuristic texture: first *.tga in string pool that is not _NRM/_LM/lightmap
            import re
            strs = [m.group().decode() for m in re.finditer(rb'[ -~]{4,}', open(p, 'rb').read())]
            tex = None
            for s in strs:
                if s.endswith('.tga') and not any(k in s.lower() for k in ('_nrm', 'lightmap', '_lm', '_mask', '_refl', 'sampler')):
                    tex = os.path.join(PNG, 'l_gothamcity_tex', s.replace('.tga', '.png'))
                    if not os.path.exists(tex):
                        tex = os.path.join(PNG, 'actors_tex', s.replace('.tga', '.png'))
                    if os.path.exists(tex):
                        break
                    tex = None
            out = os.path.join(args.outdir, base + '.glb')
            write_glb(meshes, tex, out, base)
            print(f'   GLB -> {out}  (texture: {os.path.basename(tex) if tex else None})')
