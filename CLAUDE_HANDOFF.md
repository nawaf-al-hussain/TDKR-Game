# CLAUDE_HANDOFF.md — problem brief for an outside AI collaborator

*Written 2026-10-09, updated after session 14. Everything below is verifiable
in this public repo: https://github.com/nawaf-al-hussain/TDKR-Game — live
viewer: https://nawaf-al-hussain.github.io/TDKR-Game/*

## 0. TL;DR — UPDATED AFTER SESSION 14 (same day)

We are reverse-engineering Gameloft's delisted mobile game **The Dark Knight
Rises (2012)** to rebuild its open-world Gotham City in a browser 3D viewer.
Over 14 research sessions we cracked the container formats, geometry, texture
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

**Blocker B — batch_info.bin LAYOUT SOLVED this session (value semantics
still open):**

- `batch_info.bin = u32(197) + M × 197-byte records`, **one record per
  material**: M = 307 (island1) / 196 (island2) = the EXACT material counts
  of the zones' materials bdae (`source.dae` library_materials).
- Record m's **first byte = m** (material index; 307/307 and 196/196,
  wrapping mod 256).
- The leading u32 **197 = the record stride in bytes**, NOT a record count —
  and the SAME 197 is the last u32 of `stream_info.bin` (which is
  `[6 × f32 streaming bbox][u32 X][u32 197]`; X = 234,466 / 303,832 open).
- Inside a record: 196 slots, 0xFF in 13.4% (both islands), 0x00 in 68%,
  values 0..254 saturating; 12–13-long ff runs; small f32 groups
  (UV-rect-like) at in-record offsets ~75–115.
- Full evidence + hexdumps + material name order:
  **`extraction/re/batch_info_evidence14.md`** (plus
  `batch_info_material_names14.txt`). This is where we would most like
  your help: pin the slot/value semantics.

**Also still open:**

1. **Hero-unit placements** (bridges/monorail/railway): names ARE plain
   interned strings in the lvc; the main (non-reflection) units are placed
   by the GENERIC object path (`CGameObjectManager::CreateObject @0x36774c`,
   component factory loop) — read order still to decode.
2. Secondary: ground-material split (roads/grass one planar unit) and
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

## 3. What the user sees TODAY (v14, deployed and smoke-tested)

- **Boots**: street tier (21 GLBs, world-placed, engine-correct road/grass/
  prop materials — ~600 near-tier building segments still dark, blocker B)
  **+ skyline tier (5 island-1 LongDist GLBs at the engine's own
  TRS (-730,-1250,0))**.
- Island-2 skyline units removed (no main-level record; they belonged to the
  separate island-2 level and were floating in the wrong place). The
  island-2 hero units (monorail/railway/small-bridge) remain as OFF-by-default
  research toggles (local frames, generic-object records not yet decoded).
- **Deploy = gh-pages branch @ v14, verified by
  `extraction/scripts/site_smoke_test.py` (53/53 PASS)**. The gh-pages
  branch had gone stale (v13 served while main held v14) — the smoke test
  now guards every deploy. Hero-tier `GC_Railway_Island2_LongDist` overlaps
  the island-1 area by 21k u² at local coords; it stays hidden by default
  until its placement record is decoded.

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

### B. Street batch material index — LAYOUT SOLVED (session 14), value semantics open

**What we need**: for each segment of the streamed street geometry, the
material index into the zone material DB (cracked in session 10 — now
counted exactly: **307 island-1 / 196 island-2 materials**, from
`source.dae` in each `<island>_materials.bdae`).

**SOLVED this session (full evidence pack:
`extraction/re/batch_info_evidence14.md`):**

```
batch_info.bin := u32(197) + M × 197-byte records      M = material count
record(m)      := u8(m)  + 196 slot bytes
```

- M = 307 (island1) / 196 (island2) — the exact division that motivated
  the old "197 records of 307/196 B" reading was an arithmetic shadow of
  this layout.
- Record m starts with byte m (material index; verified 307/307 + 196/196,
  mod 256 for m ≥ 256). The file header 197 = record stride, NOT a count;
  stream_info.bin repeats it as its last u32 (it is
  `[6×f32 bbox][u32 X][u32 197]`).
- Slot bytes: 0xFF 13.4% (12–13-long runs), 0x00 68%, values 0..254
  saturating; adjacent slots highly correlated; f32 groups (UV-rect-like)
  around in-record offsets 75–115.

**Remaining unknowns (the asks):**
1. The semantics of the 196 slots and their byte values. Fixed engine pool
   (both islands share the SAME slot count while segment counts differ
   1,526 vs 1,020) is the leading hypothesis; 0 = free / FF = N/A / value
   = per-(material, slot) segment count or weight — unresolved. A u16
   reading of the slots does NOT produce clean values.
2. The engine reader: `CLevelStreaming_DB::Load` @0x406dfc orchestrates;
   the per-file parse is in non-exported helpers (bl targets 0x3dac58 ×8,
   0x42e2bc ×7, 0x455e2c ×6). The stream-name table @0xb40704 has NO
   absolute pointers in the whole image (full-file literal scan) — it is
   reached via a computed base + enum index, so string-xref hunting is a
   dead end; the enum-index code path in PrepareFiles/Load is the way in.
3. stream_info's X u32 (234,466 / 303,832).
4. Cross-check: match material m's slot values against the street GLB
   per-mesh material bindings (gt DB) — if slot ≈ spatial batch, per-
   (material, slot) mesh counts should track the byte values.

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

1. **batch_info.bin value semantics** (§5B): the layout is solved
   (`u32 197 + M × 197-byte records`, record m starts with byte m; M =
   material count). What are the 196 slots (fixed engine batch/LOD pool?),
   and what does a slot byte mean (0x00 68%, 0xFF 13.4% in 12–13 runs,
   values saturating at 254, f32 groups at offsets 75–115)? Evidence pack:
   `extraction/re/batch_info_evidence14.md`.
2. **Generic object records** (CreateObject component loop): read order for
   the non-special typeIds so the hero units (bridges/monorail/railway)
   get their world TRSs.
3. Sanity checks welcome on the v14 skyline placement — with the ZNCC
   retraction in mind, the load-bearing evidence is the engine record +
   the per-prim centroid correspondence (`extraction/re/skyline_verify14.json`).
4. Anything that looks wrong in the deployed pipeline that we've gone blind
   to after 14 sessions of fixes (fresh eyes welcome).

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
