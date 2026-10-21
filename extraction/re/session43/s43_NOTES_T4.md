# T4 — DISAGREEMENT CLASSIFICATION DONE (+ s42 misattribution bug found & fixed); browser walker adoption NOT completed in time-box (honest)

## The 10 "navmesh/soup height disagreements" re-classified (rerun with per-route fail isolation)
FINDING FIRST: s42's classifier shared one ctx.fails list across all 40 routes and
reported ctx.fails[-1] per route — routes that stalled WITHOUT appending a fail
(slide-stall path in follow_nm) BORROWED the previous route's failure record.
Routes 41-47 were misattributed to route 39's elevated-deck failure. Honest
reclassification of the 10:
1. GENUINE elevated-deck height disagreements: 3 —
   - route 39 (-319,-718) z=8.88: soup walkable levels {-0.23 street, 6.34 ledge,
     8.88 deck}; navmesh ramp cells 8.31..8.91 — the walker tops out at 8.31 and
     the soup deck is 0.57 higher = REGISTRATION GAP on an elevated deck over street.
   - route 45 (-279,-754) z=8.88: same deck family (soup {-0.23,6.34,8.88}).
   - route 46 (-708,-697) z=8.88: soup {6.34, 8.88}, no street below = structure
     deck (overpass/plaza) with the same ~0.57 gap.
2. GROUND-LEVEL NAVMESH HOLES: 2 — routes 37 (-119,-760) and 61 (-81,-923):
   walker 'fell' at z=0.21 where soup walkable ground EXISTS (0.0) — the navmesh
   has no cell under the next step (coverage gap), not a height disagreement.
3. MISATTRIBUTED (s42 bug): 5 — routes 41-44, 47 actually end in ground-level
   slide-stalls (z ~ 0, soup walkable == navmesh, walls agree) = plain wall
   stalls, NOT height disagreements.
=> the true height-disagreement population is 5, all on elevated decks with
   delta 0.57 (soup deck above navmesh ramp); the fix direction is per-cell
   navmesh->soup z reconciliation on deck structures (named next, unchanged).

## Browser walker adoption (playable page): NOT COMPLETED — time-box spent on T1-T3 + this classification
Recipe stands (s42: ship navdata .nm to browser + JS nm_ground + step-ignore;
soup as walls only). The .nm parse + cell-triangle height query in JS is the
first milestone of the next session; the harness numbers to reproduce are
navmesh+stepignore0.55 = 15/40 routes / 14,040.7 m, full 10/40, ghost 36/40,
null 4/40.

Artifacts: s43_t4_classify.py, s43_t4_disagree.json.
