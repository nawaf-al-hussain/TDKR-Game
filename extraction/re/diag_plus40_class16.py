#!/usr/bin/env python3
"""Session 16 diagnostic: per-+40-value exporter-class structure.

If +40 is a per-segment material index, the segments sharing a +40 value
should be exporter-CLASS-pure (one material -> one texture -> one class).
Purity under the lib order + per-class top +40 values tell us whether the
field carries segment-type info and where the mapping diverges.
"""
import collections
import json
import struct
import sys

import numpy as np

sys.path.insert(0, "/home/z/my-project/repo/extraction/scripts")
from export_zone import parse_island, bind_segment, cross_sections, ISLANDS  # noqa

ZONE = "/home/z/my-project/work/zone"
RE = "/home/z/my-project/repo/extraction/re"
ROAD_FAMILY = {"GothamCity_Road_v1_Island_1", "GothamCity_Road_v2_Island_1",
               "GothamCity_Road_Island_2", "GothamCity_Road_v2_Island_2",
               "GothamCity_Road_Crossings_Island_1",
               "GothamCity_Road_Crossings_Island_2", "gothamcity_roads_details"}
FLAT_FAMILY = {"GC_Park_grass", "GC_Park_dirt", "GothamCity_sand_tile",
               "GothamCity_asphalt_tile", "GC_SXC_grass"}


def family_of(stem):
    if stem is None:
        return "dark"
    if stem in ROAD_FAMILY:
        return "road"
    if stem in FLAT_FAMILY:
        return "flat"
    if "Props" in stem or "Prop_" in stem:
        return "props"
    return "other"


def descriptors(island):
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
        out.append(struct.unpack_from("<I", ld, off + 40)[0])
    return out


def main():
    XSECS = {
        "GothamCity_Road_v1_Island_1": cross_sections("GothamCity_Road_v1_Island_1"),
        "GothamCity_Road_v2_Island_1": cross_sections("GothamCity_Road_v2_Island_1"),
        "GothamCity_Road_Island_2": cross_sections("GothamCity_Road_Island_2"),
        "gothamcity_roads_details": cross_sections("gothamcity_roads_details"),
        "GothamCity_Road_Crossings_Island_1": cross_sections("GothamCity_Road_Crossings_Island_1"),
        "GothamCity_Road_Crossings_Island_2": cross_sections("GothamCity_Road_Crossings_Island_2"),
    }
    for islname, isl in ISLANDS.items():
        xs = {k: v for k, v in XSECS.items()
              if (isl["isl"] == "1" and ("Island_1" in k or "details" in k))
              or (isl["isl"] == "2" and ("Island_2" in k or "details" in k))}
        mats = json.load(open(f"{RE}/mat_tex_{islname}.json"))["mats"]
        segs = parse_island(islname)
        m40s = descriptors(islname)
        classes = []
        for s in segs:
            tex, mode = bind_segment(s, isl, xs)
            classes.append(family_of(tex))

        # per +40 value: exporter-class histogram
        per = collections.defaultdict(collections.Counter)
        for m40, cl in zip(m40s, classes):
            per[m40][cl] += 1
        # purity stats
        tot = pure = 0
        pur_by_n = []
        for v, c in per.items():
            n = sum(c.values())
            top_n = c.most_common(1)[0][1]
            tot += n
            pure += top_n
            if n >= 5:
                pur_by_n.append((n, top_n / n, v, dict(c)))
        print(f"\n===== {islname}: class-purity weighted = {pure}/{tot} = {100.0*pure/tot:.1f}%")
        pur_by_n.sort(reverse=True)
        print("largest +40 groups (n>=5) with class mix:")
        for n, p, v, c in pur_by_n[:18]:
            m = mats[v]
            print(f"  +40={v:3d} n={n:4d} purity={p:.2f} dif={(m['DiffuseMap'] or '-')[:38]:38s} "
                  f"lm={(m['LightMap'] or '-')[:30]:30s} classes={c}")

        # per exporter class: top +40 values
        by_class = collections.defaultdict(collections.Counter)
        for m40, cl in zip(m40s, classes):
            by_class[cl][m40] += 1
        print("per exporter class, top 8 +40 values:")
        for cl in ("road", "flat", "props", "dark", "other"):
            if cl not in by_class:
                continue
            tops = by_class[cl].most_common(8)
            desc = ", ".join(f"{v}({c})" for v, c in tops)
            print(f"  {cl:6s}: {desc}")
            for v, c in tops[:3]:
                m = mats[v]
                print(f"      m{v:3d} dif={(m['DiffuseMap'] or '-')[:40]:40s} "
                      f"lm={(m['LightMap'] or '-')[:34]}")


if __name__ == "__main__":
    main()
