# s46 T2 — GLB provenance PROVEN (bit-identical positions), failable render test DROPS the pixel claim, browser textured page GATED PASS — PASS-WITH-DROPPED-PIXEL-CLAIM

## 1. How the deployed GLB was produced (proven from data, two signals)

- **Per-vertex identity**: on the equal-count population (986 of 1,517 matched
  segs; 531 differ), single-prim segs compare **986/986 EXACT** — GLB
  POSITION f32s are bit-identical to lod_data positions under
  glb = (lod_x, lod_z, -lod_y) (s45's frame, inverted correctly this time;
  s45's formula was lod=(glb_x,-glb_z,glb_y)). maxd quantiles all 0.0.
  Order-sensitive (no sorting). Nulls: row-shuffle 4/300 "hits" (degenerate
  tiny segs), wrong-seg 0/300.
- ⟹ the street GLBs were exported FROM the lod stream for these segs; the 531
  count-mismatched segs hold a different (authoring/variant) geometry. The
  exporter is not in the repo (s38-era, only batman.glb generators found);
  provenance established from the data itself.

## 2. UV relation (why pixel identity was never going to hold)

- GLB TEXCOORD_0 is affine to the lod @12 snorm16 uv0 on only **147/986** segs
  (|resid|max < 0.01 per axis) — the GLB carries a DIFFERENT (authoring/export)
  parameterization for 85% of segs. Confirms and quantifies s45's
  "no affine relation" finding at per-seg resolution.

## 3. Pre-registered failable render comparison — CLAIM DROPPED

Design: FIXED geometry (lod positions/tris — bit-identical to GLB), swap only
the UV source (lod vs GLB) vs the texture (engine binding vs other blocks'
bindings); metric = histogram TV; rule = UV-effect TV < min(texture-swap TVs)
on >= 4/5 blocks.
Result: **PASS 1/5** (mat73 only; mat11/23/180/196 fail — UV-effect TV
0.60-0.88 >= texture-swap TVs 0.37-0.65). Per the pre-registered rule the
pixel-level binding claim vs the deployed GLB is DROPPED. Binding validation
rests on (a) the 99.1%/98.8% name census (s45) and (b) this session's
bit-exact position identity. The GLB is NOT a valid render oracle for the lod
runtime-UV layout — consequence for T7: the browser path renders straight from
lod_data (its own UVs) + source.dae bindings + user textures; the GLBs are
unnecessary for the user-files path.

## 4. Browser textured page (s41-city-slice branch) — GATED PASS

playable/city_slice_textured.html (branch-only, NOT deployed):
user release zip -> l_gothamcity.gla -> GothamCity.zip (lod_table/lod_data)
+ l_gothamcity_tex.gla -> TDKR texture wrapper decoded (52-B PVR2 header per
s40_t1a: [0]=52, [4]=height, [8]=width, [12]=mipcount, [44]='PVR!' LE,
data@52; top mip = ETC1 via the s40-calibrated etc1_tdkr.js) -> seg696
(mat73, nv=1264, 745 tris, stride 24) rendered top-down ortho with lod UVs
and the engine binding gothamcity_roads_details.

Gate (headless Chromium + the USER'S release zip, persisted s46_t2_gate.py):
- 0 console errors, 0 page errors, 0 gate errors
- geometry digest (pos f32 + u16 idx, order-sensitive) == Python:
  bb07916a...:5128144b...
- ETC1 top-mip digest == s42 cleanroom decoder (cross-implementation):
  49d6a237...
- pixel correlation page-vs-Python over the covered mask:
  real 0.9719 vs shuffled-binding nulls 0.4717 / 0.3757 -> separation PASS
  (pre-registered: real > 0.8 AND margin >= 0.2)
- debug probes retained behind ?debug=red|wire|quad|ndc|box|origin

## Artifacts
s46_t2_vertexmatch.py/.json, s46_t2_render_ab.py/.json,
s46_t2_city_slice_textured.html (branch), s46_t2_reference.py/.json,
s46_t2_py_real.png + s46_t2_py_null_*.png, s46_t2_gate.py + gate_shot.png.
