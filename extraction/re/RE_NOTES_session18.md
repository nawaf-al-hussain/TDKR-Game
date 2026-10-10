# RE Session 18 — round-5 review: shader semantics extracted (no Overbright,
# no VC in the street path), the footprint pillar retracted (estimator
# mismatch), popA flips back to +40 under enrichment, the LM chain's
# distributional tests are honestly insensitive, pipeline gates hardened

## Trigger
Outside-AI round-5 review (log-only). Prescriptions: T1 LightmapVCBlendDC
shader semantics; T2 street-flip evidence with the page-density confound
removed (enrichment, geometry-profile, v5 footprint + breakdown); T3
discriminate the (121,145) LM chain from alternatives + seam continuity +
wrap-mode + non-compact list + park check + slot 109/133 + stride-20
count; T4 deploy allowlist + dry-run + luminance-gate negative controls +
status tagging. Rule: every metric next to a null; willing to conclude
against ourselves; no version bump for a no-op.

## T1. LightmapVCBlendDC / LightMapDC shader semantics — SOLVED

Shader sources live in `effects.gla` inside the release zip (APK data/, not
the OBB); extracted with a 20-line index walk to `work/effects_chunks/`
(`LightmapVCBlendDC-{f,v}.glsl`, `LightMapDC-{f,v}.glsl`, plus 4 more
techniques banked).

**LightMapDC fragment (the street tier's technique — 227/307 + 141/196
materials; ALL street-stream segments):**

```glsl
lowp vec4  LightMapColor    = texture2D(LightMap, vCoord1) * 2.0;
highp vec4 DiffuseMapColor  = texture2D(DiffuseMap, vCoord0, LOD_BIAS);
lowp  vec4 Color            = DiffuseMapColor * LightMapColor;
    // * vColor;  // ATICA - removed on 26.04 to save memory in batching
gl_FragColor                = vec4(Color.rgb, 1.0);   // then fog
```

Conclusions (all three reviewer questions closed):
1. **There is NO Overbright uniform.** The ×2 is a hardcoded literal in the
   shader (same in LightmapVCBlendDC). The session-16 handoff framing
   "LM*2 + vec4(Overbright)" was a hypothesis; reality is simpler.
2. **The vertex-colour multiply is REMOVED by the authors** (commented out,
   dated 26.04) — street vertices carrying no vertex colour is
   engine-consistent, not a decoding gap.
3. **LightmapVCBlendDC is irrelevant to the street tier**: exactly 4+4
   materials use it, all park-ground grass/dirt/rock blends
   (`Color = LM*2 * mix(Texture1, Texture2, vColor.a) * vec4(vColor.rgb,1)`
   — a vertex-colour alpha blend), and **0 street segments** bind those
   materials via +40 on either island (152-155 / 1,2,3,35).
4. **The LM UV chain FORM is engine-proven** (`LightMapDC-v.glsl`):
   `vCoord1 = (Coord1 * Coord1_scaleoffset.xy + Coord1_scaleoffset.zw) *
   LightMapAtlas.xy + LightMapAtlas.zw`, and the type-7 LightMapAtlas vec4
   = (1,1,0,0) for **all 284 + 184** LM materials → the second stage is
   identity and the shipped chain `pageUV = w3·s121 + o145` is the exact
   engine expression. Both Coord0 AND Coord1 go through per-material
   scaleoffset uniforms.
5. Viewer impact: none needed — the shipped material already implements
   `Diffuse * LM*2` (now engine-exact by extraction, no longer an
   assumption).

## T2. Street-flip evidence with the density confound removed

(`round5_t2_evidence.py`, `round5_footprint_recheck.json`,
`round5_t2_evidence.json`.)

### 2a. Enrichment metric (the confound removed)
ENRICHMENT = observed non-empty-texel rate / uniform-random non-empty rate
on the same texture (mask_A = alpha<64 or near-black only; the round-4
mask's modal-colour rule labels road surfaces themselves "empty" on
full-bleed pages — asphalt IS the modal colour). Null ≈ 1 by construction;
>1 means the binding's UVs preferentially sample content.

- **popA flips to +40 on both islands**: enrichment +40 1.086 / 1.096 vs
  v5 1.009 / 1.012 vs shuffle null 0.982±0.019 / 0.974±0.016; head-to-head
  wins 479:97 (isl-1) and 333:35 (isl-2). The session-17 popA ordering
  (v5 0.80 > +40 0.655) was the density confound itself.
- Per family: **billboards +40** (1.193 vs v5 0.990, d=7.2σ; isl-2 1.179,
  d=4.4σ); **props_mono_rail +40** on isl-1 (1.093 vs 0.945, d=5.0σ);
  props_street both > null (+40 1.149 vs v5 1.065 — +40 leads, not
  decisive); building/road/flat/trees **metric-silent by construction**
  (opaque pages, baseline ≈ 1); coronas anti-enriched (additive-glow pages
  break the mask; metric inapplicable).
- Verdict: enrichment where it is defined supports +40; where silent, the
  geometry test below is the arbiter.

### 2b. Geometry-profile test (texture-independent) — the new decisive pillar
Per segment: z-extent, planarity (SVD residual), upward-normal and
horizontal-normal fractions (normals from triangle winding — the streams
carry no normal attribute), size, area. Scored as between-group variance
explained (eta²) under each labelling + nearest-centroid classifier
(5-fold CV) vs an always-majority floor:

- eta² (+40 labels vs v5 labels), island-1: up_frac 0.505 vs 0.073;
  horiz_frac 0.383 vs 0.057; planarity 0.424 vs 0.197; area 0.207 vs 0.033.
  Island-2: up_frac 0.401 vs 0.019; planarity 0.638 vs 0.230.
- Classifier accuracy: +40 labels 0.45 / 0.64 vs floors 0.173 / 0.259
  (2.6x / 2.5x above). **v5 labels 0.726 vs floor 0.771 (BELOW the floor,
  island-1) and 0.716 vs 0.658 (island-2, +0.06)** — the v5 labelling
  carries almost no geometric information, which a TRUE labelling would.
- Verdict: decisive for +40's labelling on both islands; covers all
  2537 segments (the enrichment metric alone leaves 1164/930 unresolved).

### 2c. UV-footprint — RETRACTED (estimator mismatch)
Re-running v5's footprint + per-family breakdown exposed that the round-4
"dom95 +40 0.263/0.161 vs null 0.013/0.007 (~20x)" compared a single
deterministic dom (+40) against a null that thresholded the MEAN of 24
permuted doms. The matched single-perm null is **0.301±0.009 / 0.208±0.012
— at or ABOVE +40's rates**; conditioned on atlas-like permuted pages
0.174 / 0.105. The footprint metric does not discriminate +40 from
shuffled labels; the ~20x was an artifact
(`round5_footprint_recheck.json`). The round-4 class-UV-rect-tightness
metric is likewise degenerate (1.0 for +40, v5 AND shuffled classes).
Per-family footprint numbers (for the record): +40 above null only on
building_residential/landmark; at or below null on
footprint/mono_rail/trees — consistent with tiny-UV-footprint segments
passing trivially on any texture.

### 2d. Overall T2 verdict
The +40 street flip STANDS on: the engine record (compiled bdae
self-indexing 307/307 + 196/196, order == library_materials), the
geometry-profile test (texture-independent, both islands), and enrichment
where the metric is defined — with the footprint pillar RETRACTED and the
raw texel-validity pillar retired to enrichment. v5 wins nothing: its
labels fail the geometry test and it never beats +40 where the metric is
defined. No change to the shipped output (v17 already ships +40).

## T3. Lightmap chain — alternatives, seams, wrap, populations

(`round5_t3_chain.py`, `round5_t3_chain.json`.)

### 3a. Alternatives table (visited luminance structure over 123/81 LM materials)
| chain | lum-std (isl-1) | lum-std (isl-2) |
|---|---|---|
| C1 shipped (s121,o145) wrap | 0.1284±0.051 | 0.0897±0.030 |
| C1 clamp (no wrap) | 0.0963 | 0.0671 (in-page 1.0 trivially) |
| C2 (s133,o109) | 0.000 | 0.000 (degenerate constant) |
| C3 (s109,o145) | 0.001 | 0.001 (degenerate constant) |
| C4 (s121,o133) | 0.1229 | 0.0810 |
| C5 (s109,o133) | 0.000 | 0.000 (degenerate constant) |
| C6 identity (w3 alone) | 0.1267 | 0.0847 |
| C7 permuted (121,145) null (k=12) | 0.1114±0.0035 | 0.0797±0.0036 |

**Honest negative: the luminance-structure metric separates the shipped
chain only from DEGENERATE (constant-UV) chains.** Permuted parameters and
identity score page-like structure because area bakes carry structure
everywhere. Round-4's "0.129 vs 0.001" is downgraded accordingly.

### 3b. Seam continuity (the prescribed discriminator) — NEGATIVE
Near-coincident vertices (<0.30u) on segments of DIFFERENT materials
(4000/3724 pairs, LM-bound stride-24):
- value-space, all pairs: authored 0.1554 vs permuted-null 0.1384±0.0134
  (isl-1); 0.1399 vs 0.0991±0.008 (isl-2) — authored NOT better.
- value-space, same-page pairs only: 0.156 vs 0.144±0.013 (isl-1);
  0.144 vs 0.103±0.008 (isl-2) — authored NOT better.
- pageUV-space, same-page: 0.467 vs 0.474±0.029 (isl-1); 0.557 vs
  0.487±0.061 (isl-2) — authored ≈ random.

Interpretation: per-tile AREA bakes do not guarantee cross-material seam
continuity (each material has its own tile; adjacent tiles' edge lighting
need not match), so the seam test is INSENSITIVE here rather than
refuting. Combined with 3a: **no distributional test available to us
discriminates (121,145) from permuted parameters.** The chain's support
remains: the engine-proven FORM (T1.4), the m90 exact tile-rect anchor,
the m76 a=15.25 band-strip, and occupancy compactness (91/123 + 55/81).
Recorded as "best-supported mapping, not independently confirmed" — no
better candidate exists, so the shipped v17 chain stays.

### 3c. Wrap mode
- bdae sampler records carry NO wrap flag (all are type-13 texture / type-7
  vec4 declarations; census banked).
- The engine's GL enum-conversion table (literal block at 0xb862f8..)
  contains GL_NEAREST/GL_LINEAR/mipmap filters/**GL_REPEAT (0x2901)**/
  **GL_CLAMP_TO_EDGE (0x812F, x3)**/**GL_MIRRORED_REPEAT (0x8370)** — wrap
  is a first-class sampler state; no evidence of a global clamp.
- Empirically: 59-63% of pageUVs leave [0,1) before wrapping (in-page
  40.9%/36.6%, banked session 17); the clamp variant scores LOWER
  structure (0.096 vs 0.128). WRAP retained (no longer a bare assumption:
  engine supports it, data demands it).

### 3d. Non-compact LM materials (visited wrapped extent > 0.30)
28 of 123 (isl-1) / 21 of 81 (isl-2). Common traits: LARGE horizontal /
extended surfaces — footprint floors (VD_Floor/_2 x5), rooftop grounds,
concrete/asphalt/bridge tiles, roads_details/crossings, residential
roofs/windows, monorail props, billboards, park tiles — with the LARGEST
|a121| scales (multi-wrap, up to 18.25; m76 = 15.25). All LightMapDC,
stride-24. Top entries: m97 (0.90, Concrete_02, a=[-18.25,-3.19]),
m73 (0.80, roads_details — the session-17 "m73-class" flag),
m30 (0.72, hedge), m138 (0.69, VD_Floor), m51 (0.66, bridge_tile);
isl-2: m14/m10 (0.92), m22 (0.88), m48 (0.70), m33 (0.63). One oddity:
m126's LightMap stem decodes as "LightMapSampler" (image-table name
collision — its tile rect cannot be checked against a page). Full list in
`round5_t3_chain.json`.

### 3e. Park check (20 largest LM-bound segments)
New chain: sampled LM mean 0.106-0.280, std 0.055-0.365 — page-histogram-
shaped (page std 0.087-0.137). Old (degenerate) chain: std 0.000
(a single texel per segment). Examples: seg1403 (m196, LB_Cinema, 6710
verts) new 0.280±0.365 vs old 0.082±0.000; seg968 (m76, VD_Items, 6299
verts) new 0.178±0.109 vs old 0.255±0.000. The "flat tint" failure mode of
the old chain is confirmed across all 20, not just the one segment probed
in session 17.

### 3f. Slots 109/133 — UNRESOLVED (neither placeholders nor confirmed)
- Exactly 1/65535 (the u16 dequant constant) appears in 9/227 (isl-1) and
  5/141 (isl-2) LightMapDC records; the broader distribution has median
  4.2x dequant, p90 ~20x, max 995x (z = 0 for all).
- Position-scale hypothesis REJECTED by construction (positions are f32;
  a ~1e-5 scale would collapse them).
- uv0-transform hypothesis TESTED: engine form `u16·s109 + o133` (wrapped)
  vs shipped `u16/65535` on per-material wrapped diffuse validity —
  16 vs 13 material wins (isl-1), 5 vs 5 (isl-2), mean Δ −0.009 — no
  systematic gain. Slot 109/133 is NOT established as the Coord0
  scaleoffset for the street family; per-technique layouts (session-15
  word-position table) may make these offsets mean different things per
  technique. Left open; no exporter change.

### 3g. Stride-20 (no w3) buildings
Stride-20 totals: 100 (isl-1) / 25 (isl-2). Building-family stride-20:
**3 (isl-1) + 1 (isl-2)** (vs 391 + 307 building segments on stride-24).
The flat-tint fallback affects a negligible slice; the session-17
97.6%/98.2% per-vertex-varying figures only ever covered LM-bound
stride-24 segments — now quantified at the other end too.

## T4. Pipeline robustness

- `deploy_site.py` rewritten as the ONLY deploy path with an explicit
  MANAGED-PATH allowlist: the single deletable pattern is `models/*.glb`
  not in the manifest (aux-protected files excluded); `enforce_allowlist`
  runs BEFORE any filesystem mutation and aborts (exit 2) on any planned
  delete outside the allowlist — verified by injecting
  ["worklogs/notes.md", "skybox.jpg"] (aborted). `--dry-run` prints every
  ADD/CHANGE/DELETE plus the URL gate and writes nothing (banked output:
  plan 0/0/0 on the current staging, gate 98 files 0 missing, manifest
  v17, 263 meshes).
- `viewer_luminance_gate.py` gained spatial checks: near-black fraction
  (>0.97 fails), per-quadrant mean floor (4.0), quadrant imbalance, and
  left/right asymmetry (0.15; the default camera looks down a street axis,
  healthy asym ≈ 0.00-0.03). Calibrated: healthy 12.79 mean / 0.846
  near-black / quads 8.9-16.7 / asym 0.02.
- Negative controls (`round5_gate_negative_controls.py`,
  `round5_pipeline.json`): synthetic black / half-black / right-half-dim-10
  / right-half-dim-3 frames ALL FAIL; healthy frame PASSES. Live stagings:
  removing the LUT or the fog texture does NOT fail the luminance gate —
  the v17 viewer degrades gracefully (the v16 black-LUT-pass mode was
  fixed in the viewer, not the gate) — but BOTH are caught by the deploy
  URL gate (MISSING: LUT_000_default.png / GC_VerticalFOG.png). A
  manifest broken on 6 street GLBs is also caught by the URL gate (the
  luminance gate stays green — partial street loss does not black the
  frame). Division of labour recorded: aux/asset loss -> URL gate;
  whole-render black -> luminance gate.
- **Staging hygiene fix**: `work/ghpages_site` was missing 23 referenced
  files that existed only on repo/gh-pages since the session-17 live
  restore (City_BKG, LongDist FP/Roads JPGs, reflections, water, windows).
  Back-ported from repo/gh-pages; staging now passes the URL gate
  standalone. This was a real latent trap for any future full re-stage.
- Session-16/17 notes tagged: every retracted/downgraded/resolved claim
  now carries an inline [RETRACTED/DOWNGRADED/RESOLVED/CORRECTED session
  N] tag plus a status ledger table at the end of each file (incl. the
  round-4 slot-109 retraction).

## Shipped / not shipped

**No site change** — T1 confirmed the viewer formula is already
engine-exact; T2/T3 support the shipped +40 bindings and the shipped LM
chain as the best-supported mapping. Per the round-5 rule, no version
bump for a no-op: the site remains v17. Verified post-decision:
`site_release_check.py` PASS (manifest v17 == origin/gh-pages, cache
versions consistent), `site_smoke_test.py` 58/58 PASS.

## Honest open items (updated)

- LM chain: best-supported, not independently confirmed — the two new
  distributional tests are insensitive in the area-bake regime; a
  discriminating test would need per-tile ground truth (e.g. decoding the
  assembly bake-list rects per material, if such a table exists).
- batch_info slot 109/133 role; the u16 array (rec 45-108); stream_info X;
  stride-24 word 5.
- m126's "LightMapSampler" image-table stem (name collision or a
  special-case material).
- Hero-unit generic-object records (unchanged, session 15+).
- The texel-validity/footprint family needs a cell-aware redesign before
  it can adjudicate dark-pad thin-stroke families — currently only
  geometry-profile + enrichment(where-defined) + engine record carry the
  binding case.

## Round-6 addendum (same session): page-type table, grouped-CV geometry,
## 109/133 tiling pattern

(`round6_pagetypes.py/json`, `round6_geom_grouped_cv.py/json`,
`round6_geom_features.json`, `round6_slot_tiling.py/json`.)

### R6-1. Page-type table (the enrichment baselines, tabulated)

146 unique diffuse pages referenced by either island's materials, 0 decode
failures. Types by mask_A contentA (alpha<64 | near-black) + cell count:
full_bleed cA>=0.85; atlas_dense cells>=2 & cA>=0.50; atlas_mid
cells>=2 & 0.15<=cA<0.50; dark_pad cells>=2 & cA<0.15; sparse_blob
cells<=1 & cA<0.85.

| type | pages | contentA | street segs bound |
|---|---|---|---|
| full_bleed | 124 | 0.982 [0.86,1.00] | 1382 |
| atlas_dense | 19 | 0.743 [0.51,0.85] | 1145 |
| atlas_mid | 3 | 0.459 [0.44,0.49] | 4 |
| dark_pad | **0** | - | 0 |
| sparse_blob | **0** | - | 0 |

Family x type (material-weighted): building_footprint 206/253 pages
full-bleed; residential 173/198; landmark 181/231; flat 37/43;
trees 3/3 (trunk cA=1.000 - the round-4 modal-colour mask, not the page,
made trunks look "thin-stroke"); road_band 13 full-bleed + 11 atlas_dense;
billboards 20/22 atlas_dense (enrichment home turf); props_street mixed
(14 full-bleed incl. GC_Z1_Props_Street_Alpha cA=0.995, 5 atlas_dense);
coronas 3 atlas_dense (additive caveat stands at cell level).

**The round-4 "dark-pad page" category does not exist at page level** —
the confound lived at CELL level inside atlas pages, and mask_A (round-5)
already normalizes it. This is why enrichment's null is ~1 by
construction on every page type.

### R6-2. Geometry test re-scored with GROUPED CV — pillar DOWNGRADED

Leakage concern: city batching re-instances the same template; random
5-fold splits copies across folds. Control: exact-duplicate vertex buffers
= **0 groups on both islands** (batching emits unique buffers), but
97%/98% of segments sit on materials with >=2 segments (isl-1: 136
materials / 1517 segs; biggest materials own hundreds), so random folds
still leak template identity. Schemes: random5 (baseline) / **by_material**
(whole materials held out; a test fold contains materials unseen in
training) / by_space (256u grid cells) / dedup_random5 (exact-dups
collapsed — no-op here). Nearest-centroid on the same 6 features,
K=12 permuted-label nulls under the SAME folds.

| island | scheme | +40 acc (floor) | +40 z vs null | v5 acc (floor) |
|---|---|---|---|---|
| isl-1 | random5 | 0.457 (0.173) | 51 | 0.679 (0.772) |
| isl-1 | **by_material** | **0.139 (0.173)** | 8.3 | 0.637 (0.772) |
| isl-1 | by_space | 0.429 (0.173) | 52 | 0.679 (0.772) |
| isl-1 | dedup_random5 | 0.445 (0.173) | 40 | 0.684 (0.772) |
| isl-2 | random5 | 0.648 (0.259) | 51 | 0.700 (0.660) |
| isl-2 | **by_material** | **0.094 (0.259)** | 3.2 | 0.602 (0.660) |
| isl-2 | by_space | 0.644 (0.259) | 55 | 0.688 (0.660) |
| isl-2 | dedup_random5 | 0.644 (0.259) | 42 | 0.702 (0.660) |

Per-class recall under by_material: only **billboards** generalize
(0.69 isl-1); props_street 0.04, props_rooftop 0.01-0.06,
residential 0.0-0.07, footprint 0.17, landmark 0.03-0.29.

Reading: the session-18 geometry signal is **material-template
consistency at segment level, NOT family-level shape laws** — a material's
instances share geometry and family, so random CV "predicts" the family by
identifying the material. With whole materials held out, accuracy falls to
or below the majority floor (still 1.6-2.6x the matched chance null, so
not literally empty, but far from the "decisive arbiter" wording).
v5 stays at/below floor under EVERY scheme, and billboards — the strongest
enrichment family — are the one family with true shape generalization.
**The +40 flip's support is now: the engine record (compiled self-indexing,
primary) + enrichment where defined + segment-level template consistency.**
"covers all 2537 segments decisively" is RETIRED.

### R6-3. The 109/133 tiling pattern — no street-family tiling; 14 records
### carry an explicit Coord0-identity transform

Per-technique census of the four vec3 slots (109/121/133/145), components
over .xy, both islands. For LightMapDC: **slot 133 is <=1e-4 in ALL 454+282
components** (dequant-ish or zero); slot 109 likewise <=1e-4 except ONE
0.015 component per island. So no (109|133) value can serve as an origin
(>=0.01 filter leaves n=0) or a working scale (C2/C3/C5 degenerate BY
CONSTRUCTION at record level). The exact-dequant (1/65535 +-1%) occurrences
concentrate 100% in one signature group:

- isl-1: 9 records, all `tiles_KjsfSXF4YP_*`;
- isl-2: 5 records, all `Material__4986_*`;
- ALL 14 have **s121 = (0.5, 0.5)** (half-page LM rect) and a tile offset
  at s145, with s109 = 1/65535 and s133 ~ 0..1.5e-5.

Reading: the packed pair (109,133) is the OTHER stage's scaleoffset
(Coord0): (1/65535, 0) = the identity on raw u16 uv0 — written explicitly
only where the tool emitted it, ~zero elsewhere. This RETAINS session-18's
conclusion (not a working diffuse transform; shipped /65535 identity is
engine-equivalent where the pair is the identity) and now explains WHY the
uv0 test tied: for the only records with a real value there, the value IS
the identity.

Page-level tiling lives in (121,145) and is loose, not a partition:
origins 24-33% on a 1/8 grid (uniform ~2%); extents concentrated at 0.5/1
(tiles family); rect overlap == permuted-origin null (z=-0.2/0.0,
coverage 1.0); edge-adjacency saturates at the null rate (227 rects on one
page -> some edge always matches). Consistent with round-5's area-bake
conclusion (shared tile regions, no exclusivity).

Other techniques DO carry real 109/133 values (NSO s133: 61/74 "other"
isl-1; StandardDiffuseDC s133 all real) — per-technique slot semantics
confirmed; 109/133 are not global placeholders.

## Round-7 addendum: LightMap-page x |s121| table, wraps test, 109/133
## byte reinterpretation, matched-granularity AMI, live gates

(`round7_lm_pages.py/json`, `round7_slot_bytes.py/json`,
`round7_geom_ami.py/json`, `round7_street_shot.py` + previews
`round7_street_block{0,1,2}.png`, `round7_netlog.json`,
`../scripts/staging_manifest_gate.py`.)

### R7-1. LightMap page identity x |s121| (the axis round-6 tabulated wrong)

Every LightMapDC material of both islands, LightMap sampler page identity
vs |s121| (max component), bins <=1 / 1-4 / >4 (materials/segments):

| island | page class | <=1 | 1-4 | >4 |
|---|---|---|---|---|
| isl-1 (227) | BakeGroup_* | 133/692 | 60/188 | 29/147 |
| isl-1 | named tiling | 5/14 | 0/0 | 0/0 |
| isl-2 (141) | BakeGroup_* | 79/419 | 47/137 | 13/4 |
| isl-2 | named tiling | 2/0 | 0/0 | 0/0 |

**All 149 |s121|>1 materials (89+60) sample BakeGroup_* area-bake pages;
zero named/tiling pages above |s|=1.** Extremes: m240 |s|=486.9 (0 segs),
m234 30.0, m116 22.0 (14 segs), m97 (GC_T_Concrete_02, s121=(-18.255,
-3.195)) -> BakeGroup_Island1_Landmarks0 (full_bleed), m76
(GC_Footprint_VD_Items) 15.2 with 62 segs. An 18x (worse: 487x) multi-wrap
on an area bake is not physical IF the chain applies per-segment full-span
UVs — which is exactly what the wraps test measures.

### R7-2. Periodicity test: content-blind by construction; WRAPS metric
### replaces it

The transect-ACF as specified cannot discriminate page content: under the
shipped chain pageUV = frac(w*s121 + s145) re-visits the same texels
|s|*span times, so the sampled luminance is EXACTLY periodic in the packed
coordinate for ANY page content.  Empirically the world-transect ACF at
the expected lag came out ~0 (m17: acf=-0.03, z=-0.6) because transect
binning mixes the v-direction — neither outcome is evidence.  The honest
replacement is deterministic arithmetic on measured spans:

    wraps_axis = per-segment packed-UV span * |s121_axis|

verdicts (median over segments, w4 = the shipped chain word), questioned
materials with segments (isl-1, 45 of 89; 44 have no street segments):

- **MULTI-WRAP (>=1.5): 16 materials** — m97 18.1x, m30 11.4x (6 segs),
  m230 9.3x, m72 4.3x, m181 4.4x, m172 7.5x (10 segs), m60 5.4x, m73 5.5x
  (24 segs), m76 3.8x (62 segs), m272 3.9x, m178 2.5x (43 segs), m49 2.8x,
  m208 2.2x, m180 2.2x, m271 1.6x, m18 2.0x.  For these the shipped chain
  tiles a BakeGroup area bake across single segments — unphysical.
- single-ish (0.5-1.5): 16.  sub-rect (<0.5): 11 — incl. the 46-seg
  billboard material m128 (median wraps 0.04): chain plausible there.
- Controls (|s121|<=1, 15 materials): never multi-wrap (max median 0.88) —
  by construction |s|*span<=1.

Supporting structure: pooled chain-UV coverage shows multi-segment
questioned materials smearing across the WHOLE bake page (m73 w4 0.996 of
Roads0; m178 0.539 with centroid spread 1200u; m76 0.484, spread 743u) —
under the chain every segment of a material samples the same pattern at
different world positions; a per-slab bake gives each slab its own rect.
This is the strongest available explanation of the dark/garbled buildings.

**Diffuse-tiling alternative (reading B, s121 as diffuse scale): MIXED,
not a resolution.**  Reference band (|s|<=1 materials, identity reading,
flat >=8u segments, 1-D world-vs-uv fit): isl-1 median 190.9 texels/u
(IQR 130-496, p10-p90 31-957).  readingB pulls below-band materials into
the band (m73 18.8->106.4, m40 15.6->133.5, m180 19.3->173.3) but pushes
atlas-textured materials far above p90 (m76 4216.7, m230 4136.6, m172
2355.7, m30 1094.4 — tiling an items/footprint ATLAS 15x is nonsense).
m97: identity 34.5 vs readingB 630.3 — both inside the wide band, i.e.
the density test cannot discriminate for it.  No exporter/viewer change
made this round: the implicated set is partial (16 of 89 questioned
materials with segments) and reading B is not uniformly supported.

### R7-3. Slot 109/133: u16/u8/flags/counts reinterpretation REFUTED;
### 14 of 368 records explained

Byte-level structure over the 218 unexplained LightMapDC records (isl-1;
136 on isl-2):

- mantissa bytes at FULL entropy (210-218 distinct values of 218
  records); exponent bytes concentrated in 0x32-0x3A — the two bytes
  behave exactly like genuine tiny floats, not reinterpreted integer
  fields;
- repeat share 0.014 (chance level for 32-bit values); top (u16lo,u16hi)
  pair occurs twice; no u16 small-int concentration (frac<1024: 0.00-0.04);
- no correlation with segment count (r = -0.04 / +0.008); no record with
  u32@109 == u32@133; f16 views nothing special.

Sharper per-technique fact (census table): **(121,145) carries plausible
scale/offset in EVERY technique** (NSO s121 med 0.77 / s145 0.50;
StandardDiffuseDC 0.31-0.81; LightMapDC 0.36-0.5 / 0.50) while **(109,133)
carries tiny floats (1e-6..1e-3) in EVERY technique** (NSO s109 med
2.7e-4, SDD 5.7e-6).  So the engine's Coord0 transform is simply not
stored in batch_info for any technique — identity-by-dequant or sourced
elsewhere — and the 14 records with explicit (1/65535, 0) are tool-written
identity echoes.  Count bases, stated plainly: **14 of 368 LightMapDC
records explained (9/227 isl-1 + 5/141 isl-2); 354 records unexplained**
(218 isl-1 records = 436 of 454 isl-1 .xy components — the reviewer's
"~440"; 136 isl-2 records = 272 of 282 components).  The contradiction
stands as the reviewer framed it: if (109,133) were the diffuse
scaleoffset, streets would collapse — they do not, so those slots are not
the diffuse transform.  What the engine binds for Coord0 remains OPEN
(candidate: hardcoded dequant like the x2 literal; disassembly follow-up).

### R7-4. Matched-granularity AMI (standardised features confirmed)

Features = round-6 bank (log1p on size axes, z-score on kept rows —
explicitly confirmed), KMeans(k = #classes, n_init=10, seed 6018), AMI +
K=200 label-permutation null:

| island | label set | k | AMI | null | z |
|---|---|---|---|---|---|
| isl-1 | +40 | 12 | **0.326** | -0.000+-0.002 | 147 |
| isl-1 | shuffled | 12 | -0.003 | -0.000+-0.002 | -1 |
| isl-1 | v5 (own k) | 4 | 0.125 | 0.000+-0.004 | 35 |
| isl-1 | v5@k40 | 12 | 0.172 | -0.000+-0.004 | 44 |
| isl-2 | +40 | 11 | **0.454** | 0.000+-0.003 | 139 |
| isl-2 | shuffled | 11 | -0.005 | 0.000+-0.003 | -2 |
| isl-2 | v5 (own k) | 3 | 0.194 | -0.000+-0.003 | 56 |
| isl-2 | v5@k40 | 11 | 0.238 | 0.000+-0.005 | 47 |

Reading: +40 labels (from the texture table, geometry-independent) carry
moderate real geometry association at matched granularity.  v5's positive
AMI is PARTIALLY CIRCULAR — the v5 binder's flat/vertical split is itself
a geometry test, so some association is built in.  As stated in round-6:
geometry cannot check the index->texture-name mapping; that rests on the
compiled self-indexing 307/307 (+196/196) and the renders.

### R7-5. Live v17 evidence + gates

- Street-level near-field screenshots from the LIVE site (playwright,
  camera via window.__v; viewer is y-up: viewer=(x, z, -y) of world):
  `previews/round7_street_block{0,1,2}.png` — **visual, unquantified**.
  block0: street-level view where some facade walls carry correctly-bound
  textures while footprint-tier slabs above render as garbled stretched
  atlases and the street plane is black.  block2: a near-field building
  wall rendering almost pure black — the dark-building pathology up close.
- **Headless network-log gate: PASS** — 135 responses, 0 failed requests,
  0 4xx/5xx (`round7_netlog.json`).
- **Staging-from-manifest gate: FAIL (real drift found)** —
  `../scripts/staging_manifest_gate.py` builds the expected tree from
  models/manifest.json + texture names parsed out of every GLB's material
  names (`<dif>|<lm>|<mode>` contract) + aux, then diffs against
  origin/gh-pages: 0 missing, 0 glb size mismatches (manifest v17, 170
  expected files), **3 stray v16-leftover textures** (GC_Park_dirt.jpg,
  GothamCity_Road_Island_2.jpg, GothamCity_sand_tile.jpg — unreferenced by
  all 41 GLBs and by app.js).  Cleanup must go through deploy_site.py in a
  reviewed follow-up; gate stays red until then.

No exporter/viewer/site changes this round (evidence partial; no version
bump).
