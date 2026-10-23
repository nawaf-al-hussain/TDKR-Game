# Session 53 — T3: trigger-volume model of record (final; nothing further tested)

## Decision (per the s52 declared criterion and this session's review)

**Model of record: A_engine_exact** — the engine construction (half_xy = 0.5*size_xy*scale,
z-height = size_z*scale_z, from the lvc trigger records) is the model of record.
**Refinement (kept, not promoted): D_union** — volume-OR-script-radius (union with the
GetDistFromMC thresholds mined from the 437 scripts) adds real signal on top of A and is
recorded as the refinement; it is NOT the model of record because the script thresholds are
derived data, not engine data.

## The two views (s52 numbers, both recorded)

Held-out AUC view (max held-out AUC of the margin d/H among calibrated models):
  B_no_scale ranks first (full 0.6766; folds 0.6953 / 0.6506; radius-subset 0.6397) BUT it is a
  DEGENERATE CONTAINER: on the 43 radius-subset pairs its containment is 0.0 real AND 0.0 null
  (containment z 0.0) — it "ranks first" by pushing everything far away, not by modeling
  trigger extent. Its calibration (wrong variant auc 0.4824, contain z -0.76) shows the AUC
  metric itself is calibrated, but the model is rejected on the degeneracy ground.
  A_engine_exact held-out AUC: full 0.6098, folds 0.6157 / 0.6016; D_union 0.6046 (full),
  0.6114 (radius subset). A vs B on the SAME folds differ by <0.07 AUC — far less than the
  interpretive gap created by B's degeneracy.

Containment view (real > null supports; same-construction nulls):
  A_engine_exact: 9.67% vs 3.34+/-0.77, z +8.18 (folds +6.16/+4.87 — holds out)
  D_union:        11.96% vs 4.19+/-0.86, z +9.03 (radius subset 65.12% vs 45.20+/-4.03, z +4.94)
  C_script_radius (43 pairs): 51.16% vs 41.41+/-3.21, z +3.04
  B_no_scale:     2.54% vs 0.13, z +13.8 but 4x lower absolute coverage (rejected, degenerate)
  Calibration: wrong-construction variants land at contain z -0.01 (A) / -0.76 (B) and
  auc 0.4895 / 0.4824 - both metrics are calibrated (silent-on-wrong variants were not used).

## Which statistic the playable page should use

**Proximity/margin, not containment.** The playable walker needs a boolean "am I near/in a
trigger" gate; engine-exact containment captures only ~10-12% of the real script-linked
events (the engine volumes under-cover: half-extents p50 0.5 m), while the margin statistic
d/H separates real from null at z -11.93 (A) with held-out AUC ~0.61. Practical recipe for
the page: engine-exact volume test FIRST (hard containment), then the script-radius union
(D) as the proximity halo; containment percentages stay a RESEARCH statistic (they measure
how much of the script-linked event mass the engine volumes explain) and should not gate
gameplay.

## Stopping decision

Nothing further is worth testing this session: the four models were compared with matched
nulls and held-out folds, both metrics calibrated, the degenerate case identified and
excluded, and the remaining uncertainty (absolute containment is low for every model) is a
property of the data (script events are proximity-dominated, volumes are small), not of the
statistics. Re-opening requires new data (e.g. decoding the runtime trigger-activation call
path in libKRHP.so), which is out of scope for the browser reimplementation slice.

## Sign conventions (repeated from s52)

containment z > 0 supports (real containment > same-construction null); margin z < 0 supports
(real mean margin < null); AUC 0.5 = no discrimination.
