# s48 T1 — engine lightmap chain (CORRECTED): effects come from the scene-instance table; roads x2 verified; stride28 is an AlphaMasking LIGHT DECAL; gate PASS

## CORRECTION to the first s48-T1 commit (and to s46's effect keying)

The per-material EFFECT is defined by the compiled scene-instance table at
0x5fea0 (307 entries x 36 B — s47's "301" was an undercount that stopped one
row short of the FX tail; ids run 0..306 and ALL 307 DB materials have
instances). Its effect URLs equal the source.dae instance_effect URLs for
**307/307** materials. The s46 260-B effect records @0x23308 are NOT keyed by
material id (record i's effect name == instance i+1's for the tail; record 302
says SimpleAdditive while instance/authoring say AlphaMasking) — any per-material
conclusion drawn from those records' keying is superseded.

Corrected effect census over the 1,526 segments (instance table x lod headers):
LightMapDC 1,041 segs / 297,818 tris; StandardDiffuseDC 324 / 56,229;
SimpleAdditive 94 / 978; NormalSpecOverbright 21 / 4,486; NV_Glass 7 / 7,226;
AlphaMasking 32 / 1,640.

## Engine math per effect (shader sources from effects.gla; Overbright default)

- LightMapDC: `LightMapColor = texture2D(LightMap, vCoord1) * 2.0` (x2 hardcoded);
  `Color = Diffuse * LightMapColor`; vCoord1 = TC1_raw (s133=1, s145=0, REPEAT).
- AlphaMasking: `LightMapColor = texture2D(LightMap, vCoord1) * 2.0 + vec4(Overbright)`;
  Overbright DEFAULT = 1.0 (AlphaMasking.bdae value word 0x3F800000); SPLIT
  TDKR_SPLIT_ALPHA: alpha = `texture2D(DiffuseMap_alpha, vCoord0, -2.0).r`;
  `if (fAlpha < 0.3) discard`.
- SimpleAdditive / StandardDiffuseDC: `Color = Diffuse * vColor` (vertex Color0;
  SimpleAdditive FS has NO LightMap sampler and its VS has NO Coord1 attribute).

## The five blocks (engine modes)

| block | mat | effect | plain | engine mode |
|---|---|---|---|---|
| road276 | 73 | LightMapDC | 119.76 | **32.84** (LM x2) |
| road696 | 73 | LightMapDC | 124.75 | **40.63** (LM x2) |
| stride28 | 302 | AlphaMasking | 55.09 | **111.43** (LM x2 + 1.0, discard a<0.3; kept 96.6% cov) |
| cls24nc | 11 | StandardDiffuseDC | 103.77 | 103.77 (Color0 all 255) |
| cls2017 | 300 | SimpleAdditive | 54.80 | **10.31** (vColor tint (3,93,78)/255 — colored light-add decal) |

Interpretation: the streets' base pass (roads) IS dark pre-fog at the engine's
exact math (x2 applied; the game's visible brightness comes from fog + post);
the street_alpha decal (mat 302) is an AlphaMasking LIGHT decal that BRIGHTENS
(masked, Overbright=1.0) — s47's dark multiply and the first s48-T1 additive
reclassification were both wrong models; the billboards (mat 300) are colored
additive light-add layers.

## Lightmap page-region check (LightMapDC road blocks; s133=1, s145=0, REPEAT)

Unchanged from the first pass: TC1 bbox (atlas [0,1] space) road276 0.7916,
road696 0.7909 (roads bake spread across most of the Roads0 page; s47's 0.51 was
a different segment and [-1,1] 4x scaling); swap-atlas moves the render by
30.7 / 37.1 mean luminance (content-sensitive); sampled-LM non-empty enrichment
vs uniform-random page UVs 0.95 / 1.06 (roads lit at page-average). JS bbox ==
Python bbox to 0.0 on both blocks.

## SPLIT restore (regression found + fixed)

Committed s47_t3_reference.py CRASHES regenerating its own committed JSON (PK
zip wrapper fed to the ETC1 header parse). s48_t1_render.py restores the SPLIT
unwrap (17 SPLIT textures in l_gothamcity_tex.gla) and samples alpha.pvr with
its OWN dims (1024x1024, separate lookup).

## Browser gate (city_slice6.html, s41-city-slice, branch-only, NOT deployed)

s48_t1_gate.py after the correction: 0 console errors, 0 page errors,
source.dae digest match; corr(JS, Python engine-mode):
road276 lm2 0.99996, stride28 lm2o 0.99952, cls24nc 1.0000, cls2017 additive
0.99990, road696 lm2 0.99997; TC1 bbox max-diff 0.0 / area diff 0.0 (both road
blocks); JS Color0 means match Python (16.72/255 decal; 0.227 billboard tint).
VERDICT PASS.

## Artifacts

s48_t1_render.py (+ s48_t1_render.json), s48_t1_gate.py (+ s48_t1_gate.json),
playable/city_slice6.html (branch), reference PNGs untracked in city_slice_wt.
