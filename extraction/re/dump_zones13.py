#!/usr/bin/env python3
"""Dump ALL CTemplateZone (0x2667) and CSpawnPointObject (0x2662) records
from GothamCity.lvc + GothamCity_Island2.lvc with names + TRS."""
import struct

for PATH in ("/home/z/my-project/download/TDKR_assets/raw/game_config/"
             "GothamCity.lvc",
             "/home/z/my-project/download/TDKR_assets/raw/game_config/"
             "GothamCity_Island2.lvc"):
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
    sidx = {s: i for i, s in enumerate(strings)}
    print("=" * 76)
    print(PATH.split("/")[-1], f"{len(strings)} strings")
    print("=" * 76)

    def rstr(o):
        i = struct.unpack_from(">i", d, o)[0]
        return (strings[i] if 0 <= i < len(strings) else f"<idx {i}>"), i

    # zone records: find [u32 nameidx][u32 1][typeId 0x2667]... OR bare typeId?
    # dispatcher: typeId read, then CTemplateZone::Load reads
    #   bool, string, float, bool, int, 9f, bool, bool, bool
    for tid_want, label, nfloats_after in ((0x2667, "ZONE", None),):
        pat = struct.pack(">I", tid_want)
        s = 9
        cnt = 0
        while True:
            j = d.find(pat, s, tbl)
            if j < 0:
                break
            s = j + 4
            p = j + 4
            try:
                b1 = d[p]; p += 1
                nm, nmi = rstr(p); p += 4
                f1 = struct.unpack_from(">f", d, p)[0]; p += 4
                b2 = d[p]; p += 1
                ii = struct.unpack_from(">i", d, p)[0]; p += 4
                trs = struct.unpack_from(">9f", d, p); p += 36
                bb = list(d[p:p + 3])
                if not all(abs(v) < 1e6 for v in trs):
                    continue
                print(f"  {label} @{j:#x}: bool={b1} name={nm!r} f={f1:.4g} "
                      f"bool={b2} int={ii} TRS={[round(v,3) for v in trs]} "
                      f"bools={bb}")
                cnt += 1
            except Exception:
                continue
        print(f"  ({cnt} {label} records)")

    # spawn records 0x2662: [name?][1?][typeId]... — scan [u32 nameidx][u32 X][0x2662]
    print("\n  -- spawn/0x2662 records with name prefix --")
    cnt = 0
    for j in range(9, tbl - 12):
        if d[j + 8:j + 12] == struct.pack(">I", 0x2662):
            nmi = struct.unpack_from(">i", d, j)[0]
            x = struct.unpack_from(">i", d, j + 4)[0]
            if 0 <= nmi < len(strings) and 0 <= x <= 16:
                nm = strings[nmi]
                p = j + 12
                b1 = d[p]; p += 1
                oid = struct.unpack_from(">i", d, p)[0]; p += 4
                trs = struct.unpack_from(">9f", d, p); p += 36
                if all(abs(v) < 1e6 for v in trs):
                    print(f"  SPAWN @{j:#x}: name={nm!r} pre={x} bool={b1} "
                          f"objId={oid} TRS={[round(v,3) for v in trs]}")
                    cnt += 1
    print(f"  ({cnt} spawn records)")
