#!/usr/bin/env python3
"""Session 16 — batch_info b/d DIRECT TEST (reviewer-prescribed).

Population: street segments whose +40 material has a runtime-BOUND LightMap
(type-13 sampler, texIdx != 255). For each such material, batch_info record
m carries four vec3 f32 groups at record offsets 109/121/133/145 (a/b/c/d).
Hypothesis: lm_uv = uv0 * b.xy + d.xy  (b=scale @121, d=offset @145).

Score per candidate transform: fraction of transformed UVs inside [0,1]^2
(the LightMap page), averaged over the material's segments. Nulls:
  - identity (no transform)
  - shuffled-pairing (b of one material x d of another), 200 draws
  - all four group pairings (a+b, a+d, c+b, c+d, b+d) for completeness

Output: extraction/re/lightmap_uv_test16.json + stdout.
"""
import collections
import json
import random
import struct

import numpy as np

sys_path = "/home/z/my-project/repo/extraction/scripts"
import sys  # noqa: E402
sys.path.insert(0, sys_path)
from export_zone import parse_island, uv_of, ISLANDS  # noqa: E402

ZONE = "/home/z/my-project/work/zone"
RE = "/home/z/my-project/repo/extraction/re"
OUT = f"{RE}/lightmap_uv_test16.json"


def m40s_and_segs(island):
    lt = open(f"{ZONE}/{island}/lod_table.bin", "rb").read()
    ld = open(f"{ZONE}/{island}/lod_data.bin", "rb").read()
    u = struct.unpack(f"<{len(lt)//4}I", lt)
    n = u[0]
    pairs = [(u[1 + 2 * k], u[2 + 2 * k]) for k in range(n)]
    out = []
    segs = parse_island(island)
    i = 0
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
        out.append(struct.unpack_from("<I", ld, off + 40)[0])
        i += 1
    assert len(out) == len(segs)
    return out, segs


def batch_groups(island):
    """record m -> (a,b,c,d) each 3 floats, from offsets 109/121/133/145."""
    d = open(f"{ZONE}/{island}/batch_info.bin", "rb").read()
    stride = struct.unpack_from("<I", d, 0)[0]
    assert stride == 197, stride
    M = (len(d) - 4) // stride
    groups = []
    for m in range(M):
        rec = d[4 + stride * m: 4 + stride * (m + 1)]
        assert rec[0] == m % 256
        g = []
        for o in (109, 121, 133, 145):
            g.append(struct.unpack_from("<3f", rec, o))
        groups.append(g)
    return groups


def main():
    rng = random.Random(1618)
    report = {}
    for islname, isl in ISLANDS.items():
        rows = json.load(open(f"{RE}/runtime_mats_{islname}.json"))
        groups = batch_groups(islname)
        m40s, segs = m40s_and_segs(islname)

        # population: LightMap bound
        pop = collections.defaultdict(list)   # m -> [seg indices]
        for i, (s, m) in enumerate(zip(segs, m40s)):
            if m < len(rows) and rows[m].get("LightMap") and rows[m]["LightMap"] != "UNBOUND":
                pop[m].append(i)
        print(f"\n===== {islname}: {sum(len(v) for v in pop.values())} segments, "
              f"{len(pop)} materials with bound LightMap")

        uv_cache = {}
        def uvs(i):
            if i not in uv_cache:
                u, v = uv_of(segs[i])
                uv_cache[i] = np.stack([u, v], 1)
            return uv_cache[i]

        def in01(t, pair_idx):
            n_in = n_tot = 0
            for m, idxs in pop.items():
                b = groups[m][pair_idx[0]]
                d = groups[m][pair_idx[1]]
                for i in idxs:
                    uv = uvs(i)
                    lm = uv * np.array(b[:2]) + np.array(d[:2])
                    inside = np.all((lm > -0.02) & (lm < 1.02), axis=1)
                    n_in += int(inside.sum())
                    n_tot += len(inside)
            return n_in / max(n_tot, 1)

        cands = {
            "identity": None,
            "b+d (121,145)": (1, 3),
            "a+d (109,145)": (0, 3),
            "c+b (133,121)": (2, 1),
            "a+b (109,121)": (0, 1),
            "c+d (133,145)": (2, 3),
            "b only (121)": (1, 1),   # scale-only, offset=0 via b.z? use b as both
        }
        res = {}
        for name, pr in cands.items():
            if name == "identity":
                n_in = n_tot = 0
                for m, idxs in pop.items():
                    for i in idxs:
                        uv = uvs(i)
                        inside = np.all((uv > -0.02) & (uv < 1.02), axis=1)
                        n_in += int(inside.sum())
                        n_tot += len(inside)
                res[name] = n_in / max(n_tot, 1)
            else:
                res[name] = in01(None, pr)
        # null: shuffled b/d pairing
        ms = list(pop.keys())
        nulls = []
        for _ in range(200):
            n_in = n_tot = 0
            for m in ms:
                m2 = ms[rng.randrange(len(ms))]
                b = groups[m][1]
                d = groups[m2][3]
                for i in pop[m][:6]:
                    uv = uvs(i)
                    lm = uv * np.array(b[:2]) + np.array(d[:2])
                    inside = np.all((lm > -0.02) & (lm < 1.02), axis=1)
                    n_in += int(inside.sum())
                    n_tot += len(inside)
            nulls.append(n_in / max(n_tot, 1))
        res["null_shuffled_bd"] = dict(mean=float(np.mean(nulls)),
                                       sd=float(np.std(nulls)),
                                       max=float(np.max(nulls)),
                                       p99=float(np.percentile(nulls, 99)))

        for k, v in res.items():
            if isinstance(v, float):
                print(f"  {k:16s}: inside[0,1]^2 = {100*v:6.2f}%")
            else:
                print(f"  {k:16s}: mean {100*v['mean']:6.2f}% sd {100*v['sd']:.2f} "
                      f"max {100*v['max']:6.2f}% p99 {100*v['p99']:.2f}%")

        # per-material detail for b+d (the hypothesis): show top materials
        detail = []
        for m in sorted(pop, key=lambda m: -len(pop[m]))[:12]:
            b = groups[m][1]
            d = groups[m][3]
            n_in = n_tot = 0
            for i in pop[m]:
                uv = uvs(i)
                lm = uv * np.array(b[:2]) + np.array(d[:2])
                inside = np.all((lm > -0.02) & (lm < 1.02), axis=1)
                n_in += int(inside.sum())
                n_tot += len(inside)
            detail.append(dict(m=m, n=len(pop[m]),
                               name=rows[m]["name"],
                               lm=rows[m]["LightMap"],
                               b=[round(x, 4) for x in b],
                               d=[round(x, 4) for x in d],
                               inside=round(n_in / max(n_tot, 1), 4)))
        print("  top materials (b+d):")
        for dd in detail:
            print(f"    m{dd['m']:3d} n={dd['n']:4d} inside={dd['inside']:.2f} "
                  f"lm={str(dd['lm'])[:34]:34s} b={dd['b']} d={dd['d']}")
        report[islname] = dict(population_segments=sum(len(v) for v in pop.values()),
                               population_materials=len(pop),
                               results=res, top_materials=detail)
    json.dump(report, open(OUT, "w"), indent=1)
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
