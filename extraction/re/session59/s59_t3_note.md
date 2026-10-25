# s59 T3 — template closure: mechanism VERIFIED at the engine level, blocker classes NAMED, walker rebuild FAILED calibration (scripts lost) — closure numbers stand at s58's 326/653 + 30/50 (PARTIAL)

## Template-stream dispatcher VERIFIED (the task's "gol Reload path" question)
`_Z25GenerateComponentTemplateiP13CMemoryStream` @0x368ac0 (11308 B) is called from exactly:
- CGameObjectManager::Load @0x365db0
- **CGameObjectManager::Reload(CMemoryStream*) @0x3669e4** (the gol Reload path)
- CGameObjectManager::CreateObject @0x367fdc
Structure: per-comp id compare chains (movw/movt pairs), per case `new <class>` (+vptr),
common tail @0x368bfc: `mov r0,r4; ldr r3,[r3,#0x10]; mov r1,r6; blx r3` =
**[vptr+0x10] = the per-class TEMPLATE reader virtual, invoked with the stream** —
a different slot from the instance Load used by lvc (s56's vtable+0x18). Templates read
differently from instances BY DISPATCH.
- For 0x2db081e2 (CCollisionComponent): the vtable group containing CCollisionComponent::Load
  (0x2230a8) has the Load AT [vptr+0x10] — **the template reader IS CCollisionComponent::Load**,
  the same function whose s58 CMemoryStream read-sequence was decoded (16-B base +
  conditional primitive tail). s58's "template payload = 16-B base flat" is CONSISTENT with
  the dispatcher (the conditional tail is skipped by the base's own flag in templates).
  The case also stores a global+0xc ref at obj+8 (shared default-shape holder).
- CComponentAwareness::Load (0x3bbb68, reached via CAwarenessComponent::Load 0x394ec8 wrapper,
  0x44-B object) = 16 sequential ReadFloats into fields +0x4..+0x40 — byte-exact match with
  the walk's 64-B Awareness payloads. **Engine field naming**: ResetVisibilityAngle
  (0x39638c): `[aware+0x38]` (field 13) = **VisibilityAngle in DEGREES** (160.0 for
  Melee_Enemy_Merc = s56/s58's "FOV 160"), copied to [comp+0x24] (GetVisibilityAngle
  0x3963bc returns it) with cosf(angle*K) precomputed to [comp+0x28] for the cone test;
  GetVisibilityFront uses +0x24/+0x14; DetectTarget uses +0xc/+0x10/+0x18/+0x24/+0x38.
  The 11/17 radii (fields 0/1) have NO consumer inside CAwarenessComponent — their readers
  live outside (AI-side) and are NOT named this session (recorded open).

## Blocker ids -> classes (movw/movt scan of .text; ids appear NOWHERE as literals/hashes)
| id | n (of 653) | class (two signals: CreateComponent case + GetType/ctor) | GCT template case? |
|---|---|---|---|
| 0x4cc04ddb | 59 | **CBeastOmniComponent** (GetType 0x2e23b4; GCT case @0x369058) | YES -> decodable in principle |
| 0x43c8a8d1 | 24 | unnamed 0x14-B comp (GCT case @0x368c14; +4/+8 = global+0xc refs) | YES |
| 0x0116a6fa | 18 | trail comp (StartTrail/StopTrail lua, CWeapon ctor, CreateComponent @0x224ff4) | **NO GCT case** |
| 0x7d561d33 | 18 | GCT case @0x369f5c; CreateComponent @0x225c88 | YES |
| 0x67c82e62 | 14 | **CVehicleCollisionComponent** (GetType 0x2e1470; CreateComponent @0x224294) | **NO GCT case** |
| 0x4cc07242 | 11 | **CBeastSpotComponent** (GetType 0x2e2590; GCT case @0x36ab74) | YES |
| 0x28091330 | 10 | **CCollectibleComponent** (GetType 0x2d7fcc; GCT case @0x36affc) | YES |
| 0x0dd583de | 9 | 0x10-B comp (GCT case @0x368ce4) | YES |
| 0x0e1f5b6f | 2 | **CSniperComponent** (ctor C1; CreateComponent case) | **NO GCT case** |
KEY FINDING: the ids that block 0x67c82e62 (14 vehicle carriers incl. Bane_SUV x2,
Car_Sedan_Minigame) and 0x0e1f5b6f (Sniper, Ranged_Disarm_Dummy) have NO case in
GenerateComponentTemplate — the engine's own gol template path cannot construct them
(no movw/movt pair in GCT, no literal anywhere in the binary). Their blocker status is an
ENGINE-side unsupported-comp fact, not just a missing spec in our walker. (Caveat: if GOM's
comp-id vector built in Reload pre-filters unsupported ids, the payload framing must still
come from somewhere — the filter loop at 0x366954..0x3669c8 assembles flag bytes + ReadInt
ids; whether the payload of a skipped comp is length-skipped could not be pinned in-budget.)

## Walker rebuild FAILED (honest)
The s57/s58 walker scripts were lost with the s57 workspace (only receipts survive). The
rebuild (s59_t3_walk.py: s30 lvc table + the 11 documented s57/s58 template overrides)
closes only 5/653 — the s30 specs do NOT fit the gol template path for the ~40 remaining
legacy-id comps (0x14ca79 445, 0x152b87 26 — legacy-address ids with template-specific
shapes documented only in the lost script, e.g. '0014ca79:spec:44'). Re-deriving all of
them = more than the remaining budget. **Closure stands at s58's 326/653 (49.9%) and
carriers 30/50 (60%); this session's additions are the mechanism + class-name table above.**
LEN-MISMATCH (111): templates whose ordered walk consumed != payload length (residual tails
on late comps) — with the engine insight these are templates whose tails contain comps the
engine's own path handles outside GCT cases; per-template residuals listed in
s58_t2_walk_out.json (unchanged).

## Vehicle health 300 second signal (partial)
1. (existing, s58) 15-vehicle simultaneous boundary alignment under the collision 16-B spec.
2. (new) the Awareness field map is now ENGINE-verified (16 ReadFloat -> +0x4..+0x40) with
   field 13 named VisibilityAngle-degrees by ResetVisibilityAngle/GetVisibilityAngle — the
   same Load semantics decode the vehicle aware vectors [5,15,2,8,...]; vehicles use
   CComponentVehicleAwareness (Load 0x1c2ee4) whose base shares the 16-float layout.
3. Lua SetActorHealth (63 call sites) constant-pool decode remains OPEN (compiled-Lua
   bytecode) — not achieved in budget; recorded.

## Verdict vs acceptance
- Decode blocking comp Loads (template path) from the engine: PARTIAL — dispatcher +
  Collision template-reader identity + 6 class names + 3 no-case findings done; the per-class
  template Load read sequences for 0x4cc04ddb/0x43c8a8d1/0x7d561d33/0x28091330/0x0dd583de
  NOT extracted (vtable slot resolution needs per-class ctor chains; out of budget).
- Reduce failures / report fractions of 653 and 50: NOT MET numerically (walker rebuild
  failed calibration 5/653); fractions stand at 326/653 + 30/50 with the blocker table now
  class-named and mechanism-explained.
- Collision/StateSet/Motion template-reader verification: DONE for Collision (template
  reader == Load 0x2230a8; 16-B base); StateSet/Motion dispatch through the same [vptr+0x10]
  mechanism (s57's byte-forced shapes remain the best evidence for their sequences).
- Vehicle health second signal: PARTIAL (engine field map + named FOV consumer; Lua open).
