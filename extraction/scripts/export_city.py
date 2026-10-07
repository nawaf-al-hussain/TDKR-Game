#!/usr/bin/env python3
"""Full-city LOD-aware GLB exporter v2 for the GitHub Pages viewer.

v2 fixes texture mapping (v1 bound one texture per FILE via filename token
overlap, collapsing dozens of props onto shared atlases). v2 binds textures
PER MESH using the game's own ground truth:

  0. uv-verified OVERRIDE table (island/bridge/roads bakes)
  1. footer material name <-> pool candidate (token containment)
  2. unique diffuse candidate in the file's string pool
  3. per-mesh UV-fit scoring among pool candidates
  4. bake-atlas family fallback for footprint/longdist files
  5. None -> neutral dark material

GLB layout: one node per FILE, one mesh with one PRIMITIVE per source mesh,
each primitive referencing a material NAMED after its texture (viewer maps
material.name -> models/tex/<name>.jpg).

Output: site/models/*.glb, site/models/tex/*.jpg, site/models/manifest.json
Usage: python3 export_city.py [--dry] [--max-glb-mb 4]
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
from tex_bind import diffuse_candidates, resolve_file, find_png  # noqa: E402

RAW = "/home/z/my-project/download/TDKR_assets/raw"
PNG = "/home/z/my-project/download/TDKR_assets/textures_png"
SITE = "/home/z/my-project/work/site"
MODELS = os.path.join(SITE, "models")
TEXD = os.path.join(MODELS, "tex")

OVERRIDE_TEX = {
    # uv-verified bindings (probe renders, previous session)
    "GC_island1_LongDist": "GC_Island1_LongDist_Low",
    "GC_Island2_LongDist": "GC_Island2_LongDist_low",
    "GC_LongDist_Island1_Roads": "BakeGroup_Island1_Roads0",
    "GC_Bigbridge": "bridge_1",
    "GC_Bigbridge_LongDist": "bridge_tile",
    "GC_Broken_BigBridge": "bridge_1",
    "GC_Broken_BigBridge_LongDist": "bridge_tile",
    "GC_Bigbridge_1_islands_LongDist": "bridge_tile",
    "GC_Bigbridge_2_islands_LongDist": "bridge_tile",
    "GC_Bigbridge_3_LongDist": "bridge_tile",
    "GC_Small_Bridge_Island2_LongDist": "bridge_tile",
    "GC_Monorail_Island1_LongDist": "GC_Residential_Props_Monorail",
    "GC_Monorail_Island2_LongDist": "GC_Residential_Props_Monorail",
    "GC_Railway_Island2_LongDist": "GC_Residential_Props_Railroad",
}

SKIP_FILES = {"GC_Irradiance_Volume", "GC_Refl_Test",
              "GC_Island1_ReflOccluder", "GC_Island2_ReflOccluder"}

# textures rendered at 2048 (city-wide bakes)
HERO_TEX = {"GC_Island1_LongDist_Low", "GC_Island2_LongDist_low",
            "GC_LongDist_Island2_Roads", "BakeGroup_Island1_Roads0",
            "GC_LongDist_Island1_FP1", "GC_LongDist_Island1_FP2",
            "GC_LongDist_Island1_FP3", "GC_LongDist_Island2_FP1",
            "GC_LongDist_Island2_FP2", "GC_LongDist_Island2_FP3",
            "GC_LongDist_Island1_Roads"}


def classify(name):
    n = name.lower()
    if "collision" in n or name in SKIP_FILES:
        return "skip"
    if n.endswith("_low") or n.endswith("low"):
        return "low"
    if "bigbridge" in n:
        return "hero"
    if "roads" in n:
        return "hero"
    if "longdist" in n and ("island1" in n or "island2" in n):
        return "hero"
    if "fp" in n and "longdist" in n or re.search(r"fp\d", n) or "footprint" in n:
        return "fp"
    return "district"


def fp_island(name):
    n = name.lower()
    return "island1" if "island1" in n or "_1_" in n else "island2"


def file_pool(path):
    """diffuse texture candidates referenced by the file's own string pool"""
    d = open(path, "rb").read()
    strs = [m.group().decode() for m in re.finditer(rb"[ -~]{4,}", d)]
    return sorted({s[:-4] for s in strs if s.endswith(".tga")})


def jpg_from_png(png_path, out_path, max_dim, quality):
    from PIL import Image
    im = Image.open(png_path).convert("RGB")
    if max(im.size) > max_dim:
        im.thumbnail((max_dim, max_dim), Image.LANCZOS)
    im.save(out_path, "JPEG", quality=quality, optimize=True)
    return os.path.getsize(out_path)


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

    def material_for(self, tex):
        """dedup materials by texture name; tex=None -> dark neutral"""
        if tex in self._mat_by_tex:
            return self._mat_by_tex[tex]
        if tex is None:
            mat = dict(name="__dark", doubleSided=True,
                       pbrMetallicRoughness=dict(baseColorFactor=[0.055, 0.07, 0.10, 1.0],
                                                 metallicFactor=0.0, roughnessFactor=1.0))
        else:
            mat = dict(name=tex, doubleSided=True,
                       pbrMetallicRoughness=dict(baseColorFactor=[1.0, 1.0, 1.0, 1.0],
                                                 metallicFactor=0.0, roughnessFactor=1.0))
        self.materials.append(mat)
        mid = len(self.materials) - 1
        self._mat_by_tex[tex] = mid
        return mid

    def add_file(self, name, mesh_list, per_mesh_tex, yup=True):
        prims = []
        for m, tex in zip(mesh_list, per_mesh_tex):
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
                              indices=len(a) - 1, material=self.material_for(tex), mode=4))
        mi = len(self.meshes)
        self.meshes.append(dict(name=name, primitives=prims))
        self.nodes.append(dict(mesh=mi, name=name))

    def write(self, out_path):
        pad = (-len(self.buf)) % 4
        self.buf.extend(b"\0" * pad)
        gltf = dict(
            asset=dict(version="2.0", generator="tdkr-export-city-v2"),
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

    city_dir = os.path.join(RAW, "l_gothamcity")
    files = sorted(f for f in os.listdir(city_dir) if f.endswith(".bdae.bin"))
    entries = []
    print(f"scanning {len(files)} city bdae files ...")
    for fn in files:
        base = fn[:-len(".bdae.bin")]
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
        pool = file_pool(p)
        if base in OVERRIDE_TEX and find_png(OVERRIDE_TEX[base]):
            per_mesh = [OVERRIDE_TEX[base]] * len(meshes)
        else:
            per_mesh = resolve_file(base, meshes, pool)
        verts = int(sum(m["count"] for m in meshes))
        tris = int(sum(m["numIdx"] // 3 for m in meshes))
        gbytes = verts * 32 + tris * 12
        texs = sorted({t for t in per_mesh if t})
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

    manifest = dict(tiers={}, glbs=[], total_verts=tv, total_tris=tt, version=2)
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
    for tex in sorted(tex_used):
        src = find_png(tex)
        if not src:
            print(f"  !! texture missing on disk: {tex}")
            continue
        hero = tex in HERO_TEX
        n = tex + ".jpg"
        sz = jpg_from_png(src, os.path.join(TEXD, n), 2048 if hero else 1024,
                          82 if hero else 78)
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
