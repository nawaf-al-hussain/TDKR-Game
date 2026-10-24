# s58 T1 — glide blend distance PINNED: takeoff-anchor distance, NOT a ground query

## The virtual call (RefreshForcesGlide 0x3836b0..0x383a08; ARM disasm)
0x383758 `ldr r2,[r4,#4]` -> r2 = [comp+4] = the owner CGameObject
(CActorBaseComponent ctor 0x36bfc0: `str r1,[r0,#4]`). 0x383768/6c: `ldr r3,[r2]; ldr r3,[r3,#0x18]`
= vtable slot 6. CGameObject vtable base 0xbd8028 (ctor 0x35aad0 literals; stored vptr = base+8):
slot 6 [+0x18] = **CGameObject::GetPosition() const @0x2d6f1c** (`add r0,r0,#0xc; bx lr` = &obj->pos,
position at [obj+0xc..0x14], same three words SetPosition 0x35b5f0 writes).
Secondary-interface slot 6 = GetTargetedPos (thunk 0x360a08) — NOT the called slot (r2 is the plain
object pointer). **The blend distance is NOT a ground raycast, nav height, or collision query.**

## Blend arithmetic (exact, per-instruction)
- 0x3837a0..c8: d = sqrt((P.x-pos.x)^2+(P.y-pos.y)^2+(P.z-pos.z)^2), P = GetPosition() pointer.
- 0x3837cc: d /= f9 ([gadget+0x2c]); 0x3837d0: 1 - d/f9; 0x3837d4 vmla s21,s15,s16:
  blend_raw = fB + (1-d/f9)*(f7-fB)  with fB=[gadget+0x24] (floor), f7=[gadget+0x28] (start).
- 0x3837ec vcmpe s21,fB; 0x383804 vmovge s15,s21: blend = max(blend_raw, fB) — LINEAR ramp
  f7 (at d=0) -> fB (at d>=f9), clamped below at fB. No curve, no second clamp.
- 0x383814 vsub s21,s20,s15: vertical -= blend (then 0x383878 *dt into [r5+8]).

## What the distance MEASURES (writer census of [comp+0x1a4..0x1ac])
Per-symbol scan of all CActorBaseComponent methods: written by ctor/ReInit (zero), Update
(0x36e74c, right after SetActorPosition), UpdateNavSimpleBehavior/NormalSimplified/
TransitionWithMovement/ClimbBox, TryEdgeGrab, UpdateFloorTesting, ResolveAirCollision —
ALWAYS immediately after a CActorBaseComponent::SetActorPosition (0x3a36c0) call.
**UpdateNavGlide (0x380e94..0x3813bc) NEVER writes it (0 stores; calls: GetActorPosition,
GetGlide, RefreshForcesGlide @0x380fbc, normalize, 2x CollisionMgr::GetIntersectionPoint).**
=> during a glide the cache is frozen at the last engine-set position = the TAKEOFF position:
   **d = 3D distance travelled since glide start.** Blend = glide-entry dip: f7=2 u/s extra sink
   at takeoff, linearly decaying to fB=0 over f9=16 u of travel. (s56/s57 proxy = height over nm
   is the wrong measure; kept as the ?s5=1 default for digest stability, control below.)

## GetGliderGravityHelper (0x1e1508)
= UpgradesManager map (std::map<int,SUpgrade>::operator[] 0x209dbc) lookup key 0x1f, returns
[SUpgrade+0xc]. SUpgrade layout (AddUpgrade 0x1e03c0): {u16 key, s16 level=-1, float base@+8,
float value@+0xc}; base = value at insert. Upgrade 0x1e045c: mode 0 value+=arg; mode 1
value = base*(1+k*arg); level stored at +2. **Base/level-0 value is data-driven** (ResetUpgrades
0x1e0780 iterates engine definition tables 0x481154/0x478e24; no bl callers of AddUpgrade, no
0x1f constant with a float in .text; game_config.gla has no upgrade table — analytics XML only).
In-page helper stays 0 (no upgrades) — additive into the vertical rate at 0x383784. NUMBER
inconclusive from static evidence; MECHANICS pinned (additive sink, upgrade-scaled, add/mul modes).

## Implementation + gates (branch s56-t1-glide; runner s58_t1_gate.py -> s58_t1_gate.json)
?s5=1 unchanged (proxy measure, digest-stable default); ?s5blend=1 = exact engine measure
(anchor captured at glide start, d = 3D distance from anchor, same closed form, helper 0).
| config | pass | errs | soup sha256 | nTri | routes | model | landed | landMs |
|---|---|---|---|---|---|---|---|---|
| default | PASS | 0/0 | 00ce7970e45adc85 (= LIVE) | 137893 | 10/10 | - | - | - |
| ?s5=1 (proxy) | PASS | 0/0 | 00ce7970 | 137893 | 10/10 | acc | True | 417 (=s57) |
| ?s5=1&s5blend=1 | PASS | 0/0 | 00ce7970 | 137893 | 10/10 | acc | True | 400 |
| ...&s5plunge=1 | PASS | 0/0 | 00ce7970 | 137893 | 10/10 | acc | True | 467 (=s57) |
| ?s5=1&s5sink=1 | PASS | 0/0 | 00ce7970 | 137893 | 10/10 | sink56 | True | 917 (=s57) |
| ?s5=1&s5ctl=1 | PASS | 0/0 | 00ce7970 | 137893 | 10/10 | acc+ctl | True | 450 (=s57) |

## Trajectory vs analytic (s58_t1_blend_check.json; plot s58_t1_traj.png)
- analytic vz = acc*sin(p) - sink56(p) - helper - max(fB, fB+(1-d/f9)(f7-fB)) evaluated from each
  page-reported state: exact config max |err| = **0.0048 u/s** (Glider, n=24; away-from-ground
  n=16: 0.0047), Plunge n=28: **0.0049** — rounding noise only, **well under 0.1**.
- control (proxy measure) MOVES: max |dvz(exact, proxy)| = **0.93 u/s** at t=50 ms (matched t,
  n=24); blend(d) shapes differ (anchor distance monotone 2->0 vs height proxy non-monotone).
- sink control fwd = 3.5 u/s (n=55) — s57 receipt reproduced; wrong-model calibration holds.

## Verdict vs acceptance
- Blend inputs pinned (virtual call = GetPosition; f7/fB/f9 shaping = linear clamp; helper
  mechanics): DONE. Level-0 helper NUMBER: inconclusive (data-driven table).
- Exact blend implemented behind ?s5blend=1 with trajectory vs analytic + moving control: DONE
  (0.0048 u/s < 0.1; control 0.93 u/s).
- Gates re-run (default digest, routes, s5, ctl, sink): DONE — all PASS, receipts reproduce.
