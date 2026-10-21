# s47 T3 — browser-side binding table from the user's files + 5-block textured gate: PASS

## JS source.dae binding-table parity (value digest)

city_slice5.html (s41-city-slice branch, branch-only) parses source.dae IN JS
from the user's release zip: release zip -> data gla -> GothamCity.zip ->
GothamCity_materials.bdae (zip-in-zip) -> source.dae (2.19 MB XML) -> DOMParser
walk (library_images init_from; per-material instance_effect setparams:
surface/init_from -> image -> tga; sampler2D/source -> surface ref).
Canonical form: rows [name, DiffuseMap_tga, LightMap_tga] sorted by name ->
JSON.stringify -> SHA-256.

- JS digest == Python digest (independent ElementTree parse, same canonical
  form): **4f6e2d070e7ea2201d9e81cd67502e6e8a27b4f3a2a7160ac28d7a7835fbb26c**
- Python table: 307 rows, DiffuseMap 298/307, LightMap 284/307 — reproduces the
  s45 census EXACTLY from an independent parse.

## 5-block textured render gate (all from the user's zip, no Python-generated data)

Blocks chosen across the T2 declaration classes (seg / mat / class):
road276 (695/73/24), stride28 (1525/302/28 lightmapped), cls24nc (100/11/24
props), cls2017 (28/300/20), road696 (696/73/24). The page decodes batch_info
declarations IN JS (s47 T2 END-offset semantics), builds positions + lod
UVs + TC1, picks textures from the JS table, decodes ETC1 (etc1_tdkr.js,
incl. the SPLIT-zip Street_Alpha wrapper: zip{SPLIT, rgb.pvr 2048x2048,
alpha.pvr 1024x1024}), software-rasterizes 700x700 top-down (painter's order
by height, matching the Python reference), and compares vs the Python renders.

Gate (playwright headless, 0 console errors, 0 page errors):

| block | corr(JS, Py) | tv_real | tv_shuffle-null | tv_random-null |
|---|---|---|---|---|
| road276 | 1.0000 | 0.0076 | 0.0188 | 0.0194 |
| stride28 | 0.9998 | 0.0004 | 0.0054 | 0.0047 |
| cls24nc | 1.0000 | 0.0019 | 0.0244 | 0.0256 |
| cls2017 | 1.0000 | 0.0016 | 0.0178 | 0.0209 |
| road696 | 1.0000 | 0.0111 | 0.0217 | 0.0235 |

All 5: tv_real < both nulls (2-8x); corr >= 0.9998 on 5/5. VERDICT PASS.

## Lightmap chain (Coord1 = TC1_raw x 1 + 0, GL_REPEAT; LightMapAtlas (1,1,0,0))

- The chain is implemented and BITES: multiplying the lightmap changes the
  render by ~4.2-5.8 mean luminance on the road blocks (measured as
  |render_with_lm - render_without_lm|; swap-the-atlas null differs by a
  similar magnitude, i.e. the sampling is content-sensitive).
- Region quantification: the TC1 raw bbox per block is COMPACT relative to
  the full atlas — road276 earlier run: TC1 area 0.508 vs cross-block null
  4.0 (7.9x); road696: 3.16 vs 1.14 (the props-class TC1); stride28 (mat 302,
  props): TC1 spans the full [-1,1]^2 (area 4.0) — the props' bake coords
  cover the whole atlas, reported as-is.
- HONEST NOTE: the multiplied render is DARK (the bake atlases decode to mean
  37-47/255 and the sampled road regions sit in dark patches; roads_details
  mean 109 x ~0.15 = ~16). The chain mechanics + region are verified; the
  absolute-brightness curve (sRGB/gamma/decode of the bake pages) is left as
  the dedicated s48 item. The gate renders are diffuse-only for continuity
  with the s46 gate.

## Gotchas fixed on the way

- The display/tool layer strips the two-char sequence bracket-m from text
  written via shell heredocs (rule 6): the first patch attempt silently
  corrupted list comprehensions ("rows[m]" -> "rows]]"); all writes now go
  through the file tool and variables named m* are never bracket-indexed.
- Gate tv() must compare the 32-bin thumb vectors directly (histogramming the
  histogram is meaningless).
- The JS software raster must scale px/py to canvas pixels and sort triangles
  by mean height (painter) exactly like the Python reference — otherwise corr
  drops to 0.79-0.92 on dense blocks.

## Artifacts

s47_t3_reference.py (+ s47_t3_reference.json), s47_t3_gate.py
(+ s47_t3_gate.json), playable/city_slice5.html on s41-city-slice
(branch-only, NOT deployed; reference PNGs stay untracked, regenerable by
s47_t3_reference.py).
