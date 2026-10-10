#!/usr/bin/env python3
"""Round-7 ask 1 — the LIGHTMAP page-type x |s121| table (round-6 tabulated
the DIFFUSE axis; this is the axis that was actually asked), plus the two
follow-ups: the multi-wrap check for |s121|>1 materials under the shipped
chain, and the "s121 as diffuse tiling scale" density test.

Parts:
  1. TABLE  -- every LightMapDC material of both islands: LightMap page
     identity (BakeGroup_* area bake vs named tiling texture vs none) x
     |s121| bin (<=1, 1-4, >4), with segment counts and the round-6 page
     type of the LM page.  The question: do the |s121|>1 materials sample
     BakeGroup_* pages (=> an area bake)?
  2. WRAPS  -- the honest replacement for the transect-autocorrelation
     test.  Under the shipped chain pageUV = frac(w*s121 + s145), a
     segment whose packed-UV span is delta re-visits the same bake texels
     |s|*delta times; the sampled luminance is therefore EXACTLY periodic
     in w for ANY page content (chain-forced), so an ACF cannot test page
     content -- what matters is the wrap COUNT per segment:
        wraps_u = per-segment w-span(u) * |s121.x|   (same for v)
     wraps >= ~1.5  => the bake repeats across that segment (unphysical
     for a BakeGroup_* area bake).  wraps ~ 1   => single wrap, chain
     plausible.  wraps << 1 => sub-rect sampling, chain plausible.
     Measured per segment for BOTH packed words (w3 = word at +12, w4 =
     word at +16) since which word feeds Coord1 is exactly what is in
     question.  Control: |s121|<=1 materials under the same metric.
     Also: pooled chain-UV page coverage and cross-block centroid spread
     (a real per-slab bake gives different slabs different rects; the
     shipped chain gives every segment of a material the SAME sampling
     pattern up to w-offsets).
  3. DENSITY -- reading B: s121 as the DIFFUSE tiling scale.  For each
     questioned material's flat segments, regress world xy on the packed
     u (per word) -> meters per UV unit -> texel density under identity
     (shipped diffuse reading) vs |s121|-multiplied (reading B).
     Reference band: the same identity density over |s121|<=1 LightMapDC
     materials' flat segments.

Outputs: extraction/re/round7_lm_pages.json + stdout tables.
"""
import collections
import json
import random
import struct
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, "/home/z/my-project/repo/extraction/scripts")
sys.path.insert(0, "/home/z/my-project/repo/extraction/re")
from export_zone import ISLANDS, find_png  # noqa
from round4_street_evidence import TexData, stem_of, m40_list  # noqa

RE = "/home/z/my-project/repo/extraction/re"
ZONE = "/home/z/my-project/work/zone"
rng = random.Random(7018)


# ---------------------------------------------------------------- data
def slots_of(islname):
    d = open(f"{ZONE}/{islname}/batch_info.bin", "rb").read()
    stride = struct.unpack_from("<I", d, 0)[0]
    M = (len(d) - 4) // stride
    out = []
    for m in range(M):
        rec = d[4 + stride * m: 4 + stride * (m + 1)]
        out.append(dict(s121=struct.unpack_from("<3f", rec, 121),
                        s145=struct.unpack_from("<3f", rec, 145),
                        s109=struct.unpack_from("<3f", rec, 109),
                        s133=struct.unpack_from("<3f", rec, 133)))
    return out


def parse_island_w34(name):
    """parse_island with BOTH packed words kept (filters identical to
    export_zone.parse_island / round4_street_evidence.m40_list)."""
    lod = open(f"{ZONE}/{name}/lod_data.bin", "rb").read()
    lt = open(f"{ZONE}/{name}/lod_table.bin", "rb").read()
    u = struct.unpack(f"<{len(lt)//4}I", lt)
    n = u[0]
    pairs = [(u[1 + 2 * k], u[2 + 2 * k]) for k in range(n)]
    out = []
    for off, sz in pairs:
        data_off, four, vb, ib = struct.unpack_from("<4I", lod, off + 68)
        if four != 4:
            continue
        vstart = data_off + 4
        istart = vstart + vb
        idx = np.frombuffer(lod[istart:istart + ib], "<u2").astype(np.int32)
        real = idx[idx != 0xffff]
        mx = int(real.max()) if len(real) else 0
        stride = None
        for s in (24, 20, 32):
            if vb % s == 0 and mx < vb // s:
                t = np.frombuffer(lod[vstart:vstart + vb], "<f4").reshape(
                    -1, s // 4)[:, :3]
                if np.isfinite(t).all() and np.abs(t).max() < 6000:
                    stride = s
                    break
        if stride is None:
            continue
        nv = vb // stride
        v = np.frombuffer(lod[vstart:vstart + vb], "<f4").reshape(
            nv, stride // 4)
        words = np.frombuffer(lod[vstart:vstart + vb], "<u4").reshape(
            nv, stride // 4)
        out.append(dict(pos=v[:, :3].copy(),
                        w3=words[:, 3].copy(), w4=words[:, 4].copy(),
                        idx=real.astype(np.uint32)))
    return out


def deq(word_arr):
    """u32 -> (u, v) in [0,1]."""
    a = word_arr.astype(np.int64)
    return ((a & 0xffff) / 65535.0, (a >> 16) / 65535.0)


def page_class(lm_stem):
    if not lm_stem:
        return "none"
    if lm_stem.startswith("BakeGroup"):
        return "BakeGroup_*"
    return "named"


def smax_of(s121):
    return max(abs(s121[0]), abs(s121[1]))


def bin_of(smax):
    return "<=1" if smax <= 1.0 else ("1-4" if smax <= 4.0 else ">4")


def tex_w(stem):
    p = find_png(stem)
    if p is None:
        return None
    with Image.open(p) as im:
        return im.size[0]


def flat_ok(seg):
    p = seg["pos"]
    zr = float(np.ptp(p[:, 2]))
    return zr < max(2.0, 0.06 * float(np.ptp(p[:, :2])))


def seg_spans(seg):
    """Per-segment packed-UV spans for both words: dict of spans."""
    u3, v3 = deq(seg["w3"])
    u4, v4 = deq(seg["w4"])
    return dict(w3u=float(np.ptp(u3)), w3v=float(np.ptp(v3)),
                w4u=float(np.ptp(u4)), w4v=float(np.ptp(v4)))


def wraps_of(seg, s121):
    sp = seg_spans(seg)
    return dict(
        w3u=sp["w3u"] * abs(s121[0]), w3v=sp["w3v"] * abs(s121[1]),
        w4u=sp["w4u"] * abs(s121[0]), w4v=sp["w4v"] * abs(s121[1]))


def coverage_of(segs, s, o, word, n=16):
    occ = np.zeros((n, n), bool)
    for seg in segs:
        uu, vv = deq(seg[word])
        u2 = np.mod(uu * s[0] + o[0], 1.0)
        v2 = np.mod(vv * s[1] + o[1], 1.0)
        i = np.clip((v2 * n).astype(int), 0, n - 1)
        j = np.clip((u2 * n).astype(int), 0, n - 1)
        occ[i, j] = True
    return round(float(occ.mean()), 3)


def meters_per_unit(seg, word):
    """1-D fit: world xy displacement per unit of packed u.  Returns
    meters per u-unit, or None if the u-span is degenerate."""
    uu, _ = deq(seg[word])
    if np.ptp(uu) < 0.05:
        return None
    G = np.column_stack([uu, np.ones(len(uu))])
    coef, *_ = np.linalg.lstsq(G, seg["pos"][:, :2], rcond=None)
    return float(np.linalg.norm(coef[0]))


def verdict_of(wraps):
    m = wraps
    if m >= 1.5:
        return "MULTI-WRAP"
    if m >= 0.5:
        return "single-ish"
    return "sub-rect"


# ------------------------------------------------------------------ main
def main():
    report = {}
    for islname in ISLANDS:
        print(f"\n########## {islname}")
        rows = json.load(open(f"{RE}/runtime_mats_{islname}.json"))
        tech = [r.get("technique", "").split("-fx_")[0].lstrip("#")
                for r in rows]
        names = [r.get("name", f"m{m}") for m, r in enumerate(rows)]
        slots = slots_of(islname)
        m40s = m40_list(islname)
        segcount = collections.Counter(m40s)
        lm = [m for m in range(len(rows)) if tech[m] == "LightMapDC"]
        ptypes = {p["stem"]: p["type"] for p in
                  json.load(open(f"{RE}/round6_pagetypes.json"))["pages"]}

        # ---------------- part 1: the table
        tab = collections.defaultdict(lambda: dict(mats=0, segs=0))
        qmats = []
        for m in lm:
            smax = smax_of(slots[m]["s121"])
            pc = page_class(stem_of(rows[m].get("LightMap")))
            cell = tab[(pc, bin_of(smax))]
            cell["mats"] += 1
            cell["segs"] += segcount.get(m, 0)
            if smax > 1.0:
                qmats.append((m, smax))
        qmats.sort(key=lambda x: -x[1])
        print("-- LightMap page identity x |s121| (LightMapDC materials):")
        print(f"   {'page class':12s} {'<=1':>16s} {'1-4':>16s} {'>4':>16s}"
              f"     (mats/segs)")
        for pc in ("BakeGroup_*", "named", "none"):
            cells = [tab[(pc, b)] for b in ("<=1", "1-4", ">4")]
            print(f"   {pc:12s} " + " ".join(
                f"{c['mats']:>6d}/{c['segs']:<9d}" for c in cells))
        detail = []
        for m, smax in qmats:
            lm_stem = stem_of(rows[m].get("LightMap"))
            detail.append(dict(
                m=m, name=names[m], smax=round(smax, 3),
                s121=[round(v, 4) for v in slots[m]["s121"][:2]],
                s145=[round(v, 4) for v in slots[m]["s145"][:2]],
                diffuse=rows[m].get("DiffuseMap"), lm=lm_stem,
                lm_page_type=ptypes.get(lm_stem),
                segs=segcount.get(m, 0)))
        nq = collections.Counter(bin_of(s) for _, s in qmats)
        nbake = sum(1 for m, _ in qmats
                    if page_class(stem_of(rows[m].get("LightMap")))
                    == "BakeGroup_*")
        print(f"-- |s121|>1 materials: {len(detail)} "
              f"(1-4: {nq['1-4']}, >4: {nq['>4']}); "
              f"BakeGroup_* pages: {nbake}/{len(detail)}")
        for d in detail[:14]:
            print(f"   m{d['m']:3d} |s|={d['smax']:7.3f} "
                  f"dif={str(d['diffuse'])[:30]:30s} "
                  f"lm={str(d['lm'])[:36]:36s} segs={d['segs']}")

        # ---------------- segments
        segs = parse_island_w34(islname)
        assert len(segs) == len(m40s)
        by_mat = collections.defaultdict(list)
        for i, sgm in enumerate(segs):
            by_mat[m40s[i]].append(sgm)

        # word3 vs word4 relationship
        corr_w, diff_w = [], []
        for sgm in segs[:: max(1, len(segs) // 400)]:
            a3, _ = deq(sgm["w3"])
            a4, _ = deq(sgm["w4"])
            if np.std(a3) > 1e-6 and np.std(a4) > 1e-6:
                corr_w.append(float(np.corrcoef(a3, a4)[0, 1]))
            diff_w.append(float(np.mean(np.abs(a3 - a4))))
        print(f"\n-- word3-vs-word4 (u-axis): corr median "
              f"{np.median(corr_w):.3f}, mean|diff| median "
              f"{np.median(diff_w):.3f}")

        # ---------------- part 2: per-segment wraps
        def wraps_block(matlist, label):
            out = {}
            print(f"-- per-segment wraps ({label}): median over segments of "
                  f"span*|s| per axis (w4 = shipped chain word)")
            for m, smax in matlist:
                sgs = by_mat.get(m, [])
                if not sgs:
                    continue
                s121 = slots[m]["s121"]
                agg = collections.defaultdict(list)
                for sg in sgs:
                    for k, v in wraps_of(sg, s121).items():
                        agg[k].append(v)
                med = {k: round(float(np.median(v)), 2)
                       for k, v in agg.items()}
                mx = {k: round(float(np.max(v)), 2) for k, v in agg.items()}
                lm_stem = stem_of(rows[m].get("LightMap"))
                v4 = verdict_of(med["w4u"])
                v3 = verdict_of(med["w3u"])
                out[m] = dict(name=names[m], smax=round(smax, 3), n_segs=len(sgs),
                              median=med, maximum=mx,
                              verdict_w4=v4, verdict_w3=v3, lm=lm_stem)
                print(f"   m{m:3d} |s|={smax:7.2f} n={len(sgs):3d} "
                      f"w4u={med['w4u']:6.2f} w4v={med['w4v']:6.2f} "
                      f"w3u={med['w3u']:6.2f} w3v={med['w3v']:6.2f} "
                      f"(max w4u {mx['w4u']:6.2f})  w4:{v4:11s} w3:{v3}")
            return out

        wr = wraps_block(qmats, "|s121|>1 materials with segments")
        ctrl_mats = [(m, smax_of(slots[m]["s121"])) for m in lm
                     if smax_of(slots[m]["s121"]) <= 1.0 and by_mat.get(m)]
        rng.shuffle(ctrl_mats)
        wc = wraps_block(ctrl_mats[:15], "|s121|<=1 controls")

        # pooled coverage + spread for questioned materials
        cov = {}
        for m, smax in qmats:
            sgs = by_mat.get(m, [])
            if not sgs:
                continue
            cen = np.array([sg["pos"][:, :2].mean(0) for sg in sgs])
            spread = float(np.linalg.norm(np.ptp(cen, axis=0)))
            cov[m] = dict(coverage_w4=coverage_of(sgs, slots[m]["s121"],
                                                  slots[m]["s145"], "w4"),
                          coverage_w3=coverage_of(sgs, slots[m]["s121"],
                                                  slots[m]["s145"], "w3"),
                          centroid_spread=round(spread, 1),
                          n_segs=len(sgs))

        # ---------------- part 3: density (reading B)
        def dens_block(matlist, label):
            out = []
            skips = collections.Counter()
            for m, smax in matlist:
                dif = stem_of(rows[m].get("DiffuseMap"))
                W = tex_w(dif) if dif else None
                if not W:
                    skips["no_diffuse"] += 1
                    continue
                sx = abs(slots[m]["s121"][0])
                ids, bs, m3s, n = [], [], [], 0
                for sg in by_mat.get(m, []):
                    if len(sg["idx"]) < 512:
                        skips["small_idx"] += 1
                        continue
                    if not flat_ok(sg):
                        skips["not_flat"] += 1
                        continue
                    if float(np.ptp(sg["pos"][:, :2])) < 8.0:
                        skips["small_footprint"] += 1
                        continue
                    mp4 = meters_per_unit(sg, "w4")
                    mp3 = meters_per_unit(sg, "w3")
                    if not mp4 or mp4 <= 0.5:
                        skips["degenerate_fit"] += 1
                        continue
                    ids.append(W / mp4)
                    bs.append(sx * W / mp4)
                    if mp3 and mp3 > 0.5:
                        m3s.append(sx * W / mp3)
                    n += 1
                if ids:
                    out.append(dict(
                        m=m, name=names[m], diffuse_w=W, sx=round(sx, 2),
                        identity_w4=round(float(np.mean(ids)), 1),
                        readingB_w4=round(float(np.mean(bs)), 1),
                        readingB_w3=round(float(np.mean(m3s)), 1)
                        if m3s else None,
                        n_segs_used=n))
                else:
                    skips["no_usable_seg"] += 1
            if label == "questioned":
                print(f"   (density skips: {dict(skips)})")
            return out

        ref_dens = dens_block(ctrl_mats, "reference")
        refv = np.array([d["identity_w4"] for d in ref_dens])
        if len(refv):
            print(f"\n-- diffuse texel density reference (|s121|<=1, "
                  f"identity reading, {len(refv)} flat segs): median "
                  f"{np.median(refv):.1f}, IQR {np.percentile(refv, 25):.1f}-"
                  f"{np.percentile(refv, 75):.1f}, p10-p90 "
                  f"{np.percentile(refv, 10):.1f}-{np.percentile(refv, 90):.1f}"
                  f" texels/u")
        dens = dens_block(qmats, "questioned")
        print(f"-- questioned materials, identity vs readingB densities:")
        for d in dens:
            print(f"   m{d['m']:3d} {d['name'][:26]:26s} W={d['diffuse_w']:4d} "
                  f"|sx|={d['sx']:6.2f}  identity {d['identity_w4']:7.1f}  "
                  f"readingB(w4) {d['readingB_w4']:7.1f}  "
                  f"readingB(w3) {str(d['readingB_w3']):>7s} texels/u")

        report[islname] = dict(
            table={f"{pc}|{b}": dict(v) for (pc, b), v in tab.items()},
            questioned=detail,
            word3_word4=dict(corr_median=round(float(np.median(corr_w)), 3),
                             meandiff_median=round(float(np.median(diff_w)),
                                                   3)),
            wraps_questioned=wr, wraps_control=wc, coverage=cov,
            density_ref=dict(n=len(refv),
                             median=round(float(np.median(refv)), 1),
                             iqr=[round(float(np.percentile(refv, 25)), 1),
                                  round(float(np.percentile(refv, 75)), 1)],
                             p10p90=[round(float(np.percentile(refv, 10)), 1),
                                     round(float(np.percentile(refv, 90)), 1)])
            if len(refv) else None,
            density_questioned=dens)

    json.dump(report, open(f"{RE}/round7_lm_pages.json", "w"), indent=1)
    print(f"\nwrote {RE}/round7_lm_pages.json")


if __name__ == "__main__":
    main()
