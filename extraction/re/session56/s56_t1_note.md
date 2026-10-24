# s56 T1 — engine glide model applied to the staged slice (branch s56-t1-glide @77dd3c6, NOT deployed)

## What landed
`playable/integration_lazy.html` S5 block, flag-gated (default-mode bytes unchanged):
- `?s5=1` — ENGINE MODEL per the s55 note: fwd = f5+(f6-f5)*(2/pi)*|p|, sink = f0+(f1-f0)*(2/pi)*|p|, pitch held at f10.
- `?s5old=1` — pre-s56 staged model (const fwd 16, sink 4+12*|p|) as control.
- `?s5legacy=1` — s53 placeholders (unchanged).
- `?s5acc=1` — NEW accumulator re-read (below). `?s5plunge=1` — GetGlide(1) 'Glider_Plunge' pitch0 -60.

## Gate results (s56_t1_gate.json; runner s56_t1_gate.py; all 6 configs)
| config | pass | errs | soup sha256 (prefix) | nTri | model | landed | landMs |
|---|---|---|---|---|---|---|---|
| default | PASS | 0 | 00ce7970 (LIVE-identical) | 137893 | - | - | - |
| ?s5=1 (Glider) | PASS | 0 | 00ce7970 | 137893 | engine | True | 917 |
| ?s5=1&s5plunge=1 | PASS | 0 | 00ce7970 | 137893 | engine | True | 767 |
| ?s5=1&s5acc=1 | PASS | 0 | 00ce7970 | 137893 | acc | True | 433 |
| ?s5=1&s5old=1 | PASS | 0 | 00ce7970 | 137893 | old | True | 1000 |
| ?s5=1&s5legacy=1 | PASS | 0 | 00ce7970 | 137893 | legacy | True | 933 |

**Default-mode digest identical to LIVE (00ce7970…/137893, routes 10/10) — acceptance met.**
s5 gate passes on BOTH glide models (engine + old control) — acceptance met.

## Trajectories (s56_t1_traj_metrics.json, plot s56_t1_traj.png)
Sign convention: vz < 0 = descending (z-up); fwd > 0 = horizontal speed; alt/m = drop/dist (positive = losing height).
n = per-frame in-page traj samples (~60 Hz; the s54-era ">=200 ms" gate compares absolute now vs a
relative t and never throttles — pre-existing, kept: more samples, no behavioural effect).

| run | mean vz (n) | mean fwd (n) | drop u | dist u | alt/m | analytic (fwd, sink, alt/m) |
|---|---|---|---|---|---|---|
| engine Glider p0=-45 | **-10.0** (55) | **3.5** (55) | 8.24 | 3.15 | 2.618 | 3.5, 10.0, 2.857 — vz & fwd EXACT |
| engine Plunge p0=-60 | **-12.0** (46) | **4.333** (46) | 8.28 | 3.25 | 2.546 | 4.333, 12.0, 2.769 — vz & fwd EXACT |
| acc re-read p0=-45 | -9.278 (26) | 4.419 (26) | 3.23 | 1.86 | 1.737 | series: vz(t=17ms) = -8.446 w/ blend=2 → measured -8.45 EXACT |
| old staged (control) | -13.42 (60) | 16.0 (60) | 8.36 | 15.73 | 0.531 | reproduces s55's live -13.42 exactly |
| s53 legacy (control) | -9.875 (56) | 18.0 (56) | 8.53 | 16.51 | 0.517 | gravity -25 ramp from +2 |
| wrong-param (analytic, sink x2 / fwd x0.5) | -20.0 | 1.75 | - | - | 11.429 | every comparison quantity moves |

These are deterministic integrations, so the engine-model agreement is FORMULA EXACTNESS
(vz and fwd equal to analytic at 3+ decimals across 46-55 samples per run), not a statistical
correlation; the wrong-parameter and legacy controls both move every tabulated quantity
(parameter-sensitivity calibrated). The engine model's alt/m (2.618) trails the instantaneous
2.857 because the wall-evade hold stops horizontal advance while descent continues (dist underestimates).

## SEMANTIC CONFLICT found while re-reading RefreshForcesGlide (0x3836b0..0x383a08, ARM)
The s55 note names f0/f1 the "sink" and f5/f6 the "forward speed". The byte-level re-read says the opposite:
1. The f0/f1 formula s10 = f0+(f1-f0)(2/pi)|p| feeds the accumulator branch: pitch<=0 -> acc += s10*dt toward
   f1 (0x3839dc, guarded acc<f1); pitch>0 -> acc -= s10*dt toward f0 (0x383724, guarded acc>f0). So f0/f1 are
   AIRSPEED CLAMPS [4,16] u/s and the formula is the acceleration rate (u/s^2), not the sink.
2. The output velocity (0x383858..0x383880): X = -sin(f6*pi/180)*acc*cos(p)*dt, Y = cos(f6*pi/180)*acc*cos(p)*dt,
   Z = (sin(p)*acc - [f5+(f6-f5)(2/pi)|p| + gravityHelper] - blend)*dt. The f5/f6 family lands in the VERTICAL term.
3. f6=6 does DUAL DUTY: fwdMax in the speed formula AND a 6-degree side-slip tilt of the horizontal direction
   (cosf/sinf of f6*pi/180 at 0x38381c..0x383838).
4. Blend (f7=0, f8=2, f9=16) SUBTRACTS in Z near ground: descent is up to 2 u/s FASTER within f9 of the ground
   (landing-assist, not flare). Blend distance in-page = height over nm ground; engine dist = |virtual-call
   position - actor| (target object of the blx r3 call not pinned).
Both models are implemented so future engine-side capture (or locating the StartGlide acc-init, absent from
StartGlide/StartGlideFromGrapnel/UpdateNavGlide/SetInitialGlideAngle per the +0x530-base scan) can discriminate.
Until then the s55-note model stays the ?s5=1 default per the session brief; this is an OPEN fidelity question,
not a settled claim (one signal each way).

## Float naming table (consolidated; read sites = ARM libKRHP.so)
| f# | Glider | Plunge | status (s55 site-scan + s56 pools) | implement now? |
|---|---|---|---|---|
| f0 | 4 | 4 (identical) | s55-note sink-min / s56 re-read airspeed clamp-lo; RefreshForcesGlide 0x383704 | YES (both models) |
| f1 | 16 | 16 | clamp-hi / sink-max; 0x383708 | YES (both models) |
| f2 | 14 | -80 | unread by the 6 glide functions (site-scan negative) | no |
| f3 | 4 | -30 | unread | no |
| f4 | 16 | 40 | the 0x3836e4 read [r3+0x18] is the ACTOR pitch (deg) via [r4+4], not template f4 (s55); template f4 unattributed | no (actor state drives pitch) |
| f5 | 1 | 1 | fwd-min (s55) / base sink (s56 re-read); 0x38374c | YES |
| f6 | 6 | 6 | fwd-max / sink slope AND 6-deg side-slip angle; 0x383750 + 0x383824 | YES |
| f7 | 0 | 0 | blend min; 0x38375c | YES (acc model) |
| f8 | 2 | 2 | blend max; 0x383760 | YES (acc model) |
| f9 | 16 | 16 | blend distance; 0x383798 | YES (acc model) |
| f10 | -45 | -60 | initial pitch DEG (SetInitialGlideAngle 0x380e78; hard default -30) | YES |
| f11 | -60 | -80 | entry-setup pair of f10 (StartGlide/FromGrapnel ldr [r3,#0x34]) - site-attested only | no (entry dynamics) |
| f12 | 30 | 40 | unread | no |
| f13 | 35 | 6 | StartGlideFromGrapnel attested | no |
| f14 | 1.25 | 0.1 | written at StartGlide ([r4,#0x40]), runtime state field | no |
| f15 | 0.05 | 35 | written at StartGlide | no |
| f16 | 45 | 6 | unread | no |
| f17 | 0.5 | 30 | unread | no |
| f18 | 30 | 30 | NOT a component read (s55 corrected the 0x380e34 annotation artifact) | no |
| f19 | 30 | 100 | unread | no |
| f20 | 40 | 15 | StartGlideFromGrapnel attested ([r2,#0x58]) | no |
| int1 | 0 | 1 | GetGlide gadget slot (byte-proven s55 T3) | YES (slot select) |
| int2 | 0 | 0 | s55 T3 corrected s54's 600 (off-by-one artifact); unconsumed | no |

UpdateNavGlide pools resolved (s56_t2_pools.py): 90, pi/180, 180, 0.001, 360, -180, 360, 0.001, 180, 360, -180, 360
- it is NAV STEERING (angle wrap to +/-180/360 with 0.001-scale rates), NOT stick control; no pitch clamps,
  roll max or yaw rate live there. CLevel::s_glide* and k_glide* remain DEAD (s55 verdict stands).

## Verdict vs acceptance criteria
- Apply engine model on a branch with flags: DONE (77dd3c6; ?s5=1 engine default, ?s5old=1 old, ?s5legacy=1 untouched).
- Trajectories tabulated/plotted for decoded Glider+Plunge vs old vs wrong-parameter control vs analytic: DONE (exact matches; controls move).
- Three gates re-run + s5 gate on both models, default digest identical: DONE (6/6 PASS, 0 errors, 00ce7970/137893 everywhere).
- Name remaining floats with read sites + decide implement-now: DONE (table above; f2/f3/f12/f16/f17/f19 confirmed unread;
  UpdateNavGlide = nav steering only; implement-now set = f0/f1/f5/f6/f7/f8/f9/f10 + int1 slot).
- NOT done: engine-side trajectory capture to settle the f0/f1-vs-f5/f6 semantic (no engine reference available in-session).
