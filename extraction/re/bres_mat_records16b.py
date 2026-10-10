#!/usr/bin/env python3
"""Session 16: find the runtime material record array (pointers to material
name strings), decode its stride, and dump it in ARRAY ORDER with the
texture names each record references."""
import struct
import sys
import zipfile

ZONE = "/home/z/my-project/work/zone"


def all_len_strings(d):
    """[u32 len][chars] -> {content_off: s}"""
    out = {}
    i = 0
    n = len(d)
    while i + 4 <= n:
        L = struct.unpack_from("<I", d, i)[0]
        if 4 <= L <= 80 and i + 4 + L <= n:
            s = d[i + 4:i + 4 + L]
            if all(0x20 <= c < 0x7f for c in s):
                out[i + 4] = s.decode()
                i += 4 + L + 1
                continue
        i += 1
    return out


def main():
    island = sys.argv[1] if len(sys.argv) > 1 else "GothamCity"
    z = zipfile.ZipFile(f"{ZONE}/{island}/{island}_materials.bdae")
    d = z.read("little_endian_quantized.bdae")
    strs = all_len_strings(d)
    print(f"strings: {len(strs)}")

    # material names: match source.dae material ids
    import json
    lib = json.load(open(f"/home/z/my-project/repo/extraction/re/mat_tex_{island}.json"))["mats"]
    libnames = {m["name"] for m in lib}
    mat_strs = {o: s for o, s in strs.items() if s in libnames}
    print(f"material name strings found: {len(mat_strs)} / {len(libnames)}")

    # find u32 pointers to them
    locs = []
    for off, s in mat_strs.items():
        pat = struct.pack("<I", off)
        j = d.find(pat)
        while j >= 0:
            locs.append((j, off, s))
            j = d.find(pat, j + 4)
    locs.sort()
    print(f"pointers to material names: {len(locs)}")

    # dump context of each pointer (the record should reference more strings)
    # candidate record = [name_ptr][X][tech/effect ptr][...]
    for j, off, s in locs[:10]:
        w = struct.unpack_from("<10I", d, j - 4)
        ctx = []
        for x in w:
            ctx.append(strs.get(x, hex(x)))
        print(f"  rec@{j:7d} {s[:36]:36s} ctx={ctx}")

    # stride detection: distances between consecutive record pointers
    if len(locs) > 2:
        import collections
        dists = collections.Counter()
        for a, b in zip(locs, locs[1:]):
            dists[b[0] - a[0]] += 1
        print("pointer spacing histogram (top):", dists.most_common(8))


if __name__ == "__main__":
    main()
