# T1 — sampler records SOLVED (binding table extracted + validated); 5-block A/B vs deployed GLB run (binding chain validated, pixel identity not established); browser textured page NOT DONE (time-box)

## T1a: per-material sampler records — CLOSED

Where the records live (provenance):
1. The RUNTIME compiled DB (little_endian_not_quantized.bdae, 455,012 B) contains
   307 effect-instance nodes @0x23308, stride 260 B (perfect lag-65 u32
   autocorrelation over 0x23308..0x369C4). Node schema: {12 zero words, 1,
   {ptr,cnt} technique list, {ptr,cnt} setparam list, {ptr,cnt} render-state
   block, zeros, const 0x21e0510 @148, const 0x2dccc1 @200, name-pool ptr x2
   @252/256}. Param entry = 24 B {name_ptr, type, a, b, valptr1, valptr2}.
   Type census: 13=sampler (DiffuseMap x299, LightMap x284, DiffuseMaskSampler
   x86, NormalMap x37, ReflectionMapSampler x20), 7=float4 (LightMapAtlas x284,
   ExtraDiffuse x6), 1=flag (Default x137, Glass_NoAlpha x66, 2Sided x13...),
   4=Overbright, 6=float (Amplitude/Frequency/Speed).
2. **All sampler surface values in the compiled DB are 0xffffffff (EMPTY)** —
   verified by full pointer-chain walks on rec70/rec73 + source.dae proof: the
   authoring effects declare <surface type="2D"/> with NO init_from. This is
   BY DESIGN: textures bind per-INSTANCE via the material's
   <instance_effect><setparam> overrides (collada pattern), applied at zone
   geometry load. The compiled DB also carries the image table: 176 x 12 B
   triples {image_name_ptr, dup, tga_ptr} @0x22a9c (image56 =
   gothamcity_roads_details.tga confirmed; source.dae library_images[56] =
   same file, order-preserving).
3. THE BINDING TABLE = source.dae per-material instance_effect setparams
   (extraction/re/session45/s45_t1a_bindings.json, 307 entries):
   - DiffuseMap bound 298/307 (296 resolve to compiled image ordinals)
   - LightMap bound 284/307 (284 with ordinals — EXACT match to s43's 284/307)
   - LightMapAtlas float4 = (1,1,0,0) for ALL 284 carriers -> lightmap
     scale/offset is identity: Coord1 UVs are fully pre-baked (grounds the s43
     chain w4_raw*s133+s145 with s=1, o=0)
   - diffuse-color tint only on material 0 (0.584 grey)
   - 3 tga not in the compiled 176: FX_Coronas, GC_SXC_Atlas2_Refl, GC_Skybox
     (skybox/coronas handled outside the material DB)
   - wrap: NO per-material wrap state anywhere in the dae (authoring or
     compiled) -> wrap is engine-default (CCustomColladaFactory::getSamplerState
     @0x43d504); s43's GL_REPEAT assumption stands, engine-side confirmation
     still pending
4. Validation: mat73 anchor PASS (DiffuseMap=gothamcity_roads_details.tga
   ordinal 56; LightMap=BakeGroup_Island1_Roads0.tga ordinal 6).
5. batch_info-as-texture-index hypothesis REFUTED: diffuse ordinals appear in
   the material's 196-byte record at chance (3/10 materials; mat72's 38,
   mat74's 57, mat157's 91, mat302's 11 absent). The 196-slot grid is NOT the
   texture binding (semantics still open).

## T1b: 5-block comparison vs the deployed street GLB

Correspondence (new, exact):
- The 9 street_island1_XX.glb nodes are named seg_NNN = lod_table segment N
  (1517 of 1526 segs; vertex counts equal on most segs, differ on some — e.g.
  seg1486 935->229, seg1496 14->30 — the GLB holds the authoring-geometry
  variant, lod_data the streaming variant).
- Frame fit over 10 segs: GLB = lod axes permuted (0,2,1) with signs (1,-1,1),
  i.e. lod = (glb_x, -glb_z, glb_y), residual 0.0000 on all samples.

Binding agreement census (1517 segs, first primitive each):
- diffuse name: 1503/1517 = 99.1%; lightmap: 1499/1517 = 98.8%; mode: 90.4%.
- Mismatches: case-sensitivity (.TGA), mat156 (multi-sampler roof; GLB picked
  GC_Z1_Props_Rooftop_Alpha where the engine binds GC_footprint_AB_atlas —
  known s43 case), and lightmap-page swaps on mats 145/150 (A0 vs Roads0) ->
  the lightmap bake page is assigned PER SEGMENT at conversion, not
  per-material (the named-next item).

Pixel A/B (s45_t1b_render2.py, top-down ortho, union AABB, same rasterizer,
same deployed texture set; 5 blocks mat73/11/23/180/196, 700px, cover masks):
- real A/B meandiff/255: 44.4 / 102.0 / 79.5 / 50.5 / 64.2; histTV:
  0.38/0.73/0.57/0.69/0.59; SSIM -0.10..0.11
- shuffled-material nulls: 49-120 diff, TV 0.49-0.97; different-block nulls:
  38-101, TV 0.50-0.91
- Separation is real but WEAK and inconsistent (mat73: 44 vs null 120/89 clear;
  mat23: 79 vs 108/101 clear; mat180: 50 vs 55/38 mixed; mat196: 64 vs 49
  FAILS). Cause measured, not guessed: the GLB TEXCOORD_0/1 have NO affine
  relation to the lod @12 snorm16 field (per-axis lstsq residuals 0.15-0.75,
  slopes ~0.004-4.4) — the deployed render samples the same textures at
  authoring-UV positions while the lod streaming data carries its own
  (runtime-atlas) UV layout. Pixel identity is therefore NOT established by
  this test; what IS validated: per-material texture choice (99%+ census),
  frame, and colour statistics direction (real TV < null TV on 3/5).

Verdict T1b: PASS-WITH-SCOPE-NOTE — binding chain engine<->deployed validated;
per-pixel identity open (UV provenance: runtime atlas pages vs authoring pages).

## Not done (honest)

- T1c browser textured block page on s41-city-slice: NOT built this session
  (time-box; budget went to the sampler-record hunt + A/B). The s44 effort
  estimate for option (a) stands at 2 sessions; with the sampler records now
  closed, remaining = per-seg lightmap-page assignment, JS textured path,
  LOD/streaming order, blend states.
- Engine-side wrap confirmation via getSamplerState disassembly: pending.

Artifacts: s45_t1a_*.py, s45_t1a_bindings.json, s45_t1b_parse.py,
s45_t1b_geom2.py, s45_t1b_uvfit.py, s45_t1b_render2.py, s45_t1b_scores.json,
s45_t1b_*_{A,B}.png.
