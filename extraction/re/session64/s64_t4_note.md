# SESSION 64 — T4: deploy candidate review (NOT deployed — no instruction this session)

## Tree to deploy
s56-t1-glide @ **b7df902** (includes s63 T3 ?s5air + s64 T2 ?s5airto on top of the s62
page state). LIVE gh-pages = 6145545. Merge-base == LIVE head -> pure fast-forward.

## Exact delta (deploy_site.py dry-run, materialized trees 6145545 vs b7df902)
```
plan: 5 added, 2 changed, 0 deleted (DRY RUN - nothing will be written)
  ADD    extraction/re/session56/s56_t1_gate.json
  ADD    extraction/re/session56/s56_t2_ctl_validation.json
  ADD    extraction/re/session56/s56_t2_ctl_validation2.json
  ADD    extraction/re/session56/s56_t2_note.md
  ADD    playable/enemy_viewer.html
  CHANGE playable/integration_lazy.html
  CHANGE playable/tdkr_pipeline.js
pre-deploy URL gate: 98 referenced files, 0 missing
DRY RUN PASS - manifest v21, 263 meshes; no files were written
```
(The 4 extraction ADDs are branch bookkeeping carried by the glide branch; the SITE
surface change = enemy_viewer.html (new, 27,860 B) + integration_lazy.html
(90,706 -> 141,240 B) + tdkr_pipeline.js (19,420 -> 28,576 B).)

## >5 MB audit: CLEAN
Largest delta file = integration_lazy.html 141,240 B. Zero blobs > 5 MB in the delta.

## Page battery on the EXACT tree (headless Chromium, real 895 MB zip, serial)
| page | console errors | failed reqs | requests | notes |
|---|---|---|---|---|
| /index.html (root viewer) | 0 | 0 | 144 | |
| /playable/walktest.html | 0 | 0 | 8 | |
| /playable/index.html | 0 | 0 | 10 | |
| /playable/integration.html | 0 | 0 | 11 | |
| /playable/integration_lazy.html (default) | 0 | 0 | 11 | |
| /playable/enemy_viewer.html | 0 | 0 | 2 | combat gate **True** |
ALL CLEAN. The s5 slice gates on this exact tree: s64_t2_gate.json (4 runs - control
reproduces s62, the s5air=85 second-real-re-anchor run, the s5air=185 calibration
negative, the no-soup control) - soup digest 00ce7970/137893 byte-identical in all,
0 errors, gate pass=true.

## Game-derived assets in the deployed tree
models/ (263 meshes per manifest v21), models/tex, skybox.jpg, playable/patch.json,
playable/batman.glb, playable/*.json - **unchanged byte-identical vs LIVE; the delta
adds NO game-derived asset** (enemy_viewer.html is code, not data). Nothing removed.

## Verdict
The candidate is deploy-ready: fast-forward, 7-file plan (3 site files), URL gate clean,
all pages load clean, default digests unchanged, rollback = force-push gh-pages to
6145545. **Not deployed** - awaiting explicit user instruction (deploy_site.py dry run
-> URL gate -> gates -> live verify, per the standing procedure).
