# s48 T1 — engine lightmap chain: LightMapDC x2 applied; stride28 reclassified as SimpleAdditive (no lightmap at all); gate PASS

## Shader facts (effects.gla, APK `files/data/effects.gla`; cross-checked s18 copies)

- `LightMapDC-f.glsl`: `LightMapColor = texture2D(LightMap, vCoord1) * 2.0` (x2 hardcoded);
  `Color = DiffuseMapColor * LightMapColor`; vertex color removed (ATICA comment).
- `LightMapDC-v.glsl`: `vCoord1 = (Coord1 * Coord1_scaleoffset.xy + Coord1_scaleoffset.zw) * LightMapAtlas.xy + LightMapAtlas.zw`;
  s45: LightMapAtlas = (1,1,0,0) on all 284 carriers; s43: Coord1 scale/offset = (1,0)
  -> vCoord1 = TC1_raw, GL_REPEAT (no per-material wrap anywhere; engine default REPEAT).
- `AlphaMasking-f.glsl` (17 mats incl mat 8): `LightMapColor = texture2D(LightMap, vCoord1) * 2.0 + vec4(Overbright)`;
  TDKR_SPLIT_ALPHA: alpha = `texture2D(DiffuseMap_alpha, vCoord0, -2.0).r`; output alpha = diffuse alpha;
  `if (fAlpha < 0.3) discard`.
- `SimpleAdditive-f/v.glsl` (8 mats incl mat 302): **FS = `Color = DiffuseMapColor * vColor` only — NO LightMap
  sampler, NO Coord1 attribute in the VS.** vColor = vertex Color0 (optionally x ExtraDiffuse).

## Effect census (compiled DB, s46 walk) projected onto geometry

| effect | materials | segments | triangles |
|---|---|---|---|
| LightMapDC | 227 | 1,040 | 297,738 |
| StandardDiffuseDC | 5 | 324 | 56,229 |
| NormalSpecOverbright | 38 | 29 | 11,792 |
| AlphaMasking | 17 | 57 | 1,966 |
| SimpleAdditive | 8 | 68 | 646 |

## THE FINDING that closes the s47 "too dark" item

The stride-28 block (seg 1525, mat 302, GC_Z1_Props_Street_Alpha) is NOT a lightmapped material:
its effect is **SimpleAdditive** — the engine renders it as `Diffuse * vColor` with
vColor = Color0/255 (mean 16.7/255 — a dark vertex tint), additive blend, alpha = vColor.a.
The SPLIT alpha.pvr is bound but UNUSED (no DiffuseMap_alpha in this FS). This is a
vertex-tinted additive decal layer (shadow/AO-style), 1 segment, 646 tris total class-wide.
s47's lightmap-multiply model was wrong for it — hence "dark". Engine math now:

| block | effect | plain | engine mode | s47 wrong model |
|---|---|---|---|---|
| road276 (73) | LightMapDC | 119.76 | **32.84** (LM x2) | — |
| road696 (73) | LightMapDC | 124.75 | **40.63** (LM x2) | — |
| stride28 (302) | SimpleAdditive | 55.09 | **10.69** (Diff x vColor) | 19.09 (LM x2, wrong) |
| cls24nc (11) | StandardDiffuseDC | 103.77 | = plain (no LM bound) | — |
| cls2017 (300) | AlphaMasking | 54.80 | = plain (no LM bound on mat 300) | — |

LightMapDC roads at |2x are ~x0.27 of diffuse-only: the x2 is applied and the streets ARE
dark pre-fog — the in-game look comes from fog (ComputeFogFS mixes toward a bright haze)
and post-processing, which our top-down block render deliberately excludes.

## Lightmap page-region check (LightMapDC road blocks; s133=1, s145=0, REPEAT)

- TC1 bbox (atlas [0,1] space): road276 0.7916, road696 0.7909 — roads bake spread across
  most of the Roads0 page (NOT compact; the s47 0.51 figure was a different segment and
  [-1,1]-space area 4x scaling: 0.7916 x 4 = 3.166 == s47's 3.1666 for the same seg).
- Content sensitivity: swapping the atlas moves the render by 30.7 / 37.1 mean luminance.
- Sampled-LM non-empty enrichment vs uniform-random page UVs: 0.95 / 1.06 — the road TC1
  region samples the bake page at page-average brightness (roads are lit at page-average,
  not brighter); the region check therefore grounds IDENTITY of transform (JS/Python bbox
  diff = 0.0) and content sensitivity, not "compact bright patch".
- JS (city_slice6.html) TC1 bbox == Python bbox to 0.0 on both road blocks.

## SPLIT restore (regression found + fixed)

The committed s47_t3_reference.py CRASHES regenerating its own committed JSON:
`decode_etc1` feeds the PK zip wrapper (SPLIT/rgb.pvr/alpha.pvr) to the ETC1 header parse
-> BAD_TEX -> None -> AttributeError. The committed JSON predates the loss of the Python
SPLIT unwrap (JS city_slice5.html kept it). s48 `s48_t1_render.py` restores
`unwrap_split` (17 SPLIT textures in l_gothamcity_tex.gla) and decodes alpha.pvr with its
own dims (1024x1024 alpha sampled at the same UV, separate lookup).

## Browser gate (city_slice6.html on s41-city-slice, branch-only, NOT deployed)

s48_t1_gate.py: 0 console errors, 0 page errors, source.dae digest match
(4f6e2d07...), corr(JS, Python engine-mode render): road276 lm2 0.99996, stride28
additive 0.99979, cls24nc 1.0000, cls2017 1.0000, road696 lm2 0.99997; TC1 bbox
max-diff 0.0 / area diff 0.0 on both LightMapDC blocks; JS Color0 mean 0.06556 ==
Python 16.7176/255. VERDICT PASS.

## Artifacts

s48_t1_render.py (+ s48_t1_render.json), s48_t1_gate.py (+ s48_t1_gate.json),
playable/city_slice6.html (branch), reference PNGs untracked in city_slice_wt
(s48_ref_*_{plain,lm2,additive}.png, s48_ref_stride28_lm2_discard.png dropped —
SimpleAdditive has no ALPHA_TEST; discard variant not applicable).
