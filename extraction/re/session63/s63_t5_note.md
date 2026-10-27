# SESSION 63 — T5: gate re-run after T1-T4 + default digest + deploy plan (NOT deployed)

## Gate re-run (s63_t5_gate.py -> s63_t5_gate.json)
- Combat slice (playable/enemy_viewer.html, skinned merc) on the glide branch worktree
  WITH all s63 T1-T3 changes: **PASS**, 0 console errors.
- Same receipt as s62: mercLoaded true, 1294 verts; hp 120 -> 115 -> 105 -> 0;
  stateSeq Idle/Walk/Run/Hurt/Death transitions all correct (24 rows);
  wrong-clip control detected at both levels (point-cloud ctlWrongClipDiff 0.2211,
  mesh silhouette meshWrongClipDiff 60 lit px); meshSilPass true.
- The s63 T1 closure work (decoder-side only) and T3 (?s5air mid-air glide start,
  branch commit aeabaa5) did not regress the combat slice.

## Default soup digest (s63_t5_defaultgate.py -> s63_t5_defaultgate.json)
- Default page (no flags), integration_lazy.html on the glide branch tree:
  soup digest **00ce7970e45adc854ac7cae6d0f97797b602342d101e1ecb5eb1c2c01016beb8 /
  nTri 137893** — byte-identical to the s62 baseline and to the LIVE site.
  0 console errors. The s63 session changed nothing on the default/Batman path.

## Deploy plan for the glide branch page state (NOT EXECUTED — needs explicit user instruction)
- Source: s56-t1-glide @ aeabaa5 (includes s57-s62 glide work + s63 T3).
- Delta vs LIVE gh-pages (6145545): merge-base == LIVE head -> **pure fast-forward**,
  no history rewrite.
- Files changed (3):
  - M playable/integration_lazy.html  90,706 -> 141,048 B
  - M playable/tdkr_pipeline.js       19,420 -> 28,576 B
  - A playable/enemy_viewer.html      (new, 27,860 B)
- Untouched on deploy: root viewer (index.html/app.js/style.css/skybox), walktest,
  playable/index.html, batman.glb, patch.json, all data JSONs — byte-identical.
- Default behaviour after deploy: identical digests (verified above); all s63 flags
  (e.g. ?s5air) default-OFF.
- Rollback: force-push gh-pages back to **6145545** (static tree, exact, same as the
  s54/s56 rollback procedure).
- Push hygiene: 0 blobs >5 MB in the delta range; deployment would be a single push of
  one ref (gh-pages -> glide tree) following the deploy_site.py gates (dry run -> URL
  gate -> gates -> live verify).
