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
   falsified outright.  Round-7 narrowed the problem: ALL 149 |s121|>1
   LightMapDC materials sample BakeGroup_* area-bake pages, and the
   shipped chain MULTI-WRAPS the bake on 16 of the 45 questioned
   materials that have street segments (m97 18x, m73 5.5x/24 segs, m76
   3.8x/62 segs, m178 2.5x/43 segs — `round7_lm_pages.json`); 16 are
   single-ish, 11 sub-rect (chain plausible).  The s121-as-diffuse-tiling
   alternative is MIXED (fixes the below-band densities of m73/m40/m180
   but absurdly tiles item atlases).  OPEN: what the engine actually
   binds for Coord1 on the multi-wrap materials — a disassembly pass on
   the batch_info consumer would settle it.
2. **batch_info slot 109/133** — round-7 byte-level reinterpretation
   REFUTED the u16/u8/flags/counts hypothesis: mantissa bytes at full
   entropy (210-218 distinct of 218), exponent bytes in the tiny-float
   band 0x32-0x3A, repeat share 0.014 = chance, no correlation with
   segment counts, no 109==133 pairing (`round7_slot_bytes.json`).
   Sharper per-technique fact: (121,145) carries plausible scale/offset
   in EVERY technique while (109,133) carries tiny floats (1e-6..1e-3)
   in EVERY technique (NSO included) — so the engine's Coord0 transform
   is not stored in batch_info for any technique.  14 of 368 LightMapDC
   records are explained (explicit tool-written (1/65535, 0) identity
   echoes); 354 records unexplained.  OPEN: disassemble the uniform
   upload path for the LightMapDC technique to find where Coord0 really
   comes from (hardcoded dequant is the leading candidate).
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
6. **gh-pages stray cleanup** — the new staging-from-manifest gate
   (`extraction/scripts/staging_manifest_gate.py`) FAILS on 3 unreferenced
   v16-leftover textures (GC_Park_dirt.jpg, GothamCity_Road_Island_2.jpg,
   GothamCity_sand_tile.jpg).  Remove them through a reviewed
   deploy_site.py extension (texture strays are currently never deleted
   by design); the gate stays red until then.
7. Round-7 matched-granularity AMI is banked
   (`round7_geom_ami.json`): +40 vs geometry clusters AMI 0.326/0.454
   (z 147/139), shuffled at null, v5 partially circular (its binder's
   flat/vertical split is itself geometry).  Live street-level evidence:
   `extraction/previews/round7_street_block{0,1,2}.png` (visual,
   unquantified); network-log gate PASS (`round7_netlog.json`).

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

---

## SESSION 22 (round 12) — 2026-10-13 — **PUSHED 2026-10-13 (session 23): main @ 7e96326 and gh-pages-staged @ c7f73c9 are on the remote; LIVE gh-pages REMAINS v17 @ f22b098 until the user merges gh-pages-staged. Gate results in this section: v18-staged PASS 26/26 vs v17-live FAIL 21/26.**

**State**: sandbox was reset AGAIN (sixth round running); nothing since v17
has reached the remote. Remote heads: main @ `3ae66a2`, gh-pages @ `f22b098`
(v17 live). This session was rebuilt from the round-12 briefing + the
session-18 repo state; sessions 19-21 artifacts were re-derived.

**DEPLOYED THIS SESSION (v18, via deploy_site.py, dry-run first)**:
- **Skyline boot fix re-applied** (12-line app.js change, lost in the
  session-20 reset): the skyline tier was `enabled` at boot (v14 policy)
  but the boot loader only streamed the street tier — the 5 island-1
  LongDist GLBs never loaded (v14-v17). Fix streams skyline right after
  street. Manifest v18, cache-bust v18. **NOT PUSHED** — gh-pages-staged
  @ c7f73c9 local; the user must push.
- **Gate v2** (`extraction/scripts/gate_v2.py` — NEW; replaces
  viewer_luminance_gate.py as the pre-deploy gate): stream-complete from
  real network responses (boot-enabled = street+skyline = 26 GLBs) +
  fingerprint (128x72 luminance r vs stored reference) + spatial checks
  (mean>=8, near-black in [0.5, 0.97] — the LOWER bound is new: catches
  uniform mid-load frames — quadrant floor 4, ratio 12, L/R asym <= 0.6).
  Results (labelled by version): **v18 staged/deployed tree: PASS,
  stream 26/26, fp 0.994, asym 0.373-0.416. v17 live copy: FAIL,
  stream 21/26** (mean luminance 12.78 = the calibrated v17 default view).
  Synthetic controls (all FAIL correctly): black, half-black,
  right-half-dim @ mean 10, right-half-dim @ mean 3, mid-load uniform
  (caught by the new night-floor check), street-GLB removal (25/26).
  **The fingerprint alone would NOT have caught the missing skyline**
  (r(staged, live) = 0.816 >= 0.5) — it detects drift, not correctness;
  skyline placement still rests solely on engine record 0x14051.

**batch_info.bin layout — NOW ENGINE-PROVEN end-to-end** (Unicorn emulation
of loadHeadersAndSkipData @0x8e1d34 [symtab-true; ghidra table's 0x8f1d34
is a shifted export] over all 503 records, 0 errors; pure-Python parser
cross-validated byte-exact):
`[u16 self][30 attr bytes = attrId->pairbuf-slot map, 0xff=absent][u8]
[u32le N][N x 12B desc {u32 byteOff; u16 attrId; u16 f2(type); u16 f3;
u16 stride}][(K+1) x 24B pair (vec3f scale, vec3f offset) — SCALE FIRST]
[u32 X][seek X*desc0.stride][24B tail {t0, kind=1, count, ...}]`.
K = popcount(mask & 0xFFFE) (attrs 1..15 only; Normal=16/Color0=17 get no
pair) — K comes from `CVertexStreams::allocate` -> ctor stores it at +0xc:
**engine-derived, not harness-provided** (the T3 circularity worry is
closed). Pair slot j <-> descriptor j (slot0 = position = zeros). Attr
registry (string table @0xb87518): id0=Position, **id1=TexCoord0 (word3,
byteOff 12), id2=TexCoord1 (word4, byteOff 16)**, id16=Normal, id17=Color0.
The uniform-commit path (commitCurrentMaterialAutomaticParameters
@0x7e3290, dispatcher types 0x37/0x38/0x39/0x85-0x8a) builds
`CoordX_scaleoffset = vec4(pair[slot(attr)].scale.xy, pair[slot(attr)].offset.xy)`
via the 30-byte map — **so the engine chain is**
`vCoord0 = w3_raw * s109.xy + s121.xy`, `vCoord1 = w4_raw * s133.xy + s145.xy`
(GL_REPEAT; scales are sized for RAW u16: diffuse scales x65535 = 1..52
tiling, lightmap scales x65535 <= 1.0). **The shipped v17/v18 chain
`frac(w3_deq * s121 + s145)` contradicts the consumer on both channels**
(s121 is Coord0's OFFSET used as Coord1's SCALE; source word w3 is
TexCoord0, not TexCoord1). This upgrades session-21's "contradicts the
consumer" claim to PROVEN at the uniform-commit level.

**T1 falsifiable tests of EF2raw (`t1_tests.py`) — VERDICT: KEEP v17.**
- Containment (raw, unwrapped): EF2raw 0.341/0.259 vs permuted-pair null
  0.317+/-0.016 / 0.274+/-0.021 (z=+1.51/-0.71 — **at null**). The engine
  relies on GL_REPEAT; offsets are negative (>1) for some materials
  (e.g. -18.25 m97-isl1, 3.33 m76-isl2), so raw containment was never a
  design goal. Shipped chain: 0/123 inside (unwrapped), multi-wrap 122/123.
  Identity (w4 dequant): trivially 1.0 by construction — vacuous, not
  evidence.
- Partition: EF2raw total-area 4.60x (isl1) / 2.78x (isl2) of page area,
  pairwise overlap 0.653/0.687 vs permuted-origins null 0.560+/-0.039
  (z=+2.38) / 0.549+/-0.026 (z=+5.27) — **overlaps MORE than random
  origin placement**; shipped/identity 11.8-16.2x. The briefing's hope
  ("total area near 1.0x, low overlap") is FALSIFIED for the engine chain
  too: bake pages are REPEATED/tiled per city area under the engine chain
  (~2.8-4.6x oversubscription), consistent with round-6's "area bakes
  with legitimately overlapping tiles" surviving in modified form.
- Per-segment spread (pairs >= 200u): EF2raw non-overlapping footprints
  0.711 (isl1) / 0.605 (isl2) vs shipped 0.002 / 0.001 — shipped collapses
  far-apart segments to identical patterns; EF2raw vs its own null:
  0.786+/-0.004 (z=-18.3) / 0.472+/-0.008 (z=+16.2) — **islands disagree**;
  reported as-is. Decision rule (containment AND partition must beat
  nulls) -> **EF2raw not shipped; v17 chain retained; no claim that the
  shipped chain is engine-true** (it is proven NOT engine-true; its
  render-superiority is also unproven — next session: staged EF2raw build
  + visual before/after review).
- m128/m141 "compact rects under EF2raw": stays a **plausibility
  argument, unproven** (T1 did not support the partition model).

**T2 classes**: records (N,K) isl1: (4,2) 276, (4,1) 9, (5,2) 9, (3,1) 11,
(3,0) 1, (1,0) 1; isl2: (4,2) 178, (4,1) 7, (5,2) 6, (3,1) 4, (1,0) 1.
Segments: isl1 (4,2) 1092, (4,1) 325, (3,1) 95, (3,0) 5 of 1517; isl2
(4,2) 658, (4,1) 337, (3,1) 25 of 1020. **All lm-bound street segments are
(4,2)** — the exporter's fixed bytes 109/121/133/145 land on the right
BYTES for every shipped uv1, but with the wrong semantics (above); the
briefing's "K<2 materials 23 and 12" was wrong — m23-isl1 is (4,2);
m12-isl1 is (4,1) (K=1, no TexCoord1, and not lm-bound). TexCoord1's pair
offset is 133/145 ONLY in the (4,2) class; N=3 shifts -12, N=5 +12 ✓
(session-21 shift rule confirmed); the pair index is TexCoord1's
DESCRIPTOR INDEX, not a constant.

**T3 raycast (rebuilt double-sided raycaster, grid-pruned)**: cameras are
RECONSTRUCTED (session-21's were lost) — same-camera identity is NOT
provable; the 19.9% coincidence is noted, not claimed. camA (default-view
proxy, fitCamera geometry, fov 55): ground-third hits 0.184 / void 0.816;
hits by +40: m76 42.4%, m6 11.9%, m23 10.2%... (labels NOT carrying the
claim — index-level report); hit heights median 7.2u (street level).
Positive controls FAILED informatively: camB above a Roads0-bound segment
(+40=25) returns 4.4% hits, 0/71 same-material (hits are m17/m229/m172);
camC plaza 2.9%, 0 same-material. Interpretation: the street archive's own
floor is SPARSE — most downward rays find nothing, and the triangles under
a road segment's centroid belong to OTHER materials — the void is largely
REAL in the street archive, not (only) a raycaster artifact; but per
ground rule 8 the raycaster is NOT certified for per-material attribution
(positive control failed). Far-LOD slabs (+40 value 34/35 in
GothamCity_low): 5/6 parsed extents are garbage (low-archive stride
misparse — vertex format differs); ONE sane slab x[-710,0] y[0,2]
z[0,779] suggests real ground slabs exist; **slab-vs-miss coverage NOT
established** (method could not see reliably; needs the low-archive
vertex-format pass). Verdict unchanged in substance: street floor
near-black/void remains OPEN; "road-family triangles exist and are
intersected" stands (m76/Roads0 42% of ground hits).

**Claim status changes (rounds 7-11)**: see RE_NOTES_session22.md §7.

---

## SESSION 23 (round 13) — 2026-10-13 — **main @ <see commit> pushed; gh-pages-staged advanced with v19 (engine-chain A/B, default pixels unchanged); LIVE gh-pages REMAINS v17 @ f22b098 — v19 is staged, not live**

**State recovery**: sandbox was NOT reset this round (previous disk still
materializing at start). Session-22 bundles verified and fetched:
main_s22_inc.bundle -> 7e96326 ✓, ghpages_staged_s22.bundle -> c7f73c9 ✓.
**First successful push in 7 rounds** (user supplied a PAT): main 3ae66a2 ->
7e96326 and gh-pages-staged -> new remote branch @ c7f73c9. Live gh-pages
NOT touched (ground rule 7: live is v17 until the user decides).

**T1 diffuse-channel test of the engine chain** (scripts/t1_diffuse.py,
t1_class42.py): v17's uv0 is words[:,4] — for (4,1)/(3,1) records that is
Normal/Color0, i.e. STRUCTURALLY INVALID as a diffuse uv; the engine chain
(w3_raw*s109+s121) is valid for all classes. Enrichment (permuted-param
null K=100) is weakly powered (most city diffuse textures are near-fully
content -> insensitive); strongest pro-engine signal: 8/10 BillboardRoof_01
(4,2) materials at enrichment 1.36-1.46 on BOTH islands (null 0.99+/-0.19);
4 dark-cell anomalies (m86/m128 isl1, m13/m5 (4,1) tint constants)
UNEXPLAINED. Atlas-cell containment: engine at permuted-null (z -0.32 /
+0.22) — INSENSITIVE; v17's higher rate is a footprint-size artifact.
Texel density (the decisive test): engine roads 85-96 texel-u/m, m97/
Concrete_02 512px worked example = 52 repeats / 136.7m = 195.8 texel-u/m
(~5mm/texel); v17 = 3.7 texel-u/m (~27cm/texel, 10x too coarse; degenerate
0.0 on (4,1) roofs; 251 on props). Counts: isl1 125/134 materials scale!=1,
1484 segments; isl2 83/88, 984.

**T2 staged A/B (?chain=engine)**: export_zone19.py adds TEXCOORD_2/3
(engine Coord0/Coord1, per-descriptor field selection; (0,0) when no
Coord1 stream) with v17-parity default uv0/uv1; app.js swaps uv<-uv2,
uv1<-uv3 + RepeatWrapping under ?chain=engine (three r160 maps them
natively). Manifest v19, 21 street GLBs 52.6->72.3MB. Default render
pixel-identical (gate fingerprint 0.994 vs v18 ref). A/B renders (block0,
plaza; visual, unquantified): v17's flat cyan wash replaced by coherent
bake structure under the engine chain — engine looks BETTER. Numeric
lightmap stats comparable (isl1 mean 44.3 vs 44.1). RECOMMENDATION: make
the engine chain the default after user review; NOT done (per instruction).
Stride-28 ((5,2)) segments remain unshipped in v17 AND v19 (~60 segments;
documented gap).

**T3 raycaster rebuilt + certified** (raycast_t3_v2.py): double-sided MT,
grid+DDA, giant-tri global list, exact z-window culling; 640x360 full-frame
(half pitch; giant-tri pollution), ground-third 76,800 rays/camera.
CERTIFIED at algorithm level: (c1) analytic 278/278 exact t=5;
(c2) synthetic nearest/far-only/double-sided PASS. The SPECIFIED in-archive
controls are UNSATISFIABLE on this archive: (a)/(b) self-return at +40u
0/100 — the archive contains 5,108 giant overhanging wall tris (m40=11,
extents to 600u) caging the city (worked example in results JSON);
(c) two-sided centroid rays 0/278 same-triangle (taxonomy: 71 coplanar
strip neighbors + 377 giant tris + 107 other geometry).
Per-camera first-hits (caveat: first-hit = depth-buffer view):
block0 hit 1.000 void 0.000 (m11 88.1%, m74 10.9%; heights 12.4/83.1);
plaza hit 1.000 void 0.000 (m11 57.4%, m76 13.7%, m73 12.1%, m14 11.3%);
roadtop nadir hit 1.000 (m76 63.2% at v0-height ~83u = an ELEVATED deck;
m11 36.8%).
**RETRACTED (round-11/12): "street floor renders near-black / void ~80%"**
— method artifact of the failed-control raycaster. Round-12 "archive floor
is sparse" DOWNGRADED to unestablished. Slab coverage (+40 value 34/35,
GothamCity_low): vacuous at these cameras (empty miss set); low-archive
stride misparse still OPEN. Viewer LOD swap: low tier is manual; engine
swap distance not RE'd — OPEN.

**T4 skyline/v19 gates**: gate v2 on v19-staged PASS 26/26 fp 0.994;
controls all FAIL correctly (black, half-black, right-dim@10, right-dim@3,
mid-load uniform, street-GLB removal 5/26 fp -0.071, NEW skyline-GLB
removal 21/26 — reproduces the live-v17 signature; fingerprint is
basis-dependent: -0.044 vs stored ref here, 0.816 screenshot-vs-screenshot
in session 22 — stream-complete is the deterministic detector). Boot GLB
list = exactly 21 street + 5 island-1 LongDist skyline; NO island-2
LongDist at boot. Skyline placement still rests solely on 0x14051.

**Session-22 file corruption note**: extraction/re/session22/batch_parser.py
(main()) and raycast_t3.py were committed with mangled syntax; their RESULT
JSONs are intact and were re-validated this session (parser 503/503 vs
harness). Use extraction/re/session23/ scripts instead.

## RECORD CORRECTION (session 52/53, 2026-10-23) — the zone-renderer 0.99 target IS valid and MET

The session-50 T1 redefinition ("corr>=0.99 vs the exact-float reference is UNATTAINABLE for any
GPU-faithful renderer; the GL render is DEFINED as the engine-faithful reference") and the
session-51 "swiftshader-suspect / regime-dependent draw artifact" statement are BOTH SUPERSEDED.

Root cause found in session 52 (city_bisect2.html, commit 969bd3e): the diagnostic pages' draw
loop had a texture-UNIT CLOBBER — texZget's cache-miss path binds on the CURRENT unit, so a
lightmap resolving on a miss rebinds unit 0 (the diffuse) to the lightmap -> Color = LM^2 x 2
(near-black). 4/120 zone LM batches were affected (mids 73, 132, 29, 30). The session-50
"sub-pixel road-detail geometry" attribution and the session-51 minification-artifact story were
observations of this defect, not engine/GPU properties.

After the one-line fix (pre-resolve both textures before any bind): mat73 zoom step2 ratio
0.9954 / step4 1.0068 vs an independent CPU per-pixel model; whole-zone corr 0.9285 -> 0.9923.
The game pages (integration.html, integration_lazy.html) pre-resolve at batch-build time and were
never affected; the live viewer uses THREE's internal unit management. Session 53 adds a
draw-time unit audit on EVERY zone draw of all three pages (bisect + both game pages): 0
mismatches expected and measured (extraction/re/session53/).

Consequence for future work: treat corr>=0.99 vs the CPU per-pixel reference as the STANDING
acceptance bar for the zone renderer; do not re-litigate the s50 "GL is the reference" clause.

## SESSION 54 (round 44, 2026-10-23) — glide/grapple parameters DECODED; state/clip table applied; per-effect corr boosted

**T1 glide parameters**: s53's "CComponentGlide::Load = 2x ReadInt + 41x ReadFloat" was a
Thumb-mode junk disasm (the s48 warning applied). ARM truth @0x3c0938: Load = ReadInt +
21xReadFloat + ReadInt; object 0x60 B = [vptr@0][int1@4][f0..f20 @8..0x58][int2@5c].
Class id 0x0110ce1f (GenerateComponentTemplate case @0x36b0e0; vptr = _ZTV15CComponentGlide
@0xbd8990 + 8; 66+ factory ids - the full sweep found 158 pc-rel case sites; s25's 49-case
extraction was partial). The component is LIVE (not vestigial): CGameObjectManager::Reload ->
CGadgetManager::AddObject resolves it from templates 'Glider' 0x2674 (slot int1=0) and
'Glider_Plunge' 0x4c741 (slot 1); CGadgetManager::GetGlide(0/1) returns it;
RefreshForcesGlide (sink = f0 + (f1-f0)*|pitch| = 4 + 12*|pitch| u/s), UpdateNavGlide and
SetInitialGlideAngle (f10 = initial pitch DEG; engine hard default -30) consume its fields.
NO Glider instances exist in any of the 12 lvc files - the parameters come from the gol.bin
template payloads (flag-0 components DO get template-payload defaults at Reload; the s24
parser's "template data skipped" note was the missing piece). Decoded: Glider f0..f20 =
4,16,14,4,16,1,6,0,2,16,-45,-60,30,35,1.25,0.05,45,0.5,30,30,40, int2=600; Glider_Plunge
f10..f20 = -60,-80,-30,40,6,0.1,35,6,30,100,15. Validation: 10/21 floats byte-identical
across the two independent templates; consumer field offsets match the layout exactly.
Named statics (.data): k_glideWallEvadeDistance 6, MinDistance 1, MaxAngle 10,
s_fallAheadOffset 0.4. OPEN: the .bss CLevel::s_glidePitchMin..s_glideDeadAngle family
(GOT-indirect, 7-13 read sites each) - their writers were not located; values not extracted.
Staged slice (?s5=1) now: fwd 16, sink 4+12*|pitch| u/s, pitch0 -45 deg, wall-evade
analogue, ledge-stand at grapple end; placeholders behind ?s5legacy=1.

**T2 grapple targets**: waypoint census (CWayPointObject records, engine cases 0x798f/
0x2666/0x4741): GothamCity 8,428 / Island2 4,048 / Police_Station 315 / Military 227 /
StockExchange 219 / Underground 198 / ThePit 142 / Stadion 49 / BatCave 31. Flag byte
uniform (1) - no per-record grapple discriminator (runtime selection via the
GetGrapnelTargetPosition virtual + range/LOS filters). 25.5% of sampled waypoints within
2 m of walkable nm ground vs 2.0% uniform null. The slice now pulls to REAL waypoint
anchors decoded from the user's lvc (elevated-first scoring), portal-edge BFS fallback.

**T3 clips**: landing transition now _065_glide_idle_to_run (table state
Grapnel_Horizontal_To_Glide_Idle) before _008_run; GLB whitelist 7 clips; pull stays
_089_grapnel_pull; 12 glide-family + 4 grapple-family clips tabled, ~88/104 have no
state-table row (bdae anim_pack node bindings remain the standing gap).

**T4 per-effect corr (boosted)**: label-mask method (geometry mask, value-free - both
families render near-black; a mean>8 filter caps them). StandardDiffuseDC n 76 -> 777,
corr 0.9079 -> 0.9764, ratio 1.0161, IoU 0.9873 (alignment control); AlphaMasking
n 29 -> 342 comparable (1,793 geometry px), corr 0.8256 -> 0.9999, ratio 1.002; wronglm
positive control 0.9999 -> 0.7768. VERDICT PARTIAL vs the literal "thousands" criterion
(zone geometry caps: SD = dark water plane + sparse props, AM = vertical fences top-down).

**T5 memory floor**: empty three.js 84.9 MB; +170x512^2 RGBA GPU set only +23.5 MB (uploads
lazily materialized); game default 813.5 MB peak / 6.1 s; poolchunk 690.8 MB / 8.4 s;
gates PASS, digests unchanged. <600 NOT reached; residual = browser-internal copies + soup.

**T7**: live verified (viewer 94 reqs/0 failed/0 errs; walktest 6/0); NOTHING deployed;
deploy plan for staged-s44 @ 6145545 written; real-GPU check still PENDING (page verified
working during the T4 renders).

Local refs after s54: main dfcd2eb (s51-s54 unpushed), gh-pages-staged-s44 6145545,
s41-city-slice 7b0807e. Bundles: download/bundles_s54/.

### s54 remaining-work estimate update (sized)
- IN: walkable world, character renderer + animation, Lua shim, browser asset pipeline,
  user-file material binding, descriptor decoding, engine shader + fog chain, zone renderer
  (corr 0.9923 standing), glide + grapple as gated slices with DECODED engine parameters
  (component floats + waypoint anchors + state-table clips).
- NOT in (sized, unchanged where still true):
  - combat/AI/mission flow: 4-6 sessions (unchanged)
  - audio: 1-2 (unchanged); UI: 1-2 (unchanged); cloth cape: 1 (unchanged)
  - cross-region navigation: 1-2 (unchanged); city-scale lit rendering from user files: 1-2
  - glide/grapple FULL behavior (pitch/roll stick dynamics, rope render, QTE timing,
    dive/roll landing variants): +0.5-1 session (was 1-1.5; the 21-float decode + anchors
    + clips landed this session)
  - CLevel::s_glide* .bss static values (pitch/roll/yaw clamp+rate family): 0.25-0.5
    (find the writers; the GOT-indirect read sites are catalogued in session54)
  - memory <600 MB: bounded by swiftshader/Chromium-internal copies - 0.5 session to verify
    on real GPU only (floors now measured: 84.9 + 23.5 + soup)
  - real-GPU validation run: pending user paste-back (0.25 to analyze)

### s55 (round 45) — deploy audit, glide 2nd signal, grapple data, memory, combat survey
**T1**: live site healthy post-deploy (8 variants, 0 errors; live ?s5=1 gate reproduces
soup 00ce7970/137893 + routes 10/10). Deployed tree = 194 files 113.82 MB, 99.54%
game-derived (street GLBs 60.8 MB, tex 51.05 MB, patch.json 1.06 MB, lvc_gol_templates
85 KB, batman.glb 299 KB) — removal is the user's call; per-page dependency map in
s55_t1_asset_inventory.json. Title fix on branch s55-t1-title-fix @0cea8b8 (NOT deployed).
Batman-from-zip: only playable/index.html consumes the static GLB (port buildGLB ~200
lines, drop batman.glb); patch.json is consumed ONLY by playable/index.html.
**T2**: glide floats PROVEN from RefreshForcesGlide: sink = f0+(f1-f0)*(2/pi)*|pitch_rad|,
speed = f5+(f6-f5)*(2/pi)*|pitch_rad|+GetGliderGravityHelper(); f7/f8/f9 proximity blend;
f10 initial pitch deg (hard default -30). s_glide* .bss family RESOLVED DEAD (zero
readers AND writers; s54's "7-13 read sites" was a decoder artifact); k_glide* also
code-dead. Staged-slice gaps: fwd 16 u/s should be 1-6 (3.5 @ -45deg), sink missing the
(2/pi) factor — exact fix in s55_t2_note.md, NOT applied.
**T3**: CComponentGrapplingGun::Load = 5xReadInt+28xReadFloat; gun is UPGRADE-map-driven
(keys 3/4/5), no template payload; Glider int1 = GetGlide slot (byte-proof), int2 = 0
(corrects s54's 600). Enemy_Grapnel_Target 0xaae6a: script-spawned (0 lvc instances,
1 game_config ref); waypoint anchors stand.
**T4**: poolchunk peak 555.9 MB by 2s-sampling (PROVISIONAL <600; fine harness 691),
steady 205.6 MB, native residual ~261 MB swiftshader copies; first image <8s not met in
poolchunk. **T5**: real-GPU check PENDING; llvmpipe/Xvfb second renderer negative.
**T6**: combat survey done — minimal slice (Melee_Enemy_Merc + 4-8 clips + health) scoped
1.5-2 sessions; full combat/AI 4-6 unchanged.
Local refs after s55: main <T7-sha>, s55-t1-title-fix 0cea8b8, gh-pages-staged-s44 6145545,
s41 7b0807e. Bundles: download/bundles_s55/.

## SESSION 56 (round 46, 2026-10-24) — glide engine model APPLIED on branch + control; migration branch; memory floor; enemy templates decoded

**T1 glide on branch s56-t1-glide (77dd3c6+0280152, NOT deployed):** ?s5=1 now runs the s55-note
engine model (fwd = f5+(f6-f5)*(2/pi)*|p| = 3.5 u/s, sink = f0+(f1-f0)*(2/pi)*|p| = 10.0 u/s at
-45 deg; was const fwd 16 / sink 4+12|p|); ?s5old=1 keeps the old model as control; ?s5acc=1 runs
an ACCUMULATOR re-read; ?s5plunge=1 = slot-1 pitch0 -60. Gates: 6 configs ALL PASS 0 errors,
default digest = LIVE (00ce7970/137893, routes 10/10). Trajectories (s56_t1_traj_metrics.json +
plot): engine Glider/Plunge vz and fwd EXACT vs analytic (deterministic integration, n=46-55
frame samples); old control reproduces s55's -13.42 exactly; wrong-parameter and legacy controls
move every measure. **SEMANTIC CONFLICT (open, one signal each way):** a full re-read of
RefreshForcesGlide says the f0/f1 formula is the ACCELERATION rate of an airspeed accumulator
clamped [f0,f1] (pitch<=0 grows toward f1 @0x3839dc, pitch>0 decays toward f0 @0x383724), and
the f5/f6 family lands in the VERTICAL term (0x383858..0x383880: X,Y = -/+sin(f6 deg)*acc*cos(p),
cos(f6 deg)*acc*cos(p); Z = sin(p)*acc - (f5+(f6-f5)(2/pi)|p| + helper) - blend). f6=6 does dual
duty (fwdMax AND a 6-deg side-slip tilt); the f7/f8/f9 blend SUBTRACTS in Z near ground (landing
assist, not flare). Discriminating needs an engine-side trajectory capture or the StartGlide
acc-init (absent from the 4 entry functions). Float naming table complete (f2/f3/f12/f16/f17/f19
confirmed unread; int2=0; int1=slot).

**T2 control (?s5ctl=1, ba85416+cff36da):** scripted pitch control + auto-level on the engine
model. Validation EXACT: hold -60 deg -> vz -12.0 / fwd 4.333 / slip -6.0 deg (decoded mapping +
decoded f6 side-slip); zero input -> pitch = -60*exp(-k(t-t1)) with k-fit 2.0000 vs the placeholder
2.0 (n=26) and per-frame vz residual <= 0.005 u/s. PROVENANCE: the auto-level coefficient and any
pitch clamps are PLACEHOLDERS (s_glide* dead; f12/f16/f17/f19 unread; UpdateNavGlide pools = nav
steering 90/pi/180/0.001/360/-180 only) - the validation covers the CONTROL MECHANISM.

**T3 migration branch s56-t3-migrate (69696df+dddaa9e, NOT deployed):** based on the LIVE tree.
playable/index.html builds Batman IN-BROWSER from the user zip (buildGLB port; zip-built GLB
268,528 B, 7 clips, RGB888 texture; gate: WALKER ACTIVE, soup sha-verified, 0 errors);
patch.json + batman.glb + models/ (110.9 MB) + app.js + skybox.jpg REMOVED on the branch; root
index.html replaced by the zone-renderer prototype (integration_lazy copy at ./playable/ paths;
gate PASS with the LIVE-identical digest). Post-migration tree = 22 files, 708,208 B (-99.4%);
residual game-derived = 100,504 B (lvc_gol_templates.json + lvc_readseq_s30.json parse tables;
in-browser gol.bin decode is future work). Trigger markers retire with patch.json (no in-browser
CTriggerShapeAABB decoder yet). Rollback if ever deployed = redeploy 6145545.

**T4 memory (1a8e53a):** FINE harness (100 ms) x3 on the SAME config as s53/s55 (pristine 6145545
poolchunk page): peak RSS 611.3/547.1/592.1 MB (median 592, +/-5.4%), peak at t=5-7 s (build
transient), steady ~210 MB, first image 8.76-8.98 s, 0 errors. The s55 coarse 2 s number (555.9)
underestimated the spike ~6%. VERDICT: <600 MB AND <8 s NOT MET - floor ~590 MB / ~8.9 s on this
2-core swiftshader config; the lever remains dropping decode arrays after upload.

**T5:** real-GPU check still PENDING (paste-back page: integration_lazy.html?gpucheck=1); llvmpipe
not retried.

**T6 enemy data (2117b9c):** CComponentHealth = 0x0ddcd6c4 and CComponentAwareness = 0x6754056b
resolved with two anchors each (Load-fingerprint vs s30 readseq; vtable +0x18 = Load). Health::Load
= ReadFloat->[+4] (HP), ReadChar->bool, 2x ReadInt; Awareness::Load = 16 floats. Melee_Enemy_Merc
(0x000c351d, 683 B payload): health = 120.0, awareness16 = [11,17,0,0,2,5,0,0,1.5,6,0,0,1.1,160,2.7,1.5]
(FOV field only takes authored {45,120,160,180}). 37/50 carriers decoded: boss family (Bane,
LeadMerc, Turhan, Miranda) 1400 HP + 180 deg FOV; civilians 60 HP; vehicles health=2 with
sensor-only vectors; Melee family vectors identical across Merc/Pit/Test/PoliceMelee (structural
control). Shuffled-template null on health: z=-0.26, p~0.84 (unremarkable by design). Motion id
candidate 0x592ce07c NOT pinned (Load = tailcall to a shared reader @0x33a0d4). Damage numbers
(GiveDamage args in Lua bytecode) NOT decoded - PARTIAL.

**T7:** local main 2117b9c (11 ahead of remote a8e6124: 7 s55 + 3 s56 + delivery), branches
s56-t1-glide cff36da, s56-t3-migrate dddaa9e; bundles download/bundles_s56/ (verified SHA256 in
the session record). NOTHING deployed; remote unchanged.

### s56 remaining-work estimate update (sized)
- IN (unchanged): walkable world, character renderer + animation, Lua shim, browser asset pipeline,
  user-file material binding, descriptor decoding, engine shader + fog chain, zone renderer
  (corr 0.9923 standing), glide slice WITH the engine model + control on a branch, grapple slice.
- CHANGED: glide/grapple FULL behavior (stick dynamics, rope render, QTE, dive/roll variants):
  +0.5-1 session (the engine model + control mechanism now exist on the branch; remaining =
  engine-side capture to settle the f0/f1-vs-f5/f6 semantic, 0.25 session, + polish).
- NEW: user-zip migration (playable/index.html Batman-from-zip DONE on the branch; root prototype
  DONE; gol.bin in-browser decode for the 100 KB residual: 0.5-1 session; CTriggerShapeAABB
  in-browser decode: 0.5 session).
- NOT in (unchanged): combat/AI/mission flow 4-6 sessions (now with decoded Merc data: health 120,
  awareness16, FOV 160 - the data layer of the combat slice is ~30% surveyed); audio 1-2; UI 1-2;
  cloth cape 1; cross-region navigation 1-2; city-scale lit rendering from user files 1-2.
- Combat slice remaining specifics: GiveDamage argument decode (0.25-0.5), Motion component reader
  (0.25), enemy skeleton clip bindings (bdae anim_pack gap, standing), then implementation 1-1.5.
## SESSION 57 (round 47, 2026-10-24) — glide model DECIDED (accumulator); enemy templates double-signal; enemy viewer; gol JS parity; memory floor restated

**T1 glide DECIDED (branch s56-t1-glide af90aff, NOT deployed):** the s56 accumulator re-read IS the
engine model; the s55 note had the f0/f1 and f5/f6 families swapped. Byte evidence: RefreshForcesGlide
0x3836b0 integrates [actor+0x53c] with rate f0+(f1-f0)(2/pi)|p| (grow p<=0 @0x3839dc guarded acc<f1,
decay p>0 @0x383724 guarded acc>f0, x dt=[actor+0x2a8]); output velocity 0x383858..80: X/Y = ∓/+
sin/cos(f6deg)*acc*cos(p)*dt (6-deg side-slip), Z = (sin(p)*acc - (f5+(f6-f5)(2/pi)|p| +
GetGliderGravityHelper()) - blend)*dt — the f5/f6 formula is VERTICAL-only (helper into forward speed
byte-refuted @0x383784). acc census (computed-base scan; 0x53c is beyond the vldr 1020 range so all
accesses decompose add #0x530 +0xc): StartGlide 0x3806a8 acc=f1=16 (INIT = clamp-hi),
StartGlideFromGrapnel 0x380b80/0x380c48 acc=f1=16, UpdateNavGlide 0x381bc0 acc=|v @[actor+0x224]|
(momentum seed); readers RefreshForcesGlide 0x38379c + UpdateNavGlide 0x381c5c; NO others.
SetGlideSpeed @0x38a120 (Lua SetActorSpeedGlide) writes [actor+0x3b8] = a SEPARATE scripted-speed
field (ctor/ReInit write; SaveSave/SlideOnCollisions read) — not the accumulator. Plausibility: acc
model glides FASTER than a run with distinct Glider/Plunge angles (52.8/66.4 deg); the s55 model gives
a constant 3.5 u/s (slower than a run) and no role for the accumulator. ?s5=1 default = accumulator
(seed f1=16); ?s5sink=1 = s55-note control; ?s5acc=1 alias. Gates 5/5 PASS 0 errs, soup
00ce7970e45adc85/137893 = LIVE on every config, routes 10/10; fwd EXACT 11.314/8.0/3.5 (Glider/
Plunge/sink-control); vz within 1.14 u/s of sin(p)acc-s56-blend (declared blend-proxy residual);
ctl on acc: head -6.0 deg EXACT, fwd = 16 cos(pitch) sample-exact.

**T2 enemy templates SECOND SIGNAL (63db87c):** component Load sequences derived from the engine
(ARM): CStateSet instance Load = 4-B no-op thunk (0x298f38) but TEMPLATE path = 8 STR state-name
list (Merc: ''-ref,'Idle','Hurt','Death','Idle','Walk','Run','Run'); DropCollectible i+n*(i,i);
NpcAI 38 B; WantedGenerator 16 B; ActorBase template Load = 3B+16f+3B+2i+n*(i+1B) = 78+5n; Motion
template = [c,f,f,c,f,f] = 18 B speed pairs (uniform 750.0/750.0/500.0/500.0, flag 1, across Batman
+ all enemies; instance path = CMemoryStream::ReadString 0x33a0d4 PINNED). Structural walk (no
sanity filter) closes 110/653 templates exactly; Health/Awareness boundaries: 25 carriers MATCH s56
gap-search values (Merc Health@121/Awareness@154 exact), Blake CORRECTED 2.0->150.0 (walk wins,
25:1), 4 NEW decodes (Helicopter, Helicopter_Bane, Military_Heli, Test_Object @121/@138); missing
sequences LISTED (CustomizeActor template variant = [count][count STR] groups; 0x2db081e2 vehicles;
Sniper blocker). s30 read-seq table = LVC-instance path, not valid for gol walks. GiveDamage Lua
arg constants NOT decoded (standing).

**T3 enemy viewer (branch s56-t1-glide, enemy_viewer.html, NOT deployed):** Melee_Enemy_Merc data
in-scene — awareness cone FOV 160 deg (near 11/far 17 u), 120-deg wrong-FOV control cone, health
120 HP, scripted hit -10 (damage = LABELED PLACEHOLDER; GiveDamage args still open), state-table
combat states + clip families; enemy skeleton clip bindings remain the standing bdae anim_pack gap
(no enemy clip playback). Load-tested 0 errors; gate pass (aperture 160 vs 120, radii delta 6,
health 120->110).

**T5 gol.bin JS parity (branch s56-t3-migrate, playable/gol_parse.js):** dependency-free in-browser
parser (header, offsets, string table, template table, per-comp walks with the s57 sequences);
NODE == PYTHON digest on all 653 templates (sha256 5edaa1485e6ca6ab..., closed=77 both; rep-bearing
specs unresolved both sides). Retires part of the 100 KB parse-table residual.

**T4 memory:** streaming rework NOT attempted (time went to T1/T2); floor by phase restated with
harness attribution (s57_t4_note.md): empty 84.9 MB (s53 fine), +textures 23.5, build peak median
592 MB @t=5-7 s (s56 FINE x3; 2 s sampling underestimates ~6%), steady ~210, native residual ~261
swiftshader copies, first image 8.76-8.98 s. <500 MB / <8 s NOT MET — floor ~590 MB / ~8.9 s.

**T6:** real-GPU check PENDING (no block pasted; load integration_lazy.html?gpucheck=1 on a real
GPU and paste; a GPU run does not answer the glide question — T1 settled it from code).

**T7:** local main 2 commits ahead of the s56 state (63db87c T2 + T5 receipts), branches
s56-t1-glide af90aff (+T3 enemy viewer commit), s56-t3-migrate (T5 gol_parse.js), s55-t1-title-fix
0cea8b8. Bundles download/bundles_s57/ verified (SHA256 in the session record). NOTHING deployed;
remote unchanged. Working-tree regression found at session start (CLAUDE_HANDOFF.md missing the s56
section + 41 mode-only flips) — restored from HEAD before work.

### s57 remaining-work estimate update (sized)
- IN (unchanged): walkable world, character renderer + animation, Lua shim, browser asset pipeline,
  user-file material binding, descriptor decoding, engine shader + fog chain, zone renderer
  (corr 0.9923 standing), glide slice NOW WITH THE DECIDED ENGINE MODEL + control, grapple slice,
  gol.bin in-browser parse (NEW, done this session on the migration branch).
- CHANGED: glide/grapple FULL behavior +0.25-0.5 session (the semantic conflict is SETTLED; remaining
  = stick-dynamics polish + rope render + QTE, no more model ambiguity).
- NEW sizes: combat slice data layer ~60% done (Health/Awareness double-signal, Motion speeds,
  state/clip families; remaining: GiveDamage Lua arg decode 0.25-0.5, CustomizeActor template
  variant 0.25-0.5, enemy skeleton clip bindings (bdae anim_pack gap, standing), then implementation
  1-1.5 sessions). Enemy viewer exists as the data-visualization base.
- NOT in (unchanged): AI/mission flow 4-6 sessions total with combat; audio 1-2; UI 1-2; cloth cape 1;
  cross-region navigation 1-2; city-scale lit rendering from user files 1-2.
- Memory: streaming rework 0.5-1 session to attempt <500 MB; browser floor + swiftshader copies are
  not in-page addressable (real GPU is the only path below ~350 MB native).

## SESSION 58 (round 48, 2026-10-25) — glide blend distance PINNED (takeoff anchor); template walk 110->326/653; enemy rig found + clips FK-validated; gol-from-user-zip gate live on migration branch

**STATE at start:** remote unchanged (main a8e6124, gh-pages 6145545 LIVE); CLAUDE_HANDOFF.md complete (946 lines, s56+s57 present, NO mode flips); bundles_s57 hashes verified; NO GitHub token files on disk (filename-only scan; only s28 lexical-token scripts) — NOTHING pushed this session (no token supplied).

**T1 glide blend PINNED (branch s56-t1-glide 1abd8e2, main 2614884):** the 0x383788 virtual call is
[comp+4]->vtable[+0x18] where comp+4 = owner CGameObject (ctor 0x36bfc0 str r1,[r0,#4]); CGameObject
vtable base 0xbd8028, slot 6 = **CGameObject::GetPosition @0x2d6f1c** ('add r0,r0,#0xc' = &obj->pos
at +0xc..0x14). **NOT a ground raycast / nav height / collision query.** Distance =
|GetPosition(obj) − [comp+0x1a4..0x1ac]| where that vec3 cache is stored right after EVERY
CActorBaseComponent::SetActorPosition (Update 0x36e74c, UpdateNavSimpleBehavior/NormalSimplified/
TransitionWithMovement/ClimbBox, TryEdgeGrab, UpdateFloorTesting, ResolveAirCollision) and NEVER by
UpdateNavGlide (0x380e94..0x3813bc: 0 stores; single RefreshForcesGlide call @0x380fbc) => during a
glide the cache is frozen at the TAKEOFF position: **d = 3D distance travelled since glide start**.
Blend arithmetic: blend_raw = fB + (1−d/f9)(f7−fB) [fB=[gadget+0x24] floor, f7=[+0x28] start,
f9=[+0x2c] range]; blend = **max(blend_raw, fB)** (0x3837d4 vmla, 0x3837ec vcmpe, 0x383804 vmovge);
vz −= blend (0x383814). With the decoded floats (0/2/16) = a 2 u/s extra-sink entry dip decaying
linearly over the first 16 u of travel. GetGliderGravityHelper 0x1e1508 = UpgradesManager
std::map[0x1f].SUpgrade+0xc (SUpgrade {u16 key, s16 level=−1, base@+8, value@+0xc}; AddUpgrade
sets base=value; Upgrade mode 0 add / mode 1 multiply / mode 2 keyed switch; base value is
DATA-DRIVEN from the ResetUpgrades definition tables — number inconclusive from .text; in-page 0
stands). Page: proxy (height-over-nm) kept as the ?s5=1 default for digest stability; **?s5blend=1**
= exact engine measure. Gates 6/6 PASS 0 errs, soup 00ce7970/137893 = LIVE everywhere, routes 10/10,
land receipts reproduce s57 (417/467/917/450); exact-vs-analytic vz error **0.0048 (Glider n=24) /
0.0049 (Plunge n=28) u/s** (well under 0.1); proxy-vs-exact control MOVES 0.93 u/s at t=50 ms;
sink control fwd 3.5 reproduced.

**T2 templates 110 -> 326/653 close (49.9%); carriers 30/50 (main):** three Loads decoded: (1)
CCollisionComponent::Load 0x2230a8 — instance shape = base CComponentCollision::Load (0x2d72bc:
c,c,STR,i,c,c,i = 16 B) + ReadChar cnt + cnt*(STR+i+9f+c); **TEMPLATE payload = the 16-B base
ONLY** (instance shape REFUTED for templates by closure: 0651bdaa@125=[2.0,1.8,1.6] and
Health@137=2.0 align across 15 vehicle carriers simultaneously); (2) **0x33702f4a =
CComponentSniper::Load 0x2e4b5c = 5f = 20 B** (unlocks the 9 Batarang*/Assault_Rifle_01 weapon
templates); (3) CComponentCustomizeActor::Load 0x3bf688 (wrapper 0x396db4) = **i(n) +
n*(STR,STR,STR,i(m),m*STR) + i + i** — exact walk, no candidate search. Walk re-run (no sanity
filter): 326/653 close; carriers 30/50 with values: **21 MATCH s56** (health + 16 aware floats +
ints), **9 CORRECTIONS** (Blake 150 re-confirmed; 8 vehicles = health **300** not s56's 2.0, ints
−1/−1 not 16320/16448 — s56's vehicle boundary pre-dated the collision fix; aware [5,15,...]).
Remaining blockers listed per template (top: LEN-MISMATCH 111, 0x4cc04ddb 59, 0x43c8a8d1 24,
0x67c82e62 14 vehicle-extra, 0x0e1f5b6f Sniper/Ranged_Disarm pair; heli/monorail/Test_Object big
rep residuals). **Motion shapes explained:** template [c,f,f,c,f,f] speed pairs are the operative
data (generic template loader); the instance string reader (CMotionComponent::Load 0x2395f8 ->
CComponentMotion::Load 0x2d79ec -> ReadString) is DORMANT on the placement path — lvc census over
11/12 files (Test.lvc OOM at 6.5 GB heap): **ZERO Motion instances**; s57's "string names a motion
set with these speeds" refuted for placement data. **GiveDamage(actorId, damage) @0x155e4c:**
arg2 = literal lua_tointeger -> float; 8-word info struct {damage, 0, −1 (source), 0×5} dispatched
via [obj vtable+0xa8] (slot 42), id 0 = level dispatcher path. Census over game_config.gla: **146
call sites, ALL literal, 12 distinct values: 5 x91, 7 x11, 10 x9, 500 x8, 1000 x7, 50 x6, 25 x5,
15 x3, 300/20 x2, 30/5000 x1** (the 541-script lvc trigger corpus carries 18, all GiveDamage(0,5)).

**T3 enemy rig FOUND, clips FK-validated; in-page mesh = PARTIAL (branch c6aeb9b):**
Bane_mercenary.bdae (1,229,264 B) + Bane_mercenary_low.bdae (750,064 B) exist in the user zip's
actors.gla; textures chara_banemercenarya_c/_n/_mask.tga + gear_mercenaryA..D_LOD00..03 (from the
exact CustomizeActor walk — template and container agree). Animation file = the SHARED bank
batman_anims.bdae (921 clips): Merc state table Idle/Walk/Run -> **_014_idle_enemy_combat /
_166_enemy_walk / _171_enemy_run** (aim/hip variants _167/_172/_173). FK battery (the s35/s36
Batman machinery, unchanged) on the enemy clips: loop continuity 0.252-0.908 u (batman walk/run
calibration 0.191-0.575; enemy idle 0.43/0.25), foot band −0.87 u (grounded), walk/run root bob
0.865-0.966 (±5 cm), rolled wrong-case breaks the step profile. ?enemy=1 wired through the Batman
GLB path with __GATE.enemy/enemyPlay receipts — **fails cleanly: readBdae's SKIN_OFFS layout is
batman-hardcoded** (the earlier "1449-vert shared topology" reading was that artifact); merc bdae
section-table derivation = one focused session (the ONLY remaining step to in-page enemy playback).
enemy_viewer.html damage 10 -> decoded **5** with GiveDamage provenance. Gates: default digest
unchanged; ?enemy=1 pass with recorded blocker; 0 errs.

**T4 memory (lever attempted, target NOT MET):** ?texfree=1 (drop decoded texture CPU bytes right
after GL upload, behind flag, digests identical 00ce7970/137893 on all runs) — peak does NOT move:
median ~560 MB across 4 fine runs (538.7/568.2/593.9/551.8) vs s56's 592 (same ballpark, ±5% run
noise); first image 8.5-8.9 s. Spike = zone-build transient: swiftshader native copies (~261 MB,
s55 breakdown) + soup/batch intermediates; textures were already LRU-capped (64 MB). Floor: empty
three.js 93 MB (s58), steady ~210 MB. <500 MB / <8 s NOT MET — the remaining JS lever (batch-build
intermediates refactor) is digest-risky; real GPU is the path below ~350 MB native.

**T5 gol-from-user-zip gate LIVE (branch s56-t3-migrate 47e73d1a):** the migration root prototype
now slices game_config.gla member **gol.bin (1,270,660 B) from the USER'S zip** and parses it
in-browser (gol_parse.js). Gate __GATE.golzip = {ok:true, nrec:653, closed:77, digest 5edaa148...
MATCH, **triggers:2 (BoxTrigger, CylinderTrigger), carriers:50, Merc health=120 aware=11/17
fov=160** decoded at the walk-proven payload offsets}; soup 00ce7970/137893 unchanged; 0 errors.
Also noted for a later session: game_config.gla carries **Upgrades.bin (721 B)** — the likely
T1-helper base-value source.

**T6:** real-GPU check PENDING (no block pasted; load integration_lazy.html?gpucheck=1 on a real
GPU and paste the block).

**T7:** bundles download/bundles_s58/ verified — main_s58_inc.bundle (requires a8e6124 = remote
main), branch_glide_s58_inc.bundle (requires 6903059 = the s57 glide bundle), branch_migrate_s58_inc.bundle
(requires fb7a6b5 = the s57 migrate bundle); SHA256 in the session record. NOTHING deployed; remote
unchanged. State at handoff: local main ahead 21+ commits (through the s58 receipts + handoff);
branches s56-t1-glide 22b77bc9, s56-t3-migrate 47e73d1a, s55-t1-title-fix 0cea8b8.

### s58 remaining-work estimate update (sized)
- IN (unchanged): walkable world, character renderer + animation, Lua shim, browser asset pipeline,
  user-file material binding, descriptor decoding, engine shader + fog chain, zone renderer, glide
  slice NOW WITH THE EXACT BLEND (anchor-distance measure implemented; helper number pending
  Upgrades.bin), grapple slice, gol.bin in-browser parse + user-zip trigger/enemy templates (NEW).
- CHANGED: combat data slice ~70% (walk coverage 326/653 with collision/customize/sniper specs;
  carriers 30/50 with corrections; GiveDamage decoded + censused; enemy rig located; enemy clips
  validated). Remaining: merc bdae section-table derivation 0.25-0.5 session -> in-page enemy
  playback; remaining comp Loads for the other 327 templates (~0.5-1 session per cluster:
  0x4cc04ddb/0x43c8a8d1 props cluster, 0x67c82e62 vehicle-extra, 0x0e1f5b6f sniper pair, big-rep
  behavior templates); Upgrades.bin decode 0.25 session (T1 helper number); combat implementation
  1-1.5 sessions (unchanged).
- NOT in (unchanged): AI/mission flow 4-6 sessions total with combat; audio 1-2; UI 1-2; cloth cape 1;
  cross-region navigation 1-2; city-scale lit rendering from user files 1-2. Memory: the JS levers
  are exhausted (T4); <500 MB needs a real GPU (or accept the ~560 MB floor).
## SESSION 59 (round 49, 2026-10-25) — glide blend cache writer/state analysis COMPLETE (frozen anchor DECIDED + collision re-anchor refinement); merc rig IN-PAGE (generalized bdae reader, batman digests EQUAL, ?enemy=1 gate PASS); template dispatcher VERIFIED (GOM::Reload -> GenerateComponentTemplate -> [vptr+0x10]); combat behaviour slice gate PASS; helper = 0.0 code-verified

**STATE at start:** remote unchanged (main a8e6124, gh-pages 6145545 LIVE, staged 39298a4, staged-s44 6145545, s41 7b0807e, s40 80274a1, essentials 7c8defc); local main ff94ca0 (21 ahead), s56-t1-glide 22b77bc, s56-t3-migrate 47e73d1, s55-t1-title-fix 0cea8b8 — all as expected. CLAUDE_HANDOFF.md 1051 lines complete. NO token supplied -> NOTHING pushed. No real-GPU block supplied -> T5 = environment-dominated.

**T1 glide blend cache — writer/state analysis COMPLETE (two signals, DECIDED):**
(1) UpdateNavGlide 0x380e94 has EXACTLY ONE caller: Update.part.2842 0x3a2c58 (the GLIDE case of
the nav-mode jump table @0x3a33e0). RefreshForcesGlide 0x3836b0 called ONLY from UpdateNavGlide
@0x380fbc. (2) Update 0x36e394: r5 = UpdateSpeed(dt) return; r5!=0 -> early return (no nav, no
write). r5==0 -> byteB=[[comp+0x60]+0xa] (CComponentActorBaseComponent bool, template payload
byte 6): byteB!=0 -> forces path (SetActorPosition + THE cache write 0x36e74c, velocity-predicted
= GetActorPosition + [comp+0x224] from RefreshForces) and NO nav dispatch; byteB==0 -> part.2842
nav dispatch (incl. glide), NO cache write. MUTUALLY EXCLUSIVE per frame. (3) Writer census
(CActorBaseComponent): ctor/ReInit (zero), Update (exclusive branch), TryEdgeGrab, UpdateNav-
SimpleBehavior, UpdateNavNormalSimplified x4, UpdateNavNormal, UpdateFloorTesting,
UpdateFloorProjection (strne), UpdateNavGhost (strne), ResolveAirCollision x2. Glide call-cone
closure: GCT-glide case calls ONLY UpdateNavGlide; its 12 calls touch NO writer; SetActorPosition
itself writes nothing; RefreshForcesGlide's 10 calls touch none. **=> free-flight glide: cache
frozen at takeoff (s58 holds). NEW REFINEMENT: UpdateNavGlide @0x382ec0 CheckForContacts ->
ResolveAirCollision 0x398570 on contact STORES the resolved position into the cache
(0x3987a4/0x3987d4) -> the blend anchor RE-ANCHORS at every air collision (entry dip restarts);
code-proven, not page-exercisable (open-sky slice).** Signal 2 (measured, ?s5blend=1 battery
n=25/28): frozen model closed form 5e-4; per-frame-displacement wrong model errs 0.525 (Glider)/
1.082 (Plunge) u/s = 100-200x the residual -> data arbitrates for frozen. Gates 6/6 PASS,
digest 00ce7970=LIVE, land 417/417/467/917/450 (=s57/s58), 0 errs.
**Upgrades.bin (721 B) decoded: SHOP/LOCALE metadata (u32be 11 + 1 + 9xu16 keys 2..10; records
{u16 key, u16 5, 4 len-prefixed strings, 25-B tail: prices LE 80/90/180/50/..., 'EOF'}) — NO
engine floats, NO key 0x1f. GetGliderGravityHelper = map[0x1f].value; map inserted ONLY by
AddUpgrade (ZERO code refs in the loaded image — symtab artifacts only), ResetUpgrades
(function-pointer registry @0xc366f8 = shop reset UI), LoadUpgradesStatus (save file ->
CInventory::SaveLoadGlobal), or operator[] default {0,0,0,0}. => HELPER BASE LEVEL 0 = 0.0
(code-verified; s58 'inconclusive' resolved; page helper 0 stands, no patch).**

**T2 merc rig IN-PAGE (the s58 blocker closed):** BRES bdae container is self-describing:
header n_relocs@0x10, offsets@0x18 (reloc table 0x3c..pool0; pool0/pool1/off3/off4; data
section > off4 relocation-free). **readBdae2 added to tdkr_pipeline.js** (generalized, no
per-file constants): validated 0x50 node scan (4-B stepping) -> stride run at off4 -> INVB run
(64-B mats, row3 (0,0,0,1), >=10, BACKWARD-extended) -> palette (8-B 'Bone' entries after
INVB) -> skin-record run (stride/weights {(20,4),(16,3),...}, run>=200 gives NV) -> verts
(descriptor-bbox-validated full-run scan; uv at stride-8/-4 /4096) -> u16 index run.
**VALIDATION: readBdae2(batman.bdae) digests == readBdae(batman.bdae)** (verts bf4cd6849d3834ed,
idx 968b43d5b220f980/5431, skinJ d1d89fa17550f19b, 31 joints). Merc layout derived: NV=**1294**
(s58's 1449 = batman layout misread), stride 52, INVB 0x74080 x31, palette 0x748d8 x31, skinrec
0x749d0 **16-B/3-influence** maxJoint 30 (=31 bones), VERTS 0x53c4, IDX 0x15b16/6007 — python ==
JS identical. Merc skeleton INDEPENDENTLY validated: |bind origin - skin-weighted centroid|
median **0.075 u** (batman calibration 0.089; permuted-mapping null 0.64-0.90 ~9x). Clip-channel
overlap 37/72; ALL 35 missing = Batman cape CBones (enemy clips locomotion-complete). Enemy-clip
FK on MERC rest locals: walk loops 0.346/0.065, run 0.461/0.264, pelvis z 0.87-0.96 (matches
s58's batman-skeleton numbers — pelvis translation is clip-carried; leg rest offsets identical
0.106/0.4098/0.45); rolled-25 control breaks the profile. **?enemy=1 GATE PASS: 0 errs,
enemy.ok {1294 verts, 31 joints, 3 clips}, enemyPlay {wraps 2, phasesSeen 3, dispIdle 1.330 <
dispWalk 1.753 < dispRun 1.926 (CPU-skin probe, 150 verts), wrong-clip control 1.769},
soup 00ce7970 = LIVE unchanged, routes 10/10.** Page changes on branch s56-t1-glide b1f5dfb:
buildGLB clip-list param + invB count generalized; finalizeGate defers done in enemy mode;
mercTick hoisted to walk phase; updateMatrixWorld in the control loop.

**T3 template closure — mechanism VERIFIED, classes NAMED; walker rebuild FAILED (PARTIAL):**
GenerateComponentTemplate 0x368ac0 (11308 B) called from GOM::Load/Reload/CreateObject (the
gol Reload path). Per case: `new <class>` + common tail @0x368bfc `ldr r3,[r3,#0x10]; blx r3`
= **[vptr+0x10] = the per-class TEMPLATE reader** (different slot than the instance Load).
For 0x2db081e2: [vptr+0x10] == CCollisionComponent::Load 0x2230a8 -> s58's 16-B base template
shape CONSISTENT with the dispatcher. CComponentAwareness::Load = 16 ReadFloat -> +4..+0x40;
**field 13 engine-NAMED = VisibilityAngle degrees** (ResetVisibilityAngle 0x39638c -> [comp+0x24],
GetVisibilityAngle, cos table +0x28) = the FOV 160. Blocker classes: 0x4cc04ddb=CBeastOmni
(GCT case), 0x43c8a8d1=unnamed 0x14-B (GCT case), **0x67c82e62=CVehicleCollisionComponent
(NO GCT case — the engine's own template path cannot construct it; ids appear NOWHERE as
literals/movw pairs)**, 0x0e1f5b6f=CSniperComponent (NO GCT case), 0x0116a6fa=trail (NO case),
0x4cc07242=CBeastSpot, 0x28091330=CCollectible, 0x7d561d33/0x0dd583de (GCT cases). Walker
rebuild (s30 table + 11 documented overrides) closed only 5/653 — the s57 script was lost with
its workspace; ~40 legacy-id template specs (0x14ca79 445, 0x152b87 26) unrecoverable from
receipts in-budget. **Closure stands at s58's 326/653 (49.9%), carriers 30/50 (60%).** Vehicle
health 300 second signal PARTIAL: engine-verified Awareness field map + named FOV consumer;
Lua SetActorHealth constant-pool decode remains open.

**T4 combat behaviour slice (enemy_viewer.html, branch-only) GATE PASS 0 errs:** state machine
(StateSet names Idle/Walk/Hurt/Death); cone test = dist<=17 AND |angle-facing|<=80 deg
(engine-named FOV); alert Idle->Walk on player-in-cone; hits 5/10 HP (census values) -> Hurt
(0.4 s) -> Walk; Death at 0 HP. NEGATIVE CONTROL x2: 60 u away -> Idle AND 15 u BEHIND the
facing (inside R_FAR, outside the cone) -> Idle (the transition discriminates ANGLE). Sequence
Idle,(Hurt,Walk)x12,Death; hp 120->115->105->0; screenshot receipts.

**T5 memory: environment-dominated** (no real-GPU gpucheck block supplied; standing floor
~560-592 MB / 8.5-9.0 s restated; the ?gpucheck=1 page remains ready for paste-back).

**T6 refs/bundles:** commits this session on main: T1 (s59 receipts), 610b86c (T2 receipts),
58d5fce (T3), bfc2eba+cf02f36 (T4), ff66a91 (T5), handoff (this section); on s56-t1-glide:
b1f5dfb (in-page merc playback). Bundles download/bundles_s59 (verified, SHA256 in the session
record). NOTHING deployed; remote unchanged.

### s59 remaining-work estimate update (sized)
- IN (unchanged): walkable world, character renderer + animation, Lua shim, browser asset
  pipeline, user-file material binding, descriptor decoding, engine shader + fog chain, zone
  renderer, glide slice NOW WITH the writer/state proof + re-anchor note, grapple slice,
  gol in-browser parse, **enemy rig IN-PAGE (NEW: readBdae2 generalized reader + merc playback
  gate PASS)**, **combat behaviour slice (NEW: alert/hurt/death machine on decoded data)**.
- CHANGED: combat data slice ~85% (mechanism + class table + FOV named; remaining: the ~40
  legacy-id template specs for the walker (0.5-1 session, needs re-derivation from engine
  disasm), per-class template Loads for the 5 GCT-case blockers (0.5 session), Lua
  SetActorHealth constant-pool decode (0.5 session), Hurt/Death clips wired into the in-page
  merc path (0.25 session)).
- NOT in (unchanged): AI/mission flow 4-6; audio 1-2; UI 1-2; cloth cape 1; cross-region nav
  1-2; city-scale lit rendering 1-2. Memory: environment-dominated until a real-GPU block.

## SESSION 60 (round 50, 2026-10-25) — template walker REBUILT FROM THE ENGINE (64 GCT cases; engine-true 144/149 pure; hybrid 524/653); vehicle health 300 signal-1-pinned; merc discriminating validation + IoU 0.9516; combat slice runs the REAL merc; glide re-anchor page-verified

**STATE at start:** remote unchanged (main a8e6124, gh-pages 6145545 LIVE, staged 39298a4, staged-s44 6145545, s41 7b0807e, s40 80274a1, essentials 7c8defc); local main 3dea1e3 (28 ahead), s56-t1-glide b1f5dfb, s56-t3-migrate 47e73d1, s55-t1-title-fix 0cea8b8. CLAUDE_HANDOFF.md 1152 lines complete. NO token supplied -> NOTHING pushed. No real-GPU block -> T6 = environment-dominated.

**T1 template walker — REBUILT FROM THE ENGINE, calibration PASSED (751b5c7):**
- GenerateComponentTemplate 0x368ac0 = pure if-chain, **64 cases** (s59 said 63 - the
  prologue case 0x365cfd67 compares before push; extractor window bug). Every case:
  `movw/movt id; cmp r0,r3; beq CASE` -> `bl _Znwj; ldr r3,[pc,..]; add r3,pc,r3;
  add r3,r3,#8; str r3,[r0]; b 0x368bfc` -> tail `ldr r3,[r4]; ldr r3,[r3,#0x10]; blx r3`
  = **template reader = [vptr+0x10]** (vptr = vtable+8).
- **DEFAULT PATH = `mov r4,#0; ldr r3,[r4]` @0x368bf4 = null-deref CRASH** (all 15 bne
  defaults converge). GOM::Load/Reload call GCT for EVERY comp (no flag check, no skip);
  CreateObject's `beq -> skip` null-check is unreachable (GCT cannot legally return null).
  => **classes outside the 64 are engine-unloadable in templates**; records are
  offset-table framed so unread tails are never consumed by GCT.
- s59 corrections: 0x14ca79 = CComponentBase::Load 0x1fe924 = c,i,f*9,c,c,c (44 B, 446 uses)
  and 0x152b87 = CComponentMesh::Load 0x2d6ddc = STR,c,c,c,c (8 B, 441 uses) - the two top
  "unrecoverable legacy" blockers HAVE cases; 0x0116a6fa HAS a case (CComponentTrail);
  0x33702f4a -> CComponentDummies::Load (not Sniper). NO case (constants appear nowhere in
  .text/data): Awareness 0x6754056b, StateSet 0x5441a117, Motion 0x592ce07c, CustomizeActor
  0x40c6b80a, DropCollectible 0x3ef5108d, CVehicleCollision 0x67c82e62, CBeastSpot,
  CCollectible, Sniper 0x0e1f5b6f.
- ActorBase CORRECTED from disasm: **7c + 16f + 3c + i + i + n*(i+c) = 82+5n, loop count =
  the SECOND int** (s58 said 78+5n, count = first int). Hand-verified readers:
  MainStoryQuests = i(n) + n*(i,i,4STR,i,STR,c); NewShopItemProperty = s30 spec CONFIRMED.
- Walk: **ENGINE-TRUE 149/653 templates are pure-case; 144/149 bounds-closed (96.6%),
  139/149 exact**, 5 NA (empty comps), 5 legit tails (4,4,4,15,21 B). Blockers on pure = 0.
- **HYBRID (engine 64 + s30 lvc-instance specs + s58 overrides + 1 labelled gol-shape
  correction): 524/653 bounds-closed (80.2%), 393 exact**, carriers 33 bounded; **18/18
  s58-comparable carrier values EXACT** (health + 16 aware floats); two position classes:
  NPC carriers (health@121, aware@138) x14, VEHICLE carriers (health@137, aware@154) x19.
- Gol-shape correction (labelled data-derived): 0x59a8390c = 16 B in gol vs s30 12 B
  (159 tail-4 records; exact 234->393) - consistent with the template/instance reader
  duality; engine cannot verify (no GCT case).
- s58 blocker ledger: Base 445->0, Mesh 441->0, Beast_Omni 59->0, Objective 24->0,
  365cfd67 156->0, 0e31d4a0 10->0, Gadget 9->0, LEN-MISMATCH 111->131 small-tails;
  UNRESOLVED same-cause: Trail 20 (spec incomplete), 7d561d33 18, CVehicleCollision 14,
  CustomizeActor 12 (CUST OOB), CBeastSpot 11, CCollectible 10.
- Nulls (documented): spec-permutation 118/149 vs real 144 (weak - fixed-size collisions);
  payload rot-7 142/149 (length-only closure for all-fixed specs). Strongest basis =
  engine derivation + 18/18 value agreement.

**T2 vehicle health (c0d5783):** Signal 1 (engine): 19 vehicle carriers read Health via the
ENGINE reader (f,c,i,i) at aligned offset 137 -> **300.0** (records close to bounds);
Signal 2 (Lua): SetActorHealth x26 / GetActorHealth x12 / GetActorPercentHealth x4, ALL
actor-generic (gol scripts embed 1,916 Lua bodies; zero vehicle-word+Health co-refs);
GiveDamage 146 sites context-decoded: 500 x8 = player hazards, 1000 = window destruction,
5000 = scripted player kill, 300 = scripted events - NONE target vehicles (the 300-damage
literal is a coincidence, NOT evidence). Verdict: mechanism agrees (one generic health
system); the VALUE is pinned by signal 1 only. Open: consumer-named roles for awareness
fields 0..12; GetActorMaxHealth C++ export untraced.

**T3 merc rig validation (ce4e200 branch + 3445fa3 receipts):** Python readBdae2 port;
weights sum EXACTLY 1.0 (1449/1294 verts, 100% in window) vs shuffled null 8.0/19.8%
(sd 0.72-0.74), bad-case 0%; max joint 30 < 31 (100%); heights 1.9164/1.8713; V4
|world bind - centroid| batman 0.0888 / merc 0.0750 (n=31 each) vs permuted nulls
0.59-0.91 (reproduces s59; bind origin = NODE-hierarchy world transforms, not the invB
translation row). Hurt/Death clips wired (_223_enemy_hurtl 1.666 s, _250_enemy_death1
1.2 s, LoopOnce) - dispHurt 7.14 / dispDeath 12.91, one-shots DONE. **IoU gate PASS:
page render vs numpy merc reference 0.9516** (batman cross-null 0.6922, x-flipped 0.6772),
height 1.8713, feetZ -0.0012 (raw WebGL1 + readPixels; rest-pose uses static bind
geometry - three r160 applyBoneTransform is dead before first render; skinning validated
by the 5-clip displacement battery). Default soup 00ce7970/137893 unchanged.

**T4 combat slice runs the REAL merc (fe33520):** enemy_viewer.html loads the merc +
anims from the USER ZIP (lazy gla slices); FK-skinned point cloud (node hierarchy,
nearest-key rotation channels, root pos channel, file invB pairing; CH names carry
'-node'); machine = s59 + **Run** (alerted && dist > 14). **Gate PASS 0 errors:**
far/behind controls -> Idle; Walk/Run/Walk discriminate distance; hp 120 -5=115 Hurt ->
Walk -10=105 Hurt -> 0 Death; wrong-clip control diff 0.2211 u/vertex; screenshot receipt.

**T5 glide re-anchor (cf74c5b):** ?s5reanchor=1&s5wall=N: wall crossing clamps the
horizontal step and resets the anchor to the resolved position (engine 0x398570 ->
[comp+0x1a4]). Gate PASS: wall @267 ms, **blend dip restarts (+0.32 jump)**, trajectory
vs piecewise analytic max err **0.0047 u/s** (n=25); no-wall control reanchors=[];
flag-gated; default soup re-verified post-patch (s60_default_gate.json). Helper level-0
= 0.0 stands ("no evidence of a nonzero value"; labelled constant). Operational: the
waypoint decode is gated on ?s5=1 - use ?s5=1&s5blend=1 for the blend runs.

**T6 memory: environment-dominated** (no real-GPU block; standing floor ~560-592 MB /
8.5-9 s; ?gpucheck=1 ready for paste-back).

### s60 remaining-work estimate update (sized)
- IN (unchanged): walkable world, character renderer + animation, Lua shim, browser asset
  pipeline, user-file material binding, descriptor decoding, engine shader + fog chain,
  zone renderer, glide slice (NOW with page-verified re-anchor), grapple slice, gol
  in-browser parse, enemy rig IN-PAGE (generalized reader + Hurt/Death + IoU-validated
  mesh), combat behaviour slice (NOW with the real merc in-scene).
- CHANGED: combat data slice ~92% (walker engine-true; remaining: Trail/MissionsList
  reader completion (0.25), the 8 no-case classes' gol shapes are data-derived-only by
  design (documented), CUST OOB on 12 carriers (0.25), Awareness field roles 0..12 from
  consumers (0.5)).
- NOT in (unchanged): AI/mission flow 4-6; audio 1-2; UI 1-2; cloth cape 1; cross-region
  nav 1-2; city-scale lit rendering 1-2. Memory: pending real GPU.

## SESSION 61 (round 51, 2026-10-26) — id-space question RESOLVED (engine loads ALL 653 templates; s60 "504 unknown" = capstone-stall artifact; complete 120-id reader registry); vehicle-health 2nd-signal search closed (single-signal PARTIAL); skinning root cause proven (3 concrete causes, one-bone repro exact); posed capture landed on the enemy page (PARTIAL on the convention gap)

- **T1 (400fef9):** GenerateComponentTemplate 0x368ac0..0x36b658 is a BINARY-SEARCH compare tree
  split across two code islands ($d pools at 0x369ab8/0x36b658 halt naive linear disassembly -
  s60's "64 cases" = island-1 movw compares only). Restart-on-invalid + raw movw/movt/mov+movt
  scanning: **ALL 120 distinct component ids in gol.bin have GCT cases** (incl. 0x222500f6 via
  `mov r3,#0xf6; movt r3,#0x2225` @0x368be4). GOM::Load (ctor-only, from CLevel::CLevel) parses
  game_config.gla's gol.bin COMPLETELY: DICT magic -> BeginRead (rewind, gol mode, consumes
  tableOff+pad, wires the STRING TABLE into [stream+0x28]) -> "GO"+ver3 header -> 653 records:
  oid, refs-list (M[oid], read by GetObjectReferencesTemplateFromObject), name (u32 string-table
  index -> M2 name->oid), cnt2 x (classId u32, flag u16) -> TObjectData{flag,comp,id}, then
  cnt2 x GCT(classId, stream) - NO filter and none needed. CheckObjectCategory post-scan:
  0x3438ab08=CComponentGrenade (gadget), 0x378ded9b=CComponentDropCollectible (vehicle template).
  Case-body extraction gives the COMPLETE registry (vtable[+0x10]=Load, no RTTI prefix):
  120/120 ids -> named readers (0x5441a117=CComponentBuiltinPlane NOT "StateSet",
  0x6754056b=CComponentAwareness, 0x222500f6=CComponentTheBatHandle, 0x2ca13c06=
  CComponentVehicleCollision...). Hash hypothesis MOOT. Closure (denominator 653): engine-true
  bounds **555/653 (85.0%)**, exact **313/653 (47.9%)** with ONE labelled fitted rule (0x59a8390c
  template shape 16 B); 93 fails = auto-extractor sequence gaps (18 call-incomplete specs:
  Trail/MissionsList/Awareness auto-specs need hand verification, est. 0.5 session). Nulls:
  perm 313->3 (collapse), rot7 311 (length-only, weak, documented). Carriers: s58 30/50 (fitted)
  + s60 18/18-exact (hybrid) remain the value source; under pure engine specs 13/50 close with
  misaligned values (same auto-spec gaps). REMOVES s60's "engine-cannot bucket 90" entirely.
- **T2 (bae0faf):** second-signal search CLOSED - 300.0 occurs EXACTLY ONCE per vehicle payload
  (at the Health position; heli 2783/3048 hits = float-array coincidence at family-specific
  offsets). Signal 1 now engine-NAMED (CComponentHealth::Load via the case body). Verdict
  unchanged: PARTIAL single-signal (mechanism corroborated, value has no independent signal).
- **T3 (22daa84 branch + e4386ee main):** s60's applyBoneTransform zeros ROOT-CAUSED with a
  one-bone repro (jsverify/s61_t3_repro.mjs): (a) r160 applyBoneTransform reads 4-component
  skin attrs unconditionally (1-comp attrs -> undefined weights -> bones[undefined]);
  (b) bind() without explicit bindMatrix RECOMPUTES inverses from the posed state (explicit
  `bind(skel, new Matrix4())` keeps the file invB - verified exact);
  (c) skeleton.pose() clobbers the clip pose. Per-frame recipe proven:
  action.time -> mixer.update(0) -> updateMatrixWorld(true) -> skeleton.update() ->
  applyBoneTransform == numpy convention. Page: captureSkinnedFrames landed (15 posed frames,
  3x5 clips, raw WebGL1 raster, skinDiff wrong-clip 6.4824, 0 errors, play gate intact).
  PARTIAL: CPU-chain rest/bind convention gap remains (restMaxDev 1.87 = body-height; posed
  heights 26-154 u vs render 1.87 u; mesh-transform zeroing ruled out) -> posed numpy IoU
  table + rolled/batman nulls NOT achieved (est. 0.5-1 session: dump page boneWorlds, numpy
  re-skin, IoU).
- **T4:** PARTIAL/not-attempted - the combat slice keeps the s60 point cloud; the skinned-mesh
  swap is blocked by the same T3 convention gap (the point cloud uses its own node-hierarchy FK
  and was already validated).
- **T5:** INCONCLUSIVE - not attempted this session (time; the virtual-wall re-anchor gate from
  s60 stands; real-soup collision re-anchor remains scoped).
- **T6:** no real-GPU gpucheck block supplied -> environment-dominated, pending real GPU (unchanged).
- **T7:** bundles_s61 built (main 8d8a6a9..HEAD, glide cf74c5b..22daa84), SHA256 in
  download/bundles_s61/SHA256SUMS.txt; NO push this session (no token supplied); estimate:
  template-coverage residual = hand-verify ~18 rep-heavy reader sequences (0.5) + T3 convention
  gap (0.5-1); NOT in (unchanged): AI/mission flow 4-6, audio 1-2, UI 1-2, cloth cape 1,
  cross-region nav 1-2, city-scale lit rendering 1-2. Memory: pending real GPU.
## SESSION 62 (round 52, 2026-10-26) — s61's 3 residuals CLOSED (engine-true template closure 473/653 exact, zero fitted rules; posed skinning restMaxDev 1.87 -> 0; combat slice runs the SKINNED merc mesh); REAL-soup glide re-anchor gate PASS; STR = string-table INDEX correction

- **T1 (104f78a):** engine-true closure with hand-derived readers - **exact 473/653 (72.4%),
  pass 642/653 (98.3%), ZERO fitted rules** (s61: 313 exact + 1 fitted golshape; +160 exact,
  +87 pass, fitted rule REMOVED). TWO s61 extraction defects found and fixed: (a) tail-call
  reads missed (BeastObjectComponentGlobal/BeastObject/SurveillanceCam/Destroyable/Motion
  read strings at function end); (b) the id->case pairing was SHIFTED for 42/137 ids (s61
  paired cmp sites in tree order with ids in value order) - re-extracted from the
  movw/movt pair feeding each cmp; validated by GetId co-location, template names
  (Batarang_* contain 0x0f992a02=CComponentBatarang), s57's page-validated 0x5441a117.
  Corrections incl. 0x0f5f8cfd=Animated (NOT ExhaustFan), 0x62353c58=SurveillanceCam,
  0x519ad19b=MuzzleFlash, 0x1d50aa73=CharXPLevels; s61's "0x3c3f30=CComponentTutorial for
  0x59a8390c" was wrong (0x59a8390c = the GCT fall-through BeastObjectComponentGlobal).
  44 readers hand-derived incl. Trail [i, rep(c,STR,STR,f6)], CustomizeActor (nested),
  ActorBase [c7,f16,c3,i,i, rep(i: i,c)], StateSet [i(count), rep(count: CCS::Load), STRx7].
  Nulls: spec-perm 473 -> 24 (collapse, discriminative); rot-7 349 (length-only, documented).
  Residual 6 fails = StateSet count>0 templates (CContainerStateAnimation body) -> T5.
- **T2 (a6bc03d):** posed merc skinning FIXED IN PAGE - restMaxDev 1.87 -> **0**. The gap
  was TWO stacked defects, neither skeleton/invB: (1) r160 applyBoneTransform CALLING
  CONVENTION - `_basePosition.copy(vector).applyMatrix4(bindMatrix)`: the PASSED vector is
  the base position and the geometry is never read; s61's capture passed (0,0,0) -> every
  CPU-skinned vertex was exactly 0 (restMaxDev 1.87 = max|bind coords|, a body-height).
  FIX: seed vTmp.fromBufferAttribute before every call. (2) the enemy clips' ROOT CHANNEL
  overwrites mercObj placement per mixer.update - re-zero AFTER the mixer. GLB/skeleton
  needed NO change: file invB == inv(BIPED-FK rest) EXACTLY (prior "mismatch" was an
  orientation bug in the comparison); numpy cross-check: 15 frames mean vertex distance
  0.0000, IoU mean 0.9001 (nulls: rolled 0.0-0.55, batman cross 0.4377); default soup
  digest 00ce7970/137893 unchanged, 0 errors.
- **T3 (a56c4dc):** combat slice runs the SKINNED MERC MESH - enemy_viewer triangle raster
  replaces the s60 FK point cloud; per-state skinned silhouettes Idle/Walk/Run/Hurt/Death
  lit 1364-1717 px @128 raster; diffs idleWalk 60 / walkRun 44 / idleDeath 39 / idleHurt 41
  occupancy cells; mesh wrong-clip control 60 = detected. Gate PASS: stateSeq
  Idle,Walk,Run,Walk,(Hurt,Walk)xN,Death; hp 120-5=115 Hurt, -10=105, drain->0 Death;
  cone FOV 160, negatives far/behind -> Idle; 0 console errors; s60 point-cloud gates
  re-verified green.
- **T4 (68df188 main + 73fbecb glide page):** REAL collision-soup air-collision re-anchor
  for the glide (?s5real=1) - GATE PASS. The walker's blocked() capsule query at the
  DESTINATION altitude; edge-triggered not-blocked->blocked; try_slide resolution;
  S5.anchor reset = the ResolveAirCollision analogue (0x398570). 2 real re-anchors
  @17/300 ms (distinct slide-resolved positions), blendD dip restart measured @300 ms,
  landed, control reanchors=[], soup digest 00ce7970/137893 unchanged, 0 errors. THREE
  defects caught by gating and fixed by patches 2/4/6 (kept as generators): nz TDZ
  (block referenced `const nz` before declaration); staging v1 probed 3 u BELOW the
  ground plane (never fired) while v2's retarget landed the glide start on nm_ground
  VOID (straight fall, 3 identical probe runs) -> v3 DETECT-ONLY facade census (8/16
  rays at 64..156 u); `const tgt` -> let once staging fires. Physics recorded: with the
  engine-default glide (pitch0 fixed) the reach from a ~9 u ledge is 2.51 u - mid-glide
  facade hits at 12+ u are unreachable; the natural facade-adjacent-ledge pattern is the
  engine-true demonstration; the s60 virtual-wall case remains the controlled geometry
  test. s5 gate object gained from/tgt/wpsN/realStaged provenance on BOTH finalize paths.
- **T5 (65e2b2d):** CAS decode PARTIAL with 2 structural findings: (1) **payload STR =
  u32 string-table INDEX** (gol-mode ReadString path 0x33a2f0 bounds-checks the index
  into the wired table; Helicopter reads 0x0fcc..0x0fd1 sequentially = state/anim/script
  names; NO inline ASCII in any residual payload) - SIZE-compatible, closure numbers
  STAND, s61's STR readers reinterpreted as index-reads; (2) state boundaries directly
  observable: Helicopter 13 states (159/175/131/... B), BatPod 2x110 B + S x7 tail, and
  EVERY state reads its first CAS name at EXACTLY +82 ('-- NONE --' for Idle,
  'propeller_rotate'/'fly'/'land') -> CCS fixed head = 82 B, f10 byte-verified
  [0,0,0,0,1,1,1,0,0,20] at +0x17. Blocker: the inlined trigger element [i6,f,i2,S,i]
  (44 B address-order) cannot fit 131-B states (animName@82 + scriptName@110) -> the
  inline loop blocks are compiler-reordered; needs a real CFG trace of the loop bodies.
  Zero speculative rules committed; residual stays 6 fails.
- **T6:** no real-GPU gpucheck block supplied -> environment-dominated, pending real GPU
  (unchanged).
- **T7:** handoff section; bundles_s62 (main 8d8a6a9..65e2b2d, glide cf74c5b..73fbecb)
  with SHA256SUMS.txt; NO push this session (no token supplied; remote READ-verified at
  session start: main 8d8a6a9, gh-pages 6145545 LIVE, staged 39298a4 - all as expected).
  Estimate: T5 finish = CFG-trace the trigger loop bodies 0x3b88cc..0x3b8988 + CAS sweep
  with the +82 anchor (0.25-0.5); NOT in (unchanged): AI/mission flow 4-6, audio 1-2,
  UI 1-2, cloth cape 1, cross-region nav 1-2, city-scale lit rendering 1-2. Memory:
  pending real GPU.
