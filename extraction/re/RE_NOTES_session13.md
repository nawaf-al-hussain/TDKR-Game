# RE Session 13 — blocker A CLOSED (for real this time), skyline placed by the engine's own record

## Trigger
Outside-AI review (Claude) audited the session-12 skyline validation and
listed 7 weak spots. Every one was executed. Result: **the session-12
placement was Batman's spawn point, not the skyline placement.** The real
record was found by disassembling the remaining CLevel::LoadNextObject
handlers.

## The seven review points — results

1. **Translation sweep** — done with FFT cross-correlation (street vertex
   occupancy vs filled skyline footprints) and ZNCC of density maps. The
   binary-overlap metric is indeed too flat (peak/p99 ~1.3); the ZNCC
   discriminates: **+0.66 at the true record TRS** vs -0.04 (identity) and
   +0.08 (v13 offset).
2. **Two X values (-140.7 vs -141.69)** — both were WRONG, and both came
   from the same misparse: reading a "CTemplateObject" record at 0x55575
   actually straddles TWO records (see 3). The (-140.69, -681.19, 0.114)
   TRS belongs to... Batman.
3. **The record is `batman.bdae`!** typeId 0x2662 = CSpawnPointObject
   (NOT CTemplateObject). Disasm of the 0x2662 handler (0x48af5c) and
   CSpawnPointObject::Create (0x2a7840) proves the layout:
   `bool, int objId, 9f TRS, 3 bools, string, string (Lua!), 3 bools, int`.
   The spawn @0x5557d is `batman.bdae` objId=2000108 at (-140.69, -681.19,
   0.114) — a street-level player spawn. The 'gc_island1_longdist.bdae'
   name at 0x55575 belongs to the PREVIOUS record's mesh component.
4. **THE REAL RECORD — typeId 0x14051 @0x55545**: the handler (0x48ad00)
   calls CComponentBase::Load (bool, int objId, 9f TRS, 3 bools) +
   CComponentMesh::Load (string mesh, 4 chars) -> ConstructColladaScene ->
   scale/rot(deg->rad pi/180 @0x48b120)/position ->
   **CLevel::AddLowPolyLongDistanceNode**. Record:
   `objId=111989, TRS pos=(-730.0, -1250.0, 0.0) rot=(0,-0,0) scale=(1,1,1),
   mesh='gc_island1_longdist.bdae'`, chars=00000001.
   GothamCity_Island2.lvc has the same record type (@0x58a0a, same TRS)
   for 'gc_island2_longdist.bdae' — in the SEPARATE island-2 level.
5. **FP4/LOW** — FP4 does not exist; the family is FP1/FP2/FP3/Roads/LOW.
   Centroid correspondence recomputed from the shipped GLBs: FP1 max 3.8u,
   FP2 4.4u, FP3 10.9u (nearest-match noise; session-12's "0.5u" was
   optimistic), Roads bbox-identical, LOW is a different mesh structure.
   One transform for all — confirmed.
6. **Axis convention** — exporter applies the record TRS in game coords
   BEFORE the (x,z,-y) Y-up rotation; rot=0 stays 0 under the basis change.
   Verified in code; the failure was the VALUES, not the convention.
7. **Island-2 identity** — WRONG. The main level has NO island-2 skyline
   record; its LongDist units belong to GothamCity_Island2.lvc only. The
   v13/v12 "identity" placement made island-2 buildings float over island-1
   (40% filled-footprint overlap). All 5 island-2 skyline GLBs REMOVED from
   the deployed site in v14 (they remain in the repo history / hero tier of
   future exports).

## Record-type dictionary now proved (all from disasm)

| typeId  | class/function                          | payload read order |
|---------|------------------------------------------|--------------------|
| 0x2657  | CTemplateLevelProperties                 | (session 3)        |
| 0x2667  | CTemplateZone::Load @0x48d5f4            | bool,str,f,bool,int,9f,3b |
| 0x265f  | CTemplateMetaZone::Load @0x48d708        | 4b,3i,9f,str       |
| 0x2662  | CSpawnPointObject::Create @0x2a7840      | bool,i,9f,3b,str,str(Lua),3b,i |
| 0x2663  | (marker object)                          | i,9f               |
| 0x2664  | (ref marker)                             | i                  |
| 0x1869f | CTemplateBakeGroup::Load @0x48d870       | bool,i,9f,3b,str(page),f,str(page_low),f |
| 0x14050 | reflection: CComponentBase+Mesh->ConstructColladaScene->AddBatchNodeReflection | bool,i,9f,3b,str(mesh),4c |
| 0x14051 | LongDistance: same -> AddLowPolyLongDistanceNode | same |
| other   | -> CGameObjectManager::CreateObject @0x36774c (generic) | |

42x 0x14050 records in GothamCity.lvc = one per `gc_footprint_*_reflection.bdae`
(+ gc_railway_island1_reflection) — each with a REAL world TRS (e.g. vb
@(-850,-980), ic @(-730,-1250)). Four 0x1869f bake-group templates (pages
Island1 A/B/Landmarks/Roads; two at identity, Landmarks @(-735.17,-910.72),
Roads @(-837.38,-1163.00) — meaning still open).

Full walk: extraction/re/lvc_records.json (320 exact records + resyncs over
the generic-object region), island-2: lvc_island2_records.json.

## Shipped (v14)

- export_city.py: corrected ISLAND_WORLD_OFFSET island1 = (-730, -1250, 0);
  LD_WORLD now island-1-only (island-2 LongDist files fall to hero/research).
- gh-pages/models: the 5 island-1 skyline GLBs shifted by
  delta_gltf = (-588.31, -0.114, +568.85); city_low.glb shifted
  GC_island1_LongDist_LOW and dropped GC_Island2_LongDist_LOW; the 5
  island-2 skyline GLBs deleted; manifest v14 (40 GLBs; tiers: street 21,
  skyline 5, hero 11, fp 1, low 1, district 1).
- gh-pages/index.html RESTORED (the deployed viewer had no entry point —
  casualty of the earlier site-root wipe).
- Screenshots: work/valout/shot_*.png (viewer boots street+skyline; skyline
  tier now 5 GLBs / 58k tris).

## Q3 (runtime bake multiply) — CLOSED

LightMapDC-f.glsl texture calls: DiffuseMap, LightMap (+ alpha/mask/reflection
branches + FogTexture). StandardDiffuseDC-f.glsl: DiffuseMap only. Color =
Diffuse * LightMap * 2.0 (+ fog). TWO samplers — no runtime scene/island
bake multiplication; the shipped bake pages are the final lightmap.
`page_low` = low-LOD variant of the same page (LOD swap), not a second bake.

## Blocker B (batch_info.bin) — evidence banked for the collaborator

- Files: zone zips carry batch_info.bin per island. GothamCity: 60,483 B,
  Island2: 38,616 B. BOTH begin u32le 197 (0xc5).
- Striking arithmetic: (60483-4)/197 = 307.000 and (38616-4)/197 = 196.000
  — EXACT integers for both files. Island-2 shows a repeating 196-byte
  record template (`00 01 00 00 | 01 02 | ff*17 | 03 04 | ff*19 | 00 05 |
  00 ...`); island-1's 307B grid drifts by rec3 (floats visible), so the
  307B "period" may be average-not-fixed. Header interpretation open:
  197 = count? (same for both islands!) or magic/version?
- Oracle: lod_table segment counts are 1526 (island1) / 1020 (island2);
  street-tier GLB mesh counts 1517/1020. NOT 197 — so batch_info records
  are NOT per segment; 197 matches nothing counted so far.
- Engine side: getBatchMaterial @0x44ef08 shows SBatch+0x8 = intrusive_ptr
  <CMaterial> (already resolved), +0xc = second ptr. The zone-streaming
  name table ('.zip','stream_info.bin','bih_data.bin','bih_struct.bin',
  'batch_info.bin','_materials.bdae','lod_table.bin','lod_data.bin',
  'lod_selector.bin') is a static char[16] array in .rodata @0xb40704
  (16B stride, NO pointers anywhere reference it — indexed by enum at
  runtime); source file = LevelStreaming_DB.cpp. Loader classes:
  CDoubleBufferedLODStreaming (0x45e190), CDoubleBufferedDynamicBatchMesh
  (0x45c750) — constructed via template/vtable paths, no direct BL xrefs.

## Next (ordered)

1. batch_info.bin layout — with the collaborator, using the hexdumps in
   CLAUDE_HANDOFF.md; the ReadBits-style helper hunt in
   LevelStreaming_DB / DynamicBatchMesh code continues.
2. Decode generic-object records (CreateObject component loop) => world
   placements for bridges/monorail/railway/hero units (names are PLAIN
   interned strings — no hashing, ever).
3. Ground fidelity split + near-field density (blocker C).
