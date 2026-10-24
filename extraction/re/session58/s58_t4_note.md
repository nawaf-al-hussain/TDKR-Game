# s58 T4 — memory/first-image: lever attempted, target NOT met; floor restated

## Harness (s58_t4_mem_fine.py; same 100 ms sampling as s56; CURRENT branch page ghpages_staged_wt)
| run | peak RSS | peak at | first image | steady | pass | soup |
|---|---|---|---|---|---|---|
| base_run1 (?poolchunk=1) | 538.7 MB | t=5.2 s | 8654 ms | 209 MB | PASS | 00ce7970 / 137893 |
| base_run2 | 568.2 MB | t=5.1 s | 8566 ms | 415.8 MB* | PASS | 00ce7970 |
| texfree_run1 (+&texfree=1) | 593.9 MB | t=5.1 s | 8718 ms | 210 MB | PASS | 00ce7970 |
| texfree_run2 | 551.8 MB | t=7.4 s | 8849 ms | 416.2 MB* | PASS | 00ce7970 |
| empty three.js (walktest.html) | 93.0 MB | - | - | 92.6 MB | - | - |
*steady-state sampler variance (GC phase at the 40 s+ window); medians: peak ~560 MB (4 runs:
538.7/568.2/593.9/551.8, median 560 vs s56's 592 on the pristine page — same ballpark, ±5% run noise).

## Lever attempted: ?texfree=1 (drop decoded CPU bytes right after GL upload)
texZget nulls t.data/t.alpha.data and evicts the LRU entry after texImage2D (behind flag;
digests identical — verified 00ce7970/137893 on all runs). **Result: the peak does NOT move**
(within run noise), first image slightly WORSE (+0.1..0.3 s, re-decode on LRU re-use).
Why: the texture CPU bytes were already bounded by the 64 MB LRU byte cap (LRU_BYTES,
s52 T4) — the t=5-7 s spike is the zone-build transient: swiftshader native copies
(s55 T4 breakdown: 87 MB native floor + 261 MB swiftshader copies) plus soup/batch
intermediates, not texture CPU residency.

## Verdict vs acceptance
- Target peak < 500 MB and first image < 8 s with identical digests: **NOT MET**
  (peak median ~560 MB, first image 8.5-8.9 s; digests identical on every run).
- Floor by phase (reconciled s55+s56+s58): empty three.js 93 MB (s58, was 85-87) +
  zone build transient ≈ +465 MB of which per s55 ≈ 261 MB swiftshader native copies
  (not JS-addressable), soup/geometry intermediates the remainder; steady state ~210 MB.
- The cheap JS levers are exhausted (textures already LRU-capped; upload path already
  immediate under poolchunk). Further reduction needs the batch-build intermediates
  refactor (digest-risky, not attempted this session) or a real GPU (no swiftshader
  copies).
