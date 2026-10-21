# T4 — NAVMESH WALKING FINISHED IN THE BROWSER (slipped twice, done this session) + harness re-check

## Part 1: headline harness re-run with PER-ROUTE fail isolation (s44_t4_harness_rerun.py)

The s42 bug (one shared ctx.fails per mode; row['fail'] = ctx.fails[-1] borrowed the
previous route's record on stall paths) affected FAIL ATTRIBUTION ONLY. Re-run with
route-tagged fail records (isolation by construction — every fail appended with its
route id; the s42 'returns without appending' paths now tag explicitly):

- navmesh + stepignore 0.55: **15/40 ok** (matches s42 headline)
- full collision: **10/40 ok** (matches)
- ghost (pure polyline, L.follow): **36/40 ok** (matches)
- null (shuffled spawn->destination pairing, seed 42): **4/40 ok** (matches)

All four headline counts are UNAFFECTED by the attribution bug. Per-route fail records:
31 tagged fails across the navmesh + null runs (s44_t4_result.json per_route_fails).
Two independent signals: (a) verdicts are computed per-route independently of the fail
list (code inspection); (b) the isolated re-run reproduces all four counts exactly.

## Part 2: the walker IN THE BROWSER (playable page, staged — nothing deployed)

Page: playable/walktest.html on local branch **gh-pages-staged-s44** (off gh-pages
36788a9; local commit, NOT pushed — staged = local and unpushed). Components:
- walktest.js: 1:1 JS port of the harness engine (soup ground_at, blocked with
  stepignore 0.55, nearest_walls, try_slide, nm_ground, astar with Python-heapq
  tuple-order MinHeap, follow_nm). np.linalg.norm sites use sequential sqrt-sum
  (BLAS ddot order); math.hypot sites use Math.hypot.
- walktest_run.js: runner + gate (console.error/window.onerror capture, 1024x1024
  top-down route map canvas, per-route rows, pixel statistics).
- walktest_routes.js: first 24 same_region routes (s40_t6_routes4) + per-route
  harness expectations (generated).
- .nm parse in JS from the USER'S zip: game_config.gla (26.3 MB member view) ->
  TDKR.glaSlice -> GothamCity_502299_navdata.nm -> big-endian u16/f32 parse, with a
  self-check against Python-reference constants (vcount 30824, ccount 31647, first/
  last vertex, first/last cell) = PASS in the run.
- gc_collision.bin (5.4 MB derived soup, 137,893 tris) is staged next to the page as
  an UNTRACKED file — the branch ships code only; a user-file soup path is future work.

## Gate (the actual headless run, Chromium via agent-browser, zip = user release file)

- page loads, file input -> 895 MB zip read lazily; game_config.gla 26.3 MB;
  .nm self-check PASS; soup 137,893 tris / 23,334 grid buckets.
- console errors: **0** (window.onerror + console.error hooked).
- routes: **24** run in-browser, wall time 4,030 ms total (including zip read).
- verdict agreement vs harness: **24/24**; distance agreement (<0.25 m):
  **24/24** (max delta 0.038 m = the harness's 1-decimal rounding).
- pixel statistics (route map canvas): mean RGB (19.53, 24.69, 33.96), stdR 23.04 —
  non-blank, structured render (island-shaped navmesh + colored route paths;
  s44_t4_map.png).

Two independent signals: (a) the JS engine reproduces the Python harness verdicts and
distances on all 24 routes (bit-level distance agreement at harness precision); (b)
independent node parity check on 4 routes BEFORE the browser run gave identical
verdicts + distances (305.2/321.0/382.5/1076.0), so the browser result is not a
browser-specific accident.

## Verdict

T4 PASS: headline counts confirmed (15/40, 10/40, 36/40, 4/40 — attribution bug
did not touch counts); navmesh-surface walker now runs in the browser from the
user's zip with 24/24 route agreement vs the harness. Remaining known gaps (unchanged
from s43 classification): 3 elevated-deck registration gaps + 2 navmesh coverage holes
in the harness population; the collision soup is still a staged derived file, not
parsed from user files in JS (named next).

Artifacts: s44_t4_harness_rerun.py, s44_t4_result.json, s44_t4_routes24.json,
s44_t4_walktest_engine.js / s44_t4_walktest_run.js / s44_t4_walktest.html (deployed to
the staged worktree as walktest.js / walktest_run.js / walktest.html),
s44_t4_walktest_gate.json, s44_t4_map.png, s44_t4_node_parity.js + s44_t4_node_body.js.
