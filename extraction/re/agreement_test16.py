#!/usr/bin/env python3
"""Session 16 — STREET-TIER AGREEMENT TEST (gate before exporter v16).

Question (collaborator round-3, point 1/3): does descriptor +40, read
through the materials DB in **library_materials order**, reproduce the
street-tier bindings the v5 exporter already gets right (roads, band-atlas
sidewalks, flats, small props)?

Populations over every segment of both islands:
  A  exporter NON-dark  AND  +40 material has a DiffuseMap
     -> exact-stem agreement (primary) + family agreement
  B  exporter NON-dark, any +40          -> coverage of the claim
  C  +40 material has a DiffuseMap, exporter dark -> the v16 payoff set

Orderings compared (the test must RULE ON THE ORDER):
  lib        library_materials order (hypothesis)
  alpha_name alphabetical by material name
  alpha_dif  alphabetical by DiffuseMap stem, None last
  rand(200)  null distribution (process rule: every metric gets a null)

Output: extraction/re/agreement_test16.json + stdout report.
"""
import collections
import json
import random
import struct
import sys

import numpy as np

sys.path.insert(0, "/home/z/my-project/repo/extraction/scripts")
from export_zone import (parse_island, bind_segment, cross_sections,  # noqa
                         ISLANDS, uv_of)

ZONE = "/home/z/my-project/work/zone"
RE = "/home/z/my-project/repo/extraction/re"
OUT_JSON = f"{RE}/agreement_test16.json"

ROAD_FAMILY = {"GothamCity_Road_v1_Island_1", "GothamCity_Road_v2_Island_1",
               "GothamCity_Road_Island_2", "GothamCity_Road_v2_Island_2",
               "GothamCity_Road_Crossings_Island_1",
               "GothamCity_Road_Crossings_Island_2",
               "gothamcity_roads_details"}
FLAT_FAMILY = {"GC_Park_grass", "GC_Park_dirt", "GothamCity_sand_tile",
               "GothamCity_asphalt_tile", "GC_SXC_grass"}


def family_of(stem):
    if stem is None:
        return "unbound"
    if stem in ROAD_FAMILY:
        return "road_band"
    if stem in FLAT_FAMILY:
        return "flat"
    if "Props" in stem or "Prop_" in stem:
        return "props"
    if stem.startswith("FX_Coronas"):
        return "coronas"
    if stem.startswith("GC_Footprint") or stem.startswith("GC_LongDist"):
        return "bake/facade"
    return "other"


def descriptors(island):
    """Mirrors export_zone.parse_island filters exactly; returns per-segment
    (+40, +36) in the same order as parse_island output."""
    lt = open(f"{ZONE}/{island}/lod_table.bin", "rb").read()
    ld = open(f"{ZONE}/{island}/lod_data.bin", "rb").read()
    u = struct.unpack(f"<{len(lt)//4}I", lt)
    n = u[0]
    pairs = [(u[1 + 2 * k], u[2 + 2 * k]) for k in range(n)]
    out = []
    for off, sz in pairs:
        data_off, four, vb, ib = struct.unpack_from("<4I", ld, off + 68)
        if four != 4:
            continue
        vstart = data_off + 4
        istart = vstart + vb
        idx = np.frombuffer(ld[istart:istart + ib], "<u2").astype(np.int32)
        real = idx[idx != 0xFFFF]
        mx = int(real.max()) if len(real) else 0
        stride = None
        for s in (24, 20, 32):
            if vb % s == 0 and mx < vb // s:
                t = np.frombuffer(ld[vstart:vstart + vb], "<f4").reshape(-1, s // 4)[:, :3]
                if np.isfinite(t).all() and np.abs(t).max() < 6000:
                    stride = s
                    break
        if stride is None:
            continue
        out.append((struct.unpack_from("<I", ld, off + 40)[0],
                    struct.unpack_from("<I", ld, off + 36)[0]))
    return out


def stem(dm):
    return dm.replace(".tga", "") if dm else None


def agreement(mats, order, exp_tex, m40s, fam_fn):
    """order: list mapping +40 value -> material dict.
    Returns dict with exact/family agreement over population A."""
    exact = fam_n = tot = 0
    for tex, m40 in zip(exp_tex, m40s):
        m = order[m40]
        d = stem(m.get("DiffuseMap"))
        if tex is None or d is None:
            continue
        tot += 1
        exact += (tex == d)
        fam_n += (fam_fn(tex) == fam_fn(d))
    return dict(popA=tot, exact=exact,
                exact_pct=100.0 * exact / max(tot, 1),
                family=fam_n, family_pct=100.0 * fam_n / max(tot, 1))


def main():
    rng = random.Random(1616)
    XSECS = {
        "GothamCity_Road_v1_Island_1": cross_sections("GothamCity_Road_v1_Island_1"),
        "GothamCity_Road_v2_Island_1": cross_sections("GothamCity_Road_v2_Island_1"),
        "GothamCity_Road_Island_2": cross_sections("GothamCity_Road_Island_2"),
        "gothamcity_roads_details": cross_sections("gothamcity_roads_details"),
        "GothamCity_Road_Crossings_Island_1": cross_sections("GothamCity_Road_Crossings_Island_1"),
        "GothamCity_Road_Crossings_Island_2": cross_sections("GothamCity_Road_Crossings_Island_2"),
    }
    report = {}
    for islname, isl in ISLANDS.items():
        xs = {k: v for k, v in XSECS.items()
              if (isl["isl"] == "1" and ("Island_1" in k or "details" in k))
              or (isl["isl"] == "2" and ("Island_2" in k or "details" in k))}
        mats = json.load(open(f"{RE}/mat_tex_{islname}.json"))["mats"]
        M = len(mats)
        segs = parse_island(islname)
        desc = descriptors(islname)
        assert len(segs) == len(desc), (len(segs), len(desc))
        m40s = [d[0] for d in desc]
        id36s = [d[1] for d in desc]

        binds = []
        classes = collections.Counter()
        for s in segs:
            tex, mode = bind_segment(s, isl, xs)
            binds.append(tex)
            if tex is None:
                classes["dark"] += 1
            else:
                fam = family_of(tex)
                classes[fam] += 1

        exp_tex = binds
        families = {}   # per stem, for family agreement
        def fam(st):
            if st not in families:
                families[st] = family_of(st)
            return families[st]

        # population stats
        popA = sum(1 for t, m in zip(exp_tex, m40s)
                   if t is not None and mats[m].get("DiffuseMap"))
        popB = sum(1 for t in exp_tex if t is not None)
        popC = sum(1 for t, m in zip(exp_tex, m40s)
                   if t is None and mats[m].get("DiffuseMap"))
        popB_m = sum(1 for t, m in zip(exp_tex, m40s)
                     if t is not None and mats[m].get("DiffuseMap"))
        unbound = sum(1 for m in m40s if not mats[m].get("DiffuseMap"))

        # ---- orderings
        res = {}
        res["lib"] = agreement(mats, mats, exp_tex, m40s, fam)

        alpha_name = sorted(mats, key=lambda m: m["name"])
        res["alpha_name"] = agreement(mats, alpha_name, exp_tex, m40s, fam)

        alpha_dif = sorted(mats, key=lambda m: (m.get("DiffuseMap") or "~", m["name"]))
        res["alpha_dif"] = agreement(mats, alpha_dif, exp_tex, m40s, fam)

        nulls = []
        idx = list(range(M))
        for _ in range(200):
            perm = idx[:]
            rng.shuffle(perm)
            shuffled = [mats[i] for i in perm]
            nulls.append(agreement(mats, shuffled, exp_tex, m40s, fam)["exact_pct"])
        res["rand200"] = dict(mean=float(np.mean(nulls)),
                              sd=float(np.std(nulls)),
                              max=float(np.max(nulls)),
                              p99=float(np.percentile(nulls, 99)))

        # ---- confusion: exporter class x +40 family (library order)
        conf = collections.Counter()
        for t, m in zip(exp_tex, m40s):
            conf[(fam(t) if t else "dark", fam(stem(mats[m].get("DiffuseMap"))))] += 1

        # ---- exact-mismatch listing (population A)
        mism = []
        for i, (t, m) in enumerate(zip(exp_tex, m40s)):
            d = stem(mats[m].get("DiffuseMap"))
            if t is not None and d is not None and t != d:
                mism.append(dict(seg=i, m40=m, exporter=t, plus40=d,
                                 lm=(mats[m].get("LightMap") or "")))

        # ---- mode discovery: LightMap-bound materials in +40
        lm_bound = sum(1 for m in m40s if mats[m].get("LightMap"))
        lm_stem = collections.Counter(stem(mats[m].get("LightMap") or "")
                                      for m in m40s if mats[m].get("LightMap"))

        r = dict(N=len(segs), M=M, popB_exporter_bound=popB,
                 popA_both=popA, popB_plus40_has_dif=popB_m,
                 popC_exporter_dark_plus40_binds=popC,
                 plus40_unbound_materials=unbound,
                 exporter_classes=dict(classes),
                 orderings=res,
                 lm_bound_segments=lm_bound, lm_pages=dict(lm_stem),
                 confusion={f"{k[0]}->{k[1]}": v for k, v in conf.most_common(40)},
                 mismatches=mism[:80], n_mismatches=len(mism),
                 id36=[(d[0], d[1]) for d in desc])
        report[islname] = r

        print(f"\n===== {islname}: N={len(segs)} M={M}")
        print(f"exporter bound={popB} ({dict(classes)}), +40-diffuse available on {popB_m}/{popB} of those")
        print(f"popA (both bound)={popA}   popC (exporter dark, +40 binds)={popC}")
        for k in ("lib", "alpha_name", "alpha_dif"):
            a = res[k]
            print(f"  {k:11s}: exact {a['exact']:3d}/{a['popA']:3d} = {a['exact_pct']:6.2f}%   "
                  f"family {a['family_pct']:6.2f}%")
        n = res["rand200"]
        print(f"  rand200 null: exact% mean {n['mean']:.2f} sd {n['sd']:.2f} "
              f"max {n['max']:.2f} p99 {n['p99']:.2f}")
        print(f"  LightMap-bound +40 segments: {lm_bound}  pages: {dict(lm_stem)}")
        print(f"  mismatches (popA): {len(mism)}")
        for mm in mism[:12]:
            print(f"    seg{mm['seg']:5d} m40={mm['m40']:3d} exp={mm['exporter'][:36]:36s} "
                  f"+40={mm['plus40'][:36]:36s} lm={mm['lm'][:34]}")

    json.dump(report, open(OUT_JSON, "w"), indent=1)
    print(f"\nwrote {OUT_JSON}")


if __name__ == "__main__":
    main()
