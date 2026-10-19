
# Session 38 (round 28) notes — living document

## State on entry
Remote: main 6620e62, gh-pages df7b0f7 (v20 LIVE), gh-pages-staged df7b0f7, essentials-s36 7c8defc.
Bundles s37 verified (main_s37_inc f0f0e132..43e6a0 requires fbc1d8e; essentials 251,743 B).
No credentials this session -> no push; verified incremental bundles only.

## T1a skinning root cause (ce9f12c)
The 162 cm "hand-built skinning error" was a HARNESS PHANTOM, three stacked bugs:
1. s37 fresh-state check: npz key lookup `t${ms}` vs stored `0`,`50`,... — every
   expected-array lookup missed; all 434 evals skipped; zeros recorded as PASS.
2. All JS-side npz/npy readers since s37 hardcoded an 80-byte npy header
   (real padded header 128 B for these shapes) -> misaligned garbage floats.
3. s37_t3_slerp.py fed a SECONDS grid through t/1000 (channel times ARE seconds;
   Bip01 translation 0..5.0) -> the s37 "truth" sampled only the first 5 ms.
Conventions were correct all along: numpy row-form M_all=invB@world + row einsum
is algebraically identical to three.js (bone.matrixWorld @ ibm) @ v (numpy worlds
are the exact TRANSPOSES of three.js matrixWorld; 31/31 bones). With fixes,
three.js fresh-state vs numpy: idle worst 0.0501 cm / mean 0.00094 cm over
146,349 evals; wrong-time null 67+ cm. GPU convention (documented for pages):
GLTFLoader binds IDENTITY (GLTFLoader.js:4105) + AttachedBindMode -> net GPU
skinning = SUM w_b (bone.matrixWorld @ ibm_b) v in world space; the mesh node's
transform cancels — rotate a bone ANCESTOR, never the mesh node.
REAL BUG found en route: browser assembleClip splices ONE extra boundary key at
each track start (walk key0 = idle's pelvis quat; run key0 = walk's) and
float-noise ticks defeat the tick dedupe (idle pelvis 3x t=0). Shipped
python-built batman.glb UNAFFECTED (verify_s34 re-run 0.0004 cm). Fix in T5.

## T1b+T1c live page fixed + quantified (5bec388)
- MESH HEADER DECODED: at IDX_OFF-28 ("Batman", 0,0, stride=20, INDEX_COUNT=5430,
  MAX_VERT_IDX=1448, 0). 5430 = true index count (1810 tris); the old 5655-index
  overread spanned into the NEXT mesh record (global vertex pool; trimmed tris
  referenced 31904..61853). With 5430: ALL indices in-range (assert passed).
- "SPIKY TRIANGLES" = THE CAPE (262 long-edge tris form a coherent manifold cloth
  sheet shoulders->knees; 2285/3145 edges shared by exactly 2 tris, 0 non-manifold).
  Spiky LOOK was flat-shading (no NORMAL exported) + single-sided. GLB now carries
  NORMALS (+12 field) + doubleSided + metallicFactor=0 (gltf default metallic=1
  rendered near-black without env map = the real "dark shading" root cause).
- batman.glb v2 (1.33 MB): + embedded Batman diffuse PNG, sampler REPEAT (atlas
  [0,16) tiled), POSITION min/max, 5 anims.
- index.html: rotation.x=-PI/2 on the bone ancestor; SRGBColorSpace explicit;
  lights retuned for r160 physical units (hemi 2.6 + ambient 1.1 + sun 3.0);
  #freeze/#gate deterministic hooks (test-only white-bg view).
- QUANTIFIED (headless chromium 1280x720): silhouette IoU 0.9421 (nulls: LYING
  unrotated 0.0229 = the v20 regression; wrong-pose 0.89 — idle self-similar;
  shifted 0.013); aspect 1.312 vs ref 1.279 (2.6%); feet min world-y 0.095 m;
  albedo dist-to-texture 5.1 (was 183 to the old grey); UV seams: 48.9% of 888
  shared-position pairs are integer-offset and match 100.0% texels (shuffled
  null 25.3%) — REPEAT tiling interpretation confirmed.

## T1d v21 release (local; push pending credentials)
- NEW GATE extraction/scripts/playable_screenshot_gate.py in the release chain
  (fails: IoU<0.80, margin over LYING null<0.25, aspect>15%, feet off ground,
  albedo closer to grey than texture). Deployed-tree result: PASS (IoU 0.9421,
  lying null 0.0229).
- deploy_site.py: dry-run 5 changes (app.js, manifest, playable/batman.glb,
  playable/index.html, .git artifact) -> URL gate 98/98 -> sync -> DEPLOY PASS.
- playable_screenshot_gate PASS on the DEPLOYED tree; smoke 59/59
  (http.server 8907 over the deploy worktree).
- Release commit 54686e4 on branch gh-pages-release-v21 (worktree
  /tmp/my-project/work/ghpages_deploy_wt), parent df7b0f7. Main mirror bump
  44bf6dc (manifest 20->21 + APP_CACHE_VERSION v20->v21, minimal 2-line diff).
- site_release_check: FAIL "main=21 vs origin/gh-pages=20" — EXPECTED pre-push;
  goes green when gh-pages-release-v21 is pushed to gh-pages.
- staging_manifest_gate: known-red class unchanged (3 stray textures +
  intentional playable/, now also reading pre-push v20 remote); repo path fixed
  to resolve relative to the script (was the stale /home/z/my-project/repo).
- PUSH REQUIRES CREDENTIALS. Do NOT push without a fresh user-supplied PAT.

## T2 PVRTC — oracle complete + semantics solved; real-data transform gap OPEN
1. ORACLE HARNESS FIXED: the s37 UC_ERR_INSN_INVALID was the MISSING RETURN PATH
   (the function POPs {pc} from the stack; s37 left dest as the top-of-stack word
   so the decoder "returned" into the DEST mapping and executed zeros). With a
   proper LR (magic page) + SP: the engine PVRTCDecompress @0x746e34 RUNS TO
   COMPLETION with ZERO faults (pc = return magic). COMPLETENESS PROVEN:
   DEST pre-filled 0x00 vs 0xFF -> outputs byte-identical (262,144/262,144),
   zero fill-dependent bytes, and byte-exact vs the s37-banked output (the s37
   dump was complete all along). Banked: s38_t2_engine_rgba(_4bpp).bin.
2. PROLOGUE/FLAGS: cmp r1,#0 -> r6 = 4 (r1==0) / 8 (r1!=0); the conversion-path
   caller @0x800f84 passes flag=1 ONLY for internal format ids 0x15/0x16 (table
   of 40-B format descriptors, bpp byte at +0x15, flag byte at +0x24), else 0.
   Synthetic probes: flag=1 shows 8-px endpoint spacing (2bpp geometry),
   flag=0 = 4bpp.
3. MODULATION TABLE SOLVED EMPIRICALLY (uniform-block probes, exact):
   mod 0 -> colorB (bits 16-30, 555), 1 -> (3A+5B)/8, 2 -> (5A+3B)/8,
   3 -> colorA (bits 0-14); 555->8 = bit replication; alpha = 255 if bit15
   (opA) set, else 255*wA/8 (wA = 0,3,5,8); with opA=0 colorA bleeds toward
   black + neighbor bleed (g=16 signature measured); mode bit31 has NO effect
   on 555 blocks (the 444+delta path is NOT taken for these).
4. MORTON STRUCTURE PROVEN BOTH WAYS: the disassembly computes FOUR neighbor
   block fetches (stack slots 0x130/134/138/13c) via bit-INTERLEAVE loops and
   `add ip, data, ip, lsl #3`; empirically (8 bit-plane runs, flag=0) the
   permutation between my LINEAR synthetic input and the decoded output blocks
   is EXACTLY interleave(by, bx) (by in the low bits) — linmap banked.
5. OPEN GAP: the REAL .tga mip0 (256^2, first 32,768 B of the 43,704-B chain —
   size law re-verified: 32768+8192+2048+512+128+32+8+8+8 = 43,704 exact) still
   decodes to structured noise through the engine under BOTH flags, and my
   python decoder (empirical table + linear/morton/morton-swapped/tiled order
   variants) does not reproduce it; block-level de-Morton of the engine OUTPUT
   also fails. The conversion path must transform the data (or the output)
   with an additional swizzle/step not yet reversed (caller-of-caller hunt).
   The 10-level-texture street patch is therefore NOT deliverable this round;
   T2 verdict: oracle + semantics DONE (4 of 5 items), real-texture decode
   remains open with all artifacts banked for the next session.

## T7 navmesh clearance-weighted routes (final)
Clearance per cell = 2D distance from cell center to the nearest non-walkable
collision edge (cap 2 m, cached); A* edge cost = length*(1+2*max(0,(0.45-clr)/0.45));
low-clearance waypoints pushed toward the locally clearest of 8 directions.
RESULT: 13/40 same-region routes ok (s37 baseline 12/40) — MARGINAL (+1).
Failure classes (40 attempts): stuck_wall 14, fell 6, step_too_high 5,
no_ground 1, ok 13 + the 24 cross-region engine-rejects unchanged.
VERDICT: the "missing agent-radius clearance" hypothesis is REFUTED as the
primary cause — clearance-weighted pathing does not recover the failures;
they remain collision-layer/data issues (missing walkable flags, step geometry).
NOTE: the first run clobbered extraction/re/session37/s37_t1_routes2.json
(save path); restored from git and the s38 output now saves to its own file.

## T8 inventory + release addendum
gh-pages v20 LIVE = 182 files / 120.0 MB (models 117.3, playable 2.6, shell 0.1).
playable/ game-derived assets: batman.glb 1.33 MB + patch.json 1.06 MB = 2.41 MB.
User-supplied-only proposal: ~0.5 MB pure code; batman.glb/patch.json decoded
at runtime via the T5 lazy pipeline (demonstrated); models/* has no runtime
pipeline (city decode not built). FINDING ACTIONED: pipeline.html +
tdkr_pipeline.js were tracked in the main mirror dir but NEVER synced to
gh-pages — deployed to the v21 tree (39298a4) via deploy_site.py + re-gated.

## Round-28 delivery state
Commits this session (main): ce9f12c 5bec388 3f5783a 021e327 f6784d3 7c3072f
c623076 254ee4d e665e20 + T7/notes commit. gh-pages-release-v21: 54686e4 +
39298a4 (ready to push AS gh-pages; v21 = upright textured Batman + pipeline
page). Main mirror: 44bf6dc. Push requires FRESH user credentials.

## Bundles (final)
- download/bundles_s38/main_s38_inc.bundle — 1,854,620 B, SHA256 027b51287113a6ed40dc20eba55045589b50359bb824cdbcb264b4000e3bfe7a, requires 6620e62, contains main 6620e62..a9948dd (11 commits).
- download/bundles_s38/essentials_s38.bundle — 251,743 B, SHA256 3d2639feb972b347d714bc4cc3d28007df07b1d1a4691392ce3230f9cea6ffe5 (essentials-s36 ref, unchanged protocol).
- download/bundles_s38/v21_release_branch.bundle — 1,229,424 B, SHA256 a1ac584ece3955544236bff1f776f6ed2d8c744c8a583cbab53342b64a220202, requires df7b0f7 (origin/gh-pages = v20), contains gh-pages df7b0f7..39298a4 (release v21: 54686e4 + 39298a4; the deploy worktree carried them onto the LOCAL gh-pages branch = push-ready state).
- PUSH REQUIRES FRESH USER CREDENTIALS. After pushing main->a9948dd and gh-pages->39298a4: site_release_check green, v21 LIVE.
