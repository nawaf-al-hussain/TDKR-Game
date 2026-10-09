# CLAUDE_HANDOFF.md — problem brief for an outside AI collaborator

*Written 2026-10-09, updated after session 13. Everything below is verifiable
in this public repo: https://github.com/nawaf-al-hussain/TDKR-Game — live
viewer: https://nawaf-al-hussain.github.io/TDKR-Game/*

## 0. TL;DR — UPDATED AFTER SESSION 13 (same day)

We are reverse-engineering Gameloft's delisted mobile game **The Dark Knight
Rises (2012)** to rebuild its open-world Gotham City in a browser 3D viewer.
Over 13 research sessions we cracked the container formats, geometry, texture
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
  Validated by ZNCC of street-vertex density vs skyline roof density:
  **+0.66 at this TRS** (-0.04 identity, +0.08 at the old value).
  The session-12 value (-141.69, -681.15, 0.114) was **Batman's spawn
  point** — a `0x2662 CSpawnPointObject` record for `batman.bdae`
  (@0x5557d) whose bytes overlap the skyline record's mesh-name field;
  the earlier scan read them as a "CTemplateObject" TRS.
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

**The remaining problem is now focused on blocker B:**

1. **Street batch material index** — `batch_info.bin` (per-island files in
   the zone zips). NEW hard evidence this session: both islands' files begin
   with u32le **197**, and `(60483-4)/197 = 307.000`,
   `(38616-4)/197 = 196.000` — EXACT integers for both files. Island-2
   shows a repeating 196-byte record template. Engine-side:
   `getBatchMaterial` @0x44ef08 shows `SBatch+0x8 = intrusive_ptr<CMaterial>`
   (resolved at load). Hexdumps + candidate structure in §5B. This is where
   we would most like your help.
2. **Hero-unit placements** (bridges/monorail/railway): their names ARE
   plain interned strings in the lvc (`gc_bigbridge_2_islands.bdae`,
   `gc_monorail_island1.bdae`, `gc_railway_island1.bdae`, …). The 42
   `0x14050` reflection records carry full TRSs for the `*_reflection.bdae`
   files. The main (non-reflection) units are placed by the GENERIC object
   path (`CGameObjectManager::CreateObject @0x36774c`, component factory
   loop) — read order still to decode.
3. Secondary: ground-material split (roads/grass one planar unit) and
   near-field geometry density.

## 1. Project context

- **Game**: The Dark Knight Rises, Gameloft 2012, Android, delisted. Version
  1.1.6b. Source: APK (7.8 MB) + OBB expansion (895 MB), both attached to
  release `v1.1.6b` in this repo (attestation in README §Provenance).
- **Engine bits of interest**: native lib `lib_libKRHP.so` (ARM A32, not
  Thumb, committed at `extraction/lib_libKRHP.so`); Lua bootstrap embedded
  in the level config.
- **Deliverable**: a GitHub Pages three.js viewer streaming the extracted
  city as GLBs (v14: 40 GLBs, tiers street/skyline/hero/fp/low/district).
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

## 3. What the user sees TODAY (v14)

- **Boots**: street tier (21 GLBs, world-placed, engine-correct road/grass/
  prop materials — ~600 near-tier building segments still dark, blocker B)
  **+ skyline tier (5 island-1 LongDist GLBs, now at the engine's own
  TRS (-730,-1250,0))**.
- Island-2 skyline units removed (no main-level record; they belonged to the
  separate island-2 level and were floating in the wrong place).
- `gh-pages/index.html` restored this session (the deployed site had lost
  its entry point).

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

### B. Street batch material index (near-tier building albedo)

**What we need**: for each segment of the streamed street geometry, the
material index into the zone material DB (fully cracked — 305+195 materials
with exact DiffuseMap+LightMap via `source.dae` setparam chains).

**New hard evidence (session 13)**:

- Files: `work/zone/GothamCity/batch_info.bin` = 60,483 B;
  `GothamCity_Island2/batch_info.bin` = 38,616 B (each island's zip carries
  its own). Both begin with **u32le 197 (0xc5)**.
- **(60483−4)/197 = 307.000** and **(38616−4)/197 = 196.000** — exact
  integers for BOTH files. Island-2 then shows a repeating 196-byte record
  template; island-1's 307-byte grid drifts by record 3, so treat
  fixed-vs-variable carefully.
- Oracle checks: lod_table segments = 1526 (island1) / 1020 (island2);
  street-tier GLB mesh counts 1517/1020 — **NOT 197**. So records are not
  per segment; 197 matches nothing counted so far (same value in both
  islands!).
- Engine side: `getBatchMaterial` @0x44ef08 reads `SBatch+0x8` =
  `intrusive_ptr<CMaterial>` (already RESOLVED at load — so batch_info
  entries map to material objects somewhere between the file and this
  struct). Zone-streaming file-name table = static `char[16]` array in
  `.rodata` @0xb40704: `{".zip", "stream_info.bin", "bih_data.bin",
  "bih_struct.bin", "batch_info.bin", "_materials.bdae", "lod_table.bin",
  "lod_data.bin", "lod_selector.bin"}` (16-byte stride, no pointers
  reference it — indexed by enum at runtime). Source file:
  **LevelStreaming_DB.cpp**. Loader classes:
  `CDoubleBufferedLODStreaming<…>` ctor @0x45e190 (3× IReadFile),
  `CDoubleBufferedDynamicBatchMesh<…>` ctor @0x45c750 (3× IReadFile);
  both constructed via template/vtable paths (no direct BL xrefs).
- **batch_info.bin header + first records (hexdump)** —
  GothamCity (island 1), 60,483 B:
  ```
  00000000  c5 00 00 00 00 00 00 ff ff ff ff ff ff ff ff
  0000000f  ff ff ff ff ff ff ff 01 02 ff ff ff ff ff ff
  0000001e  ff ff ff ff 00 03 00 00 00 00 00 00 00 00 00
  0000002d  06 00 03 00 14 00 0c 00 00 00 01 00 02 00 02
  0000003c  00 14 00 10 00 00 00 03 00 14 00 0c 00 00 00
  ...                              (record grid @307 B: rec1 @0x137 = all
                                    zeros; rec2 @0x26a = ff-run then
                                    00 03 00 00 00 00 00 00 00 00 00 06
                                    00 03 00 14 00 0c 00 00 00 01 00 02
                                    00 02 00 14 00 10 00 ...; rec3
                                    @0x39d starts mid-floats:
                                    8a ff df 3e = 0.4368, 19 02 e0 3e =
                                    0.1406, 0b 5e 77 3f = 0.9650 …)
  ```
  Island2 (38,616 B), 196-byte template repeating from rec1:
  ```
  rec1 @0x0cc: 00 01 00 00 01 02 ff ff ff ff ff ff ff ff ff ff
               ff ff ff ff 03 04 ff ff ff ff ff ff ff ff ff ff
               ff ff 00 05 00 00 00 00 00 00 00 00 00 00 00 00
  rec2 @0x190: 00 00 02 00 00 01 02 ff ff ff ff ff ff ff ff ff
               ff ff ff ff 03 04 ff ff ff ff ff ff ff ff ff ff
               ff ff 00 05 00 00 00 00 00 ...
  rec3 @0x254: 00 00 00 03 00 00 01 02 ff ... (same template,
               varying u8 prefix counter 01→02→03 …)
  ```
  (full dumps will be committed with the session-13 notes).
- Candidate structure to test: `[u32 197][197 records][fixed 307/196 B]`
  vs `[u32 197][bit-packed records]`. The `ff` runs look like all-ones
  bit-fields; the `01 02 … 03 04 … 00 05` pairs look like small indices
  (material ids? sub-mesh ids?).

**Our concrete asks for you on B**:
1. Given the header + template above, does `[u32 197]` + fixed-stride
   records hold? What fields would explain `01 02 / 03 04 / 00 05` pairs
   and the all-ones runs?
2. In `lib_libKRHP.so`, the zone-streaming reader chain: we failed to find
   direct xrefs to the `batch_info.bin` string (name table indexed by
   enum). If you can suggest where `LevelStreaming_DB`-style code keeps the
   enum→file mapping, or a `ReadBits(n)` helper used by
   `CDoubleBufferedDynamicBatchMesh`, the field widths would fall out of
   its call sites (this is exactly how the DICT stream fell).
3. Sanity check: is `197` plausibly a *batch* count (material groups)
   rather than segments? The material DB has 305 island-1 materials — 197
   could be the subset actually used by the stream.

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

1. **batch_info.bin layout** (§5B): does `[u32 197][fixed-stride records]`
   hold? Field hypothesis for the `01 02 / 03 04 / 00 05` pairs and
   all-ones runs? Any pointer to a `ReadBits(n)`-style helper in the
   zone-streaming chain (LevelStreaming_DB / CDoubleBufferedDynamicBatchMesh)
   whose call sites would give the field widths?
2. **Generic object records** (CreateObject component loop): read order for
   the non-special typeIds so the hero units (bridges/monorail/railway)
   get their world TRSs.
3. Sanity checks welcome on the v14 skyline placement (ZNCC +0.66) and the
   island-2 removal decision.
4. Anything that looks wrong in the deployed pipeline that we've gone blind
   to after 13 sessions of fixes (fresh eyes welcome).

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
  2 samplers; the shipped bake pages are final.
