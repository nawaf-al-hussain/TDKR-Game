# CLAUDE_HANDOFF.md — problem brief for an outside AI collaborator

*Written 2026-10-09. Everything below is verifiable in this public repo:
https://github.com/nawaf-al-hussain/TDKR-Game — live viewer:
https://nawaf-al-hussain.github.io/TDKR-Game/*

## 0. TL;DR — UPDATED AFTER SESSION 12 (same day)

We are reverse-engineering Gameloft's delisted mobile game **The Dark Knight
Rises (2012)** to rebuild its open-world Gotham City in a browser 3D viewer.
Over 12 research sessions we cracked the container formats, geometry, texture
decoding, material database, the bake/UV system, and — as of session 12 —
**the lvc node-graph placement records**.

**Blocker A from the first version of this brief is SOLVED.** The LongDist
skyline units are now placed at their real world coordinates, decoded from
the lvc DICT object stream (`CTemplateObject` typeId 0x2662 records):
island1 = (-141.69, -681.15, 0.114), island2 = identity. Deployed as v13:
the viewer boots STREET + SKYLINE together. Full write-up:
`extraction/re/RE_NOTES_session12.md`.

**The remaining problem** is now:

1. **Street batch material index** (which of the 500 cracked materials does
   each streamed zone segment use?) — `batch_info.bin` bitstream via
   `CInterleavedDataAllocator`, undecoded. This leaves ~600 near-tier
   building segments dark. This is THE remaining visual blocker.
2. Placements for the hero units (bridges/monorail/railway) — their lvc
   records exist in the extracted placement table but are not yet matched
   to units (the generic `CGameObjectManager::CreateObject @0x36774c` read
   order needs decoding).
3. Secondary: ground-material split (roads/grass one planar unit) and
   near-field geometry density.

## 1. Project context

- **Game**: The Dark Knight Rises, Gameloft 2012, Android, delisted. Version
  1.1.6b. Source: APK (7.8 MB) + OBB expansion (895 MB), both attached to
  release `v1.1.6b` in this repo (attestation in README §Provenance).
- **Engine bits of interest**: native lib `lib_libKRHP.so` (ARM A32, not
  Thumb), `lib_gameloop*`; Lua bootstrap embedded in the level config.
- **Deliverable**: a GitHub Pages three.js viewer streaming the extracted
  city as GLBs (45 GLBs / 1.53M verts / 1.65M tris at last full deploy).
- All RE artifacts (notes, decompilations, scripts, intermediate JSON) are
  committed under `extraction/` — this repo is the single source of truth.

## 2. Pipeline in one paragraph

`TDKR_v1.1.6b.apk + OBB` → `.gla` big-endian containers (16-byte header +
n×16 index table + name pool + chunks: `game_config.gla`, `l_gothamcity.gla`,
`l_gothamcity_tex.gla`, `commons_tex.gla`) → geometry chunks (.bdae meshes),
zone-stream archive (`GothamCity*.zip`, 168.5 MB, inside `l_gothamcity.gla`),
level config `.lvc` (BRES nodes + bake groups + zones), textures (PVR,
ZIP_SPLIT rgb/alpha pairs) → `extraction/scripts/export_city.py` builds
textured GLBs → `gh-pages/models/manifest.json` (tiers: street / hero / fp /
district / low) → three.js viewer `gh-pages/app.js`.

## 3. What the user sees TODAY (v12.2) and why it "still looks wrong"

Deployed state (`origin/gh-pages` @ b500639, manifest internal version 11):

- **Boots**: street tier only (21 GLBs, world-placed, engine-correct
  road/grass/prop materials). v12 boot policy comment in `app.js` explains
  why the other tiers are default-off.
- **The ~600 near-tier building segments inside the street tier have no
  albedo** — they render dark. The per-segment material index for the zone
  stream is not decoded yet, so the exporter can only bind a conservative
  dark fallback to them. This is blocker **B** below.
- **The skyline (all LongDist bake units: hero assemblies + 54 footprint
  meshes) is hidden by default** because every one of those units is authored
  in LOCAL coordinates (bbox ≈ ±100 around origin; verified via
  `parse_meshes`) — rendering them unplaced would pile city blocks at the
  origin, which was the source of the original "grass/roads on buildings"
  report. Their world placement lives in the lvc/BRES node graph, which is
  not decoded yet. This is blocker **A** below.
- District props default-off for the same reason.

Net effect: a flat streetscape with dark building shells and no towers. From
the user's perspective, "everything looks wrong."

## 4. Symptom history — what each texture complaint was and how it died

| # | User report | Root cause found | Session/commit |
|---|-------------|------------------|----------------|
| 1 | Wrong textures on models | fp meshes used UV-fit heuristic against 8 `GC_LongDist_*` atlas pages | pre-6 |
| 2 | Wrong + low quality | V-convention: game UVs are bottom-origin; viewer `flipY=false` sampled every page vertically mirrored; bake pages re-encoded at 1024/q78 | session 8 (0c133e2) |
| 3 | Still wrong assets | LongDist DiffuseMaps are *runtime bakes*, not shipped textures; fp meshes store bake UV (Coord1) in the FIRST vertex dword (+12), not +16 | session 7 (985da5d) |
| 4 | Grass/roads ON BUILDINGS | (a) edge-density UV-fit scored road atlases highest and bound buildings to the Roads page; (b) bake pages were used as albedo substitutes (mode 2x); (c) bdae TRUTH says these are `StandardDiffuseDC-fx` ×1; (d) whole LongDist layer is local-coord → unplaced pile at origin | session 11 (3fa5a70) |
| 5 | "Still everything looks wrong" | state described in §3 — dark near-tier buildings + hidden skyline | **current** |

Fixed along the way and verified (do NOT re-litigate): `flipY` semantics, V
origin, ZIP_SPLIT rgb/alpha PVR decode, LongDist pages as runtime bakes,
per-footprint→assembly-bdae page map (54 entries, zero heuristics —
`load_fp_page_map()` in export_city.py), bake-as-albedo prohibition,
water-plane binding, LUT color grade (`000_default.tga`), lightning system,
rainbow smears on street tier (structural cross-section binding, session 10),
street-tier material bindings (zone material DB cracked via `source.dae`
setparam chain — 305+195 materials with exact DiffuseMap+LightMap bindings).

## 5. THE TWO BLOCKERS (all knowns, all unknowns)

### A. Node-graph world transforms for LongDist units (skyline placement)

**What we need**: the transform (translate/rotate/scale) that the engine
applies to each LongDist bake unit (`GC_Footprint_*_LongDist.bdae` meshes,
`GC_island1_LongDist`, hero assemblies, monorail/railway LongDist) so they
can be rendered at their true world positions.

**Knowns**:
- All such units are local-authored: per-unit bbox ≈ ±100 units around
  origin (`parse_meshes` in export_city.py).
- The 530 bake-group frames in the lvc (see `extraction/re/
  bake_regions_v2.json`, 89 records / 54 footprints, and
  `bake_regions.json` 530 records) carry page+scale/offset (Coord1 = uv ×
  so.xy + so.zw; loader verified: `CComponentBeastObjectComponent::Load`
  @0x2e1e8c reads `{so1, page, so2}`) but **no world transform**.
- `GothamCity.lvc` string table does **not** reference the footprint mesh
  names at all — so placement is not a simple name→transform table there.
- Candidate homes for the transforms: the **BRES node hierarchy** in
  `GothamCity.lvc` (parsed: `extraction/re/lvc_gothamcity_parsed.json`,
  `lvc_bakegroups.json`), bdae node/scene sections, or a separate placement
  chunk inside `l_gothamcity.gla` we haven't identified.
- Loader-side code we already have in `extraction/ghidra/decompiled/`:
  `bakegroup__3ce548.c` (CComponentBeastBakeGroup::Load — reads only
  `{string, float, string, float}`), `bakegroup__49d870.c`
  (CTemplateBakeGroup::Load), `batchbaker__*.c`, `irradiancebaker__*.c`.
  Beast component Load handlers: `CBeastAreaComponent::Load` @0x2b164c,
  `CBeastDirectionalComponent::Load` @0x2b17e0,
  `CBeastObjectComponent::Load` @0x2b1ea4 (~2.3 KB, biggest, may hold more
  fields), `CBeastObjectGlobalComponent::Load` @0x2b2a80.
- The street tier (zone stream) IS world-placed — so the zone stream carries
  its own transforms; the contrast may help identify what the LongDist
  layer lacks.

**Tools that exist**: `extraction/re/find_zone_xrefs.py`, `find_zone_loader.py`,
`disasm_beast_loads.py` (capstone ARM-A32 disassembler with ELF symtab
annotation, targets preloaded), `parse_lvc.py`, `parse_lvc_bakegroups.py`,
`xref_bl.py`, `elf_syms.py`, `scan_movw_movt.py`.

### B. Street batch material index (near-tier building albedo)

**What we need**: for each segment of the streamed street geometry, the
material index into the zone material DB (which is fully cracked —
`extraction/REPORT.md` §; exact DiffuseMap/LightMap per material id).

**Knowns**:
- Streamed zone archives: `GothamCity*.zip` inside `l_gothamcity.gla`
  (session 9, 0d1c1fc/60fcad3); islands 1+2 extracted: 1.19M verts /
  1.45M tris.
- Geometry layout proved: `lod_table`/`lod_data` segment descriptors,
  24-byte-stride interleaved vertices (octahedral normals), u16 strip
  indices (`extraction/re/` notes + zone scripts).
- Per-segment material is NOT in the vertex data; the engine reads a packed
  **`batch_info.bin`** via `CInterleavedDataAllocator` (native). We have not
  decoded its bitstream. Loader code: see session 10 notes and
  `extraction/scripts/disasm_zone_loader.py`.
- Once decoded: ~600 dark near-tier building segments get real albedo from
  the same DB — this is the single biggest visual win available.

### C. (Secondary) Ground fidelity split + near-field density

- User complaint: roads and grass are merged into a single planar unit in
  the street tier; ground lacks fidelity; near-field visible geometry is too
  sparse. Likely answers live in the same zone stream (more detailed
  near-LOD segments, per-region material splits — the zone material DB
  already separates road/sidewalk/grass/crossing materials). Do AFTER B.

## 6. Repo map (the paths that matter)

```
CLAUDE_HANDOFF.md              <- this file
README.md                      <- provenance, viewer link, SHA256s
extraction/REPORT.md           <- format spec (bdae, gla, textures)
extraction/worklog_session10.md / re/RE_NOTES_session{9,10,11}.md
extraction/scripts/            <- all exporters/decoders
  export_city.py               <- master exporter (v12, load_fp_page_map)
  restore_assets.py            <- OBB/zip -> raw .gla restore
  zone_extract.py / disasm_zone_loader.py
extraction/re/                 <- RE data + probes
  bake_regions.json (530 recs) / bake_regions_v2.json (89 recs, 54 fp)
  lvc_bakegroups.json / lvc_gothamcity_parsed.json
  disasm_beast_loads.py / find_zone_xrefs.py / elf_syms.py
extraction/ghidra/decompiled/  <- IDA/Ghidra-style .c per function
gh-pages/                      <- viewer source (app.js, models/, manifest)
```

## 7. How to reproduce / inspect

```bash
git clone https://github.com/nawaf-al-hussain/TDKR-Game
# data (public release asset):
curl -LO https://github.com/nawaf-al-hussain/TDKR-Game/releases/download/v1.1.6b/TDKR_v1.1.6b_APK_OBB.zip
# restore raw containers, then:
python3 extraction/scripts/export_city.py --dry
# live viewer (as deployed, v12.2):
#   https://nawaf-al-hussain.github.io/TDKR-Game/
```

## 8. Concrete asks (ranked)

1. **BRES/lvc node-graph decode**: where are the world transforms for the
   LongDist bake units? Pointers: `GothamCity.lvc` (BRES), bdae node
   sections, the four CBeast*Component::Load handlers listed in §5A, and
   any chunk in `l_gothamcity.gla` that looks like a placement table. Any
   struct-layout hypothesis for the node entries (offsets, counts, parent/
   child chains) would immediately unblock the skyline.
2. **batch_info.bin bitstream**: find `CInterleavedDataAllocator` in
   `lib_libKRHP.so` and recover the per-batch material-index encoding
   (field order, bit widths, alignment) so we can map each street segment
   to its material id.
3. Sanity-check our engine model for LongDist units: is `DiffuseMap =
   GC_LongDist.tga` + `StandardDiffuseDC` (×1) really albedo-only, or does
   the runtime multiply a scene bake (island lightmap) on top as well?
4. Anything that looks wrong in the current deployed pipeline that we've
   gone blind to after 11 sessions of fixes (fresh eyes welcome).

## 9. Do-not-re-suggest list (all fixed and verified)

- UV-fit / edge-density page selection (replaced by authoritative
  assembly-bdae footprint→page map).
- `flipY=true` in three.js GLTF loader (game UVs are bottom-origin; GLB
  choke point flips V).
- Using bake/lightmap pages as building albedo; mode "2x" for these units.
- Per-footprint LongDiffuseMap aliases as standalone textures (they are
  runtime bakes of the assembly pages).
- Re-encoding textures below 2048/q88.
