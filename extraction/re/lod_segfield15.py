#!/usr/bin/env python3
"""Task 6: search lod_table segment descriptors + lod_data segment block
headers for a per-segment field with value range < M (material count).

Descriptor layout (session 9, symtab-true base): per segment at lod_table
pair offsets: +0 triCount, +4 6xf32 bounds, +68 dataOff, +72 =4, +76 vBytes,
+80 iBytes, +84 fmt1, +88 fmt2, +92 0x00010000, +96 0xffff0000, +100.. packed.
"""
import struct
import collections

ZONE = "/home/z/my-project/work/zone"
ISLANDS = [("GothamCity", 307), ("GothamCity_Island2", 196)]


def u32(d, o):
    return struct.unpack_from("<I", d, o)[0]


def main():
    for island, M in ISLANDS:
        lt = open(f"{ZONE}/{island}/lod_table.bin", "rb").read()
        ld = open(f"{ZONE}/{island}/lod_data.bin", "rb").read()
        N = u32(lt, 0)
        pairs = [(u32(lt, 4 + 8 * i), u32(lt, 8 + 8 * i)) for i in range(N)]
        M2 = u32(lt, 4 + 8 * N)
        print(f"\n===== {island}: N={N} segments, leaf idx M2={M2}, "
              f"mat count M={M} =====")

        # per-descriptor parse: stats per field
        fields = {}
        for off, sz in pairs:
            d = ld[off:off + sz]   # descriptors live in lod_data END region
            fields.setdefault("triCount", []).append(u32(d, 0))
            fields.setdefault("dataOff", []).append(u32(d, 68))
            fields.setdefault("vBytes", []).append(u32(d, 76))
            fields.setdefault("iBytes", []).append(u32(d, 80))
            fields.setdefault("fmt1", []).append(u32(d, 84))
            fields.setdefault("fmt2", []).append(u32(d, 88))
            fields.setdefault("w92", []).append(u32(d, 92))
            fields.setdefault("w96", []).append(u32(d, 96))
            # every u32 in the packed block +100..sz, keep small ones
            for p in range(100, len(d) - 3, 4):
                v = u32(d, p)
                if v < 4096:
                    fields.setdefault(f"packed+{p}", []).append(v)

        for k, vals in fields.items():
            vals = vals[:N] if k in ("triCount", "dataOff", "vBytes", "iBytes",
                                     "fmt1", "fmt2", "w92", "w96") else vals
            mx = max(vals) if vals else -1
            distinct = len(set(vals))
            under_m = sum(1 for v in vals if v < M)
            flag = "  <-- RANGE < M!" if 0 < mx < M and distinct > 1 else ""
            print(f"  {k:>10}: n={len(vals):5d} distinct={distinct:5d} "
                  f"min={min(vals) if vals else '-'} max={mx:<10} "
                  f"frac<M={under_m / max(len(vals), 1):.2f}{flag}")

        # byte-level: which descriptor byte offsets carry values < M with signal?
        # (scan first 140 bytes of each descriptor)
        byt = {}
        for off, sz in pairs[:N]:
            d = lt[off:off + min(sz, 140)]
            for p, b in enumerate(d):
                if b < M:
                    byt.setdefault(p, []).append(b)
        cand = []
        for p, vals in sorted(byt.items()):
            distinct = len(set(vals))
            if distinct >= 16 and p >= 100:  # packed area, non-trivial cardinality
                cand.append((p, distinct, max(vals), len(vals)))
        print("  packed-area byte candidates (distinct>=16, values<M):")
        for p, dc, mx, n in cand[:25]:
            print(f"    desc+{p:3d}: distinct={dc:3d} max={mx:3d} n={n}")

        # lod_data segment block headers: u32 before vertices (0x5150c200 etc.)
        hdrs = collections.Counter()
        hdr_bytes = collections.defaultdict(collections.Counter)
        for off, sz in pairs[:N]:
            do = u32(lt, off + 68)
            if do + 4 <= len(ld):
                h = u32(ld, do)
                hdrs[h] += 1
                for sh, nm in ((24, "b3"), (16, "b2"), (8, "b1"), (0, "b0")):
                    hdr_bytes[nm][(h >> sh) & 0xFF] += 1
        print(f"  segment block header u32s: {len(hdrs)} distinct; top:",
              [(hex(h), c) for h, c in hdrs.most_common(6)])
        for nm in ("b3", "b2", "b1", "b0"):
            vals = hdr_bytes[nm]
            mx = max(vals)
            if 1 < len(vals) <= 4096:
                print(f"    header {nm}: distinct={len(vals)} max={mx} "
                      f"vals={sorted(vals.items())[:12]}")
        # b1/b2 byte across headers as material index candidate
        for nm in ("b1", "b2", "b3"):
            vals = hdr_bytes[nm]
            if vals and max(vals) < M and len(vals) > 16:
                print(f"    *** header byte {nm}: range < M! "
                      f"distinct={len(vals)}")


if __name__ == "__main__":
    main()
