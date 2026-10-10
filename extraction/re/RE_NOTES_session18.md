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
