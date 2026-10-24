# s56 T2 — glide control inputs + auto-leveling (?s5ctl=1, branch s56-t1-glide @ba85416+)

## PROVENANCE (stated per ground rules)
- DECODED: pitch->sink/speed mapping (f10 initial pitch; f0/f1 pair; f5/f6 pair; 2/pi normalization),
  and the f6=6-degree side-slip tilt of the horizontal direction (RefreshForcesGlide 0x383824..0x383838:
  horizontal dir = (-sin(f6*pi/180), cos(f6*pi/180)) of the local frame).
- NOT ENGINE-DECODED (placeholders, labeled in-page): the auto-level coefficient k=2.0/s and any pitch
  clamps. Evidence chain: CLevel::s_glide* family DEAD (s55: zero readers AND writers), template floats
  f2/f3/f12/f16/f17/f19 unread by the 6 glide functions (s55 site-scan), UpdateNavGlide pools resolved
  this session (s56_t2_pools.py) contain ONLY nav-steering constants (90, pi/180, 180, 0.001, 360, -180)
  - no stick-control or auto-level constants found in-session. The task's acceptance is about the
  CONTROL MECHANISM with a known analytic outcome, which does not require those constants.

## Scripted sequence (two variants; deterministic, no UI)
- ?s5ctl=1:            ramp -45 -> -60 deg by t=0.4s; HOLD -60 in [0.4,1.2)s; auto-level pitch = -60*exp(-2.0*(t-1.2)) after.
- ?s5ctl=1&s5ctlEarly=1: ramp in [0,0.25); hold in [0.25,0.45); decay from t=0.45 (early release so the
  exponential precedes touchdown - the default variant lands at ~800 ms inside the hold window).
Side-slip: glide direction rotated by -6 deg in ctl mode (decoded); traj records pitch (deg) and
heading offset (deg) every frame; gate receipts carry ctl flag.

## Results (s56_t2_ctl_validation.json / _2.json; both runs gate PASS, 0 errors, landed)
### Variant A (?s5ctl=1, landed 800 ms, 48 traj frames, 0 errors)
| window | n | metric | measured | analytic |
|---|---|---|---|---|
| hold [450,1150]ms (cut at 800 by landing) | 22 | mean vz | **-12.0** | -12.0 (sink at -60 deg) EXACT |
| | 22 | mean fwd | **4.333** | 4.333 EXACT |
| | 22 | mean pitch | **-60.0** | -60.0 EXACT |
| | 22 | mean heading offset | **-6.0 deg** | -6.0 (decoded f6 side-slip) EXACT |

### Variant B (?s5ctlEarly=1, landed 883 ms, 53 frames, 0 errors)
| window | n | metric | measured | analytic |
|---|---|---|---|---|
| hold [260,440]ms | 11 | vz / fwd / pitch / slip | -12.0 / 4.333 / -60.0 / -6.0 | all EXACT |
| level [460,883]ms | 26 | auto-level rate fit ln(-pitch) vs t | **k = 2.0000 /s** | 2.0 /s |
| level | 26 | per-frame vz residual vs decoded mapping vz = -(4+12*(2/pi)*abs(pitch)) | max 0.0047 u/s, mean 0.0026 | 0 (frame quantization) |
| level | 26 | pitch vs closed form -60*exp(-2(t-0.45)) | max err 0.046 deg | 0 |

Sign conventions: pitch < 0 = nose-down (deg); vz < 0 = descending; slip negative = left of base heading.

## Sensitivity controls (the comparison quantities move)
- no-ctl engine run (T1): pitch -45 constant, sink 10.0, fwd 3.5 vs ctl hold -60/12.0/4.333 -> all move.
- wrong-parameter analytic control (T1): sink x2 / fwd x0.5 at -60 deg -> sink 24, fwd 2.167, alt/m 11.1 -> all move.
- In-page controls carried by the same traj machinery (s5legacy / s5old, T1) differ in every measure.

## Verdict vs acceptance
- Control implemented with template values + auto-level, validated by a scripted sequence with known
  analytic outcome: **MET** (constant pitch -> constant sink EXACT; zero input -> exponential return at
  the chosen coefficient with k-fit = 2.0000 and per-frame mapping residual <= 0.005 u/s).
- Caveat recorded: the coefficient itself and pitch clamp bounds are placeholders (provenance above);
  the decoded pieces exercised are the pitch->forces mapping and the f6 side-slip (both EXACT).
