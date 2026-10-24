# s56 T3 — distribution migration branch (s56-t3-migrate @69696df+dddaa9e, NOT deployed)

## What the branch does
Based on the LIVE tree (gh-pages 6145545). One commit pair:
1. `playable/index.html`: Batman built IN-BROWSER from the user's zip — `buildGLB` ported from
   integration_lazy.html (u16a + buildGLB verbatim, 7.7 KB; zip path via the page's existing
   TDKR.zipDirLazy/zipReadLazy/glaSlice; bdae skin 1449 verts + 921 anim clips decoded; 7-clip
   whitelist _001/_007/_008/_057/_089/_088/_065; 1024x1024 RGB888 DataTexture, s42 R8G8B8 order).
   `playable/batman.glb` (299,388 B) RETIRED. `patch.json` (1,057,419 B) RETIRED with it:
   the zip navmesh + collision-soup path (former `?userfiles=1`) is now the ONLY grounding
   (soup sha-verified in-page against 00ce7970...), spawn is a code constant
   ([-140.7, -681.2, 0.1], the former patch.spawns[0]), and the trigger markers retire with
   patch.json — an in-browser CTriggerShapeAABB decoder does not ship yet (the fengari Lua
   shim is kept for when it lands). The default no-zip walker mode is retired: the page now
   always prompts for the zip.
2. Root `index.html` replaced by the zone-renderer PROTOTYPE: integration_lazy.html copied to
   root with script/json paths pointed at ./playable/ (5 srcs + 2 fetches), retitled, banner
   comment documenting the migration. It loads EVERYTHING from the user's zip and includes the
   s56 T1/T2 glide-slice improvements (the tree's own playable/integration_lazy.html is the
   6145545 state - the prototype is standalone). REMOVED from the tree: models/ (110.9 MB),
   app.js, skybox.jpg.

## Post-migration live-site contents (git ls-tree of the branch, 22 files + .nojekyll)
| bytes | file |
|---|---|
| 219,632 | playable/fengari-web.js (Lua shim) |
| 96,782 | index.html (root zone-renderer prototype) |
| 90,706 | playable/integration_lazy.html |
| 85,029 | playable/lvc_gol_templates.json (game-derived parse table - RESIDUAL) |
| 62,891 | playable/integration.html |
| 23,809..2,006 | pipeline/walktest/tdkr_pipeline/lvc/etc1 code, worklogs, style.css |
| 15,475 | playable/lvc_readseq_s30.json (game-derived parse table - RESIDUAL) |
| **708,208 total (0.675 MB)** | vs LIVE 194 files / 119,352,318 B (113.8 MB) — **-99.4%** |

Residual game-derived: 100,504 B (lvc_gol_templates.json + lvc_readseq_s30.json = the soup
builder's template/parse metadata). Removing them needs gol.bin decoded in-browser from the
zip (parser exists in Python tooling; port unscheduled).

## Gates on the branch (s56_t3_migrate_gates.json; runner s56_t3_gates.py, real 895 MB zip, headless)
- root prototype `/`: **gate PASS**, soup sha 00ce7970.../137,893 tris (identical to LIVE),
  routes 10/10, 0 console/page errors.
- `/playable/index.html`: 0 console/page errors; logs: zip prompt -> batman.bdae 1449 verts /
  921 clips -> 1024x1024 RGB888 -> zip-built GLB 268,528 B with the 7 whitelisted clips
  (_001_idle_stand 5.00s, _007_walk 1.07s, _008_run 0.67s, _057_glide_idle 2.17s,
  _089_grapnel_pull 1.90s, _088..., _065...) -> WALKER ACTIVE navmesh 30,824 v / 31,647 c,
  soup 137,893 tris sha-verified. (No window.__GATE on this page - log-based gate.)
- Fix during gating: the ported buildBatmanFromZip lacked await on the two zipReadLazy calls
  (bare promise -> glaSlice garbage -> readBdae(undefined).buffer); fixed in dddaa9e, re-gated.

## Rollback
The live site is untouched (ground rule). If this branch were ever deployed, rollback =
`git push origin 6145545:gh-pages` (force if needed) - the pre-migration tree is exactly the
current LIVE commit, so rollback is a single ref move; all removed assets live in git history.

## Not done (time-box)
- In-browser gol.bin template decode (kills the 100 KB residual).
- CTriggerShapeAABB in-browser decode (restores trigger markers without patch.json).
- integration.html was left on the 6145545 state (it still fetches nothing game-derived at
  runtime - it is zip-driven already; its static title string is the s55-t1-title-fix item).
