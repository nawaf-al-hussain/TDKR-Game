# s56 T4 — memory reconciliation: FINE harness (100 ms) x3 on the s55 config

## Harness provenance (every number labeled)
| harness | sampling | config | source |
|---|---|---|---|
| s53/s54 fine | 100 ms (CDP) | poolchunk, s44 staged tree | s53_t4_mem.json / s54 records: peak 691 MB |
| s55 coarse | 2 s (CDP) | poolchunk, s44 staged tree | s55_t4_mem.json: peak-of-samples 555.9 MB, steady 205.6 |
| **s56 fine (this)** | **100 ms (CDP + ps)** | **poolchunk, pristine 6145545 page** (served from ghpages_mig_wt; T3 touched only root index.html + playable/index.html there), 895 MB real zip, swiftshader, 2 cores | s56_t4_mem_fine.json |

## Peak distribution (n=3 runs, 60 s each, ~435 samples/run, 0 console errors in all runs)
| run | peak RSS | peak at | peak JS heap | steady RSS (t>40 s, trimmed mean) | first image |
|---|---|---|---|---|---|
| poolchunk_run1 | 611.3 MB | t=5.2 s | 33.0 MB | 209.6 MB | 8984 ms |
| poolchunk_run2 | 547.1 MB | t=7.3 s | 30.1 MB | 210.1 MB | 8763 ms |
| poolchunk_run3 | 592.1 MB | t=5.4 s | 33.6 MB | 209.7 MB | 8925 ms |
| **summary** | **median 592.1, range 547.1-611.3 (+/-5.4%)** | 5-7 s (during soup+texture build) | ~32 MB | ~209.8 MB (s55 coarse: 205.6 - consistent) | **8.76-8.98 s** |
| empty three.js (walktest.html) | 93.2 MB | end (crawl) | 1.9 MB | 92.8 MB | n/a |

## Reconciliation of the two numbers
- s53/s55 fine (691 MB) vs s55 coarse (555.9) vs s56 fine x3 (547-611, median 592):
  the s55 coarse 2 s sampling UNDERESTIMATED the true peak by ~36 MB (6%) vs the 100 ms
  median - the spike lives 5-7 s into the build and a 2 s grid can miss its apex. The s53
  691 MB remains the high outlier (its harness also sampled at 100 ms; run-to-run spread of
  the peak on this machine is +/-5.4%, and the 691 run predates the poolchunk capture-path
  tuning of s53 T4 - treat 691 as the same config's worst observed sample, not the median).
- Attribution (from s55, unchanged here): ~93 MB chromium/swiftshader floor + ~210 MB steady
  (soup typed arrays + three.js) + a 5-7 s transient of ~340-520 MB decoder/swiftshader
  copies that peaks between "all textures decoded" and "GPU upload done", then frees to 210.

## Verdict vs target
- Target "<600 MB peak AND first image <8 s": **NOT MET** (PARTIAL).
  - Peak: median 592.1 MB is within 1.3% of the bar, but 1 of 3 runs exceeds 600 (611.3) -
    the honest statement is the FLOOR: ~590 MB median on this 2-core swiftshader config,
    and <600 cannot be guaranteed run-to-run without cutting the transient.
  - First image: 8.76-8.98 s vs the <8 s bar (consistently ~9-12% over, 3/3 runs).
- The peak is a BUILD-TIME transient, not steady state (steady 210 MB); the s55 "can be
  cut" candidates (drop decode arrays after upload) remain the lever if the target matters.
