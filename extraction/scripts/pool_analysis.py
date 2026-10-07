#!/usr/bin/env python3
"""Analyze per-file texture references (string pools) vs per-mesh footer materials
across all l_gothamcity bdae files. Decides the binding strategy per file:
  - unique diffuse tga in pool -> unambiguous
  - multiple -> per-mesh UV disambiguation needed
  - zero -> fallback (override / dark)
"""
import os, re, sys, json
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bdae_extract import parse_meshes

RAW = "/home/z/my-project/download/TDKR_assets/raw/l_gothamcity"
PNG = "/home/z/my-project/download/TDKR_assets/textures_png"
BAD = ("_nrm", "lightmap", "_lm", "_mask", "_refl", "sampler", "shadow",
       "_bump", "_spec", "_gloss", "_opacity", "_height", "_normal", "font")

def exists(c):
    for sub in ("l_gothamcity_tex", "actors_tex", "vehicles_tex"):
        if os.path.exists(os.path.join(PNG, sub, c + ".png")):
            return True
    return False

def classify(name):
    n = name.lower()
    if "collision" in n: return "skip"
    if n.endswith("_low") or n.endswith("low"): return "low"
    if "bigbridge" in n or "roads" in n: return "hero"
    if "longdist" in n and ("island1" in n or "island2" in n): return "hero"
    if "fp" in n and "longdist" in n or re.search(r"fp\d", n) or "footprint" in n: return "fp"
    return "district"

rows, skipped = [], 0
files = sorted(f for f in os.listdir(RAW) if f.endswith(".bdae.bin"))
for fn in files:
    base = fn[:-len(".bdae.bin")]
    if classify(base) == "skip":
        skipped += 1; continue
    p = os.path.join(RAW, fn)
    try:
        meshes = parse_meshes(p, verbose=False)
    except Exception:
        meshes = []
    if not meshes:
        continue
    d = open(p, "rb").read()
    strs = [m.group().decode() for m in re.finditer(rb"[ -~]{4,}", d)]
    tgas = [s[:-4] for s in strs if s.endswith(".tga")]
    dif = [t for t in tgas if not any(k in t.lower() for k in BAD)]
    dif_on_disk = sorted({t for t in dif if exists(t)})
    mats = sorted({m["material"] for m in meshes if m["material"]})
    rows.append(dict(base=base, nmesh=len(meshes),
                     verts=sum(m["count"] for m in meshes),
                     tris=sum(m["numIdx"]//3 for m in meshes),
                     pool=sorted(set(dif)), pool_disk=dif_on_disk, mats=mats))

c = Counter()
for r in rows:
    n = len(r["pool_disk"])
    c["0 (no pool tex on disk)" if n == 0 else ("1 (unique)" if n == 1 else f"2+ (ambiguous)")] += 1
print(f"files={len(rows)} skipped_collision={skipped}")
for k, v in sorted(c.items()):
    print(f"  {k:<26} {v}")

print("\n--- ambiguous (2+) samples ---")
for r in [x for x in rows if len(x['pool_disk']) > 1][:12]:
    print(f"  {r['base'][:42]:42s} pool={r['pool_disk']}  mats={r['mats'][:3]}")

print("\n--- zero-on-disk samples ---")
for r in [x for x in rows if len(x['pool_disk']) == 0][:15]:
    print(f"  {r['base'][:42]:42s} pool={r['pool'][:4]}  mats={r['mats'][:2]}")

json.dump(rows, open("/home/z/my-project/work/pool_analysis.json", "w"), indent=1)
print("\nsaved work/pool_analysis.json")
