#!/usr/bin/env python3
"""Scan GothamCity.lvc for CTemplateBakeGroup (typeId 0x140869f) and
CTemplateZone (0x2667) records. Walk CLevel::LoadNextObject's dispatch:
  0x2657 CTemplateLevelProperties  0x2667 CTemplateZone
  0x140869f CTemplateBakeGroup     0x1011 ?  0x2653 ?  0x2669 ?
  0x2661 ?  0x2662/0x2664 ?  0x1404050/51 ?  0xd0bbb8 ?  0x265f metazone
Evidence: CLevel::LoadNextObject @0x489ecc (libKRHP.so real addrs):
  cmp r5,0x140869f -> beq 0x48aea0 -> bl CTemplateBakeGroup::Load (0x48d870)
  cmp r5,0x2667    -> bl CTemplateZone::Load (0x48d5f4) -> CZone::Create
Stream primitives are BIG-ENDIAN; strings are interned charTable[idx].
CTemplateBakeGroup::Load layout:
  bool@4, int@8, 9*float@c..2c, bool@30,31,32, string@38, float@3c,
  string@40, float@44
CTemplateZone::Load layout:
  bool@4, string@8, int@c, bool@14, int@18, 9*float@1c..3c, bool@40,41,42
"""
import struct, sys, json, os

PATH = sys.argv[1] if len(sys.argv) > 1 else \
    "/home/z/my-project/download/TDKR_assets/raw/game_config/GothamCity.lvc"
d = open(PATH, "rb").read()
assert d[0:4] == b"DICT"
tbl_off = struct.unpack_from(">I", d, 4)[0]
flag = d[8]
assert flag == 0
# string table
p = tbl_off
count = struct.unpack_from(">I", d, p)[0]
p += 4
strings = []
for _ in range(count):
    ln = struct.unpack_from(">I", d, p)[0]
    p += 4
    strings.append(d[p:p + ln].decode("utf-8", "replace"))
    p += ln


def s32(idx):
    return strings[idx] if 0 <= idx < len(strings) else f"<bad {idx}>"


def u32(o):
    return struct.unpack_from(">I", d, o)[0]


def f32(o):
    return struct.unpack_from(">f", d, o)[0]


# typeId candidates from LoadNextObject dispatch
TYPEIDS = {
    0x2657: "CTemplateLevelProperties",
    0x2667: "CTemplateZone",
    0x140869f: "CTemplateBakeGroup",
    0x1011: "?0x1011",
    0x2653: "?0x2653",
    0x2669: "?0x2669",
    0x2661: "?0x2661",
    0x2662: "?0x2662",
    0x2664: "?0x2664",
    0x1404050: "?0x1404050",
    0x1404051: "?0x1404051",
    0xd0bbb8: "?0xd0bbb8",
    0x798f: "?0x798f",
    0x265f: "CTemplateMetaZone",
}
print(f"strings: {len(strings)}")

# scan for records: bytes BE of typeId
hits = {}
for tid, name in TYPEIDS.items():
    pat = struct.pack(">I", tid)
    i = 0
    while True:
        i = d.find(pat, i)
        if i < 0:
            break
        hits.setdefault(i, []).append((tid, name))
        i += 1

print(f"total candidate offsets: {len(hits)}")
by_name = {}
for off, tids in sorted(hits.items()):
    for tid, name in tids:
        by_name.setdefault(name, []).append(off)
for name, offs in sorted(by_name.items()):
    print(f"  {name:28s} x{len(offs):5d}  first@{offs[0]:#x} last@{offs[-1]:#x}")

# ---- parse CTemplateBakeGroup records ----
print("\n=========== CTemplateBakeGroup records ===========")
bakes = []
for off in by_name.get("CTemplateBakeGroup", []):
    p = off + 4
    try:
        b_en = d[p]; p += 1
        i_id = u32(p); p += 4
        fl = [f32(p + k * 4) for k in range(9)]; p += 36
        b3 = [d[p], d[p + 1], d[p + 2]]; p += 3
        # align: Load reads strings immediately (no alignment in stream)
        s0 = s32(u32(p)); p += 4
        f3c = f32(p); p += 4
        s1 = s32(u32(p)); p += 4
        f44 = f32(p); p += 4
    except Exception as e:
        print(f"@{off:#x} parse error {e}")
        continue
    bakes.append({
        "off": off, "enable": b_en, "id": i_id, "floats": fl, "bools": b3,
        "str0": s0, "f3c": f3c, "str1": s1, "f44": f44,
    })
    print(f"@{off:#08x} en={b_en} id={i_id:#x} fl={['%.6g' % v for v in fl]} "
          f"b={b3} str0={s0!r} f3c={f3c:.6g} str1={s1!r} f44={f44:.6g}")

# ---- parse CTemplateZone records ----
print("\n=========== CTemplateZone records ===========")
zones = []
for off in by_name.get("CTemplateZone", []):
    p = off + 4
    try:
        b_en = d[p]; p += 1
        name = s32(u32(p)); p += 4
        i0 = u32(p); p += 4
        b1 = d[p]; p += 1
        zid = u32(p); p += 4
        fl = [f32(p + k * 4) for k in range(9)]; p += 36
        b40, b41, b42 = d[p], d[p + 1], d[p + 2]; p += 3
    except Exception as e:
        print(f"@{off:#x} parse error {e}")
        continue
    zones.append({
        "off": off, "enable": b_en, "name": name, "i0": i0, "id": zid,
        "floats": fl, "bools": [b40, b41, b42],
    })
    print(f"@{off:#08x} en={b_en} name={name!r} i0={i0:#x} id={zid:#x} "
          f"fl={['%.6g' % v for v in fl]} b={[b40, b41, b42]}")

# ---- cross-ref with .index.bin ----
idxp = os.path.join(os.path.dirname(PATH), "GothamCity.index")
if os.path.exists(idxp):
    idx = open(idxp, "rb").read()
    n = struct.unpack_from("<I", idx, 0)[0]
    keys = [struct.unpack_from(">I", idx, 4 + k * 13)[0] for k in range(n)]
    print(f"\n.index.bin keys ({n}): {[hex(k) for k in keys]}")
    zids = {z["id"] for z in zones}
    print("all keys match CTemplateZone ids?", set(keys) <= zids,
          f"({len(set(keys) & zids)}/{len(keys)})")

out = {"bakeGroups": bakes, "zones": zones,
       "strings": len(strings)}
json.dump(out, open("/home/z/my-project/work/TDKR-Game/extraction/re/lvc_bakegroups.json", "w"),
          indent=1)
print("\nsaved extraction/re/lvc_bakegroups.json")
