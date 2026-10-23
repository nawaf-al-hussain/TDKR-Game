# s55 T5 — real-GPU check status + second software renderer attempt

## Real-GPU check: PENDING (unchanged)
No user paste-back this session. Instructions stand (extraction/re/session54/s54_t7_note.md):
serve the s41-city-slice branch, open playable/city_bisect2.html?gpucheck=1, drop the zip,
paste back window.__GPUCHECK. Acceptance vs the CPU model: corr >= 0.99, ratio within 5
percent. The page remains verified working (this session's X11/swiftshader run printed the
block header live).

## Second software renderer: NOT ACHIEVED (time-boxed)
Environment: Xvfb + Mesa 25.0.7 (llvmpipe/swrast DRI present), playwright chromium-1200
headed under X11.
- GL string probe: `--use-gl=gl` (and default) under X11 report "WebKit WebGL | WebGL 1.0
  (OpenGL ES 2.0 Chromium)" — the desktop-GL command-decoder path (Mesa), distinct from
  ANGLE/swiftshader.
- city_bisect2.html ?gpucheck=1 under the Mesa path: WebGL context works on toy pages, but
  the page produced NO __GPUCHECK within a 660 s budget (llvmpipe rasterization of the
  8,556-draw zone is far slower than swiftshader on 2 cores). Verdict: incomplete.
- Baseline re-run (X11 + --use-angle=swiftshader): block prints live
  (corr_vs_builtin_ref=0.9085, js_mean 4.162 vs ref_mean 5.110, diffuse gothamcity_roads_
  details.tga tex_mean [118.8,113.7,95.8], lightmap Roads0 [34.4,39.3,38.8]) — captured
  partially (receipt s55_t5_gpu2.json, __raw); the 240 s budget elapsed before `done`.
- Conclusion: on this 2-core box only swiftshader completes the battery; a second renderer
  needs either more cores or a real GPU. The swiftshader-suspect draw artifact (s51/s52)
  therefore remains environment-pinned, awaiting the user's real-GPU paste-back.

## Status
T5 verdict: PARTIAL — pending user action (one URL + one file input); second-renderer
attempt honestly negative on this hardware.
