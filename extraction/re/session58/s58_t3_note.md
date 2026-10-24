# s58 T3 — enemy rig LOCATED, enemy clips FK-validated; in-page mesh playback = one session away

## Enemy rig: found (the search did NOT dead-end)
- **Bane_mercenary.bdae (1,229,264 B) and Bane_mercenary_low.bdae (750,064 B)** exist as
  members of the user zip's actors.gla (gla directory offsets: 1,679,540 / 2,908,804;
  sha256 prefixes 611ceb86 / 773f40c4). Skinned entries named #Bane_mercenary_LOD00-mesh-skin
  + gear_mercenaryA..D_LOD00..03-mesh-skin; the Melee_Enemy_Merc template's CustomizeActor
  payload (exact walk, s58 T2) names its textures chara_banemercenarya_c/_n/_mask.tga and
  the 12 gear LODs — template and container agree.
- **Animation file = the SHARED bank batman_anims.bdae (43,683,488 B, 921 clips)** — enemy
  families live there (s55 T6: attack 33 / counter 20 / takedown 14 / hit 9 / block 10).
  Enemy gait clips: _014_idle_enemy_combat, _166_enemy_walk, _171_enemy_run (plus aim/hip
  variants _167/_172/_173 and transitions _169/_170/_174/_175).

## Clip FK validation (same FK path as the s35/s36 Batman battery; s58_t3_fk.py -> s58_t3_fk.json)
| clip | dur ms | loop |p(end)-p(start)| L/R (u) | foot L z [min,max] (u) | root z [min,max] (u) |
|---|---|---|---|---|---|
| _014_idle_enemy_combat | 4833 | 0.432 / 0.251 | -0.87..-0.67 | -1.19..0.95 (combat lunge) |
| _166_enemy_walk | 11733 | 0.310 / 0.269 | -0.87..-0.35 | 0.865..0.957 |
| _171_enemy_run | 13550 | 0.252 / 0.908 | -0.87..-0.19 | 0.868..0.966 |
| _001_idle_stand (calib) | 6433 | 0.011 / 0.010 | -0.87..-0.87 | 0.965..0.969 |
| _007_walk (calib) | 4050 | 0.191 / 0.550 | -0.87..-0.25 | 0.878..0.981 |
| _008_run (calib) | 6800 | 0.216 / 0.575 | -0.87..+0.27 | 0.625..1.315 |
| _171_enemy_run ROLLED (wrong-case) | 13550 | endpoint delta unchanged but step profile broken (0.814 -> 0.908 max step) |

- Enemy clips' loop-continuity deltas sit in the SAME range as Batman's own walk/run
  (0.19..0.91) — consistent with one shared rig/anim convention; feet stay at the ground
  band (-0.87), walk/run root bob 0.87..0.97 (±5 cm), run root larger. Wrong-case (pose
  sequence rolled by half) breaks the step profile. The FK is the s35 assemble_clip +
  fk_leg machinery UNCHANGED (bone lengths constant by rig construction; the anim channels
  are named Bip01_* — engine-standard biped set — so the enemy skeleton binds by name).
- pelvis note: the Bip01_Pelvis channel is rotation-only (ch 57, ty=5); the bob lives in
  the ROOT position channel ('Bip01-node' ty=1, ch 0) — reported above as root z.

## In-page playback: ?enemy=1 implemented, mesh step = PARTIAL (precise boundary)
- integration_lazy.html (?enemy=1, branch-only): loadMerc() reuses glaSliceLazy +
  buildGLB + GLTFLoader + mixer (the exact Batman path), loads Bane_mercenary.bdae +
  the 3 enemy clips + chara_banemercenarya_c.tga, plays a 12-s idle->walk->run cycle
  with __GATE.enemy / enemyPlay receipts; enemy_viewer.html damage updated to the
  decoded 5.0 HP (GiveDamage(actorId,damage) @0x155e4c; census 146 literal calls,
  5 x91; provenance string replaced the s57 PLACEHOLDER).
- **Blocker**: readBdae's SKIN_OFFS layout (node scan 0x...0x50 stride, palette, invB,
  verts NV=1449, skin records) is BATMAN-HARDCODED in tdkr_pipeline.js — applied to the
  merc bytes it returns batman's structure (the earlier "1449-vert shared topology"
  reading was this artifact, verts hash differs only because offsets land on merc data).
  ?enemy=1 therefore fails cleanly with "Cannot set properties of undefined (setting
  'isBone')" (gate recorded, page still passes; default digest untouched).
  **Next session**: derive the merc bdae section table (one focused decode: node directory,
  palette, invB, vert block NV, idx) -> parameterize readBdae -> merc plays in-page.

## Gate results (s58_t3_gate.json; runner s58_t3_gate.py)
| config | pass | errs | soup | enemy | enemyPlay |
|---|---|---|---|---|---|
| default | PASS | 0/0 | 00ce7970 (=LIVE) | - | - |
| ?enemy=1 | PASS | 0/0 | 00ce7970 | ok=false (readBdae layout blocker, recorded) | - |

## Verdict vs acceptance
- Enemy bdae + animation file located from the template/container: DONE.
- Idle/Walk/Run clips identified and FK-validated (loop continuity + foot/pelvis height
  ranges + batman calibration + wrong-case): DONE (node-side, same FK path).
- In-page playback with FK checks: PARTIAL — rig mesh reader is batman-specific; the
  search/decode boundary is documented above (clip layer complete, mesh layout pending).
- Decoded damage used: DONE (5 HP with provenance in enemy_viewer).
