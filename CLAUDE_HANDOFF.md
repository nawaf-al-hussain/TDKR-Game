# CLAUDE_HANDOFF.md — problem brief for an outside AI collaborator

*Written 2026-10-09, updated after sessions 16-18. Everything below is
verifiable in this public repo: https://github.com/nawaf-al-hussain/TDKR-Game
— live viewer: https://nawaf-al-hussain.github.io/TDKR-Game/*

## 0. TL;DR — UPDATED AFTER SESSION 18 (round-5 review round)

We are reverse-engineering Gameloft's delisted mobile game **The Dark Knight
Rises (2012)** to rebuild its open-world Gotham City in a browser 3D viewer.
Over 16 research sessions we cracked the container formats, geometry, texture
decoding, material database, the bake/UV system, and the level placement
records.

**Both earlier blockers are now closed or sharply narrowed:**

- **Blocker A (LongDist skyline world placement) — SOLVED in session 13, and
  the session-12 result was WRONG.** The real record is a **typeId 0x14051**
  entry in the lvc DICT object stream (handler: `CLevel::LoadNextObject`
  branch @0x48ad00 → `CComponentBase::Load` + `CComponentMesh::Load` →
  `ConstructColladaScene` → **`CLevel::AddLowPolyLongDistanceNode`**):
  `GothamCity.lvc @0x55545: objId=111989, TRS pos=(-730.0, -1250.0, 0.0)
  rot=(0,-0,0) scale=(1,1,1), mesh='gc_island1_longdist.bdae'`.
  Session 15 hardened this: **AddLowPolyLongDistanceNode @0x48b140 applies
  NO further offset** (identity container node "LPLDBatchCollect" under the
  scene root; sole caller LoadNextObject; the batch merger uses
  updateAbsolutePosition). Two more negative tests were run and are
  **honestly negative**: the roof/road sweep (fraction of road vertices
  under roof footprints, ±60u) has **no sharp minimum at the record**
  (@record 0.0276 vs landscape mean 0.0247 vs global min 0.0102 @(+60,+46);
  constrained-by-building-coverage min 0.0231 @(-58,-10)) — like every
  density metric in this one-blob city it cannot discriminate; the
  placement rests on the engine record + centroid correspondence. The
  round numbers: the same (-730,-1250,0) TRS is shared by the 0x14051
  record and TWO 0x14050 reflection records (footprint_ic, railway) — an
  authored far-field group origin; it matches NO stream_info/bih_struct
  bbox corner or center.
- **Island-2's LongDist units have NO record in the main level** — the only
  0x14051 in `GothamCity_Island2.lvc` (@0x58a0a, same TRS -730,-1250)
  belongs to the separate island-2 level. All 5 island-2 skyline GLBs were
  REMOVED from the deployed site (v14). The island-1 family (5 GLBs) was
  re-placed at the engine's own TRS. Deployed as **v14**.
- **Q3 (runtime bake multiply) — CLOSED**: `LightMapDC-f.glsl` uses exactly
  two samplers (DiffuseMap, LightMap), `Color = Diffuse * LightMap * 2.0`
  (+fog). `StandardDiffuseDC-f.glsl`: DiffuseMap only. **No third sampler →
  no runtime scene/island bake multiplication.** `page_low` in the bake
  records is the low-LOD variant of the same page (LOD swap).
- **Session 14 corrections (after your round-2 review):**
  - **The "+0.66 ZNCC" is RETRACTED.** Your suspicion of city-shaped density
    was right. Full ±100u sweeps show (a) the ZNCC landscape is a broad
    ridge (max +0.19 at an unrelated offset), and (b) the session-13 number
    was a *framing artifact*: the FFT-ZNCC normalizes over the
    shifted-grid-intersection window, so the same data/placement/math gives
    **+0.6625 / +0.1558 / +0.0284** under three window conventions (the
    last = direct windowed Pearson, the convention-free definition).
    The honest discriminating evidence for the record TRS is now:
    the **engine record itself** + **per-prim centroid correspondence**
    (FP1/2/3 units vs the assembly: mean |d| 0.96/1.55/2.23 u, mean delta
    VECTOR ≈ 0.1-1.1 u — a wrong frame would give a coherent offset) + raw
    overlap (record 13,776 vs v13-offset 7,406 vs identity **0**).
  - **Skyline material bindings verified at engine level**: every material
    in every LongDist unit (island1+2, LOW variants) has **LightMap texIdx
    = 0xFFFFFFFF (unbound)** → the engine itself renders them
    Diffuse × white × 2.0.  The shipped GLB materials (`<page>|2x` for the
    LightMapDC meshes, `<tex>|d` for the 5 monorail StandardDiffuseDC
    meshes) are exact parity. No second sampler needed.
  - **The deployed site was stale (v13 served while main held v14) and is
    now fixed**: gh-pages branch redeployed at v14; a post-deploy smoke
    test (`extraction/scripts/site_smoke_test.py`, 53 checks: infra files,
    manifest parse, all 40 GLB sizes, all 51 textures, island-2 absence)
    passes. It also caught: the restored index.html never linked
    style.css (it is self-contained inline styles — style.css is a root
    sentinel), and manifest v14 carried stale per-GLB byte sizes.

**Blocker B — SOLVED IN SESSION 16 (street segment→material + lightmap UVs
+ batch_info semantics):**

- **Descriptor +40 IS the per-segment material index into the zone's
  compiled material array.** The quantified case, as of round 5:
  (1) the engine record itself (compiled bdae self-indexing 307/307,
  196/196, order == library_materials); (2) the round-5 GEOMETRY-PROFILE
  test (texture-independent): +40's family labels predict segment geometry
  (up-normal fraction, planarity, size) at 2.5-2.6x the majority floor
  while v5's labels score AT/BELOW the floor — eta² up to 0.64 vs ≤0.23
  (`round5_t2_evidence.json`); (3) the round-5 ENRICHMENT metric
  (density-normalized texel-validity): +40 1.086/1.096 vs v5 1.009/1.012
  vs shuffle-null 0.982±0.019 on the disputed popA slice — the round-4
  popA ordering (v5 ahead) was the page-density confound itself;
  billboards d=7.2σ and props_mono_rail d=5.0σ for +40. **Retractions:
  the round-4 UV-footprint "~20x null" was an ESTIMATOR MISMATCH** (the
  null thresholded the mean of 24 permuted doms; the matched single-perm
  null is 0.301/0.208 ≥ +40's 0.263/0.161 — retracted,
  `round5_footprint_recheck.json`), **and the class-UV-rect-tightness
  metric is degenerate (1.0 for every labelling)**. v15→v16 changed the
  texture of 99.6% of segments (v15 was 39% bound and the bound part was
  largely wrong — 89 v5-"road" segments are props_street by +40, 135
  v5-flat segments are trees). The direct renders (lamp row, monorail,
  railroad, trees, billboards) remain **visual, unquantified** support.
- **The session-10/11 v5 exporter bindings were DISQUALIFIED by the
  prescribed agreement test**: exact agreement 1/593 and 4/374 (null-level)
  under library_materials order AND alphabetical order AND 200-shuffle null.
  The band-atlas "structural" binding was self-fulfilling (its smoking gun:
  a street-lamp row bound to a road-crossings page). Wording correction to
  session 15: +40=74 is NOT "the Roads0 material" — m74 = trunk.tga
  DiffuseMap + BakeGroup_Island1_Roads0 LightMap = the street-tree material.
- **Compiled bdae material record (36 B)**: `[name_ptr][name_ptr][0][
  effect_ptr][N][sampler_list_ptr][selfidx][0xffffffff][0x80]`; sampler
  list = N × 24 B `[name_ptr][pad][type][1][v2][v2+4]`; type-13 value block
  `[1][so_ptr][255×4][texIdx]` (255 = UNBOUND); type-7 = LightMapAtlas vec4.
  Image table = 12 B `[imageN_ptr ×2][file_ptr]`, extensions case-
  insensitive (`.TGA` truncated our first walk — beware). Runtime
  DiffuseMap vs source.dae agree 306/307 and 195/196.
  Table: `extraction/re/runtime_mats_{island}.json`.
- **Street lightmap UV chain — CORRECTED IN SESSION 17, FORM PROVEN IN 18.**
  The round-3 claim "pageUV = w3·a(109) + d(145), 100.0000% in-page" was a
  DEGENERATE-ARTIFACT (slot 109 scale is ~1e-5 → pageUV collapses to the
  constant d; ANY (a,d) pair is then in-page — the round-4 prescribed null
  test showed exactly that, 100% everywhere, 284/284 materials with d+a≤1).
  The real chain is **pageUV = w3_uv × scale@121.xy + offset@145.xy with
  WRAP sampling**, and session 18 extracted the actual shaders
  (`effects.gla` in the APK): `LightMapDC-v.glsl` computes `vCoord1 =
  (Coord1·s + o) · LightMapAtlas.xy + LightMapAtlas.zw` and the type-7
  LightMapAtlas vec4 = (1,1,0,0) for ALL 284+184 LM materials → the
  shipped expression is the exact engine formula (identity second stage).
  Supporting anchors: m90's tile rect matches the banked Roads0 rect
  EXACTLY, the "near-black central park" segments sample page-shaped
  histograms under the new chain (flat single-texel under the old one),
  91/123 (isl-1) and 55/81 (isl-2) LM materials visit compact wrapped
  regions. **Honest caveat (round 5): the two distributional tests the
  round-5 review prescribed — permuted-parameter null and seam continuity
  — are INSENSITIVE here** (permuted (121,145) scores lum-std 0.111 vs
  shipped 0.128; seam |Δ| authored ≈ permuted, both islands, even
  same-page and in pageUV space — per-tile area bakes do not guarantee
  cross-material seam continuity). The chain is the best-supported
  mapping, not independently confirmed. w3 = two unorm16 lanes (LE:
  lo=U, hi=V); NO w3==0 street segments; 97.6%/98.2% of LM-bound
  stride-24 segments carry per-vertex varying w3; building-family
  stride-20 segments (3 + 1) fall back to a flat tint. collada sampler
  scaleoffsets are all (0,0,0,0) placeholders — the runtime fills them
  from batch_info (CDoubleBufferedDynamicBatchMesh).
- **Street vertices carry NO vertex colour — and the engine does not want
  one.** Session 18 extracted the street technique's shader:
  `LightMapDC-f.glsl` computes exactly `Color = DiffuseMap(uv0) ·
  LightMap(vCoord1) * 2.0`, alpha forced to 1, then fog — the ×2 is a
  HARDCODED literal (there is NO Overbright uniform in any shipped GLSL;
  the session-16 "Overbright" hypothesis is resolved) and the vertex-
  colour multiply is commented out by the authors ("ATICA - removed on
  26.04 to save memory in batching"). The viewer's street material is
  engine-EXACT as shipped. `LightmapVCBlendDC` (the only VC technique) is
  4+4 park-ground materials with **zero** street-stream segments. WRAP
  sampling is engine-supported (GL enum table at 0xb862f8 contains
  REPEAT/CLAMP_TO_EDGE/MIRRORED; no per-material flag in the bdae
  sampler records; the clamp variant scores lower structure).
  Exporter v16.1 ships the corrected chain; deployed as **v17** with the
  new deploy gate (URL crawl + incremental sync + luminance floor).
  Unbound segments: **5** (all m40=0, engine-unbound FlippedPlane), the
  "3 missing textures" were an uppercase-.TGA stem bug (fixed).
- **+36 SOLVED**: Spearman(+36, dataOff stream order) = +0.998 / +0.988,
  ~0 vs bih grid order → **the segment's global stream index across all
  LOD levels** (ranges 0..3194 / 26..2191 exceed the visible-LOD counts).
- **Exporter v16.1 shipped (deployed as v17)**: all street segments bound
  by +40 with real per-vertex TEXCOORD_1 through the corrected chain
  (100%/99.5% bound; v15 was ~39% bound and partly wrong). Viewer got a
  `USE_UV1` guard (three r152+ auto-declares uv1). Deploy = incremental
  sync (no more `rm -rf`), pre-deploy URL gate, live crawl smoke check and
  a headless luminance floor — the process that let v16 ship aux-texture
  loss and a live batarang.glb 404 cannot repeat.

## 1. Project context

- **Game**: The Dark Knight Rises, Gameloft 2012, Android, delisted. Version
  1.1.6b. Source: APK (7.8 MB) + OBB expansion (895 MB), both attached to
  release `v1.1.6b` in this repo (attestation in README §Provenance).
- **Engine bits of interest**: native lib `lib_libKRHP.so` (ARM A32, not
  Thumb, committed at `extraction/lib_libKRHP.so`); Lua bootstrap embedded
  in the level config.
- **Deliverable**: a GitHub Pages three.js viewer streaming the extracted
  city as GLBs (v17: 40 GLBs, tiers street/skyline/hero/fp/low/district).
- All RE artifacts (notes, decompilations, scripts, intermediate JSON) are
  committed under `extraction/` — this repo is the single source of truth.

## 2. Pipeline in one paragraph

`TDKR_v1.1.6b.apk + OBB` → `.gla` big-endian containers (16-byte header +
n×16 index table + name pool + chunks: `game_config.gla`, `l_gothamcity.gla`,
`l_gothamcity_tex.gla`, `commons_tex.gla`) → geometry chunks (.bdae meshes),
zone-stream archive (`GothamCity*.zip`, 168.5 MB, inside `l_gothamcity.gla`),
level config `.lvc` (**DICT object stream** — see §4), textures (PVR,
ZIP_SPLIT rgb/alpha pairs) → `extraction/scripts/export_city.py` builds
textured GLBs → `gh-pages/models/manifest.json` (tiers: street / skyline /
hero / fp / district / low) → three.js viewer `gh-pages/app.js`.

## 3. What the user sees TODAY (v17, deployed and gate-tested)

- **Boots**: street tier (21 GLBs, world-placed, **engine-true +40 material
  bindings with per-vertex lightmap UVs** — the ~600 dark near-tier
  buildings are GONE: buildings now bind their footprint/shops/walls
  diffuse atlases × their per-material bake tiles; only 8/2,537 segments
  remain unbound) **+ skyline tier (5 island-1 LongDist GLBs at the
  engine's own TRS (-730,-1250,0))**.
- The street tier now renders the engine's LightMapDC formula exactly:
  `Diffuse(uv0) × LightMap(pageUV=w3·a+d) × 2` per material.
- Island-2 skyline units removed (no main-level record; they belonged to
  the separate island-2 level). The island-2 hero units (monorail/railway/
  small-bridge) remain OFF-by-default research toggles.
- **Deploy = gh-pages branch @ v17, verified by
  `extraction/scripts/site_smoke_test.py` (incl. the app.js/index.html URL
  crawl), `site_release_check.py` and `viewer_luminance_gate.py`**.

## 4. The lvc DICT object stream — record-type dictionary (session 13, all from disasm)

Header: `'DICT'` magic, u32be tableOffset, wide-string flag byte, then from
offset 9: `[u16][u16 version=3][u32 objcount][records…]`. Every record =
`[u32be typeId][payload]`; strings are interned `[u32be index]` into a
counted table at `tableOffset` (GothamCity.lvc: 1617 strings). All reads
big-endian via `CMemoryStream` (ReadInt @0x339914, ReadFloat @0x339b94,
ReadString @0x33a0d4, ReadChar @0x3395d8).

| typeId  | Loader (disasm)                                | Payload read order |
|---------|------------------------------------------------|--------------------|
| 0x2657  | CTemplateLevelProperties::Load @0x2023bc (+ GI) | see `parse_lvc.py` |
| 0x2667  | CTemplateZone::Load @0x48d5f4                   | bool, str, f, bool, int(zoneId), 9f TRS, 3b |
| 0x265f  | CTemplateMetaZone::Load @0x48d708               | 4b, 3i, 9f, str    |
| 0x2662  | CSpawnPointObject::Create @0x2a7840 (handler @0x48af5c) | bool, i objId, 9f TRS, 3b, str, str(Lua), 3b, i |
| 0x2663  | marker object                                   | i objId, 9f TRS    |
| 0x2664  | ref marker                                      | i                  |
| 0x1869f | CTemplateBakeGroup::Load @0x48d870              | bool, i, 9f TRS, 3b, str(page), f, str(page_low), f |
| 0x14050 | CComponentBase::Load @0x1fe924 + CComponentMesh::Load @0x2d6ddc → ConstructColladaScene → **AddBatchNodeReflection** (flag byte may redirect) | bool, i objId, 9f TRS, 3b, str(mesh), 4 chars |
| 0x14051 | same → **CLevel::AddLowPolyLongDistanceNode**   | same               |
| other   | → CGameObjectManager::CreateObject @0x36774c (generic, component factory loop) | complex |

CComponentBase::Load read order (proved @0x1fe924):
`bool, int objId, float×9 (pos xyz, rot-euler xyz DEGREES, scale xyz),
bool×3`. The 0x14051/0x14050 handler multiplies the rotation by **π/180**
(const @0x48b120) and builds a glitch quaternion.

Counts in GothamCity.lvc: 23 zones, 226 spawn points, 24 markers, **1
LongDistance record**, **42 reflection records** (one per
`gc_footprint_*_reflection.bdae` + `gc_railway_island1_reflection.bdae`,
each with a real world TRS), 4 bake-group templates. Full walk outputs:
`extraction/re/lvc_records.json`, `lvc_island2_records.json`
(script: `extraction/re/lvc_walk13.py`); raw dispatcher disasm:
`extraction/ghidra/decompiled_r2/lnobj_full2.asm`.

## 5. THE BLOCKERS (all knowns, all unknowns)

### B. Street segment→material link + lightmap UVs — **SOLVED in session 16, hardened 17-18**

**What we needed**: for each segment of the streamed street geometry, the
material index into the zone material DB (307 island-1 / 196 island-2
materials), plus the lightmap UV convention. **Both are now solved at the
data level and shipped in exporter v16** — see §0 Blocker B for the full
proof chain. Summary:

- descriptor **+40 = material index** into the compiled bdae render-record
  array (self-indexing, order == library_materials; runtime tables:
  `extraction/re/runtime_mats_{island}.json`); descriptor **+36 = global
  stream index across all LOD levels** (Spearman +0.998 vs dataOff order).
- **vertex word 3 (stride-24) = packed Coord1**; batch_info slots
  **scale @121 / offset @145 (wrapped)** give `pageUV = w3·s + o`, now
  proven IN FORM by the extracted LightMapDC-v.glsl (with the LightMapAtlas
  second stage identity for every LM material). The b/c slots are other
  techniques' params; the earlier "b=(scaleU,scaleV)" reading was off by
  one slot; the round-5 review's "a@109 is the lightmap scale" reading is
  ALSO wrong — the lightmap scale is @121 (226/227 LightMapDC records
  carry real scales there), and @109's role is unresolved (see §5).
- The v5 band-atlas structural binding is RETIRED — the agreement test
  (prescribed round 3) showed it agreed with the engine chain at null
  level; render probes show it was binding lamp rows to crossing pages;
  rounds 4-5 quantified the flip (geometry-profile 2.5-2.6x floor vs v5
  at/below floor; enrichment +40 1.09 vs v5 1.01 on popA; 99.6% of
  textures changed). The round-4 footprint "20x" is RETRACTED (see §0).
- batch_info.bin remains `u32(197) + M × 197-byte records`, record m
  starts with byte m (island-1's records 256-306 break the byte-m rule —
  a layout quirk worth a look); the four vec3 f32 groups @109/121/133/145
  are per-technique/per-sampler UV parameter slots — for the street LM
  path the pair is **scale @121 + offset @145 (wrapped)**; @109/@133 are
  UNRESOLVED (see §5); rec 45–108 u16 array and stream_info X still open.

**Remaining unknowns (updated in 18):**

- **batch_info slot 109/133** — session 18 tested and REJECTED both easy
  stories: not per-material placeholders (9/227 + 5/141 LightMapDC records
  hold exactly 1/65535, the u16 dequant constant, but the population is
  broad, median 4.2×) and not a working Coord0 (uv0) transform (applied
  wrapped it does not beat the shipped /65535 — 16 vs 13 wins, mean Δ
  −0.009); position-scale rejected (f32). Per-technique layouts may make
  these offsets mean different things per technique. Open.
- batch_info slot roles for the 28/21 non-compact LM materials (m97
  Concrete a121=[-18.3,-3.2], m73 roads_details, footprint floors — large
  horizontal surfaces with multi-wrap scales; full list in
  `round5_t3_chain.json`); the u16 array (rec 45–108); stream_info X
  (234,466 / 303,832); stride-24 word 5 content ([u16][u8][u8=0]).
- **A discriminating test for the LM chain**: the round-5 distributional
  tests (permuted params, seam continuity) are insensitive in the
  area-bake regime; per-tile ground truth (e.g. an assembly bake-list
  rect table) would settle it.

**Also still open:**

1. **Hero-unit placements** (bridges/monorail/railway): names ARE plain
   interned strings in the lvc; the main (non-reflection) units are placed
   by the GENERIC object path (`CGameObjectManager::CreateObject @0x36774c`,
   component factory loop) — read order still to decode.
2. Secondary: ground-material split — the streamed tier has no park-floor
   ground beyond what +40 binds; the big ground planes may be the separate
   GC_City_Plane unit (the v15 band-atlas look may have been papering over
   this).

### Hero units (secondary)

Names are plain interned strings (NO hashing): `gc_bigbridge_2_islands.bdae`
(str#169, 1 stream ref @0x5562c), `gc_monorail_island1.bdae` (@0x46f1e6),
`gc_railway_island1.bdae` (@0x436ca5), `gc_water.bdae` (@0x4b01f),
`gc_island1.bdae` (@0x3c139d), etc. The generic CreateObject path
(component factory: `CComponentFactory::CreateComponent(int, CGameObject*,
void*)` @0x223e3c, loop over 12-byte entries `[typeId][fn][flag]`) reads
them. Read order for the generic payload = the next decode target.

## 6. Repo map (the paths that matter)

```
CLAUDE_HANDOFF.md              <- this file
README.md                      <- provenance, viewer link, SHA256s
extraction/REPORT.md           <- format spec (bdae, gla, textures)
extraction/re/RE_NOTES_session{9,10,11,12,13}.md
extraction/re/                 <- RE data + probes
  lvc_records.json             <- session-13 exact record walk (main lvc)
  lvc_island2_records.json     <- island-2 lvc walk
  lvc_name_refs.json           <- all stream refs to interesting names
  bake_regions.json / bake_regions_v2.json / bake_regions_v3.json
extraction/scripts/            <- all exporters/decoders (export_city.py v14)
extraction/scripts/lvc_walk13.py      <- the sequential DICT parser
extraction/scripts/lvc_scan13.py      <- name-reference scanner
extraction/ghidra/decompiled_r2/ <- disasm listings (lnobj_full2.asm = the
                                    FULL CLevel::LoadNextObject)
extraction/lib_libKRHP.so      <- the native library itself
gh-pages/                      <- viewer source (index.html, app.js, models/)
```

## 7. How to reproduce / inspect

```bash
git clone https://github.com/nawaf-al-hussain/TDKR-Game
# data (public release asset):
curl -LO https://github.com/nawaf-al-hussain/TDKR-Game/releases/download/v1.1.6b/TDKR_v1.1.6b_APK_OBB.zip
# restore raw containers, then:
python3 extraction/scripts/export_city.py --dry
# live viewer (as deployed, v14):
#   https://nawaf-al-hussain.github.io/TDKR-Game/
```

## 8. Concrete asks (ranked)

1. **A discriminating test for the lightmap chain** — the round-5
   distributional tests (permuted (121,145), seam continuity incl.
   same-page/UV-space) are insensitive in the per-tile area-bake regime
   (`round5_t3_chain.json`). If you can find a per-tile ground-truth table
   (assembly bake-list rects per material?) the chain can be confirmed or
   falsified outright.
2. **batch_info slot 109/133** — round-6 census: over LightMapDC both
   slots are <=1e-4 in every component (no origins, no working scales —
   C2/C3/C5 degenerate by construction). The exact-dequant occurrences
   (9 tiles_* isl-1 + 5 Material__4986_* isl-2, all with s121=(0.5,0.5))
   read as the Coord0-identity scaleoffset (1/65535, 0) written explicitly.
   What the engine really binds for Coord0 on OTHER techniques (NSO etc.
   carry real 109/133 values) is still open (`round6_slot_tiling.json`).
3. **Generic object records** (CreateObject component loop): read order for
   the non-special typeIds so the hero units (bridges/monorail/railway)
   get their world TRSs.
4. Sanity checks welcome on the round-5/6 evidence chain
   (`round5_t2_evidence.json`, `round5_footprint_recheck.json`,
   `round5_t3_chain.json`, `round5_pipeline.json`,
   `round6_geom_grouped_cv.json`, `round6_pagetypes.json`,
   `round6_slot_tiling.json`) — note the round-6 geometry DOWNGRADE:
   grouped CV shows the segment-level signal is material-template
   consistency (only billboards generalize at family level); the "+40
   covers all 2537 segments decisively" wording is retired.
5. Anything that looks wrong in the deployed pipeline that we've gone blind
   to after 18 sessions of fixes (fresh eyes welcome).

## 9. Do-not-re-suggest list (all fixed and verified)

- UV-fit / edge-density page selection (replaced by authoritative
  assembly-bdae footprint→page map).
- `flipY=true` in three.js GLTF loader (game UVs are bottom-origin; GLB
  choke point flips V).
- Using bake/lightmap pages as building albedo; mode "2x" for these units.
- Per-footprint LongDiffuseMap aliases as standalone textures (they are
  runtime bakes of the assembly pages).
- Re-encoding textures below 2048/q88.
- **Hash-hunting the lvc names** — the strings are plain interned strings.
- **typeId 0x2662 as CTemplateObject** — it is CSpawnPointObject; the
  (-141.69,-681.15) "island placement" was Batman's spawn point.
- **Island-2 LongDist at identity / any main-level transform** — no record
  exists; those units belong to the separate island-2 level only.
- A third runtime bake multiply for LongDist units — LightMapDC has exactly
  2 samplers; the shipped bake pages are final. The LongDist materials'
  LightMap sampler is UNBOUND (0xFFFFFFFF) in every unit — engine parity
  is `<page>|2x` (×2 with white LM), already shipped.
- **The session-13 "+0.66 ZNCC" as placement evidence** — retracted
  (framing-dependent window artifact: +0.66 / +0.16 / +0.03 under three
  window conventions). Density correlation does not discriminate skyline
  placement in this city; use the engine record + centroid correspondence.
- **batch_info.bin as "197 records of 307/196 B" (either orientation)** —
  the layout is `u32(197) + M × 197 B`, one record per material, record m
  starting with byte m. Any interpretation must reproduce
  `body[197*m] == m` for all m.
- **batch_info slot letters as fixed meanings / "a @109 = LM scale"** —
  the four vec3 groups are PER-TECHNIQUE slots; for the street LM path
  the pair is **scale @121 + offset @145 (wrapped)**. Slot 109 is a ~1e-5
  degenerate slot: any "100% in-page" claim built on it is vacuous (the
  round-4 null proved every (a,d) pair lands in-page when the scale is
  ~0). The session-16 "100.0000% in-page" is retracted as evidence.
- **batch_info b/d as a transform of uv0** — the reviewer-prescribed
  test failed (44.7%/71.9% vs null ~49%); the base is **vertex word 3**
  (packed Coord1), not the diffuse uv0. Identity-on-uv0 trivially lands
  in-page and proves nothing.
- **The v5 structural band-atlas binding as ground truth** — retired in
  session 16 (agreement test null-level; render probes show lamp rows
  bound to crossing pages). Street bindings come from descriptor +40;
  rounds 4-5 quantified the flip (geometry-profile vs floor; enrichment
  on popA; 99.6% of textures changed v15->v16).
- **Raw texel-validity as a universal binding metric** — it is
  page-density biased: dark-pad thin-stroke cells (street props, coronas,
  tree trunks) score LOW for the CORRECT binding because most of a cell
  is black padding, while full-bleed road pages score high for ANY UVs.
  Use the round-5 ENRICHMENT metric (density-normalized) and the
  geometry-profile test instead.
- **UV-footprint dom95 with a mean-of-perms null** — the round-4 "~20x"
  was an estimator mismatch (matched single-perm null ≥ +40's rate).
  Any future footprint use must threshold per-perm outcomes, not the
  mean, and should condition on atlas-like permuted pages.
- **Tile-partition as an (a,d) null** — bake pages are AREA bakes:
  different materials in one area legitimately share tile regions, so
  non-overlap is the wrong hypothesis (the test saturates at 100% for
  both authored and null).
- **"Street vertices carry vertex colour"** — they do not (both strides
  checked; word 5 is not RGBA/octahedral). Any LightmapVCBlend reading
  must come from elsewhere.
- **"74 = the Roads0 material" (session-15 wording)** — m74 = trunk.tga
  diffuse + Roads0 LightMap (street trees). Roads0 is its LIGHTMAP page.
- **+36 as a building/batch id or bih-grid order** — it is the segment's
  global stream index (Spearman +0.998 vs dataOff order; 0 correlation
  with grid order).
- **Reading the compiled bdae image table case-sensitively** — some image
  files end `.TGA`; a case-sensitive walk silently truncates the table
  (cost us tex255 ghosts until fixed).
