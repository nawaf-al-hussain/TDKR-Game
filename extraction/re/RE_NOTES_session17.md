# RE Session 17 — round-4 review: the street flip held, the lightmap chain
# did not (100% was a degenerate-slot artifact; the real chain is scale@121
# + offset@145 with WRAP), plus the process fixes

## Trigger
Outside-AI round-4 review (log-only): "The result reverses the street tier,
so the evidence for it needs to be stronger than it is." Prescribed:
texel-validity (+40 vs old vs shuffled), UV-footprint, (a,d) null test,
quantify v15->v16, stratify coverage, w3 decode, vertex-colour check,
before/after of a building block, deploy-process fixes.

> **Round-5 status note (session 18):** the two distributional pillars of
> this round were re-examined — the UV-footprint "~20x null" was RETRACTED
> (estimator mismatch, see §2 tag) and the visited-luminance-structure
> metric was shown to separate only DEGENERATE chains (permuted-parameter
> null scores the same). The street flip's quantified case now rests on
> the engine record (self-indexing bdae), the round-5 geometry-profile
> test, and the round-5 enrichment metric; the LM chain rests on its
> structural anchors (m90/m76). See RE_NOTES_session18.md.

## 1. Texel-validity test (`round4_street_evidence.py`, .json banked)

Fraction of diffuse-texture samples landing on non-empty texels (alpha<64 OR
near-black OR within 10 of the page's modal colour), same segment UVs under
three bindings, by engine family (+40 material family):

- +40 WINS on the dense/atlas families (island-1): billboards 0.83 vs v5
  0.45 / null 0.62; building_footprint 0.79 vs 0.17 / 0.63;
  building_landmark 0.81 vs 0.08 / 0.66; building_residential 0.79 vs 0.26 /
  0.70; props_rooftop 0.94 vs 0.68 / 0.57; mono/rail 0.61 vs 0.03 / 0.68.
- +40 scores LOW on dark-pad thin-stroke pages (props_street 0.18, coronas
  0.002, trees 0.45): the metric is page-density biased — a lamp cell is
  mostly black padding around thin strokes, so the CORRECT binding samples
  mostly "empty" texels while a random dense page scores high.  Reported
  as a confound, not hidden: raw texel-validity cannot adjudicate those
  families (v5's popA advantage 0.80 vs 0.66 is the same bias — its pages
  are full-bleed road atlases).
- popA (v5 bound, +40 diffuse available): +40 0.655 / v5 0.801 / null
  0.618±0.017; per-segment wins +40:191 v5:248 tie:154 — v5's UV-fit DID
  align content on its (wrong) pages: content-finding but page-wrong.
  **[RESOLVED session 18: this popA ordering was the page-density confound
  itself. Under the density-normalized ENRICHMENT metric the verdict
  flips to +40 on both islands: enrichment +40 1.086/1.096 vs v5
  1.009/1.012 vs shuffle null 0.982±0.019 / 0.974±0.016 (wins 479:97 and
  333:35). Raw texel-validity stays retired as a popA arbiter.]**

## 2. UV-footprint (cell containment) — 20x over null

Atlas pages (n_cells>=2, coverage<0.85) x atlas families: dominant-cell
fraction >=0.95 for +40 = 0.263 (isl-1) / 0.161 (isl-2) vs null 0.013 /
0.007; bbox-grid containment 0.238 / 0.140 vs 0.013 / 0.007.  Absolute
rates are depressed by thin-stroke cells (samples on the cell's own black
pad label as background) — the signal is the ~20x null separation.
**[RETRACTED session 18 — ESTIMATOR MISMATCH: the null thresholded the
MEAN of 24 permuted doms (a segment passes only if it lands in one cell
on AVERAGE over all perms), while +40 got a single deterministic dom.
The matched estimator (single-perm null, same segments, 24 perms) is
0.301±0.009 / 0.208±0.012 — AT OR ABOVE +40's rates. Conditioning the
null on atlas-like permuted pages still gives 0.174/0.105. The footprint
metric does NOT discriminate +40 from shuffled labels; the "~20x" was an
artifact. Banked in round5_footprint_recheck.json. The same re-examination
showed the round-4 class-UV-rect-tightness metric is degenerate (1.0 for
+40, v5 AND shuffled classes — never evidence).]**

## 3. (a,d) null test — the reviewer predicted exactly this

Applying ANOTHER material's (a,d) pair keeps in-page at 100.00% (284/284
and 184/184 LM materials satisfy d+a<=1 componentwise) — **the round-3
"100.0000% in-page" claim is RETRACTED as chain evidence**: with scale slot
109 at ~1e-5, pageUV collapses to the constant d and ANY pair is in-page.
The committed w3_coord1_test16.py with the REAL-scale slot 121 scores only
40.9% / 36.6% in-page — the rest wraps.

## 4. The lightmap chain, corrected (`round4_lm_probe.py`, `round4_lm_partition.py`)

- slot 121 carries real scales for 135/284 (isl-1) / 87/184 (isl-2) LM
  materials; slot 109/133 are ~1e-5 degenerate (a second sampler's
  placeholder pair).  (s121, s145) = one vec4 scaleoffset (scale.xy,
  offset.xy) for the Coord1 sampler.
- Evidence for pageUV = w3_uv * scale@121.xy + offset@145.xy (WRAP):
  a) m90's tile rect matches the banked [0.25,0.62]x[0.75,1.00] of Roads0
     EXACTLY; b) visited-region luminance std 0.129 vs 0.001 (old chain —
     flat); c) the park probe: m19 samples all-zero texels under the old
     chain (the "near-black central park" = the constant d landed on a
     black texel) vs mean 0.223 / std 0.162 with page-histogram-shaped
     distribution under the new chain; d) occupancy: 91/123 (isl-1) and
     55/81 (isl-2) LM materials visit compact (<=1.2-width) wrapped regions
     incl. m76 whose a=15.25 maps its narrow w3 onto a road-band strip.
  **[DOWNGRADED session 18: evidence (b) and (c) separate the chain only
  from DEGENERATE (constant-UV) chains. The round-5 alternatives table
  (round5_t3_chain.json) shows permuted (121,145) parameters score
  lum-std 0.111±0.004 vs shipped 0.128±0.051 — indistinguishable — and
  the seam-continuity test (value-space AND pageUV-space, same-page
  conditioned) gives authored ≈ permuted-null (0.156 vs 0.144 isl-1;
  0.144 vs 0.103 isl-2 — authored NOT better). Per-tile area bakes do
  not guarantee cross-material seam continuity, so these distributional
  tests are INSENSITIVE here. The chain's support = its engine-proven
  FORM (vCoord1=(Coord1·s+o)·LightMapAtlas+..., LightMapAtlas=(1,1,0,0)
  for all 284/184 materials, session-18 shader extraction) + the m90
  exact tile-rect anchor + m76 band strip + occupancy compactness.
  Recorded as the best-supported mapping, not independently confirmed.]**
- Tile-partition null: saturated (total visited area 14.7x page) — bake
  groups are AREA bakes (A0/B0/Roads0/Landmarks0), so different materials
  in one area legitimately share tile regions; non-overlap was the wrong
  hypothesis.  Reported for completeness.
- w3 encoding: u16 x 2 lanes, both unorm [0,1], LE order (lo=U, hi=V); no
  snorm population.  NO w3==0 street segments exist (0 of 1417 stride-24
  on isl-1).  LM-bound stride-24 segments: 97.6% / 98.2% carry per-vertex
  varying w3; the rest narrow/constant.  Buildings WITH per-vertex w3:
  51 materials / 362,789 verts (isl-1), 44 / 388,860 (isl-2); without: 2 /
  1,658 verts (isl-1), 0 (isl-2).

## 5. Vertex colour — NOT FOUND (reviewer ask)

stride-24 words: [0..2]=pos, [3]=w3/Coord1, [4]=uv0, [5]=unknown
([u16 full-range][u8 0..255][u8 pad]; NOT octahedral (29-33% inside), NOT
RGBA).  stride-20 word3: mixed, no RGBA pattern.  No vertex colour exists
in the street streams; LightmapVCBlendDC's blend factor cannot come from
street vertices.  The x2-with-white assumption stands (now explicitly an
assumption for both techniques until the Overbright term is resolved).

## 6. v15 -> v16 quantified (`round4_delta16.py`)

- island-1: 99.6% of segments changed texture (1511/1517); v15 was 39.2%
  bound (594) via the v5 heuristic, v16 is 99.7% (1512); dark->bound 918;
  v15's "road" assignments alone: 89 road->props_street (the lamp-row
  smoking gun at family scale), 135 flat->trees, 117 flat->rooftop...
- island-2: 99.6% changed; v15 36.7% bound -> v16 100%.
- Coverage stratified (v16): buildings 391/391 + 301/301, props
  1046/1046 + 677/677, road 40/40 + 27/27, sidewalk/flat 19/19 + 8/8 —
  100% per family, no family hiding on a default texture.
- **"8 unbound" corrected to 5**: 3 of them were m180
  (GC_Residential_BD_04_Windows_05_v with an UPPERCASE .TGA that stem()
  didn't strip — image-table case-insensitivity struck twice).  The
  remaining 5 are seg0-4, material m40=0 (ProfileCOMMON FlippedPlane,
  BOTH samplers unbound in the engine table) — dark by engine data.
  After the fix: missing textures 0/0.

## 7. Before/after (`round4_before_after.py`, renders in
`round4_evidence_renders/`)

Densest 160x160u near-tier block (box -151,-1083; 31 building segments,
m76 VD_Items + m138 VD_Floor + ...): v15 = flat untextured polygons (dark
fallback) + flat color patches; v16.0 = real facade atlases x flat
per-material bake tints; v16.1 = facades x REAL per-vertex bake content
(diagonal light gradient on the VD_Floor plane, striped light bands on the
item cluster).  LM-channel-only pair banked (flat polygons vs structured
bake).  x3-gain variants labelled `_gain3` (engine-value raw renders also
banked).

## 8. Process fixes (deploy class the reviewer called out)

- `models/batarang.glb` was 404 ON LIVE (app.js easter-egg reference) —
  the old smoke test never requested it; restored from the origin commit
  017f967.  skybox.jpg/style.css/.nojekyll restored to the deploy source.
- `deploy_site.py`: INCREMENTAL sync (copy new/changed; delete only
  street GLBs dropped from the manifest; aux LUT/FOG/skybox/batarang are
  protected) + pre-deploy URL gate (every local URL in app.js +
  index.html + manifest must exist in the staged tree) — this gate caught
  batarang.glb and the cleanup bug (AUX_PROTECTED prefix mismatch) in
  testing.
- `site_smoke_test.py` check 7: live crawl gate — extracts every local
  asset URL from app.js/index.html and fails on any non-200.
- `viewer_luminance_gate.py`: headless default-view screenshot; mean
  luminance must be >= 8/255 (calibrated: healthy night grade 12.8,
  black-render failure mode < 3).  v17 PASS at 12.79.

## Shipped (v17)

- exporter v16.1 (`export_zone16.py`): case-insensitive stem + LM chain
  scale@121/offset@145 WRAPPED per-vertex TEXCOORD_1; manifest v17; 21
  street GLBs regenerated; missing textures 0; unbound 5 (engine-unbound
  m40=0).  Deployed via deploy_site.py; smoke + luminance gates PASS.

## Honest open items

- Overbright / the x2 in the street path — still assumed (no VC found,
  so no vertex-colour term either).
- slot-121 semantics for the ~1/3 of LM materials whose visited regions
  still sweep the page under the chain (m73-class) — per-material
  exceptions or a second technique slot not yet decoded.
- word 5 (stride-24) content unidentified ([u16][u8][u8=0]).
- The texel-validity metric needs a cell-aware redesign for dark-pad
  pages before it can adjudicate props_street/trees/coronas families.

## Round-5 status ledger (tagged session 18)

Every claim in this file whose status changed in session 18:

| Claim (session 17) | Status now |
|---|---|
| UV-footprint dom95 0.263/0.161 vs null 0.013/0.007 (~20x) | **RETRACTED s18** (estimator mismatch; matched single-perm null 0.301/0.208 >= +40) |
| Class UV-rect tightness (+40 1.0 vs v5 vs null) | **DEGENERATE — never evidence** (1.0 for every labelling incl. shuffle) |
| popA: v5 0.80 / +40 0.655 (raw validity) | **RESOLVED s18 for +40** under enrichment (1.086 vs 1.009, d≈5.5σ) |
| Visited lum-std 0.129 vs 0.001 as chain evidence | **DOWNGRADED s18** (separates only degenerate chains; permuted null 0.111 ≈ shipped 0.128) |
| Chain (scale@121, offset@145) wrapped | **STANDS as best-supported** (engine-proven FORM via LightMapDC-v.glsl + LightMapAtlas=(1,1,0,0) all materials; m90/m76 anchors; occupancy) — the new distributional tests are insensitive, recorded as an open risk |
| Wrap sampling | **STRENGTHENED s18** (engine enum table has GL_REPEAT/CLAMP_TO_EDGE/MIRRORED; no per-material wrap flag in bdae sampler records; clamp variant scores lower structure) |
| "slot 109/133 are ~1e-5 degenerate placeholder pair" | **REVISED s18: UNRESOLVED** — 9/227+5/141 LightMapDC records hold exactly 1/65535 (u16 dequant family); distribution broad (median 4.2x); as a uv0 transform it does NOT beat shipped /65535 (16 vs 13 wins, mean Δ −0.009); position-scale rejected (f32) |
| x2 / Overbright assumption | **RESOLVED s18** — no Overbright uniform exists; x2 hardcoded in LightMapDC-f.glsl |
| "street vertices carry NO vertex colour → no VC term" | **CONFIRMED s18** (vColor multiply author-removed in LightMapDC; VCBlendDC unused by street streams) |
| Luminance/footprint gates | **HARDENED s18** (spatial checks: near-black fraction, per-quadrant floor, L/R asymmetry; negative controls banked in round5_pipeline.json) |
