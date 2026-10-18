# Session 37 (round 27) notes

## State
- Pushed at session start: main fbc1d8e, gh-pages df7b0f7 (v20 LIVE),
  gh-pages-staged df7b0f7, essentials-s36 branch 7c8defc. Remote was ALREADY
  current when this session opened (rounds 17-26 were pushed at the end of the
  previous session with the user PAT; the brief's "last known 8842b35/f22b098"
  was stale). Push attempt with environment credentials failed as expected
  (git push origin main: "could not read Username for 'https://github.com':
  No such device or address" - no GH_TOKEN/gh/credential helper); the
  conversation PAT pushed essentials-s36 (new branch) and verified up-to-date.
- This session's commits: 1628415 (T1), 5331367 (T2), 3036505 (T3),
  ec92422 (T4), 6e733d1 (T5), 3bfbe00 (T6), + notes/T7.

## T1 navmesh cross-region - CLOSED (three independent signals)
- FILE: 0/64,204 cross-region n-links (shuffled-label null 51,166; random-label
  expectation 51,199). Distinct region ids = 1,021 = header field, in BOTH id
  spaces (cells and grid node lists; union 1,021; zero ids >= 1021; 7
  single-cell regions; top region id 1 = 14,059 cells). The brief's 1,035
  DOES NOT REPRODUCE from any file structure.
- WRITER HUNT (whole binary, corrected scanners): no writer for nova+0x5c/0x60.
  All 559+514 str-imm sites context-checked (ctor 0-init + dtor + [sp] stack
  slots + other objects: CNavMeshQuery has its own +0x5c, 0x410-B class). No
  add-rn-0x5c/0x60+memcpy. MOVW/MOVT + literal-pool refs to 0xc16e48/4c/54 =
  ZERO, and the brief's "global region vector" is REFUTED by symtab:
  0xc16e4c = gWanderSwitch(1B), 0xc16e50 = neighbors(12B), 0xc16e60 =
  CNavMeshNova::m_cellsIdsBuff. Load sequence = new(0x68) -> ctor -> Create
  @0x48afe4 -> SetNavMesh @0x48aff0, nothing else.
- READER DECODED: CanReachCellFrom(a,b,flags) = same-region?1:binary-search
  over pair entries {u16 regionA, u16 regionB, u32 flags-mask} (tst flags,mask)
  - a per-pair FLAG mechanism, not adjacency. SearchPortalPath @0x1d48b8
  inlines the same search as a precheck and REJECTS all cross-region queries
  when count=0. CanReachCellFrom: 0 direct bl callers + 0 literal-pool refs.
  EnablePortal/DisablePortal Lua = bool toggle at +8 of a NAMED portal OBJECT
  via registry lookup @0x2b5490 - a different gameplay-portal system.
- VERDICT: cross-region movement impossible in the shipped build - no data
  edges + no table writer + gate rejects empty table. Mechanism exists
  (level-gated region unlocks), unpopulated and uncalled.
- ROUTES: follower 8/40 -> 12/40 ok (timeout 11->0 via A*-proportional budget;
  spawn_blocked 2->0 via 2.0 m ring snap; 8-dir slide + 3-slide grace; sub-step
  climbing). Remaining failures COLLISION-layer, classified: stuck_wall 15,
  step_too_high 8, fell 3, no_ground 2 (clearance-aware waypoint variant
  tested, zero change, frozen). Nulls: shuffled OD 20 cross/14 same vs real
  spawn pairs 24 cross/10 same.

## T2 triggers - independent null (Lua-script ARGUMENT positions)
- Independent positions = object ids passed as ARGUMENTS in the 541 scripts
  (76 call-arg pairs; 46 with known position; 40 unique ids) - pairing driven
  by script logic, not spawn construction.
- RESULT: Lua-arg inside-rate 0.750 (30/40) vs street 0.002 = 500x;
  SHUFFLED-position null = 0.875 >= real -> per-object association NOT
  established; honest claim = "script-referenced objects live in trigger-dense
  areas". Spawn positive control 0.077 (1/13, consistent with r26's
  13.3-13.8%) -> script-reference association ~6x stronger than spawn
  construction. SENSITIVITY: split 5/10/20 -> 0.625/0.750/0.825 (enrichment
  1250x/500x/97x); height default 10,000 vs 50 and rotation: ZERO effect.
  small n=322 (r26 said 340; scale-field accounting noted).

## T3 animation - per-class rates, error attribution, anim_pack verdict
- SIGNATURE battery per-class (verbatim replay; totals reproduce 246/174):
  idle 92/120, walk 38/46, jump 21/24, turn 5/6, fall 7/15 (6 = loop net-z by
  design), run 11/35 (17 = NPC/enemy variants); 25 decode-untestable
  (code-driven roots; joint channels fine); every fail cause-tagged; 12
  name-pattern-unexplained listed.
- FK GAIT per-class (verbatim left-foot criteria; totals reproduce 43/154):
  walk 19/79, run 24/75; criterion-level breakdown shows the battery
  UNDER-DETECTS running: _008_run fails ONLY anti-phase (anti0=0.072, flight
  phase; acR=0.629, foot z>1.1 m are the run evidence) and _022_sprint
  likewise - CORRECTS r26's "canonical set all pass" claim.
- THREE.JS ERROR ATTRIBUTED WITH NUMBERS: numpy FK dual-mode (true slerp vs
  nlerp): idle 0.0, walk 0.0005, run 0.0027, run_jump_start 0.0319 cm max
  (steepest adjacent-key omega 1395 deg/s), jab 0.0001 cm; three.js
  FORWARD-ONLY fresh-state (new mixer per t, ascending t; 434 evals) vs
  numpy-SLERP = 0.0000 cm worst on all 5 anims -> three.js == slerp ==
  numpy-slerp; the r25/r26 0.088 cm residual = numpy-was-nlerp + PropertyMixer
  backward-time path-dependence (2.87 cm probe artifact). NOT scale, NOT a
  channel, NOT a seam. (Caveat banked: the s37 fk_mode t/1000 scaling samples
  near-rest micro-times; the r36 protocol numbers stand; a clip-local-seconds
  resweep is the named next step.)
- ANIM_PACK bindings: state-name strings 0 hits in both bdaes; LE-u16 window
  scan (>=3/4 target clip indices) = 3.963% of offsets == 3.993% random-null
  base rate -> all noise, no detectable u16-index surface. Per-node bindings
  UNDECODED; machinery fully symbolized (SAnimationGraph/SNode/SWeightTable/
  CBarycentricGrid2D/SAnimationSurface; CAnimationPackage ctor @0x75d9c0;
  getGraphNodeId @0x75fe00) - named next step: parse SAnimationPackage headers.

## T4 browser pipeline second slice - PASS (with a visual-bug finding)
- HEADLESS CHROMIUM (playwright) from the REAL 895 MB release zip via File
  input: 164 entries 0.7 s; commons.gla 114 chunks; actors.gla 113; batman
  1449 verts; 663 segs / 921 clips; 921/921 clips nch exact, valsum worst
  rel-diff 1.782e-15; total 1.4 s, heap 949 MB, 0 errors.
- TEXTURE header decoded: [+0 u32be 0x34][+4 u32le w][+8 u32le h][+12 fmt]
  [+20 u32le datasize][+24 bpp][+44 'PVR!' magic][+48 u32le 1]. Size law
  EXACT: fmt-0 = RGB888 no-mips; GC = PVRTC 4bpp full-mip 8-B-min chain
  (43,704 / 174,776 byte-exact). Engine truth: PVRTCDecompress @0x746e34
  called UNDER UNICORN on Gargoyle mip0 (RGBA banked; 2.7x structure over
  shuffled null; partial-execution flagged). Python PVRTC decode 0% exact vs
  engine = declared gap (oracle banked). Batman DIFFUSE RGB888: python and JS
  decodes BYTE-IDENTICAL (1,048,576 px).
- shop.lvc divergence REMOVED: lvc.js accepts only the documented 0xFFFFFF00
  end-of-data sentinel (cursor table+1; unsigned-tid fix - JS read it as
  -256); 12/12 levels JS==Python; parity 14/14 maintained.
- PIPELINE BUG FIX: readBdae palette tag branch was inverted (python takes
  blk[0:2] when blk[4:8]=='Bone') -> jointNodes were all-NULL; now resolve;
  pnameOf chains correct; digest unchanged.
- PIPELINE-ONLY PAGE gh-pages/playable/pipeline.html: user zip -> pipeline ->
  in-memory GLB (corrected r34 hierarchy via pnameOf+BIPED; per-track tick
  dedupe + time normalization) -> GLTFLoader -> skinned mesh + idle/walk/run
  crossfade + WASD capsule (flat ground this slice). Chromium: READY 1.4 s,
  clips 5.00/1.12/0.72 s, 0 errors. VISUAL = visual, unquantified, known
  issues: dark shading (texture colorspace/UV), spiky triangles (tail overrun
  index trimmed; more), facing pivot.
- MAJOR INCIDENTAL FINDING: the SHIPPED batman.glb renders LYING DOWN in a
  plain y-up three.js viewer (raw rig z-up; rotation never applied; all prior
  verification was headless/numpy-side). rotation.x=-PI/2 now in the pipeline
  page; MUST be ported to the shipped playable page.

## T5 Lua behaviour - 30/30 IDENTICAL call logs
- 30 OnEnter+OnReach scripts (15+15): fengari vs REAL Lua 5.1 (lupa), identical
  stubs, identical log format, coroutine-resumed on both sides. After fixing
  the 5.1 Wait logging wrapper, 30/30 call sequences IDENTICAL (names, values,
  types, order). The 5 earlier diffs were all the harness artifact (missing
  Wait row).
- MC_MAX_DISTANCE true value: NOT EXTRACTED (two-signal negative): zero
  references to the name string @0xb30948 by pointer/relocation/GOT/pool/
  pc-relative anywhere in the binary + zero definitions in the 541 scripts.
  ASSUMED=10.0 stands declared; next step: tracer-hook lua_setglobal or
  reverse the script-manager name-table format.

## T6 cape - CLOSED VIA THE ENGINE TYPE TABLE
- E_VERTEX_ATTRIBUTE_VALUE_TYPE (from the binary's own tables): Byte(1),
  UByte(1), Short(2), UShort(2), Int(4), UInt(4), Float(4) - NO half-float
  type exists -> no loader path can emit an f16 vertex stream (closes the r37
  f16 branch by engine evidence). Attributes include SkinWeights/SkinIndices.
- CAPE VERDICT (three independent grounds): engine Load = cloth-only (r25/26);
  f32 strides 20-64 scan clean (r37); engine type table has no format the
  scan missed (this round). Cape = runtime cloth, generated.

## T7 estimate (unchanged + upgraded)
- IN: walkable world, character renderer + 5 verified anims, Lua shim
  (541/541; 30/30 behavioural identity), positional triggers with REAL
  volumes, browser asset pipeline slice (zip/gla/lvc/anims/skin/texture-id,
  browser-verified from the user's own file), navmesh cell graph + per-region
  pathing, pipeline-only playable page.
- NOT IN: cross-region navmesh movement (engine-closed), cape cloth
  (engine-closed), glide/grapple/combat/AI/mission flow/audio/UI, anim_pack
  state bindings, MC_MAX_DISTANCE true value, exact PVRTC decode in JS/py
  (oracle banked), collision-ground in the pipeline page (flat ground slice),
  correct visual orientation in the SHIPPED playable page (z-up finding).
- First playable milestone the evidence supports: walk-as-Batman driven by the
  user's own OBB in-browser (pipeline.html slice) with verified animation
  data; the shipped playable page needs the z-up rotation port + texture
  colorspace pass to look right.
