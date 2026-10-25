# s59 T4 — combat behaviour slice (enemy_viewer.html, branch-only): gate PASS with angular negative control

Data (all decoded): health 120.0 @payload+121 (walk + s56 agree); hits 5 HP (GiveDamage
census 5 x91) and 10 HP (census 10 x9) via applyHit; awareness cone FOV 160 deg =
engine-NAMED this session (CComponentAwareness::Load = 16 ReadFloat -> +4..+0x40; field 13
= VisibilityAngle degrees: ResetVisibilityAngle 0x39638c copies [aware+0x38] -> [comp+0x24],
GetVisibilityAngle returns +0x24, cosf(angle*K) -> [comp+0x28]); radii 11/17 (f0/f1).
State names from the StateSet template: Idle, Walk, Hurt, Death (Run reserved).
Clip bindings: Idle=_014_idle_enemy_combat, Walk=_166_enemy_walk, Run=_171_enemy_run,
Hurt=_222_enemy_hurtl, Death=_250_enemy_death1 (the s59-T2 in-page merc path plays Idle/
Walk/Run; Hurt/Death clips exist in the shared bank and are bound by name here).

Semantics implemented: inCone = dist <= R_FAR AND |angle-to-facing| <= FOV/2 (the engine
cone test shape: cosf((VisibilityAngle)*K) precomputed at +0x28); alert transition
Idle -> Walk on inCone(player); hit -> Hurt (0.4 s) -> Walk (or Death at 0 HP).

GATE (s59_t4_gate.json, playwright headless, 0 errors, screenshot s59_t4_viewer.png):
- NEGATIVE CONTROL (two cases): player at (0,60) = 60 u away -> state stays Idle; player
  15 u BEHIND the facing (inside R_FAR=17 but outside the 160-deg cone) -> Idle. The second
  case shows the transition discriminates ANGLE, not just radius (ctlPass true).
- Alert: player inside the cone at 8 u -> Walk (alertState).
- Cone geometry: drawnAperture 160 deg != 120-deg control cone (apertureMoves), radii 17-11=6.
- Health: 120 ->115 (hit 5, state Hurt) -> Hurt expires -> Walk -> 105 (hit 10, Hurt) ->
  ... -> 0 -> Death (hitsTotal 13 = 1x5 + 12x10 hits? no: 1x5 + 12x10 = 125 >= 120, last
  hit clamps at 0).
- State sequence: Idle, Walk, (Hurt, Walk) x12, Death — Hurt always precedes Death, Death
  only at 0 HP.
PASS = ctlPass && alertState==Walk && coneGeom && hp 115/105/0 && stateFinal==Death.
