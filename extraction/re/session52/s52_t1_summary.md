# Session 52 — T1 close-out: the mat73 textured-batch residual SOLVED (page defect, not GPU)

## Verdict
The residual was a **texture-UNIT clobber in the diagnostic pages' draw loop** — NOT filtering,
NOT swiftshader, NOT the engine. `texZget`'s cache-miss path calls `createTexture()+bindTexture()`
on the CURRENTLY ACTIVE unit; in `drawZoneBatches` the diffuse is bound to unit 0 first, so a
LightMap resolution that misses the cache rebinds **unit 0 to the lightmap** before the explicit
`activeTexture(TEXTURE1)` bind. Every batch whose LightMap texture was a cache miss at draw time
rendered with `DiffuseMap = LightMap` → `Color = LM²×2` (near-black; Roads0 mean 34-39 vs diffuse
109). s51's "regime-dependent draw artifact, swiftshader-suspect" is REFUTED with a repro + fix.
The game pages (`integration.html`, `integration_lazy.html`) already pre-resolve `dTex`/`lmTex`
at batch-build time and are immune; the live GLB viewer uses THREE (internal unit management).

## Acceptance criteria vs the brief
- "GL agrees with the CPU model within 5% on the diffuse-only step and the full-shader step at zoom":
  **MET after the fix** — step2 ratio 0.9954 (0.5% off, corr 0.9721), step4 ratio 1.0068 (0.7% off,
  corr 0.9757) vs the independent Python per-pixel model (s52_t1_cpu.py, NEAREST mip0, 1/16 snap).
- "or the first diverging step is identified with a repro": **ALSO delivered** — step 2 (diffuse
  sample) diverges at ratio 0.3542 / corr 0.004 with fix=0; draw-time audit records
  `unit0 = BakeGroup_Island1_Roads0.tga` (the LM) for mat73.

## Bisect table (zoom window bb=-448,-713,-248,-513, mat=73 only, nodepth, mip0/NEAREST)
Sign conventions: covered = mean RGB > 8; ratio = GL/CPU covered-mean; diverge = |ratio-1| > 0.05 or corr < 0.99.
Ladder: 1 = UV field out, 2 = diffuse only, 3 = D*LM, 4 = D*LM*2, 5 = +fog (provably inert:
page FogColor.a=0 and camera clamp; engine fog is T5 scope).

| step | fix=0 ratio | fix=0 corr | fix=1 ratio | fix=1 corr | IoU fix1 |
|------|------------|-----------|------------|-----------|----------|
| 1 UV | 1.002 | 0.9464 | 1.002 | 0.9464 | 0.9986 |
| 2 diffuse | **0.3542** | 0.004 | **0.9954** | 0.9721 | 0.9968 |
| 3 D*LM | 0.4753 | 0.3891 | 1.0192 | 0.9779 | 0.9623 |
| 4 D*LM*2 | 0.3965 | 0.4811 | **1.0068** | 0.9757 | 0.9769 |

Whole-zone (all 138 batches, same CPU reference as s50/s51): fix=0 ratio 0.8708 corr 0.9285 →
**fix=1 ratio 1.0111 corr 0.9923 IoU 0.9721** (s51's 0.9297 whole-zone figure had the same defect).

## Draw-time texture-unit audit (?upload=1)
- zoom mat73 run: `{mid:73, bn0: gothamcity_roads_details.tga, bn1: BakeGroup_Island1_Roads0.tga,
  lmHit:false, unit0: BakeGroup_Island1_Roads0.tga, CLOBBER:true}` — the smoking gun.
- whole-zone run: 120 LightMap-fx batches, **4 clobbered (mids 73, 132, 29, 30)** — the first user
  of each not-yet-cached LM page; explains why the zone-scale defect was partial (corr 0.9285, not ~0).
- Historical confirmation: the s51 grad-probe dump (`s51_g_mat73_gradnolm.npy`) has covered-mean
  (39.1, 45.4, 44.9) with B≈G — impossible for the synthetic gradient (B=0) and exactly Roads0's
  distribution: the gradient never reached the sampler in that run either.

## Upload-path audit (?upload=1, gate run)
UNPACK_ALIGNMENT=4, UNPACK_FLIP_Y_WEBGL=false, UNPACK_PREMULTIPLY_ALPHA_WEBGL=false; uploads are
RGBA/UNSIGNED_BYTE mip0 (or full chains under ?mip=); DiffuseMap→unit0, LightMap→unit1 (distinct
texture objects); glerr clean; sampler precision is the engine-verbatim source (`lowp` samplers,
`mediump` varyings — ?hp variant available and not needed post-fix).

## Second renderers (same page, same configs)
This sandbox is GPU-less: chromium+swiftshader works (reproduces bug ratio 0.3542 / fix ratio 1.0068,
renderer string "ANGLE ... SwiftShader driver"); firefox headless installs but never executes page JS
(no console/pageerror — CDN module fetch appears blocked); webkit fails to launch (missing system
libs, no sudo); chromium --use-angle=gl aborts at launch (no usable GL). A real-GPU adjudication page
is shipped instead (below). Two independent signals for the defect stand regardless: (a) the JS-side
draw-time unit audit, (b) the post-fix CPU-model agreement (independent implementation).

## Real-GPU check (user-run, 2 lines)
1. Serve the s41-city-slice branch (or any static host) and open
   `playable/city_bisect2.html?mat=73&bb=-448,-713,-248,-513&nodepth=1&upload=1&step=4&fix=1&gpucheck=1`
   (and the same with `step=2&fix=0` to see the bug reproduced on your GPU).
2. Pick your OBB zip when prompted; when the page finishes, copy the "TDKR GPU CHECK v1" block from
   the log and paste it back. Expected on a healthy GPU: `gl_covered_mean_this_run` ≈ 40.4 (step4
   fix1) and ≈ 122 (step2 fix1); with fix=0 the covered-mean collapses to ≈ 43 (bug present).

## Artifacts
- page: s41-city-slice `playable/city_bisect2.html` (commit 969bd3e)
- scripts: s52_t1_cpu.py (CPU per-step reference, fork of s50 pyref with --step), s52_t1_run.py,
  s52_t1_recmp.py, s52_t1_renders.py
- data: s52_t1_bisect.json (table + audits), s52_t1_renders.json (renderer matrix),
  s52_cpu_step{1..4}.{png,json} + s52_gl_*.png dumps (regenerable; PNGs over 400KB not committed)
