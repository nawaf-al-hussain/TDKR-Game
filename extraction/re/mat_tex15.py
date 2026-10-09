#!/usr/bin/env python3
"""Task 3 support: material index -> texture names from source.dae;
identify road/grass material indices for both islands.
"""
import re
import xml.etree.ElementTree as ET
import zipfile

ZONE = "/home/z/my-project/work/zone"
NS = {"c": "http://www.collada.org/2005/11/COLLADASchema"}

ROAD_PAT = re.compile(r"road|asphalt|street|grass|sidewalk|pavement|crosswalk|ground", re.I)


def material_table(island):
    z = zipfile.ZipFile(f"{ZONE}/{island}/{island}_materials.bdae")
    root = ET.fromstring(z.read("source.dae"))
    imgs = {}
    lib_i = root.find("c:library_images", NS)
    if lib_i is not None:
        for im in lib_i.findall("c:image", NS):
            iid = im.get("id")
            init = im.find("c:init_from", NS)
            imgs[iid] = init.text.strip() if init is not None and init.text else ""
    mats = []
    lib_m = root.find("c:library_materials", NS)
    for m in lib_m.findall("c:material", NS):
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
        mats.append({"name": m.get("id"),
                     "DiffuseMap": sam.get("DiffuseMap"),
                     "LightMap": sam.get("LightMap"),
                     "textures": list(sam.values())})
    return mats


def main():
    import json as _json
    import re as _re
    for island in ("GothamCity", "GothamCity_Island2"):
        mats = material_table(island)
        print(f"\n===== {island}: {len(mats)} materials =====")
        pat = _re.compile(r"road|crossing", re.I)
        road = []
        for i, m in enumerate(mats):
            dm = m.get("DiffuseMap") or ""
            if dm and pat.search(dm):
                road.append(i)
        print(f"DiffuseMap-road materials ({len(road)}): {road[:30]}")
        for i in road[:12]:
            m = mats[i]
            print(f"  m{i:3d} {m['name'][:44]:44s} dif={m['DiffuseMap']} "
                  f"lm={m['LightMap']}")
        _json.dump({"mats": mats, "road_idx": road},
                   open(f"/home/z/my-project/work/TDKR-Game/extraction/re/mat_tex_{island}.json", "w"))


if __name__ == "__main__":
    main()
