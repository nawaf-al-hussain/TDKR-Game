#!/usr/bin/env python3
"""Session 16: THE RUNTIME ORDER TEST.

source.dae library_materials order FAILED the agreement test. The engine
does not parse source.dae — it parses the compiled BRES variant
(little_endian_quantized.bdae). Its render-unit array IS the runtime
material table. Map descriptor +40 -> render unit +40 -> DiffuseMap/LightMap
texIdx -> texture stem, re-run the street agreement test.
"""
import collections
import json
import struct
import sys
import zipfile

import numpy as np

sys.path.insert(0, "/home/z/my-project/repo/extraction/scripts")
from export_zone import parse_island, bind_segment, cross_sections, ISLANDS  # noqa
from ground_truth import parse_file  # noqa

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


def runtime_table(island, variant="little_endian_quantized.bdae"):
    z = zipfile.ZipFile(f"{ZONE}/{island}/{island}_materials.bdae")
    d = z.read(variant)
    import tempfile, os
    p = tempfile.NamedTemporaryFile(suffix=".bdae", delete=False)
    p.write(d)
    p.close()
    ft = parse_file(p.name)
    os.unlink(p.name)
    texs = ft["textures"]
    units = ft["units"]
    rows = []
    for u in units:
        dm = lm = None
        if "DiffuseMap" in u["samplers"]:
            ti = u["samplers"]["DiffuseMap"]["texIdx"]
            dm = texs[ti] if 0 <= ti < len(texs) else f"tex{ti}"
        if "LightMap" in u["samplers"]:
            ti = u["samplers"]["LightMap"]["texIdx"]
            lm = texs[ti] if 0 <= ti < len(texs) else f"tex{ti}"
        rows.append(dict(name=u["material"], technique=u["technique"],
                         DiffuseMap=dm, LightMap=lm,
                         so=u["samplers"].get("DiffuseMap", {}).get("scaleoffset")))
    return rows, len(texs)


def stem(s):
    return s.replace(".tga", "") if s else None


def main():
    XSECS = {
        "GothamCity_Road_v1_Island_1": cross_sections("GothamCity_Road_v1_Island_1"),
        "GothamCity_Road_v2_Island_1": cross_sections("GothamCity_Road_v2_Island_1"),
        "GothamCity_Road_Island_2": cross_sections("GothamCity_Road_Island_2"),
        "gothamcity_roads_details": cross_sections("gothamcity_roads_details"),
        "GothamCity_Road_Crossings_Island_1": cross_sections("GothamCity_Road_Crossings_Island_1"),
        "GothamCity_Road_Crossings_Island_2": cross_sections("GothamCity_Road_Crossings_Island_2"),
    }
    import os
    lt_cache = {}
    for islname, isl in ISLANDS.items():
        xs = {k: v for k, v in XSECS.items()
              if (isl["isl"] == "1" and ("Island_1" in k or "details" in k))
              or (isl["isl"] == "2" and ("Island_2" in k or "details" in k))}
        rows, ntex = runtime_table(islname)
        print(f"\n===== {islname}: {len(rows)} runtime material units, {ntex} textures")
        for i, r in enumerate(rows[:8]):
            print(f"  unit{i:3d} {str(r['name'])[:34]:34s} tech={str(r['technique'])[:24]:24s} "
                  f"dif={str(r['DiffuseMap'])[:36]:36s} lm={str(r['LightMap'])[:30]}")
        # position of road-ish materials in runtime order
        for want in ("GothamCity_Road_v1_Island_1", "GothamCity_Road_v2_Island_1",
                     "GothamCity_Road_Crossings_Island_1", "gothamcity_roads_details",
                     "GC_Park_grass", "GC_Z1_Props_Street", "trunk", "FX_Coronas"):
            pos = [i for i, r in enumerate(rows) if r["DiffuseMap"] == want]
            print(f"  runtime positions of {want}: {pos[:8]}")

        # segments + +40
        lt = open(f"{ZONE}/{islname}/lod_table.bin", "rb").read()
        ld = open(f"{ZONE}/{islname}/lod_data.bin", "rb").read()
        u32 = struct.unpack(f"<{len(lt)//4}I", lt)
        n = u32[0]
        pairs = [(u32[1 + 2 * k], u32[2 + 2 * k]) for k in range(n)]
        m40s = []
        segs = parse_island(islname)
        si = 0
        for off, sz in pairs:
            data_off, four, vb, ib = struct.unpack_from("<4I", ld, off + 68)
            if four != 4:
                continue
            vstart = data_off + 4
            idx = np.frombuffer(ld[vstart + vb:vstart + vb + ib], "<u2").astype(np.int32)
            real = idx[idx != 0xFFFF]
            mx = int(real.max()) if len(real) else 0
            ok = False
            for s in (24, 20, 32):
                if vb % s == 0 and mx < vb // s:
                    t = np.frombuffer(ld[vstart:vstart + vb], "<f4").reshape(-1, s // 4)[:, :3]
                    if np.isfinite(t).all() and np.abs(t).max() < 6000:
                        ok = True
                        break
            if not ok:
                continue
            m40s.append(struct.unpack_from("<I", ld, off + 40)[0])
            si += 1
        assert len(m40s) == len(segs)

        exp = []
        for s in segs:
            tex, mode = bind_segment(s, isl, xs)
            exp.append(tex)

        # agreement under runtime order
        ok = tot = fok = 0
        mism = []
        for i, (t, v) in enumerate(zip(exp, m40s)):
            if v >= len(rows):
                continue
            dm = stem(rows[v]["DiffuseMap"])
            if t is None or dm is None:
                continue
            tot += 1
            ok += (t == dm)
            fok += (family_of(t) == family_of(dm))
            if t != dm:
                mism.append((i, v, t, dm, rows[v]["LightMap"]))
        print(f"  RUNTIME-ORDER agreement: exact {ok}/{tot} = {100.0*ok/max(tot,1):.2f}%  "
              f"family {100.0*fok/max(tot,1):.2f}%")
        for mm in mism[:12]:
            print(f"    seg{mm[0]:5d} +40={mm[1]:3d} exp={mm[2][:34]:34s} "
                  f"rt={mm[3][:34]:34s} lm={str(mm[4])[:28]}")


if __name__ == "__main__":
    main()
