#!/usr/bin/env python3
"""Session 16 pre-test survey: descriptor +40 histogram -> material DB rows.

Re-bases the +40 field exactly as session 15 did (u32 LE at lod_data
descriptor offset +40) and joins it against mat_tex_<island>.json
(library_materials order from source.dae). Output informs the family
mapping used by the street-tier agreement test.
"""
import json
import struct
import sys
import collections

sys.path.insert(0, "/home/z/my-project/repo/extraction/scripts")
from export_zone import parse_island, uv_of  # noqa: E402

ZONE = "/home/z/my-project/work/zone"
RE = "/home/z/my-project/repo/extraction/re"
ISLANDS = [("GothamCity", 307), ("GothamCity_Island2", 196)]


def descriptors(island):
    """(offset,size) pairs -> list of dicts with +36/+40, in parse_island
    filter order (four==4, stride found). Mirrors export_zone.parse_island
    filters exactly so indices align with parse_island output."""
    import numpy as np
    lt = open(f"{ZONE}/{island}/lod_table.bin", "rb").read()
    ld = open(f"{ZONE}/{island}/lod_data.bin", "rb").read()
    u = struct.unpack(f"<{len(lt)//4}I", lt)
    n = u[0]
    pairs = [(u[1 + 2 * k], u[2 + 2 * k]) for k in range(n)]
    out = []
    for off, sz in pairs:
        data_off, four, vb, ib = struct.unpack_from("<4I", ld, off + 68)
        if four != 4:
            continue
        vstart = data_off + 4
        istart = vstart + vb
        idx = np.frombuffer(ld[istart:istart + ib], "<u2").astype(np.int32)
        real = idx[idx != 0xFFFF]
        mx = int(real.max()) if len(real) else 0
        stride = None
        for s in (24, 20, 32):
            if vb % s == 0 and mx < vb // s:
                t = np.frombuffer(ld[vstart:vstart + vb], "<f4").reshape(-1, s // 4)[:, :3]
                if np.isfinite(t).all() and np.abs(t).max() < 6000:
                    stride = s
                    break
        if stride is None:
            continue
        out.append(dict(off=off,
                        m40=struct.unpack_from("<I", ld, off + 40)[0],
                        id36=struct.unpack_from("<I", ld, off + 36)[0]))
    return out


def main():
    for island, M in ISLANDS:
        mats = json.load(open(f"{RE}/mat_tex_{island}.json"))["mats"]
        assert len(mats) == M
        desc = descriptors(island)
        segs = parse_island(island)
        print(f"\n===== {island}: {len(desc)} descriptors / {len(segs)} segments, M={M}")
        hist = collections.Counter(d["m40"] for d in desc)
        print(f"+40 distinct={len(hist)} max={max(hist)} (must be < {M})")
        print("top 15 +40 values -> material row:")
        for v, c in hist.most_common(15):
            m = mats[v]
            print(f"  +40={v:3d} n={c:4d}  {m['name'][:40]:40s} "
                  f"dif={str(m['DiffuseMap'])[:44]:44s} lm={str(m['LightMap'])[:40]}")
        print("bottom 6:", hist.most_common()[-6:])
        # family histogram: +40 -> DiffuseMap stem, top 20
        fam = collections.Counter()
        for d in desc:
            dm = (mats[d["m40"]].get("DiffuseMap") or "<unbound>")
            fam[dm.replace(".tga", "")] += 1
        print("DiffuseMap family histogram (top 24):")
        for k, c in fam.most_common(24):
            print(f"  {k:<48} {c}")
        print("distinct DiffuseMaps:", len(fam))


if __name__ == "__main__":
    main()
