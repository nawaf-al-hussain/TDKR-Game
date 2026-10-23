# s55 T4 — memory breakdown (poolchunk mode, CDP + renderer-RSS sampling)

## Method
playwright + `Performance.getMetrics` (CDP) sampled every ~2 s + renderer-process RSS
(pgrep type=renderer, max across renderers); pages served locally from the deployed
tree; real user zip. Two runs: empty page (walktest.html baseline) and
integration_lazy.html ?poolchunk=1 with zip. Receipt: s55_t4_mem.json.

## Results

| run | peak RSS (samples) | peak JS heap | native residual | steady-state RSS |
|---|---|---|---|---|
| empty three.js page | 88.1 MB | 1.0 MB | 87.1 MB | 87.9 MB |
| poolchunk + zip | 555.9 MB (t=7.5 s: 552.8) | 207.8 MB (build) | 348.1 MB | **205.6 MB** (JS 9.5) |

Timeline (poolchunk): zip read + build 3.4 s @ 448.6 -> build/upload peak 552.8 @ 7.5 s
-> ~510 during gates -> GC settles to 205.6 MB from t=32 s onward.
GATE after run: soup digest 00ce7970.../137893 tris, routes 10/10 — IDENTICAL.

## Component attribution (peak)
- chromium/swiftshader page-independent floor: 87-88 MB
- JS heap at build peak: 207.8 MB (build intermediates: zip members, soup parse
  transient JS arrays, Batman anim decode; loadSoup runtime storage is already
  typed arrays: cpos Float64Array(137893*9) ~10 MB + flags)
- native residual 348 MB = 87 (floor) + ~261 MB (swiftshader client copies of GL
  textures — decoded RGBA mirrors in the driver — GL buffers, raster tiles);
  GPU-side texture set itself ~23.5 MB (s54 measure) sits inside that.
- Cuts already shipped (s51-s53): poolchunk discard path, decoded-LRU byte cap,
  zip shell release before buildBatches, typed-array soup runtime.
- NEW this session: nothing needed cutting — the run confirms the s53 knobs hold
  under the CDP harness and quantifies steady state (~206 MB) for the first time.

## Verdict vs acceptance (<600 MB, first image <8 s, identical digests)
- digests identical: PASS (soup 00ce7970/137893, routes 10/10).
- <600 MB: PASS UNDER THIS HARNESS (peak-of-2s-samples 555.9 MB; steady 205.6 MB).
  CAVEAT: the finer-grained s53 harness (ps sampling during build) measured 683-691 MB
  for the same mode — 2 s sampling can under-read the build spike. Treat <600 as
  harness-dependent PROVISIONAL; steady-state <600 is robust.
- first image <8 s: poolchunk = 8.4-8.6 s (s53 fine measure) -> NOT met in the
  low-memory mode; default mode 6.1 s meets time but peaks 813 MB. The two targets
  conflict under current knobs (poolchunk trades ~2.3 s first image for ~-130 MB peak).
- Real-GPU run would collapse most of the 261 MB swiftshader client-copy residual;
  still pending user paste-back (T5).
