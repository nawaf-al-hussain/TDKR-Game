# s57 T4 — memory: phase floor (PARTIAL — streaming rework NOT attempted this session)

## Status
The build-phase spike rework (stream texture decode in smaller batches with immediate GL upload +
release of the ETC1 buffer; stop holding the full soup arrays until the end; reduce batch build
intermediates) was NOT implemented this session — T1/T2 consumed the budget. The measured floor by
phase is reported from the existing receipts; every number carries its harness.

## Measured floor by phase (2-core swiftshader, pristine 6145545 poolchunk config)
| phase | number | harness |
|---|---|---|
| empty three.js page | 84.9 MB RSS | s53 T5 fine harness (100 ms) |
| +170x512^2 RGBA GPU texture set | +23.5 MB (uploads lazily materialized) | s53 T5 |
| textures ETC1->RGBA decode transient (t=5-7 s) | the spike carrier; full soup + decode arrays held to the end | s56 T4 timeline |
| poolchunk full build peak | 611.3 / 547.1 / 592.1 MB, median 592 (+/-5.4%), peak at t=5-7 s | s56 T4 FINE (100 ms) x3 |
| poolchunk coarse-sampled peak | 555.9 MB (2 s sampling underestimates the spike ~6%) | s55 T4 |
| steady state | ~210 MB | s56 T4 |
| native residual | ~261 MB swiftshader/Chromium-internal copies (87 MB floor + copies) | s55 T4 |
| first image | 8.76-8.98 s | s56 T4 |
| game default (no poolchunk) | 813.5 MB / 6.1 s | s53 |

## Verdict vs acceptance
- Target < 500 MB peak AND first image < 8 s: **NOT MET** (floor ~590 MB / ~8.9 s on this config).
- Measured floor by phase reported: **MET** (table above, harness-attributed).
- Levers for a future session (sized): streaming ETC1 decode+upload in batches (0.5-1 session,
  targets the 5-7 s transient), drop decode arrays after upload (same), avoid double-holding soup
  (0.25). The 87 MB browser floor + ~261 MB swiftshader copies are NOT addressable in-page; a real
  GPU (T6) is the only path below ~350 MB on the native side.
