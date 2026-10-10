#!/usr/bin/env python3
"""Session 16: decode the compiled bdae runtime material records and re-run
the street agreement test through them.

Record array (found at first material-name pointer, stride 32B):
  [name_ptr][name_ptr][u32 0][effect_ptr][u32 N][sampler_list_ptr][X][0xffffffff][0x80]
Sampler list: records [name_ptr][name_ptr][13][ptr][w1..w4][texIdx]
  name in {DiffuseMap, LightMap, ...}; texIdx -> compiled image table.
Image table: array of u32 pointers to '<name>.tga' strings (image0, image1...).

Outputs rows[i] = {name, technique, DiffuseMap, LightMap} in RUNTIME order,
then agreement vs the v5 exporter bindings.
"""
import collections
import json
import struct
import sys
import zipfile

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


def all_len_strings(d):
    out = {}
    i = 0
    n = len(d)
    while i + 4 <= n:
        L = struct.unpack_from("<I", d, i)[0]
        if 4 <= L <= 80 and i + 4 + L <= n:
            s = d[i + 4:i + 4 + L]
            if all(0x20 <= c < 0x7f for c in s):
                out[i + 4] = s.decode()
                i += 4 + L + 1
                continue
        i += 1
    return out


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


def stem(s):
    return s.replace(".tga", "") if s else None


def decode_runtime(island, variant="little_endian_quantized.bdae"):
    z = zipfile.ZipFile(f"{ZONE}/{island}/{island}_materials.bdae")
    d = z.read(variant)
    strs = all_len_strings(d)

    libnames = {m["name"] for m in
                json.load(open(f"{RE}/mat_tex_{island}.json"))["mats"]}
    mat_strs = sorted(o for o, s in strs.items() if s in libnames)
    if not mat_strs:
        raise RuntimeError("no material name strings")

    # locate name pointers; records = pointer positions (stride 32, name twice)
    ptr_locs = []
    for off in mat_strs:
        pat = struct.pack("<I", off)
        j = d.find(pat)
        while j >= 0:
            ptr_locs.append(j)
            j = d.find(pat, j + 4)
    ptr_locs.sort()
    # records: keep positions where next ptr loc is +4 (double name) or +32
    recs = []
    i = 0
    while i < len(ptr_locs):
        j = ptr_locs[i]
        if i + 1 < len(ptr_locs) and ptr_locs[i + 1] == j + 4:
            recs.append(j)
            i += 2
        else:
            recs.append(j)
            i += 1
    # dedupe the double-name (+4) pairs; verify stride 36 (histogram said
    # 4 x307 + 32 x306 = 613 gaps for 614 ptrs => record = 9 words = 36 B)
    starts = []
    i = 0
    while i < len(ptr_locs):
        j = ptr_locs[i]
        if i + 1 < len(ptr_locs) and ptr_locs[i + 1] == j + 4:
            starts.append(j)
            i += 2
        else:
            starts.append(j)
            i += 1
    diffs = collections.Counter(b - a for a, b in zip(starts, starts[1:]))
    print(f"  record starts: {len(starts)}, stride histogram: {diffs.most_common(4)}")
    grid = starts

    # image table: 12-byte records [imageN_ptr x2][<name>.tga_ptr], in order;
    # scan pointer positions (not string positions)
    imgs = []
    n = len(d)
    tga_offs = {o for o, s in strs.items() if s.lower().endswith(".tga")}
    base = None
    for j in range(0, n - 12, 4):
        a, b, c = struct.unpack_from("<3I", d, j)
        if a == b and a in strs and strs[a].startswith("image") and c in tga_offs:
            base = j
            break
    if base is not None:
        while base + 12 <= n:
            a, b, c = struct.unpack_from("<3I", d, base)
            if a == b and a in strs and strs[a].startswith("image") and c in tga_offs:
                imgs.append(strs[c])
                base += 12
            else:
                break
    print(f"  image table: {len(imgs)} entries")

    rows = []
    for rec in grid:
        w = struct.unpack_from("<9I", d, rec)
        name = strs.get(w[0])
        effect = strs.get(w[3])
        nsam = w[4]
        listp = w[5]
        sam = {}
        selfidx = w[6]
        if 0 < listp < len(d) - 24 and 0 < nsam <= 8:
            q = listp
            for _ in range(nsam):
                # sampler record = 6 words (24 B): [name][pad][type][1][v2][v2+4]
                # type-13 value block at v2: [1][ptr][255][255][255][255][texIdx]
                sw = struct.unpack_from("<6I", d, q)
                sname = strs.get(sw[0])
                typ = sw[2]
                v2 = sw[4]
                if typ == 13 and 0 < v2 < len(d) - 28:
                    blk = struct.unpack_from("<7I", d, v2)
                    tex = (imgs[blk[6]] if 0 <= blk[6] < len(imgs)
                           else ("UNBOUND" if blk[6] == 255 else f"tex{blk[6]}"))
                    if sname:
                        sam[sname] = tex
                elif typ == 7 and 0 < v2 < len(d) - 28:
                    blk = struct.unpack_from("<4f", d, v2 + 4)
                    if sname:
                        sam[sname] = tuple(round(float(x), 4) for x in blk)
                q += 24
        rows.append(dict(name=name, technique=effect, selfidx=selfidx,
                         DiffuseMap=sam.get("DiffuseMap"),
                         LightMap=sam.get("LightMap"), samplers=sam))
    return rows


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
        rows = decode_runtime(islname)
        print(f"\n===== {islname}: {len(rows)} runtime material records")
        for i, r in enumerate(rows[:6]):
            print(f"  rec{i:3d} {str(r['name'])[:32]:32s} tech={str(r['technique'])[:28]:28s} "
                  f"dif={str(r['DiffuseMap'])[:32]:32s} lm={r['LightMap']}")

        # compare with lib order
        lib = json.load(open(f"{RE}/mat_tex_{islname}.json"))["mats"]
        same_order = sum(1 for a, b in zip(rows, lib) if a["name"] == b["name"])
        selfok = sum(1 for i, a in enumerate(rows) if a["selfidx"] == i)
        print(f"  selfidx == position: {selfok}/{len(rows)}")
        print(f"  runtime vs lib: same name at same index: {same_order}/{len(lib)}")
        dif_same = sum(1 for a, b in zip(rows, lib)
                       if a["name"] == b["name"] and stem(a["DiffuseMap"]) == stem(b["DiffuseMap"]))
        print(f"  same-index DiffuseMap agreement: {dif_same}/{len(lib)}")

        xs = {k: v for k, v in XSECS.items()
              if (isl["isl"] == "1" and ("Island_1" in k or "details" in k))
              or (isl["isl"] == "2" and ("Island_2" in k or "details" in k))}
        # segments + +40 (same filter order as parse_island)
        lt = open(f"{ZONE}/{islname}/lod_table.bin", "rb").read()
        ld = open(f"{ZONE}/{islname}/lod_data.bin", "rb").read()
        u32 = struct.unpack(f"<{len(lt)//4}I", lt)
        n = u32[0]
        pairs = [(u32[1 + 2 * k], u32[2 + 2 * k]) for k in range(n)]
        m40s = []
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
        segs = parse_island(islname)
        assert len(segs) == len(m40s)

        exp = [bind_segment(s, isl, xs)[0] for s in segs]
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
                  f"rt={mm[3][:34]:34s} lm={str(mm[4])[:30]}")
        json.dump(rows, open(f"{RE}/runtime_mats_{islname}.json", "w"), indent=1)


if __name__ == "__main__":
    main()
