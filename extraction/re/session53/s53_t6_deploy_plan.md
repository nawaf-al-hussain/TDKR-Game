# Session 53 — T6: live verification + deploy candidate plan (NOTHING deployed)

## Live verification (public URLs, this session)
- Viewer `https://nawaf-al-hussain.github.io/TDKR-Game/?userfiles=1`: loads, 94 requests,
  0 failed, 0 console errors on the definitive run. One transient 503 (GitHub Pages) on the
  first load — clean on reload, not a site defect. gh-pages = 16a22ce (unchanged all session).
- `playable/walktest.html` (live): loads, 6 requests, 0 console errors.
- s52_t6_live.json (s52 baseline: 0 errors / 142 reqs viewer, 6 reqs walktest) — consistent.

## What deploying the staged tree would change on the live site
Branch `gh-pages-staged-s44` (39f2d5c + s53 commits b682393..aa0296f) vs live gh-pages 16a22ce:
- ADDS `playable/integration.html` (gated zone+walker page, 8-check gate)
- ADDS `playable/integration_lazy.html` (lazy-zip variant; s51 lazy reads, s52 T4 memory pass,
  s53 T4 ?poolchunk=1, s53 T1 ?unitaudit=1, s52 T5 ?fog=1&lut=1 engine fog+LUT, s53 T5 ?s5=1
  glide+grapple slice; all optional knobs OFF by default -> default pixels/digests unchanged)
- UPDATES `playable/batman.glb` (adds engine clips _057_glide_idle, _089_grapnel_pull,
  _088_grapnel_shoot; idle/walk/run/jump/jab unchanged; FK validation mean 0.0199 cm)
- Root viewer (index.html, app.js, models/, skybox) UNCHANGED by these commits — the live
  viewer experience is untouched; the viewer fog diff
  (extraction/re/session50/s50_t6_viewer_fog.diff) remains UNAPPLIED unless instructed.

## Gates the staged pages have passed (evidence)
- s53 T1: draw-time unit audit 0 mismatches on both game pages (8,556 / 9,108 draws),
  full default gate PASS on both.
- s53 T4: default / ?poolchunk=1 / ?lrumb16 all gate PASS, texDecoded 71 + texMiss 2
  identical, soup digest 00ce7970.../137,893 tris identical.
- s53 T5: default re-gate PASS 8/8 + 10/10 routes agree + soup digest identical; ?s5=1
  slice gate PASS (reachDist 0 u, glide clip sampled, landed 417 ms).
- s52 T5 (carried): ?fog=1&lut=1 variant PASS with the shipped fog/LUT constants.
- s52 T4 (carried): ?corrupt=1 negative control DETECTED (nm self-check abort).

## Deploy procedure (only on explicit instruction)
1. `python3 scripts/deploy_site.py` --dry-run first (staged tree -> gh-pages worktree),
   verify the file list matches the ADD/UPDATE list above and touches nothing else.
2. Real run: URL gate (must hit 16a22ce first), then the staged-page gates re-run from the
   gh-pages worktree (default 8/8 + digests identical + corrupt control).
3. Push gh-pages; verify LIVE by public-URL load (0 console errors, soup digest in log).
4. Rollback: `git push origin <previous gh-pages sha>:gh-pages` (force) — previous = 16a22ce;
   the root viewer is untouched so rollback risk is limited to the playable/ directory.

## Decision
Nothing deployed this session (per brief). The deploy candidate is ready and gate-tested.
