#!/usr/bin/env python3
"""Round-6 ask 3 — THE 109/133 TILING PATTERN.

batch_info records carry four consecutive vec3 slots at byte offsets
109 / 121 / 133 / 145.  For the street LightMapDC path the working pair is
scale@121.xy + offset@145.xy (wrapped); slots 109/133 were left UNRESOLVED
in session 18 (dequant value 1/65535 in 9/227 + 5/141 LightMapDC records,
broad distribution otherwise; not a working uv0 transform).

This script asks the reviewer's tiling question directly:

  1. PER-TECHNIQUE SLOT CENSUS -- for each technique base x island, the
     fraction of records whose components at each slot are ~0, ~1/65535
     (u16 dequant), ~1, or "other" (with distribution stats).  If 109/133
     are Coord0 scaleoffset for OTHER techniques (per-technique layouts),
     the census should show dequant+offset structure concentrated there.
  2. QUANTIZATION / TILING STRUCTURE -- for each candidate (origin,
     extent) interpretation over LightMapDC materials:
        P_ship  o145 / s121    P_C2  o109 / s133    P_C3  o145 / s109
        P_C4    o133 / s121    P_C5  o133 / s109
     compute (a) grid alignment: best quantum q maximizing the fraction of
     values with |v*q - round(v*q)| < 0.01 (uniform null ~0.02 for any q),
     for origins and extents separately; (b) rect tiling: mean pairwise
     overlap of wrapped [o, o+s) rects and union coverage, against a
     permuted-origin null (K=24) -- with effect sizes.  A real per-material
     tile table should show strong grid alignment on BOTH origin and
     extent, and near-partition rects.
  3. THE dequant RECORDS THEMSELVES -- dump the 9+5 LightMapDC records with
     s109 ~ 1/65535 (name, all four vec3s) and test whether their s133 /
     o133 form plausible Coord0 scaleoffsets; plus the m90 anchor for
     reference.

Outputs: extraction/re/round6_slot_tiling.json + stdout tables.
"""
import collections
import json
import random
import struct
import sys

import numpy as np

sys.path.insert(0, "/home/z/my-project/repo/extraction/scripts")
sys.path.insert(0, "/home/z/my-project/repo/extraction/re")
from export_zone import ISLANDS  # noqa

RE = "/home/z/my-project/repo/extraction/re"
ZONE = "/home/z/my-project/work/zone"
DEQ = 1.0 / 65535.0
K_PERM = 24


def slots_of(islname):
    d = open(f"{ZONE}/{islname}/batch_info.bin", "rb").read()
    stride = struct.unpack_from("<I", d, 0)[0]
    M = (len(d) - 4) // stride
    # byte0 == per-section material id; the sequence restarts at 256
    # (two library sections) -- sequential read, as in round5_t3_chain.
    out = []
    for m in range(M):
        rec = d[4 + stride * m: 4 + stride * (m + 1)]
        out.append(dict(s109=struct.unpack_from("<3f", rec, 109),
                        s121=struct.unpack_from("<3f", rec, 121),
                        s133=struct.unpack_from("<3f", rec, 133),
                        s145=struct.unpack_from("<3f", rec, 145)))
    return out


def classify(v):
    if abs(v) < 1e-6:
        return "zero"
    if abs(v - DEQ) < 3e-7:
        return "dequant"
    if abs(v - 1.0) < 1e-6:
        return "one"
    return "other"


def best_quantum(vals, eps=0.01, qmax=4096):
    """Best q: fraction of vals aligning to a 1/q grid (|v*q - round|<eps).

    Values with |v| < 0.01 are excluded (they align to EVERY grid
    trivially -- the near-zero/dequant junk would otherwise fake q=1
    alignment).  Uniform expectation is ~2*eps for any q."""
    vals = np.asarray([v for v in vals if np.isfinite(v) and abs(v) >= 0.01])
    if len(vals) == 0:
        return dict(q=None, align=None, n=0, median=0.0)
    best = (0, None)
    for q in list(range(2, 65)) + [96, 128, 192, 256, 384, 512, 1024, 2048,
                                   4096]:
        x = vals * q
        frac = float(np.mean(np.abs(x - np.round(x)) < eps))
        if frac > best[0]:
            best = (frac, q)
    return dict(q=best[1], align=round(best[0], 3), n=len(vals),
                median=round(float(np.median(np.abs(vals))), 4),
                uniform_null=round(2 * eps, 3))


def adjacency(origins, extents, rng, tol=0.012):
    """Tiling signature: does material j's left edge continue material i's
    right edge (mod 1) for a reasonable fraction of pairs?  Rect tables
    packed by a bake tool show high edge-adjacency; random placements do
    not.  Returns obs rate + permuted-origin null."""
    O = np.mod(np.asarray(origins, float), 1.0)
    S = np.asarray(extents, float)
    n = len(O)
    xr = np.mod(O[:, 0] + S[:, 0], 1.0)
    xl = O[:, 0]
    yu = np.mod(O[:, 1] + S[:, 1], 1.0)
    yd = O[:, 1]

    def rate(pair_kind="x"):
        cnt = 0
        tot = 0
        for i in range(n):
            if pair_kind == "x":
                d = np.abs(np.mod(xr[i] - xl, 1.0))
                d = np.minimum(d, 1.0 - d)
                d[i] = 1.0
            else:
                d = np.abs(np.mod(yu[i] - yd, 1.0))
                d = np.minimum(d, 1.0 - d)
                d[i] = 1.0
            tot += 1
            cnt += int((d < tol).any())
        return cnt / tot

    def null_rate(pair_kind):
        out = []
        for _ in range(K_PERM):
            perm = np.random.default_rng(
                int(rng.random() * 2 ** 31)).permutation(n)
            if pair_kind == "x":
                out.append(ratepair(xr[perm], xl))
            else:
                out.append(ratepair(yu[perm], yd))
        return float(np.mean(out)), float(np.std(out))

    def ratepair(rights, lefts):
        n2 = len(rights)
        cnt = 0
        for i in range(n2):
            d = np.abs(np.mod(rights[i] - lefts, 1.0))
            d = np.minimum(d, 1.0 - d)
            d[i] = 1.0
            cnt += int((d < tol).any())
        return cnt / n2

    ox, sx = rate("x"), None
    nx, sdx = null_rate("x")
    oy = rate("y")
    ny, sdy = null_rate("y")
    return dict(frac_right_edge_continued=round(ox, 3),
                null_x=round(nx, 3), null_x_sd=round(sdx, 3),
                frac_top_edge_continued=round(oy, 3),
                null_y=round(ny, 3), null_y_sd=round(sdy, 3))


def rect_stats(origins, extents, rng):
    """Wrapped-rect overlap/coverage + permuted-origin null."""
    O = np.asarray(origins, float) % 1.0
    S = np.asarray(extents, float)
    n = len(O)
    # wrapped rects may exceed the page: split into at most 4 sub-rects
    def subrects(o, s):
        x0, y0 = o
        w, h = s
        out = []
        for (ox, ow) in split1d(x0 % 1.0, w):
            for (oy, oh) in split1d(y0 % 1.0, h):
                out.append((ox, oy, ow, oh))
        return out

    def split1d(a, w):
        w = min(w, 4.0)
        first = min(1.0 - a, w)
        out = [(a, first)] if first > 1e-9 else []
        rem = w - first
        while rem > 1e-9:
            seg = min(1.0, rem)
            out.append((0.0, seg))
            rem -= seg
        return out

    R = [subrects(O[i], S[i]) for i in range(n)]
    # mean pairwise overlap (sampled if large)
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    if len(pairs) > 20000:
        idx = rng.sample(range(len(pairs)), 20000)
        pairs = [pairs[k] for k in idx]

    def inter(ra, rb):
        ax, ay, aw, ah = ra
        bx, by, bw, bh = rb
        w = min(ax + aw, bx + bw) - max(ax, bx)
        h = min(ay + ah, by + bh) - max(ay, by)
        return max(0.0, w) * max(0.0, h)

    def mean_overlap(rectlist):
        if not pairs:
            return 0.0
        tot = 0.0
        for i, j in pairs:
            best = 0.0
            for ra in rectlist[i]:
                for rb in rectlist[j]:
                    best = max(best, inter(ra, rb))
            tot += best
        return tot / len(pairs)

    obs = mean_overlap(R)
    grid = np.zeros((256, 256), bool)
    for rl in R:
        for (x, y, w, h) in rl:
            i0, i1 = int(y * 255), min(255, int((y + h) * 255))
            j0, j1 = int(x * 255), min(255, int((x + w) * 255))
            if i1 >= i0 and j1 >= j0:
                grid[i0:i1 + 1, j0:j1 + 1] = True
    cover = float(grid.mean())
    null = []
    for _ in range(K_PERM):
        perm = list(range(n))
        random.Random(rng.random()).shuffle(perm)
        Rp = [R[perm[i]] for i in range(n)]
        null.append(mean_overlap(Rp))
    nm, ns = float(np.mean(null)), float(np.std(null))
    return dict(mean_pairwise_overlap=round(obs, 4),
                null_mean=round(nm, 4), null_sd=round(ns, 4),
                z=(round((obs - nm) / (ns + 1e-9), 1) if ns > 0 else None),
                union_coverage=round(cover, 3), n_materials=n)


def main():
    rng = random.Random(6018)
    report = {}
    for islname in ISLANDS:
        print(f"\n########## {islname}")
        rows = json.load(open(f"{RE}/runtime_mats_{islname}.json"))
        tech = [r.get("technique", "").split("-fx_")[0].lstrip("#")
                for r in rows]
        names = [r.get("name", f"m{m}") for m, r in enumerate(rows)]
        slots = slots_of(islname)
        M = len(slots)
        assert M == len(rows)

        # ---------- 1. per-technique census
        cens = collections.defaultdict(list)
        for m in range(M):
            cens[tech[m]].append(m)
        census = {}
        print("-- slot census by technique (components over .xy of each "
              "vec3):")
        print(f"   {'technique':22s} {'n':>4s} | "
              f"s109 zero/deq/one/other | s121 ... | s133 ... | s145 ...")
        for t, ms in sorted(cens.items(), key=lambda kv: -len(kv[1])):
            row = {}
            line = []
            for key in ("s109", "s121", "s133", "s145"):
                comps = [slots[m][key][c] for m in ms for c in (0, 1)]
                cl = collections.Counter(classify(v) for v in comps)
                others = [v for v in comps if classify(v) == "other"]
                row[key] = dict(
                    zero=cl.get("zero", 0), dequant=cl.get("dequant", 0),
                    one=cl.get("one", 0), other=cl.get("other", 0),
                    other_med=round(float(np.median(others)), 4)
                    if others else None,
                    other_p10=round(float(np.percentile(others, 10)), 5)
                    if others else None,
                    other_p90=round(float(np.percentile(others, 90)), 5)
                    if others else None)
                line.append(f"{cl.get('zero',0)}/{cl.get('dequant',0)}/"
                            f"{cl.get('one',0)}/{cl.get('other',0)}")
            census[t] = dict(n=len(ms), slots=row)
            print(f"   {t:22s} {len(ms):4d} | " + " | ".join(line))

        # ---------- LightMapDC subset
        lm = [m for m in range(M) if tech[m] == "LightMapDC"]
        deq109 = [m for m in lm
                  if classify(slots[m]["s109"][0]) == "dequant"
                  and classify(slots[m]["s109"][1]) == "dequant"]
        deq121 = [m for m in lm
                  if classify(slots[m]["s121"][0]) == "dequant"
                  and classify(slots[m]["s121"][1]) == "dequant"]
        print(f"\n-- LightMapDC: {len(lm)} materials; s121~dequant "
              f"{len(deq121)}; s109~dequant {len(deq109)} "
              f"(session-18 said 9/227 + 5/141)")

        # overlap of dequant flags: two-stage reading
        both = sorted(set(deq109) & set(deq121))
        only109 = sorted(set(deq109) - set(deq121))
        print(f"   records with BOTH s109 and s121 dequant: {len(both)} "
              f"{both[:12]}")
        print(f"   records with s109 dequant but s121 NOT: {len(only109)}")

        # ---------- 2. tiling candidates
        def vals(key, comp, subset):
            return [slots[m][key][comp] for m in subset]

        cand = {}
        for pname, okey, skey in (("P_ship_o145_s121", "s145", "s121"),
                                  ("P_C2_o109_s133", "s109", "s133"),
                                  ("P_C3_o145_s109", "s145", "s109"),
                                  ("P_C4_o133_s121", "s133", "s121"),
                                  ("P_C5_o133_s109", "s133", "s109")):
            subset = [m for m in lm
                      if abs(slots[m][skey][0]) > 1e-4
                      and abs(slots[m][skey][1]) > 1e-4
                      and classify(slots[m][skey][0]) != "dequant"
                      and classify(slots[m][skey][1]) != "dequant"]
            if len(subset) < 8:
                cand[pname] = dict(n_materials=len(subset),
                                   note="too few non-degenerate extents")
                continue
            ox, oy = vals(okey, 0, subset), vals(okey, 1, subset)
            sx, sy = vals(skey, 0, subset), vals(skey, 1, subset)
            qox, qoy = best_quantum([v % 1.0 for v in ox]), \
                best_quantum([v % 1.0 for v in oy])
            qsx, qsy = best_quantum(sx), best_quantum(sy)
            rs = rect_stats(list(zip(ox, oy)), list(zip(sx, sy)), rng)
            adj = adjacency(list(zip(ox, oy)), list(zip(sx, sy)), rng)
            cand[pname] = dict(
                n_materials=len(subset),
                origin_quantum=dict(x=qox, y=qoy),
                extent_quantum=dict(x=qsx, y=qsy),
                rects=rs, adjacency=adj)
            print(f"\n   {pname}  (n={len(subset)}):")
            print(f"     origin grid: x q={qox['q']} align={qox['align']} "
                  f"(n={qox['n']}, med|v|={qox['median']})  "
                  f"y q={qoy['q']} align={qoy['align']} (n={qoy['n']})")
            print(f"     extent grid: x q={qsx['q']} align={qsx['align']} "
                  f"(n={qsx['n']}, med|v|={qsx['median']})  "
                  f"y q={qsy['q']} align={qsy['align']} (n={qsy['n']})")
            print(f"     rects: overlap {rs['mean_pairwise_overlap']} vs "
                  f"perm-null {rs['null_mean']}±{rs['null_sd']} "
                  f"(z={rs['z']}), union coverage {rs['union_coverage']}")
            print(f"     adjacency: right-edge {adj['frac_right_edge_continued']}"
                  f" vs null {adj['null_x']}±{adj['null_x_sd']}; top-edge "
                  f"{adj['frac_top_edge_continued']} vs null "
                  f"{adj['null_y']}±{adj['null_y_sd']}")

        # ---------- 3. the dequant-s109 records dumped
        dump = []
        for m in deq109:
            dump.append(dict(m=m, name=names[m],
                             s109=[round(v, 8) for v in slots[m]["s109"]],
                             s121=[round(v, 8) for v in slots[m]["s121"]],
                             s133=[round(v, 8) for v in slots[m]["s133"]],
                             s145=[round(v, 8) for v in slots[m]["s145"]]))
            print(f"   m{m:3d} {names[m][:34]:34s} s109={slots[m]['s109']} "
                  f"s121={slots[m]['s121']} s133={slots[m]['s133']} "
                  f"s145={slots[m]['s145']}")

        # m90 anchor (session-17 tile-rect evidence)
        if len(lm) > 90:
            m90 = slots[90]
            print(f"\n   m90 anchor: s109={m90['s109']} s121={m90['s121']} "
                  f"s133={m90['s133']} s145={m90['s145']}")

        # ---------- 2b. magnitude buckets for s109/s133 over LightMapDC
        #           + WHERE the dequant records live (name family)
        def buckets(key):
            comps = [slots[m][key][c] for m in lm for c in (0, 1)]
            b = collections.Counter()
            for v in comps:
                av = abs(v)
                if av < 1e-6:
                    b["zero"] += 1
                elif av < 1e-4:
                    b["dequant-ish (1e-6..1e-4)"] += 1
                elif av < 0.01:
                    b["small (1e-4..1e-2)"] += 1
                elif av < 1.0:
                    b["mid (1e-2..1)"] += 1
                else:
                    b["large (>1)"] += 1
            return dict(b)

        b109, b133 = buckets("s109"), buckets("s133")
        print(f"\n-- LightMapDC |s109| buckets: {dict(b109)}")
        print(f"-- LightMapDC |s133| buckets: {dict(b133)}")

        stem_prefix = collections.Counter()
        for m in deq109:
            nm = names[m]
            stem_prefix[nm.split("_")[0] if "_" in nm else nm] += 1
        print(f"-- dequant-s109 records by stem prefix: {dict(stem_prefix)}")

        # tiles_* family: the s121=0.5 half-page tiling
        tiles = [m for m in lm if names[m].startswith("tiles")]
        t121 = collections.Counter(
            tuple(round(v, 3) for v in slots[m]["s121"][:2]) for m in tiles)
        print(f"-- tiles_* LightMapDC materials: {len(tiles)}; their s121 "
              f"scale values: {dict(t121)}")

        report[islname] = dict(
            census=census,
            lm_n=len(lm), lm_deq109=len(deq109), lm_deq121=len(deq121),
            both_deq=both, only109=only109,
            candidates=cand, deq109_dump=dump,
            s109_buckets=b109, s133_buckets=b133,
            deq109_stem_prefixes=dict(stem_prefix),
            tiles=dict(n=len(tiles),
                       s121_values={str(k): v for k, v in t121.items()}),
            m90={k: list(v) for k, v in slots[90].items()} if lm else None)

    json.dump(report, open(f"{RE}/round6_slot_tiling.json", "w"), indent=1)
    print(f"\nwrote {RE}/round6_slot_tiling.json")


if __name__ == "__main__":
    main()
