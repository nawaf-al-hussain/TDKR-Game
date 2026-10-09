#!/usr/bin/env python3
"""batch_info.bin word-position decode (session 15, reviewer test 1).

TRUE layout (session 14):  file := u32(197) + M x 197-byte records
  record(m) := [byte0 = m & 0xff] + 196 bytes payload
  payload   := 49 x u32  (the reviewer's proposed reading)

For every word position w (0..48) over all M records, classify the u32
in both LE and BE as:
  ff      = 0xffffffff (sentinel)
  zero    = 0x00000000
  byte    = 0 < v < 256
  u16     = 256 <= v < 65536
  big     = v >= 65536
  fsane   = IEEE f32 decode finite and 1e-6 <= |v| <= 1e6  (not denormal junk)
  fuv     = f32 finite in [0, 2]  (UV-rect / normalized plausible)

Also: are the payload 0xff runs u32-aligned (=> whole -1 words)?
And a handful of records fully decoded as words for the collaborator.
"""
import struct
import collections

ZONE = "/home/z/my-project/work/zone"
ISLANDS = [("GothamCity", 307), ("GothamCity_Island2", 196)]
NW = 49  # 196 bytes payload = 49 u32


def words_of(payload, endian):
    fmt = ("<" if endian == "LE" else ">") + "49I"
    return struct.unpack(fmt, payload)


def classify(v, endian):
    """Independent tags (a word can carry several)."""
    if v == 0xFFFFFFFF:
        return ["ff"]
    if v == 0:
        return ["zero"]
    f = struct.unpack(("<f" if endian == "LE" else ">f"), struct.pack("I", v))[0]
    tags = []
    if 1e-6 <= abs(f) <= 1e6:
        tags.append("fsane")
    if 0.0 <= f <= 2.0:
        tags.append("fuv")
    if v < 256:
        tags.append("byte")
    elif v < 65536:
        tags.append("u16")
    else:
        tags.append("big")
    return tags


def ff_runs(buf):
    runs, cur, start = [], 0, None
    for i, b in enumerate(buf):
        if b == 0xFF:
            if cur == 0:
                start = i
            cur += 1
        else:
            if cur:
                runs.append((start, cur))
            cur, start = 0, None
    if cur:
        runs.append((start, cur))
    return runs


def main():
    for island, M in ISLANDS:
        d = open(f"{ZONE}/{island}/batch_info.bin", "rb").read()
        body = d[4:]
        recs = [body[m * 197:(m + 1) * 197] for m in range(M)]
        assert all(r[0] == (m & 0xFF) for m, r in enumerate(recs))

        for endian in ("LE", "BE"):
            print(f"\n===== {island}  M={M}  words as {endian} u32 =====")
            print("pos |   %ff   %zero  %byte  %u16  %big  %fsane  %fuv | distinct | note")
            notes = []
            for w in range(NW):
                vals = [words_of(r[1:], endian)[w] for r in recs]
                c = collections.Counter()
                for v in vals:
                    for t in classify(v, endian):
                        c[t] += 1
                n = M
                pc = lambda k: 100.0 * c.get(k, 0) / n
                distinct = len(set(vals))
                note = ""
                if pc("ff") > 90:
                    note = "<- almost always -1"
                elif pc("zero") > 90:
                    note = "<- almost always 0"
                elif pc("fsane") > 60:
                    fvals = sorted(set(
                        struct.unpack("<f" if endian == "LE" else ">f",
                                      struct.pack("I", v))[0]
                        for v in vals
                        if "fsane" in classify(v, endian)))
                    note = f"floaty: {fvals[0]:.6g}..{fvals[-1]:.6g}"
                elif pc("byte") > 50:
                    mx = max(v for v in vals if v < 65536)
                    note = f"byte-ish max {mx}"
                if distinct == 1:
                    note = "CONSTANT " + hex(vals[0])
                print(f"{w:3d} | {pc('ff'):5.1f} {pc('zero'):6.1f} "
                      f"{pc('byte'):6.1f} {pc('u16'):5.1f} {pc('big'):5.1f} "
                      f"{pc('fsane'):6.1f} {pc('fuv'):5.1f} | {distinct:8d} | {note}")

        # 0xff run alignment inside payloads (LE/BE identical at byte level)
        runs = []
        for r in recs:
            runs += ff_runs(r[1:])
        mod4 = collections.Counter(s % 4 for s, L in runs)
        lens = collections.Counter(L for s, L in runs)
        mod4_all = collections.Counter((s + 1) % 4 for s, L in runs)  # incl byte0
        print(f"\n  0xff runs in payload: n={len(runs)}")
        print(f"  run-length hist: {dict(sorted(lens.items()))}")
        print(f"  start%4 (payload-relative): {dict(sorted(mod4.items()))}")
        print(f"  start%4 (record-relative, byte0 included): {dict(sorted(mod4_all.items()))}")
        # exact 3-word (12B) aligned runs?
        n12 = sum(1 for s, L in runs if L == 12)
        n12al = sum(1 for s, L in runs if L == 12 and s % 4 == 0)
        print(f"  runs of exactly 12: {n12}, of which payload-u32-aligned: {n12al}")


def byte_profile(island, M):
    """Per-byte-position profile over all records (TRUE grid) -> template map."""
    d = open(f"{ZONE}/{island}/batch_info.bin", "rb").read()
    body = d[4:]
    recs = [body[m * 197:(m + 1) * 197] for m in range(M)]
    print(f"\n===== {island} byte profile (pos 0..196; rec-rel incl byte0) =====")
    print("legend: .=mixed  f=always ff  F>=90% ff  0=always 00  O>=90% 00  S>=90% 254  U=always same value")
    row = []
    segdesc = []
    for p in range(197):
        col = [r[p] for r in recs]
        distinct = len(set(col))
        fff = 100.0 * sum(1 for b in col if b == 0xFF) / M
        z00 = 100.0 * sum(1 for b in col if b == 0) / M
        sfe = 100.0 * sum(1 for b in col if b == 0xFE) / M
        if distinct == 1:
            ch = "U"
            segdesc.append((p, f"CONST 0x{col[0]:02x}"))
        elif fff == 100:
            ch = "f"
        elif fff >= 90:
            ch = "F"
        elif z00 == 100:
            ch = "0"
        elif z00 >= 90:
            ch = "O"
        elif sfe >= 90:
            ch = "S"
        else:
            ch = "."
            segdesc.append((p, f"mixed distinct={distinct} min={min(col)} max={max(col)}"))
        row.append(ch)
    for i in range(0, 197, 49):
        print(f"{i:4d}: {''.join(row[i:i + 49])}")
    print("segments with distinct structure:")
    # merge consecutive CONSTANT/mixed into ranges for readability
    for p, txt in segdesc[:80]:
        print(f"  pos {p:3d}: {txt}")


def paste_samples():
    """Fully decode a handful of records: the collaborator paste."""
    for island, M, pick in [("GothamCity", 307, (0, 1, 2, 306)),
                            ("GothamCity_Island2", 196, (0, 1, 2, 100))]:
        d = open(f"{ZONE}/{island}/batch_info.bin", "rb").read()
        body = d[4:]
        for m in pick:
            if m >= M:
                continue
            rec = body[m * 197:(m + 1) * 197]
            print(f"\n--- {island} record {m} (file offset {4 + m * 197}) ---")
            print("byte0 = 0x%02x (expect 0x%02x)" % (rec[0], m & 0xFF))
            wle = words_of(rec[1:], "LE")
            wbe = words_of(rec[1:], "BE")
            for w in range(NW):
                fle = struct.unpack("<f", struct.pack("I", wle[w]))[0]
                fbe = struct.unpack(">f", struct.pack("I", wbe[w]))[0]
                print(f"  w{w:02d} off={1+4*w:3d}: LE {wle[w]:08x} int {wle[w]:>10d} f {fle:>14.6g}   "
                      f"BE {wbe[w]:08x} int {wbe[w]:>10d} f {fbe:>14.6g}")


if __name__ == "__main__":
    main()
    byte_profile("GothamCity", 307)
    byte_profile("GothamCity_Island2", 196)
    paste_samples()
