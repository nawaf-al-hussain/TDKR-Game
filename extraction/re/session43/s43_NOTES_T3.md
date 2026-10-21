# T3 — CITY SLICE 3: runtime material variant IDENTIFIED + material→texture bridge + textured block renders PASS null; branch-only (nothing deployed)

1. RUNTIME MATERIALS VARIANT SOLVED (closes the s42 blocker): of the four variants
   in GothamCity_materials.bdae (authoring zip), **little_endian_not_quantized.bdae**
   parses with the s6 ground_truth chain -> 176-texture runtime universe
   (StorageBox_D, GC_refl_exterior, BakeGroup_Island1_B0, ...). The two QUANTIZED
   variants s42 tried are the wrong pair; big_endian_* is the import-side twin.
2. MATERIAL->TEXTURE BRIDGE: all 305 dae material names (mat_tex_GothamCity.json,
   from source.dae via the s6 chain) occur verbatim in the runtime bdae
   (0x1c704.., length-prefixed pool) -> **dae material order == runtime material
   index** (307 = batch_info M). Bindings used this session: mats[302]
   Diffuse=GC_Z1_Props_Street_Alpha + LM=BakeGroup_Island1_A0; mats[73]
   Diffuse=gothamcity_roads_details + LM=BakeGroup_Island1_Roads0; mats[156]
   textures={GC_footprint_AB_atlas, _rfl, confroom_Reflection, confroom_lightmap}.
   284/307 mats carry a LightMap binding.
3. FILE STRUCTURE decoded so far: length-prefixed string pool (uniform/sampler
   names 0x18b40+: DiffuseMap/MaskMap/ReflectionMap/FogColor/...), texture
   .tga<->imageN triples 0x229b4+, shader reflection table @0x36c78+
   ({name_ptr,type,slot,0xffff}), effect defs with pass->program tables
   (StandardDiffuseDC @0x23e2c, LightmapVCBlendDC @0x2cd60). REMAINING GAP:
   per-material sampler VALUE records (texIdx + scale/offset) — the s6 unit
   heuristic finds 0 (units=0); needed for exact atlas-window math (identity
   mapping used for the renders below).
4. TEXTURED RENDERS (software rasterizer, textures = the DEPLOYED converted set
   = same texels the street GLB uses; top-down ortho; snorm16 uv *0.5+0.5):
   - seg680 (mat73, 510x181 m road, 204 verts): diffuse = gothamcity_roads_details
     -> recognizable curving road, lane bands along the road direction
     (s43_t3_road680_diffuse.png / _combined.png). mean RGB (94.6,87.2,74.2),
     warmth +20.5; lightmap page sampled (35.5,41.8,41.4).
   - seg1486 (mat156, roof z=162, stride-28): Coord0 -> GC_footprint_AB_atlas
     (mean 105,95,85 warmth +19.8), Coord1 -> bake page (54.7,55.9,53.2) —
     both channels land on real texture content.
   - seg1525 (mat302, street props z=5..91): GC_Z1_Props_Street_Alpha
     (163,158,154 warmth +9.1).
5. SHUFFLED-MATERIAL NULL (wrong diffuse per block): seg680 vs hedge texture
   mean abs pixel diff **58.8**/255; seg1486 vs park atlas **81.8**; seg1525 vs
   footprint atlas **91.6** — the correct binding discriminates decisively in
   all three blocks.
6. COMPARISON vs deployed street GLB: pixel-aligned diff is NOT possible this
   session (deployed street models are island2 static batch meshes, different
   blocks); at colour-statistics level my renders share the deployed texture
   universe and its warm-asphalt family; pixel-aligned A/B lands with the
   branch render (city_slice.html textured mode) — documented as next.
7. EFFORT option (a) full city (browser renders from the USER'S zip): closed so
   far = geometry 1526/1526 (s42), vertex format table (T2), variant ID +
   material bridge (this), ETC1 pipeline (s41, engine-verified s42), Coord1
   lightmap channel (T2). Remaining = per-material sampler records (texIdx +
   scale/offset precision), lightmap page assignment per region, JS textured
   path in city_slice.html, LOD selector + streaming order, blend states.
   **2 sessions stand (s41 estimate), realistically 2 now.** Option (b)
   (removing converted street models ~117 MB): site keeps playable + pipeline +
   branch preview; city viewer loses its data until (a) lands. NOTHING removed,
   NOTHING deployed (branch-only per task).
