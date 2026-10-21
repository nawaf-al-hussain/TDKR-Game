# T3 — PARTIAL (time-box): sampler-record hunt advanced (structure mapped, binding table still open); 5-block street-GLB comparison and browser textured page NOT DONE this session (honest)

## What was done (s44_t3_samplers.py + follow-up probes on little_endian_not_quantized.bdae, 455,012 B)

1. The 4-variant zip (GothamCity_materials.bdae -> little_endian_not_quantized.bdae)
   re-anchored. Texture universe 176 names; the image<->tga name pool decoded:
   `image55 -> GC_CBCE_Atlas.tga`, `image56 -> gothamcity_roads_details.tga`
   (the mat-73 diffuse), `image57 -> ...` — entries are {image_name, len,
   tga_name} triples at 0x171ec+ with a POINTER TABLE at ~0x22d04+ (two
   pointers per image: image-name ptr + tga-name ptr, e.g. 0x22d3c/0x22d40 ->
   image56, 0x22d44 -> gothamcity_roads_details.tga).
2. The effect/PROGRAM library structure mapped (0x36a70+): per-effect blocks
   {name, VS file ("ProfileCOMMON_emul_VS.glsl"), "main", FS file, "main",
   magic 0xff000101/0xffff00ff, 0x1c0700, 0x1d03007, uniform DEFAULT floats
   (1.0/0.0 arrays), 0x700, uniform-reflection {name_ptr,type,slot,0xffff}
   entries ("DiffuseColor" @0x18ad0 etc.)}. PinkBadShader + Vehicle effects
   identified; uniform DEFAULT arrays are per-EFFECT, not per-material.
3. The per-material SAMPLER VALUE records (texture index + Coord0/Coord1
   scale/offset per material) are still NOT located. The candidate region is
   the back half (u32-dense 0x23308..0x6f164); the material records should
   bind {effect index, image indices, uniform overrides}. NAMED NEXT with
   anchors: parse the effect-def tables @0x23e2c (StandardDiffuseDC) /
   0x2cd60 (LightmapVCBlendDC) -> pass/program tables -> uniform-slot layout
   -> material override array; cross-check count 305/307 and the known
   bindings (mat 73 = gothamcity_roads_details = image56).

## Not done this session (honest)

- 5-block street-GLB pixel-aligned comparison (image diff / colour histogram
  / SSIM with shuffled-material + different-block nulls): NOT executed — the
  session budget went to T1 (value resolution) and T4 (browser walker, which
  had slipped twice). The s43 software-render + shuffled-material null
  result (58.8/81.8/91.6 per 255 on three blocks) remains the standing
  binding-discrimination evidence.
- Lightmap chain implementation with data-driven scale/offset + page
  placement check: BLOCKED on the sampler records above.
- Browser branch textured page (city_slice.html textured mode, ETC1 binding,
  gate): NOT built this session. The s41-city-slice branch page already
  decodes 1526/1526 segments in-browser (untextured); the textured path
  needs the sampler records for correct atlas windows.

## Effort estimates (unchanged from s43, refined wording)

- Option (a) full city from USER files: closed items = geometry 1526/1526 +
  vertex format table + material->texture bridge + ETC1 pipeline
  (engine-verified) + Coord1 lightmap channel + browser zip pipeline +
  in-browser walker (T4 this session). Remaining = per-material sampler
  records (this hunt, anchors above), lightmap page assignment, JS textured
  path in city_slice.html, LOD selector + streaming order, blend states.
  2 sessions (s41 estimate) stands.
- Option (b) (removing the converted street models ~117 MB): site keeps
  playable + pipeline + walktest + branch previews; city viewer loses its
  data until (a) lands. Nothing removed, nothing deployed (branch-only).

Artifacts: s44_t3_samplers.py, s44_t3_bres_runs.json.
