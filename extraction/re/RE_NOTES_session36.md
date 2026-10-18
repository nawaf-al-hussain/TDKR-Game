# Session 36 (round 26) notes

## State
- Remote unchanged (push still pending): main 8842b35, gh-pages f22b098
  (v17 live), gh-pages-staged 9a9fb3b. TEN rounds (17-26) now exist only in
  sandbox bundles.
- Local main after this session: 8b0cfbb (924c4af T1, c0eac46 T2, b435d1c T3,
  7de39d6 T4, 704bc27 T5, 8b0cfbb T6 on top of b143711).
- Bundles: download/bundles_s36/main_s36_inc.bundle (incremental, requires
  8842b35) + bundles_s36/essentials_s36.bundle.

## T1 navmesh - PASS (engine-driven; the zone is not portals)
- CNavMeshNova::Create @0x1d17cc ran on the REAL .nm under Unicorn: final
  cursor 1,208,898/1,208,898 BYTE-EXACT (GothamCity); BatCave 55,629/55,629.
- Layout (engine read order): [u16 vcount][soup][u16 regionCount][u16 ccount]
  [cells 15-B][u16 0][u8 gridClass][grid]. vcount = 30,824 (r25's 30,905 =
  float-scan overrun). regions = 1,021 = engine regionCount field. cells
  31,647; links 64,204 directed, symmetry 1.0000.
- The "portal zone" @0xce337 = [u16 0][u8 class][cell-lookup grid]
  [nx=222][ny=122][4 f32 bbox][27,084 x [u8 N][N x [f32][u16 region]
  [u16 count][count x u16 cells]]] = 18,846 per-region node lists. Parse
  byte-exact on ALL 10 .nm files (slack 0).
- Portals = DERIVED shared edges (GetPortalId = ordered vertex pair);
  315/315 midpoints on both cells' edges vs 2/315 random null.
- CROSS-REGION IMPOSSIBLE BY DESIGN: CanReachCellFrom pair table nova+0x5c
  = NULL after Create, no writer in the binary. 24/24 cross-region pairs
  classified by design; same-region A* 41/41 pathed; follower 8/40
  (collision layer, classified).
- Grid nodes validated: 392/400 query cells in their own region list.

## T2 triggers - PASS (extents data-determined)
- OBB template (GOT 0xc07f70 -> 0xc585b8, .bss 64 B) = IDENTITY 4x4, writer
  = init[42] @0x74eb30 (isolated by running all 54 init_array entries).
- Extents = CTriggerShapeAABB @0x24a4c0: half = 0.5 * size.x/y, height =
  size.z or 10,000.0 default; size from CComponentBuiltinBox::Load (3 f32).
- 484 box records (78.5% exactly 1x1x1); null: small triggers 13.3-13.8%
  spawns-in vs 0.4% street-in = 33-39x with NO fitted constant; 100 large
  triggers = district zones (99.9% x/y coverage).
- Playable page updated: patch.json t.half, index.html data-determined test.

## T3 animation - PASS (name-keyed + attribution)
- Name-keyed battery 921 clips, 16 classes + 227 transitions: 174/246
  signature-tested pass; failures listed with causes (code-driven roots,
  loops, overlay idles).
- FK gait battery (r25 machinery) over all 154 walk/run-named clips: 43/154
  pass ALL criteria; failures = compound-name transitions/overlays.
- three.js worst-error 0.0884 cm ATTRIBUTED: data continuous (numpy smooth
  across seams; chunk-boundary disagreements <= 0.135 deg, root exact);
  fresh-state three.js matches numpy; 2.87-cm probe artifact = PropertyMixer
  path-dependence on backward time; residual = nlerp/slerp micro-diff in the
  jump clip's steepest segment.
- batman_s36_anims.glb: idle/walk/run/run_jump_start/jab_combat (5 anims).
- State table: Lua states + clip families; mechanism = CAnimationGraph from
  the bdae anim_pack (per-node bindings = format undecoded, declared gap).

## T4 cape - PASS (f32 strides closed; engine evidence decisive)
- Sweep strides 20-64 x f32/f16/u16: f32 survivors only in known table zones
  (gap-zone floats, tail binds tables); controls stride-selective
  (0.423 / 0.092 / -1.0). Quantised formats not fully excludable by scan.
- Engine (r25) remains the proof: Load = 27 floats + 1 int, no vertex reads.

## T5 pipeline - PASS (14/14 node-vs-python)
- tdkr_pipeline.js: zip (EOCD+CD, store+deflate-raw via DecompressionStream,
  verified on the real 164-entry release zip), .gla (pool-relative names,
  fixed), lvc (lvc.js), anims decoder, skin reader, texture identify.
- 11/12 islands byte-exact lvc; shop = end-of-data sentinel note; Test =
  python-side anomaly. 663-seg digest byte-exact; 921/921 clips (worst rel
  diff 1.78e-15 = summation order); skin digest byte-exact.

## T6 Lua - PASS (541/541)
- 19 r25 errors fixed (10+2 APIs, 9 x MC_MAX_DISTANCE=10.0 ASSUMED declared).
- fengari vs real Lua 5.1 (lupa.lua51): 10/10 OnEnter call logs IDENTICAL.

## Estimate (unchanged + upgraded)
- IN: walkable world, character renderer + 5 verified anims, Lua shim
  (541/541), positional triggers with REAL volumes, browser asset pipeline
  slice (zip/gla/lvc/anims/skin all node-verified), navmesh cell graph +
  lookup grid + per-region pathing (A* 41/41).
- NOT IN: cross-region navmesh movement (impossible by engine design),
  cape cloth (generated), glide/grapple/combat/AI/mission flow/audio/UI,
  anim_pack state bindings, MC_MAX_DISTANCE true value, FPS evidence.
- First playable milestone the evidence supports: walk-as-Batman on Gotham
  collision ground with idle/walk/run blending, REAL data-determined Lua
  trigger volumes firing mission scripts, and the same asset path running
  in-browser from the user's own OBB (pipeline slice verified).
