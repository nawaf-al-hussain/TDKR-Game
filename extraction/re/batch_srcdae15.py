#!/usr/bin/env python3
"""Parse mat/source.dae library_materials -> per-index material DB, then
cross-reference batch_info record fields against it.

Outputs (per island):
  - material index -> {name, technique, diffuse texIdx, lightmap texIdx,
                       scaleoffset vec4, ntextures}
  - which batch_info field groups light up for which material subsets
  - value-set comparison: do the <=28 u16s match texIdx space? do the f32
    groups match scaleoffset components?
"""
import json
import struct
import sys
import xml.etree.ElementTree as ET
import zipfile

ZONE = "/home/z/my-project/work/zone"
NS = {"c": "http://www.collada.org/2005/11/COLLADASchema"}


def load_source_dae(island):
    z = zipfile.ZipFile(f"{ZONE}/{island}/{island}_materials.bdae")
    xml = z.read("source.dae")
    return ET.fromstring(xml)


def parse_materials(root):
    """ordered library_materials + effect params."""
    mats = []
    lib_m = root.find("c:library_materials", NS)
    effs = {}
    lib_e = root.find("c:library_effects", NS)
    if lib_e is not None:
        for e in lib_e.findall("c:effect", NS):
            eid = e.get("id")
            effs[eid] = e
    for m in lib_m.findall("c:material", NS):
        inst = m.find("c:instance_effect", NS)
        eff = effs.get(inst.get("url", "#").lstrip("#")) if inst is not None else None
        info = {"name": m.get("id"), "technique": None,
                "samplers": {}, "floats": {}, "ints": {}}
        if eff is not None:
            # technique profile name
            for prof in eff:
                tag = prof.tag.split('}')[-1]
                if "profile" in tag.lower():
                    tech = prof.find("c:technique", NS)
                    if tech is not None:
                        info["technique"] = tech.get("sid") or tech.get("id")
                    # setparam chain
                    for sp in prof.findall("c:technique/c:setparam", NS) + prof.findall("c:setparam", NS):
                        ref = sp.get("ref")
                        sam = sp.find("c:sampler2D", NS)
                        if sam is not None:
                            inst_from = sam.find("c:instance_image", NS)
                            info["samplers"][ref] = {"image": inst_from.get("url", "").lstrip("#") if inst_from is not None else None}
                            continue
                        fl = sp.find("c:float2", NS)
                        if fl is not None:
                            info["floats"][ref] = [float(x) for x in fl.text.split()]
                        fl1 = sp.find("c:float", NS)
                        if fl1 is not None:
                            info["floats"][ref] = float(fl1.text)
                        it = sp.find("c:int", NS)
                        if it is not None:
                            info["ints"][ref] = int(it.text)
        mats.append(info)
    return mats


def main():
    for island, M in [("GothamCity", 307), ("GothamCity_Island2", 196)]:
        root = load_source_dae(island)
        mats = parse_materials(root)
        print(f"\n########## {island}: {len(mats)} materials from source.dae ##########")
        # techniques histogram
        techs = {}
        for m in mats:
            techs[m["technique"]] = techs.get(m["technique"], 0) + 1
        print("techniques:", techs)
        # sampler name histogram
        samnames = {}
        for m in mats:
            for s in m["samplers"]:
                samnames[s] = samnames.get(s, 0) + 1
        print("sampler param names:", samnames)
        # float param names
        flnames = {}
        for m in mats:
            for s in m["floats"]:
                flnames[s] = flnames.get(s, 0) + 1
        print("float param names:", flnames)
        # sample a few
        for i in (0, 2, 6):
            if i < len(mats):
                print(f" mat{i}:", json.dumps(mats[i])[:400])

        # ---- batch_info cross-ref ----
        d = open(f"{ZONE}/{island}/batch_info.bin", "rb").read()
        body = d[4:]
        recs = [body[m * 197:(m + 1) * 197] for m in range(M)]

        # per-material interesting fields
        rows = []
        for m, r in enumerate(recs):
            info = mats[m] if m < len(mats) else {}
            # field extraction from the byte map established in batch_words15
            w = struct.unpack("<49I", r[1:])
            f = {
                "idx": m,
                "name": info.get("name", "?")[:44],
                "tech": (info.get("technique") or "")[:22],
                "nsam": len(info.get("samplers", {})),
                "b3": r[3], "b4": r[4],
                "b17": r[17], "b18": r[18], "b19": r[19],
                "w8": w[8], "w11": w[11] & 0xFFFF, "w11b": w[11] >> 16,
                "w12": w[12], "w13": w[13], "w16": w[16], "w17": w[17] >> 16,
                "w18": w[18], "w19": w[19], "w20": w[20] >> 16,
                "w25": w[25], "w26": w[26],
                "a": struct.unpack_from("<2f", r, 109),
                "b": struct.unpack_from("<2f", r, 121),
                "c": struct.unpack_from("<2f", r, 133),
                "dd": struct.unpack_from("<2f", r, 145),
                "w40": w[40], "w41": w[41],
            }
            rows.append(f)

        # how many have float groups
        nz = lambda t: sum(1 for r in rows if any(abs(x) > 1e-12 for x in r[t]))
        print(f"\nfloat groups: a={nz('a')} b={nz('b')} c={nz('c')} d={nz('dd')}")
        # techniques vs float presence
        have_b = {r["idx"] for r in rows if any(abs(x) > 1e-12 for x in r["b"])}
        tech_of = {i: (mats[i]["technique"] if i < len(mats) else None) for i in range(M)}
        cnt = {}
        for i in have_b:
            cnt[tech_of.get(i)] = cnt.get(tech_of.get(i), 0) + 1
        print("materials WITH b-group by technique:", cnt)
        cnt0 = {}
        for i in range(M):
            if i not in have_b:
                cnt0[tech_of.get(i)] = cnt0.get(tech_of.get(i), 0) + 1
        print("materials WITHOUT b-group by technique:", cnt0)

        # compare b-group to sampler scaleoffsets from source.dae
        def so_set(mats):
            vals = set()
            for mm in mats:
                for s, sd in mm["floats"].items():
                    if isinstance(sd, list) and len(sd) == 2:
                        vals.add((round(sd[0], 5), round(sd[1], 5)))
            return vals
        sv = so_set(mats)
        print("source.dae float2 param value set (size):", len(sv))
        bvals = {(round(r["b"][0], 5), round(r["b"][1], 5)) for r in rows
                 if any(abs(x) > 1e-12 for x in r["b"])}
        print("batch_info b-group value set (size):", len(bvals))
        inter = sv & bvals
        print("intersection:", len(inter), list(inter)[:10])

        # save the joined table for the record
        out = [dict(r, a=list(r["a"]), b=list(r["b"]), c=list(r["c"]), dd=list(r["dd"]))
               for r in rows]
        json.dump(out, open(f"batch_xref_{island}.json", "w"), indent=1)
        print(f"saved batch_xref_{island}.json")


if __name__ == "__main__":
    main()
