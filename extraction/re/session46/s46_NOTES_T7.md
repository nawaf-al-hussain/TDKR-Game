# s46 T7 — Option (a)/(b) decision brief: browser city rendering from user files

Per-component state (all numbers verifiable in this repo):

| component | state | remaining work |
|-----------|-------|----------------|
| zone geometry (lod_table/lod_data) | DONE — 1526/1526 segments decode bit-exact in JS from the user's zip (s41/s42; re-verified by the s46 T2 gate digests) | none for geometry itself |
| per-material bindings | source.dae instance_effect table (307 mats; 99.1% diffuse / 98.8% lightmap census vs the deployed GLB, s45); engine chain decoded (s46 T1) — the compiled DB provably does NOT carry them, so source.dae stays the browser source | none |
| textures | TDKR 52-B PVR2 wrapper + ETC1 decode bit-exact in JS (etc1_tdkr.js; s40-calibrated); s46 T2 gate: JS top-mip digest == s42 cleanroom | wire the non-ETC1 formats (RGB888/565 — decoders exist from s37/s42) into the page path (~0.25 session) |
| UVs | the lod stream carries its OWN runtime UVs (uv0 @12, uv1 @16 on stride 28) — s46 T2 proved the deployed GLB's UVs are a different (authoring) parameterization, so the browser must and does use the stream's | none |
| lightmaps | bindings 284/307 + LightMapAtlas = identity (Coord1 pre-baked, s45); lightmap PAGE is assigned PER SEGMENT at conversion (s45 found mats 145/150 page swaps) | derive + verify the per-seg lightmap-page rule (~0.5-1 session) |
| blend/render modes | mode census 90.4% (s45); render-state blocks live in the compiled effect nodes (schema decoded s45) | map mode -> blend state (~0.5 session) |
| LOD / streaming order + culling | bih_struct.bin (73.5 KB) + bih_data.bin (271 KB) + lod_selector.bin (36 KB) UNDECODED; s46 T3's batch_info gives the per-material declaration the renderer uses | decode bih + lod_selector for view culling and distance LOD (~1 session); short-term alternative: render a whole island statically (works, heavier) |
| performance path | the streamed-city renderer (CDoubleBufferedDynamicBatchMesh equivalents) exists in-engine; browser currently renders buffer slices | port the batch loop onto the declarations (T3 table) (~0.5 session) |

## Option (a) — full city from user files (ship code only)
- Effort: **2-3 sessions** (lightmap-page rule + formats; bih/culling/LOD; batch
  loop + perf + gates). Matches s44's estimate, now with the bindings/UV
  blockers of s45 resolved.
- Live site would contain: index/walktest/city_slice_textured pages (CODE +
  small parser tables), NO converted models — models/street_*.glb, tex/*.jpg,
  batman.glb (a conversion) removed or kept only for the no-zip fallback; the
  user's zip supplies geometry, textures, navmesh, soup.
- Risk: the static-island fallback without bih may be too heavy on low-end
  devices until culling lands.

## Option (b) — keep the converted subset
- Live keeps today's site (converted street GLBs + textures + patch.json
  default mode); user files only power ?userfiles=1 (walker, textured slice).
- No further sessions required; the derived data stays derived (gc_collision.bin
  already obsolete — the walker builds soup from user files).
- Cost: the live city stays a hand-converted subset; fidelity/pixel identity
  questions (s46 T2 dropped the pixel claim) remain attached to it.

The user decides; nothing has been removed or changed on live this session
(all s46 page work is branch-only).

## Recommendation (if asked)
(a) for fidelity + the project's "ship code only" principle: the two hard
blockers of s45 (sampler values, UV provenance) are now resolved in favor of
(a); the remaining work is bounded engineering, not research.
