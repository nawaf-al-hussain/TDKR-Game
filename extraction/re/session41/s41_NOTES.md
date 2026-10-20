# Session 41 (round 31) notes

## State on entry
Remote exactly as expected: main 13b7890, gh-pages 582a0d0 (LIVE, s40 content),
s40-user-zip-slice 3af4b64, essentials-s36 7c8defc, gh-pages-staged 39298a4.
Local tree clean. CREDENTIALS: nothing to clean — 0 credential.helper entries
in any git scope, 0 remote URLs containing '@', no shell history files, no
.git-credentials anywhere accessible (the s40 cleanup already removed
/home/z/.git-credentials, mode 600, 75 bytes, + the ~/.gitconfig helper entry).
No token this session -> local commits + verified bundles only.

## T1 (this commit) — PASS: full-page deployment gate + negative controls + LIVE verification
1. NEW GATE (s41_t1_gate.py, playwright/chromium): loads EVERY gh-pages page
   locally (street viewer index.html, playable/index.html, playable/
   pipeline.html with the real zip) and fails on ANY console error, pageerror,
   requestfailed, non-2xx response, or unmet DOM/canvas expectation.
   RESULT: 3/3 pages PASS. Batman IoU vs numpy truth 0.9421 (lying null
   0.0229, shifted 0.002); pipeline street SHA == Python reference
   52fcbf32...; street viewer scene alive (children>0, 583k tris, fg painted).
2. NEGATIVE CONTROLS (new): for each page a copy with an injected
   SyntaxError script served from a symlink-farm overlay; the SAME monitor
   must flag it. 3/3 controls flagged (pageerror: Unexpected token).
   Incident recorded honestly: the first farm build used a DIRECTORY symlink
   for playable/ and the corrupted-page replace step followed it and deleted
   the real worktree playable/index.html (restored via checkout; the farm was
   rewritten to real dirs + file symlinks + a ROOT-alias assert on the parent
   path). Lesson: path-aliasing in overlay farms is a data-deletion hazard.
3. LIVE VERIFICATION via public URLs (s41_t1_live.py): all three pages
   PASS, 111 requests 0 non-2xx, 0 console errors.
   - Batman: IoU 0.9421 / lying 0.0229 / wrong-pose 0.89 / shifted 0.002;
     FK idle+run at 2 times each vs numpy = max 2.0 cm (wrong-time null mean
     30.0 cm = sensitive); albedo-vs-texture 5.0.
   - Pipeline: READY in ~1 s, street SHA exact, preview-canvas colour
     statistics vs Python reference: the preview draws the TOP-LEFT 512x512
     CROP (drawImage full,0,0,512,512 -> 256) — stats vs that reference:
     mean-dist 0.12, std-dist 0.05; NULL (BakeGroup_Island1_A0 same crop):
     mean-dist 19.9 = margin ~20x over the pass threshold.
   - Street viewer: scene children 8, "streaming city 6-7/21", 583-596k tris,
     0 errors while streaming (gate checks error-freedom, not completeness).
4. s40 NOTES CORRECTED (in place, marked [CORRECTED s41 T1]): the engine's
   8 modifier tables ARE the standard ETC1 intensity modifier table (rows 5-7
   = {24,80},{33,106},{47,183}); the "differ from ETC2-spec punchthrough"
   claim and the 74/109/159 numbers were WRONG (s40_t1_refdec.py comment
   fixed too). The JS/Py decoders always used the correct values (647/647
   bit-exact), so no code change — notes only.

Artifacts: extraction/re/session41/s41_t1_*.{py,json,png} + s41_refdec_lib.py.
