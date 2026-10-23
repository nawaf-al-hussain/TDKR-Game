# s55 T6 — combat/AI data survey (scoping only; no implementation)

## 1. Engine components/classes (libKRHP.so symbols)
- CComponentHealth: Load @0x2d7bf0 (+6 more syms) — actor health persistence.
- CAwarenessComponent: ClearStates @0x3950dc, DetectTarget(GameObject) @0x3955d4,
  RayQueue_Init/Update @0x396554/0x396564 (LOS raycast queue), Reset @0x394d80;
  static g_rayQueueLen @0xc175f0. Detection = ray-queue based.
- CMotionComponent: GetMoveDir/GetEndPoint/StopMotion/GenerateAvoidingPath (path
  avoidance around listed CGameObjects) — steering layer above the navmesh.
- CActorBaseComponent combat surface: SetHitBone(string) @0x38acd0, SetHitEffect
  @0x38acc4, GetHitAngle @0x38a7ec, IsTargetHit(vec3,vec3,int) @0x38bb44 (per-bone
  hit test), RepositionForHit(iii) @0x389614, DrawHitTriangle(CollisionResponse)
  @0x370f04 — melee hit detection is bone/geometry-based on the actor component.
- NPC AI: CNpcAIComponent state machine (symbols seen in the s55 T2 scan:
  OnZoneUnload, SetEnemy, Decor_Update, Stuck_OnEnter/TestEnter, Attack_OnEnter,
  Attack_UpdateRanged(float), Nav_WP_OnNext) + AI_Target::MessageAlert,
  AI_ShoutReinforcements::Update(state,scope,stance) — alert/reinforce broadcast.

## 2. Combat states (state table, s36 mechanism)
- core[10] = "Enemy_Combat_Idle / Knife_Combat_Idle / Enemy_Idle_Aim" (lua_uses 4)
  -> clips _385_mc_combat_idle_attack family + enemy idle family.
- The full Lua state list (s36_t3_lua_states.json) carries the combat families;
  deep combat states beyond combat-idle are script-driven (NPCSState*).

## 3. Animation clips (batman_anims.bdae, 921 numbered clips — s55_t6_clipfams.json)
attack 33 (_385_mc_combat_idle_attack, _386_enemy_combat_idle_attack,
_461/_462 batman jab counter attacks), counter 20 (_456 enemy jab countered hurt,
_486 cross countered hurt, _630 batman leg-kick counter attack), takedown 14
(_076 glide_parachute_takedown, _085/_086 hang_edge silent takedowns, _247 wire
silent takedown), hit 9 (_429 doublehammer_hit, _431 enemy hithurt, _619 gargoyle
takedown hit), block 10 (enemy crowbar upper/lower block family), plus grapnel 61,
glide 42. A minimal melee set needs ~6-8 clips: attack, countered-hurt, block,
hit-reaction, combat idle x2.

## 4. Lua API (game_config.gla 26.3 MB, occurrence counts = call volume)
NPCAttackTarget 529, SetActorSpeed 291, GiveDamage 146, ActorIsAttacked 73,
SetActorHealth 63, GetActorHealth 21, NPCCombatSet 2, NPCGetEnemyFlag 1,
Enemy_Melee_Attack 1; NPCSStateCombat/SplashDamage/IsActorKillable/SetAwareness 0
(engine-internal paths instead). Template usage: Crowbar_Enemy 220, Knife_Enemy
109, Melee_Enemy_Merc 40, Spawn 1216 (all families).

## 5. Enemy templates (gol.bin; 38 combat-ish named records)
- Melee archetype (19 comps, ~500-700 B payload): Melee_Enemy_Merc 0xc351d (683 B),
  Melee_Enemy_Stadium 0xea61 (523 B), Melee_Enemy_Pit 0xc3521, Melee_Enemy_Test
  0x4c71a — the 18-19-comp build = health + awareness + motion + npc-ai + melee-
  attack component stack; payloads are per-instance tunings.
- Behavior templates (1 comp, BIG payloads): Enemy_Melee_Attack 0x7a12a (10,756 B),
  Enemy_Melee_Hurt 0xc0df9 (13,113 B), Enemy_Ranged_Hurt 0x4c72b (9,026 B),
  Enemy_Melee_Movement 0x7a128 (2,191 B), Enemy_Cover_Shooting 0xc3508 (3,413 B),
  Enemy_Grapnel_Target 0xaae6a (2,572 B) — these are the AI behavior definitions
  (state trees/parameters), the primary decode targets.
- MeleeEnemy** count as archetypes: LeadMerc, Bazooka_Enemy, Knife_Enemy(+Prisoner),
  Crowbar_Enemy, Ranged_Enemy_Test (18-comp builds).

## 6. Scoped plan: minimal combat slice (one enemy, one attack, one hit reaction)
Data sources (all already in hand, user-zip derived):
1. Enemy = Melee_Enemy_Merc template (0xc351d) — instantiate from its 19-comp
   payload; reuse the s49/s54 bdae/anim pipeline with the enemy skin if present in
   actors.gla (needs one check: enemy skin/anim set exists in the same bdae format).
2. Attack = _386_enemy_combat_idle_attack + batman _461 jab counter; hit reaction =
   _456 enemy jab countered hurt; combat idle = _385/_386 family.
3. State flow = the s36 state-table mechanism (Lua ActorSetState -> clip), already
   shipped for glide/grapple; add states Enemy_Combat_Idle, Attack, Hurt.
4. Health/damage = CComponentHealth::Load decode (1 session item; simple
   ReadFloat/ReadInt like glide) + the Lua GiveDamage/SetActorHealth shim.
5. Hit detection = IsTargetHit(vec3,vec3,int) semantics: distance + facing cone +
   hit-bone string (SetHitBone) — decode the function (~0.5 session).
6. Awareness = skip for the slice (script-driven proximity instead, as the playable
   page already does for triggers).
Unknowns / risks: enemy skin assets (may be in a separate actors pack per level);
NPCAttackTarget argument semantics (529 call sites give plenty of calibration data);
the 10-13 KB behavior-template payloads (Enemy_Melee_Attack/Hurt) — decode only the
fields the slice needs (timings, ranges) rather than the full tree.
Size estimate: 1.5-2 sessions for the minimal slice (enemy render+anim 0.5, combat
state flow + 4 clips 0.5, health/damage + hit test 0.5-1); full combat/AI remains
4-6 sessions (unchanged from s54 estimate).
