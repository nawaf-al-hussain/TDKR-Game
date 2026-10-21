# T3 — class-split validation + id bridge (EXACT for trigger scripts) + near-trigger action test: WEAK DISCRIMINATION above the calibrated null (z 2.47); volume model upgrades to "weakly validated for script-linked triggers"

## Class-split validation (s45_t3_classsplit.py, census-containment attribution)

The loose TRS records attribute to census classes (>=20-record classes, largest
first): 0x14CA79/1362553 = C_BASE object TRS (island1 3905, island2 2403),
0x2DB081E2/766542306 = collision components (794/444), and the trigger/script
family. V-battery per class (island1):
- C_BASE objects: V2 in-AABB 3069/3905 (79%), V4 |rot|<=4 2723/3905 (70%), V5 100%
- collision comps: the "TRS" read there is the first TRIANGLE's data — parse
  artifacts of the loose scan (V2 = 0/794; in-AABB fails by construction), NOT
  placements. s43's 8,064-record population therefore over-counted by these.
- trigger/script family: V2 437/440 (99%), V4 355/440 (81%).
**The 2,518 |rot|>4 records are NOT concentrated in a droppable class** — pass
rates 0.69-0.81 across the real classes — so "drop failing classes" would drop
the whole population; the honest treatment stays per-record flags (s44), now
with the collision-class records REMOVED from the placement population (they
are artifacts, not records).

## The id bridge — EXACT

- Scripts live in census class 938977454 (440 records island1): each trigger
  record carries its Lua text (string-pool STR); 437 non-empty
  (t1_lua_GothamCity.json).
- **100% of the 437 scripts' objIds are trigger-record ids** — the script's own
  object IS the trigger; no id-space conversion needed.
- The objects a script ACTS ON are the integer arguments in its text
  (HideOccluder(800407) etc.): 1,150 references; **402 (35%) resolve to C_BASE
  TRS positions** (the rest: ids in other spaces — occluders/lights without
  placement records — reported as coverage, not failure).

## Near-trigger action test (s45_t3_bridge.py)

- Design: for each trigger T and each object a its script acts on:
  d_real = |pos(a) - T|; null = median |pos(a) - T'| over OTHER triggers T'
  with |log(H'/H)| <= ln2 (same size class). 402 pairs (>= 100 gate PASS).
- Result: **median d_real 83.0 m vs median d_null 253.6 m; AUC = 0.9104**
  (P the object is nearer its own trigger than a same-size-class alternative).
- Calibration: shuffled-assignment null (permute d_real across pairs, 400
  reps) = 0.8908 +/- 0.0080 (p95 0.903) -> **real AUC z = 2.47 above the null
  (p ~ 0.007 one-sided)**.
- Strict reading: only **15.4%** of acted-on objects lie within 2*H+1 of their
  own trigger — the volumes are NOT tight spatial bounds around the acted-on
  objects; the signal is in the script pairing, not in "objects inside boxes".
- Interpretation: the bulk of the raw AUC (0.891 of 0.910) is spatial
  clustering (objects live near SOME same-size trigger); the specific
  script->trigger assignment adds a real but modest increment (z 2.47).
  s43/s44's "does not discriminate" verdicts used the WRONG instrument
  (proxy-feature correlation over unlinked pairs); the script-linked pairing
  is the right one and it DOES discriminate — weakly.

**Verdict: the trigger volume model upgrades from "unvalidated, engine-derived
only" to "weakly validated for script-linked triggers"** — engine-derived
volumes + exact script linkage put acted-on objects nearer their own trigger
than same-size-class alternatives above the calibrated null (z 2.47, 402
pairs), while 84.6% of acted-on objects sit far outside their trigger's volume
(the volumes bound gameplay presence, not object positions).

Artifacts: s45_t3_classsplit.py, s45_t3_classsplit.json, s45_t3_bridge.py,
s45_t3_pairs.json.
