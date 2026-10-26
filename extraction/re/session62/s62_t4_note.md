# SESSION 62 — T4: REAL collision-soup air-collision re-anchor for the glide (?s5real=1) — GATE PASS

## What was built
The s60 T5 virtual-wall re-anchor case (?s5reanchor=1&s5wall=N) now has its REAL-soup
counterpart. With ?s5real=1 the glide step runs the walker's capsule-vs-soup query
(walktest.js blocked(), r=0.45) at the DESTINATION altitude (nz - 0.9, the step about to
be committed) and, on the not-blocked -> blocked EDGE TRANSITION, resolves the step with
the walker's wall-slide (try_slide) and RE-ANCHORS the glide at the resolved position
(ResolveAirCollision analogue - engine 0x398570 stores the resolved pos into the glide
cache; here S5.anchor = resolved pos, blend distance restarts). Edge-triggered, so
sliding along one facade counts once; a second facade entry counts again. The s5 gate
object gained provenance on BOTH finalize paths (landing + glide-timeout):
from/tgt/wpsN/realStaged.

## Three defects the gate caught (all fixed by patches 2/3/4/6; generators kept)
1. s62_t4_patch.py (v1) placed the REAL block BEFORE `const nz` in the same block scope
   -> TDZ ReferenceError every glide frame. patch2 relocates the block after the nz/gz
   lines, still before the P commit (anchor z stays pre-move, identical to the s60
   virtual-wall block).
2. v1 staging probed facades at ft0 - 3.0 = 3 u BELOW the ground plane where no collision
   triangles live -> never fired. patch3 (v2) probed glide altitudes - and exposed that
   a retarget "8 u short of the facade" lands on a point with NO navmesh under it
   (nm_ground = -1e9 void): the glide fell straight down (x,y frozen, z 8 -> -81.8,
   gz null throughout, 6 s timeout; 3 identical probe runs s62_t4_probe2.py). Deeper:
   with the engine-default glide (pitch0 fixed -45, sink ~10 u/s) the reach from the
   picked ~9 u ledge is only 2.51 u, so a 12+ u facade is geometrically unreachable
   mid-glide. patch6 (v3) = DETECT-ONLY staging: records the 16-ray facade census
   (8/16 rays hit facades at 64..156 u at glide altitudes) and leaves the pick untouched.
3. patch4: s5Begin declared `const tgt = s5PickEdge()` while staging retargets tgt ->
   'Assignment to constant variable' the moment staging fired (v1 masked it by never
   firing). const -> let.
patch5: provenance exposure (window.__S5DBG + from/tgt/wpsN in both s5 finalize paths).

## Gate results (s62_t4_gate.json, deterministic pick: from (-462.24,-767.72) z 1.11,
## tgt (-443.25,-715.03) z 8.30, wpsN 8428)
- ?s5=1&s5blend=1&s5real=1: **2 re-anchors kind 'real'** - #1 @17 ms pos (-439.761,
  -705.340) z 9.279, #2 @300 ms pos (-438.674, -702.325) z 8.707 (two distinct facade
  entries; edge-trigger worked); wallHit = #1; **landed** (25 traj samples);
  **blendD dip restart measured @300 ms** (post-reanchor min blendD < pre max - 0.5 -
  the anchor-distance reset, i.e. the s60 virtual-wall semantic reproduced on the REAL
  collision path); soup digest 00ce7970.../137893 PASS; 0 console errors, 0 page errors.
- Control ?s5=1&s5blend=1 (no s5real): reanchors == [], landed, digest PASS, 0 errors.
- Verdict: **PASS**.

## Honest scope
The demonstrated pattern is the NATURAL facade-adjacent-ledge hit (the picked portal
ledge sits against a building face, so glide step 1 crosses real collision, slides, and
a second facade is entered 283 ms later). Mid-glide hits of distant facades are
unreachable under the engine-default glide physics (fixed pitch0; reach 2.51 u from this
ledge) - recorded, not overclaimed. The ?s5reanchor=1&s5wall=N virtual-wall case (s60)
remains the controlled mid-glide geometry test; ?s5real=1 adds the REAL-soup path.
Default (no flags) behaviour untouched: soup digest = LIVE 00ce7970/137893 in every run.
