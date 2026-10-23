# s54 T7 — real-GPU check (PENDING user), live report, deploy plan

## Live verification (gh-pages 16a22ce, nothing deployed this session)
- Viewer `?userfiles=1`: load OK 10.7 s, 94 requests, 0 failed, 0 console errors (s54_t7_live.json).
- `playable/walktest.html`: load OK 8.6 s, 6 requests, 0 failed, 0 console errors.
- Conclusion: the live site is healthy; NO deploy performed; the viewer fog diff remains unapplied.

## Real-GPU check — final instructions (one URL, one file input, paste back)
1. Serve the s41-city-slice branch locally (it contains `playable/city_bisect2.html`):
   - `git fetch && git checkout s41-city-slice` (or download the branch zip);
   - `python3 -m http.server 8080` in the repo root.
2. Open `http://localhost:8080/playable/city_bisect2.html?gpucheck=1`, drop in your
   `TDKR_v1.1.6b_APK_OBB.zip` at the file prompt, wait for the gate (~1 min).
3. Copy the block the page prints under `window.__GPUCHECK` (it includes the
   per-step ratios, the whole-zone corr/ratio, the every-draw unit audit and the
   wronglm calibration — dump survives a missing reference PNG) and paste it back.
4. What we compare: your REAL-GPU numbers vs the CPU per-pixel model
   (s52_t1_cpu.py: NEAREST mip0, 1/16 snap) — acceptance corr >= 0.99, ratio
   within 5 percent (the standing bar after the s52 unit-clobber fix).
   Status: PENDING since s52 (no user output received); the page is verified
   working under swiftshader this session (T4 used it for 6 renders).

## Deploy plan (only on instruction; not executed)
- Candidate: `gh-pages-staged-s44` @ 6145545 (s54 T1 decoded glide params +
  T2 waypoint anchors + T3 state-table clips; ?s5=1 default-off; default-mode
  pixels/digests unchanged — gate PASS 8/8 with identical soup digest
  00ce7970.../137893 and 10/10 routes).
- What it would change on the live site: playable/integration_lazy.html +
  playable/integration.html gain the s52-s54 staged features (lazy texture
  pool, fog/LUT flags, s5 glide/grapple slice, unit audit), playable/batman.glb
  gains the 3 engine clips; the ROOT viewer (index.html/app.js) is untouched.
- Procedure: deploy_site.py dry run -> URL gate -> gates -> push -> live verify.
- Rollback: force-push the previous gh-pages sha (16a22ce) — the site is a
  static tree, rollback is exact.
