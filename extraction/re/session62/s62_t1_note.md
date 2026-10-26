# SESSION 62 — T1: engine-true template closure with hand-derived readers

## Headline
Census first: the s61 "93 fails / ~18 gap readers" decomposed into 13 distinct blocking
component ids + a dominant tail:8 x160 cluster. Hand-derivation from the ARM disassembly
found TWO systematic s61 extraction defects:
1. **Tail-call reads missed** (b ReadString at function end): BeastObjectComponentGlobal
   (0x2e1fb0 = i,i,STR), BeastObjectComponent (0x2e1e8c = f4,STR,f4,STR - two strings),
   SurveillanceCam (0x2e4e98 = f7,i,f,i3,f2,STR), Destroyable (0x2e3500 = i,STR5,c2,STR),
   Motion (0x2d79ec = STR tail call - the whole reader!), etc.
2. **The id->case pairing was shifted for 42 of 137 ids** (s61 paired cmp sites in tree
   order with ids in value order). Re-extracted by reading the movw/movt pair that feeds
   each cmp (152 cases; 4 more via mov rX,#imm8 low halves). Validated by GetId
   co-location (VehicleLogic 0x378ab920, BeastGlobal 0x59a8390c), template names
   (Batarang_* contain 0x0f992a02 = CComponentBatarang; ExhaustFan_BEAST contains
   0x65da04ed = CComponentExhaustFan), and s57's page-validated 0x5441a117=stateset.
   Corrections include: 0x0f5f8cfd=Animated (NOT ExhaustFan), 0x65da04ed=ExhaustFan,
   0x62353c58=SurveillanceCam (0x592ce07c=ActorSpecialEffects), 0x519ad19b=MuzzleFlash
   (0x2c9a0e3f=BuiltinColors), 0x2ad2a046=BuiltinGroup (0x2cf1c31c=GrapplingGun),
   0x1d50aa73=CharXPLevels (0x378ab920=VehicleLogic), 0x010fcfd6=Dummy (0x0e31d4a0=Weapon),
   0x0651bdaa=ActorsCollision (0x0d6f39c4=Platform_Properties), 0x4a04f065=KombatCameraParams,
   0x2ef26c52=SoundAndLight (0x6bb478e6=PlayerCaught), 0x6a204677=GadgetZoom. s61's
   "reader 0x3c3f30=CComponentTutorial for 0x59a8390c" was wrong (0x3c3f30 belongs to
   0x58b2b422; 0x59a8390c is the GCT fall-through BeastObjectComponentGlobal).

## Reader sequences hand-derived this session (all from disassembly, ARM mode)
44 new/rederived readers, incl. the blockers: Trail 0x2e5318 = [i, rep(c,STR,STR,f6)]
(std::fill = vector defaults, no reads); CustomizeActor 0x3bf688 =
[i, rep(STR,STR,STR,i, rep(i: STR)), i, i] (nested; SkinSets ctor = no reads);
MuzzleFlash 0x3c2a48 = [STR,i,rep(i: STR),STR,c5,f4,i3]; SmartLight 0x2e30bc =
[STR,c,f,f,c,i,c,i, rep(i: c4,i3,f)]; Dummies 0x2e3940 = [i, rep(i: STR)] (fill loop
READS a string per element); ActorBase 0x3baee0 = [c7,f16,c3,i,i, rep(i: i,c)] (82+5n,
s60's note confirmed, rep found); DropCollectible 0x2e27b8 = [i, rep(i: i,i)]
(s57 page-validated shape); StateSet 0x3b8e9c = [i(count), rep(count:
CContainerState::Load), STRx7] with CContainerState::Load = [STR,i,i,c7,f10,i4,c2,
i(animN), rep(animN: CContainerStateAnimation::Load), i(n2), rep(n2: i6,f,i2,STR,i)]
- nested containers make the element size DATA-DEPENDENT; CContainerStateAnimation's
body is the one remaining undecoded reader. Awareness 0x6754056b = [f x16] EXACTLY
(no leading int - the s61 auto-spec's leading i was wrong; the -1 belongs to Motion).

## Closure (denominator = all 653 gol records; zero fitted rules)
- **S62 ENGINE-DERIVED: exact 473/653 (72.4%), pass 642/653 (98.3%), fail 6, na 5.**
  vs s61: exact 313 (1 fitted golshape rule), pass 555. +160 exact, +87 pass, fitted rule REMOVED.
- Nulls: spec-permutation exact 473 -> 24 (collapse; discriminative); payload rot-7 -> 349 (length-only, weak, documented).
- Residual fails (6): BatPod, Helicopter, Helicopter_Bane, Military_Heli, Test_Object,
  TheBatDrive - all multi-state StateSet templates (count>0); blocked by the
  CContainerStateAnimation body (est. 0.25 session).
- Non-exact tails: tail:4 x27, tail:2 x18, tail:16 x7 (small epilogues; documented).

## Carriers (Health 0x0ddcd6c4 = [f,c,i,i]; Awareness 0x6754056b = [f x16])
51 of 57 Health/Awareness carriers walk with the engine-true specs (6 fails = the
StateSet residual templates). Values vs s58/s60 calibrations:
- Melee_Enemy_Merc/Pit/Stadium/Test + Police_Officer_Melee: health 120.0 EXACT (s58),
  awareness radii [11,17,0,0,2,5,0,0,1.5,6,...] EXACT (s58's family).
- 18 of s60's 19 vehicle carriers: health 300.0 EXACT (Tumbler, Police_Car, Bane_SUV,
  Coupe, Hatch, Limousine, ...). Helicopter = the 1 not closed (StateSet residual).
- Full distribution: 300x18, 150x6, 1400x5, 120x5, 60x3, 100/90/140/70/50/1/0 (bosses
  1400, civilians 60 - matches s56's family clustering). Awareness families: (11,17)x13
  NPC-melee, (5,15)x20 vehicles, (16,23)x2, (70,70)x2, (10,15)x2, (13,15), (15,23), (60,60).
- AGREEMENTS: every s58/s60 calibrated value re-derived exactly; DISAGREEMENTS: none;
  NEW: the remaining 33 carriers (Bane, Batman, Blake, officers, ... = health 150/1400/60...).

## Artifacts
s62_t1_blockers.py/.json (fail census), s62_t1_id2reader.py/.json (corrected 152-case
registry), s62_t1_diffreaders.py (42-mismatch proof), s62_t1_specplan.py/.json,
s62_t1_closure2.py -> s62_t1_closure.json + s62_t1_final_specs.json (156-id table,
57 assignments from 59 hand-derived readers), s62_t1_carriers.py ->
s62_t1_carriers62.json, s62_reader.py/s62_disasm.py (tooling), s62_t1_sweep_ss.py
(StateSet variant sweep).
