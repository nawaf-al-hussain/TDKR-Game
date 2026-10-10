#!/usr/bin/env python3
"""Round-4: quantify the v15 -> v16 street-binding change.

Reviewer asks:
  - how many segments changed texture from v15 to v16, and what the old
    binding assigned to them (the original brief said street materials were
    correct — that is now false for most of the tier; say so explicitly).
  - stratify the 99.5% coverage by family (road, sidewalk, props, buildings).
  - list the 8 unbound segments (with material name + reason).

Output: extraction/re/round4_delta16.json + stdout tables.
"""
import collections
import json
import struct
import sys

import numpy as np

sys.path.insert(0, "/home/z/my-project/repo/extraction/scripts")
from export_zone import (parse_island, bind_segment, cross_sections,  # noqa
                         ISLANDS, find_png)

RE = "/home/z/my-project/repo/extraction/re"
ZONE = "/home/z/my-project/work/zone"
OUT = f"{RE}/round4_delta16.json"


def stem_of(dm):
    if not dm or dm == "UNBOUND":
        return None
    s = dm
    for ext in (".tga", ".png", ".jpg"):
        if s.lower().endswith(ext):
            return s[: -len(ext)]
    return s


def m40_and_w3(island):
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
        idx = np.frombuffer(ld[vstart + vb:vstart + vb + ib], "<u2").astype(np.int32)
        real = idx[idx != 0xFFFF]
        mx = int(real.max()) if len(real) else 0
        stride = None
        for s in (24, 20, 32):
            if vb % s == 0 and mx < vb // s:
                t = np.frombuffer(ld[vstart:vstart + vb], "<f4").reshape(-1, s // 4)[:, :3]
                if np.isfinite(t).all() and np.abs(t).max() < 6000:
                    stride = s
                    break
        if not stride:
            continue
        m40 = struct.unpack_from("<I", ld, off + 40)[0]
        out.append(m40)
    return out


def fam15(stem):
    if stem is None:
        return "dark"
    if "Road" in stem or "roads_details" in stem:
        return "road_band"
    if stem in ("GC_Park_grass", "GC_Park_dirt", "GothamCity_sand_tile",
                "GothamCity_asphalt_tile", "GC_SXC_grass"):
        return "flat"
    if "Props" in stem or "Prop_" in stem:
        return "props"
    if stem.startswith("FX_Coronas"):
        return "coronas"
    return "other"


def fam16(stem):
    if stem is None:
        return "unbound_dark"
    if "Road" in stem or "roads_details" in stem:
        return "road_band"
    if stem in ("GC_Park_grass", "GC_Park_dirt", "GothamCity_sand_tile",
                "GothamCity_asphalt_tile", "GC_SXC_grass", "GC_SXC_ground_tile",
                "GC_SXC_hedge", "GC_T_Concrete_01", "GC_T_Concrete_02"):
        return "sidewalk_flat"
    if stem.startswith("GC_Z1_Props_Street"):
        return "props_street"
    if stem.startswith("GC_Z1_Props_Rooftop"):
        return "props_rooftop"
    if stem == "trunk":
        return "trees"
    if stem.startswith("FX_Coronas"):
        return "coronas"
    if stem.startswith("HC_Prop_Billboard"):
        return "billboards"
    if "Residential_Props" in stem:
        return "props_mono_rail"
    if stem.startswith(("GC_Footprint", "GC_footprint", "GC_Residential_BD",
                        "GC_Z1_Shops", "GC_Cath", "GC_SXC_Atlas", "GC_Walls",
                        "GC_CBCE", "GC_DMUS", "GC_Glass", "GC_Statues",
                        "GC_Park_atlas", "GC_VPOW", "GC_VRS", "GC_Truck",
                        "GC_Industrial")) or "bridge" in stem.lower():
        return "buildings"
    return "other"


def main():
    report = {}
    XSECS = {k: cross_sections(k) for k in (
        "GothamCity_Road_v1_Island_1", "GothamCity_Road_v2_Island_1",
        "GothamCity_Road_Island_2", "gothamcity_roads_details",
        "GothamCity_Road_Crossings_Island_1",
        "GothamCity_Road_Crossings_Island_2")}
    for islname, isl in ISLANDS.items():
        print(f"\n########## {islname}")
        rows = json.load(open(f"{RE}/runtime_mats_{islname}.json"))
        segs = parse_island(islname)
        m40s = m40_and_w3(islname)
        assert len(segs) == len(m40s)
        xs = {k: v for k, v in XSECS.items()
              if (isl["isl"] == "1" and ("Island_1" in k or "details" in k))
              or (isl["isl"] == "2" and ("Island_2" in k or "details" in k))}

        n = len(segs)
        v15 = []
        for s in segs:
            t, mode = bind_segment(s, isl, xs)
            v15.append(t)
        v16 = [stem_of(rows[m].get("DiffuseMap")) for m in m40s]
        v16_lm = [stem_of(rows[m].get("LightMap")) for m in m40s]

        changed = sum(1 for a, b in zip(v15, v16)
                      if (a or None) != (b or None))
        v15_bound = sum(1 for t in v15 if t)
        v16_bound = sum(1 for t, l in zip(v16, v16_lm) if t or l)
        both_bound = sum(1 for a, b in zip(v15, v16) if a and b)
        same_both = sum(1 for a, b in zip(v15, v16) if a and b and a == b)
        dark_to_bound = sum(1 for a, b in zip(v15, v16) if not a and b)
        bound_to_dark = sum(1 for a, b in zip(v15, v16) if a and not b)
        crosstab = collections.Counter(
            (fam15(a), fam16(b)) for a, b in zip(v15, v16))
        print(f"n={n}  v15 bound {v15_bound} ({100.0*v15_bound/n:.1f}%)  "
              f"v16 bound {v16_bound} ({100.0*v16_bound/n:.1f}%)")
        print(f"changed texture: {changed} ({100.0*changed/n:.1f}%)  | kept same "
              f"{same_both} | dark->bound {dark_to_bound} | bound->dark "
              f"{bound_to_dark}")
        print("crosstab v15-family -> v16-family (top 14):")
        for (fa, fb), c in crosstab.most_common(14):
            print(f"  {fa:14s} -> {fb:16s} {c:5d}")

        # stratified coverage by v16 coarse family
        COARSE = {"road_band": "road", "sidewalk_flat": "sidewalk_flat",
                  "props_street": "props", "props_rooftop": "props",
                  "trees": "props", "coronas": "props", "billboards": "props",
                  "props_mono_rail": "props", "buildings": "buildings",
                  "other": "other", "unbound_dark": "unbound_dark"}
        strat = collections.defaultdict(lambda: dict(n=0, bound=0, missing=0))
        for i, (t, l) in enumerate(zip(v16, v16_lm)):
            f = COARSE[fam16(t if t else l)]
            e = strat[f]
            e["n"] += 1
            if t or l:
                if find_png(t or l) is None:
                    e["missing"] += 1
                else:
                    e["bound"] += 1
        print("coverage by family (v16):")
        for f, e in sorted(strat.items()):
            print(f"  {f:14s} n={e['n']:5d} bound={e['bound']:5d} "
                  f"({100.0*e['bound']/max(e['n'],1):.1f}%) missing={e['missing']}")

        # unbound segments under v16 (+ .TGA fix applied)
        unbound = []
        for i, (t, l) in enumerate(zip(v16, v16_lm)):
            if t or l:
                continue
            m = m40s[i]
            row = rows[m] if m < len(rows) else {}
            tech = (row.get("technique") or "")
            reason = ("no-material" if m >= len(rows)
                      else "vcblend-no-dif" if "vcblend" in tech.lower()
                      else "null-material-renderer" if "Null" in tech
                      else "unbound-both-samplers")
            unbound.append(dict(seg=i, m40=m, name=row.get("name"),
                                technique=tech.split("-fx_")[0].lstrip("#"),
                                dif=row.get("DiffuseMap"),
                                lm=row.get("LightMap"), reason=reason))
        print(f"unbound segments: {len(unbound)}")
        for u in unbound:
            print(f"  seg{u['seg']:5d} m40={u['m40']:3d} {u['technique']:22s} "
                  f"{u['reason']:22s} dif={u['dif']} lm={u['lm']}")

        # missing-texture segments under v16 (stem fix applied)
        missing = [i for i, (t, l) in enumerate(zip(v16, v16_lm))
                   if (t or l) and find_png(t or l) is None]
        print(f"missing-texture segments after .TGA fix: {len(missing)}")
        for i in missing:
            print(f"  seg{i} m40={m40s[i]} tex={v16[i] or v16_lm[i]}")

        report[islname] = dict(
            n=n, v15_bound=v15_bound, v16_bound=v16_bound, changed=changed,
            pct_changed=round(100.0 * changed / n, 1),
            kept_same=same_both, dark_to_bound=dark_to_bound,
            bound_to_dark=bound_to_dark,
            crosstab={f"{a}->{b}": c for (a, b), c in crosstab.most_common()},
            coverage={f: e for f, e in strat.items()},
            unbound=unbound, missing=missing)

    json.dump(report, open(OUT, "w"), indent=1)
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
