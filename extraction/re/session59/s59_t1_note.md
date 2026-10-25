# s59 T1 — glide blend cache: writer/state analysis COMPLETE; frozen-at-takeoff CONFIRMED for free flight + NEW re-anchor-on-air-collision refinement; helper = 0.0 at level 0 (code-verified)

## Q1 Who calls UpdateNavGlide / RefreshForcesGlide (BL xref, whole .text)
- UpdateNavGlide 0x380e94: EXACTLY ONE caller — CActorBaseComponent::Update(float).part.2842
  @0x3a2c58, call site 0x3a33e0 = the GLIDE case of a nav-mode jump table (siblings: Ride
  0x3a33c0, GrapplingHook 0x3a33d0, Flight 0x3a33f0, Transition 0x3a3400, ...).
- RefreshForcesGlide 0x3836b0: EXACTLY ONE caller — UpdateNavGlide @0x380fbc.

## Q2 Does Update's cache write execute in the glide state? NO — mutually exclusive branch
Update @0x36e394 per-frame structure (ARM disasm):
1. r5 = UpdateSpeed(dt) return (0x36e5ec..0x36e5f4; r5 in {0,1,2,3} from state flags 0x2/0x200/0x400
   at 0x38a250..0x38a3a8). If r5 != 0 -> Update returns at 0x36e690 with NO nav dispatch and NO
   cache write (movement handled by animation/displacement states).
2. r5 == 0 -> byteB = [[comp+0x60]+0xa] test at 0x36e694..0x36e6a0:
   - byteB != 0 -> "forces" path (0x36e6bc): pos = GetActorPosition() + [comp+0x224..0x22c]
     (velocity filled by RefreshForces 0x385788), SetActorPosition(0x36e744), THEN the cache
     write 0x36e74c..0x36e75c (velocity-predicted position). part.2842 NOT called this frame.
   - byteB == 0 -> bl Update.part.2842 (0x36e6ac) = nav-mode dispatch (incl. GLIDE). Cache
     write path NOT reached this frame.
   => a glide frame (byteB == 0, r5 == 0) NEVER writes the cache at 0x36e74c.
- byteB identity: [comp+0x60] = CComponentActorBaseComponent (218 B, allocated in
  CActorBaseComponent::Load 0x36cbfc); its Load (0x3baee0) fills bools +4..+0xa from the
  ActorBase template payload bytes 0..6: byteB = payload byte 6. A gliding actor MUST have
  byte[6] = 0 or no nav mode (incl. glide) would ever dispatch. byteA = payload byte 3
  (gates the animation-speed section at 0x36e604).

## Q3 Every writer of [comp+0x1a4..0x1ac] (per-symbol census, CActorBaseComponent only;
     171 other functions with coincidental offsets excluded)
ctor 0x36c15c (zero) | ReInit 0x36da3c (zero) | Update 0x36e74c (exclusive branch, above) |
TryEdgeGrab 0x371ce4 | UpdateNavSimpleBehavior 0x374750 | UpdateNavNormalSimplified
0x37490c/0x374de4/0x374f60/0x375758 | UpdateNavNormal 0x3776c4 | UpdateFloorTesting 0x386520 |
UpdateFloorProjection 0x3865d8 (strne) | UpdateNavGhost 0x386790 (strne) |
ResolveAirCollision 0x3987a4+0x3987d4.
Glide call-cone closure: part.2842 GLIDE case calls ONLY UpdateNavGlide; UpdateNavGlide's 12
direct calls touch NO writer (SetActorPosition 0x3a36c0 itself writes nothing — 2 calls only,
GetActorPosition + getAbsolutePosition); RefreshForcesGlide's 10 direct calls touch NO writer.

## NEW REFINEMENT (corrects s58's "NEVER written during glide" at one point)
UpdateNavGlide @0x382ec0: CollisionMgr::CheckForContacts -> if contacts and [[comp+0x2d0]+0xe]==0
-> ResolveAirCollision(pos, &out, 1) @0x382ef0, which STORES the collision-resolved position into
[comp+0x1a4..0x1ac] (0x3987a4/0x3987d4, from the resolved vec3 at sp+0x28..0x30).
=> blend distance d = |pos − cache| where cache = takeoff position in FREE FLIGHT, but the cache
   RE-ANCHORS to the resolved position at every air collision during glide (wall/ceiling scrape
   restarts the entry dip). Open-sky staged trajectories have no contacts, so the s58
   frozen-anchor implementation is exact on its domain; the re-anchor is code-proven,
   not page-exercisable (slice has no glide collision) — recorded as a domain note.

## Two signals (ground rule)
1. Call/state analysis above (writer census + branch exclusivity + call-cone closure).
2. Predicted behaviour on measured trajectories (?s5blend=1 battery, this session, n=25 Glider /
   n=28 Plunge, 200 ms samples, s59_t1_gate.json):
   - frozen model: page blend columns match max(0, 2*(1-d/16)) to 5e-4 (rounding); blend decays
     2.0 -> 1.434 (Glider, blendD 0 -> 4.526) / 2.0 -> 0.875 (Plunge, blendD 0 -> 9.003).
   - per-frame-displacement wrong model: blend_B = max(0, 2*(1-|v|/60/16)) ~ 1.976 constant ->
     vz error up to 0.525 u/s (Glider) / 1.082 u/s (Plunge) — 100-200x the frozen-model residual
     (s58: 0.0048/0.0049 u/s). Data arbitrates decisively for the frozen anchor.
   - s58 proxy control reproduced earlier at 0.93 u/s (different distance measure).

## Gates (s59_t1_gate.json; worktree s56-t1-glide 22b77bc, NOTHING patched — page default
   unchanged, ?s5blend=1 already implements the code-supported model for its domain)
default PASS digest 00ce7970e45adc85... = LIVE 137893 tris; s5_acc_glider landed 417 ms;
s5blend_exact 417; s5blend_plunge 467; s5_sink_control 917; s5_ctl 450 (= s57/s58 receipts);
0 console/page errors everywhere.

## Upgrades.bin (721 B, game_config.gla member) + UpgradesManager defaults
- Upgrades.bin = SHOP/LOCALE metadata, NOT engine floats: u32be 11 (key count) + u32be 1 +
  9x u16be (2..10); then records {u16 key, u16 flags(5), 4 length-prefixed strings, 25-B tail
  [u32 a, u32 b, u32 c, u32 price1 LE, u32 price2 LE, u8 id, ...]}: UPGR_NONE, UPGR_GRAPPLING_GUN_01..03
  (prices 80/90, 180/50, ...), UPGR_MC_TAKEDOWN_01, 'EOF' marker. NO float array, NO key 0x1f entry.
- GetGliderGravityHelper 0x1e1508 = UpgradesManager map[0x1f].value(+0xc) (operator[] 0x209dbc).
  Map entries are inserted ONLY by: AddUpgrade 0x1e03c0 (sets base=value=arg, level=-1),
  ResetUpgrades 0x1e0780 (defs from [mgr+0x38]/[mgr+0x94+key*4] tables, stride 0x3c, value at +8,
  walked back per level), LoadUpgradesStatus 0x1e0bd8 (save file -> ShopManager::BuyUpgrade per
  entry), or operator[] default {key 0, level 0, base 0.0, value 0.0}.
- Reachability census (4-B LE scan of the whole file + BL xref): AddUpgrade/UpdateUpgradeValues/
  ResetUpgrades/Upgrade have ZERO code references in the loaded image (only .symtab artifacts at
  0x54df5a/0xceda88 etc.); ResetUpgrades/LoadUpgradesStatus appear once each in a function-pointer
  registry at vaddr 0xc366f8/0xc36768 ({fn, 0, 0x70000, id} entries = UI/script dispatch — shop
  "reset upgrades" path); LoadUpgradesStatus BL-called ONLY from CInventory::SaveLoadGlobal 0x2554b4
  (save game). mgr Singleton (.bss 0xc16e84) constructed in Application::Init 0x3dbbf4 and
  CLevel::ResetProgress 0x3f4804; ctor 0x1e0258 initializes ONLY the map.
- => a fresh player who never bought an upgrade has NO map[0x1f] entry: GetGliderGravityHelper
  returns 0.0f. Key 0x1f is not among the shop's named upgrades (Upgrades.bin). HELPER BASE AT
  LEVEL 0 = 0.0 (two signals: setter-unreachability census; Upgrades.bin carries no engine float
  for 0x1f). Page helper 0 stands — no patch needed. s58's "number inconclusive" resolved.
