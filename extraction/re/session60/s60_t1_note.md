# SESSION 60 — T1: template walker REBUILT from the engine GCT dispatcher

## Mechanism (all from disasm, ARM, libKRHP.so v1.1.6b)
- GenerateComponentTemplate 0x368ac0 (11308 B) = pure if-chain, **64 cases**, every case:
  `movw/movt id; cmp r0,r3; beq CASE` -> `mov r0,#alloc; bl _Znwj; ldr r3,[pc,..];
  add r3,pc,r3; add r3,r3,#8; str r3,[r0]; b 0x368bfc` -> common tail
  `ldr r3,[r4]; ldr r3,[r3,#0x10]; blx r3` = **template reader = [vptr+0x10]** (vptr = vtable+8).
- **DEFAULT PATH = `mov r4,#0; ldr r3,[r4]` @0x368bf4 = null-deref CRASH.** All 15 bne defaults
  converge there. GOM::Load (0x365780) and GOM::Reload (0x366104) call GCT for EVERY comp id
  (no flag check, no skip); GOM::CreateObject (0x367fdc) has a `beq -> skip` null-check that
  GCT cannot legally return. => **the engine cannot template-load any class outside the 64;
  there is no skip/empty mechanism.** Records are offset-table framed (GOM::Load seeks
  offsets[i] per record), so leftover bytes inside a record span are never read by GCT.
- Per-comp stream layout re-verified from the Load/Reload loops: (u32 BE id, u16 BE flag) pairs,
  flag stored as bool in TObjectData[+0]; the u16 is NOT a payload gate (flags 0/1 mixed for
  both case and no-case ids; GCT is called regardless).
- Primitives: ReadInt 0x339914 = plain 4-B BE; ReadString = mode-gated (stream+0x34/0x35) but
  the gol path reads a u32 index; readers also do INLINE stream reads (ldrb from [stream_base]
  + pos store [stream,#0xc]) that plain bl-census misses (7-byte prologue reads etc.).

## The 64 GCT cases (id -> reader, all symbols resolved)
64/64 readers resolved to per-symbol bounds. Key members:
0x14ca79 CComponentBase::Load 0x1fe924 = c,i,f*9,c,c,c (44 B) [446 gol uses]
0x152b87 CComponentMesh::Load 0x2d6ddc = STR,c,c,c,c (8 B) [441 uses]
0x365cfd67 (156 uses), 0x2db081e2 CComponentCollision::Load 0x2d72bc = 16-B base flat,
0x0ddcd6c4 CComponentHealth::Load = f,c,i,i (13 B), 0x43c8a8d1 CComponentObjective = STR,STR,i,i,
0x4cc04ddb CComponentBeast_Omni = 34 B, 0x0116a6fa CComponentTrail (2108 B, 10 loops,
spec INCOMPLETE - 'call' inside), 0x54989cb1 CComponentActorBaseComponent::Load =
**7c + 16f + 3c + i + i + n*(i+c) = 82+5n, loop count = the SECOND int** (s58 said 78+5n with
count = first int - corrected from disasm 0x3baee0..0x3bb238).
Hand-verified from disasm (auto-extractor loop-blind spots):
0x5863bd59 CComponentMainStoryQuests::Load = i(n) + n*(i,i,STR,STR,STR,STR,i,STR,c);
0x4ca5f00e CComponentNewShopItemProperty::Load = i,STR,STR,i,i,f,f,f,c,c,c,c,i +
n*(c,i,i,f,f,f,f,STR,STR,STR,STR,i,c,i,c) [= s30 spec, confirmed].
INCOMPLETE (marked, fail closed): 0x0116a6fa Trail, 0x5471c18b MissionsList (3548 B, 28 loops).

## s59 corrections
- "0x14ca79 / 0x152b87 unrecoverable legacy specs" -> BOTH have GCT cases with readers (above).
- "0x0116a6fa trail NO case" -> it HAS a case (CComponentTrail::Load 0x2e5318).
- 63 cases -> actually 64 (the prologue case 0x365cfd67 compares before push; window bug).
- 0x33702f4a -> CComponentDummies::Load 0x2e3940 (not CComponentSniper::Load).
- Awareness 0x6754056b / StateSet 0x5441a117 / Motion 0x592ce07c / CustomizeActor 0x40c6b80a /
  DropCollectible 0x3ef5108d / CVehicleCollision 0x67c82e62 / CBeastSpot 0x4cc07242 /
  CCollectible 0x28091330 / Sniper 0x0e1f5b6f: CONFIRMED NO GCT case (constants appear nowhere
  in .text or data as words) -> engine-unloadable in templates.

## Walk results (closure; walker = s60_t1_walker.py)
- **ENGINE-TRUE (64 engine specs only): 149/653 templates are pure-case** (every comp
  constructible by GCT). Closure: **144/149 bounds-closed (96.6%), 139/149 exact**; 5 NA
  (empty comp lists - engine never walks their payload); 5 legit tails (4,4,4,15,21 B -
  offset-table framing; Base/Mesh/Beast readers verified to have no conditional tails).
- **HYBRID (engine 64 + s30 lvc-instance specs + s58 overrides for no-case classes +
  1 labelled gol-shape correction): 524/653 bounds-closed (80.2%), 393/653 exact (60.2%),
  131 small-tail, 124 fail, engine-cannot bucket 90.**
- Gol-shape correction (data-derived, labelled): 0x59a8390c = 16 B in gol (i,i,STR,i) vs
  s30 lvc-instance 12 B. Evidence: 159 templates with it LAST left exactly +4 tail; adding
  the int flips exact closure 234 -> 393. Consistent with the template/instance reader duality
  (cf. Collision: template 16-B base vs cnt-extended instance). The engine cannot verify
  (no GCT case) - the label stays.
- s58-326 continuity: every s58 blocker resolved or same-cause: Base 445->0, Mesh 441->0,
  Beast_Omni 59->0, Objective 24->0, 365cfd67 156->0, 0e31d4a0 10->0, Gadget 9->0, LEN-MISMATCH
  111->131 small-tails (most now close); UNRESOLVED same as s58: Trail 20, 7d561d33 18,
  CVehicleCollision 14, CustomizeActor 12 (CUST OOB), CBeastSpot 11, CCollectible 10, 2c9a0e3f 8.
- Carrier values (Health f,c,i,i + Awareness 16f at walk positions): 33 bounded-closed carriers
  in two position classes: **NPC carriers (health@121, aware@138) x14, vehicle carriers
  (health@137, aware@154) x19**; all 18 carriers present in s58's receipt match s58's values
  EXACTLY (health + all 16 aware floats) = 18/18. Exact-closure carriers: 8/8 consistent.

## Calibration / nulls
- Calibration basis: specs derived from engine disasm (not fitted); 2 hand-verified readers;
  18/18 carrier value agreement with s58's independent receipt; s58 blocker set strictly reduced.
- N1 spec-permutation (pure set): 118/149 vs real 144 - WEAK by construction: pure templates
  are dominated by fixed-size Base(44)+Mesh(8), so size-collisions survive permutation.
  Documented, not hidden.
- N2 payload rot-7: 142/149 - length-only closure for all-fixed specs (rotation preserves
  length); rep-driven closures are the discriminative subset. Documented.
- The strongest structural check: engine-true pure-set closure 96.6% with zero fitted
  parameters, plus blockers=0 on the 149.

## Artifacts
- s60_t1_gct_extract.py -> s60_gct_cases.json (64 cases, readers, vtables)
- s60_t1_reader_specs2.py -> s60_reader_specs.json (64 specs w/ inline reads + loop forest)
- s60_t1_walker.py -> s60_t1_walk.json (engine-true + hybrid + nulls + fails)
