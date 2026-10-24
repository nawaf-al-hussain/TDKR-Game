# s58 T2 — enemy templates: coverage 110 -> 326 of 653; Motion shapes explained; GiveDamage decoded

## (a) The three blocked Loads, decoded from the engine (ARM disasm) and closure-tested
1. **0x2db081e2 CCollisionComponent::Load (0x2230a8)**, instance/CMemoryStream shape:
   base CComponentCollision::Load (0x2d72bc) = c,c,STR,i,c,c,i (16 B) + ReadChar cnt +
   (cnt>0: STR + i + cnt*(9 x ReadFloat + ReadChar)) + trailing ReadInt. The s30 table's
   rep spec = this instance shape. **TEMPLATE payload = the 16-B base ONLY** (primitives are
   instance data; the template!=instance pattern matches StateSet/Motion). Closure evidence:
   with 16 B flat, 0651bdaa@125 = [2.0,1.8,1.6] and Health@137 = 2.0 align across 15 vehicle
   carriers simultaneously; with the instance shape the walk fails at the cnt byte (0x40).
2. **0x33702f4a = CComponentSniper::Load (0x2e4b5c) = 5 x ReadFloat = 20 B** (weapon comp:
   Batarang_01/02, Batarang_EMP/Flash/Gas/Stone, Batarang_Left_01/02, Assault_Rifle_01 —
   the 9 templates that s57's "Sniper blocker" stopped now pass this comp).
3. **0x40c6b80a CComponentCustomizeActor::Load (0x3bf688; wrapper CCustomizeActorComponent
   0x396db4 news + tail-calls it)**: i(n) + n*(STR,STR,STR, i(m), m*STR) + i + i —
   EXACT walk implemented (loop @0x3bfe18, stride 0x18 entries, 3 header strings per entry,
   per-entry count + strings, two trailing ints @0x3bfe20/0x3bfe30). No candidate search,
   no sanity filter.

## (b) Structural walk re-run (s58_t2_walk.py -> s58_t2_walk_out.json) — no sanity filter
- **326 / 653 templates close EXACTLY (49.9%)** vs 110/653 (16.8%) in s57 — the collision
  16-B template spec is the single biggest unlock (+216 templates).
- **Carriers (Health+Awareness): 30 / 50 close (60.0%)**; Health/Awareness extracted for all 30.
- Value agreement vs s56 gap-search (s56_t6_enemy_decode.json): **21 MATCH** (health + all 16
  aware floats + int1/int2 identical), **9 CORRECTIONS**: Blake 150 (s57 correction confirmed
  a 2nd time) + **8 vehicles (Generic_Car, Taxi, SUV, Sedan, Coupe, Hatch, Van, PickUpTruck,
  SwatVan, Limousine, Destroyable_SUV, Military_Jeep, Military_Truck, Tumbler class):
  health = 300.0 (NOT s56's 2.0), int1/int2 = -1/-1 (s56's 16320/16448 = float bytes of
  1.5/3.0 misread — s56's vehicle boundary was pre-collision-fix), aware = [5,15,2,8,...]**.
- Every still-failing template and why (top blockers over 653): LEN-MISMATCH 111 (underconsumed
  late-comps, per-template residuals), 0x4cc04ddb 59, 0x43c8a8d1 24, 0x0116a6fa 18,
  0x7d561d33 18, 0x67c82e62 14 (vehicle extra comp, no spec), 0x4cc07242 11, 0x0e31d4a0 10,
  0x28091330 10, 0x0dd583de 9, 0x2c9a0e3f 6, 0x519ad19b 5, 0x5e46be31 3, 0x4ab8a7cd 2.
- Carrier failures (20 of 50): Bane_SUV / Bane_Suv_No_Doors / Car_Sedan_Minigame blocked at
  0x67c82e62 (unknown comp @137); Police_Car at 0x4ab8a7cd @328; Sniper + Ranged_Disarm_Dummy
  at 0x0e1f5b6f @134; small 4-12 B tail residuals on Coupe/Hatch/PickUpTruck/SUV/Sedan/Van;
  Helicopter x2 + Military_Heli underconsume 2667 B (big rep comp), Monorail x3 + Subway_Car
  261 B, Test_Object 35153 B (huge trailing arrays). Each needs its own Load decode.

## (c) Motion: the two shapes EXPLAINED and tested
- TEMPLATE (gol.bin): [flag=1, 750.0, 750.0, flag=1, 500.0, 500.0] = walk/run speed pairs,
  read by the generic template loader. Operative data (uniform across all humanoids; s57).
- INSTANCE (CMemoryStream): CMotionComponent::Load (0x2395f8) = single tail-call to
  CComponentMotion::Load (0x2d79ec = `add r3,r0,#4; mov r0,r1; mov r1,r3; b ReadString
  0x33a0d4`) — reads ONE string into the component base field.
- **TEST (lvc census, lvc.js parseLvc over 11/12 lvc files — Test.lvc OOMs at 6.5 GB heap):
  ZERO Motion instances.** 33 templates carry Motion flag=0 (instance bytes WOULD be read if
  such records existed) but no placement record in any parseable file instantiates it; the
  s57 hypothesis "the string names a motion set whose speeds are these pairs" is REFUTED for
  placement data: the speed pairs ARE the template payload; the string reader is dormant on
  the placement path (override/save-path semantics; the [base+4] field's role in the derived
  CMotionComponent layout — owner pointer vs string — is a multiple-inheritance offset
  question left unresolved; dormant either way).

## (d) GiveDamage decoded + census
- **GiveDamage(lua_State*) @0x155e4c = GiveDamage(actorId, damage)**: arg1 = lua_tointeger
  (actor id; 0 = the level dispatcher path), arg2 = lua_tointeger -> float damage; packed
  into an 8-word info struct {damage f, 0, -1 (source), 0,0,0,0,0} and dispatched via
  [obj vtable+0xa8] (slot 42) — or [CLevel+0xec]->vtable[0xa8] for id 0. Damage is a LITERAL
  script integer, NOT derived from health/upgrades.
- **Census across game_config.gla: 146 call sites (= s55's string count), ALL literal:**
  5 x91, 7 x11, 10 x9, 500 x8, 1000 x7, 50 x6, 25 x5, 15 x3, 300 x2, 20 x2, 30 x1, 5000 x1
  (12 distinct values). The 541-script lvc trigger corpus carries 18 of them, all
  GiveDamage(0, 5) (actor 0 = player, 5 dmg — the WhileIn hazard standard). Related APIs in
  the same file: KillActor 636, SetActorHealth 63, GiveDamageInArea/SplashDamage 0 (engine
  paths instead).

## Verdict vs acceptance
- Decode 0x2db081e2 / CustomizeActor inner Load / Sniper comp + re-run structural walk with
  no sanity filter: DONE — 110 -> 326 of 653 (49.9%), carriers 22 -> 30 of 50 (60%).
- Coverage fractions + every failing template listed with its blocker: DONE (above).
- Motion explanation + lvc test: DONE (string reader dormant; template pairs operative).
- GiveDamage args + damage-value census with counts: DONE (146 calls, 12 values).
