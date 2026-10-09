#!/usr/bin/env python3
"""Cross-reference batch_info record fields vs material properties.

Questions:
 A. Which material indices carry each field group (w0, w4, w8, w11-17 u16s,
    w18-20, w21-26, w27-28 f32, w30-31 f32, w33-34 f32, w36-37 f32,
    w39-41, w43-44)?  What do those materials have in common?
 B. Do the small u16 values (<=28) match texture indices / sizes from the
    zone material DB?
 C. Do the f32 groups match bake_regions so1 scale/offset values?
"""
import json
import re
import struct
import collections

ZONE = "/home/z/my-project/work/zone"
RE = "/home/z/my-project/work/TDKR-Game/extraction/re"

GROUPS = {
    "w0": (1, 4),      # rec byte range (start,end) — payload word w covers rec bytes 1+4w..4+4w
    "w4": (17, 20),
    "w8": (33, 36),
    "w11_17": (45, 72),   # the 3,20,12,16,3,20,16,17,1,4,20 block
    "w18_20": (73, 84),
    "w21_26": (85, 108),
    "w27_28": (109, 116),  # 8B float group 1
    "w30_31": (121, 128),  # 8B float group 2
    "w33_34": (133, 140),  # 8B float group 3
    "w36_37": (145, 152),  # 8B float group 4
    "w39_41": (157, 168),
    "w43_44": (173, 180),
    "w47_48": (189, 196),
}


def load_names():
    names = {}
    isl = None
    for ln in open(f"{RE}/batch_info_material_names14.txt"):
        m = re.match(r"# (GothamCity\S*) —", ln)
        if m:
            isl = m.group(1)
            names[isl] = []
            continue
        m = re.match(r"\s*(\d+)\s+(\S.*)", ln)
        if m and isl:
            names[isl].append(m.group(2).strip())
    return names


def main():
    names = load_names()
    mats_db = json.load(open(f"{ZONE}/zone_materials_GothamCity.json"))
    mats2_db = json.load(open(f"{ZONE}/zone_materials_GothamCity_Island2.json"))

    for island, M in [("GothamCity", 307), ("GothamCity_Island2", 196)]:
        d = open(f"{ZONE}/{island}/batch_info.bin", "rb").read()
        body = d[4:]
        recs = [body[m * 197:(m + 1) * 197] for m in range(M)]
        db = mats_db if island == "GothamCity" else mats2_db
        texinfo = db["material_textures"]
        images = db["images"]

        print(f"\n########## {island}  M={M} ##########")
        # A. which records have each group non-(-1,0)?
        for g, (a, b) in GROUPS.items():
            hits = []
            for m, r in enumerate(recs):
                chunk = r[a:b + 1]
                if any(x not in (0x00, 0xFF) for x in chunk):
                    hits.append(m)
            if hits:
                print(f"\n group {g} (rec bytes {a}..{b}): {len(hits)} records: {hits[:40]}")
                for m in hits[:6]:
                    nm = names[island][m] if m < len(names[island]) else "?"
                    ti = texinfo.get(nm, {})
                    print(f"   m={m:3d} {nm[:52]:52s} tex={json.dumps(ti)[:150]}")

        # B. u16 array decode for a record with w11_17 set
        for m, r in enumerate(recs):
            chunk = r[45:73]
            if any(x not in (0x00, 0xFF) for x in chunk):
                nm = names[island][m]
                print(f"\n u16-decode rec {m} ({nm[:40]}): bytes45-72:")
                u16s = struct.unpack("<14H", chunk)
                print("   LE u16:", u16s)
                u16b = struct.unpack(">14H", r[45:73])
                print("   BE u16:", u16b)
                print("   bytes:", chunk.hex(" "))
                ti = texinfo.get(nm, {})
                print("   material_textures:", json.dumps(ti)[:400])
                break

        # C. f32 groups vs bake_regions so1
        try:
            br = json.load(open(f"{RE}/bake_regions.json"))
            frames = br if isinstance(br, list) else br.get("frames", [])
            so1s = set()
            for f in frames:
                so = f.get("so1") or f.get("scale_offset")
                if so:
                    so1s.add(tuple(round(x, 5) for x in so))
            print(f"\n bake_regions so1 set size: {len(so1s)}; sample: {list(so1s)[:4]}")
        except Exception as e:
            print("bake_regions load failed:", e)


if __name__ == "__main__":
    main()
