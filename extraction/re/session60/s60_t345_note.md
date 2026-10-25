# SESSION 60 — T3/T4/T5 notes (page work on branch s56-t1-glide)

## T3 — merc rig validation that DISCRIMINATES (s60_t3_mercval.json + s60_t3_gate.json)
- Python port of readBdae2 (s60_t3_mercval.py) re-derives both layouts from file headers.
- V1 skin weights: per-vertex sums EXACTLY 1.0 (1449/1449 batman, 1294/1294 merc,
  frac-in-window 1.0); shuffled-weights null: 8.0% (batman) / 19.8% (merc) in window
  (sd 0.72-0.74); deliberately-wrong case (+0.05 offset): 0% in window. CALIBRATED.
- V2 bone indices: max joint 30 < nBones 31, 100% of indices valid (both rigs).
- V3 bbox: batman height 1.9164, merc 1.8713 (both plausible humanoid, z-up, feet ~0).
- V4 |node-hierarchy world bind origin - skin-weighted centroid|: batman median 0.0888 u
  (n=31), merc 0.0750 u (n=31); permuted-mapping nulls 0.59-0.91 (~7-12x) - REPRODUCES s59
  exactly (bind origin = node world transforms, NOT the invB translation row).
- V5 (in-page): rest-pose render height 1.8713, feetZ -0.0012 (upright, feet on ground).
- IoU (raw WebGL1 + readPixels, 256 -> 64 grid, exact projection match with Python):
  **page-vs-numpy-merc-ref 0.9516**; batman-ref cross-null 0.6922; x-flipped 0.6772.
  Gate PASS (0 console/page errors). Default soup 00ce7970/137893 unchanged.
- Hurt/Death wired: ENEMY_CLIPS + _223_enemy_hurtl (1.666 s) + _250_enemy_death1 (1.2 s),
  LoopOnce+clamp; dispHurt 7.14 / dispDeath 12.91 u/vertex-sample > 0; hurtDone/deathDone
  flags true at report; wrong-clip control 1.76 != idle 1.30.
- NOTE: in-page applyBoneTransform at load time returns zeros (three r160 skeleton state
  before first render) - the rest-pose silhouette therefore uses the STATIC bind geometry;
  skinning itself is validated by the displacement battery (5 clips + wrong-clip control).

## T4 — combat slice with the REAL merc (s60_t4_gate.json + s60_t4_viewer.png)
- enemy_viewer.html loads Bane_mercenary.bdae + batman_anims.bdae from the USER ZIP via
  lazy gla slices; FK = node hierarchy (BIPED parents, nearest-key rotation channels,
  root position channel, qmul/qrot Hamilton), skin = sum_k w_k M_{J_k} invB_{J_k} v
  (the pairing three.js validated); rendered as a top-down point cloud that POSES PER STATE.
- Channel-name gotcha fixed: CH table names carry a '-node' suffix.
- Machine: s59 states + **Run** (alerted && dist > 14 u -> Run chase).
- Gate PASS 0 errors: controls (60 u far -> Idle; 15 u behind facing -> Idle);
  8 u in-cone -> Walk; 15.5 u in-cone -> Run; 8 u -> Walk; hit 5 -> hp 115 Hurt -> Walk;
  hit 10 -> 105 Hurt; drain -> 0 Death; stateSeq Idle,Walk,Run,Walk,(Hurt,Walk)xN,Death;
  wrong-clip control: Idle-state vs Walk-clip skin diff 0.2211 u/vertex (> 0.05).
- The uncommitted s59 T4 enemy_viewer.html work is now committed on the branch.

## T5 — ResolveAirCollision re-anchor in the exact-blend path (s60_t5_gate.json)
- ?s5reanchor=1&s5wall=<u>: virtual wall along the glide heading; crossing clamps the
  horizontal step (collision response) and RESETS S5.anchor to the resolved position
  (engine: ResolveAirCollision 0x398570 stores into [comp+0x1a4] @0x3987a4/74 - s59).
- Gate PASS: wall at 3 u -> hit @267 ms, blend dip RESTARTS (+0.32 jump in the 200-ms
  trajectory), vertical trajectory vs piecewise analytic (vz = acc*sin(pitch) - fwd56
  - blend(d from ACTIVE anchor), acc=16 seeded, pitch -45) max err **0.0047 u/s** (n=25).
- Controls: no-wall run reanchors = [] (PASS); flag-gated; default soup 00ce7970/137893
  re-verified after the patch (s60_default_gate.json), routes 10/10.
- Helper level-0 = 0.0 stands: "no evidence of a nonzero value" (code-verified s59 T1;
  no live setter for key 0x1f; kept behind the labelled constant in the page header).
- Operational note: the grapple-target waypoint decode is gated on ?s5=1 (S5ON) - the
  s5blend-only runs fall back to the BFS edge path and may skip the glide; the gate now
  uses ?s5=1&s5blend=1.

## T6 — memory/GPU: NO real-GPU gpucheck block supplied this session -> standing record:
  environment-dominated (swiftshader copies ~261 MB native residual; peak ~560-592 MB,
  first image ~8.5-9 s); pending a real-GPU paste-back via ?gpucheck=1. No time spent.
