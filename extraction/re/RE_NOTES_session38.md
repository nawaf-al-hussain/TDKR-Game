
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
