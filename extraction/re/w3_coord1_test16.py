#!/usr/bin/env python3
"""Session 16 — H_uv1 test: is vertex word 3 the packed lightmap UV (Coord1)?

If yes, pageUV = w3_uv * b.xy + d.xy (batch_info) must land inside the
LightMap page for ~all vertices of LM-bound materials, and segments of one
material should occupy a COHERENT sub-rect (the bake tile).
Competing model H_flat: Coord1 absent (w3 = packed normal), pageUV = d.xy.
"""
import collections
import json
import struct
import sys

import numpy as np

sys.path.insert(0, "/home/z/my-project/repo/extraction/scripts")
from export_zone import parse_island, ISLANDS  # noqa: E402

ZONE = "/home/z/my-project/work/zone"
RE = "/home/z/my-project/repo/extraction/re"


def raw_segs(island):
    """Same filter order as parse_island but returns words too."""
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
        stride = None
        for s in (24, 20, 32):
            if vb % s == 0 and mx < vb // s:
                t = np.frombuffer(ld[vstart:vstart + vb], "<f4").reshape(-1, s // 4)[:, :3]
                if np.isfinite(t).all() and np.abs(t).max() < 6000:
                    stride = s
                    break
        if stride is None:
            continue
        words = np.frombuffer(ld[vstart:vstart + vb], "<u4").reshape(-1, stride // 4)
        out.append(dict(words=words, stride=stride))
    return out


def main():
    for islname, isl in ISLANDS.items():
        rows = json.load(open(f"{RE}/runtime_mats_{islname}.json"))
        d = open(f"{ZONE}/{islname}/batch_info.bin", "rb").read()
        stride_b = struct.unpack_from("<I", d, 0)[0]
        bd = []
        for m in range((len(d) - 4) // stride_b):
            rec = d[4 + stride_b * m: 4 + stride_b * (m + 1)]
            bd.append((struct.unpack_from("<3f", rec, 121),
                       struct.unpack_from("<3f", rec, 145)))
        segs = raw_segs(islname)
        # +40 in same order
        m40s = []
        lt = open(f"{ZONE}/{islname}/lod_table.bin", "rb").read()
        ld = open(f"{ZONE}/{islname}/lod_data.bin", "rb").read()
        u = struct.unpack(f"<{len(lt)//4}I", lt)
        n = u[0]
        pairs = [(u[1 + 2 * k], u[2 + 2 * k]) for k in range(n)]
        si = 0
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
            if not ok:
                continue
            m40s.append(struct.unpack_from("<I", ld, off + 40)[0])
            si += 1
        assert si == len(segs)

        # per material: pageUV = w3uv * b.xy + d.xy, inside fraction
        # w3 = word index 3 (0-based) for both strides
        per = collections.defaultdict(lambda: [0, 0, [], []])
        for s, m in zip(segs, m40s):
            if m >= len(rows) or not rows[m].get("LightMap") \
                    or rows[m]["LightMap"] == "UNBOUND":
                continue
            w3 = s["words"][:, 3]
            cu = (w3 & 0xFFFF).astype(np.float32) / 65535.0
            cv = (w3 >> 16).astype(np.float32) / 65535.0
            b, dd = bd[m] if m < len(bd) else ((0, 0, 0), (0, 0, 0))
            pu = cu * b[0] + dd[0]
            pv = cv * b[1] + dd[1]
            inside = np.sum((pu > -0.02) & (pu < 1.02) & (pv > -0.02) & (pv < 1.02))
            per[m][0] += int(inside)
            per[m][1] += len(cu)
            per[m][2].append(float(np.min(pu)))
            per[m][2].append(float(np.max(pu)))
            per[m][3].append(float(np.min(pv)))
            per[m][3].append(float(np.max(pv)))
        tot_in = tot_n = 0
        coherent = 0
        print(f"\n===== {islname} (H_uv1: pageUV = w3*b.xy + d.xy)")
        for m in sorted(per, key=lambda m: -per[m][1])[:16]:
            i, nn, ur, vr = per[m]
            u_lo, u_hi = min(ur), max(ur)
            v_lo, v_hi = min(vr), max(vr)
            area = (u_hi - u_lo) * (v_hi - v_lo)
            tot_in += i
            tot_n += nn
            if area < 0.30:
                coherent += 1
            print(f"  m{m:3d} n={nn:6d} inside={i/nn:5.2f} "
                  f"uRect=[{u_lo:6.2f},{u_hi:6.2f}] vRect=[{v_lo:6.2f},{v_hi:6.2f}] "
                  f"rectArea={area:5.2f} lm={str(rows[m]['LightMap'])[:30]}")
        all_in = sum(v[0] for v in per.values())
        all_n = sum(v[1] for v in per.values())
        print(f"  TOTAL inside: {all_in}/{all_n} = {100.0*all_in/max(all_n,1):.2f}%"
              f"   coherent-rect materials (of top16): {coherent}")


if __name__ == "__main__":
    main()
