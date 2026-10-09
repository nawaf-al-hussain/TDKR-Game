# RE Session 12 — lvc node-graph cracked: the skyline gets its world placement

## User complaint
"Still everything looks wrong." (after v12.2: street-only boot, ~600 dark
near-tier segments, hidden skyline)

## What happened this session

Outside-AI review (Claude) hypothesized the LongDist placement lives on the
owning object, not the Beast component, and suggested hash/transform scans.
All tests run; the placement records were found — no hashing needed, the
names are PLAIN interned strings.

### 1. Beast family re-disassembled with symtab-true addresses
The old TARGETS (0x2b1ea4 etc.) were constructors, not Loads. Real family:
- CComponentBeastObjectComponent::Load @0x2e1e8c (136 B):
  `{vec4 so1, string page, vec4 so2, string page_low}` — page_low = the
  low-res bake page (bake_regions_v2.json's second string, confirmed).
- CComponentBeastObjectComponentGlobal::Load @0x2e1fb0, Beast_Area @0x2e207c,
  Beast_Directional @0x2e219c, Beast_Omni @0x2e22f8, Beast_Spot @0x2e24b0,
  Beast_Window @0x2e2638 — all lights/bake, NO transforms anywhere.
=> Claude was right: transforms live on the owning object.

### 2. The lvc is a DICT object stream (not BRES)
GothamCity.lvc: magic 'DICT', BE ints/floats, string table @0x5eb80b
(1617 interned strings), object stream from offset 9:
  [u32 objcount=14917] then per object [typeId u32][payload].
Dispatcher = CLevel::LoadNextObject @0x489ecc (see
extraction/ghidra/decompiled_r2/load_next_object.asm):
  0x2657 CTemplateLevelProperties, 0x2667 CTemplateZone (Load 0x48d5f4),
  0x1869f CTemplateBakeGroup (branch 0x48aea0 -> Load 0x48d870),
  0x2661/0x2662/0x2664 CTemplateObject family, 0x1404050/51, 0xd0bbb8
  CWorldBox (0x2b56f4), 0x265f CTemplateMetaZone (0x48d708), and the
  generic default -> CGameObjectManager::CreateObject @0x36774c (3520 B).

### 3. THE PLACEMENT RECORDS (the breakthrough)
Object records (typeId 0x2662) carry: [name str][01][typeId][payload:
int, TRS 9 floats (pos3, rot-euler3, scale3), bools, -1 refs, nested
typeIds...].  Extraction anchored on scale=(1,1,1) triple + plausibility:

**gc_island1_longdist.bdae (str#166 @0x55575, typeId 0x2662):
  pos = (-141.69, -681.15, 0.114), rot = 0, scale = 1  (game Z-up coords)**

Island2's gc_island2_longdist.bdae (str#92 @0x58a3a, typeId 0x1869f
CTemplateBakeGroup, pages #93/#94 + 1.0f pairs): TRS = IDENTITY —
island-2 bake geometry is authored origin-relative (no object record).

### 4. Local-frame sharing proved
FP assemblies vs GC_island1_LongDist (54 meshes): per-mesh centroid
correspondence FP1/FP2/FP3 max error 0.5 units (Roads: merged strips,
bbox-identical frame). ONE transform places:
  GC_island1_LongDist, GC_LongDist_Island1_{FP1,FP2,FP3,Roads},
  GC_island1_LongDist_LOW — and island2's five units at identity.

### 5. Validation (Claude's overlap test)
Placed island1 footprints: world bbox x[-818,417] y[-1148,152] (game
coords) — overlaps 8/9 street_island1_* chunks, up to 28k units^2 XY
each; sign checks: +681.15 would yield ZERO overlap with the street
city's negative-y range => (-141.69, -681.15) confirmed.

### 6. Shipped (v13)
- export_city.py: ISLAND_WORLD_OFFSET + LD_WORLD regex; offsets applied
  in game coords before the glTF Y-up conversion; new 'skyline' tier
  (10 GLBs, one per unit); manifest v13 totals now cover all GLBs.
- app.js: TIER_ORDER street+skyline first; skyline boots WITH street.
  Hero bridges/monorail/railway stay research toggles (their own lvc
  records not decoded yet — monorail collision segments ARE placed in
  the placement table: 120 records @ (20.8,-188.3)... etc).

## Artifacts
- extraction/re/lvc_placement_table.json — 1876 records (name, pos, rot,
  scale, offsets). Props/billboards/redlightmesh/monorail segments.
- extraction/ghidra/decompiled_r2/{beast_family_r2.asm, load_next_object.asm,
  create_object.asm, beast_object_loads.asm}
- scripts: lvc_placement_table.py, lvc_hash_transform_scan.py,
  disasm_load_next_object.py, disasm_beast_family_r2.py

## Next (ordered)
1. Decode remaining CTemplateObject variants (0x2661/0x2664/0x1404050/51)
   + CGameObjectManager::CreateObject read order => placements for
   bridges/monorail/railway/hero units (records exist: 120 monorail
   collision segments, billboard roofs, water).
2. batch_info.bin street material index (the ~600 dark near-tier
   segments) — unchanged, blocker B.
3. Ground fidelity split + near-field density (blocker C).
