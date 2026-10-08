# TDKR-Game RE Worklog

---
Task ID: 6
Agent: Super Z (main)
Task: per-building rect-relative UV refinement; tracing the FP-page origin for the 8 runtime-bake footprints

Work Log:
- Restored workspace after sandbox reset: cloned repo (main=4abdf8b), re-downloaded 895MB OBB release asset, re-extracted game_config.gla (lvc), l_gothamcity.gla (541 bdae), l_gothamcity_tex.gla + commons_tex.gla (294+266 textures).
- Traced the Beast component family in the banked libKRHP.so with capstone (true ELF symtab addresses; symbols.txt is +0x10000-shifted):
  - CComponentBeastObjectComponent::Load @0x2e1e8c reads {vec4 so1, string page, vec4 so2}.
  - CBeastObjectComponent::Load @0x2a1ea4 binds getTexture(page) into material 'LightMap' slot, getTexture('LightMapSampler.tga'), sets uniform 'LightMapAtlas'; so2 is discarded (belongs to the trailing {ATLAS_low0, W, H, -1} low-path component).
  - LightMapDC-v.glsl: vCoord1 = (Coord1*so.xy + so.zw)*LightMapAtlas.xy + LightMapAtlas.zw => pageUV = uv*so1.xy + so1.zw.
  - The v1 "rect" was the discarded so2 misread as (u0,v0,u1,v1); u0==v0 was just square Beast tiles (scaleU==scaleV).
  - CLevel::LoadNextObject @0x499ecc typeIds: 99999=CTemplateBakeGroup, etc.; component payloads follow the per-class template order (hashes not in stream).
- Rewrote extractor (extract_bake_regions_v2.py): scans ALL *.tga page refs, decodes the full frame + mesh window; validates so1/so2/pow2 dims. Result: 89 frames, 54 footprints + 35 props with exact (page1, so1).
- FP-page origin traced: GF -> Island1_A0 @(0.0002,0.2502); VPOW -> Island1_Landmarks0 @(0.4995,0.5002) (both v7 UV-fit pages were WRONG); ~20 dark footprints gained real tiles; CB/CC/CD/CG/VA have no bake component (mass-repeated far-only buildings; CC x1059, CD x394) — only the GC_LongDist_Island* streaming pages exist for them statically.
- Decoded all 8 BakeGroup pages (2048² ETC1 mip-chained) + ZIP_SPLIT chunks (SPLIT zip: rgb.pvr + alpha.pvr) for the GC_LongDist FP pages; fixed the committed corruption in batch_decode_tex.py (blob[hdr:...) and export_city.py load_bake_groups (out[mesh]).
- export_city.py v8: BAKE_REGIONS_JSON -> bake_regions_v2.json; fp tier binds page1 at 2x and applies per-mesh rect-relative UV refinement (apply_bake_so) for _LongDist files with records; Reflection variants untouched; manifest v8.
- Rebuilt 24 GLBs (346,960 verts / 202,137 tris, 13.3MB geom, 55 textures incl. the new pages). Verified VC's refined UVs land exactly in its tile (u[0.0002..0.2493] v[0.0001..0.1894]).
- Headless smoke test (agent-browser): site loads, canvas renders, zero page errors, fp tier loads fp_island2.glb + fetches all 7 shipped BakeGroup pages (no 404s).
- Deployed gh-pages branch (models -> v8) and pushed; RE_NOTES.md session-6 findings appended; pushed main.

Stage Summary:
- Deliverables: bake_regions_v2.json (89 records), extract_bake_regions_v2.py, elf_syms.py, disasm_reader_seq.py, disasm_beast_loads.py, decode_bake_pages.py, quad_semantics_probe.py, extra_uv_probe.py, gla_pull.py, fixed batch_decode_tex.py + tex_bind.py + export_city.py; gh-pages manifest v8 deployed.
- Key results: authoritative FP-page origin for the runtime-bake footprints (page1 + so1 tile per object), per-building rect-relative UV refinement live in the viewer, UV-fit heuristic retired for 42/55 fp files.
- Open: Island1_Roads0 page ships nothing (its records are prop-tier — prop-tier binding could reuse records later); the five far-only footprints' in-page tiles are dynamic (streaming) and stay heuristic.
