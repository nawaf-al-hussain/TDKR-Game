#!/usr/bin/env python3
"""Full-city LOD-aware GLB exporter v4 — GROUND TRUTH bindings + ENGINE SHADING.

v4 adds the game's own shading model, recovered from the shipped GLSL
(effects/LightMapDC-v.glsl, LightMapDC-f.glsl — plain text in the .gla):

    LightMapColor  = texture2D(LightMap, vCoord1) * 2.0;
    Color          = DiffuseMapColor * LightMapColor;

City bakes bind LightMap = UNBOUND (texIdx 0xFFFFFFFF) -> engine supplies a
white texture -> Color = bake * 2.0 (overbright night look).  Bakes are
authored dark (mean ~0.11) for exactly this reason.

Per-primitive material NAME now encodes the shading mode:

    '<tex>|2x'  LightMapDC technique  -> viewer multiplies by 2.0
    '<tex>|d'   StandardDiffuseDC etc -> viewer shows diffuse at 1.0
    '__dark'    untextured

Viewer contract unchanged otherwise: texture stem -> models/tex/<name>.jpg,
flipY=false (PVR top-down).

v3 replaces ALL texture heuristics with the game's own data, decoded from the
BRES material system (see ground_truth.py):

  - per-file texture list (ordered, from the meta section)
  - per render unit: material -> technique -> sampler records
  - sampler value block: [ptr->Coord0_scaleoffset vec4, wraps..., texIdx]
  - mesh footer material name joins mesh -> unit -> DiffuseMap texture index

Binding ladder per mesh:
  0. ground-truth DiffuseMap (deterministic, 97% of hero/low/district meshes)
  1. same name minus '_alpha' suffix (alpha variant shares RGB art)
  2. UV-fit among the file's own texture list that exists on disk
  3. footprint files: UV-fit among the island's bake family (FP1/2/3, Roads)
  4. None -> dark material

Also applies Coord0_scaleoffset (uv' = uv*scale + offset) when non-identity,
keeps v2 geometry fixes (water z-shift, MAX_EXTENT, tiers).

Viewer contract: material.name == texture stem; viewer maps it to
models/tex/<name>.jpg with flipY=false (game samples PVR top-down).
"""
import argparse
import json
import os
import re
import struct
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bdae_extract import parse_meshes  # noqa: E402
from tex_bind import find_png, edge_map  # noqa: E402

RAW = "/home/z/my-project/download/TDKR_assets/raw"
PNG = "/home/z/my-project/download/TDKR_assets/textures_png"
SITE = "/home/z/my-project/work/ghpages_site"
MODELS = os.path.join(SITE, "models")
TEXD = os.path.join(MODELS, "tex")
GT_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ground_truth_city.json")

SKIP_FILES = {"GC_Irradiance_Volume", "GC_Refl_Test",
              "GC_Island1_ReflOccluder", "GC_Island2_ReflOccluder",
              "GothamCity_Map", "GC_Props_Monorail", "GC_CityBG",
              "GC_bridge_1_LongDist"}

MAX_EXTENT = 2500
WATER_FILES = {"GC_water", "GC_Water_Island2"}
WATER_Z_SHIFT = 160

# v7: exact per-object bake-page bindings extracted from the zone bake-group
# streams (extraction/re/extract_bake_regions.py -> bake_regions.json).
# CComponentBeastBakeGroup payloads: {page.tga, rect[u0 v0 u1 v1],
# atlasLow.tga, ...} + mesh component {bdae, 4 bools}. These are the game's
# OWN bake assignments — authoritative, no UV-fit guessing.
BAKE_REGIONS_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 os.pardir, "re", "bake_regions_v3.json")

# v8: code-verified record frame (session 6). CComponentBeastObjectComponent::
# Load (@0x2e1e8c) reads {vec4 so1, string page, vec4 so2}; the runtime
# CBeastObjectComponent::Load (@0x2a1ea4) then binds getTexture(page) into the
# material 'LightMap' slot and copies so1 into Coord1_scaleoffset. Vertex
# shader (LightMapDC-v.glsl):
#     vCoord1 = (Coord1*Coord1_scaleoffset.xy + Coord1_scaleoffset.zw)
#               * LightMapAtlas.xy + LightMapAtlas.zw
# => pageUV = uv * so1.xy + so1.zw  (so1 = scaleU, scaleV, offU, offV;
#    scaleU==scaleV: Beast tiles are square). The v1 "rect" was the discarded
#    so2 (low/-0 path) misread as (u0,v0,u1,v1) — the u0==v0 pattern was
#    simply square tiles. GF/VPOW's v7 UV-fit pages were wrong; now exact.

HERO_TEX = {"GC_Island1_LongDist_Low", "GC_Island2_LongDist_low",
            "GC_LongDist_Island2_Roads", "BakeGroup_Island1_Roads0",
            "GC_LongDist_Island1_FP1", "GC_LongDist_Island1_FP2",
            "GC_LongDist_Island1_FP3", "GC_LongDist_Island2_FP1",
            "GC_LongDist_Island2_FP2", "GC_LongDist_Island2_FP3",
            "GC_LongDist_Island1_Roads"}

# v7: REMOVED — the DIM_TEX ground-plane dimming (asphalt/sand/road/water at
# 0.42/0.55) contradicted the shipped shaders. GC_City_Plane (the ground) uses
# StandardDiffuseDC: Color = Diffuse * vColor with vColor = white (no vertex
# color stream in the 20B stride). The LightMapDC path multiplies by
# LightMap*2.0 where LightMap = shipped LightMapSampler.tga — a FLAT 0.4706
# gray (32x32, decoded from commons_tex) — net 0.941. Both render the ground
# at native diffuse brightness. The v4 dim was pre-grade (fog+LUT) tuning
# fudge and made the ground 2.4x too dark.
DIM_TEX = {}

BAD_FIT = re.compile(r"(nrm|lightmap|sampler|shadow|bump|spec|gloss|opacity|height"
                     r"|normal|refl|rfl|font|emissive|corona|_mask)", re.I)
BAKE_TARGET = re.compile(r"(LongDist|CompleteMap)", re.I)

# ground-truth textures absent from shipped data (runtime bakes) -> best
# on-disk equivalent for the viewer
MISSING_TEX_FALLBACK = {
    "GC_road_plane": "GothamCity_asphalt_tile",     # city ground plane
    "GC_Bigbridge_3_LongDist": "bridge_tile",       # bridge islands bake
}


def classify(name):
    n = name.lower()
    if "collision" in n or name in SKIP_FILES:
        return "skip"
    if n.endswith("low"):
        return "low"
    if "bigbridge" in n or "roads" in n:
        return "hero"
    if "longdist" in n and ("island1" in n or "island2" in n):
        return "hero"
    if re.search(r"fp\d", n) or "footprint" in n:
        return "fp"
    return "district"


def fp_island(name):
    n = name.lower()
    return "island1" if "island1" in n or "_1_" in n else "island2"


ISLAND_BAKES = {
    "island1": ["GC_LongDist_Island1_FP1", "GC_LongDist_Island1_FP2",
                "GC_LongDist_Island1_FP3", "GC_LongDist_Island1_Roads",
                "GC_Island1_LongDist_Low",
                "BakeGroup_Island1_A0", "BakeGroup_Island1_B0",
                "BakeGroup_Island1_Roads0", "BakeGroup_Island1_Landmarks0",
                "BakeGroup_Island1_ATLAS_low0"],
    "island2": ["GC_LongDist_Island2_FP1", "GC_LongDist_Island2_FP2",
                "GC_LongDist_Island2_FP3", "GC_LongDist_Island2_Roads",
                "GC_Island2_LongDist_low",
                "BakeGroup_Island2_A0", "BakeGroup_Island2_B0",
                "BakeGroup_Island2_Roads0", "BakeGroup_Island2_Landmarks0",
                "BakeGroup_Island2_ATLAS_low0"],
}


def jpg_from_png(png_path, out_path, max_dim, quality, dim=1.0):
    from PIL import Image, ImageEnhance
    im = Image.open(png_path).convert("RGB")
    if max(im.size) > max_dim:
        im.thumbnail((max_dim, max_dim), Image.LANCZOS)
    if dim != 1.0:
        im = ImageEnhance.Brightness(im).enhance(dim)
    im.save(out_path, "JPEG", quality=quality, optimize=True)
    return os.path.getsize(out_path)


def load_bake_groups():
    """base mesh bdae stem -> {page, so} from the zone bake-group streams (v2
    frame: so1 = Coord1_scaleoffset for the page the component binds via
    getTexture). Only records whose page ships on disk yield a binding."""
    try:
        rows = json.load(open(BAKE_REGIONS_JSON))
    except Exception:
        return {}
    out = {}
    for r in rows:
        mesh = r.get("mesh") or ""
        page = (r.get("page") or "").replace(".tga", "")
        so1 = r.get("so1")
        if mesh and page and so1 and find_png(page):
            out.setdefault(mesh, dict(page=page, so=so1))
    return out


def apply_bake_so(mesh, so):
    """Rect-relative UV refinement (engine parity): uv' = uv*scale + offset.
    so = (scaleU, scaleV, offU, offV) — the component's Coord1_scaleoffset."""
    su, sv, ou, ov = so
    if not all(np.isfinite([su, sv, ou, ov])) or su <= 0 or sv <= 0:
        return
    uv = mesh["uv"]
    mesh["uv"] = np.column_stack([uv[:, 0] * su + ou,
                                  uv[:, 1] * sv + ov]).astype(np.float32)


# ---- v9: Coord1 channel selection (session 7) ------------------------------
# The engine's LightMapDC shader samples the bake page with vCoord1 =
# Coord1*so1.xy + so1.zw.  The fp LongDist meshes store Coord1 in the FIRST
# vertex dword (+12, u16 x2) — NOT in the +16 stream (that is Coord0, the
# runtime complete-map UV; for 16B meshes +16 would read the NEXT vertex's
# position bytes).  Landmark bake targets (VPOW...) store a normal at +12 and
# derive Coord1 at runtime as a top-down planar projection of position.
# Both candidates are content-scored against the assigned page tile (Sobel
# edge density inside the rasterized UV mask vs a uniform-fill control).

_page_edge_cache = {}

def _page_edges(page):
    if page in _page_edge_cache:
        return _page_edge_cache[page]
    from PIL import Image
    p = find_png(page)
    if p is None:
        _page_edge_cache[page] = None
        return None
    im = Image.open(p).convert("L")
    im.thumbnail((1024, 1024), Image.BILINEAR)
    a = np.asarray(im, np.float32) / 255.0
    gx = np.zeros_like(a); gy = np.zeros_like(a)
    gx[:, 1:-1] = a[:, 2:] - a[:, :-2]
    gy[1:-1, :] = a[2:, :] - a[:-2, :]
    e = np.hypot(gx, gy)
    _page_edge_cache[page] = (e, a.shape)
    return _page_edge_cache[page]

def _uv_score(page, so, uv, idx):
    """edge density inside the so-transformed UV mask / page mean."""
    pe = _page_edges(page)
    if pe is None or uv is None or len(idx) < 9:
        return -1.0
    e, (h, w) = pe
    su, sv, ou, ov = so
    t = np.column_stack([uv[:, 0] * su + ou, uv[:, 1] * sv + ov])
    u = np.clip(t[:, 0] * (w - 1), 0, w - 1).astype(np.int32)
    # v10: page rows are top-down; game v is bottom-origin — flip the row index
    # so scoring samples the TRUE tile (was validating at the mirrored tile).
    v = (h - 1) - np.clip(t[:, 1] * (h - 1), 0, h - 1).astype(np.int32)
    s = e[v, u]
    if len(s) > 40000:
        s = s[:: len(s) // 40000]
    return float(s.mean() / (e.mean() + 1e-9))

def bake_coord1(mesh, page, so, floor=0.3):
    """v11 ENGINE PARITY: the LightMap slot samples vCoord1 = Coord1*so1 on the
    record's page — the engine multiplies Diffuse * LightMap * 2 (LightMapDC
    GLSL).  The record (page+so1) is authoritative; the content score only
    CHOOSES the Coord1 source (stored +12 stream vs top-down projection).
    Returns (uv1_page_space, source) or (None, None); mesh['uv'] (Coord0 for
    the DiffuseMap) is NEVER touched."""
    su, sv, ou, ov = so
    if not all(np.isfinite([su, sv, ou, ov])) or su <= 0.001 or sv <= 0.001:
        return None, None
    idx = mesh["idx"]
    pe = _page_edges(page)
    if pe is None:
        return None, None
    e, (h, w) = pe
    # control: edge density of a uniform tile fill
    u0 = int(ou * (w - 1))
    u1 = min(w - 1, u0 + int(su * (w - 1)))
    # v10: control rect in flipped (top-down row) space to match _uv_score
    rv0 = (h - 1) - int((ov + sv) * (h - 1))
    rv1 = (h - 1) - int(ov * (h - 1))
    rv0, rv1 = max(0, min(rv0, rv1)), min(h - 1, max(rv0, rv1))
    fill = float(e[rv0:rv1, u0:u1].mean() / (e.mean() + 1e-9))
    cands = []
    if mesh.get("uvm") is not None:
        cands.append(("uvm", mesh["uvm"]))
    pos = mesh["pos"]
    mn, mx = mesh["mn"], mesh["mx"]
    proj = np.column_stack([(pos[:, 0] - mn[0]) / (mx[0] - mn[0] + 1e-6),
                            (pos[:, 1] - mn[1]) / (mx[1] - mn[1] + 1e-6)]).astype(np.float32)
    cands.append(("proj", proj))
    best, best_uv, best_s = None, None, -1.0
    for name, uv in cands:
        s = _uv_score(page, so, uv, idx)
        if s > best_s:
            best, best_uv, best_s = name, uv, s
    # v11: score picks the SOURCE only — the binding itself comes from the
    # record.  The low floor rejects only degenerate candidates (NaN/empty).
    if best is None or best_s < floor:
        return None, None
    t = np.column_stack([best_uv[:, 0] * su + ou,
                         best_uv[:, 1] * sv + ov]).astype(np.float32)
    mesh["bake_channel"] = best
    return t, best


def uv_fit(uv, name):
    """edge-magnitude ratio score: >1 = samples detail-rich regions"""
    em = edge_map(name)
    if em is None:
        return -1.0
    e, (h, w) = em
    u = np.clip(uv[:, 0] * (w - 1), 0, w - 1).astype(np.int32)
    v = (h - 1) - np.clip(uv[:, 1] * (h - 1), 0, h - 1).astype(np.int32)
    s = e[v, u]
    if len(s) > 20000:
        s = s[:: len(s) // 20000]
    return float(s.mean())


def apply_scaleoffset(mesh, so):
    """Coord0_scaleoffset stored as (offU, offV, scaleU, scaleV); identity (0,0,1,1)"""
    if not so or len(so) != 4 or mesh.get("uv") is None:
        return
    ou, ov, su, sv = so
    if su <= 0 or sv <= 0:          # degenerate/none
        return
    if abs(ou) < 1e-6 and abs(ov) < 1e-6 and abs(su - 1) < 1e-6 and abs(sv - 1) < 1e-6:
        return                       # identity
    uv = mesh["uv"]
    mesh["uv"] = np.column_stack([(uv[:, 0] * su + ou) % 1.0,
                                  (uv[:, 1] * sv + ov) % 1.0]).astype(np.float32)


class GlbBuilder:
    """Geometry-only GLB: one node per file, one primitive per source mesh,
    per-primitive materials named after their texture."""

    def __init__(self):
        self.buf = bytearray()
        self.offset = 0
        self.views, self.accessors, self.meshes, self.nodes, self.materials = [], [], [], [], []
        self._mat_by_tex = {}
        self._uv1_count = 0

    def _add(self, data, align=4):
        pad = (-len(self.buf)) % align
        self.buf.extend(b"\0" * pad)
        self.offset += pad
        start = self.offset
        self.buf.extend(data)
        self.offset += len(data)
        return start, len(data)

    def material_for(self, tex, mode="d", lm=None):
        # v11 contract: '<dif>|<lm>|<mode>' when a LightMap is bound, else
        # '<tex>|<mode>' (unchanged from v4 for viewer back-compat).
        name = f"{tex}|{lm}|{mode}" if (tex and lm) else (
            f"{lm}|2x" if (lm and not tex) else
            (f"{tex}|{mode}" if tex else "__dark"))
        key = name
        if key in self._mat_by_tex:
            return self._mat_by_tex[key]
        if tex is None and lm is None:
            mat = dict(name="__dark", doubleSided=True,
                       pbrMetallicRoughness=dict(baseColorFactor=[0.055, 0.07, 0.10, 1.0],
                                                 metallicFactor=0.0, roughnessFactor=1.0))
        else:
            mat = dict(name=name, doubleSided=True,
                       pbrMetallicRoughness=dict(baseColorFactor=[1.0, 1.0, 1.0, 1.0],
                                                 metallicFactor=0.0, roughnessFactor=1.0))
        self.materials.append(mat)
        mid = len(self.materials) - 1
        self._mat_by_tex[key] = mid
        return mid

    def add_file(self, name, mesh_list, per_mesh_tex, yup=True):
        prims = []
        for m, bind in zip(mesh_list, per_mesh_tex):
            if isinstance(bind, tuple) and len(bind) == 3:
                tex, lm, mode = bind
            else:
                tex, mode = bind if isinstance(bind, tuple) else (bind, "d")
                lm = None
            if yup:
                pos = m["pos"][:, [0, 2, 1]].copy()
                pos[:, 2] = -m["pos"][:, 1]
                nrm = m["nrm"][:, [0, 2, 1]].copy()
                nrm[:, 2] = -m["nrm"][:, 1]
            else:
                pos, nrm = m["pos"], m["nrm"]
            pos = np.ascontiguousarray(pos, np.float32)
            nrm = np.ascontiguousarray(nrm, np.float32)
            if m.get("uv") is not None:
                # v10 V-CONVENTION FIX: game GLES UVs are bottom-origin (v=0 =
                # bottom row of the decoded page — proven by the FP1 full-page
                # raster + plaza probe: coherent atlas only under v-bottom).
                # glTF/three.js flipY=false sample v=0 at the TOP row, so the
                # deployed viewer has been sampling every page VERTICALLY
                # MIRRORED (symmetric content looked plausible; asymmetric
                # bake pages showed other tiles' content = "wrong textures").
                # Flip V once here — the single choke point for TEXCOORD_0/1.
                uv = np.asarray(m["uv"], np.float32).copy()
                uv[:, 1] = 1.0 - uv[:, 1]
                uv = np.ascontiguousarray(uv)
            else:
                uv = np.ascontiguousarray(np.zeros((m["count"], 2), np.float32))
            uv1 = None
            if lm and m.get("uv1") is not None:
                uv1 = np.asarray(m["uv1"], np.float32).copy()
                uv1[:, 1] = 1.0 - uv1[:, 1]
                uv1 = np.ascontiguousarray(uv1)
            idx = np.ascontiguousarray(m["idx"], np.uint32)
            sp, lp = self._add(pos.tobytes())
            sn, ln = self._add(nrm.tobytes())
            su, lu = self._add(uv.tobytes())
            si, li = self._add(idx.tobytes())
            s1 = l1 = None
            if uv1 is not None:
                s1, l1 = self._add(uv1.tobytes())
            base = len(self.views)
            self.views += [dict(buffer=0, byteOffset=sp, byteLength=lp),
                           dict(buffer=0, byteOffset=sn, byteLength=ln),
                           dict(buffer=0, byteOffset=su, byteLength=lu),
                           dict(buffer=0, byteOffset=si, byteLength=li)]
            if s1 is not None:
                self.views += [dict(buffer=0, byteOffset=s1, byteLength=l1)]
            mn, mx = pos.min(0), pos.max(0)
            a = self.accessors
            a.append(dict(bufferView=base, componentType=5126, count=len(pos), type="VEC3",
                          min=[float(v) for v in mn], max=[float(v) for v in mx]))
            a.append(dict(bufferView=base + 1, componentType=5126, count=len(nrm), type="VEC3"))
            a.append(dict(bufferView=base + 2, componentType=5126, count=len(uv), type="VEC2"))
            a.append(dict(bufferView=base + 3, componentType=5125, count=len(idx), type="SCALAR"))
            attrs = dict(POSITION=len(a) - 4, NORMAL=len(a) - 3,
                         TEXCOORD_0=len(a) - 2)
            if uv1 is not None:
                a.append(dict(bufferView=base + 4, componentType=5126, count=len(uv1), type="VEC2"))
                attrs["TEXCOORD_1"] = len(a) - 1
                self._uv1_count += 1
            prims.append(dict(attributes=attrs,
                              indices=len(a) - 1, material=self.material_for(tex, mode, lm), mode=4))
        mi = len(self.meshes)
        self.meshes.append(dict(name=name, primitives=prims))
        self.nodes.append(dict(mesh=mi, name=name))

    def write(self, out_path):
        pad = (-len(self.buf)) % 4
        self.buf.extend(b"\0" * pad)
        gltf = dict(
            asset=dict(version="2.0", generator="tdkr-export-city-v3"),
            scene=0, scenes=[dict(nodes=list(range(len(self.nodes))))],
            nodes=self.nodes, meshes=self.meshes, materials=self.materials,
            accessors=self.accessors, bufferViews=self.views,
            buffers=[dict(byteLength=len(self.buf))])
        js = json.dumps(gltf, separators=(",", ":")).encode()
        js += b" " * ((-len(js)) % 4)
        total = 12 + 8 + len(js) + 8 + len(self.buf)
        with open(out_path, "wb") as fo:
            fo.write(struct.pack("<III", 0x46546C67, 2, total))
            fo.write(struct.pack("<II", len(js), 0x4E4F534A))
            fo.write(js)
            fo.write(struct.pack("<II", len(self.buf), 0x004E4942))
            fo.write(self.buf)
        return os.path.getsize(out_path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--max-glb-mb", type=float, default=4.0)
    args = ap.parse_args()

    gt = json.load(open(GT_JSON))
    bake_groups = load_bake_groups()
    if bake_groups:
        print(f"bake-group exact page bindings: {len(bake_groups)} meshes")
    city_dir = os.path.join(RAW, "l_gothamcity")
    files = sorted(f for f in os.listdir(city_dir) if f.endswith(".bdae"))
    entries = []
    gt_stats = dict(gt_bind=0, alpha_fix=0, pool_fit=0, bake_fit=0, dark=0, fp_family=0)
    print(f"scanning {len(files)} city bdae files ...")
    for fn in files:
        base = fn[:-len(".bdae")]
        cat = classify(base)
        if cat == "skip":
            continue
        p = os.path.join(city_dir, fn)
        try:
            meshes = parse_meshes(p, verbose=False)
        except Exception:
            meshes = []
        if not meshes:
            continue
        if base in WATER_FILES:
            for m in meshes:
                m["pos"] = m["pos"] - np.array([0, 0, WATER_Z_SHIFT], np.float32)
                m["mn"], m["mx"] = m["pos"].min(0), m["pos"].max(0)
        elif max((m["mx"] - m["mn"]).max() for m in meshes) > MAX_EXTENT:
            print(f"  skip (out-of-world extent): {base}")
            continue

        g = gt.get(base, {})
        gt_meshes = {m["offset"]: m for m in g.get("meshes", [])}
        file_texlist = [t for t in g.get("textures", [])]
        gt_names = {m.get("diffuse") for m in g.get("meshes", [])}
        allow_water = any(t and "water" in t.lower() for t in gt_names)
        pool_avail = [t for t in file_texlist
                      if find_png(t) and not BAD_FIT.search(t)
                      and (allow_water or t.lower() != "water")]
        bake_fam = (ISLAND_BAKES[fp_island(base)]
                    if cat == "fp" or any(t and BAKE_TARGET.search(t) for t in gt_names)
                    else [])

        per_mesh = []
        gt_stats = gt_stats  # noqa
        for m in meshes:
            gm = gt_meshes.get(m["offset"], {})
            so = gm.get("scaleoffset")
            apply_scaleoffset(m, so)   # engine's own UV transform (Coord0)
            tex = gm.get("diffuse")
            tech = gm.get("technique") or ""
            # v10.1: honor the engine's own blend technique — SimpleAdditive
            # meshes (glow planes, coronas, diner logos, volumetrics) rendered
            # opaque = giant white wedges over the city.
            if "additive" in tech.lower():
                mode = "add"
            else:
                mode = "2x" if "LightMapDC" in tech else "d"
            how = "gt"

            # v11: resolve the object's Beast bake record (the game's OWN
            # LightMap binding: page + Coord1_scaleoffset).  Applies to
            # _LongDist render units of the same object.  uv0 (DiffuseMap
            # Coord0) is untouched; uv1 = Coord1*so1 (page space).
            is_ld = base.lower().endswith("_longdist")
            bg = None
            if base.lower() in bake_groups:
                bg = bake_groups[base.lower()]
            elif is_ld:
                stripped = re.sub(r"_longdist$", "", base.lower())
                if stripped in bake_groups:
                    bg = bake_groups[stripped]
            lm = None
            if bg:
                uv1, src = bake_coord1(m, bg["page"], bg["so"])
                if uv1 is not None:
                    m["uv1"] = uv1
                    lm = bg["page"]

            # v9: st=16 meshes (uv=None: pos + ONE dword at +12) — the +12
            # stream is the mesh's only UV candidate.  It feeds BOTH Coord0
            # (DiffuseMap) and Coord1 (LightMap, via so1) in the engine.
            had_uv = m.get("uv") is not None
            if m.get("uv") is None:
                m["uv"] = m.get("uvm")

            # ---------------- fp tier: engine-faithful ladder ----------------
            if cat == "fp":
                dif = tex
                # v4 fix: some texIdx slots resolve to SAMPLER-name strings
                # (runtime atlases) — not shipped textures -> drop to None.
                if dif and (dif.endswith("Sampler") or dif.endswith("sampler")):
                    dif = None
                fp_tex, fp_lm, fp_mode, fp_how = None, None, ("add" if "additive" in tech.lower() else "2x"), "dark"
                if dif and dif.lower() == "gc_longdist":
                    # runtime island bake as the DIFFUSE slot (page not shipped).
                    # v11: render the best-fit island page x2 (no lm multiply —
                    # the record page IS this family; double multiply would
                    # double-darken the approximation).
                    pages = ["GC_LongDist_Island1_FP1", "GC_LongDist_Island1_FP2",
                             "GC_LongDist_Island1_FP3", "GC_LongDist_Island1_Roads",
                             "GC_LongDist_Island2_FP1", "GC_LongDist_Island2_FP2",
                             "GC_LongDist_Island2_FP3", "GC_LongDist_Island2_Roads"]
                    if m["uv"] is None:
                        scored = []
                    else:
                        scored = sorted(((uv_fit(m["uv"], t), t) for t in pages), reverse=True)
                    if scored and scored[0][0] >= 0.9:
                        fp_tex, fp_how = scored[0][1], "fp-page-fit"
                        fp_mode = "2x"
                elif dif:
                    base2 = re.sub(
                        r"_(longdist(completemap|diffusemap|diffuse_map)?|longdistdiffusemap|longdist)$",
                        "", dif, flags=re.I)
                    if find_png(base2):
                        fp_tex, fp_how = base2, "gt"
                    else:
                        alt = MISSING_TEX_FALLBACK.get(dif) or re.sub(r"_alpha$", "", dif, flags=re.I)
                        if find_png(alt):
                            fp_tex, fp_how = alt, "alpha-fix"
                        else:
                            fam = [t for t in file_texlist
                                   if t.lower().startswith(base2.lower())
                                   and not BAD_FIT.search(t) and find_png(t)]
                            if fam:
                                fam.sort(key=len)
                                fp_tex, fp_how = fam[0], "fp-family"
                # v11: engine parity — Diffuse * LightMap * 2.  When the
                # offline bake (dif) exists AND the Beast record page exists,
                # BOTH bind.  Without dif, the lm page renders alone (x2).
                if fp_tex is None and lm is not None:
                    fp_tex, fp_lm, fp_how = lm, None, "bakegroup"
                elif lm is not None:
                    fp_lm = lm
                    fp_how = fp_how + "+lm" if fp_how != "dark" else "bakegroup"
                per_mesh.append((fp_tex, fp_lm, fp_mode))
                gt_stats[{"gt": "gt_bind", "gt+lm": "gt_bind", "fp-family": "fp_family",
                          "fp-page-fit": "bake_fit", "bakegroup": "bake_fit",
                          "alpha-fix": "alpha_fix",
                          "dark": "dark"}.get(fp_how, "dark")] += 1
                continue

            # v4 fix: SAMPLER-name texIdx slots for non-fp files too.
            if tex and (tex.endswith("Sampler") or tex.endswith("sampler")):
                tex = None
            how = "gt"
            if tex and not find_png(tex):
                alt = MISSING_TEX_FALLBACK.get(tex)
                if alt is None:
                    alt = re.sub(r"_alpha$", "", tex, flags=re.I)
                if find_png(alt):
                    tex, how = alt, "alpha-fix"
                elif len(pool_avail) == 1:
                    tex, how = pool_avail[0], "pool-single"
                elif pool_avail and m["uv"] is not None:
                    scored = sorted(((uv_fit(m["uv"], t), t) for t in pool_avail), reverse=True)
                    if scored and scored[0][0] >= 0.9:
                        tex, how = scored[0][1], "pool-fit"
                    else:
                        tex, how = None, "dark"
                else:
                    tex, how = None, "dark"
            if tex is None and bake_fam and m["uv"] is not None:
                scored = sorted(((uv_fit(m["uv"], t), t) for t in bake_fam), reverse=True)
                if scored and scored[0][0] >= 2.2:
                    tex, how = scored[0][1], "bake-fit"
            # v11: attach the Beast LightMap when the object has a record —
            # engine renders dif * lm * 2 (LightMapDC).
            out_lm = lm if tex else None
            if lm and not tex:
                tex, how, out_lm = lm, "bakegroup", None
            gt_stats[{"gt": "gt_bind", "alpha-fix": "alpha_fix", "pool-single": "pool_fit",
                      "pool-fit": "pool_fit", "bake-fit": "bake_fit",
                      "bakegroup": "bake_fit",
                      "dark": "dark"}.get(how, "dark")] += 1
            per_mesh.append((tex, out_lm, mode))

        verts = int(sum(m["count"] for m in meshes))
        tris = int(sum(m["numIdx"] // 3 for m in meshes))
        gbytes = verts * 32 + tris * 12 + sum(len(m['uv1']) * 8 for m in meshes if m.get('uv1') is not None)
        texs = sorted({t for b in per_mesh for t in ([b[0]] if len(b) == 2 else [b[0], b[1]]) if t})
        entries.append(dict(base=base, cat=cat, texs=texs, per_mesh=per_mesh,
                            verts=verts, tris=tris, nmesh=len(meshes),
                            gbytes=gbytes, path=p, meshes=meshes))

    from collections import Counter
    c = Counter(e["cat"] for e in entries)
    tv = sum(e["verts"] for e in entries)
    tt = sum(e["tris"] for e in entries)
    textured = sum(1 for e in entries if e["texs"])
    lm_count = sum(1 for e in entries for b in e["per_mesh"] if len(b) == 3 and b[1])
    print(f"parsed: {len(entries)} files | {tv:,} verts {tt:,} tris | "
          f"{textured} files with textures | "
          f"{len({t for e in entries for t in e['texs']})} unique textures")
    print(f"binding method: {gt_stats} | lightmap-bound meshes: {lm_count}")
    for k, v in sorted(c.items()):
        sub = [e for e in entries if e["cat"] == k]
        print(f"  {k:<9} {v:>4} files  {sum(e['verts'] for e in sub):>9,}v "
              f"{sum(e['tris'] for e in sub):>8,}t  texless={sum(1 for e in sub if not e['texs'])}")
    if args.dry:
        for e in entries:
            print(f"  [{e['cat']:<8}] {e['base']:<52} {e['verts']:>7}v {e['tris']:>7}t "
                  f"tex={','.join(e['texs'][:3]) or '-'}"
                  f"{'…' if len(e['texs']) > 3 else ''}")
        return

    # ---------------- pack tiers into GLBs ----------------
    os.makedirs(MODELS, exist_ok=True)
    os.makedirs(TEXD, exist_ok=True)
    plan = []
    for e in [x for x in entries if x["cat"] == "hero"]:
        plan.append((e["base"], [e]))
    for isl in ("island1", "island2"):
        sub = [x for x in entries if x["cat"] == "fp" and fp_island(x["base"]) == isl]
        if sub:
            plan.append((f"fp_{isl}", sub))
    low = [x for x in entries if x["cat"] == "low"]
    if low:
        plan.append(("city_low", low))
    dist = [x for x in entries if x["cat"] == "district"]
    cap = int(args.max_glb_mb * 1024 * 1024)
    cur, cur_b = [], 0
    bins = []
    for e in sorted(dist, key=lambda x: -x["gbytes"]):
        if cur and cur_b + e["gbytes"] > cap:
            bins.append(cur)
            cur, cur_b = [], 0
        cur.append(e)
        cur_b += e["gbytes"]
    if cur:
        bins.append(cur)
    for i, b in enumerate(bins):
        plan.append((f"district_{i:02d}", b))

    manifest = dict(tiers={}, glbs=[], total_verts=tv, total_tris=tt, version=11)
    # v11: PRESERVE the street tier (exported separately by export_zone.py) —
    # the manifest is shared state; dropping it orphans the streamed city.
    _mprev = os.path.join(MODELS, "manifest.json")
    if os.path.exists(_mprev):
        try:
            _prev = json.load(open(_mprev))
            _street = [g for g in _prev.get("glbs", []) if g.get("tier") == "street"]
            if _street:
                manifest["glbs"].extend(_street)
                print(f"preserved street tier: {len(_street)} GLBs")
        except Exception:
            pass
    tex_used = {}
    for glb_name, group in plan:
        gb = GlbBuilder()
        for e in group:
            gb.add_file(e["base"], e["meshes"], e["per_mesh"])
        glb_file = glb_name + ".glb"
        size = gb.write(os.path.join(MODELS, glb_file))
        manifest["glbs"].append(dict(
            file="models/" + glb_file, bytes=size,
            verts=sum(e["verts"] for e in group), tris=sum(e["tris"] for e in group),
            tier=group[0]["cat"] if len({e["cat"] for e in group}) == 1 else "district",
            files=[dict(name=e["base"], texs=e["texs"], verts=e["verts"], tris=e["tris"],
                        meshes=e["nmesh"]) for e in group]))
        for e in group:
            for t in e["texs"]:
                tex_used[t] = max(tex_used.get(t, 0), e["gbytes"])
        print(f"  + {glb_file:<28} {size/1024:>7.0f} KB  {len(group)} files  "
              f"{sum(e['tris'] for e in group):>7,} tris")

    # ---------------- textures -> external JPEG ----------------
    # v4: DIM_TEX applies ONLY when every usage is diffuse-mode ('d'); textures
    # rendered through the LightMapDC x2.0 overbright path keep native levels.
    tex_modes = {}
    for glb_name, group in plan:
        for e in group:
            for b in e["per_mesh"]:
                if len(b) == 3:
                    tex, lm, mode = b
                else:
                    tex, mode = b
                    lm = None
                for t in (tex, lm):
                    if t:
                        tex_modes.setdefault(t, set()).add(mode)
    for tex in sorted(tex_used):
        src = find_png(tex)
        if not src:
            print(f"  !! texture missing on disk: {tex}")
            continue
        # v10/v11 QUALITY: every bake/atlas page ships at FULL 2048 source res;
        # v11: fp/district diffuse pages too (albedo atlases now visible —
        # they must not be the blurry 1024 q78 of the v5 era).
        hero = (tex in HERO_TEX or tex.lower().startswith("bakegroup_")
                or tex.lower().startswith("gc_footprint"))
        n = tex + ".jpg"
        dim = DIM_TEX.get(tex, 1.0) if tex_modes.get(tex, {"d"}) <= {"d"} else 1.0
        sz = jpg_from_png(src, os.path.join(TEXD, n), 2048 if hero else 1024,
                          88 if hero else 85, dim=dim)
        print(f"  tex {n:<48} {sz/1024:>6.0f} KB{' (hero 2048 q88)' if hero else ''}")

    # ---------------- batarang showcase (self-contained) ----------------
    bat = os.path.join(RAW, "actors", "Batarang.bdae.bin")
    if os.path.exists(bat):
        from bdae_extract import write_glb
        meshes = parse_meshes(bat, verbose=False)
        if meshes:
            write_glb(meshes, os.path.join(PNG, "actors_tex", "Batarang.png"),
                      os.path.join(MODELS, "batarang.glb"), "batarang")
            print(f"  + batarang.glb  {os.path.getsize(os.path.join(MODELS, 'batarang.glb'))//1024} KB (embedded tex)")

    for t in manifest["glbs"]:
        manifest["tiers"].setdefault(t["tier"], []).append(t["file"])
    with open(os.path.join(MODELS, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    total = sum(t["bytes"] for t in manifest["glbs"])
    print(f"\nDONE: {len(manifest['glbs'])} GLBs, {total/1024/1024:.1f} MB geometry, "
          f"{len(tex_used)} external textures, {tv:,} verts / {tt:,} tris")


if __name__ == "__main__":
    main()
