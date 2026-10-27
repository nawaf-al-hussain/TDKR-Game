# SESSION 63 — T3: second real re-anchor case — PARTIAL (machinery landed, geometry blocks the hit)

## What landed (committed on s56-t1-glide)
- `?s5air=N` (s63_t3_patch.py generator, single-match asserts, node --check PASS on the
  139 KB module): the grapple-elevated anchor - the glide starts N u ABOVE the ledge anchor
  (`P.z += S5AIR` after the ledge ground-snap, BEFORE the takeoff anchor is taken, so the
  blend measures from the elevated start). Provenance `s5air` recorded on BOTH s5 finalize
  paths. Defaults unchanged (s5air absent = 0 = the s62 behaviour).

## Gate runs (s63_t3_gate.py, playwright, local HTTP, soup digest 00ce7970/137893 in ALL runs, 0 console/page errors in ALL runs)
- control ?s5air=0: reproduces s62 exactly - 2 real re-anchors @17/300 ms, landed,
  pre-hit blendD = 0 (the ledge-adjacent facade is hit at the FIRST sample: blend never
  decays - the documented s62 case).
- ?s5air=28: 144 traj samples, landed, ZERO re-anchors. The glide CLEARS the near facade
  (its top is below ledge+26) and lands 16.5 u out on the street. Clean run, no hit.
- ?s5air=180: 361 traj samples, phase TIMEOUT (not landed), ZERO re-anchors. The glide
  envelope ends ~50 u out; the nearest far facade is at 64 u.

## The geometry blocker (measured, not assumed)
- Glide descent ratio 2.857 u/u (sink 10.0 / fwd 3.5 at pitch0 -30 deg, engine default).
- Facade distances along the picked glide direction: 0.6 u (the ledge-adjacent wall, the
  control's hit) then 64+ u (the s62 detect-only census: 8/16 rays, first hits 64..156 u).
- Mid-air reach envelope: (ledge 9 u + N)/2.857 forward, capped by the glide phase timeout
  at ~50 u. For a decayed-blend hit at distance d the start must satisfy N = 2.857*d - 0.5
  => d in [2.5 .. 52] u of reachable facade band. Intersection with {0.6, 64+} = EMPTY.
  The near facade is cleared for any N >= 28; the far ones are beyond the envelope for
  every N that keeps the flight inside the phase timeout.

## Verdict
PARTIAL against the acceptance criterion (a second real re-anchor with a decayed blend and
a measured dip restart). The re-anchor machinery itself is proven altitude-independent
(the control reproduces; both air runs are clean), and the analytic vz comparator is wired
(s60 closed form; max err 4.25 u/s is dominated by the acc transient before steady state -
the steady-state segment matches as in s60).
Finish (0.25 session): extend the facade census down to 2..12 u and either pick a glide
direction whose mid-band (5..52 u) contains a wall, or lift the glide phase timeout for
s5air runs so N ~= 182 reaches the 64-u band.

## Artifacts
s63_t3_patch.py (generator), s63_t3_gate.py (harness), s63_t3_gate.json (all three runs),
the patched page committed on s56-t1-glide.
