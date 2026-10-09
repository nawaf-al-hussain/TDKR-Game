# Worklog — TDKR-Game private research

---
Task ID: 9
Agent: Super Z (main)
Task: (a) higher fidelity ground (roads/grass currently merged into a single planar unit), (b) increase density of visible near-field geometry

Work Log:
- Recovered sandbox-reset workspace: cloned repo (73563fa), re-downloaded 895MB OBB from release, re-extracted l_gothamcity/game_config/commons/effects gla + all texture archives (277 gothamcity + 257 commons PNGs, 17 ZIP_SPLIT bake pages reassembled)
- Ground-truthed the ground: GC_City_Plane = 1 flat quad at z=17.43 (flood layer) binding GC_road_plane which ships nowhere; road/grass albedo pages (GothamCity_Road_v1/v2_Island_*, Crossings, GC_Park_grass/dirt) bind NO l_gothamcity mesh
- Binary-grepped all archives -> found GothamCity.zip / GothamCity_Island2.zip (+4 low/_inorm variants), 168.5MB of never-extracted streamed zone data inside l_gothamcity.gla
- Cracked the zone format (see extraction/re/RE_NOTES_session9.md): stream_info (AABB+counts), lod_table ([1526 (offset,size) descriptor pairs]+[5317 leaf values]), lod_data (segment blocks = 4B header + 24B-stride verts [pos + octahedral snorm16 normal + 2 extra dwords] + u16 strip indices with 0xFFFF cuts, descriptors at end), batch_info (bit-packed, 197 batches, vertex element sizes), bih_struct/data (culling), lod_selector ('rang'/'proj' tag stream); loader = CDoubleBufferedLODStreaming ctor @0x45e190 (disasm confirmed read order)
- Extracted both islands: island1 1,517/1,526 segs (651,431v / 785,053t), island2 1,020 segs (536,668v / 660,668t) — coordinate AABB matches stream_info exactly
- Built street tier exporter (extraction/scripts/export_zone.py): grid-chunked GLBs (21), primitives merged per material (2600 draw calls -> ~20/GLB), v10 manifest (45 GLBs, 1,535,059v / 1,647,858t total)
- Texture binding v4 (conservative): flat ground -> island bake family at 2x ('tiles' materials are LightMapDC per zone materials DB); small-UV-box flats -> grass/dirt/sand albedo; props <15u with decisive score -> Z1_Props atlases; walls/uncertain -> __dark. Authoritative batch->material binding (batch_info bitstream + compiled-COLLADA material DB) left open — documented in RE_NOTES_session9.md
- Viewer: added 'Street level' tier (background-loaded after skyline), verified headless: 21/21 GLBs render, roads/grass/crossings/props visible at street level, no garish misbindings
- Pushed main (60fcad3) + gh-pages (641a633)

Stage Summary:
- Deployed: street level tier = the game's own streamed near-field city; ground fidelity (separate roads/grass/dirt/crossings) + 7x triangle density vs previous manifest
- Open: authoritative material table (batch_info bitstream parse; compiled-COLLADA DB in little_endian_not_quantized.bdae); wall textures remain dark until then
