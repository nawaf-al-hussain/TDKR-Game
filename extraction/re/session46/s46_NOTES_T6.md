# s46 T6 — trigger volumes under region-preserving nulls: effect SHRINKS TO THE NULL -> model reverts to "unvalidated, engine-derived only" — HONEST NEGATIVE

## Design (402 pairs rebuilt from the same inputs as s45 T3)

- Null A (triggers swapped within region): for each real pair (t, o), t' =
  another trigger in o's 500 m grid region; 386/402 pairs (16 regions have a
  single trigger).
- Null B (objects swapped within region): o' = another C_BASE object in t's
  region; 402/402 pairs.
- Paired AUC (dr < dnull, elementwise) + permutation z (200 reps: shuffle the
  real-to-null pairing; the paired-AUC null band).

## Results

| statistic | real | null A | null B |
|-----------|------|--------|--------|
| median d | 83.0 m | 153.2 m | 178.7 m |
| paired AUC | — | 0.7358 | 0.7363 |
| permuted-pairing AUC | — | 0.7298 ± 0.0137 | 0.7518 ± 0.0122 |
| z vs permuted null | — | **0.43** | **-1.27** |
| fraction inside 2H+1 | 0.154 | 0.078 | 0.030 |

## Interpretation (honest)

- The s45 effect (AUC 0.910 vs same-size-class null 0.891, z 2.47) does NOT
  survive region-preserving nulls: once the null trigger is drawn from the
  SAME 500 m region, the real pairing carries no additional signal
  (z_A = 0.43; z_B = -1.27 — both within the permuted-pairing band).
- The bulk of the s45 signal was REGION STRUCTURE (script-linked triggers and
  their acted-on objects co-locate because zones group them), not
  volume-model specificity.
- Fraction-inside: real 15.4% vs 7.8%/3.0% under the nulls — still elevated
  (2-5x) but driven by the same region structure.
- PER THE TASK RULE the volume model is marked **"unvalidated,
  engine-derived only"** (downgraded from s45's "weakly validated").
- Named-next if ever revisited: per-zone authored trigger links from the
  mission scripts (the engine's own volume->script binding), not statistics.

## Note
A tool-layer bug ate `[m` bracket sequences in the first write of this script
(rule 6) — repaired and byte-audited; all printed numbers come from the
repaired run.

## Artifact
s46_t6_nulls.py, s46_t6_nulls.json.
