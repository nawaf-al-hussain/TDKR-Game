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
SITE = "/home/z/my-project/work/TDKR-Game/gh-pages"
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
                                 os.pardir, "re", "bake_regions_v2.json")

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


def uv_fit(uv, name):
    """edge-magnitude ratio score: >1 = samples detail-rich regions"""
    em = edge_map(name)
    if em is None:
        return -1.0
    e, (h, w) = em
    u = np.clip(uv[:, 0] * (w - 1), 0, w - 1).astype(np.int32)
    v = np.clip(uv[:, 1] * (h - 1), 0, h - 1).astype(np.int32)
    s = e[v, u]
    if len(s) > 20000:
        s = s[:: len(s) // 20000]
    return float(s.mean())


def apply_scaleoffset(mesh, so):
    """Coord0_scaleoffset stored as (offU, offV, scaleU, scaleV); identity (0,0,1,1)"""
    if not so or len(so) != 4:
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

    def _add(self, data, align=4):
        pad = (-len(self.buf)) % align
        self.buf.extend(b"\0" * pad)
        self.offset += pad
        start = self.offset
        self.buf.extend(data)
        self.offset += len(data)
        return start, len(data)

    def material_for(self, tex, mode="d"):
        key = (tex, mode)
        if key in self._mat_by_tex:
            return self._mat_by_tex[key]
        if tex is None:
            mat = dict(name="__dark", doubleSided=True,
                       pbrMetallicRoughness=dict(baseColorFactor=[0.055, 0.07, 0.10, 1.0],
                                                 metallicFactor=0.0, roughnessFactor=1.0))
        else:
            # v4: shading mode rides in the material name -> viewer parses it
            mat = dict(name=f"{tex}|{mode}", doubleSided=True,
                       pbrMetallicRoughness=dict(baseColorFactor=[1.0, 1.0, 1.0, 1.0],
                                                 metallicFactor=0.0, roughnessFactor=1.0))
        self.materials.append(mat)
        mid = len(self.materials) - 1
        self._mat_by_tex[key] = mid
        return mid

    def add_file(self, name, mesh_list, per_mesh_tex, yup=True):
        prims = []
        for m, bind in zip(mesh_list, per_mesh_tex):
            tex, mode = bind if isinstance(bind, tuple) else (bind, "d")
            if yup:
                pos = m["pos"][:, [0, 2, 1]].copy()
                pos[:, 2] = -m["pos"][:, 1]
                nrm = m["nrm"][:, [0, 2, 1]].copy()
                nrm[:, 2] = -m["nrm"][:, 1]
            else:
                pos, nrm = m["pos"], m["nrm"]
            pos = np.ascontiguousarray(pos, np.float32)
            nrm = np.ascontiguousarray(nrm, np.float32)
            uv = np.ascontiguousarray(m["uv"], np.float32)
            idx = np.ascontiguousarray(m["idx"], np.uint32)
            sp, lp = self._add(pos.tobytes())
            sn, ln = self._add(nrm.tobytes())
            su, lu = self._add(uv.tobytes())
            si, li = self._add(idx.tobytes())
            base = len(self.views)
            self.views += [dict(buffer=0, byteOffset=sp, byteLength=lp),
                           dict(buffer=0, byteOffset=sn, byteLength=ln),
                           dict(buffer=0, byteOffset=su, byteLength=lu),
                           dict(buffer=0, byteOffset=si, byteLength=li)]
            mn, mx = pos.min(0), pos.max(0)
            a = self.accessors
            a.append(dict(bufferView=base, componentType=5126, count=len(pos), type="VEC3",
                          min=[float(v) for v in mn], max=[float(v) for v in mx]))
            a.append(dict(bufferView=base + 1, componentType=5126, count=len(nrm), type="VEC3"))
            a.append(dict(bufferView=base + 2, componentType=5126, count=len(uv), type="VEC2"))
            a.append(dict(bufferView=base + 3, componentType=5125, count=len(idx), type="SCALAR"))
            prims.append(dict(attributes=dict(POSITION=len(a) - 4, NORMAL=len(a) - 3,
                                              TEXCOORD_0=len(a) - 2),
                              indices=len(a) - 1, material=self.material_for(tex, mode), mode=4))
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
            apply_scaleoffset(m, so)   # engine's own UV transform
            tex = gm.get("diffuse")
            tech = gm.get("technique") or ""
            mode = "2x" if "LightMapDC" in tech else "d"
            how = "gt"

            # ---------------- fp tier: engine-faithful, name-driven ladder ----
            # Shipped per-footprint textures (GC_Footprint_AWT.tga etc.) are the
            # OFFLINE Beast bakes (complete maps: lit windows baked in, mean
            # ~0.28 vs island-page ~0.11). In-game they render through the
            # diffuse slot at 1x — the runtime LightMap slot is bound to the
            # same bake. x2 on them = daylight-bright (the v5 viewer bug).
            if cat == "fp":
                dif = tex
                fp_tex, fp_mode, fp_how = None, "d", "dark"
                # v8: the zone bake-group record (so1 + page1) is the game's OWN
                # binding for this object — applies to _LongDist render units of
                # the same object (the Beast component sets the 'LightMap' slot
                # + Coord1_scaleoffset on ALL of the object's materials).
                # Reflection/decal variants keep their own material bindings.
                is_ld = base.lower().endswith("_longdist")
                bg = None
                if is_ld:
                    stripped = re.sub(r"_longdist$", "", base.lower())
                    for nm in (base.lower(), stripped):
                        if nm in bake_groups:
                            bg = bake_groups[nm]
                            break
                if bg:
                    apply_bake_so(m, bg["so"])          # rect-relative refinement
                    fp_tex, fp_how = bg["page"], "bakegroup"
                    fp_mode = "2x"                       # bake pages authored for LM*2
                elif dif and not dif.lower().endswith("sampler"):
                    if dif.lower() == "gc_longdist":
                        # runtime island bake. v7: the zone bake-group streams
                        # give the EXACT page for many footprints (the game's
                        # own CComponentBeastBakeGroup assignment). Only the
                        # files with no shipped bake-group page fall back to
                        # UV-fit among the GC_LongDist island pages.
                        pages = ["GC_LongDist_Island1_FP1", "GC_LongDist_Island1_FP2",
                                 "GC_LongDist_Island1_FP3", "GC_LongDist_Island1_Roads",
                                 "GC_LongDist_Island2_FP1", "GC_LongDist_Island2_FP2",
                                 "GC_LongDist_Island2_FP3", "GC_LongDist_Island2_Roads"]
                        scored = sorted(((uv_fit(m["uv"], t), t) for t in pages), reverse=True)
                        if scored and scored[0][0] >= 0.9:
                            fp_tex, fp_how = scored[0][1], "fp-page-fit"  # page -> 2x (hero parity)
                            fp_mode = "2x"
                    else:
                        base2 = re.sub(
                            r"_(longdist(completemap|diffusemap|diffuse_map)?|longdistdiffusemap|longdist)$",
                            "", dif, flags=re.I)
                        if find_png(base2):
                            fp_tex, fp_how = base2, "gt"            # complete bake -> 1x
                        else:
                            fam = [t for t in file_texlist
                                   if t.lower().startswith(base2.lower())
                                   and not BAD_FIT.search(t) and find_png(t)]
                            if fam:
                                fam.sort(key=len)
                                fp_tex, fp_how = fam[0], "fp-family"  # same-footprint albedo family -> 1x
                per_mesh.append((fp_tex, fp_mode))
                gt_stats[{"gt": "gt_bind", "fp-family": "fp_family", "fp-page-fit": "bake_fit",
                          "bakegroup": "bake_fit", "dark": "dark"}.get(fp_how, "dark")] += 1
                continue

            # v4 fix: some texIdx slots resolve to SAMPLER-name strings
            # (e.g. Reflections-fx DiffuseMap -> 'LightMapSampler' runtime
            # atlas).  Those are not shipped textures -> unbind and let the
            # fallback ladder pick the island bake family instead.
            if tex and (tex.endswith("Sampler") or tex.endswith("sampler")):
                tex = None
            # v4 shading mode from the engine's own technique binding:
            #   LightMapDC with LightMap unbound -> bake * 2.0 (GLSL: *2.0)
            #   anything else (StandardDiffuseDC, ...) -> diffuse * 1.0
            how = "gt"
            if tex and not find_png(tex):
                alt = MISSING_TEX_FALLBACK.get(tex)
                if alt is None:
                    alt = re.sub(r"_alpha$", "", tex, flags=re.I)
                if find_png(alt):
                    tex, how = alt, "alpha-fix"
                elif len(pool_avail) == 1:
                    tex, how = pool_avail[0], "pool-single"
                elif pool_avail:
                    scored = sorted(((uv_fit(m["uv"], t), t) for t in pool_avail), reverse=True)
                    if scored and scored[0][0] >= 0.9:
                        tex, how = scored[0][1], "pool-fit"
                    else:
                        tex, how = None, "dark"
                else:
                    tex, how = None, "dark"
            if tex is None and bake_fam:
                # v4: bake-fit only on an EXTREMELY strong edge-match — a wrong
                # atlas-cell guess renders as an amplified garbage patch (x2),
                # far worse than the honest dark fallback.
                scored = sorted(((uv_fit(m["uv"], t), t) for t in bake_fam), reverse=True)
                if scored and scored[0][0] >= 2.2:
                    tex, how = scored[0][1], "bake-fit"
            gt_stats[{"gt": "gt_bind", "alpha-fix": "alpha_fix", "pool-single": "pool_fit",
                      "pool-fit": "pool_fit", "bake-fit": "bake_fit",
                      "dark": "dark"}.get(how, "dark")] += 1
            per_mesh.append((tex, mode))

        verts = int(sum(m["count"] for m in meshes))
        tris = int(sum(m["numIdx"] // 3 for m in meshes))
        gbytes = verts * 32 + tris * 12
        texs = sorted({t for t, _ in per_mesh if t})
        entries.append(dict(base=base, cat=cat, texs=texs, per_mesh=per_mesh,
                            verts=verts, tris=tris, nmesh=len(meshes),
                            gbytes=gbytes, path=p, meshes=meshes))

    from collections import Counter
    c = Counter(e["cat"] for e in entries)
    tv = sum(e["verts"] for e in entries)
    tt = sum(e["tris"] for e in entries)
    textured = sum(1 for e in entries if e["texs"])
    print(f"parsed: {len(entries)} files | {tv:,} verts {tt:,} tris | "
          f"{textured} files with textures | "
          f"{len({t for e in entries for t in e['texs']})} unique textures")
    print(f"binding method: {gt_stats}")
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

    manifest = dict(tiers={}, glbs=[], total_verts=tv, total_tris=tt, version=8)
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
            for tex, mode in e["per_mesh"]:
                if tex:
                    tex_modes.setdefault(tex, set()).add(mode)
    for tex in sorted(tex_used):
        src = find_png(tex)
        if not src:
            print(f"  !! texture missing on disk: {tex}")
            continue
        hero = tex in HERO_TEX
        n = tex + ".jpg"
        dim = DIM_TEX.get(tex, 1.0) if tex_modes.get(tex, {"d"}) <= {"d"} else 1.0
        sz = jpg_from_png(src, os.path.join(TEXD, n), 2048 if hero else 1024,
                          82 if hero else 78, dim=dim)
        print(f"  tex {n:<48} {sz/1024:>6.0f} KB{' (hero 2048)' if hero else ''}")

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
