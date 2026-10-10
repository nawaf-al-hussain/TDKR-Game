#!/usr/bin/env python3
"""Round-4 LM chain — the decisive visited-rect partition test.

Replaces the over-approximating [d, d+a] boxes: each material's VISITED
pageUV region = [min, max] of (w3_uv * a.xy + d.xy) unwrapped, wrapped onto
the page torus.  Under the engine-true chain the visited rects should be
compact and mostly non-overlapping (authored bake tiles / band strips);
the null = same-size rects placed uniformly on the torus.

Chains compared: (s121, s145), (s109, s145), (s133, s145), plus
w3-range census (full [0,1] vs narrow) per material.
"""
import collections
import json
import struct
import sys

import numpy as np

sys.path.insert(0, "/home/z/my-project/repo/extraction/scripts")
from export_zone import ISLANDS  # noqa: E402

RE = "/home/z/my-project/repo/extraction/re"
ZONE = "/home/z/my-project/work/zone"
OUT = f"{RE}/round4_lm_partition.json"


def seg_words(island):
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
        m40 = struct.unpack_from("<I", ld, off + 40)[0]
        words = np.frombuffer(ld[vstart:vstart + vb], "<u4").reshape(-1, stride // 4)
        out.append((m40, words if stride == 24 else None))
    return out


def torus_iv(a0, wa, b0, wb):
    shift = (b0 - a0) % 1.0
    def iv(s):
        return max(0.0, min(wa, s + wb) - max(0.0, s))
    return iv(shift) + iv(shift - 1.0)


def collisions(rects):
    n = len(rects)
    if n < 2:
        return 0.0
    fr = []
    for i in range(n):
        u0, v0, w, h = rects[i]
        w = max(w, 1e-6)
        h = max(h, 1e-6)
        cov = 0.0
        for j in range(n):
            if i == j:
                continue
            b = rects[j]
            bw = max(b[2], 1e-6)
            bh = max(b[3], 1e-6)
            cov += torus_iv(u0, w, b[0], bw) * torus_iv(v0, h, b[1], bh)
        fr.append(min(1.0, cov / (w * h)))
    return float(np.mean(fr))


def main():
    report = {}
    for islname in ISLANDS:
        print(f"\n########## {islname}")
        rows = json.load(open(f"{RE}/runtime_mats_{islname}.json"))
        d = open(f"{ZONE}/{islname}/batch_info.bin", "rb").read()
        stride_b = struct.unpack_from("<I", d, 0)[0]
        M = (len(d) - 4) // stride_b
        slots = []
        for m in range(M):
            rec = d[4 + stride_b * m: 4 + stride_b * (m + 1)]
            slots.append(dict(s109=struct.unpack_from("<3f", rec, 109),
                              s121=struct.unpack_from("<3f", rec, 121),
                              s133=struct.unpack_from("<3f", rec, 133),
                              s145=struct.unpack_from("<3f", rec, 145)))
        lm = {m for m in range(M)
              if rows[m].get("LightMap") and rows[m]["LightMap"] != "UNBOUND"}
        w3_by_m = collections.defaultdict(list)
        for m40, words in seg_words(islname):
            if words is not None and m40 in lm:
                w3_by_m[m40].append(words[:, 3])
        w3_cat = {m: np.concatenate(v) for m, v in w3_by_m.items() if v}

        # w3-range census
        full_range = 0
        narrow = 0
        for m, W in w3_cat.items():
            cu = (W & 0xFFFF).astype(np.float32) / 65535.0
            cv = (W >> 16).astype(np.float32) / 65535.0
            if cu.max() - cu.min() > 0.9 and cv.max() - cv.min() > 0.9:
                full_range += 1
            else:
                narrow += 1
        print(f"w3 census over {len(w3_cat)} LM materials: "
              f"full[0,1]x[0,1] range {full_range}, narrow {narrow}")

        npr = np.random.default_rng(4416)
        part = {}
        for tag in ("s109", "s121", "s133"):
            rects = []
            n_all = 0
            for m in w3_cat:
                W = w3_cat[m]
                cu = (W & 0xFFFF).astype(np.float32) / 65535.0
                cv = (W >> 16).astype(np.float32) / 65535.0
                a = slots[m][tag]
                dd = slots[m]["s145"]
                pu = cu * a[0] + dd[0]
                pv = cv * a[1] + dd[1]
                w = float(pu.max() - pu.min())
                h = float(pv.max() - pv.min())
                n_all += 1
                if max(w, h) > 1.2:      # page-sweeping population, skip
                    continue
                rects.append((float(pu.min() % 1.0), float(pv.min() % 1.0), w, h))
            if len(rects) < 5:
                continue
            coll = collisions(rects)
            areas = np.array([r[2] * r[3] for r in rects])
            nulls = []
            for _ in range(40):
                u0 = npr.uniform(0, 1, len(rects))
                v0 = npr.uniform(0, 1, len(rects))
                nulls.append(collisions([(u0[i], v0[i], rects[i][2], rects[i][3])
                                         for i in range(len(rects))]))
            part[tag] = dict(n=len(rects), n_all=n_all,
                             total_visited_area=round(float(areas.sum()), 3),
                             authored=round(coll, 4),
                             null=round(float(np.mean(nulls)), 4),
                             null_sd=round(float(np.std(nulls)), 4))
            print(f"  visited-partition[{tag}] compact-only: "
                  f"n={len(rects)}/{n_all} area={areas.sum():.2f}  "
                  f"authored {coll*100:.1f}% vs null "
                  f"{np.mean(nulls)*100:.1f}%±{np.std(nulls)*100:.1f}%")
        report[islname] = dict(w3_census=dict(n=len(w3_cat), full=full_range,
                                              narrow=narrow),
                               partition=part)

        # per-material visited-rect table for the winning chain (s121)
        rowsx = {}
        for m in sorted(w3_cat, key=lambda m: -len(w3_cat[m]))[:20]:
            W = w3_cat[m]
            cu = (W & 0xFFFF).astype(np.float32) / 65535.0
            cv = (W >> 16).astype(np.float32) / 65535.0
            a = slots[m]["s121"]
            dd = slots[m]["s145"]
            pu = cu * a[0] + dd[0]
            pv = cv * a[1] + dd[1]
            rowsx[m] = dict(n=int(len(W)),
                            a=[round(x, 4) for x in a], d=[round(x, 4) for x in dd],
                            uArc=[round(float(pu.min()), 3), round(float(pu.max()), 3)],
                            vArc=[round(float(pv.min()), 3), round(float(pv.max()), 3)],
                            dif=rows[m].get("DiffuseMap"),
                            lm=rows[m].get("LightMap"))
        report[islname]["top_visited_s121"] = rowsx

    json.dump(report, open(OUT, "w"), indent=1)
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
