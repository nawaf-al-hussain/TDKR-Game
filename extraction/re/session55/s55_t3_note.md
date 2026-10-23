# s55 T3 — grapple/glide data: grappling gun component, Enemy_Grapnel_Target census

## CComponentGrapplingGun::Load (@0x3bb510, ARM, bound 0x3bb6ac)
Stream order: ReadInt, ReadInt, ReadFloat x20, ReadInt, ReadFloat x5, ReadInt,
ReadFloat x3, ReadInt  =>  5 x ReadInt + 28 x ReadFloat.
Field layout: [i0][i1][f0..f19][i2][f20..f24][i3][f25..f27][i4].

## Is the gun data-driven? — NO from templates
- Glider (0x2674) / Glider_Plunge (0x4c741) templates byte-decoded (payload 101 B):
  `[u8 0x01][u32 0][u32 0][int1][f0..f20 (21 BE floats)][int2]` — the block after the
  9-byte head is ENTIRELY the CComponentGlide block (92 B = 4+84+4). There is NO
  grappling-gun payload anywhere (gun Load would need 132 B).
- NEW byte-level proof: byte 12 differs between the templates (Glider 0x00,
  Glider_Plunge 0x01) => **int1 = the CGadgetManager::GetGlide(0/1) SLOT index**
  (matches the s54 AddObject finding: 'Glider' slot 0, 'Glider_Plunge' slot 1).
- CORRECTION of s54: int2 = 0, not 600. s54's 600 (0x258) came from a 1-byte
  misparse of the payload end (payload_len 102 vs true 101) leaking the next
  record's bytes.
- Where gun values come from: UpgradesManager getters read a
  `std::map<int,SUpgrade>` — GetGrapplingGunCombatRange key 3, EnemyPoolSpeed/
  EnemyHit key 4, HookSpeed key 5; value float at SUpgrade+0xc (level short at +2).
  => gun parameters are UPGRADE-driven; the population source of that map
  (shop/upgrade config) is the remaining RE item (est. 0.25-0.5 session).
- Component float naming: structural only (i0..i4, f0..f27 with their read order)
  — no consumer names claimed without a data source; CRopeSceneNode::Init
  (@0x18ab64) is the main runtime consumer for later work.

## Enemy_Grapnel_Target (gol template 0xaae6a) census
- gol.bin: 1 record, oid 0xaae6a, 1 component 0x5441a117 flagword 1, payload 2572 B
  (full enemy/AI component template data — belongs to the T6 combat survey).
- lvc census (pure parser, spawn records tid 0x2662): 12 levels parsed
  (Test.lvc frame error, shop.lvc incomplete — same as s54): 436 spawn records,
  414 distinct objIds, **0 x 0xaae6a in every level** (per-level counts 0; null
  control = the 414 real ids that DO appear, max 3 per id — the census mechanism
  detects instances when present).
- game_config.gla (26,281,135 B, from the user zip): exactly **1** occurrence of
  'Enemy_Grapnel_Target' (and 6 of 'GrapplingGun', 1216 of 'Spawn').
- VERDICT: Enemy_Grapnel_Target is SCRIPT-spawned from a single config/site —
  NOT level-placed. The slice's grapple-target source (CWayPointObject anchors,
  s54) remains the correct data-driven stand-in. A minimal combat slice would
  spawn this template from its script site; the 2572-B payload decode is deferred
  to the combat survey.

## What is data-driven vs needs more RE
- data-driven NOW: glide floats (21, T2), grapple targets = waypoint anchors,
  gun upgrade effect keys (3/4/5).
- needs RE: SUpgrade map population (shop/upgrade tables) 0.25-0.5 session;
  0xaae6a payload (combat survey, T6 scope); CRopeSceneNode::Init gun-consumer
  naming (only useful once upgrade values are decodable).
