#!/usr/bin/env python3
"""Session 16 diagnostic: WHERE is the material field, and WHICH order?

Two hypotheses after the agreement failure:
  H1: the material index lives at a different descriptor offset
      -> scan every u32/u16 descriptor offset, compute popA exact
         agreement under library_materials order for each candidate.
  H2: +40 is right but the runtime material enumeration differs
      -> test alternative orderings derived from source.dae itself:
         lib (document order), visual_scenes instance_material order,
         library_effects order, node-order of materials in scenes.

Also: spatial-spread control for the top +40 groups (is purity just
spatial autocorrelation?).
"""
import collections
import json
import struct
import sys
import xml.etree.ElementTree as ET
import zipfile

import numpy as np

sys.path.insert(0, "/home/z/my-project/repo/extraction/scripts")
from export_zone import parse_island, bind_segment, cross_sections, ISLANDS  # noqa

ZONE = "/home/z/my-project/work/zone"
RE = "/home/z/my-project/repo/extraction/re"
NS = {"c": "http://www.collada.org/2005/11/COLLADASchema"}


def descriptors_full(island):
    """Return per-segment (off, 208-byte descriptor head) in parse order."""
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
        out.append(ld[off:off + 208])
    return out


def stem(dm):
    return dm.replace(".tga", "") if dm else None


def alt_orders(island):
    """Material rows from source.dae in several enumerations."""
    z = zipfile.ZipFile(f"{ZONE}/{island}/{island}_materials.bdae")
    print(f"  bdae members: {z.namelist()}")
    root = ET.fromstring(z.read("source.dae"))
    imgs = {}
    for im in root.find("c:library_images", NS).findall("c:image", NS):
        iid = im.get("id")
        init = im.find("c:init_from", NS)
        imgs[iid] = init.text.strip() if init is not None and init.text else ""
    lib_m = root.find("c:library_materials", NS)

    def samplers(m):
        inst = m.find("c:instance_effect", NS)
        sam = {}
        if inst is not None:
            surf = {}
            for sp in inst.findall("c:setparam", NS):
                sf = sp.find("c:surface/c:init_from", NS)
                if sf is not None and sf.text:
                    surf[sp.get("ref")] = imgs.get(sf.text.strip(), sf.text.strip())
            for sp in inst.findall("c:setparam", NS):
                s2 = sp.find("c:sampler2D/c:source", NS)
                if s2 is not None and s2.text and s2.text.strip() in surf:
                    sam[sp.get("ref")] = surf[s2.text.strip()]
        return sam

    lib = []
    for m in lib_m.findall("c:material", NS):
        sam = samplers(m)
        lib.append(dict(name=m.get("id"),
                        DiffuseMap=sam.get("DiffuseMap"),
                        LightMap=sam.get("LightMap")))
    orders = {"lib": list(lib)}

    # instance_material order in library_visual_scenes
    seq = []
    vs = root.find("c:library_visual_scenes", NS)
    if vs is not None:
        for im in vs.iter("{http://www.collada.org/2005/11/COLLADASchema}instance_material"):
            tgt = (im.get("target") or "").lstrip("#")
            seq.append(tgt)
    by_name = {m["name"]: m for m in lib}
    o = [by_name[t] for t in seq if t in by_name]
    print(f"  instance_material seq: {len(seq)} refs, {len(o)} matched")
    orders["vis_scene"] = o if len(o) == len(lib) else None

    # library_effects order -> materials whose effect appears there
    eff_seq = []
    lib_e = root.find("c:library_effects", NS)
    if lib_e is not None:
        for e in lib_e.findall("c:effect", NS):
            eff_seq.append(e.get("id"))
    # map material -> its effect url
    m2e = {}
    for m in lib_m.findall("c:material", NS):
        inst = m.find("c:instance_effect", NS)
        if inst is not None:
            m2e[m.get("id")] = (inst.get("url") or "").lstrip("#")
    eff_order_mats = []
    for e in eff_seq:
        for m in lib:
            if m2e.get(m["name"]) == e:
                eff_order_mats.append(m)
    print(f"  effect-order seq: {len(eff_seq)} effects, {len(eff_order_mats)} matched")
    orders["effect"] = eff_order_mats if len(eff_order_mats) == len(lib) else None

    # scene node order (all materials referenced in node instance_materials
    # is the same as vis_scene; add node-attribute order fallback)
    return orders, lib


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
        M = len(mats)
        segs = parse_island(islname)
        descs = descriptors_full(islname)
        exp = []
        for s in segs:
            tex, mode = bind_segment(s, isl, xs)
            exp.append(tex)

        print(f"\n===== {islname} N={len(segs)} M={M}")

        # ---- H1: offset scan under lib order
        hits = []
        for off in range(0, 208, 4):
            vals = [struct.unpack_from("<I", d, off)[0] for d in descs]
            distinct = len(set(vals))
            if not (8 < distinct and max(vals) < M):
                continue
            ok = tot = 0
            for t, v in zip(exp, vals):
                d = stem(mats[v].get("DiffuseMap"))
                if t is None or d is None:
                    continue
                tot += 1
                ok += (t == d)
            if tot > 50:
                hits.append((off, distinct, max(vals), ok, tot,
                             100.0 * ok / tot))
        print("H1 u32 offset scan (distinct>8, max<M), by agreement:")
        for h in sorted(hits, key=lambda x: -x[5])[:10]:
            print(f"  +{h[0]:3d}: distinct={h[1]:4d} max={h[2]:4d} "
                  f"exact {h[3]}/{h[4]} = {h[5]:.2f}%")

        # u16 scan
        hits16 = []
        for off in range(0, 208, 2):
            vals = [struct.unpack_from("<H", d, off)[0] for d in descs]
            distinct = len(set(vals))
            if not (8 < distinct and max(vals) < M):
                continue
            ok = tot = 0
            for t, v in zip(exp, vals):
                d = stem(mats[v].get("DiffuseMap"))
                if t is None or d is None:
                    continue
                tot += 1
                ok += (t == d)
            if tot > 50:
                hits16.append((off, distinct, max(vals), ok, tot,
                               100.0 * ok / tot))
        print("H1 u16 offset scan, by agreement (top):")
        for h in sorted(hits16, key=lambda x: -x[5])[:10]:
            print(f"  +{h[0]:3d}: distinct={h[1]:4d} max={h[2]:4d} "
                  f"exact {h[3]}/{h[4]} = {h[5]:.2f}%")

        # ---- H2: alternative orderings at +40
        orders, lib = alt_orders(islname)
        for name, order in orders.items():
            if order is None:
                print(f"H2 order {name}: unavailable (length mismatch)")
                continue
            ok = tot = 0
            for d, t in zip(descs, exp):
                v = struct.unpack_from("<I", d, 40)[0]
                if v >= len(order):
                    continue
                dm = stem(order[v].get("DiffuseMap"))
                if t is None or dm is None:
                    continue
                tot += 1
                ok += (t == dm)
            print(f"H2 order {name:10s}: exact {ok}/{tot} = "
                  f"{100.0*ok/max(tot,1):.2f}%")

        # ---- spatial control: centroid spread of top +40 groups
        cents = collections.defaultdict(list)
        for d, s in zip(descs, segs):
            v = struct.unpack_from("<I", d, 40)[0]
            cents[v].append(s["pos"][:, :2].mean(0))
        print("spatial spread of top groups (bbox diag, u):")
        for v in (11, 74, 13, 299, 178, 90, 6, 5, 82, 194, 153):
            if v not in cents:
                continue
            pts = np.array(cents[v])
            diag = float(np.linalg.norm(pts.max(0) - pts.min(0)))
            print(f"  +40={v:3d} n={len(pts):4d} spread={diag:8.1f}")


if __name__ == "__main__":
    main()
