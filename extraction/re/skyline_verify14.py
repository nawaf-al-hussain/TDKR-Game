#!/usr/bin/env python3
"""Consolidated skyline verification v14 — honest metrics only.

Round-2 external-Claude check 1 asked for a ZNCC sweep showing a single
sharp maximum at the record TRS.  Result of the investigation:

  * The session-13 "+0.66 ZNCC" is NOT a robust statistic.  The FFT-ZNCC
    normalizes over the shifted-grid-intersection window, whose extent
    depends on arbitrary framing choices (margin/grid extent).  Same data,
    same placement, same math:
        +0.6625  (zncc13b framing: sky local, grid union(street, sky_local),
                  mgn=340, read at record index)
        +0.1558  (sky shipped framing, read at d=0)
        +0.0284  (direct windowed Pearson over the sky support - the
                  framing-independent definition)
    The +0.66 is RETRACTED.  ZNCC of smoothed densities does not
    discriminate skyline placement in this city (both maps are one big
    blob; the correlation is city-shaped, exactly the broad-ridge risk).

  * The sharp evidence for the record TRS is:
      1. the engine record itself (0x14051 @ GothamCity.lvc 0x55545,
         disasm-proven read path: bool,objId,9f TRS,3b, mesh string,4c ->
         AddLowPolyLongDistanceNode) — the GAME's own placement,
      2. per-mesh NAME correspondence: the FP unit bdaes share mesh names
         with the assembly bdae; with both placed by the record TRS the
         same-named meshes must coincide (this script measures it),
      3. raw binary overlap (street vertex occupancy vs skyline roof
         footprint): discriminates large displacements (record 13.8k vs
         v13 7.4k cells); within +-60u it is plateau-like.

This script computes (2) and (3) on the shipped v14 GLBs and writes
extraction/re/skyline_verify14.json.
"""
import json
import os
import sys

import numpy as np
from scipy.signal import fftconvolve

RE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RE)
from val_skyline import (load_unit_game, rasterize_tris_xy, vert_occupancy,
                         MODELS, OUT, SKY_UNITS)

CELL = 1.0


def centroid_correspondence():
    """Per-prim nearest-centroid correspondence: FP units vs the assembly
    unit, both placed at the record TRS (shipped v14 GLBs).

    The GLBs pack each bdae's meshes as prims of ONE node, so there are no
    per-mesh names to match; instead every FP prim centroid must land on
    SOME assembly prim centroid.  The discriminative statistic is the MEAN
    DELTA VECTOR: a wrong frame shifts every prim the same way (coherent
    direction, magnitude = displacement); a correct frame gives ~zero mean
    with small scatter (LOD noise only)."""
    asm = load_unit_game("GC_island1_LongDist")
    A = np.array([p["game"].mean(0) for p in asm])[:, :2]
    out = {}
    for unit in ("GC_LongDist_Island1_FP1", "GC_LongDist_Island1_FP2",
                 "GC_LongDist_Island1_FP3"):
        prims = load_unit_game(unit)
        C = np.array([p["game"].mean(0) for p in prims])[:, :2]
        D = np.linalg.norm(C[:, None, :] - A[None, :, :], axis=2)
        nearest = D.argmin(1)
        d = D[np.arange(len(C)), nearest]
        mean_vec = (C - A[nearest]).mean(0)
        out[unit] = dict(
            n_prims=len(C),
            mean_abs=float(d.mean()), max_abs=float(d.max()),
            mean_vec=[float(mean_vec[0]), float(mean_vec[1])],
            mean_vec_norm=float(np.linalg.norm(mean_vec)),
            frac_lt_5u=float((d < 5.0).mean()),
            frac_lt_15u=float((d < 15.0).mean()),
        )
        print(f"{unit}: {len(C)} prims -> nearest assembly centroid |d| "
              f"mean {d.mean():.2f}u max {d.max():.2f}u; "
              f"mean vector ({mean_vec[0]:+.2f},{mean_vec[1]:+.2f}) "
              f"|{np.linalg.norm(mean_vec):.2f}u; <5u: {(d < 5).sum()}/{len(C)}")
    return out


def raw_overlap():
    """Binary overlap map: street vert occupancy vs skyline roof footprint,
    CELL=1, whole plane.  Values at the record (d=0), at the ±60u raw
    argmax, at identity, v13, and the global argmax."""
    street = [p for i in range(9)
              for p in load_unit_game(f"street_island1_{i:02d}")]
    sky = [p for u in SKY_UNITS for p in load_unit_game(u)]
    sv = np.vstack([p["game"] for p in street])[:, :2]
    lv = np.vstack([p["game"] for p in sky])[:, :2]
    mgn = 40.0
    origin = np.minimum(sv.min(0), lv.min(0)) - mgn
    shape = (int(np.ceil((max(sv[:, 1].max(), lv[:, 1].max()) - origin[1] + mgn) / CELL)),
             int(np.ceil((max(sv[:, 0].max(), lv[:, 0].max()) - origin[0] + mgn) / CELL)))
    Sm = vert_occupancy(street, origin, shape, CELL)
    Km, ntri = rasterize_tris_xy(sky, origin, shape, CELL)
    C = fftconvolve(Sm.astype(np.float32), Km[::-1, ::-1].astype(np.float32),
                    mode="full")
    Hs, Ws = Km.shape
    i0, j0 = Hs - 1, Ws - 1          # d = 0 == record (shipped)

    def at(dx, dy):
        ii, jj = i0 + int(round(dy / CELL)), j0 + int(round(dx / CELL))
        if 0 <= ii < C.shape[0] and 0 <= jj < C.shape[1]:
            return float(C[ii, jj])
        return None

    win = C[i0 - 60:i0 + 61, j0 - 60:j0 + 61]
    kk = np.unravel_index(np.argmax(win), win.shape)
    wdx, wdy = kk[1] - 60, kk[0] - 60
    gz = np.array(C)
    gk = np.unravel_index(np.argmax(gz), gz.shape)
    res = dict(
        record=at(0, 0),
        v13_delta=[588.31, 568.85],
        v13=at(588.31, 568.85),
        identity_delta=[730.0, 1250.0],
        identity=at(730.0, 1250.0),
        win60_argmax=dict(d=[int(wdx), int(wdy)], v=float(win[kk])),
        global_argmax=dict(d=[int(gk[1] - j0), int(gk[0] - i0)],
                           v=float(gz[gk])),
        sky_cells=int(Km.sum()), street_cells=int(Sm.sum()),
        grid=list(shape),
    )
    print("\nraw binary overlap (CELL=1):")
    print(f"  record d=(0,0):        {res['record']:10,.0f} cells")
    print(f"  identity d=(+730,+1250): {res['identity']:9,.0f}")
    print(f"  v13 d=(+588,+569):     {res['v13']:10,.0f}")
    print(f"  ±60u argmax d=({wdx:+d},{wdy:+d}): {win[kk]:10,.0f} "
          f"({100 * win[kk] / res['record']:.2f}% of record)")
    print(f"  global argmax d=({gk[1] - j0:+d},{gk[0] - i0:+d}): "
          f"{gz[gk]:10,.0f} ({100 * gz[gk] / res['record']:.2f}%)")

    # slice profile for the handoff (record ±100 diagonal + axes)
    prof = {}
    for ax in ("X", "Y"):
        prof[ax] = {d: at(d if ax == "X" else 0, 0 if ax == "X" else d)
                    for d in (-100, -60, -40, -20, -10, -5, -2, -1, 0, 1, 2,
                              5, 10, 20, 40, 60, 100)}
    res["profile"] = prof
    return res


def main():
    print("=" * 72)
    print("1) mesh-NAME correspondence (record placement, shipped GLBs)")
    print("=" * 72)
    names = centroid_correspondence()
    print()
    ov = raw_overlap()
    summary = dict(
        context="v14 verification of the 0x14051 record TRS (-730,-1250,0); "
                "ZNCC +0.66 retracted (framing-dependent window artifact; "
                "direct windowed Pearson at record = +0.028)",
        zncc_retraction=dict(
            fft_read_zncc13b_framing=0.6625,
            fft_read_shipped_framing=0.1558,
            direct_windowed_pearson_at_record=0.0284,
            direct_fullgrid_pearson_at_record=0.1425,
            direct_identity=0.0000, direct_v13=-0.0709,
            direct_sweep_argmax_635_158=0.1188,
        ),
        centroid_correspondence=names,
        raw_overlap=ov,
    )
    with open(os.path.join(RE, "skyline_verify14.json"), "w") as f:
        json.dump(summary, f, indent=1)
    print("\nsaved extraction/re/skyline_verify14.json")


if __name__ == "__main__":
    main()
