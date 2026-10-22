# s48 T6 — zone-scale browser render: PASS (corr 0.9999 vs Python)

## What runs in the browser (city_zone.html, branch-only, NOT deployed)

All 1,526 GothamCity segments from the user's zip: declaration-driven decode
(END-offset batch_info, no stride probes), bindings + effects from the COMPILED
instance table (no source.dae XML anywhere), ETC1 textures with an LRU cache
(cap 20 RGBA textures incl. SPLIT alpha pages), per-effect shading —
LightMapDC Diff*(LM*2); AlphaMasking Diff*(LM*2+1) with SPLIT alpha.r discard
< 0.3; SimpleAdditive/StandardDiffuseDC Diff*vColor(Color0); NormalSpecOverbright/
NV_Glass/LightmapVCBlendDC rendered diffuse-only (documented deviation, applied
identically on the Python side). Orthographic top-down camera over the zone
AABB (x[-1620.0, 185.2] z[-1312.7, -246.8], 0.5673 px/u), 1024x605, painter
order = global ascending mean height with deterministic (seg, tri) tie-break.

## Numbers (headless Chromium, release zip path)

| metric | browser | python reference |
|---|---|---|
| load (zip->ready incl. compiled table) | 2,372-2,456 ms | n/a |
| decode (all segs + painter build + sort) | 71-86 ms | ~0.5 s |
| raster (368,749 tris; 346,772 drawn) | 46 s software | 101 s numpy |
| triangles | 368,749 total / 346,772 drawn | identical |
| painter texture binds | 30,500 | 30,500 (identical) |
| texture LRU | 2,147 misses / 2,127 evictions | 549 / 508 |
| peak JS heap | 1,373 MB | n/a |
| **pixel corr (grayscale, 619,520 px)** | **0.9999** | — |

The painter heads match BIT-IDENTICALLY (e.g. seg 36 mat 299 z=-24.235759735107422;
seg 537 mat 31 z=-19.440109888712566) — same order, same binds, corr 0.99994.

## Bugs found en route (all fixed, worth remembering)

1. Index array under-allocation: `new Uint32Array(ib/6)` (triangle count) instead
   of `ib/2` (index count) silently dropped the last two-thirds of every
   segment's triangles AND made 2/3 of the z-mean reads NaN (comparator NaN ->
   insertion order). Symptom was tris_drawn matching while corr sat at 0.46.
2. UV transform applied at sample time must be (raw/32767*0.5+0.5) with the
   y-flip — storing raw snorm without the transform corr 0.29.
3. Python-side alpha lookup needed its own dims (1024 alpha vs 2048 rgb).
4. Painter tie-break made explicit on both sides: key=(zm, seg, tri) via
   np.lexsort / comparator.

## Honest notes

- Peak heap 1,373 MB is dominated by the LRU decode churn (cap 20 x up to
  16 MB RGBA + zip/lod buffers + per-seg Float64 z arrays); a production path
  would store RGB565 and cap lower.
- The render is DARK (mean luminance 5.2/255) — the engine's exact pre-fog math
  (T1); the game's visible brightness comes from fog + post, which a top-down
  bake-style render deliberately excludes.
- Draw-call accounting: 1,526 segment batches (one per seg), 30,500 painter-order
  texture binds, 346,772 triangles drawn.

## Artifacts

s48_t6_render.py (+ s48_t6_render.json, s48_t6_gate.py + s48_t6_gate.json),
playable/city_zone.html (branch), s48_ref_zone.png untracked in the worktree.
