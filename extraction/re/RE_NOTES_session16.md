# RE Session 16 — the agreement test flipped the world: v5 street bindings
# were WRONG, +40 is engine-true, and the whole street lightmap chain fell out

## Trigger
Outside-AI round-3 review point: "run the street-tier agreement test before
any export; every mismatch has information." The mismatches ended up
disqualifying the exporter, not +40.

## 1. Street-tier agreement test — honest negative, then root cause

Setup (`agreement_test16.py`): for every segment of both islands, compare
the v5 exporter binding (`bind_segment`, band-atlas structural test) vs
+40 -> material DB DiffuseMap, under library_materials order, alphabetical
name, alphabetical DiffuseMap, and 200 random permutations (null).

Result: **exact agreement 1/593 (0.17%) island-1, 4/374 (1.07%) island-2 —
at null level under EVERY ordering.** Family agreement 1.5-2.7%. The null
(mean 0.31%/0.63%) is indistinguishable from all three orderings.

Diagnostics run before concluding anything (`diag_plus40_class16.py`,
`diag_offsets_orders16.py`):

- **Class purity 76.3% / 76.2%**: segments sharing a +40 value are mostly
  one exporter class. Weighted purity, and the big groups are spread across
  773-1334u (spatial autocorrelation EXCLUDED).
- **Enrichment**: +40=11 predicts the exporter-"road" class at 43% vs 8.3%
  base rate (85/199); +40=299/194 (FX_Coronas) -> 100% exporter-dark
  (additive coronas are dark in v5); +40=178/153 (Monorail props) -> 100%
  dark; +40=5 -> 99% flat.
- **Offset scan (H1)**: NO u32/u16 descriptor offset 0..204 reproduces the
  exporter bindings under lib order. Only +40 and +32 have range<M at all.
- **bdae members**: source.dae is NOT what the engine parses; the zip also
  carries big/little_endian_(not_)quantized.bdae.

Conclusion at this point: +40 carries real per-segment material identity;
either the DB enumeration or the exporter is wrong.

## 2. The compiled materials bdae fully decoded (`runtime_mats16.py`)

The runtime material table is the render-record array inside
`little_endian_quantized.bdae` (BRES container). Layout (all LE):

- **Material record = 36 B**: `[name_ptr][name_ptr][0][effect_ptr][N][
  sampler_list_ptr][selfidx][0xffffffff][0x80]`. 307/196 records.
- **`selfidx == array position` for 307/307 and 196/196 records** — the
  array is self-indexing; +40 is structurally an index into THIS array.
- Record order == source.dae library_materials order (name at same index:
  307/307, 196/196) — the "which order" question is dead: there is only
  one order and the exporter still disagreed.
- **Sampler list**: N x 24 B records `[name_ptr][pad][type][1][v2][v2+4]`;
  type 13 = sampler2D, value block at v2 = `[1][so_ptr][255][255][255][255][
  texIdx]` (texIdx = 7th word; 255 = UNBOUND). type 7 = LightMapAtlas vec4
  (identity (1,1,0,0) for the street materials checked).
- **Image table**: 12 B records `[imageN_ptr x2][<name>.tga_ptr]`, 179/140
  entries (NOTE: extensions are case-insensitive — `.TGA` broke the first
  walk and silently truncated the table at 116/102, producing fake
  "tex255" unbound rows; fixed, and runtime-vs-source.dae DiffuseMap
  agreement went to **306/307 and 195/196**).
- Techniques seen: LightMapDC, StandardDiffuseDC, SimpleAdditive,
  AlphaMasking, NormalSpecOverbright, Reflections, TDKR-Vehicles,
  **LightmapVCBlendDC** (island-2 roads family, DiffuseMap UNBOUND,
  LightMap = Landmarks0 — bake-lit geometry).
  **[CORRECTED session 18: LightmapVCBlendDC is 4+4 materials, ALL park-
  ground grass/dirt/rock blends (T1/T2 = GC_Park_*), and ZERO street-stream
  segments bind them via +40 on either island. Its fragment shader is
  Color = LM(vCoord1)*2 * mix(Texture1, Texture2, vColor.a) *
  vec4(vColor.rgb,1) — a vertex-colour alpha blend requiring vertex
  colours its own (non-batched) streams must supply.]**
- Output banked: `extraction/re/runtime_mats_{island}.json`.

## 3. DECISIVE: render probes (`render_probe16.py`, renders in work/probe16)

**Round-4 tagging (session 17): these five probes are VISUAL,
UNQUANTIFIED evidence — they motivated the tests below but do not replace
them. The quantified case now rests on round4_street_evidence.py
(texel-validity by family + UV-footprint vs shuffle null) and
round4_delta16.py.**

XY-projected, UV-sampled renders of individual segments textured by their
+40 material's DiffuseMap vs the v5 exporter choice:

- seg199 (+40=11, GC_Z1_Props_Street): **a clean street lamp post** under
  the +40 texture. The v5 exporter had bound the SAME geometry to
  GothamCity_Road_Crossings_Island_1 (a lamp row is not a crossing page).
- seg1359 (+40=178): 620u elevated curve = **the monorail**, textured with
  GC_Residential_Props_Monorail.tga — v5 had it dark.
- seg1048 (+40=90): coherent curved **railroad track** (Railroad props).
- seg802 (+40=74): **trees** (trunk.tga) seen top-down.
- seg20 (+40=300): SimpleAdditive + billboard = glow plane (v5 dark).

**Verdict: +40 is engine-true; the v5 structural band-atlas binding was a
self-fulfilling heuristic** (raw UVs happened to fit plausible-looking
pages). The v15 deployed street tier is visually plausible but not engine
parity. The correction of record from session 15 also lands here:
+40=74 is NOT "the Roads0 material" — **m74 = trunk.tga DiffuseMap +
BakeGroup_Island1_Roads0 LightMap = the street-tree material** (210
segments); the session-15 "74 = Roads0 material" line is corrected.

## 4. batch_info vec3 groups — the street lightmap chain SOLVED

The reviewer's b/d direct test was run and FAILED as stated
(`lightmap_uv_test16.py`: b+d maps uv0 into the page at 44.7%/71.9% vs
null 49.4%/47.3%, identity 100%). But the failure itself was informative:

- collada LightMap sampler value blocks carry so_ptr -> **vec4 = (0,0,0,0)
  everywhere** — placeholders; the runtime Coord1_scaleoffset must come
  from batch_info (CDoubleBufferedDynamicBatchMesh consumes it, session 15).
- street verts have ONE uv (word 4). Stride-20 = 5 words, stride-24 = 6.
- **Vertex word 3 (w3) of stride-24 segments is the packed Coord1**
  (u16x2 / 65535). Stride-20 segments never carry LM-bound materials.
- The four vec3 groups at record offsets 109/121/133/145 are per-technique
  slots. Pairing sweep over LM-bound materials
  (`w3_coord1_test16.py`): **(a,d) = (offset 109 scale, offset 145 offset)
  wins for 40/40 island-1 and 40/40 island-2 materials** (b @121 and
  c @133 are other slots — the reviewer's letter labels were off by one).
  **[RETRACTED session 17: the pairing-sweep metric was the degenerate
  in-page test (scale ~1e-5 -> constant UV -> trivially in-page for ANY
  pair). The real pair is scale@121 + offset@145 WRAPPED.]**

**pageUV = w3_uv x a.xy + d.xy**: 100.00% inside [0,1]^2 on BOTH islands
(577,017 / 469,133 vertices), per-material coherent tile rects
(m90: [0.25,0.62]x[0.75,1.00] of Roads0, area 0.09; m229: area 0.01).
d values sit on the 1/16 grid 3.7x over null (bake-atlas tile grid);
w3 = 0 segments degrade gracefully to the flat d-tesel tint.
**[RETRACTED session 17: the 100.0000% in-page number is a degenerate
slot-109 artifact — the round-4 prescribed null showed ANY (a,d) pair is
in-page (284/284 d+a<=1). Superseded by pageUV = w3 x scale@121 +
offset@145 WRAPPED.]**

Engine model (street tier): `Color = DiffuseMap(uv0) x LightMap(pageUV)
x 2.0` with pageUV per-vertex from w3 — LightMapDC-f.glsl exact with
Coord1 = w3, Coord1_scaleoffset = (a.xy, d.xy) from batch_info.
**[CONFIRMED session 18, strengthened: the extracted LightMapDC-f.glsl
has NO Overbright uniform and NO vertex-colour term — `LightMapColor =
texture2D(LightMap, vCoord1) * 2.0` is a hardcoded literal and the vColor
multiply is commented out by the authors ("ATICA - removed on 26.04 to
save memory in batching"). The x2 is engine-exact, not an assumption.]**

## 5. +36 SOLVED (`plus36_probe16.py`)

Spearman(id36, dataOff stream order) = **+0.9977 / +0.9884**; vs bih grid
cell order ~0 (both axis permutations); 0 duplicates per island; ranges
0..3194 / 26..2191 exceed the visible-LOD segment counts (1517/1020) —
**+36 = the segment's global index in the zone stream across ALL LOD
levels** (lod_table references a subset). Not a building id, not a batch id.

## 6. Exporter v16 (`extraction/scripts/export_zone16.py`) — shipped

Binding rule per segment (+40 -> runtime_mats row):
- SimpleAdditive -> `<tex>|add`
- LightMap bound -> `<tex>|<lm>|2x` with **TEXCOORD_1 = w3*a.xy+d.xy**
  (per-vertex, V-flipped at the GLB choke point) — viewer
  makeCityMaterialLM = LightMapDC exact
- LightmapVCBlend / unbound diffuse + bound LM -> `|<lm>|2x` (bake-alone)
- otherwise -> `<tex>|d`; unknown/missing -> `__dark`

Results: island-1 1517 segments = 1091 lightmapped + 326 diffuse + 94
additive + 1 bake-alone + 5 dark + 3 missing-texture; island-2 1020 =
658 + 337 + 25 + 0 + 0. **99.5% / 100% engine-true bindings** (v15 had
~61% bound, and the bound part was wrong).

Deploy notes: the old `rm -rf models` lost LUT_000_default/LUT_023_lighting/
GC_VerticalFOG -> whole-screen black (the LUT post pass nulls out); restored
from v15. three r152+ auto-declares `attribute vec2 uv1` when geometry has
TEXCOORD_1 — app.js cityVertLM's manual declaration became a redefinition;
fixed with `#ifdef USE_UV1` guard (fallback vUv1 = vUv). Manifest v16
(40 GLBs, 21 street), APP_CACHE_VERSION v16. Headless verification
(`shots16.py`): full island renders, coherent night grade, monorail/lamps/
trees/billboards all textured; 435/436 lightmapped primitives carry varying
TEXCOORD_1.

## Shipped (committed)

- extraction/re/: agreement_test16.py(+.json), diag_plus40_class16.py,
  diag_offsets_orders16.py, runtime_order_test16.py, runtime_mats16.py,
  runtime_mats_{island}.json, bres_mat_records16{,b}.py,
  render_probe16.py, lightmap_uv_test16.py(+.json), w3_coord1_test16.py,
  plus36_probe16.py, decode_tex_pool16.py, restore_tex16.py,
  survey_plus40_16.py, shots16.py
- extraction/scripts/: export_zone16.py
- gh-pages: app.js (USE_UV1 fix, cache v16), models/manifest.json v16,
  21 street GLBs + 51 textures + aux textures

## Next (ordered)

1. Overbright: LightMapColor = LM*2 + vec4(Overbright) — find the
   technique param default (NormalSpecOverbright name suggests it matters);
   the current render is engine-exact only if Overbright = 0.
   **[RESOLVED session 18: there is NO Overbright uniform in any shipped
   GLSL; the x2 is a literal in LightMapDC/VCBlendDC. The street render is
   engine-exact as shipped.]**
2. The 8 unbound island-1 segments (3 missing textures + 5 dark) — identify.
3. Hero-unit generic-object records (unchanged from session 15).
4. Ground-material split: the streamed data has no park-floor/road-plane
   ground beyond what +40 binds; the big ground planes may be a separate
   non-streamed unit (GC_City_Plane) — reconcile with the v15 look.

## Round-5 status ledger (tagged session 18)

Every claim in this file whose status changed in sessions 17-18:

| Claim (session 16) | Status now |
|---|---|
| +40 = per-segment material index; compiled bdae self-indexing 307/307, 196/196 | **STANDS** (round-5 added the geometry-profile + enrichment evidence; see ledger in session-17 file for the footprint retraction) |
| (a,d)=(109,145) pairing, 40/40 wins | **RETRACTED s17** (degenerate in-page metric; real pair (121,145) wrapped) |
| pageUV = w3·a(109)+d(145), 100.0000% in-page | **RETRACTED s17** (degenerate artifact) |
| v5 band-atlas binding disqualified by agreement test | **STANDS** |
| Render probes (lamp/monorail/railroad/trees/billboard) | **visual, unquantified** (tagged s17; unchanged) |
| m74 = trunk diffuse + Roads0 lightmap (street trees) | **STANDS** |
| LightMapDC = Diffuse × LM × 2 | **CONFIRMED s18 at shader level** (x2 hardcoded; no Overbright uniform; no vColor term — author comment) |
| LightmapVCBlendDC = island-2 roads family | **CORRECTED s18** (8 park materials, 0 street segments; shader = vColor alpha blend) |
| TEXCOORD_1 = w3·a+d in exporter v16 | **SUPERSEDED s17** by v16.1 (scale@121+offset@145 wrapped) |
| "Overbright=0 assumption" / Next#1 | **RESOLVED s18** (no such uniform exists) |
| Deploy `rm -rf models` fragility | **FIXED s17/s18** (deploy_site.py: incremental sync + explicit allowlist, deletes outside `models/*.glb` impossible, --dry-run) |
