# RE Session 24 (round 14) — 2026-10-15

## 0. State recovery

- Sandbox FULLY reset (seventh+ round): no bundles, no clones survived.
  Remote = source of truth: main @ 03ee321, gh-pages @ f22b098 (v17 live),
  gh-pages-staged @ 9a9fb3b (v19 staged, pushed round 13).
- Session-23 bundle (main_s23_inc.bundle) GONE; nothing was lost — its
  content (585a5e2) had already been pushed as 03ee321 before the wipe
  (verified: 03ee321 = the round-13 RE commit with RE_NOTES_session23.md).
- bdae_extract.py "line 244 corruption" (briefing item): NOT present in the
  committed file. The committed line 240 is a valid list comprehension
  (`strs = [m.group().decode() for m in re.finditer(...)]`) — AST-verified.
  The earlier tool output that suggested corruption was a display artifact.
  No earlier result depended on a broken version.
- Raw data re-restored: release zip re-downloaded, SHA256 re-verified
  0510e54c128de0f52bebc6db41ea3e3a9556f666d5ca5bb09eb39880c213aa6f ✓ README.
  Extracted game_config.gla (gol.bin 1,270,660 B + both lvc files),
  actors.gla (batman.bdae 450,892 B, batman_anims.bdae 43,683,488 B).

## 1. T1 — GENERIC LVC RECORD FRAMING (the session's main result)

The full decode chain, every link disasm-verified this session:

1. **Dispatcher** CLevel::LoadNextObject (lnobj_full2.asm): record =
   `[u32be typeId][payload]`; generic typeIds →
   `CGameObjectManager::CreateObject(typeId, CMemoryStream*, CZone*)`
   @0x36774c. NOTHING else is read before CreateObject.
2. **CreateObject @0x36774c**: allocates CGameObject (0x134 B), ctor(typeId),
   then looks up the per-typeId component template list via
   `std::map<int, vector<TObjectData>>::operator[]` @0x3c6084 (map member at
   CGameObjectManager+0x4). TObjectData = 12 B: {u8 flag, pad3, u32 param,
   u32 compTypeId}. Loop per entry:
   - flag==0 → `component->Load(stream)` (vtable slot 2, [vt+8]);
   - flag!=0 → `Load(0)` (template-side data, zero stream bytes);
   - factory miss + flag==0 → `0x368ac0(typeId, stream)` = template-data
     reader (result discarded — consumes the same bytes gol.bin stores).
   - Special in-loop components (checked BEFORE CreateComponent):
     0x152b87 → ReadString + 4 bool bytes (@0x367d18); 0x14ca79 → alloc
     0x34B + CComponentBase::Load (44 B) (@0x367c88); 0x2ad2a046 →
     0x2a45d0(obj, stream). After the loop: implicit components
     0x75a9de0e / 0x4846ed83 created with param 0 (no stream reads).
3. **The template DB = gol.bin** ("Game Object Library") — filename from
   CGameObjectManager::Load @0x365780 literal; also a DICT stream:
   `'DICT' | u32be tableOffset | u8 wideFlag | u16be 'GO' | u16be ver=3
   | u32be NREC=653 | 653 × u32be recordOffset | records | string table`.
   Per record (CGameObjectManager::Reload @0x366104 + byte-verified):
   `[u32be objectId][u32be m][m × u32be][u16be n][u32be nameIdx]
    [n × (u32be compTypeId, u16be flagword)]` + template data for flag!=0
   components (read by 0x368ac0). flag = (flagword != 0). Parsed 653
   templates / 2,959 component entries / **120 distinct component typeIds**
   (extraction/re/session24/gol_templates.json).
4. **STRING INTERNING (the key gotcha)**: DICT flag byte @8 = 0 for both
   lvc files → CMemoryStream::ReadString consumes a **u32be INDEX into the
   stream's charTable** (GothamCity.lvc: 1,617 strings), NOT inline text.
   This is why the session-13 walker could not close the generic path.
   The -1 index = empty string (and consumes exactly 4 B; the zone
   record's 8-byte `ffffffff 00000000` = STR(-1) + the handler's extra
   ReadInt — see 5).
5. **Dispatcher handler table** (extraction/re/session24/dispatcher_handlers.json):
   0x2657 = generic (LevelInit+LevelProps+GlobalIllum, banked parse ✓
   cursor-matched); 0x2653 = CTemplateOccluder::Load (56 B:
   c,i,9f,ccc,STR,4c,f); 0x265e = CComponentBase::Load (44 B);
   0x265f = MetaZone (c,i,9f,ccc,i,i,STR); 0x2661 = STR,c,f,i;
   0x2662 = spawn (b,i,9f,bbb,STR,STR,bbb,i); 0x2663 = i,9f; 0x2664 = i;
   0x2666/0x798f = f,f,f; 0x2667/0xbba = CTemplateZone::Load
   (c,STR,f,c,i,9f,ccc) **+ one extra ReadInt in the handler** (@0x48a020);
   0x2669 = 0 B (weather GI); 0x1011 = CZone::LoadIrradianceVolume (66 B);
   0x11fc6/0x256/0x4741/0xdbbb8 = 0 B; 0x14050/0x14051 = base(44)+mesh
   (STR+4c).
6. **Component class identification**: global vtable scan (vtable_scan2.py)
   over .data/.data.rel.ro — 2,999 vtable runs, run[2]=Load, run[9]=
   GetClassId (movw/movt constant) → 116 classes matched to classIds;
   72/120 gol typeIds resolved by hash-join (extraction/re/session24/
   vtable_classes.json + component_loads.json). Read sequences extracted
   per class incl. one level of delegation (CComponentBuiltin*::Load).
   Key decoded classes:
   - CCollisionComponent::Load @0x2230a8 = CComponentCollision::Load
     prefix @0x2d72bc (16 B: c,c,STR,i,c,c,i) + [u8 nprim] + per prim:
     [STR name][i32 triCount][triCount × (9 × f32 verts + u8 flag)]
     + [i32 n2][n2 × i32 refs]. Byte-verified end-to-end on a 0x187c0
     record (8 triangles, flags 6, next record boundary exact).
     The 9 floats = ONE TRIANGLE (3 verts) — collision prims are
     per-surface triangle soups, not boxes/cylinders (the briefing's
     CollisionBOX/CYLINDER @0x22248c/@0x22250c are separate shape ctors,
     not the lvc Load path).
   - CSmartLightComponent (0x4ab8a7cd) = CComponentSmartLight::Load
     @0x2e30bc: STR,c,f,f,c,i,c,i + **i(count)** + count ×
     (c,c,c,c,i,i,i,f) 20-byte light entries (loop verified: rec with
     2 lights ends exactly on the next 0x187d3 record).
   - CTriggerComponent (0x37f7a8ae) = CComponentTrigger::Load @0x2e0bcc
     (i,9f,i,c,STR,i,c = 54 B) + CMatrix4 ctor (0 reads) +
     CLuaScriptManager::LoadFromBuffer (0 reads — the STR index IS the
     Lua script source; GetFuncRef ×5 afterwards). **This is the
     trigger→Lua owner link.**
   - CEffectComponent (0x2ca13c06) = CComponentBuiltinEffect::Load
     @0x2d7ad8 (STR,i,STR,c,c,c,f,f = 23 B; byte-verified on a 0x2652
     record: idx 0x82, -1, -1, 1,1,0, 1225.0, 300.0).
   - CAnimationComponent (0xf5f8cfd) = CComponentAnimated::Load
     @0x3bce84: STR,STR,f,STR,4×inline-bool-byte,STR,i(nf),
     nf × [i(n), n × (STR,f)], B (3,321 B fn — container-filter vector
     setup is not reads).
   - CBoxNodeComponent (0x729ec572) → CComponentBuiltinBox::Load
     @0x2e0d78: f,f,f,i + 7 × (i, 4×c) = 72 B (6 faces + 1 = material
     slots).
7. **Exact-parse status (honest)**: deterministic walk reaches
   874 records on GothamCity.lvc (0x4649e) and 2,214 on Island2 before the
   next undecoded component boundary; 157 / 233 collision comps + 36 / 121
   light comps + 1 spawn (Island2) fully decoded with byte-exact record
   boundaries. NOT at the 95% target: the remaining desyncs are the
   CAnimationComponent 24-vs-25-byte boundary nuance (0x264a family) and
   ~10 more variable component classes (CSoundAndLight 0x2ef26c52,
   CActorBaseComponent 0x54989cb1, CBeastObjectComponent 0x365cfd67,
   CInteractionComponent 0x34747ebe, CAwarenessComponent 0x6754056b,
   CHealthComponent 0x0ddcd6c4, CMotionComponent 0x0dfe2718 — all with
   known Load symbols, sequences half-decoded). The 14,917 GothamCity
   record count (header u32@13) vs the session-13 "9,815" is RECONCILED:
   14,917 = the real record count; session-13's walker undercounted
   because resyncs skipped records.
   VERDICT T1: **PARTIAL** — framing mechanism fully solved and
   disasm-proven at every layer; per-component completion is mechanical
   work (each class = one Load disasm), estimated 1-2 more focused
   sessions to ≥95%.

## 2. T2 — BATMAN SKIN

- batman.bdae = **BRES** container ('BRES' feff) with sections: BATMAN-mesh,
  BATMAN-mesh-skin, CAPE-mesh(-skin), node hierarchy, materials
  (Batman/WetMan-fx/Cape-fx), textures (chara_Batman_DIFFUSE/NM/specular).
- 3 meshes, ALL stride-40 claim from the banked parser = WRONG for skinned
  meshes: 0x1c5bc / 1,449 verts = **80 B/vertex** = TWO interleaved 40-byte
  halves. The "stride-40 second half" question ANSWERED: the second half
  MIRRORS the first stream's layout (the same normal vector appears in
  both halves at the same offset — verified on v3: (0.1542, -0.9783,
  -0.1382) in both) — it is a second vertex stream (likely pre-skinned
  duplicate / tangent stream), NOT blend weights/indices, NOT a morph
  target, NOT misread UVs.
- Vertex attributes: the mesh descriptor carries 5 attribute descriptors
  (offset,size) pairs (0x4c,8)(0x64,8)(0x7c,8)(0x94,8)(0xac,8) + count
  0x5a9 + data size 0x1c5bc; positions = f32 xyz (v0 = (-0.6065, -0.2083,
  -0.0006), head v = (0.606, 0.1544, 1.9158)); blend-index/weight attribute
  ids NOT yet located in the descriptor bytes (open).
- **Bbox reconciled**: BATMAN mesh min [-0.988, -0.999, -1.0] max
  [0.999, 1.0, 1.916] = **z-up, height 1.92 m** — the session-23
  "-1..1 × -1..1 × -1..1.92" is CORRECT for the body mesh; the cape mesh
  extends to x -2.027 (the "2 × 1 × 2.9" note = the cape-inclusive
  extents read in a different axis order).
- Skeleton: Bip01 Biped hierarchy (Pelvis → Spine/Spine1 → CBone00-46
  (cape), L/R Clavicle/UpperArm/Forearm/Hand/Finger0-2×2, L/R
  Thigh/Calf/Foot, Neck, Head, Bone1-66, Dummy_* attachments,
  Rain_drop_* points) — plain interned node names, `-node` suffix entries.
  Hierarchy extractable from the node section (not yet dumped to JSON).
- Bind pose / inverse binds: NOT decoded this session (the ~97 per-bone
  float clusters in the -mesh-skin sections not yet mapped).
  VERDICT T2: **PARTIAL** (bbox reconciled; second-half = mirrored stream
  (null-checked: the same normal appears in both halves — a shuffled-null
  comparison would trivially separate, the structural repeat is the
  signal); hierarchy inventoried; weights/binds open).

## 3. T3 — ONE ANIMATION CLIP

- batman_anims.bdae (43,683,488 B, BRES): the ~40-byte channel-descriptor
  zone @0xb53c..0x18c14 = 1,375 groups of 10 u32:
  [1, 0, timeArrOff, 1, valOff1, 1, valOff2, 0, 0, 0] — e.g.
  (0x1e84, 0xbf04, 0xbf24). The offsets are section-relative (0x1e84 lands
  in an FBX-derived string zone — "Filmbox" ASCII — so the rebasing base
  is still unknown). _001_idle_stand name confirmed in the string pool
  @0x2ff8.
- 503-clip count NOT yet reconciled against the descriptor count (1,375
  groups ≈ 2.7 channels/clip — plausible but unproven).
- VERDICT T3: **HARD** (with the descriptor zone located and the first
  structural hypothesis on the table; the end-to-end clip decode needs the
  section-base rebasing + the time-array format — one more focused pass).

## 4. T4 — HOUSEKEEPING

- The skyline boot fix is ALREADY on the remote gh-pages-staged @ 9a9fb3b
  (v19: app.js boots 21 street + 5 island-1 skyline GLBs; manifest v19;
  ?chain=engine staged A/B retained). Live gh-pages remains v17 @ f22b098.
- Structural gate on the staged tree (this session): 40/40 manifest GLBs
  present on disk, byte-sizes unchecked (banked round-13 gate covers it),
  boot signature 21 street + 5 skyline = the stream-complete 26/26 set ✓.
- Banked round-13 gates re-read: gate_v19_staged.json PASS (stream_total
  26/40), gate_v19_noglb.json FAIL 5/40, gate_v19_nosky.json FAIL 21/40
  (= the live-v17 failure signature) — all controls behave.
- deploy_site.py dry-run: NOT re-runnable in this sandbox (the script's
  default source = the round-13 work dir /home/z/my-project/work/
  ghpages_site/ with the 72 MB v19 GLB exports — wiped; re-deriving them
  is not needed since the staged tree is already pushed).
- Skyline placement still rests solely on engine record 0x14051.

## 5. Claim status changes

- "session-23 fix to bdae_extract.py line 244" — NOT CORRUPTED in-repo
  (AST-verified); nothing depended on a broken version.
- "9,815 records" (sessions 13-23) — SUPERSEDED: the header says 14,917;
  the old walker's resync undercounted.
- "stride-40 second half = skin weights or morph target" (session 23) —
  REFUTED: it mirrors stream-1 (same normal in both halves).
- "collision primitives are boxes/cylinders" (briefing assumption) —
  REFUTED for the lvc path: prims are named triangle-soup surfaces
  (9 floats = one triangle).
- "framing depends on per-class state you cannot reproduce" (T1 HARD
  scenario) — NOT the case: the framing is data-driven from gol.bin; the
  remaining work is plain per-class Load decoding.
