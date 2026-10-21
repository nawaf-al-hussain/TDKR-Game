# T5 — EXPANDED TRIGGER-VOLUME TEST: gate PASSED (440/440 triggers, 5589 pairs), model REFUTED at the expanded population

1. EXPANSION: loose TRS scan over the same s26 token trees ([i32 objId][9x f]
   runs, any prefix, deduped by (id,pos)) yields **8,064 unique TRS records**
   vs s42's 907 (the strict [B]-prefixed pattern missed 9 of 10 records —
   component_loads.json shows ~8 component classes share the (bool?,objId,TRS)
   load signature; most do not emit the leading bool token).
2. JOIN: 5,589 object-in-trigger pairs across **all 440 triggers** (s42: 635
   pairs / 87 triggers). The >=100 testable-triggers gate is now PASSED with
   440/440 — the s41/s42 '87 < 100 gate' blocker is closed.
3. TEST: log-log correlation |trigger.half| vs |object.scale|/2 over the 5,589
   pairs: **r = 0.0636**. Same-size-class shuffled null (400 reps, scale classes
   via log10*4 quantization): mean 0.0809, **p95 0.0816**, max 0.0818.
   Real r < null p95 -> **does NOT discriminate** (and the null is now TIGHTER
   and the population 9x, so the negative is much stronger than s42's
   0.2839-vs-0.2878 margin).
4. VERDICT: the trigger.half ~= object.scale/2 hypothesis is DEAD at the
   expanded population. The volume model stays **'unvalidated, engine-derived
   only'** — now with a 440-trigger, 5,589-pair quantified null. The script<->
   engine id bridge (per-zone object tables) remains the only path to a
   validated volume model; effort should go there or nowhere.
