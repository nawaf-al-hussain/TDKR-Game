#!/usr/bin/env python3
"""Round-4 preflight: texture PNG coverage for every material slot + diffuse
stem census for family design. Also rebuilds the park-segment shortlist."""
import collections
import json
import os
import struct
import sys

import numpy as np

sys.path.insert(0, "/home/z/my-project/repo/extraction/scripts")
from export_zone import parse_island, find_png, ISLANDS  # noqa: E402

RE = "/home/z/my-project/repo/extraction/re"
ZONE = "/home/z/my-project/work/zone"


def m40s(island):
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
        idx = np.frombuffer(ld[vstart + vb:vstart + vb + ib], "<u2").astype(np.int32)
        real = idx[idx != 0xFFFF]
        mx = int(real.max()) if len(real) else 0
        ok = False
        for s in (24, 20, 32):
            if vb % s == 0 and mx < vb // s:
                t = np.frombuffer(ld[vstart:vstart + vb], "<f4").reshape(-1, s // 4)[:, :3]
                if np.isfinite(t).all() and np.abs(t).max() < 6000:
                    ok = True
                    break
        if ok:
            out.append(struct.unpack_from("<I", ld, off + 40)[0])
    return out


for islname in ISLANDS:
    rows = json.load(open(f"{RE}/runtime_mats_{islname}.json"))
    segs = parse_island(islname)
    ms = m40s(islname)
    cnt = collections.Counter(ms)
    print(f"\n===== {islname}: {len(segs)} segments, {len(rows)} materials")

    dif_missing, lm_missing = [], []
    stems = collections.Counter()
    for i, r in enumerate(rows):
        d, l = r.get("DiffuseMap"), r.get("LightMap")
        ds = d.replace(".tga", "") if d else None
        ls = l.replace(".tga", "") if l and l != "UNBOUND" else None
        nseg = cnt.get(i, 0)
        if ds:
            stems[ds] += nseg
            if nseg and find_png(ds) is None:
                dif_missing.append((i, ds, nseg))
        if ls and nseg and find_png(ls) is None:
            lm_missing.append((i, ls, nseg))
    print("diffuse PNG missing (used by >=1 segment):", dif_missing)
    print("lightmap PNG missing (used by >=1 segment):", lm_missing)
    print(f"distinct diffuse stems used: {len(stems)}")
    for s, n in stems.most_common(400):
        print(f"  {n:5d}  {s}")
