#!/usr/bin/env python3
"""s42 T1: content check - Batman belt/chest region means under RGB vs BGR read.
Engine evidence (disasm) says header code 0x15 -> E_PIXEL_FORMAT::R8G8B8 (R in byte0).
This script provides the independent CONTENT check: known-colour regions must be
yellow (belt) / skin (face) under the CORRECT order, blue-ish under the wrong one.
"""
import struct, sys, zipfile, json, hashlib
import numpy as np

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session41')
from s41_refdec_lib import read_archive

Z = zipfile.ZipFile('/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')

def get_rgb888(arch, name):
    d, ents = read_archive(Z, arch)
    for (n, off, size) in ents:
        if n == name:
            full = d[off:off + size]
            hs, hgt, wid, mips, flags, dsz, bpp = struct.unpack_from('<7I', full[:52], 0)
            assert bpp == 24 and (flags & 0xff) == 0x15 and hs == 52, (hs, bpp, hex(flags))
            raw = np.frombuffer(full[52:52 + wid * hgt * 3], np.uint8).reshape(hgt, wid, 3)
            return raw, (hs, hgt, wid, mips, flags, dsz, bpp)
    raise KeyError(name)

print("=== all 8 RGB888 chunks: header + per-channel means under both reads ===")
CHUNKS = [
    ('actors_tex.gla', 'chara_Batman_DIFFUSE.tga'),
    ('actors_tex.gla', 'chara_Batman_NM.tga'),
    ('actors_tex.gla', 'chara_BATMAN_specular_1024.tga'),
    ('commons_tex.gla', 'GC_Skybox.tga'),
    ('commons_tex.gla', 'GC_Skybox_02.tga'),
    ('commons_tex.gla', 'GC_Skybox_02_Industrial.tga'),
    ('commons_tex.gla', 'GC_Skybox_City.tga'),
    ('l_gothamcity_tex.gla', 'City_BKG.tga'),
]
rows = []
for arch, name in CHUNKS:
    raw, hdr = get_rgb888(arch, name)
    rgb = raw.reshape(-1, 3).astype(np.float64)
    m_rgb = rgb.mean(0)
    m_bgr = rgb[:, ::-1].mean(0)
    print(f"{name:34s} hdr hs={hdr[0]} w={hdr[2]} h={hdr[1]} code={hdr[4] & 0xff:#x} bpp={hdr[6]}")
    print(f"   mean as RGB : R={m_rgb[0]:7.2f} G={m_rgb[1]:7.2f} B={m_rgb[2]:7.2f}")
    print(f"   mean as BGR : R={m_bgr[0]:7.2f} G={m_bgr[1]:7.2f} B={m_bgr[2]:7.2f}")
    rows.append((name, m_rgb, m_bgr))

# ---- Batman DIFFUSE region analysis ----
raw, hdr = get_rgb888('actors_tex.gla', 'chara_Batman_DIFFUSE.tga')
H, W, _ = raw.shape
rgb = raw.reshape(-1, 3).astype(np.int32)

print("\n=== Batman DIFFUSE: order-discriminating cluster census (whole texture) ===")
# yellow-ish: R,G high, B low  (correct read => belt/emblem gold)
yellow_rgb = int(((rgb[:, 0] > 170) & (rgb[:, 1] > 130) & (rgb[:, 2] < 130) & (rgb[:, 0] + rgb[:, 1] - 2 * rgb[:, 2] > 120)).sum())
# blue-ish: B high, R low (in RGB read; would be the belt if BGR were correct)
blue_rgb = int(((rgb[:, 2] > 170) & (rgb[:, 1] > 130) & (rgb[:, 0] < 130) & (2 * rgb[:, 2] - rgb[:, 0] - rgb[:, 1] > 120)).sum())
print(f"  yellow-cluster texels (R,G>>B): {yellow_rgb}  ({100.0 * yellow_rgb / rgb.shape[0]:.3f}%)")
print(f"  blue-cluster  texels (B,G>>R): {blue_rgb}  ({100.0 * blue_rgb / rgb.shape[0]:.3f}%)")
print(f"  ratio yellow/blue = {yellow_rgb / max(blue_rgb, 1):.1f}x")

# ---- UV-region means from the deployed batman.glb ----
print("\n=== Batman DIFFUSE: belt/chest/face UV-region means (from batman.glb bind mesh) ===")
glb = open('/tmp/my-project/work/TDKR-Game/gh-pages/playable/batman.glb', 'rb').read()
assert glb[:4] == b'glTF'
jlen, jtype = struct.unpack_from('<I4s', glb, 12)
g = json.loads(glb[20:20 + jlen])
bin_off = 20 + jlen
# single mesh, find primitive with TEXCOORD_0 + POSITION
prim = g['meshes'][0]['primitives'][0]
acc = g['accessors']
bv = g['bufferViews']

def read_acc(idx):
    a = acc[idx]
    v = bv[a['bufferView']]
    off = bin_off + v.get('byteOffset', 0) + a.get('byteOffset', 0)
    n = a['count']
    comp = {'VEC3': 3, 'VEC2': 2, 'SCALAR': 1}[a['type']]
    arr = np.frombuffer(glb, np.float32, n * comp, off).reshape(n, comp)
    return arr

POS = read_acc(prim['attributes']['POSITION'])
UV = read_acc(prim['attributes']['TEXCOORD_0'])
IDX = None
if 'indices' in prim:
    ai = acc[prim['indices']]
    v = bv[ai['bufferView']]
    off = bin_off + v.get('byteOffset', 0)
    IDX = np.frombuffer(glb, np.uint16 if ai['componentType'] == 5123 else np.uint32, ai['count'], off)

P = POS
zmax, zmin = float(P[:, 2].max()), float(P[:, 2].min())
hgt_world = zmax - zmin
print(f"  bind mesh: {len(P)} verts, z range [{zmin:.3f},{zmax:.3f}] (z-up bind space), height {hgt_world:.3f}")

def region_mean(zlo_f, zhi_f, label):
    zlo = zmin + zlo_f * hgt_world
    zhi = zmin + zhi_f * hgt_world
    sel = (P[:, 2] >= zlo) & (P[:, 2] <= zhi)
    if IDX is not None:
        tri_sel = sel[IDX].reshape(-1, 3).all(axis=1)
        idxs = IDX.reshape(-1, 3)[tri_sel].reshape(-1)
    else:
        idxs = np.nonzero(sel)[0]
    uvs = UV[idxs]
    u = np.clip(uvs[:, 0], 0, 0.999); v = np.clip(uvs[:, 1], 0, 0.999)
    # glTF UV origin top-left; texture row = v*h
    px = raw[(v * H).astype(np.int32), (u * W).astype(np.int32)].astype(np.float64)
    m1 = px.mean(0)                    # as RGB
    m2 = px[:, ::-1].mean(0)           # as BGR
    print(f"  {label:6s} ({len(idxs):5d} uv-samples) as RGB: R={m1[0]:6.1f} G={m1[1]:6.1f} B={m1[2]:6.1f} | as BGR: R={m2[0]:6.1f} G={m2[1]:6.1f} B={m2[2]:6.1f}")
    return m1, m2

belt = region_mean(0.50, 0.63, 'BELT')
chest = region_mean(0.66, 0.80, 'CHEST')
face = region_mean(0.86, 0.99, 'FACE')
