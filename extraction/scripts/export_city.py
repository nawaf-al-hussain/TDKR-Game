#!/usr/bin/env python3
"""Full-city LOD-aware GLB exporter for the GitHub Pages viewer.

Reads raw/l_gothamcity/*.bdae (+ actors/Batarang showcase), classifies each file
into viewer tiers (hero / fp / low / district), packs geometry-only GLBs with
per-mesh nodes + per-mesh materials, and writes textures as external JPEGs.

Output (site staging):
  site/models/<name>.glb        geometry-only, one node+mesh+material per mesh
  site/models/tex/<Base>.jpg    external textures (viewer assigns material.map)
  site/models/manifest.json     tiers, per-file stats, texture mapping
  site/models/batarang.glb      self-contained easter egg (embedded texture)

Usage: python3 export_city.py [--dry] [--max-glb-mb 4]
"""
import argparse
import io
import json
import os
import re
import struct
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bdae_extract import parse_meshes, write_glb  # noqa: E402

RAW = "/home/z/my-project/download/TDKR_assets/raw"
PNG = "/home/z/my-project/download/TDKR_assets/textures_png"
SITE = "/home/z/my-project/work/site"
MODELS = os.path.join(SITE, "models")
TEXD = os.path.join(MODELS, "tex")

BAD_TEX = ("_nrm", "lightmap", "_lm", "_mask", "_refl", "sampler", "shadow",
           "_bump", "_spec", "_gloss", "_opacity", "_height", "_normal")

OVERRIDE_TEX = {
    # proven bindings (uv-verified renders + showcase pipeline)
    "GC_island1_LongDist": "GC_Island1_LongDist_Low",
    "GC_Island2_LongDist": "GC_Island2_LongDist_low",
    "GC_LongDist_Island1_Roads": "BakeGroup_Island1_Roads0",
    "GC_LongDist_Island2_Roads": "GC_LongDist_Island2_Roads",
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


def classify(name):
    n = name.lower()
    if "collision" in n:
        return "skip"
    if "_low" in n or n.endswith("low"):
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


def find_texture(path, base):
    """Resolve the diffuse/baked texture for a bdae file.
    1. explicit overrides (uv-verified bindings)
    2. self-reference: a pool string equal to the file base that exists on disk
    3. token-overlap scoring (dropping the meaningless 'gc' prefix), min score 1
    LongDist footprint atlases live in ZIP_SPLIT chunks (open item) -> None."""
    if base in OVERRIDE_TEX:
        c = os.path.join(PNG, "l_gothamcity_tex", OVERRIDE_TEX[base] + ".png")
        if os.path.exists(c):
            return OVERRIDE_TEX[base]
    strs = [m.group().decode() for m in re.finditer(rb"[ -~]{4,}", open(path, "rb").read())]

    def toks(s):
        return {t for t in re.split(r"[^a-z0-9]+", s.lower()) if t} - {"gc"}

    def exists(cand):
        for sub in ("l_gothamcity_tex", "actors_tex"):
            if os.path.exists(os.path.join(PNG, sub, cand + ".png")):
                return True
        return False

    bt = toks(base)
    best, bs = None, 0
    for s in strs:
        if not s.endswith(".tga") or any(k in s.lower() for k in BAD_TEX):
            continue
        cand = s[:-4]
        if not exists(cand):
            continue
        if cand == base:
            return cand
        sc = len(bt & toks(cand))
        # prefix bonus for compound names (diner~dinner, citybg~city_bkg)
        for a in bt:
            for b in toks(cand):
                n = 0
                for x, y in zip(a, b):
                    if x != y:
                        break
                    n += 1
                if n >= 4:
                    sc += 1
                    break
        if sc > bs:
            best, bs = cand, sc
    return best if bs >= 1 else None


def jpg_from_png(png_path, out_path, max_dim, quality):
    im = Image.open(png_path).convert("RGB")
    if max(im.size) > max_dim:
        im.thumbnail((max_dim, max_dim), Image.LANCZOS)
    im.save(out_path, "JPEG", quality=quality, optimize=True)
    return os.path.getsize(out_path)


class GlbBuilder:
    """Geometry-only GLB: every mesh becomes its own node + mesh + material."""

    def __init__(self):
        self.buf = bytearray()
        self.offset = 0
        self.views, self.accessors, self.meshes, self.nodes, self.materials = [], [], [], [], []

    def _add(self, data, align=4):
        pad = (-len(self.buf)) % align
        self.buf.extend(b"\0" * pad)
        self.offset += pad
        start = self.offset
        self.buf.extend(data)
        self.offset += len(data)
        return start, len(data)

    def add_material(self, name, color):
        self.materials.append(dict(
            name=name, doubleSided=True,
            pbrMetallicRoughness=dict(baseColorFactor=list(color) + [1.0],
                                      metallicFactor=0.0, roughnessFactor=1.0)))
        return len(self.materials) - 1

    def add_file(self, name, mesh_list, mat_id, yup=True):
        """One node + one mesh with one PRIMITIVE per source mesh (all sharing
        mat_id). Viewer maps gltf.scene.children[i] <-> manifest files[i] by order.
        (GLTFLoader sanitizes node names, so name-based matching is unreliable.)"""
        prims = []
        for m in mesh_list:
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
                              indices=len(a) - 1, material=mat_id, mode=4))
        mi = len(self.meshes)
        self.meshes.append(dict(name=name, primitives=prims))
        self.nodes.append(dict(mesh=mi, name=name))

    def write(self, out_path):
        pad = (-len(self.buf)) % 4
        self.buf.extend(b"\0" * pad)
        gltf = dict(
            asset=dict(version="2.0", generator="tdkr-export-city"),
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
    entries, skipped = [], 0
    print(f"scanning {len(files)} city bdae files ...")
    for fn in files:
        base = fn[:-len(".bdae.bin")]
        cat = classify(base)
        if cat == "skip":
            skipped += 1
            continue
        p = os.path.join(city_dir, fn)
        try:
            meshes = parse_meshes(p, verbose=False)
        except Exception:
            meshes = []
        if not meshes:
            continue
        tex = find_texture(p, base)
        verts = int(sum(m["count"] for m in meshes))
        tris = int(sum(m["numIdx"] // 3 for m in meshes))
        gbytes = verts * 32 + tris * 12  # pos+nrm+uv+u32 idx
        entries.append(dict(base=base, cat=cat, tex=tex, verts=verts, tris=tris,
                            nmesh=len(meshes), gbytes=gbytes, path=p, meshes=meshes))

    from collections import Counter
    c = Counter(e["cat"] for e in entries)
    tv = sum(e["verts"] for e in entries)
    tt = sum(e["tris"] for e in entries)
    ntex = len({e["tex"] for e in entries if e["tex"]})
    print(f"parsed: {len(entries)} files ({skipped} collision skipped) | "
          f"{tv:,} verts {tt:,} tris | {ntex} unique textures")
    for k, v in sorted(c.items()):
        sub = [e for e in entries if e["cat"] == k]
        print(f"  {k:<9} {v:>4} files  {sum(e['verts'] for e in sub):>9,}v "
              f"{sum(e['tris'] for e in sub):>8,}t  texless={sum(1 for e in sub if not e['tex'])}")
    untex = [e["base"] for e in entries if not e["tex"]]
    if untex:
        print(f"  texture-less files ({len(untex)}): {untex[:8]}{' ...' if len(untex) > 8 else ''}")
    if args.dry:
        for e in entries:
            print(f"  [{e['cat']:<8}] {e['base']:<52} {e['verts']:>7}v {e['tris']:>7}t "
                  f"tex={e['tex']}")
        return

    # ---------------- pack tiers into GLBs ----------------
    os.makedirs(MODELS, exist_ok=True)
    os.makedirs(TEXD, exist_ok=True)
    plan = []  # (glb_name, [entries])

    for e in [x for x in entries if x["cat"] == "hero"]:
        plan.append((e["base"], [e]))

    for isl in ("island1", "island2"):
        sub = [x for x in entries if x["cat"] == "fp" and fp_island(x["base"]) == isl]
        if sub:
            plan.append((f"fp_{isl}", sub))

    low = [x for x in entries if x["cat"] == "low"]
    if low:
        plan.append(("city_low", low))

    # districts: cluster by texture first, then bin-pack clusters by geometry bytes
    dist = [x for x in entries if x["cat"] == "district"]
    cap = int(args.max_glb_mb * 1024 * 1024)
    bytex = {}
    for e in dist:
        bytex.setdefault(e["tex"] or "__none__", []).append(e)
    bins = []
    for tex, group in sorted(bytex.items(), key=lambda kv: -sum(x["gbytes"] for x in kv[1])):
        cur, cur_b = [], 0
        for e in sorted(group, key=lambda x: -x["gbytes"]):
            if cur and cur_b + e["gbytes"] > cap:
                bins.append(cur)
                cur, cur_b = [], 0
            cur.append(e)
            cur_b += e["gbytes"]
        if cur:
            bins.append(cur)
    for i, b in enumerate(bins):
        plan.append((f"district_{i:02d}", b))

    manifest = dict(tiers={}, glbs=[], total_verts=tv, total_tris=tt)
    tex_used = {}
    for glb_name, group in plan:
        gb = GlbBuilder()
        for e in group:
            color = (0.55, 0.60, 0.70) if not e["tex"] else (1.0, 1.0, 1.0)
            mid = gb.add_material(e["tex"] or e["base"], color)
            gb.add_file(e["base"], e["meshes"], mid)
        glb_file = glb_name + ".glb"
        size = gb.write(os.path.join(MODELS, glb_file))
        manifest["glbs"].append(dict(
            file="models/" + glb_file, bytes=size,
            verts=sum(e["verts"] for e in group), tris=sum(e["tris"] for e in group),
            tier=group[0]["cat"] if len({e["cat"] for e in group}) == 1 else "district",
            files=[dict(name=e["base"], tex=e["tex"], verts=e["verts"], tris=e["tris"],
                        meshes=e["nmesh"]) for e in group]))
        for e in group:
            if e["tex"]:
                tex_used[e["tex"]] = max(tex_used.get(e["tex"], 0), e["gbytes"])
        print(f"  + {glb_file:<28} {size/1024:>7.0f} KB  {len(group)} files  "
              f"{sum(e['tris'] for e in group):>7,} tris")

    # ---------------- textures -> external JPEG ----------------
    hero_tex = {"GC_Island1_LongDist_Low", "GC_Island2_LongDist_low",
                "GC_LongDist_Island2_Roads", "BakeGroup_Island1_Roads0"}
    for tex in sorted(tex_used):
        src = os.path.join(PNG, "l_gothamcity_tex", tex + ".png")
        if not os.path.exists(src):
            src = os.path.join(PNG, "actors_tex", tex + ".png")
        if not os.path.exists(src):
            print(f"  !! texture missing on disk: {tex}")
            continue
        hero = tex in hero_tex
        n = tex + ".jpg"
        sz = jpg_from_png(src, os.path.join(TEXD, n), 2048 if hero else 1024,
                          82 if hero else 78)
        print(f"  tex {n:<40} {sz/1024:>6.0f} KB{' (hero 2048)' if hero else ''}")

    # ---------------- batarang showcase (self-contained) ----------------
    bat = os.path.join(RAW, "actors", "Batarang.bdae.bin")
    if os.path.exists(bat):
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
