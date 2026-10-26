# SESSION 61 — T1: the id-space question RESOLVED (the engine loads ALL 653 templates)

## Headline
s60's "504 of 653 templates hold component ids the engine could not load" was a
**disassembly artifact**. GenerateComponentTemplate (0x368ac0..0x36b658) is a binary-search
compare tree split across TWO code islands ($d literal pools at 0x369ab8 and 0x36b658 stop
a naive linear capstone pass - s60's "64 cases" counted only island 1's movw-fed compares).
With restart-on-invalid disassembly + raw movw/movt/mov+movt immediate scanning:
**all 120 distinct component ids in gol.bin have GCT cases** (s60 found 65; the miss was
island-2 compares + `mov rX,#imm8` low-halves, e.g. 0x222500f6's case at 0x368be4 uses
`mov r3,#0xf6; movt r3,#0x2225`).

## T1(a) - the "object-id filter" dissolves
GOM::Load (0x365780, called ONLY from the GOM ctor, itself called from CLevel::CLevel +0x5b0):
1. ReadInt magic 'DICT' -> BeginRead.part (0x39e97c; the public BeginRead 0x33c8b8 rewinds,
   sets gol mode bytes +0x34/+0x35, re-checks DICT) which consumes tableOff(4)+pad(1) and
   wires the STRING TABLE into [stream+0x28..0x2c] (gol.bin tableOff@4 = 0x774d3, nstr 5799).
2. Back in Load: u16 "GO" (bytes 9..10 = 0x474f), version u16 == 3 (bytes 11..12), nrec u32
   @13 (653), offsets u32 xN @17. Header exactly matches the s57 JS parser layout.
3. Per record (ALL 653, no filter): oid u32 -> M[oid] refs list (m u32 + m x u32; this map at
   GOM+0x18 is read by GetObjectReferencesTemplateFromObject 0x3686b0), u16 cnt2, name
   (u32 string-table index -> M2 name->oid at GOM+0x2c via GetObjectIdFromName 0x3656ac),
   then cnt2 x (u32 classId, u16 flag) -> M3[oid] = vector<TObjectData>{bool flag@0,
   CComponentBase* comp@4, int classId@8} (GOM+4 map), then cnt2 x **GCT(classId, stream)**
   storing the component into TObjectData.comp@4. NO skip, NO filter, and none needed:
   every classId is cased.
- Post-pass: CheckObjectCategory(oid) for every loaded oid (0x365f8c): scans TObjectData[].id
  for 0x3438ab08 (-> CGadgetManager::AddObject) and 0x378ded9b (-> CTrafficControl::
  AddVehicleTemplate). Both ids ARE GCT cases (0x3438ab08 = CComponentGrenade, 0x378ded9b =
  CComponentDropCollectible - s60 had these classes swapped/unresolved).
- Special case: oid 0x163a6 -> CEffectsManager::LoadLODs(TD[0].comp) after its record.
- Consumers: CLevel::LoadNextObject -> CreateObject(oid, lvc-stream, zone) = template
  instantiation (M3[oid] walk + per-class switch + one nested GCT call with null-check);
  Lua SpawnObject -> CZonesManager::SpawnObject -> CreateObjectFromLibrary(oid) (14 callers).
- GOM::Reload (0x366104) has ZERO direct callers (dead in this build); ReloadComponentTemplate
  (0x36b6ec) = [vptr+0x10] thunk on an existing component.

## T1(c) - hash hypothesis: MOOT (answered better)
The ids are not name-hashes; they are registry constants whose meaning is recoverable
DIRECTLY from the case bodies: case = alloc (mov r0,#n; bl operator new) + vtable store
(ldr rX,[pc]; add rX,pc,rX [+ #8]; str rX,[obj]), vtable layout has NO RTTI prefix:
[+0]=dtor1, [+4]=dtor2, **[+0x10]=Load (the template reader)**, [+0xc]=Clone.
=> complete engine-derived registry, 120/120 ids -> named readers, e.g.
0x5441a117 = CComponentBuiltinPlane (s60 called it "StateSet" from shape-guessing - WRONG name),
0x6754056b = CComponentAwareness, 0x378ded9b = CComponentDropCollectible,
0x222500f6 = CComponentTheBatHandle (TheBatDrive's 13th component),
0x651bdaa = CComponentPlatform_Properties, 0x2ca13c06 = CComponentVehicleCollision,
0x3438ab08 = CComponentGrenade, 0x454206a4 = CComponentAIController, 0x339bfc0c =
CComponentPlayerCape, 0x110ce1f = CComponentGlide. (s60's "CVehicleCollision 0x67c82e62 has
no case" also corrected: id -> case exists? - see s61_t1_readers_merged.json for the full map.)

## T1(b) - closure under each rule set (denominator = all 653 gol records)
Walker = s61_t1_walker2.py (s60 machinery, key-format bug fixed: '0x%08x' normalization).
- ENGINE-TRUE RAW (120 auto-extracted reader specs, zero fitted): **exact 159/653 (24.4%),
  bounds 555/653 (85.0%), fail 93, NA(empty comps) 5.**
- + GOLSHAPE (single labelled fitted rule: 0x59a8390c template shape 16 B = i,i,STR,i;
  the s60 finding, kept because the engine reader 0x3c3f30 = CComponentTutorial reads
  the instance shape): **exact 313/653 (47.9%), bounds 553/653.**
- + 2 hand-verified reader specs (MainStoryQuests 0x5863bd59, NewShopItemProperty
  0x4ca5f00e - unchanged from s60): no change to the totals above (they already closed).
- The 93 fails = auto-extractor sequence gaps (18 specs contain unresolved 'call' inner
  reads: Trail 0x116a6fa, MissionsList 0x5471c18b, Awareness 0x6754056b auto-spec etc.)
  + OOB classes. This is the honest residual: the id->class registry is 100% engine-derived;
  the per-class BYTE SEQUENCES are engine-derived for the fixed-shape majority and
  still need s60-grade hand verification for the rep-heavy minority.
- Nulls (GOLSHAPE table): N1 spec-permutation exact 313 -> **3** (collapse); N2 payload
  rot-7 exact 313 -> 311 (length-preserving, documented weak, same as s60).

## Rule-set comparison (bounds/exact over 653; carrier values over 50)
| rule set | closure | carriers |
|---|---|---|
| s58 fitted (s30 + overrides) | 326/653 bounds | 30/50 closed, 9 corrections vs s56 |
| s60 hybrid (engine 64 + s30 fallback + 1 golshape) | 524/653 bounds, 393 exact | 33 closed (14 NPC@121 + 19 vehicle@137), 18/18 values EXACT vs s58 |
| s61 engine-true (120 readers, 1 golshape) | 555/653 bounds, 313 exact | 13/50 close but values MISALIGNED (auto-spec gaps) - value work stays on the s58/s60 calibrated subset |
- The other 12 of s58's 30 carriers: s58 closed them with fitted s30-instance shapes that
  the engine readers contradict; under s61 engine specs their templates sit in the 93-fail
  bucket (call-incomplete specs). Value-accurate carrier extraction must wait for hand
  verification of those ~18 rep-heavy readers (estimated 0.5 session).
- Note: s60's "Health@121 / Awareness@138 (NPC) vs @137/@154 (vehicle)" position classes
  came from the hybrid walk; they remain the best calibrated values (18/18 agreement).

## Artifacts
- s61_t1_gom_load.txt (full annotated GOM::Load), s61_t1_disasm2.py (CheckObjectCategory)
- s61_t1_gct_scan.py / s61_t1_gctfull.py (island-truncated censuses - kept to document the trap)
- s61_t1_parse_gol.py -> s61_t1_parse.json (engine-layout parse, 653 records, names, refs)
- s61_t1_xref2/3/4.py (callers, pointer words), s61_t1_golscan3.py (gol census: exactly ONE
  gol stream in all 43 .gla archives - game_config.gla gol.bin)
- s61_t1_idcheck.py -> s61_t1_id_cases.json (119/120 ids -> cmp site + case vtable)
- s61_t1_readers.py/2 + merge -> s61_t1_readers_merged.json (120/120 reader symbols)
- s61_t1_reader_specs3.py -> s61_reader_specs.json (120 auto specs)
- s61_t1_walker2.py -> s61_t1_walk2.json (closures + nulls), s61_t1_carriers.json
