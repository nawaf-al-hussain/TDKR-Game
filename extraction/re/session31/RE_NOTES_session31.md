# RE Notes — Session 31 (round 21)

## T1: parser claims tidied

### Spec provenance (canonical table = lvc_readseq_s30.json, 92 entries)
- **STATIC_DISASM 15**: 0x4CA5F00E (@0x202ae4), 0x17AC851F (@0x2dce20+0x2d9118),
  0x3189E053 (@0x1ffa1c), 0x292930B0 (@0x203858), 0x44C835D1 (@0x203764),
  0x2EF26C52 (@0x1feb64), 0xC69A6A7 (@0x2e7430), 0x2AD64F3D (@0x2a0728),
  0x2888019A, 0x39E32181, 0x7F88E44E, 0x10FCFD6 (@0x22a368), 0x14CA79-class,
  0x152B87-class, 0x2AD2A046-class.
- **ENGINE_CASE 2**: 0x2657 (LevelInit @0x2018f0+0x2023bc), 0x798f (waypoint).
- **LOOP_VERIFIED 5** (hand-derived, byte-verified on every island record):
  CCollisionComponent, CSmartLightComponent, CSoundAndLight, NPC-pos-list,
  CActorBaseComponent.
- **FITTED_ISLAND 52** (40 component + 12 dedicated): token patterns harvested
  from the GothamCity+Island2 walks, one pattern per class, no per-level bytes.
- **ZERO_READ 10**: unregistered classes (CreateObject null-check).
- **FITTED_TEST 7** (dead hex-format keys, Test.lvc raw-N spans, r17) + REC
  pseudo-entry.
- **Removal experiment**: dropping the 40 fitted component specs stops every
  level at its first fitted class (BatCave rec8 0x729EC572, l_menu rec6
  0xF5F8CFD, Stadion rec15 0xDFE2718, Police rec7 0x2CA13C06, StockEx rec3 /
  Underground rec23 / ThePit rec34 0x37F7A8AE, Military rec5 0xDDCD6C4,
  shop rec122 0xF5F8CFD). Union over the 8 non-island levels = **31 fitted
  classes validated outside the islands**. Dedicated specs are load-bearing
  (their tids are dual-registered as gol templates; removal mis-frames).
- Known-fitted ancestors retired: 0x16F31 head/body -> static since s30;
  0x7F8ED4E/0x288AE7DA fits were s29-pipeline-only and are NOT in the
  canonical table.

### shop tail + loop bound
- Junk region 0x3cf0..0x40ec = exactly 1,020 B = 255 aligned 4-B words of
  skip-tids; the final "tid" starts at 0x40e9, straddling table_off (3 junk
  bytes + 1 string-pool byte) -> +1 overrun (354 "records").
- LoadRawLvl @0x489100..0x48957c disasm: header ReadInt @0x4891f8 -> r6 never
  consumed (discarded); the whole remaining stream is slurped (rsb+memcpy);
  the record loop exits ONLY when remaining < 4 B (0x489300-18) = **stream
  size bound confirmed**. Islands' native walks ended at table_off because
  s26_engine_walk.py:122 mem_writes table_off into the stream size field
  (harness artifact). Shop's walk (no such overwrite) ran to stream end.
  Conflict resolved: engine bound = stream size; the pure parser deliberately
  bounds at table_off.

### Collision counts reconciled
Correct spec-following re-walk: **GC 794 objs / 137,893 tris** (= r15 = r16
census), I2 444 / 133,696, total 1,238 / 271,589. The r20 export lost exactly
40 tris in 4 objects (idx 770-773, militarylaser_collision.bdae): its token
scan grabbed the prefix [i]=2 as the first prim count -> 12->2 tris each.
Flag delta {6:+48, 1:-8} explained by the same misframing.

### Table generators committed
s26_build_table.py now consumes the distilled input
(s26_v2_walk_patterns.json, 0.19 MB, committed) reproducing the s26 baseline;
s30_build_table.py is repo-relative and regenerates the CANONICAL s30 table
byte-identically from the committed s26 table. lvc_pure.parse returns
complete/final_cursor instead of asserting.

## T2: Batman skeleton + skin mapping SOLVED (verdict PARTIAL, upgraded)
- bdae node records decoded: [nameA '-node'][nameB][alias 'BoneNN'|'']
  [t xyz][q xyzw unit][s xyz][u32 1][childCount][firstChildPtr], 107 nodes,
  66 BoneNN aliases; the 67 Bip01 nodes + dummies/attachments.
- Skin palette @0x3167c = 31 x 8-B 'BoneNN' records; **palette[k] = skin id k
  (0-based)**; r20's "ids 1..30, 30 distinct" was an `if b` filter artifact
  (id 0 real: 37 verts at w>=0.4).
- Mapping verified two ways: (a) palette BoneNN == node aliases; (b) per-id
  influence centroids land at the named anatomy (id0 R-ankle z0.108,
  id2 R-thigh z0.876, id18 Head z1.707, id22 Pelvis z1.014). Median
  centroid-vs-node-world 31.0 cm vs permuted-mapping null 64.1 cm (20 trials).
- Hierarchy: childCount/firstChildPtr tree + biped-standard parents agree
  with zero conflicts.
- Bind arrays located (orthonormal-affine scan): body 31 @0x30e30
  (palette-ordered; leg steps 0.444/0.405 == foot-calf-thigh 0.450/0.410),
  CAPE 38 @0x5a210 (= Spine1 + 2 clavicles + 35 CBones), CAPE_down 38 @0x675a4.
- Still open: the stored bind arrays' space transform (48-perm Kabsch best
  74 cm) and the fact that the mesh bind pose = T-pose arms vs node default
  A-pose (hand verts x +-0.44..0.58 z~1.1 vs node hands x +-0.34 z 0.66).
- Deliverable: batman_bindpose.glb (1449 verts, 5655 idx, 31 joints, IBMs =
  inverse node worlds -> mesh reproduced exactly in three.js by construction).

## T3: clips (verdict PARTIAL; r20's 93-count corrected)
- Clip list @0x11580 = **921 clips**, 12-B [nameOff, tickStart, tickEnd] over
  a shared key pool; starts rounded up to 1000s (920/920 gaps). Durations
  ms-scale: median 1,339; idle_stand 5,000; walk 666; sit 1,669.
- Tick rate = milliseconds (duration plausibility + the sampler normalizes t
  by a per-clip [sampler+0x58] via vdiv @0x763e20 in
  CAnimatorBlenderSampler::updateAnimation).
- 78 named 32-B groups @0xb53c = clip-1 head block; tOff/vOff point into a
  44-B descriptor-record zone with next-pointers (0x1ea0/0x1ed4/0x1f0c/
  0x1f44) and magic 0x14FFFF = per-channel descriptor chains (resisting
  block; pose test blocked on it). 1,375 = descriptor-zone named-group
  census (r20); r16's 503 = superseded key-run census.

## T4: prototype hardened (verdict DONE for export+numbers)
- Material flags SOLVED: GetCollisionTypeFromMaterialName @0x142e00 walks a
  13-entry name table @0xc0a6cc: 0 GConcrete, 1 GWetConcrete, 2 GMetal,
  3 GWood, 4 GDirt, 5 GWater, 6 Solid, 7 Box, 8 WalkNoNavMesh, 9 Fence,
  10 Stop, 11 SolidNoEdge, 12 BoxNoEdge; 255 = unmatched. Streets =
  GWetConcrete (73% under-probe), shell = Solid.
- Trigger volumes: CComponentTrigger::Load @0x2e0bcc = [i][f x9][i=1.0f]
  [c][STR?]; all 380 GC triggers uniform 118-B records f9=(0, pos, 0, 0, H,
  1, 1), H in 0..18.44; IsObjectInside = projection test vs 4 stored
  3-vectors (default-extent OBB).
- Corrected export: GC 794/137,893 + I2 444/133,696 = 1,238/271,589 (exact
  r16 match); i2_collision.bin new; prototype ?soup=i2 added.
- Spawn field fix: 0x2662 TRS stores (y, z, x, ...) -> pos = (f1, f0, f2):
  99.6% in-bbox, 66.7% within 3 m of ground.
- Multi-grid probes (5 GC grids at the 5 densest 200-m spawn buckets, blind):
  ground 98.4 / 87.3 / 99.3 / 100 / 87.8 %; negative control (GC soup at I2
  centroid) 0.0 %; I2 grid 99.1 %. Slope median 0.0 deg, p95 3.1-63.3 (walls);
  step median 0.00-0.22 m, p95 8.6-24.2 m (rooftop edges).
- Path test: 18 straight spawn->spawn ground-march routes (no wall sliding):
  2 ok / 10 stuck / 6 fell -> straight-line connectivity needs obstacle
  avoidance; falls = the road-gap class.
- FPS: no browser in this sandbox (limitation stated; r19 headless 20-60 fps
  on the 4x-larger visual GLB).

## T5: delivery
- Bundle: download/bundles_s31/main_s31_inc.bundle (8842b35..round 21),
  verified; SHA256 printed at creation.
- Estimate: walkable world IN (both islands exported, ground 87-100%);
  character renderer IN (glTF with joints+weights); animation pipeline
  located-but-open (descriptor chains); Lua shim top-8 family implementable;
  glide/grapple/combat/AI/mission flow/audio/UI OUT.
