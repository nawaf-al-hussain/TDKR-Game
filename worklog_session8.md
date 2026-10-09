# TDKR-Game RE Worklog

---
Task ID: 8
Agent: Super Z (main)
Task: fix "still the wrong textures" + "textures are very low quality" (v9 regression)

Work Log:
- Screenshotted live v9 site at zoom: diagonal smears across roads/plazas, black block holes, blurry 1024px bake pages; isolated Skyline layer = smears live in the hero LongDist GLBs themselves.
- GROUND-TRUTH RASTER (uv_ground_truth_render.py): drew GC_Footprint... GC_LongDist_Island1_FP1's own bdae mesh UVs straight onto its own 2048 page -> PERFECTLY coherent atlas (complete tiles, plaza, windows) under game v-bottom-origin convention. Mesh+page pair is self-consistent; the corruption happens at VIEWER sampling.
- Plaza probe (plaza_probe.py): triangles whose UVs fall in the page's circular-plaza bbox render the plaza recognizable under v-bottom (52% cov, structure visible) vs noise under v-top (30%). Decisive.
- ROOT CAUSE (wrong textures): game GLES UVs are BOTTOM-origin (v=0 = bottom row of the decoded page). PVR/ETC2 decode preserves row order (row0 = stored row0); the engine's effective sampling on our decoded pages pairs v=0 with the page BOTTOM. The viewer loads all textures flipY=false (glTF: v=0 = TOP row) -> every page sampled VERTICALLY MIRRORED. Symmetric content (window grids, bridge_tile) survived; asymmetric bake pages showed OTHER tiles' content = the "wrong textures" the user kept seeing (v5-v9 all had this).
- FIX 1 (exporter v10): flip V once at the GLB choke point (GlbBuilder.add_file: uv[:,1] = 1-uv[:,1]) — matches glTF top-left origin + viewer flipY=false; also flipped in bdae_extract.write_glb (batarang).
- FIX 2: _uv_score / choose_bake_channel control-rect / uv_fit now sample the page at row (h-1)-v — tile validation happens at the TRUE tile, not the mirrored one (scoring was consistent-but-mislocated before).
- ROOT CAUSE 2 (low quality): BakeGroup_* pages (fp tier's only textures) shipped at 1024 q78 from 2048 sources (~250KB each).
- FIX 3: all BakeGroup_* + HERO_TEX pages ship 2048 q88 (~1MB each); others 1024 q80.
- Verified offline: re-rasterized the NEW GLB TEXCOORD_0 against the deployed JPG under exact three.js flipY=false semantics -> same crisp coherent atlas (verify_glb_sampling.py). Then rebuilt 24 GLBs, synced to gh-pages, deployed.

Stage Summary:
- Engine truth finalized: pageUV = Coord1*so1 in GLES bottom-origin v; exporters must emit v' = 1-v for glTF. The "wrong textures" were never a binding-table problem for the island pages — they were a global V-mirror.
- Key files: extraction/scripts/export_city.py (v10), extraction/re/bdae_extract.py, uv_ground_truth_render.py, plaza_probe.py, verify_glb_sampling.py, probe_litpool.py, disasm_bake_v2.py.
- Disasm note: session 4-7 target addresses were +0x10000 off the real symbols (CComponentBeastBakeGroup::Load = 0x3be548 per symtab, not 0x3ce548); re-disassembled the real ones — layout conclusions unchanged ({str,float,str,float}). CZone::ChangeLightMap @0x2b9208 = runtime lightmap swap (finds "LightMap"/"LightmapTextureSampler"/"LightMapSampler" in node/material names, splices new page name) — not a static binding source.

---
Addendum (v10.1):
- White wedges over the city root-caused: 79 meshes use the engine's
  #SimpleAdditive-fx (glow planes, FX_Coronas light dots, diner logos,
  STD/VPOW volumetrics); rendered opaque they were giant solid-white polys.
- Exporter now tags these <tex>|add from the GT technique; viewer
  makeAdditiveMaterial = AdditiveBlending + depthWrite:false, no fog chain
  (local light sources). GC_CityBG additive backdrop stays skipped.
- Verified on a local server: wedges gone, black sky restored; Skyline +
  Footprints layers show aligned facades/roads/roundabout at full page res.
- NOTE for future cache busting: GLB/tex/app.js URLs are stable across
  deploys and GH Pages caches 10 min — verify via local server or wait.
