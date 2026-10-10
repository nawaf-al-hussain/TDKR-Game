#!/usr/bin/env python3
"""Round-6 ask 1 — THE PAGE-TYPE TABLE.

The round-5 enrichment verdicts ("metric-silent by construction" for
building/road/flat/trees, "dark-pad thin-stroke" for props, "additive-glow
breaks the mask" for coronas) were asserted per family but the actual pages
behind those verdicts were never tabulated.  This script produces the table:

  for every decoded texture page referenced by any material of either island
  (diffuse OR lightmap role):
    stem, archive, WxH, contentA (mask_A non-empty rate = the enrichment
    denominator / uniform-random baseline), n_cells, coverage, big_cells,
    page TYPE, bound families (+40 diffuse role), street-segment count.

Page TYPE rules (deterministic, ordered):
  full_bleed   contentA >= 0.85                  -> baseline ~1, enrichment
                                                    silent for ANY binding
  atlas_dense  n_cells>=2 and contentA >= 0.50
  atlas_mid    n_cells>=2 and 0.15<=contentA<0.50
  dark_pad     n_cells>=2 and contentA < 0.15    -> the thin-stroke confound
                                                    class (cells mostly black
                                                    padding)
  sparse_blob  n_cells <= 1 and contentA < 0.85  -> single decal/lamp on
                                                    padding
Type is pixel-derived only; the glow/corona caveat is carried by the family
column (SimpleAdditive pages are additive, mask_A overcounts "content").

Outputs: extraction/re/round6_pagetypes.json + stdout tables.
"""
import collections
import json
import sys

import numpy as np

sys.path.insert(0, "/home/z/my-project/repo/extraction/scripts")
sys.path.insert(0, "/home/z/my-project/repo/extraction/re")
from export_zone import ISLANDS, find_png  # noqa
from round4_street_evidence import (TexData, stem_of, fam40,  # noqa
                                    m40_list)

RE = "/home/z/my-project/repo/extraction/re"


def page_type(contentA, n_cells, big_cells):
    if contentA >= 0.85:
        return "full_bleed"
    if n_cells >= 2 or big_cells >= 2:
        if contentA >= 0.50:
            return "atlas_dense"
        if contentA >= 0.15:
            return "atlas_mid"
        return "dark_pad"
    return "sparse_blob"


def main():
    isl_segmats = {}
    for islname in ISLANDS:
        m40s = m40_list(islname)
        isl_segmats[islname] = m40s

    # material -> (diffuse stem, lightmap stem, technique base, family)
    mat_info = {}
    for islname, path in (("GothamCity", f"{RE}/runtime_mats_GothamCity.json"),
                          ("GothamCity_Island2",
                           f"{RE}/runtime_mats_GothamCity_Island2.json")):
        rows = json.load(open(path))
        for m, r in enumerate(rows):
            tech = r.get("technique", "").split("-fx_")[0].lstrip("#")
            mat_info[(islname, m)] = dict(
                dif=stem_of(r.get("DiffuseMap")),
                lm=stem_of(r.get("LightMap")),
                tech=tech,
                fam=fam40(stem_of(r.get("DiffuseMap"))))

    # street-segment count per (island, material)
    segcount = collections.Counter()
    for islname, m40s in isl_segmats.items():
        for m in m40s:
            segcount[(islname, m)] += 1

    # unique pages and their roles
    pages = collections.defaultdict(lambda: dict(
        roles=set(), fams=collections.Counter(), segs=0, mats=set(),
        techs=set()))
    for key, info in mat_info.items():
        islname, m = key
        nseg = segcount.get(key, 0)
        for role, stem in (("diffuse", info["dif"]), ("lightmap", info["lm"])):
            if not stem:
                continue
            p = pages[stem]
            p["roles"].add(role)
            p["fams"][info["fam"]] += 1
            p["techs"].add(info["tech"])
            p["mats"].add((islname, m))
            if role == "diffuse" and info["fam"] != "unbound":
                p["segs"] += nseg

    print(f"unique referenced stems: {len(pages)}")
    out_rows = []
    type_stats = collections.defaultdict(lambda: dict(
        n=0, cA=[], segs=0, fams=collections.Counter()))
    failures = []
    for stem, meta in sorted(pages.items()):
        t = TexData(stem)
        png = find_png(stem)
        if not t.ok or png is None:
            failures.append(stem)
            continue
        strict = (t.alpha < 64) | (t.rgb.max(axis=2) <= 10)
        contentA = 1.0 - float(strict.mean())
        pt = page_type(contentA, t.n_cells, t.big_cells)
        fams_c = meta["fams"]
        top_fams = ", ".join(f"{f}:{c}" for f, c in fams_c.most_common(4))
        arch = "commons_tex" if "/commons_tex/" in str(png) else "l_gothamcity_tex"
        row = dict(
            stem=stem, arch=arch, w=t.w, h=t.h,
            contentA=round(contentA, 4), n_cells=int(t.n_cells),
            big_cells=int(t.big_cells), coverage=round(t.coverage, 4),
            type=pt, roles=sorted(meta["roles"]),
            top_families=top_fams, n_mats=len(meta["mats"]),
            street_segs=int(meta["segs"]))
        out_rows.append(row)
        st = type_stats[pt]
        st["n"] += 1
        st["cA"].append(contentA)
        st["segs"] += meta["segs"]
        for f, c in fams_c.items():
            st["fams"][f] += c

    summary = {}
    for pt, st in sorted(type_stats.items()):
        cA = st["cA"]
        summary[pt] = dict(
            n_pages=st["n"],
            contentA_mean=round(float(np.mean(cA)), 3),
            contentA_min=round(float(np.min(cA)), 3),
            contentA_max=round(float(np.max(cA)), 3),
            street_segs_bound=st["segs"],
            top_families=[f"{f}:{c}" for f, c in st["fams"].most_common(8)])

    print("\n== PAGE-TYPE SUMMARY (mask_A = alpha<64 | near-black) ==")
    print(f"   {'type':12s} {'pages':>5s} {'contentA':>17s} {'segs':>6s}  top families")
    for pt, s in summary.items():
        print(f"   {pt:12s} {s['n_pages']:5d}   "
              f"{s['contentA_mean']:5.3f} [{s['contentA_min']:.2f},"
              f"{s['contentA_max']:.2f}] {s['street_segs_bound']:6d}  "
              f"{', '.join(s['top_families'][:5])}")

    # per-family page-type cross-tab (street-relevant families only)
    fam_type = collections.defaultdict(lambda: collections.Counter())
    fam_segs = collections.Counter()
    for row in out_rows:
        # attribute page to families via fams field
        for fv in row["top_families"].split(", "):
            f, c = fv.rsplit(":", 1)
            fam_type[f][row["type"]] += int(c)
    for (islname, m), c in segcount.items():
        info = mat_info[(islname, m)]
        if info["fam"] != "unbound" and info["dif"]:
            fam_segs[info["fam"]] += c

    print("\n== FAMILY x PAGE-TYPE (diffuse pages, weighted by material "
          "count) ==")
    order = ["road_band", "building_residential", "building_landmark",
             "building_office", "flat", "trees", "props_street",
             "props_rooftop", "mono_rail", "billboards", "coronas"]
    allf = sorted(set(list(fam_type) + order),
                  key=lambda f: -fam_segs.get(f, 0))
    print(f"   {'family':22s} {'segs':>5s} " + " ".join(
        f"{t[:9]:>10s}" for t in
        ("full_bleed", "atlas_dense", "atlas_mid", "dark_pad",
         "sparse_blob")))
    for f in allf:
        c = fam_type.get(f)
        if not c:
            continue
        tot = sum(c.values())
        print(f"   {f:22s} {fam_segs.get(f, 0):5d} " + " ".join(
            f"{c.get(t, 0):>10d}" for t in
            ("full_bleed", "atlas_dense", "atlas_mid", "dark_pad",
             "sparse_blob")) + f"   (pages {tot})")

    # extremes worth eyeballing
    print("\n== dark_pad pages with most street segments bound ==")
    for row in sorted([r for r in out_rows if r["type"] == "dark_pad"],
                      key=lambda r: -r["street_segs"])[:10]:
        print(f"   {row['stem']:36s} cA={row['contentA']:.3f} "
              f"cells={row['big_cells']:3d} segs={row['street_segs']:5d} "
              f"{row['top_families'][:60]}")
    print("== full_bleed pages with most street segments bound ==")
    for row in sorted([r for r in out_rows if r["type"] == "full_bleed"],
                      key=lambda r: -r["street_segs"])[:10]:
        print(f"   {row['stem']:36s} cA={row['contentA']:.3f} "
              f"segs={row['street_segs']:5d}  {row['top_families'][:60]}")

    json.dump(dict(
        rules=dict(full_bleed="contentA>=0.85",
                   atlas_dense="n_cells>=2 & contentA>=0.50",
                   atlas_mid="n_cells>=2 & 0.15<=contentA<0.50",
                   dark_pad="n_cells>=2 & contentA<0.15",
                   sparse_blob="n_cells<=1 & contentA<0.85",
                   mask_A="alpha<64 | rgb.max<=10",
                   note="contentA IS the enrichment denominator "
                        "(uniform-random non-empty rate); glow/corona "
                        "pages are additive: mask_A overcounts content "
                        "there (family column flags them)"),
        summary=summary,
        pages=out_rows,
        decode_failures=failures),
        open(f"{RE}/round6_pagetypes.json", "w"), indent=1)
    print(f"\nwrote {RE}/round6_pagetypes.json  "
          f"({len(out_rows)} pages, {len(failures)} decode failures)")


if __name__ == "__main__":
    main()
