#!/usr/bin/env python3
"""GothamCity.lvc — authoritative record scan (session 13).

Goals (external-Claude review):
  T2  adjudicate -140.7 vs -141.69 for gc_island1_longdist.bdae
  T7  find hero-unit records (bridges/monorail/railway/water) in the stream
  +   capture EVERY name reference with raw hexdump context for the handoff
"""
import json
import re
import struct
import sys
from collections import Counter

PATH = "/home/z/my-project/download/TDKR_assets/raw/game_config/GothamCity.lvc"
OUT = "/home/z/my-project/work/valout"
d = open(PATH, "rb").read()
print(f"file size {len(d):,}")

# ---------------- header + string table ----------------
assert d[:4] == b"DICT"
tbl_off = struct.unpack_from(">I", d, 4)[0]
flag = d[8]
print(f"magic DICT  tblOff={tbl_off:#x}  wideflag={flag}")
pos = tbl_off
count = struct.unpack_from(">i", d, pos)[0]
pos += 4
strings = []
for i in range(count):
    ln = struct.unpack_from(">i", d, pos)[0]
    pos += 4
    strings.append(d[pos:pos + ln].decode("utf-8", "replace"))
    pos += ln
print(f"strings: {count}  table ends {pos:#x}")
print(f"first 12: {strings[:12]}")
print(f"last 5: {strings[-5:]}")

idx_of = {}
for i, s in enumerate(strings):
    idx_of.setdefault(s, i)

INTEREST = re.compile(
    r"(?i)(island|longdist|bridge|monorail|railway|water|footprint|stadium"
    r"|batcave|citybg|props)")
want = {}
for i, s in enumerate(strings):
    if INTEREST.search(s):
        want.setdefault(s, []).append(i)

# ---------------- stream scan: references to name indices ----------------
# every BE u32 equal to a wanted string index, anywhere before tbl_off
ref_map = {}
for s, idxs in want.items():
    for si in idxs:
        pat = struct.pack(">I", si)
        start = 0
        while True:
            j = d.find(pat, start, tbl_off)
            if j < 0:
                break
            ref_map.setdefault(j, []).append((si, s))
            start = j + 1

# dedupe: refs at j and j+4 pointing to the same string = same ref noise;
# keep all, hexdump decides.
print(f"\n{len(ref_map)} raw u32-hit offsets for {len(want)} wanted strings")

# context decode helper
def f32be(off):
    return struct.unpack_from(">f", d, off)[0]

def i32be(off):
    return struct.unpack_from(">i", d, off)[0]

def hexdump(off, n=160):
    rows = []
    for a in range(off, min(off + n, len(d)), 16):
        chunk = d[a:a + 16]
        hx = " ".join(f"{b:02x}" for b in chunk)
        asc = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        rows.append(f"  {a:08x}  {hx:<47}  {asc}")
    return "\n".join(rows)

# ---------------- per-name report ----------------
report = {}
FOCUS = ["gc_island1_longdist.bdae", "gc_island2_longdist.bdae",
         "GC_island1_LongDist", "GC_island2_LongDist",
         "gc_bigbridge.bdae", "gc_small_bridge_island2.bdae",
         "gc_monorail_island1.bdae", "gc_monorail_island2.bdae",
         "gc_railway_island2.bdae", "gc_water.bdae", "gc_water_island2.bdae"]
for s in sorted(want):
    hits = sorted(j for j, lst in ref_map.items() if any(x[0] in want[s] for x in lst))
    # filter: hits that are part of the string table area are irrelevant
    hits = [j for j in hits if j < tbl_off - 16]
    if not hits:
        continue
    report[s] = hits
    tag = " <FOCUS>" if any(s.lower() == f.lower() for f in FOCUS) else ""
    print(f"\n=== {s!r} idx={want[s]}  {len(hits)} stream refs{tag}")
    for j in hits[:6]:
        nxt = d[j + 4:j + 6].hex()
        tid = struct.unpack_from(">I", d, j + 8)[0] if j + 12 <= len(d) else 0
        print(f"  @{j:#x}: next2={nxt}  u32@+8={tid:#x}")

json.dump({s: v for s, v in report.items()},
          open(f"{OUT}/lvc_name_refs.json", "w"), indent=1)

# ---------------- FOCUS deep dive ----------------
print("\n" + "=" * 72)
print("FOCUS deep dive (hexdumps)")
print("=" * 72)
deep = {}
for s in FOCUS:
    if s not in report:
        # try case-insensitive contains
        cand = [x for x in report if x.lower() == s.lower()]
        if not cand:
            continue
        s2 = cand[0]
    else:
        s2 = s
    for j in report[s2][:4]:
        print(f"\n--- {s2}  ref @{j:#x} ---")
        print(hexdump(j - 16, 176))
        deep[f"{s2}@{j:#x}"] = d[j - 16:j + 160].hex()

json.dump(deep, open(f"{OUT}/lvc_focus_hexdumps.json", "w"), indent=1)
print(f"\nsaved lvc_name_refs.json + lvc_focus_hexdumps.json")
