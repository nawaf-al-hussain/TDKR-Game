#!/usr/bin/env python3
"""Definitive sequential parser for GothamCity.lvc / GothamCity_Island2.lvc
DICT object streams — read orders taken from the disassembled Load functions:

  0x2667 CTemplateZone::Load      bool, string, float, bool, int, 9f, 3b
  0x265f CTemplateMetaZone::Load  4b?, 3int, 9f, 1 string (per read_counts:
                                  char x4, int x3, float x9, string x1)
  0x1869f CTemplateBakeGroup::Load bool, int, 9f, 3b, string, f, string, f
  0x2662 CSpawnPointObject::Create bool, int, 9f, 3b, string, string, 3b, int
  0x14050 / 0x14051 component records:
                                   CComponentBase::Load (bool,int,9f,3b) +
                                   CComponentMesh::Load (string, 4 chars)
  0x2663                           int, 9f                (marker object)
  0x2664                           int                    (ref marker)
  others                          -> resync: scan for the next offset where
                                     bytes look like a typeId we know.
"""
import json
import struct
import sys

PATH = sys.argv[1] if len(sys.argv) > 1 else \
    "/home/z/my-project/download/TDKR_assets/raw/game_config/GothamCity.lvc"
OUTJSON = sys.argv[2] if len(sys.argv) > 2 else \
    "/home/z/my-project/work/valout/lvc_records.json"

d = open(PATH, "rb").read()
tbl = struct.unpack_from(">I", d, 4)[0]
pos = tbl
n = struct.unpack_from(">i", d, pos)[0]
pos += 4
strings = []
for i in range(n):
    ln = struct.unpack_from(">i", d, pos)[0]
    pos += 4
    strings.append(d[pos:pos + ln].decode("utf-8", "replace"))
    pos += ln
NS = len(strings)


class Cur:
    def __init__(self, p):
        self.p = p

    def b(self):
        v = d[self.p]; self.p += 1; return v

    def i(self):
        v = struct.unpack_from(">i", d, self.p)[0]; self.p += 4; return v

    def f(self):
        v = struct.unpack_from(">f", d, self.p)[0]; self.p += 4; return v

    def s(self):
        v = self.i()
        return strings[v] if 0 <= v < NS else f"<str {v}>"

    def raw(self, k):
        v = d[self.p:self.p + k]; self.p += k; return v


def known_typeid(v):
    return v in (0x2657, 0x2667, 0x265f, 0x1869f, 0x2662, 0x2663, 0x2664,
                 0x14050, 0x14051, 0xd0bbb8, 0x265e, 0x2653, 0x1011, 0x2669,
                 0x267d, 0x14050, 0xbba, 0x4741, 0x798f, 0x2666, 0x2654)


def parse_payload(c, tid):
    r = {"typeId": tid, "off": c.p - 4}
    if tid == 0x2667:      # zone
        r["bool"] = c.b(); r["name"] = c.s(); r["f"] = c.f()
        r["bool2"] = c.b(); r["zoneId"] = c.i()
        r["trs"] = [c.f() for _ in range(9)]
        r["bools"] = [c.b() for _ in range(3)]
    elif tid == 0x1869f:   # bake group template
        r["bool"] = c.b(); r["int"] = c.i()
        r["trs"] = [c.f() for _ in range(9)]
        r["bools"] = [c.b() for _ in range(3)]
        r["page1"] = c.s(); r["f1"] = c.f()
        r["page2"] = c.s(); r["f2"] = c.f()
    elif tid in (0x2662,):  # spawn point object
        r["bool"] = c.b(); r["objId"] = c.i()
        r["trs"] = [c.f() for _ in range(9)]
        r["bools"] = [c.b() for _ in range(3)]
        r["str1"] = c.s(); r["str2"] = c.s()
        r["bools2"] = [c.b() for _ in range(3)]
        r["int2"] = c.i()
    elif tid in (0x14050, 0x14051):  # component mesh records
        r["bool"] = c.b(); r["objId"] = c.i()
        r["trs"] = [c.f() for _ in range(9)]
        r["bools"] = [c.b() for _ in range(3)]
        r["mesh"] = c.s()
        r["chars"] = c.raw(4).hex()
    elif tid == 0x2663:
        r["objId"] = c.i()
        r["trs"] = [c.f() for _ in range(9)]
    elif tid == 0x2664:
        r["int"] = c.i()
    elif tid == 0x265f:    # meta zone (approx per read_counts)
        r["bools"] = [c.b() for _ in range(4)]
        r["ints"] = [c.i() for _ in range(3)]
        r["trs"] = [c.f() for _ in range(9)]
        r["str"] = c.s()
    else:
        return None
    return r


def resync(p):
    """find the next plausible record start: a known typeId preceded by a
    valid-looking previous-record boundary. We simply scan forward for the
    next occurrence of any known typeId u32 and resume there."""
    q = p
    while q < tbl - 4:
        v = struct.unpack_from(">I", d, q)[0]
        if known_typeid(v) and v != 0x2664:   # 0x2664 too common (=-1?)
            return q, v
        q += 1
    return None, None


records = []
c = Cur(9)
h1 = c.i() & 0xffff
h2 = c.i() & 0xffff
objcount = c.i()
tid0 = c.i()
print(f"{PATH.split('/')[-1]}: header shorts={h1:#x},{h2} objcount={objcount} "
      f"first typeId={tid0:#x}")
rec = parse_payload(Cur(c.p - 4 + 4), tid0)  # payload after typeId already?? no:
# NOTE: for the first record (level properties) we reuse parse_lvc.py's known
# walk instead of guessing: it ends after the 'final int (+0x128)'.
# Simpler: level-props size was established in session 3; resync from a scan.

# --- walk ---
c = Cur(c.p)   # inside first payload; resync will jump past it
resyncs = 0
types = {}
while c.p < tbl - 8:
    start = c.p
    tid = c.i()
    if not known_typeid(tid):
        q, v = resync(start)
        if q is None:
            break
        resyncs += 1
        c = Cur(q)
        continue
    save = c.p
    try:
        r = parse_payload(c, tid)
    except Exception:
        r = None
    if r is None or c.p > tbl:
        q, v = resync(start + 1)
        if q is None:
            break
        resyncs += 1
        c = Cur(q)
        continue
    # sanity: TRS values sane?
    trs = r.get("trs")
    if trs and not all(abs(v) < 1e7 for v in trs):
        q, v = resync(start + 1)
        if q is None:
            break
        resyncs += 1
        c = Cur(q)
        continue
    types[hex(tid)] = types.get(hex(tid), 0) + 1
    records.append(r)

print(f"parsed {len(records)} records, {resyncs} resyncs")
print("type distribution:", types)
# coverage
cov = tbl - 9
print(f"stream size {cov}, coverage rough")

json.dump(dict(strings_count=NS, records=records),
          open(OUTJSON, "w"), indent=1)
print(f"saved {OUTJSON}")

# ---- focused report ----
print("\n== 0x14051 / 0x14050 records ==")
for r in records:
    if r["typeId"] in (0x14050, 0x14051):
        t = r.get("trs")
        print(f"  {r['typeId']:#x} @{r['off']:#x} objId={r.get('objId')} "
              f"TRS={[round(v,3) for v in t]} mesh={r.get('mesh')!r} "
              f"chars={r.get('chars')}")
print("\n== 0x1869f bakegroup records ==")
for r in records:
    if r["typeId"] == 0x1869f:
        t = r.get("trs")
        print(f"  @{r['off']:#x} int={r.get('int')} TRS={[round(v,3) for v in t]}"
              f" p1={r.get('page1')!r} p2={r.get('page2')!r}")
print("\n== zone records (name, zoneId, TRS pos) ==")
for r in records:
    if r["typeId"] == 0x2667:
        t = r.get("trs")
        nm = r.get("name", "")
        if len(nm) > 40:
            nm = nm[:37] + "..."
        print(f"  @{r['off']:#x} zoneId={r.get('zoneId')} name={nm!r} "
              f"pos={[round(v,2) for v in t[:3]]}")
