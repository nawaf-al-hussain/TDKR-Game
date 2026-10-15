# RE Session 25 (round 15) — 2026-10-15

## 0. State recovery

- Sandbox reset again: no clones survived. Remote = source of truth
  (main @ 03ee321 round-13; session-24 commit 39f9c47 survived only in
  download/bundles_s24/main_s24_inc.bundle, verified and fetched — the
  bundle mechanism worked as designed).
- Release zip re-downloaded (SHA256 0510e54c…aa6f re-verified ✓); raw data
  re-extracted (gol.bin 1,270,660 B, both lvc, batman.bdae 450,892 B,
  batman_anims.bdae 43,683,488 B).
- unicorn+capstone installed into the active venv (python3.12).

## 1. T1 — GENERIC LVC RECORD FRAMING: **PASS (engine-driven, byte-exact)**

Method = the Unicorn tracer (extraction/re/session25/lvc_tracer.py):
- libKRHP.so mapped at vaddr under Unicorn ARM with VFP/NEON enabled
  (Cortex-A15 + cp10/cp11 + FPEXC.EN) — the mesh/matrix code is VFP.
- The CMemoryStream fake object keeps buffer ptr @+0x0 and cursor @+0xc;
  the REAL reader functions run natively (ReadInt verified big-endian at
  0x339914: `orr r3, r3, r5, lsl #24` chain) — every consumed byte is
  consumed by engine code, we only LOG the cursor at each reader entry.
- ReadString* run NATIVELY too: the stream dictionary is real memory
  (vector<string*> at +0x1c/+0x20; our dict objects are
  {p,len,cap}+huge-refcount COW blocks the engine's own operator= accepts).
- All 342 imports serviced: .rel.plt/.rel.dyn JUMP_SLOT+GLOB_DAT(undefined)
  GOT entries filled with Python trampolines (malloc/calloc/realloc/
  memalign, mem*/str* family, math, pthread-TLS as a zeroed page,
  __cxa_guard_acquire=1 so EMPTY_STRING's static init runs natively,
  memcpy/memset with a 1 MB clamp, qsort/GL loudly logged and unused).
- Guards that were required to reach completion (each fixes a real
  interaction with emulated-state differences):
  - top-1 MB page @0xFFF00000: COW refcount decrement on zero-init
    strings computes p-4 = 0xFFFFFFFC (glitch string operator= release).
  - NULL-GOT scratch: unresolved singletons deref [0+off] onto the ELF
    header; those 16 bytes are zeroed at map AND re-zeroed per run (a
    CQuestManager list insert through a NULL manager writes them).
  - static COMP_REG (0x53000000): the bump heap is reset per run, so the
    component object must NOT live on the heap (first inner new would
    alias it).
  - magic-page restore per run (Loads write through PARENT/VT pointers).
  - benign-fault classification: a fault OUTSIDE the called function's
    symbol run is post-Load engine bookkeeping (scene-graph, quest
    registration) — stream reads are already complete; the record
    boundary check is the referee.
  - STR-INDEX invariant: the u32 read inside any native ReadString must
    be in [-1, nstr) — this is the desync detector that localized every
    framing bug.

Dispatch is FULLY engine-driven (extraction/re/session25/extract_switches.py):
- CComponentFactory::CreateComponent @0x223e3c switch: 24 classes, each
  news an object and the ctor stores a vtable; Load = [vt+8] (verified:
  0x2db081e2 -> CCollisionComponent::Load @0x2230a8).
- GenerateComponentTemplate @0x368ac0 switch: 49 classes, Load = [vt+0x10]
  (the case stores vt+8; verified: 0x37883208 ->
  CComponentVehicleGears::Load @0x3c40c4). Together with the 72
  load_sym-resolved classes, every stream-loaded component typeId now has
  its real Load address, extracted statically from the engine's own
  dispatch tables.
- Dispatcher corrections from lnobj_full2.asm (each previously unvalidated
  or wrong):
  - 0x2657, 0x2663, 0x2664 have NO dedicated case -> they are GENERIC
    gol-template records. The banked "0x2663 = i,9f" was WRONG; the true
    frame = template [[0x14ca79]=44B, [0x152b87]=8B] = 56 B records (the
    marker clusters), confirmed by the 56-B cluster periodicity.
  - 0x4741 shares the 0x2666 waypoint case; 0x256/0x269/0x24e are ctor
    parameters, not typeIds; 0x11fc6 is an Application-object offset.
  - 0xdbbb8 = CWorldBox(stream) ctor @0x2b56f4 (reads; banked "0 B" wrong).
  - 0x2669 = CWeatherManager loader @0x40e994 (reads; banked "0 B" wrong).
  - 0x2666/0x798f/0x4741 = the dispatcher news CWayPointObject and calls
    the Create thunk @0x2a8220 which virtually dispatches (vtable slot 14)
    to CWayPointObject::Load @0x2a7e58 — the payload is CONDITIONAL
    ([i id][c][3f pos][11 x i32 -1 defaults][i][i], 67-71 B), NOT f,f,f.

Walk result (extraction/re/session25/lvc_walk_emu.py):
- GothamCity.lvc: 20,767 records, cursor end 0x5eb80b == table offset,
  complete=True, ZERO failures.
- GothamCity_Island2.lvc: 18,705 records, end 0x547281 == table offset,
  complete=True, ZERO failures.
- 100% byte coverage (the banked parse reached 874/14,917 = 3.3% with
  ~10 hand-decoded classes; the emulator needs no hand formats at all).
- Cross-validation: ALL 873 banked-verified record boundaries reproduced
  1:1 (the banked parse stopped inside a 0x264a record the emulator
  parses fine).
- Positive controls exact: 0x2662 spawn objId=2000108
  TRS=(-140.692, -681.189, 0.114); 0x14051 mesh record
  gc_island1_longdist.bdae TRS=(-730, -1250, 0).

Censuses (extraction/re/session25/t1_deliverables.json + t1_lua_*.json):
- Collision: GothamCity 794 components = 794 prims = 137,893 triangles;
  Island2 444 components = 133,696 triangles (max prim 15,354 tris).
  Named triangle-soup surfaces, 9f+u8 per triangle — the collision mesh
  for the walkable world is now a decodable database (271,589 triangles).
- Trigger -> Lua: 437 + 254 trigger components, EVERY one carries an
  inline Lua script through the interned string index — 560,404 B of game
  Lua extracted (occluder show/hide on enter/exit, per-district
  color-correction + global-illumination switches, the full NPC
  population state machine: SpawnObject/MoveGroup/ActorSetState/
  NPCAttackTarget/ShowMessage with string tables). This is the script
  ownership map the briefing asked for.
- Spawns: 222 + 92 (all name=batman.bdae — these are PLAYER spawn
  points; NPC spawns are driven by the Lua layer).
- Mesh records: 43 + 19 (gc_island1_longdist skyline + footprint
  reflection planes with world TRS).

## 2. T2 — BATMAN SKIN: **PARTIAL (engine-driven evidence banked)**

- **The attribute registry is now fully enumerated** from the engine:
  glitch::video::getStringsInternal(E_VERTEX_ATTRIBUTE*) @0x7ae7a4 returns
  the name table @vaddr 0xc12318:
  0 Position, 1-15 TexCoord0-14, 16 Normal, 17 Color0, 18 Color1,
  19-22 Tangent0-3, 23-26 Binormal0-3, **27 SkinWeights, 28 SkinIndices**,
  29 InstanceId. The briefing's open question (blend-index/weight
  attribute ids) is answered: 27/28.
- Loader chain mapped (symbols): glitch::io::loadMeshBuffer @0x8e104c ->
  CColladaDatabase::CColladaDatabase(IReadFile*, bool, CColladaFactory*)
  @0x7ba83c -> CResFileManager::get (a filename-keyed cache with
  glf::Mutex/ReadWriteMutexLock/Condition threading) -> parse. The
  database ctor ALWAYS routes through the resource manager, so full
  database emulation needs the cache bypassed (next step: call the
  cache-miss parse function directly).
- Skin technique classes mapped: CHardwareMatrixSkinTechnique::init/skin
  @0x7cbbfc/0x7cbc40, CSoftwareSkinTechnique::init/skin @0x7cc234/0x7cc600,
  SSkin/SSkinBuffer; getProcessBufferConfig returns {2,2,false} (two
  process buffers).
- batman.bdae mesh-section header decoded (offset 0x4a68):
  [7 u32 signature-ish 0x100,0xf8,0x40,0x34,0x28,0x1c,0x10][1]
  [count=1449][8]
  [5 x (u32 offset, u32 8) = (0x4c,8)(0x64,8)(0x7c,8)(0x94,8)(0xac,8)]
  [0xf8][0][1][data 0x1c5bc B]
  vertex data starts with TWO position-like triples per vertex
  (-0.6065,-0.2083,-0.0006 then 0.606,0.1544,1.916 = the head vertex),
  stride 80 = 2 x 40-B halves as established in session 24.
- A bdae database harness exists (t2_bdae_harness.py: fake IReadFile with
  read/seek/size vtable over the real file, attribute-id hooks on
  CVertexStreams::getStream / CAppendMeshBuffer::configureStream) — it
  runs the ctor but hits the resource-manager threading layer; the
  cache-miss bypass is the next session's first move.
- NOT yet decoded: the exact per-vertex SkinWeights/SkinIndices packing,
  the -mesh-skin per-bone inverse binds, the node hierarchy parent table.
  VERDICT: PARTIAL — the engine-driven foundation (registry + loader +
  skin technique symbol map + harness) is banked; the decode continues
  from the cache-miss parse entry.

## 3. T3 — one animation clip: untouched this round (user priority was T1
then T2). Status unchanged from session 24 (HARD: descriptor zone located,
needs section-base rebasing).

## 4. T4 — housekeeping: live gh-pages remains v17 @ f22b098; staged v19 on
gh-pages-staged @ 9a9fb3b (pushed round 13). No viewer changes this round.

## 5. Claim status changes

- "3.3% exact parse / ~10 undecoded component classes" (session 24) —
  SUPERSEDED: 100% byte-exact via engine emulation; the per-class Load
  addresses come from the engine's own factory/GCT switches, not hand
  disasm.
- "0x2663 = i,9f" (banked dispatcher table) — REFUTED: no dispatcher case
  exists; true frame 56 B via the gol template.
- "0xdbbb8 / 0x2669 / 0x256 / 0x4741 / 0x11fc6 read 0 B" — REFUTED for
  0xdbbb8 (CWorldBox) and 0x2669 (CWeatherManager loader); 0x4741 is a
  waypoint (conditional payload); 0x256/0x11fc6 are not typeIds at all.
- "0x2666/0x798f = f,f,f" — REFUTED: CWayPointObject::Load is conditional.
- "collision prims are named triangle soups" (session 24) — CONFIRMED at
  scale: 271,589 triangles across 1,238 components on two islands.

## 6. Deliverables this session

Scripts (in-repo extraction/re/session25/): lvc_tracer.py, emu_services.py,
lvc_walk_emu.py, extract_switches.py, t1_summarize.py, so_symbols.py.
Artifacts (in-repo): so_syms.json (61,324 symbols), gct_switch.json,
factory_switch.json, t1_deliverables.json, walk_rep_*.json,
t1_lua_GothamCity.json (444 KB of decoded Lua).
Local-only: walk_census_*.json (full read traces per census component),
t1_lua_GothamCity_Island2.json, banked_bounds_gc.json.
