# s46 T5 — playable/index.html?userfiles=1 release-candidate gate: ALL PASS; release plan attached — PASS (staged, not deployed)

## Gate (persisted s46_t5_gate.py; headless Chromium; the USER'S release zip)

Positive (?userfiles=1, pick zip):
- WALKER ACTIVE, **0 console errors / 0 page errors**
- 24 track points driven (keyboard, run speed + turn); capsule base z vs the
  INDEPENDENT Python navmesh-ground reference (own BE parser, hint-limited
  like the shipped nm_ground): **24/24 exact, maxdiff 0.0**
- Batman silhouette quantified: 2,119/2,415/2,451 px across 3 frames
  (present + animating; band-checked 300..60,000)

Negative controls (all DETECTING):
- ?corrupt=1 (navmesh vertex-0 bytes flipped) -> "WALKER ERROR: navmesh
  self-check FAILED" (the NM_EXPECT v0/vlast/cell compare catches it)
- ?corrupt=2 (64 bytes flipped inside the lvc collision region @4 MB) ->
  "WALKER ERROR: soup digest MISMATCH 26a154ca... (expected 00ce7970...)" —
  NEW runtime guard added to index.html: the built soup sha256 must equal the
  s45-verified Python export digest before loadSoup
- no zip picked: walker stays INACTIVE, page healthy, Batman still renders
  (default patch.json mode unaffected)

Page changes (branch gh-pages-staged-s44):
- index.html: preserveDrawingBuffer:true (readback/silhouette), corrupt hooks,
  runtime soup-digest guard (sha 00ce7970e45adc85...).

## RELEASE PLAN (owner decision; nothing executed)

What changes on live (gh-pages):
- playable/index.html: +preserveDrawingBuffer, +runtime soup-digest guard,
  +corrupt hooks (no behavior change without ?corrupt)
- models/tex etc: unchanged; walktest.html unchanged (already live)
Rollout: commit index.html on gh-pages-staged-s44 -> verify (the s45 deploy
checklist: LIVE headless load + ?userfiles=1 smoke + negative controls) ->
fast-forward gh-pages -> anonymous LIVE verification (walktest 200, index
?userfiles=1 gate re-run against the LIVE URL) -> monitor.
Dependencies (user-side): release zip only (game_config.gla -> navdata + lvc);
no derived files needed by ?userfiles=1.
Stay derived (never shipped): gc_collision.bin (superseded by user-file soup
build), converted tex/*.jpg (only the non-userfiles path uses them),
lvc_gol_templates/lvc_readseq_s30 (CODE+tables, shipped, small).
Rollback: gh-pages is fast-forward-only history — revert = push the previous
gh-pages commit (36788a9 or 16a22ce); derived files untouched; no data
migration. Worst case the ?userfiles=1 mode fails closed (WALKER ERROR) and
the default patch.json mode keeps working (verified by the nozip case).
