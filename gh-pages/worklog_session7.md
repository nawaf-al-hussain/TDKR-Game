# TDKR-Game RE Worklog

---
Task ID: 7
Agent: Super Z (main)
Task: fix "still projecting the wrong textures into the models" (v8 regression)

Work Log:
- Restored sandbox (repo + 895MB OBB + 4 .gla + lvc + 560 textures + 541 bdae + 8 bake pages).
- Screenshotted live v8 site: fp buildings showed smeared/shifted bake content.
- ROOT CAUSE 1 — wrong UV channel: fp _LongDist meshes store the Beast bake UV (Coord1, engine LightMapDC vCoord1 = Coord1*so1.xy+so1.zw) in the FIRST vertex dword (+12, u16x2), not the +16 stream the exporter used. Proof: GC_Footprint_IC_LongDist is a 16B-stride mesh (pos + one dword at +12); its +12 stream under so1 locks exactly onto the assigned BakeGroup_Island1_A0 tile content (overlay + 2.3x edge score vs uniform fill); +16 reads the NEXT VERTEX'S position bytes (out-of-bounds garbage) for 16B meshes, and the complete-map layout for 24B meshes.
- ROOT CAUSE 2 — projection-bake landmarks: VPOW-class (st=16, +12 = packed normal, byte3==0 => z~0 wall normals) have no stored bake UV; runtime derives Coord1 as top-down planar position projection; VPOW's normalized (x,y) wireframe locks onto its Landmarks0 tile's circular machinery (visual proof).
- ROOT CAUSE 3 (pinned, mostly benign) — mesh idx offset: CComponentBeastObjectComponent::Load @0x2e1e8c disasm = {4x F32 so1, str page1, 4x F32 so2, str page2}; mesh bdae string index lives at frame+84 in the following component (empirical dq histogram: 59/67+19/22 self-consistent). v1/v2 first-hit scan was a false-positive magnet; bake_regions_v3.json reads +84.
- Exporter v9: choose_bake_channel (uvm +12 vs top-down projection, edge-scored, weak floor), so1 baked into TEXCOORD_0, page|2x materials; st=16 uv=None fixed (was garbage); infrastructure LongDist files (railway/small-bridge) bound through the same bake path; 58 meshes on exact tiles, dark 41->37.
- Rebuilt 24 GLBs; deployed models (fp_island2 + railway + small-bridge + city_low + district_00 + manifest v9).

Stage Summary:
- Key files: extraction/scripts/export_city.py (v9), bdae_extract.py (uvm), extraction/re/bake_regions_v3.json, probe_uv1.py / uv_overlay.py / uv_flip_test.py / uv_pack_test.py / uv_fullpage.py (evidence toolchain).
- Engine truth: LightMapDC samples the bake page via Coord1 = first stored UV dword (+12); so1 = (scaleU,scaleV,offU,offV) into the BakeGroup page; projection targets use normalized top-down (x,y).
