# SESSION 64 — T2: SECOND REAL RE-ANCHOR CASE — PASS (real soup facade hit with a decayed blend, dip restart, landed)

## What was blocking s63
The s63 geometry analysis used descent ratio 2.857 u/u (the sink56 COMPARATOR: sink 10.0 /
fwd 3.5). The LIVE glide runs the acc model (seed acc = f1 = 16 at pitch -45 deg):
vz 14.81, fwd 11.31 -> descent ratio **1.31 u/u** (page receipt values). With the correct
ratio the reachable band for a decayed-blend hit at distance d is start-altitude
~ 1.31*d + hit-alt, so the 64-u facade IS reachable from a ~94 u start - the s63 "empty
intersection" was a model mismatch, not a city-geometry fact.

## Page patch (s56-t1-glide)
- ?s5airto=<ms>: glide phase-timeout override; 0/absent = engine-default 6000 ms
  (unchanged behaviour). 3 single-match edits (S5AIRTO const, timeout comparison,
  timeout-receipt provenance s5airto). node --check PASS on the extracted script.
  Defaults unchanged: s5air/s5airto absent -> bit-identical s62/s63 behaviour.

## Gate runs (all 4: soup digest 00ce7970/137893 byte-identical, 0 console/page errors)
1. control-s62 (?s5real, s5air=0): reproduces s62 exactly - 2 real re-anchors @17/300 ms,
   pre-hit blendD = 0 (1 sample), landed, 25 traj samples.
2. **air-85-lifted (?s5real, s5air=85, s5airto=22000): SECOND REAL RE-ANCHOR.**
   - 1 real re-anchor @ t=3233 ms, pos [-427.424, -671.103], z=45.80, kind='real'
     (wallHit receipt = same event).
   - Pre-hit blend decay: 194 samples, blendD max **60.306 u** (acceptance: > 4 u).
   - Dip restart: blendD 60.3 (pre-hit) -> 0 (anchor reset at the re-anchor) -> 0.247
     regrowing post-hit (the strict analyzer flag compares the boundary sample at t_hit,
     whose blendD is already post-reset; the 60.3 -> 0.247 transition in the receipts is
     the dip).
   - Landed; gate pass=true; 371 traj samples.
   - Analytic vz comparison (s60 closed form at the page pitch): max err 4.2479 u/s over
     the +/-1.5 s window (n=181; 371 samples overall) - the same acc-transient dominance
     s60 measured; the steady-state segment matches.
3. air-185-lifted (calibration point): 0 re-anchors, landed - at 185 u elevation the
   acc-model glide passes the 64-u facade at ~110 u altitude (1.31 ratio) -> no hit.
   This negative run PINNED the live descent model and motivated the s5air=85 pick.
4. nosoup-staged-85 (s5real OFF, s5air=85): 0 re-anchors, glide timeout (361 samples,
   not landed) - the staged collision model cannot re-anchor mid-air, so the run-2
   re-anchor is attributable to the REAL soup facade hit, not the staged machinery.

## Verdict
PASS against the acceptance criterion (a second real re-anchor with a measured pre-hit
blend decay and a dip restart, with controls). The re-anchor machinery is now exercised
at two independent geometries: the s62 ledge-adjacent first-sample hit (blendD 0) and
the s64 64-u facade hit at 60.3 u of blend travel.

## Artifacts
s64_t2_patch.py (3 asserted edits), s64_t2_gate.py -> s64_t2_gate.json (4 runs),
the patched page committed on s56-t1-glide. Defaults unchanged (all new flags off).
