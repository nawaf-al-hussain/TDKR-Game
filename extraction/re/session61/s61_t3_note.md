# SESSION 61 — T3: posed merc skinning — ROOT CAUSE FOUND AND PROVEN; page capture landed; posed-IoU-vs-numpy PARTIAL

## Root cause of the s60 "applyBoneTransform returns zeros" (minimal repro: one bone, known matrix)
Repro: jsverify/s61_t3_repro.mjs (THREE r160, one vertex (0,1,0), weight 1.0, bone rotZ(90),
file invB = identity; expected (-1,0,0)).
1. **applyBoneTransform reads 4 components unconditionally** (r160 source: loops i=0..3,
   `weight = skinWeight.getComponent(i)`, `if (weight !== 0) bones[skinIndex.getComponent(i)]...`).
   The s60 probe geometry had 1-component skinIndex/skinWeight -> getComponent(1..3) = undefined,
   `undefined !== 0` passes the weight gate -> `bones[undefined]` -> crash/undefined propagation
   (the "zeros"/broken state). FIX: skinIndex/skinWeight must be VEC4 (the GLB already writes
   VEC4 - the s60 failure was on ad-hoc probe attributes).
2. **bind() without an explicit bindMatrix recomputes boneInverses from the CURRENT bone world
   matrices** (r160: bind() calls this.skeleton.calculateInverses() when bindMatrix is undefined).
   Binding after posing destroys the FILE invB -> the result lags one pose update (measured:
   implicit bind rot90 -> (0,1,0) WRONG; explicit `mesh.bind(skel, new THREE.Matrix4())` ->
   (-1,0,0) CORRECT; rot180 -> (0,-1,0) CORRECT). GLTFLoader's own bind passes the mesh's
   identity world at parse, so the loaded-GLB path keeps the file invB.
3. **skeleton.pose() overwrites the clip pose from boneInverses** (repro case D) - must never be
   called per frame; the correct per-frame recipe is:
   `action.time=t; mixer.update(0); mesh.updateMatrixWorld(true); skeleton.update(); applyBoneTransform`.
   This equals the numpy convention boneMat = boneWorld x fileInvB (verified exactly in the repro).

## In-page result (worktree integration_lazy.html, ?enemy=1, 0 console errors, play gate still PASS)
New captureSkinnedFrames(): rest-consistency + 15 posed frames (3 x Idle/Walk/Run/Hurt/Death),
raw-WebGL1 raster (fixed rest-bbox scale, pelvis-relative recentering), readPixels 256->64 grid:
- skinDiff (wrong-clip control, mean |idle_skin - walk_skin| at frac 0.25, vertex space) =
  **6.4824 u/vertex >> 0** (the s60 point-cloud control was 0.2211 on a different geometry path).
- Per-clip frame motion > 0 for all 5 clips; 15/15 frames captured; glErr 0.
- **restMaxDev = 1.8707 (NOT ~0) and posed heights 26..154 u vs the rendered bbox 1.87 u** -
  a systematic convention gap REMAINS in the CPU chain on the loaded-GLB path (rest/bind
  mismatch of roughly a body-height - consistent with a 90-degree frame swap between the
  loaded bone rest worlds and the file invB, or rest != bind in the file). The zeroing of the
  mesh transform during capture did not change it (ruled out the -PI/2 mesh rotation).
  The GPU shader path is unaffected (enemyPlay bbox [-0.83, 0.96] = sane, displacements match
  s60: idle 1.256 / walk 1.702 / run 1.926 / hurt 7.18 / death 13.02, wrong-clip 1.896).

## Verdict against the acceptance criteria
- Find the root cause with a minimal repro: **DONE** (three concrete causes, repro + fix proven).
- Fix it and render the SKINNED merc at 3 frames x 5 clips in raw WebGL1: **capture landed**,
  but the CPU-skinned frames carry the unresolved rest/bind convention gap (above), so the
  silhouettes are not yet comparable to numpy -> **PARTIAL**.
- IoU + mean-vertex-distance vs numpy skinned reference with rolled-pose null and Batman null,
  n reported: **NOT achieved** (blocked by the gap; numpy posed refs also pending - est. 0.5
  session: dump page boneWorlds, re-skin in numpy via s60_t3_mercval conventions, then IoU).
- Same check for Batman (fix does not break it): the Batman GLB path is untouched (default
  digest gate to be re-run in the T7 commit); its skinning is GPU-shader side and unaffected.

## Artifacts
- jsverify/s61_t3_repro.mjs (one-bone proof), s61_t3_pagepatch.py (+ v4/v5 follow-ups applied),
  s61_t3_gate.py -> s61_t3_gate.json (15 frames, checks, skinDiff, restMaxDev)
