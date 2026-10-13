# Worklog — TDKR-Game private research

---
Task ID: 10
Agent: Super Z (main)
Task: "Still the wrong assets mapped to the buildings and stuff. Cant you figure it out?"

Work Log:
- Recovered from another sandbox reset: cloned repo (60fcad3), downloaded 895MB OBB, re-extracted 4 .gla + 541 city bdae + 560 texture PNGs (294 gothamcity + 266 commons)
- Verified the DEPLOYED site headless (playwright): found the user-visible defects — street tier = rainbow smears (wrong band-atlas bindings), city = fog-washed flat gray at default view, LUT_000_default/LUT_023_lighting 404s (missing from models/tex, copied from extraction/previews)
- CRACKED the zone material DB (session-9 open item): source.dae instance_effect setparam chain gives per-material DiffuseMap + LightMap + LightMapAtlas — 305/307 + 195/196 materials resolved (scripts/parse_zone_collada2.py). Proves the engine model: Color = DiffuseMap(albedo) * LightMap(island BakeGroup page) * 2.0
- Proved fp LongDist DiffuseMaps (GC_Footprint_XX_LongDist/CompleteMap) are runtime Beast bakes — they ship nowhere; ground truth + bake-group records remain the authoritative fallbacks
- export_city.py v11: two-channel engine parity — TEXCOORD_1 = Coord1*so1 from the Beast record, material contract '<dif>|<lm>|<mode>'; bake_coord1() (score picks the Coord1 SOURCE only, floor 0.3); fp/hero/district attach lm records; manifest preserves the street tier (was being wiped)
- app.js v11: cityVertLM/cityFragLM two-texture multiply shader; 3-part material contract parse; lm-only fallback renders bake page x2
- export_zone.py v5: structural cross-section binding — road atlases' cross-section groups detected from dark separator rows; a flat segment binds the page whose ONE group contains its v-range (hard filter, score only disambiguates); kills the rainbow smears; full-page UVs -> dark
- Deployed manifest v11: 45 GLBs (24 city + 21 street), 1,535,059v / 1,647,858t; verified headless: smears gone, skyline textured, buildings show albedo structure
- Pushed main + gh-pages

Stage Summary:
- Engine-exact two-texture LightMapDC rendering for city tiers; street tier honest (no more garbage); LUTs fixed
- Open: batch_info.bin bitstream (material index per batch — needs CInterleavedDataAllocator parse); 265 flat segments match no cross-section group; bih_data leaf payload role
