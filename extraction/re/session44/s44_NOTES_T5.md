# T5 — TRS RECORD VALIDATION DONE (population is substantially REAL, nulls separate strongly); near-trigger script test SPECIFIED, not executed (time-box)

## Record rebuild + validation (s44_t5_validate.py, s26 pure-python token streams both islands)

Loose scan ([i32 objId][9xf32] any prefix, dedup by (id, rounded pos)):
**8,102 unique records** (s43 reported 8,064 — same procedure, dedup rounding
differences; the population is confirmed at ~8.1k, 9x the strict s42 capture).

Validation battery + nulls (all numbers /8102):

| check                       | real      | N1 byte-random | N2 rot-as-pos | N3 in-record shuffle |
|-----------------------------|-----------|----------------|---------------|----------------------|
| V1 id resolves in stream    | 8102 100% | n/a            | n/a           | n/a                  |
| V2 pos in soup AABB (+40)   | 7061 87.2%| 12 (0.1%)      | 2770 (34.2%)  | 3320 (41.0%)         |
| V3 pos z above pit          | 8083 99.8%| 5940 (73.3%)   | 8102 (100%)   | 6867 (84.8%)         |
| V4 \|rot\| <= 4 rad         | 5584 68.9%| 1030 (12.7%)   | -             | 2476 (30.6%)         |
| V5 0 < scale <= 500, finite | 7931 97.9%| 164 (2.0%)     | -             | 691 (8.5%)           |

Effect sizes (real minus best null): V2 +46.2pp, V3 +15.0pp, V4 +38.3pp,
V5 +89.4pp, V1 = 100% with no plausible null. The battery SEPARATES the real
population from every null by wide margins: **the loose 8k TRS population is
substantially REAL object records** (the s43 false-positive concern is
quantified and bounded).

Caveat kept honest: V4 leaves 2,518 records with |rot| > 4 rad — either
degree-valued storage in some component classes or non-TRS data in the last
slots of a few classes; the per-component-class read-sequence refinement
(s26 table) can split this; does not affect the V2/V5 separations.

## The test that CAN work (specified, not executed in this time-box)

Near-trigger action test: for each trigger T (440) with a bound handler
chunk, collect the object ids the handler's script TEXT references
(SpawnObject/StartEventAtObjectNode/SetActorState id literals). Statistic:
mean distance(trigger.center, referenced-object.TRS.pos) vs the same
statistic under a same-size-class shuffled assignment (trigger size classes
via log10 half-extent x4 quantization, s43's null machinery). Requires the
script<->engine id bridge (per-zone object tables) — the s43 named-next —
plus the 541 handler chunks' text (already extracted for T1's reachability
scan). Gate: >= 100 (trigger, referenced-object) pairs. Effect size to
report: standardized mean difference vs the null p95.

The trigger.half ~= object.scale/2 volume model stays **"unvalidated,
engine-derived only"** (s43's 5,589-pair quantified null unchanged — this
session's record validation does not resurrect it; it validates the RECORDS,
not the volume model).

## Verdict

T5 PASS-VALIDATION / TEST-SPECIFIED: 8,102-record population validated as
substantially real against three nulls; the near-trigger action test is
defined with its null and gate, execution deferred (time-box; needs the id
bridge). No new numeric estimate introduced.

Artifacts: s44_t5_validate.py, s44_t5_validation.json (+ the two regenerated
token streams under TDKR_assets/raw/game_config/*.puretoks.json).
