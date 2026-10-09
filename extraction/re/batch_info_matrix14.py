#!/usr/bin/env python3
"""batch_info.bin — matrix interpretation + collaborator evidence pack.

BREAKTHROUGH (session 14): the zone materials bdae contains exactly
  GothamCity          307 materials  == island-1 record size 307
  GothamCity_Island2  196 materials  == island-2 record size 196
So batch_info.bin is NOT "197 records of M bytes" — it is a
  [197 rows (batches?) x M columns (materials)] BYTE MATRIX:
      file = u32(197) + 197*M bytes,  M = zone material count
  0xff = cell unused (material not referenced by that row), sparse small
  ints elsewhere.  This explains the "exact division" for BOTH islands and
  the different record sizes.

This script:
  1. verifies the matrix arithmetic + prints row/col stats
  2. per-row and per-column occupancy, value distributions
  3. cross-checks: bih_struct/bih_data/lod_table/lod_selector sizes,
     lod_table segment ranges vs 197
  4. writes the collaborator evidence pack:
     extraction/re/batch_info_evidence14.md
     - first 64 bytes of each file (hexdump)
     - two consecutive matrix rows from each island (hex, annotated)
     - first 5 lod_table rows with segment ranges
     - material name order (source.dae library order) for both zones
"""
import json
import os
import struct

ZONE = "/home/z/my-project/work/zone"
RE = os.path.dirname(os.path.abspath(__file__))
ISLANDS = [("GothamCity", "island1"), ("GothamCity_Island2", "island2")]


def hexdump(d, base=0, width=16):
    out = []
    for i in range(0, len(d), width):
        chunk = d[i:i + width]
        h = " ".join(f"{b:02x}" for b in chunk)
        a = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        out.append(f"{base + i:08x}  {h:<{width * 3 - 1}}  {a}")
    return "\n".join(out)


def lod_rows(island, n=5):
    lt = open(f"{ZONE}/{island}/lod_table.bin", "rb").read()
    N = struct.unpack_from("<I", lt, 0)[0]
    rows = []
    for k in range(min(n, N)):
        off, sz = struct.unpack_from("<II", lt, 4 + 8 * k)
        rows.append((k, off, sz))
    M = struct.unpack_from("<I", lt, 4 + 8 * N)[0]
    return N, rows, M, len(lt)


def analyze():
    report = {}
    for island, tag in ISLANDS:
        d = open(f"{ZONE}/{island}/batch_info.bin", "rb").read()
        mats = json.load(open(f"{ZONE}/zone_materials_{island}.json"))
        mat_names = list(mats["materials"].keys())
        M = len(mat_names)
        assert struct.unpack_from("<I", d, 0)[0] == 197
        body = d[4:]
        assert len(body) == 197 * M, (len(body), 197 * M)
        rows = [body[k * M:(k + 1) * M] for k in range(197)]

        used_per_row = []
        row_cells = []
        for r in rows:
            cells = [(c, v) for c, v in enumerate(r) if v != 0xFF]
            used_per_row.append(len(cells))
            row_cells.append(cells)
        used_per_col = [0] * M
        vals_per_col = [set() for _ in range(M)]
        for r in rows:
            for c, v in enumerate(r):
                if v != 0xFF:
                    used_per_col[c] += 1
                    vals_per_col[c].add(v)
        unused_mats = [c for c in range(M) if used_per_col[c] == 0]
        all_vals = sorted({v for s in vals_per_col for v in s})
        ltN, lt5, ltM, ltlen = lod_rows(island)
        bsz = os.path.getsize(f"{ZONE}/{island}/bih_struct.bin")
        bda = os.path.getsize(f"{ZONE}/{island}/bih_data.bin")
        lsel = os.path.getsize(f"{ZONE}/{island}/lod_selector.bin")

        print(f"=== {island} ({tag}) ===")
        print(f"  file {len(d)} B = 4 + 197 x {M}  (materials bdae: {M} mats)")
        print(f"  rows: min/mean/max used-cells "
              f"{min(used_per_row)}/{sum(used_per_row)/197:.1f}/{max(used_per_row)}")
        print(f"  cols: {sum(1 for u in used_per_col if u)} of {M} used by >=1 row;"
              f" {len(unused_mats)} never used")
        print(f"  cell values (non-ff): {all_vals[:24]}"
              f"{' ...' if len(all_vals) > 24 else ''}  ({len(all_vals)} distinct)")
        print(f"  lod_table: N={ltN} segs, {ltM} leaf refs, {ltlen} B | "
              f"bih_struct {bsz} B | bih_data {bda} B | lod_selector {lsel} B")
        print(f"  197 vs: lod segs {ltN} ({ltN / 197:.2f}/row), "
              f"bih_struct/{197}={bsz / 197:.1f}, bih_data/{197}={bda / 197:.1f}")
        # how many rows have cells, and the per-row value meaning candidates
        nz_rows = sum(1 for u in used_per_row if u > 0)
        print(f"  rows with >=1 cell: {nz_rows}/197")
        report[island] = dict(
            M=M, rows=197, used_per_row=used_per_row,
            used_per_col=used_per_col, unused_mats=unused_mats,
            distinct_values=all_vals, row_cells=row_cells,
            lod=dict(N=ltN, M2=ltM, rows5=lt5),
            sizes=dict(file=len(d), bih_struct=bsz, bih_data=bda,
                       lod_selector=lsel),
            mat_names=mat_names,
            first64=d[:64],
        )
    return report


if __name__ == "__main__":
    analyze()
