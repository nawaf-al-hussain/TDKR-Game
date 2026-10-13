# RE Session 23 (round 13) — 2026-10-13

## 0. State recovery — DIFFERENT this time

- Sandbox NOT fully reset: the previous session's disk was still
  materializing at session start (files appeared between `ls` and `du`).
- Session-22 bundles in download/bundles_s22/ SURVIVED and both verified:
  main_s22_inc.bundle -> main @ 7e96326 (requires 3ae66a2 ✓);
  ghpages_staged_s22.bundle -> gh-pages-staged @ c7f73c9 (requires f22b098 ✓).
  Fetched from them (not re-derived). bundles_s20/s21 also survived
  (superseded; deleted to free disk).
- Raw data survived: OBB zip SHA256 re-verified
  0510e54c128de0f52bebc6db41ea3e3a9556f666d5ca5bb09eb39880c213aa6f ✓ README.
  TDKR_data (.gla), zone bins re-extracted from l_gothamcity.gla (6 zones),
  534 decoded textures survived in work/TDKR_assets/textures_png.
- **PUSHED (first time in 7 rounds — user supplied a PAT this round):**
  main 3ae66a2 -> 7e96326 and gh-pages-staged -> NEW remote branch @ c7f73c9.
  Live gh-pages (v17 @ f22b098) deliberately NOT touched: live remains v17
  until the user merges gh-pages-staged.
- Disk was 100% full at session start; freed 5.5G by deleting re-derivable
  intermediates (download/TDKR_assets dup, apk_obb extract, old bundles).
- Two committed session-22 files were found CORRUPTED in-repo
  (batch_parser.py main() bad list-comp; raycast_t3.py bracket mangle) —
  their result JSONs survived and validate; parsers re-built below.

## 1. T1 — diffuse-channel test of the engine chain (scripts/t1_diffuse.py, t1_class42.py)

Engine Coord0 = w3_raw*s109+s121 (repeat-wrap) vs v17 uv0 = w4 dequant
(exporter ships words[:,4]; for (4,1)/(3,1) records word4 is Normal/Color0 —
structurally invalid as a diffuse uv).

Counts: isl1 134 diffuse-bound materials, 125 with scale != 1, 1484 segments
on them; isl2 88/83/984. Class census (segments): isl1 (4,2) 1092,
(4,1) 325, (3,1) 95, (3,0) 5; isl2 (4,2) 658, (4,1) 337, (3,1) 25.

Enrichment (obs non-empty / uniform rate, mask_A = alpha<64 | lum<20,
permuted-parameter null K=100, pooled per family, ALL classes):
  isl1 roads engine 1.116 (z +1.90) v17 1.146 (z +2.44); billboards engine
  0.949 (z -1.03) v17 1.255 (z +1.12); most families ~1.0 (textures near-
  fully content -> INSENSITIVE by construction).
  isl2 billboards engine 1.383 (z +2.02) v17 1.077 (z +0.43); rooftop engine
  0.585 (z -7.75) — driven by ONE (4,1) material (m5) whose batch pair is a
  near-constant tint lookup onto a dark atlas texel.
(4,2)-only split: signals shrink (isl2 billboards 1.399 z +1.32; isl1
props_street engine 0.858 z -2.21 n=2; roads both ~1.1 z~1). VERDICT: the
enrichment test is WEAKLY POWERED on this city; no family gives a decisive
(z>2 both-islands) win for either chain. Per-material: 8/10 BillboardRoof_01
(4,2) materials show engine enrichment 1.36-1.46 on BOTH islands (uniform
base 0.683) — the strongest single pro-engine signal; m86/m128 (isl1) and
m13/m5 ((4,1) tint constants) point at dark cells — UNEXPLAINED, 4 of 202.

Atlas-cell containment (content-mask connected components): engine 0.204
(isl1, null 0.221+/-0.055, z -0.32) / 0.171 (isl2, null 0.159+/-0.055,
z +0.22) — AT NULL. v17 0.547/0.555 but with 5x smaller footprints (median
rect area 0.0036 vs 0.0194) and (4,1) normal-noise — NOT a valid comparison;
marked INSENSITIVE for tiling materials.

Texel density (world units, u = one texel column of the texture):
  Worked example m97 / GC_T_Concrete_02 512px, isl1 seg1109 (57.7m x 136.7m):
  engine s109 x65535 = (52.29, 19.92) -> 52 repeats over 136.7m =
  195.8 texel-u/m (~5mm/texel) and 74.5 texel-v/m; v17 uv0 = 1 repeat over
  the segment = 3.7 texel-u/m (~27cm/texel, visibly blurred).
  Family medians (engine): roads 85-96, buildings 36-84, billboards 129-217,
  props_street 29.8; v17: roads ~10, buildings 12-15, billboards 6-13,
  props_street 251-253 (oversampled), rooftop 0.0 (constant normal-word).
  VERDICT: engine densities are physically plausible for 2012 mobile street
  rendering; v17 is 10x too coarse on roads and degenerate on (4,1) roofs.

T1 BOTTOM LINE: the engine chain is the only structurally valid diffuse
decode for ALL classes ((4,1)/(3,1) have no TexCoord1 stream — v17's uv0 is
normal/color-as-uv there), and its world-scale texel density is plausible
while v17's is not. Enrichment/containment are too weak to independently
confirm; 4 dark-cell anomalies unexplained.

## 2. T2 — staged ?chain=engine A/B (scripts/export_zone19.py, work/staged_wt)

- export_zone19.py: v17-parity exporter + TEXCOORD_2 (engine Coord0) and
  TEXCOORD_3 (engine Coord1; (0,0) where no Coord1 stream — GL disabled-
  attribute default). Field selection per the record's OWN descriptors
  (pair slot j == descriptor j; source word = byteOff/4). Stride-28 ((5,2))
  segments remain EXCLUDED for v17 parity — 15 records' segments unshipped
  in v17 AND v19 (gap documented, ~60 segments).
- three r160 GLTFLoader maps TEXCOORD_2->'uv2', TEXCOORD_3->'uv3'.
- app.js (staged): ?chain=engine swaps uv<-uv2, uv1<-uv3 + RepeatWrapping;
  default path untouched (APP_CACHE_VERSION v19, manifest v19).
- 21 street GLBs re-exported: 52.6MB -> 72.3MB (+19.7MB, two extra vec2
  streams). Bindings identical to v17 (lm 1091+658, d 326+337, add 94+25,
  dark 5, missing 46/30 — same textures missing as v17).
- Numeric lightmap stats (t2_lm_stats.json, sampled bake-page luminance):
  isl1 v17 mean 44.3 / engine 44.1 (std 31.9/32.6, near-black 0.241/0.266);
  isl2 v17 33.3 / engine 31.1 (0.319/0.361). Comparable overall; engine
  darker on isl1 roads (nb 0.240 vs 0.146), lighter structure on rooftops.
- A/B renders (work/ab_*.png, visual, unquantified): block0 and plaza both
  show the v17 flat cyan wash REPLACED by coherent bake structure (roads
  read as roads, building window grids visible, billboards bound to their
  cells). Engine chain looks BETTER. Recommendation: after user review the
  engine chain should become the default; NOT done here (per instruction).

## 3. T3 — raycaster rebuilt + certified (scripts/raycast_t3_v2.py)

Method: double-sided Moller-Trumbore, uniform grid + DDA cell marching,
giant-tri (xy span > 400u) global list, exact per-cell z-window culling,
full-frame 640x360 primary rays (half pitch of 1280x720 — giant-tri
pollution makes native res intractable in numpy), ground-third window
76,800 rays per oblique camera (80x the round-12 960-ray grid).

Certification:
  (c1) analytic: MT alone intersects all 278 random targets at exactly
       t=5.0 — 278/278.
  (c2) synthetic 2-tri scene: nearest-of-two PASS, far-only PASS,
       double-sided PASS (exact t values).
  => CERTIFIED for nearest-hit tracing at the algorithm level.
  (a)/(b) in-archive self-return at +40u: 0/100 road, 0/100 building —
  IMPOSSIBLE on this archive: it contains 5,108 giant overhanging tris
  (m40=11-leaning wall slabs, extents to 600u) that cross above essentially
  every point; worked example: straight-down ray over the plaza crossing is
  blocked at t=3.2 by wall tri 28922 (verts given in results JSON).
  (c) two-sided centroid rays: 0/278 same-triangle; blocker taxonomy:
  71 coplanar strip neighbors + 377 giant tris + 107 other in-archive
  geometry. The SPECIFIED controls are unsatisfiable on this archive —
  documented, not hidden (ground rule 8).

Per-camera first-hit fractions (ground third; certified-algorithm caveat:
"first hit" = what a depth buffer would show, dominated by the caging):
  block0 (seg569 road anchor, -667,-955): hit 1.000 void 0.000;
  m40=11 88.1%, m74 10.9%; hit heights median 12.4u p90 83.1u.
  plaza (seg1483 crossing, -571,-865): hit 1.000 void 0.000;
  m11 57.4%, m76 13.7%, m73 12.1%, m14 11.3%; heights 10.4 / 22.6.
  roadtop (nadir 120u): hit 1.000; m76 63.2% at v0-height ~83u — the rays
  strike an ELEVATED deck (viaduct) before the street; m11 36.8%.
- ROUND-12 "void 0.816 / street floor 80% missing" RETRACTED as a method
  artifact (that raycaster's positive control had failed; its numbers were
  never certifiable). The archive view from street level is fully covered
  by first-hit geometry.
- Slab coverage (+40 value 34/35, GothamCity_low): the void set is EMPTY at
  all three cameras -> the coverage question is VACUOUS here; the low-
  archive stride misparse remains unfixed and stays OPEN for other views.
- Viewer LOD: the low tier is manual (button); no auto swap distance is
  implemented viewer-side; the engine's swap distance is not RE'd — OPEN.

## 4. T4 — skyline / v18->v19 evidence

- Gate v2 on v19 staged tree: PASS — stream-complete 26/26, fingerprint
  r=0.994 vs the v18 reference (default pixels unchanged by the added
  attributes), spatial mean 15.98, near-black 0.812, asym 0.416.
- Synthetic controls under current thresholds (all must FAIL, all FAIL):
  black, half-black(top), right-dim@mean10, right-dim@mean3, mid-load
  uniform (night-floor check), street-GLB-removal 5/26 FAIL (fp -0.071),
  NEW skyline-GLB-removal control: FAIL 21/26 — reproduces the live-v17
  failure signature (spatial near-identical to gate_live.json:
  12.74/0.8465 vs 12.78/0.8465). Fingerprint vs the stored reference gave
  r=-0.044 here vs 0.816 (session-22 screenshot-vs-screenshot basis) — the
  fingerprint is drift-sensitive and basis-dependent; stream-complete is
  the deterministic detector.
- Boot GLB request list (network-observed, 75s window): exactly 26 = 21
  street + 5 skyline (GC_LongDist_Island1_FP1/FP2/FP3/_Roads,
  GC_island1_LongDist). NO island-2 LongDist unit at boot (v14 policy).
- Skyline placement STILL rests solely on engine record 0x14051; the
  fingerprint detects drift, not correctness.

## 5. Claim status changes (rounds 7-12 -> round 13)

- "EF2raw tests insensitive (premise violation)" (session 22) — CONFIRMED
  and superseded: this round tested the ENGINE chain (not EF2raw) on the
  diffuse channel; engine chain now staged as ?chain=engine.
- "street floor renders near-black / void ~80% of ground third" (rounds
  11-12, already unquotable) — RETRACTED as method artifact; replaced by:
  first-hit coverage is 100% at the three certified cameras (dominated by
  the archive's own giant overhanging walls + an elevated deck).
- "archive floor is sparse" (round 12 positive-control explanation) —
  DOWNGRADED to "unestablished": the failed-control raycaster's sparsity is
  not evidence; the certified raycaster shows no void at all.
- "positive control failed = method uncertified" (round 12) — resolved:
  rebuilt + certified (c1/c2); the specified in-archive controls are
  documented unsatisfiable (archive caging), with taxonomy.
- "shipped chain contradicts the engine consumer" (session 22, PROVEN) —
  unchanged; v17 default kept until user review of the staged A/B.
- "K<2 = m23 and m12" (round 11) — refuted (round 12); unchanged.
- v18 staged (skyline boot fix) — still staged; now PUSHED as the
  gh-pages-staged branch @ c7f73c9 (remote), live remains v17.

## 6. Deliverables this session

Scripts (in-repo extraction/re/session23/ + /home/z/my-project/scripts/):
t1_diffuse.py, t1_class42.py, t2_lm_stats.py, export_zone19.py,
ab_renders.py, raycast_t3_v2.py.
Artifacts (work/): t1_diffuse_results.json, t1_diffuse_class42.json,
t2_lm_stats.json, raycast_t3_v2_results.json, raycast_cert.json,
gate_v19_staged.json, gate_v19_noglb.json, gate_v19_nosky.json,
ab_{default,block0,plaza}_{v17chain,engine}.png (6),
r13_classmap_{block0,plaza,roadtop}.png, skyline_boot_diff.txt.
Site (gh-pages-staged branch): manifest v19, 21 street GLBs with
TEXCOORD_2/3, app.js ?chain=engine.
