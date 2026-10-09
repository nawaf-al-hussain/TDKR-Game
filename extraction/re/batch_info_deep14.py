#!/usr/bin/env python3
"""batch_info deep structure: what lives in the [197 x M] byte cells?"""
import json
import os
import struct
import collections

ZONE = "/home/z/my-project/work/zone"
ISLANDS = [("GothamCity", 307), ("GothamCity_Island2", 196)]


def ff_runs(row):
    """lengths of consecutive 0xff runs."""
    runs, cur = [], 0
    for v in row:
        if v == 0xFF:
            cur += 1
        elif cur:
            runs.append(cur)
            cur = 0
    if cur:
        runs.append(cur)
    return runs


def main():
    for island, M in ISLANDS:
        d = open(f"{ZONE}/{island}/batch_info.bin", "rb").read()
        body = d[4:]
        R = [body[k * M:(k + 1) * M] for k in range(197)]
        print(f"=== {island} [197 x {M}] ===")

        # value histogram (global)
        hist = collections.Counter()
        for r in R:
            hist.update(r)
        ff = hist.pop(0xFF, 0)
        tot = 197 * M
        print(f"  0xff cells: {ff} ({100 * ff / tot:.1f}%)")
        top = hist.most_common(12)
        print(f"  top values: {[(v, c, f'{100*c/(tot-ff):.1f}%') for v, c in top]}")
        vmax = max(hist)
        print(f"  value range 0..{vmax}")

        # per-row ff-run structure
        allruns = []
        for r in R:
            allruns += ff_runs(r)
        rc = collections.Counter(allruns)
        print(f"  ff-run lengths (top): {rc.most_common(10)}")
        print(f"  rows with no ff: {sum(1 for r in R if 0xFF not in r)}/197")

        # per-column cardinality (distinct non-ff values)
        colcard = []
        for c in range(M):
            s = {r[c] for r in R if r[c] != 0xFF}
            colcard.append(len(s))
        cc = collections.Counter(colcard)
        print(f"  column distinct-value counts: {sorted(cc.items())[:12]} ...")
        low = [c for c in range(M) if colcard[c] <= 3]
        print(f"  columns with <=3 distinct values: {len(low)}; "
              f"examples: {low[:10]}")
        for c in low[:3]:
            vals = collections.Counter(r[c] for r in R if r[c] != 0xFF)
            print(f"    col {c}: {vals.most_common(5)}")

        # per-row: are low columns the busy ones? print row0/1 annotated
        for ri in (0, 1):
            r = R[ri]
            cells = [(c, v) for c, v in enumerate(r) if v != 0xFF]
            runs = ff_runs(r)
            print(f"  row {ri}: {len(cells)} non-ff, ff-runs {runs[:12]}"
                  f"{'...' if len(runs) > 12 else ''}")
            print(f"    first 24 cells (col,val): {cells[:24]}")
            print(f"    values mean {sum(v for _, v in cells)/max(1,len(cells)):.1f}"
                  f" max {max(v for _, v in cells)}")

        # cross-match against lod_table offsets/sizes (u32 LE/BE at any
        # row offset is impossible in 1 byte — but check row VALUES vs
        # segment index ranges: seg k spans lod_data offsets)
        lt = open(f"{ZONE}/{island}/lod_table.bin", "rb").read()
        N = struct.unpack_from("<I", lt, 0)[0]
        offs = [struct.unpack_from("<I", lt, 4 + 8 * k)[0] for k in range(N)]
        szs = [struct.unpack_from("<I", lt, 8 + 8 * k)[0] for k in range(N)]
        print(f"  lod seg sizes: min {min(szs)} max {max(szs)}; "
              f"first5 off/sz: {[(hex(o), s) for o, s in zip(offs[:5], szs[:5])]}")
        # value 0..254 vs segment sizes? sizes are ~0xf8=248-ish!
        print(f"  NOTE: lod seg sizes ~{min(szs)}..{max(szs)} "
              f"(many == {collections.Counter(szs).most_common(3)})")
    return


if __name__ == "__main__":
    main()
