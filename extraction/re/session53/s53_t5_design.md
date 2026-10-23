# Session 53 — T5 design note: glide + grapple (data sources, parameters, unknowns)

## 1. What the engine has (verified this session, libKRHP.so full symtab)

### 1.1 Lua API (script-facing)
Symbols (all `t` = local text, `*P9lua_State` = Lua bindings):
- `QTE_AutoGrapnel` @0x159a38 — auto-target grapple (QTE = quick-time event).
- `ActorGrapnelEnable` @0x1590f8, `CarGrapnelEnable` @0x15920c,
  `CarGrapnelGlobalEnable` @0x159038, `EnemyGrapnelGlobalEnable` @0x1590b8,
  `GargoyleGrapnelGlobalEnable` @0x159078 — per-class enable gates.
- `IsGrapnelControlEnabled` @0x15da2c / `SetGrapnelControlEnable` @0x15d814.
- `IsGlideControlEnabled` @0x15da74 / `SetGlideControlEnable` @0x15d87c.
- `SetActorSpeedGlide` @0x15f524 — script sets the glide speed.
- `NPCRunGrapnelGunTargetScript` @0x151918, enemy grapnel-gun targets
  (@0x16b168/0x16b6d8/0x16ad90).

Lua usage in the shipped scripts (437 GothamCity + Island2 objects):
- `GrapnelControlEnable(...)` x10, `GlideControlEnable(...)` x2 — e.g. obj 400528 gates
  grapple by mission progress ("under_pressure", "save_lucius", "dirty_cop", "siege_part_1",
  "saving_miranda").
- Animation clip names referenced directly: `Glide_Idle`, `Glide_Idle_To_Grapnel_Horizontal`,
  `Grapnel_Loopable_Pull_Start`, `Grapnel_Enemy_Knockdown_Hurt_Front`,
  `Gargoyle_Idle_On_Vehicle`.

### 1.2 C++ component chain
- `CComponentGlide::Load(CMemoryStream)` @0x3c0938 (ARM, verified by capstone):
  **2x ReadInt + 41x ReadFloat** — 41 streamed float parameters (gravity, forward speed,
  bank, lift, ...). Reader thunks verified: CMemoryStream::ReadInt @0x339914,
  ReadFloat @0x339b94. Defaults live in the level object template streams (gol.bin), NOT
  in the code — see unknowns.
- `PlayerComponent::EnterGlideFromGrapnel` @0x25f770: guard `state == 7` (grapple/hang),
  then a float at component+0x520 must be NEGATIVE (height-above-ground or downward-dot
  check), tail-jumps to `CActorBaseComponent::StartGlideFromGrapnel` @0x380a0c.
- `PlayerComponent::EnterGlideFall(int)` @0x259ba4 — the non-grapple glide entry.
- Pull-down mechanics (`CanPull`): `CPullDownMGBase::CanPull` @0x1cf628,
  `CPullDownMGSlider::CanPull` @0x1d160c — interactive pull-down objects, NOT navmesh.

### 1.3 Grapple targets
- `CWayPointObject::GetGrapnelTargetPosition` @0x2a9024: virtual getter (vtable+0xc)
  returns a vector3 — waypoint objects carry a grapple anchor point provided by their
  subclass (gargoyle anchors, ledge anchors).
- `CGameObject::GetGrapnelTargetPosition` @0x360c40 — same protocol on generic objects.
- Gargoyle grapnel: `GargoyleGrapnelGlobalEnable` + `Gargoyle_Idle_On_Vehicle` clip —
  gargoyles are the canonical Batman grapple anchors.
- Navmesh: `CNavMeshNova` has NO grapnel-record API (only cells/portals/ray tests:
  Create/GetCell/GetNeigh/GetPortalId/CanReachCellFrom/TestRayInters). No `.edge` files
  exist in the OBB (zip listing checked: 0 matches). The s52 brief's "grapnel records /
  CanPull edges in .edge files" is NOT how this build represents grapple targets - they are
  object anchors (waypoint/gameobject virtuals), not navmesh edge flags.

### 1.4 Animation clips (all decodable; s35 battery 921/921)
104 glide/grapnel clips in the shipped set. Key ones (battery index, duration ms):
- 55 `_057_glide_idle` (2167 ms) - the glide loop
- 63 `_065_glide_idle_to_run` (667) - landing transition
- 88 `_087_idle_to_grapnel` (399), 89 `_088_grapnel_shoot` (432),
- 91 `_089_grapnel_pull` (1899) - the pull-in loop
- 51/52/58/60/62/64: parachute variants (wall-contact, land, transitions)
Exported into `batman.glb` this session: _057_glide_idle, _089_grapnel_pull,
_088_grapnel_shoot added to the staged page's character (idle/walk/run/jump/jab remain).

## 2. The minimal slice (implemented, staged, gated)

State machine (in `?s5=1` mode only; default mode pixels/digests unchanged):
1. GRAPNEL: pick the nearest decoded navmesh portal EDGE midpoint at least 18 u from the
   capsule and inside the corridor of the current route (uses the walker's existing cell +
   portal decode; the "edge" is a real decoded CNavMeshNova portal between two cells).
   Play `_089_grapnel_pull`; pull the capsule along a straight line to the edge midpoint
   with ease-in over 1.2 s (engine shows the same pull as a rope-constrained lerp; the rope
   render is out of scope).
2. GLIDE: on arrival, play `_057_glide_idle`; physics: forward speed 18 u/s (engine default
   unknown - see 3), gravity -25 u/s^2 (gentle, parachute-like per the clip set), bank =
   0.35 rad fixed roll for the slice (script `SetActorSpeedGlide` implies a tunable speed;
   bank sign follows lateral input in the engine).
3. LAND: when the capsule base reaches the navmesh surface (nm_ground, already computed
   per frame), play `_065_glide_idle_to_run`-equivalent (slice: run clip) and resume the
   walk route.
Gate additions (`window.__GATE.s5`): grapple target reached within 2.5 u; glide clip action
active during the glide window; landed on navmesh within 4 s; 0 console errors. Default
8-check gate untouched.

## 3. Unknowns (honest list; what a full implementation still needs)
1. The 41 float parameters of CComponentGlide (gravity/speed/bank/lift/turn): need the
   gol.bin template stream for the glide component of the player object - requires the
   component-type-id -> template-instance decode of lvc gol records (s31 decoded the
   template TUPLES; the type->name mapping for 'Glide' is not yet pinned).
2. The state id table (state 7 == grapple/hang inferred from EnterGlideFromGrapnel's guard):
   full state machine ids for Glide/Grapnel need the state-table decode (s34 work has the
   clip->state mapping partially).
3. Rope render + QTE timing (QTE_AutoGrapnel) - presentational, out of scope for the slice.
4. Which waypoint objects carry grapple anchors in GothamCity.lvc (the GetGrapnelTargetPosition
   protocol needs the object-class decode to enumerate them; gargoyles are visual candidates).
5. Landing transition blend weights (engine uses a blend tree; slice hard-switches clips).
