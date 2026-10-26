# SESSION 62 — T2: posed merc skinning IN THE PAGE — rest/bind gap ROOT-CAUSED and FIXED (restMaxDev = 0)

## Bisection result (the gap's cause)
The s61 "rest/bind convention gap (restMaxDev 1.87)" decomposed into TWO stacked defects,
neither of which was a skeleton/invB/hierarchy problem:
1. **r160 applyBoneTransform CALLING CONVENTION (the actual killer)**: the r160 source is
   `_basePosition.copy( vector ).applyMatrix4( this.bindMatrix )` — the PASSED vector is the
   base position; the geometry position is NEVER read. The s61 capture passed a fresh
   (0,0,0) Vector3 -> EVERY CPU-skinned vertex was exactly 0. restMaxDev 1.87 was literally
   max|bind coords| (a body-height), skinDiff 6.48 was noise of the chained call, and the
   "posed heights 26..154 u" were bone-world magnitudes, not skin output.
   FIX: seed `vTmp.fromBufferAttribute(geo.attributes.position, i)` before every call.
2. **invB frame**: the file invBs (column-major) are EXACTLY inv(BIPED-FK rest) - the s60
   "V4 median dev 1.1559" and the s62 first comparison that said "file != BIPED-FK" were
   both orientation bugs in the comparison, not the data. The numpy-computed literal
   injected into buildGLB is bit-equal to the file invB (page inv1 == literal == file).
   Net effect: the GLB/skeleton needed NO change; the s60/s59 file invBs stand.
3. (b) GLB node TRS == bdae rest locals EXACTLY (max delta 0.000000 on t/q/s over all 31
   bones); skin.skeleton root = Bip01_Pelvis; mesh node transform identity at parse
   (bindMatrix = I). The enemy clips' ROOT CHANNEL overwrites mercObj placement on every
   mixer.update(0) - the capture must re-zero AFTER the mixer (added), else the posed
   frames carry the root placement (rot 90deg, pos (-2, 0.9, 0) measured exactly).
4. (c) LOADED geometry: skinIndex itemSize 4 (Uint16), skinWeight itemSize 4 (Float32),
   1294 verts, weight sums bad=0 maxDev=0 (exactly 1.0) - the s61 root cause (1) confirmed
   on the loaded path.
5. (d) one-vertex tests: identity boneMatrices reproduce the bind vertex to 8e-6; the full
   rest chain reproduces bind vertices EXACTLY (v100/v500/v900/v1200: out == bind to 1e-6;
   predicted MW x invB x v == measured to 1e-6).

## Gate results
- **restMaxDev = 0 (< 1e-3 gate MET)** with 0 console errors, play gate intact.
- **Per-clip posed skinned frames (3 x 5 clips) vs numpy**, numpy re-skins the file verts
  with the page's own dumped per-frame boneMatrices:
  mean vertex distance = **0.0000 on ALL 15 frames** (numpy == page CPU chain exactly).
- **Silhouette IoU (256x256 raster -> 64x64 occupancy, page projection: pelvis recenter,
  rest-bbox scale): mean 0.9001** (min 0.788 death@0.75, max 0.9389 hurt@0.75);
  n = 1294 vertices, 15 frames, page lit 7359..16844 px.
- **Nulls**: rolled-pose (90deg about Z through pelvis): 0.0..0.55 (mean ~0.29) - below
  real on all clips but weak on symmetric poses; Batman-mesh cross: mean 0.4377
  (0.013..0.60) vs real 0.90 - discriminative (matches s60's 0.692 batman null family).
- **Batman/default path unchanged**: default page (no ?enemy=1) soup digest
  = 00ce7970e45adc854ac7cae6d0f97797b602342d101e1ecb5eb1c2c01016beb8 / 137893 tris
  (= LIVE), 0 console errors - the s62 patches touch only the ?enemy capture path.

## Verdict against the acceptance criteria
- Find the cause with bisection (a-d): **DONE** (calling convention + root-channel
  overwrite; invB/hierarchy/TRS/attrs all verified exact).
- restMaxDev < 1e-3: **MET (= 0)**.
- Per-clip skinned renders vs numpy with IoU + mean vertex distance, n reported: **DONE**
  (IoU mean 0.9001, dist 0.0000, n=1294 verts x 15 frames).
- Rolled-pose null and Batman-mesh null: **DONE** (0.0-0.55 and mean 0.4377 vs real 0.90).
- Same check on Batman: **DONE via the default digest gate** (batman renders on the GPU
  shader path, untouched; digest unchanged).

## Artifacts
s62_t2_pagepatch.py/.json (bisect injection), s62_t2_pagepatch3.py (invB literal + seeded
skinAll + per-frame dumps + re-zero), s62_t2_run.py -> s62_t2_bisect.json + s62_t2_capture2.json,
s62_t2_numpy.py (numpy FK vs page worlds comparison), s62_t2_iou.py -> s62_t2_iou.json
(IoU + dist + nulls), s62_t2_defaultgate.py -> s62_t2_defaultgate.json (soup digest).
Page patches applied to the staged worktree integration_lazy.html (NOT deployed).
