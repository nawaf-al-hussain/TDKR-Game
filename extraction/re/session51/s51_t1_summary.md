> **EDITORIAL CORRECTION (2026-10-23, sessions 52-53):** the Conclusion below
> ("environment-suspect (swiftshader)... needs one real-GPU run") is SUPERSEDED.
> The mat73 residual was a texture-UNIT CLOBBER in the diagnostic pages' draw
> loop (texZget cache-miss binds on the current unit; unit 0 held the diffuse).
> Fixed in city_bisect2.html (s41 969bd3e); fix=1 ratios 0.9954 (step2) /
> 1.0068 (step4) vs the CPU model; whole-zone corr 0.9285 -> 0.9923. The
> engine-faithful renderer meets the 0.99 bar; no GPU adjudication is needed.
> Session 53 ran the every-draw unit audit on all three pages: 0 mismatches.
> Original text below is preserved unmodified for the record.

# Session 51 — T1 close-out: the zone-render mat73 residual

## Verdict
The mip/filter hypothesis is REFUTED. The residual mat73 gap is a regime-dependent
sampling artifact of the per-material batched draw, with every pipeline component
proven exact in isolation. Python matches the analytic expectation; the GL batch
draw does not, only in a specific minification regime, under swiftshader.

## Evidence (two independent signals per claim)

### 1. Engine sampler state (static RE, libKRHP.so full symtab)
- `CCustomColladaFactory::getSamplerState` @0x43d504 (ARM): writes
  `magFilter = 1 (GL_LINEAR)` always; `minFilter = (mipCount > 1) ? 3 : 1`
  where enum 3 = GL_NEAREST_MIPMAP_LINEAR (0x2701) per the GL-enum table at
  0xb862f8 ([0x2600,0x2601,0x2700,0x2701,0x2702,0x2703] = enum 0..5).
- `applyTextureSampler` @0x78c320: overrides from SSamplerState fields
  [0xc]=min, [0x10]=mag, 0xff = "leave default"; compiled zone-material sampler
  value structs = [img_idx, 1, scale_u, scale_v, off_u, off_v] — NO filter/wrap
  override fields → engine defaults apply.
- `CCustomTexturePolicy::useOnlyOneMipmap` @0x444c84: TRUE only for names
  containing (case-SENSITIVE, plain memcmp found): "longdist", "_lm",
  "bakegroup_", "htmap". Zone names (BakeGroup_* capital-B, GC_Z1_*,
  gothamcity_roads_details) match NONE → full chains. (`getMipmapCountToSkip`
  @0x444a54 is the quality-driven level skipper, name-adjusted.)
- Shipped PVRs carry full chains: gothamcity_roads_details 512^2 member
  174,828 B = 52 + 131,072 (lvl0) + 43,704 (exact sum of levels 1..9);
  BakeGroup_Island1_Roads0 2048^2 = +699,064 = exact chain.

### 2. Mip means are flat — arithmetic refutation
gothamcity_roads_details chain means: 109.45, 108.89, 108.45, 107.69, 106.78,
105.54, 104.69, 102.83, 101.33, 99.33 (lvl0..9). A 2.3-2.7x brightness gap
CANNOT come from filtering a chain whose means vary 9%.

### 3. Empirical GL runs (city_bisect_mip.html, full chains uploaded + engine filters)
- whole-zone vs s50_ref_zbuf_snap: mip0-NEAREST corr 0.9297, NML 0.8940,
  LML 0.8973 (mips move AWAY from the mip0 Python ref, as predicted).
- mat73 noLM zoom (-448,-713,-248,-513): covered-mean GL 43.1 vs ref 101.2
  (texture mean 109); with mips (nml) 38.4 vs 102.4 — ratio unchanged (2.6x).

### 4. Component-by-component isolation (zoom window, mat73)
- FLAT geometry: GL vs Python IoU 0.9988 (pixel-exact geometry incl. snapping).
- Batch-path UV field (shader debug output of vCoord0/vCoord1): full coverage
  10.80% = flat coverage; field ranges match the baked attributes.
- uv0 AND uv1 arrays: GL attribute bytes == Python parse, bit-exact (first 24
  pairs each).
- Texture upload + sampling: fullscreen quad through texZget gives mean
  (118.7, 113.7, 95.8) = Python texture mean (118.8, 113.7, 95.8) EXACT;
  Roads0 2048^2 quad mean (34.3,39.3,38.7) vs py (34.4,39.3,38.8) EXACT.
- Attributes/uniforms healthy (Coord0=1, Coord1=2, Position=0, scaleoffset
  (1,1,0,0), LightMapAtlas (1,1,0,0), glerr 0).
- LOD_BIAS -1.0 (engine constant): bias=0 and 2-arg texture2D give BIT-IDENTICAL
  renders → bias inert under swiftshader, NOT the cause.
- Depth test off: no change. nolm verified working (b-channel test).
- Textured batch draw: covered 5.11% vs 10.81% flat — ~half the fragments
  sample near-black; shared-pixel corr 0.49; covered-mean 18.1 (withLM) vs
  Python 45.6. Same artifact zone-scale (shared mean 13.2 vs 30.5) but NOT at
  street level (integration page renders richly textured, gate PASS).

### 5. Analytic acceptance
- Per-material mean of pixels covered only by that material ≈ texture mean
  x LM x 2: Python 101-126 vs analytic 109+0.294x2 path — MATCHES.
  GL 38-43 — FAILS (dark texel subset).
- Known-colour ground patch: quad test = exact (the texture-upload acceptance).
- Zoom geometry agreement: 0.9988 >= 0.99 MET (flat); textured zoom 0.777 NOT
  met under swiftshader.

## Conclusion
The s50 attribution ("sub-pixel road-detail geometry + GPU snapping") is
INCOMPLETE: the dominant mat73 residual at zone/zoom scale is a dark-sampling
artifact of the batched textured draw that (a) is not filtering, (b) is not
wrap, decode, UVs, geometry, fog, depth, or bias, (c) vanishes at street-level
cameras and is mild at heavy minification. It is environment-suspect
(swiftshader) and needs one real-GPU run to adjudicate engine-vs-environment.
The engine-faithful GL configuration is now PINNED: full mip chains + min
NEAREST_MIPMAP_LINEAR + mag LINEAR + bias -1.0 + identity scaleoffsets.

## Artifacts
- scripts: /home/z/my-project/scripts/s51_*.py (disasm, plt, pvrcheck,
  mat73samp2, vdiff, gradcmp2, locate73, make_mippage2)
- page: city_slice_wt/playable/city_bisect_mip.html (knobs: mip/nolm/bias/
  nodepth/uvabs/texquad/texname/attrdbg/shdbg/arg2)
- refs: s51_ref_mat73_{snap,noLMsnap,grad,gradnolm,zoom,zoomnolm,zoom_flat}.png,
  s51_ref_276_zoom (window empty), GL dumps s51_g_*.png/.npy
