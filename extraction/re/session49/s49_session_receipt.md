# s49 session receipt (round 39)

STATE at start: remote main=58b7f3a, gh-pages=16a22ce (LIVE), gh-pages-staged-s44=62b4ffd,
s41-city-slice=646a267, s40-user-zip-slice=80274a1, essentials-s36=7c8defc, gh-pages-staged=39298a4
(all matched the brief); local main d8e74ee (s47+s48), s41-city-slice 08ec3b3; bundles_s48 verified
(SHA256 6a07498e.../936619e8...). No token supplied -> local commits + verified bundles.

- T1 (34cf925; branch 2158b8f) PASS: engine shaders run with engine parameters.
  Uniforms: Overbright = AlphaMasking.bdae default 1.0 on 16/17 AlphaMasking materials
  (mat 5 overrides 0.2 but carries 0 segments -> rendered Overbright is 1.0 everywhere);
  LightMapAtlas (1,1,0,0) on all 284 carriers; NO Coord/TexCoord scaleoffset param exists
  anywhere in the compiled table (engine defaults hold); vegetation-anim params on
  AlphaMasking mats 4/5/302. Real effects.gla GLSL (LightMapDC, AlphaMasking, NV_Glass,
  LightmapVCBlendDC) on a raw WebGL1 context (THREE r160 RT readback broken under
  swiftshader: glerr 1282, black RT — raw GLES2 is the engine's own API): corr vs Python
  road276 0.9964 pre-fog / 0.9968 fogged, vcblend 0.9969, glass7 LIGHTMAP profile WINS
  0.901 vs 0.285 (profile discrimination), stride28 decal 0.9325 (fp32-vs-fp64 edge noise
  on a 3.4%-coverage thin-line mask; dilated corr 0.969, IoU 0.864, means 0.427 vs 0.431);
  gate PASS 7/7, 0 console errors. Stride-28 census CORRECTED: 9 segs = 7xNV_Glass mat156
  (1486-92, glass footprints) + 1xLightmapVCBlendDC mat153 (seg 1493, park dirt/grass
  blend, vColor.a=1 -> pure grass; the brief's "8 on 156" was off by this segment) +
  1xAlphaMasking mat302 (1525, s48 anchor 111.43 reproduced). Fog chain CLOSED:
  LevelInit GI record = start 0 end 140, FogColor RGBA(64,102,119,160), FogMap
  (-1210,-220,1520,-1130), FogTexture gc_verticalfog.tga, VerticalFogAlpha 0.65,
  VerticalFogHeight 0.013; NO shipped compiled variant defines VERTICALFOG -> the city's
  active fog is ComputeFogFS (FogColor-only, grayscale-weighted); the deployed viewer's
  TEXTURE_FOG port (end=154 incl x1.1) implements a path the shipped shaders cannot
  reach. Brightness: pre-fog 32.84 -> +ComputeFogFS@25u 39.75 -> +CC LUT 40.18 (154u fog:
  68.17); deployed TEXTURE_FOG path at 25u = 34.92; live viewer over the same block ~19
  center-crop mean (median 6, gaps included) = dark, consistent with engine math. LUT
  000_default.tga is RGB565 (fmt 0x13, NOT ETC1 fmt 0x136), CCFS 32-cell layout,
  near-neutral on dark streets; it is both the engine's InitTexture default and the
  level script's explicit choice.
- T2 (d1faf21) PARTIAL with a POWER CHECK: (a) atlas-cell containment NO POWER
  (z in [-2.93,+0.66] over 6 pages, one strong negative; NOT used); (b) road direction
  SILENT (43.4 deg vs shuffled 45.5; NOT used); (c) lightmap seam continuity HAS POWER
  AND PASSES: real |dLM| 27.50 (107 shared-vertex pairs) vs permuted-LM-material null
  37.17+/-1.23, z = -7.89 (caveat: the null permutes material->page, which is exactly the
  binding claim under test).
- T3 (c23e520) PASS: 389-vs-0 RESOLVED — different ownership definitions. 389 = same-
  record-id join via the gol-template component census (lvc_pure census rid = owning
  template record); s47's 0 = byte-pattern/nesting searches that cannot succeed because
  flag-0 component class ids live in gol.bin templates, not the record stream (tid-0x264b
  template = [[0,938977454 trigger],[0,1923007858 BuiltinBox]] both flag 0 = the
  CreateComponent @0x223e3c record-stream dispatch path). 389 owners have BOTH (380
  0x264b + 9 0x474a) — s23 reproduced exactly. Volumes from the trigger's own f9 TRS x
  BuiltinBox size (C_BASE is a separate record: trig&cbase=0; nbox&cbase=95 = the 95
  template-object boxes). Region-preserving test RUNS: 393 Lua pairs, real median 80.9 vs
  nullA 116.7+/-5.9 (z -6.05), nullB 117.2+/-5.4 (z -6.75); robustness (drop top-5%
  largest): 378 pairs, 75.2 vs 114.9/115.9, z -7.14/-7.87 — the record join carries REAL
  ownership signal (supersedes s46's "region structure only" for the spatial proxy).
  Extents model stays engine-derived (raw f32s; median 1.0, p95 9.4e6).
- T4 (9f656cc; branch city_zone2) PARTIAL: (a) WebGL1 per-material batching (138 draws /
  368,739 tris) reaches the SPEED target (first image ~2.5-4 s vs 46 s) but the
  corr>=0.99 fidelity gate is NOT met (0.6813; the depth-direction fix — h=0 was NEAR and
  occluded roofs — took 0.037->0.55->0.68; the residual per-pixel shading pattern needs a
  binding/order investigation that did not fit the box; heap ~1.3 GB is user-zip-dominated,
  <400 MB steady state not certified). (b) failing-smoothness classification: island1 197
  = rooftop props x95 (mat13), billboards x29 (mat14), street trees x12 (mat74 trunk.tga);
  island2 156 = vegetation.tga x84 (mat5) + footprints/roofs — LEGITIMATE hard-edge
  content classes (failed BY CONSTRUCTION); decode stays digest-proven. The
  face-normal-agreement probe calibrated SILENT and is not used.
- T5 NOT EXECUTED (honest): T1's fog/shader-parameters work (engine uniform hunt,
  WebGL1 bring-up, fog chain) consumed the session box. Carry-over plan: one staged page
  = walktest.html's walker + city_zone2.html's batched GL renderer + the s49 raw-GL
  effect shaders; gates already exist (route check, silhouette, console errors) —
  estimated half a session.
- T6: live verified during T1d — index.html?userfiles=1 loaded from the public URL,
  streamed to completion (GOTHAM overlay gone), rendered, 0 console/page errors
  (s49_t1_live.png). No deploy instruction this session; nothing deployed.

Capability estimate update: NEW = engine uniform table (Overbright/Atlas/scaleoffsets
resolved from the compiled data), real engine GLSL running in-browser (raw GLES2 path,
gate-proven per block), the fog chain fully parameterized from the level record, seam-
continuity as the first population-scale binding check with power, record-joined trigger
volumes validated by the region test (z -7.1), the 197/156 smoothness question closed as
legitimate hard-edge content. Remaining for option (a): the zone GL renderer's fidelity
gap (corr 0.68 -> 0.99: shading-order/binding diff), fog/post integration into the zone
renderer, integration page (walker + zone), cross-region navigation + mission flow.
Estimate: ~1.5-2 sessions to a full-city walkable lit render from user files.
