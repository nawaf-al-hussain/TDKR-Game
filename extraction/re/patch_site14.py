#!/usr/bin/env python3
"""v14 site patch — skyline placement fix (session 13). Robust version.

lvc evidence (session 13): the 0x14051 LowPolyLongDistance record places
'gc_island1_longdist.bdae' at game pos (-730, -1250, 0), rot 0, scale 1
(ZNCC +0.66 vs street tier). The v13 offset (-141.69, -681.15, 0.114) was
Batman's spawn point ('batman.bdae' 0x2662 record) — wrong by (588.31,
568.85). Island-2 skyline units have NO record in the main level (they
belong to the separate GothamCity_Island2 level) -> removed from the site.
"""
import json
import os
import struct

MODELS = "/home/z/my-project/work/TDKR-Game/gh-pages/models"

OLD = (-141.69, -681.15, 0.114)
NEW = (-730.0, -1250.0, 0.0)
D = (NEW[0] - OLD[0], NEW[2] - OLD[2], -(NEW[1] - OLD[1]))  # game->gltf conv
print(f"delta gltf = {D}")

I1_GLBS = ["GC_island1_LongDist", "GC_LongDist_Island1_FP1",
           "GC_LongDist_Island1_FP2", "GC_LongDist_Island1_FP3",
           "GC_LongDist_Island1_Roads"]
I2_GLBS = ["GC_Island2_LongDist", "GC_LongDist_Island2_FP1",
           "GC_LongDist_Island2_FP2", "GC_LongDist_Island2_FP3",
           "GC_LongDist_Island2_Roads"]


def read_glb(path):
    with open(path, "rb") as f:
        data = f.read()
    clen, ctype = struct.unpack_from("<II", data, 12)
    j = json.loads(data[20:20 + clen])
    bin_off = 20 + clen
    blen, btype = struct.unpack_from("<II", data, bin_off)
    return j, bytearray(data[bin_off + 8:bin_off + 8 + blen])


def write_glb(path, j, binchunk):
    jbin = json.dumps(j, separators=(",", ":")).encode()
    jbin += b" " * ((4 - len(jbin) % 4) % 4)
    binchunk += b"\0" * ((4 - len(binchunk) % 4) % 4)
    total = 12 + 8 + len(jbin) + 8 + len(binchunk)
    with open(path, "wb") as f:
        f.write(struct.pack("<III", 0x46546C67, 2, total))
        f.write(struct.pack("<II", len(jbin), 0x4E4F534A))
        f.write(jbin)
        f.write(struct.pack("<II", len(binchunk), 0x004E4942))
        f.write(binchunk)


def shift_acc(j, bc, ai, delta):
    a = j["accessors"][ai]
    bv = j["bufferViews"][a["bufferView"]]
    base = bv.get("byteOffset", 0) + a.get("byteOffset", 0)
    mn = [1e30] * 3
    mx = [-1e30] * 3
    for k in range(a["count"]):
        o = base + 12 * k
        x, y, z = struct.unpack_from("<3f", bc, o)
        x += delta[0]; y += delta[1]; z += delta[2]
        struct.pack_into("<3f", bc, o, x, y, z)
        for t, v in enumerate((x, y, z)):
            mn[t] = min(mn[t], v); mx[t] = max(mx[t], v)
    a["min"] = [round(v, 4) for v in mn]
    a["max"] = [round(v, 4) for v in mx]


def mesh_name_of(j, node):
    """mesh name for a node (node name or mesh name)."""
    mi = node["mesh"]
    return j["meshes"][mi].get("name") or node.get("name", "")


def find_node(j, name):
    for k, nd in enumerate(j["nodes"]):
        if nd.get("name") == name and "mesh" in nd:
            return k
        if "mesh" in nd and j["meshes"][nd["mesh"]].get("name") == name:
            return k
    return None


# ---------------- 1: island-1 skyline GLBs: shift everything ----------------
for stem in I1_GLBS:
    p = os.path.join(MODELS, stem + ".glb")
    j, bc = read_glb(p)
    n = 0
    for mesh in j["meshes"]:
        for prim in mesh["primitives"]:
            ai = prim["attributes"].get("POSITION")
            if ai is not None:
                shift_acc(j, bc, ai, D)
                n += 1
    write_glb(p, j, bc)
    print(f"{stem}.glb: {n} POSITION accessors shifted by {D}")

# ---------------- 2: city_low.glb ----------------
p = os.path.join(MODELS, "city_low.glb")
j, bc = read_glb(p)

# 2a. shift GC_island1_LongDist_LOW
ni = find_node(j, "GC_island1_LongDist_LOW")
assert ni is not None, "island1_LOW not found"
mi = j["nodes"][ni]["mesh"]
n = 0
for prim in j["meshes"][mi]["primitives"]:
    ai = prim["attributes"].get("POSITION")
    if ai is not None:
        shift_acc(j, bc, ai, D)
        n += 1
print(f"city_low.glb: shifted GC_island1_LongDist_LOW ({n} accessors)")

# 2b. drop GC_Island2_LongDist_LOW (node + mesh + exclusive accessors/views)
ni = find_node(j, "GC_Island2_LongDist_LOW")
if ni is not None:
    drop_mi = j["nodes"][ni]["mesh"]
    accs = set()
    for prim in j["meshes"][drop_mi]["primitives"]:
        accs.update(prim["attributes"].values())
        if "indices" in prim:
            accs.add(prim["indices"])
    others = set()
    for mi2, m2 in enumerate(j["meshes"]):
        if mi2 == drop_mi:
            continue
        for prim in m2["primitives"]:
            others.update(prim["attributes"].values())
            if "indices" in prim:
                others.add(prim["indices"])
    drop_acc = accs - others
    keep_acc = [k for k in range(len(j["accessors"])) if k not in drop_acc]
    acc_map = {old: new for new, old in enumerate(keep_acc)}
    # drop node + mesh
    del j["nodes"][ni]
    j["scenes"][0]["nodes"] = [k if k < ni else k - 1
                               for k in j["scenes"][0]["nodes"] if k != ni]
    del j["meshes"][drop_mi]
    for nd in j["nodes"]:
        if "mesh" in nd and nd["mesh"] > drop_mi:
            nd["mesh"] -= 1
    # remap accessor refs in remaining meshes
    for m2 in j["meshes"]:
        for prim in m2["primitives"]:
            for k in list(prim["attributes"]):
                prim["attributes"][k] = acc_map[prim["attributes"][k]]
            if "indices" in prim:
                prim["indices"] = acc_map[prim["indices"]]
    # drop accessors (keep order), remap bufferViews
    kept_views = set(j["accessors"][k]["bufferView"] for k in keep_acc)
    keep_bv = [k for k in range(len(j["bufferViews"])) if k in kept_views]
    bv_map = {old: new for new, old in enumerate(keep_bv)}
    j["accessors"] = [j["accessors"][k] for k in keep_acc]
    for a in j["accessors"]:
        a["bufferView"] = bv_map[a["bufferView"]]
    j["bufferViews"] = [j["bufferViews"][k] for k in keep_bv]
    print(f"city_low.glb: dropped GC_Island2_LongDist_LOW "
          f"({len(drop_acc)} accessors, {len(keep_bv)} views kept of "
          f"{len(keep_bv) + len(drop_acc - accs) + len(accs & others)})")
write_glb(p, j, bc)

# ---------------- 3: remove island2 skyline GLBs ----------------
for stem in I2_GLBS:
    fp = os.path.join(MODELS, stem + ".glb")
    if os.path.exists(fp):
        os.remove(fp)
        print(f"removed {stem}.glb")

# ---------------- 4: manifest v14 ----------------
mp = os.path.join(MODELS, "manifest.json")
m = json.load(open(mp))
keep = [g for g in m["glbs"]
        if os.path.basename(g["file"])[:-4] not in I2_GLBS]
removed = [os.path.basename(g["file"]) for g in m["glbs"]
           if os.path.basename(g["file"])[:-4] in I2_GLBS]
m["glbs"] = keep
m["total_verts"] = sum(g["verts"] for g in keep)
m["total_tris"] = sum(g["tris"] for g in keep)
m["tiers"] = {}
for g in keep:
    m["tiers"].setdefault(g["tier"], []).append(g["file"])
m["version"] = 14
with open(mp, "w") as f:
    json.dump(m, f, indent=1)
print(f"manifest v14: kept {len(keep)} GLBs, removed {removed}")
print(f"tiers: { {k: len(v) for k, v in m['tiers'].items()} }")
