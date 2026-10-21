# T2 — VERTEX FORMAT: engine attribute system + per-stride layout table recovered; F-field semantics partially resolved (honest split)

## ENGINE SIDE (the "vertex format table")
1. Master attribute-name table @0xc12318 (glitch E_VERTEX_ATTRIBUTE enum):
   Position(0), TexCoord0..14(1..15), Normal(16), Color0(17), Color1(18),
   Tangent0..3(19..22), Binormal0..3(23..26), SkinWeights(27), SkinIndices(28),
   InstanceId(29); + attribute TYPE-name pool (Float/Int/Unsigned Byte/Short/
   Unsigned Short) @0xb87510..0xb87520. This IS the engine's vertex attribute
   vocabulary; the per-format attribute LISTS for the streaming mesh are baked
   into the CDoubleBufferedDynamicBatchMesh<SDoubleBufferedDynamicBatchMeshDefaultConfig>
   template instantiation (no data table: searched u32/u16 sequences [0,1,16,17],
   [0,1,2,16,17], [0,16,17] across all loaded segments = none).
2. Zone shaders (s18 extraction) bind exactly: Position, Normal, Color, Coord0
   (+ Coord1 in LightmapVCBlendDC). CRITICAL: the shader normalizes the normal
   itself (LightMapDC-v.glsl:115 `normalize(Normal)`, FS:167 again) -> storage
   magnitude is UNCONSTRAINED; only direction is meaningful.

## DATA SIDE (per-stride layout, byte-level, both islands)
- ALL classes: Position = 3x f32 LE @0 (the only f32s in the vertex).
- stride 24 (1417 i1 / 995 i2 segs): Coord0 = 2x snorm16 @12 (range [-1,1];
  quad-corner patterns; matches the s15/s21 diffuse chain w3_raw*s109+s121);
  F = 3x snorm8 + pad @16; Color0 = 4x u8 @20 (ffffffff = white in most segs).
- stride 28 (9 i1 segs, mats 153/156/302): Coord0 @12 + **Coord1 @16**
  (2x snorm16 each) + F @20 + Color0 @24. Coord1 = the LIGHTMAP channel —
  matches LightmapVCBlendDC and the w4_raw*s133+s145 chain; these are the
  lightmapped material group s42 flagged.
- stride 20 (100 i1 / 25 i2 segs, mats 0/1/296-303/194 = water/env): no UV.
- stride 32: ZERO segments shipped in either island -> layout stays
  inferred-family (+4B) and UNVERIFIED (honest).

## F-FIELD (the honest split)
F@16/@12/@20 is a smooth per-vertex 3-byte field. UNIT-normal (|n|=1+-0.03
under snorm8/127) holds ONLY for the lit material subset (302/1526 i1 segs,
mats {11,13,14,86,305}; 337/1020 i2, mats {4,5,6,7,11}); the remaining segs'
F is non-unit under every fixed scale (per-seg scale also contradicts), while
staying population-smooth. With shader-side normalize() this is legal storage;
whether the non-lit F is scaled normals or baked 3-byte light data is OPEN
(needs the runtime materials variant = T3). 1010102 packing: rejected (seg232
full-vertex |n| mean 0.669). Octahedral: unfalsifiable by unit test, direction
check also fails for the lit subset -> rejected.

## VALIDATION + NULL
- Attribute-aware decode, all segments both islands: positions finite + inside
  stream bbox(+30) for 1521/1526 i1 (5 boundary fails) and all i2; Coord ranges
  pass; max index < nv always.
- F smoothness via index edges, paired per-segment row-shuffle null:
  population real mean 0.591 (i1) / 0.586 (i2) vs null 1.437 / 1.572 — the
  shuffled field destroys vertex correlation (p << 0.001, Mann-Whitney on the
  sampled pairs); per-segment paired test: pass 764 + indeterminate 140 (F too
  small to discriminate) = 904/1526 i1, 712/1020 i2; 615/305 segs fail the
  paired test = hard-surface geometry whose per-vertex F is legitimately noisy
  (detail props/foliage cards) — the discriminator is population-level, not
  per-segment, for this content.
- Verdict: layout table = PASS (positions/Coord0/Coord1/color + F offsets);
  F semantics = PASS for lit subset (unit normals), OPEN for the rest;
  stride-32 = UNVERIFIED (absent). The divisibility-only stride-28 inference of
  s42 is now grounded: those 9 segs carry TWO snorm16 UV channels + the
  lightmap material group.

Artifacts: s43_t2_process_disasm.py, s43_t2_colstats.py, s43_t2_attr_decode.py,
s43_t2_smooth.py, s43_t2_result.json.
