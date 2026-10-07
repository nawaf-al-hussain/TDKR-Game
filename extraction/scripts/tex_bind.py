#!/usr/bin/env python3
"""Texture binding resolver for TDKR city meshes.

Resolution per mesh (footer material name = game ground truth for the material):
  1. material name matches a pool candidate (normalized)  -> bind
  2. exactly one diffuse candidate in the file's pool      -> bind
  3. UV-fit scoring among pool candidates                  -> per-mesh argmax
  4. no candidates: UV-fit vs island bake-atlas family     -> bind if above threshold
  5. else                                                  -> None (dark fallback)

UV-fit score for (mesh, tex):
    ratio = mean(edge_map[sampled uv]) / mean(edge_map)
  i.e. does this mesh sample above-average-detail regions of the texture.
Validated against uv-verified bindings (island1 -> GC_Island1_LongDist_Low etc).
"""
import os
import re
import numpy as np
from PIL import Image

PNG = "/home/z/my-project/download/TDKR_assets/textures_png"
SUBS = ("l_gothamcity_tex", "actors_tex", "vehicles_tex", "commons_tex")

BAD_PAT = re.compile(r"(_nrm|lightmap|_lm$|_mask|sampler|shadow|_bump|_spec|_gloss|"
                     r"_opacity|_height|_normal|_refl|_Refl|_rfl|font|_Emissive)", re.I)

# island bake atlas family for footprint fallback
BAKE_FAMILY = [
    "GC_Island1_LongDist_Low", "GC_Island2_LongDist_low",
    "GC_LongDist_Island1_FP1", "GC_LongDist_Island1_FP2", "GC_LongDist_Island1_FP3",
    "GC_LongDist_Island2_FP1", "GC_LongDist_Island2_FP2", "GC_LongDist_Island2_FP3",
    "GC_LongDist_Island1_Roads", "GC_LongDist_Island2_Roads",
    "BakeGroup_Island1_A0", "BakeGroup_Island1_B0", "BakeGroup_Island1_Roads0",
    "BakeGroup_Island2_A0", "BakeGroup_Island2_B0", "BakeGroup_Island2_Roads0",
    "BakeGroup_Island1_Landmarks0", "BakeGroup_Island1_ATLAS_low0",
    "BakeGroup_Island2_ATLAS_low0",
]

_edge_cache = {}

def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())

def find_png(name):
    for sub in SUBS:
        p = os.path.join(PNG, sub, name + ".png")
        if os.path.exists(p):
            return p
    return None

def edge_map(name, size=512):
    """normalized edge-magnitude map of a texture, downscaled to size"""
    if name in _edge_cache:
        return _edge_cache[name]
    p = find_png(name)
    if p is None:
        _edge_cache[name] = None
        return None
    im = Image.open(p).convert("L")
    im.thumbnail((size, size), Image.BILINEAR)
    a = np.asarray(im, np.float32) / 255.0
    gx = np.zeros_like(a); gy = np.zeros_like(a)
    gx[:, 1:-1] = a[:, 2:] - a[:, :-2]
    gy[1:-1, :] = a[2:, :] - a[:-2, :]
    e = np.sqrt(gx * gx + gy * gy)
    m = float(e.mean()) + 1e-6
    _edge_cache[name] = (e / m, a.shape)
    return _edge_cache[name]

def uv_fit_score(uv, name):
    """ratio of sampled edge magnitude over texture average (>=1 = detail-rich)"""
    em = edge_map(name)
    if em is None:
        return -1.0
    e, (h, w) = em
    u = np.clip((uv[:, 0] * (w - 1)), 0, w - 1).astype(np.int32)
    v = np.clip((uv[:, 1] * (h - 1)), 0, h - 1).astype(np.int32)
    s = e[v, u]
    # subsample huge meshes for speed
    if len(s) > 20000:
        s = s[:: len(s) // 20000]
    return float(s.mean())

def diffuse_candidates(pool):
    """pool names that exist on disk and are diffuse-like"""
    out = []
    for t in pool:
        if BAD_PAT.search(t):
            continue
        if find_png(t):
            out.append(t)
    return out

def resolve_file(base, meshes, pool, verbose=False):
    """return per-mesh tex list (len == len(meshes), entries may be None)"""
    cands = diffuse_candidates(pool)
    per_mesh = [None] * len(meshes)

    # 1) material-name matches
    by_norm = {norm(c): c for c in cands}
    unmatched = []
    for i, m in enumerate(meshes):
        mn = norm(m.get("material") or "")
        hit = by_norm.get(mn)
        if hit:
            per_mesh[i] = hit
        else:
            unmatched.append(i)

    # 2) single candidate
    if len(cands) == 1:
        for i in unmatched:
            per_mesh[i] = cands[0]
        unmatched = []

    # 3) UV-fit among candidates
    for i in unmatched:
        uv = meshes[i]["uv"]
        scored = sorted(((uv_fit_score(uv, c), c) for c in cands), reverse=True)
        if verbose and scored:
            print(f"    {base} mesh{i} mat={meshes[i].get('material')!r}: " +
                  ", ".join(f"{c}={s:.2f}" for s, c in scored[:4]))
        per_mesh[i] = scored[0][1] if scored and scored[0][0] > 0 else None

    # 4) no candidates at all: try island bake family (footprints/districts)
    if not cands:
        for i in range(len(meshes)):
            uv = meshes[i]["uv"]
            scored = sorted(((uv_fit_score(uv, c), c) for c in BAKE_FAMILY), reverse=True)
            best = scored[0] if scored else (0, None)
            per_mesh[i] = best[1] if best[0] >= 1.35 else None
    return per_mesh
