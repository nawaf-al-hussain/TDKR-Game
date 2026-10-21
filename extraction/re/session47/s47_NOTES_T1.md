# s47 T1 — engine runtime material image resolution: FOUND (static chain closed end-to-end)

## The mechanism (all from libKRHP.so + compiled DB bytes)

1. **Scene-material instance table** in little_endian_not_quantized.bdae at
   0x5fea0..0x628f4: **301 entries**, 36 B each:
   `{char* mat_instance_name; char* same; u32 0; char* effect_url ("#Effect-fx_hash");
     u32 newparam_count; u32 profile_block_ptr; u32 id; u32 -1; u32 0x80}`
2. **Profile SNewParam blocks** (per instance, count x 24 B):
   `{char* name ("DiffuseMap"/"LightMap"/...); char* semantic (empty); u32 13; u32 1;
     u32 v1; u32 v2=v1+4}`; value header at v1 = `{1, v1+24}`, 16 B 0x000000ff fill,
   **node at v1+24 = {u32 image_index}** (0xffffffff = none).
3. **postLoadProcess** (`CResFileManager::postLoadProcess` @0x7c8b90): loop 1
   (@0x7c8cbc) over DB materials ([db+0x78] x 36 B @ [db+0x7c]) and loop 2
   (@0x7c8d50) over the 260-B effect records ([db+0x74]): for every param with
   type in (11,16] it reads SSetParam+0x14 -> node -> index; index == -1 ->
   writes 0 (null); else **[node] = [db+0x6c] + idx*3*4 = &SImage (12-B entry)
   in the 176-image table** (loop 2 bounds-checks idx < [db+0x68]).
4. Application: `setMaterialParameter<CMaterialRenderer,SNewParam>` @0x78c44c
   (from `createMaterialRendererForProfile<SProfileGLES2Traits>` @0x799e1c) and
   `<CMaterial,SSetParam>` @0x7891d0 (sole caller `glitch::collada::createMaterial`
   @0x776828 <- `CColladaFactory::createMaterial` x2 + ChooseSkin) both walk the
   value arrays, skip null nodes, `constructImage(SImage*)` @0x7bd5fc ->
   ITexture -> setParameter -> applyTextureSampler. The game hook
   `CCustomColladaFactory::createImage` @0x43d52c only post-adjusts
   filter/anisotropy by texture-name suffix (nm/atlas patterns).
   `constructImage(by-name)`/`(by-index)` overloads: 0 xrefs (dead).

## Why s46's pointer hunt failed

The per-material bindings are stored as **u32 image INDICES** (not pointers) in
the profile blocks; pointers exist only after the postLoadProcess patch, in
heap/runtime memory. The 651 material-level sampler value nodes are -1 by
design (the DB-level materials bind nothing); the real bindings live one level
up, in the scene-instance SNewParam blocks. Full-file scan: **723 value nodes
with idx in [0,176), 738 with -1, 4 other**.

## Engine table vs source.dae authoring table (s45_t1a_bindings.json, 307 rows)

- Scene table: **301/301 name-matched** to authoring rows (0 unmatched).
- **299/301 full texture-row agreement** (DiffuseMap/LightMap/MaskMap/
  ReflectionMap/NormalMap all equal).
- 2 differences, both FX_Coronas materials (Material__3220_8DYdD3ojxS_NIsNrmwUlN,
  Material__10_zdGc81tBDK_zMCk8R6BEu): engine DiffuseMap = none (idx -1) vs
  authoring FX_Coronas.tga — the corona textures load through the corona
  system (constructCoronas @0x7c28c0), not the material path. Explained; not a
  data mismatch.
- 6 authoring rows have NO scene-table entry: 1 "Null Material" + 5 unused
  export duplicates (302 Material__28_ItdsWlhi1v_s0G9s83W4B's used twin
  Material__28_ItdsWlhi1v_W2rLc6AveP IS bound with the identical tga set
  {GC_Z1_Props_Street_Alpha.tga, BakeGroup_Island1_A0.tga}; 303's corona
  variants unbound; 304-306 (uvanim, SimpleModulate_ZWrite x2) unbound here).
- Probe material 73 (tiles_KjsfSXF4YP_vgEsjieOpx): engine == authoring EXACTLY
  (DiffuseMap=gothamcity_roads_details.tga, LightMap=BakeGroup_Island1_Roads0.tga,
  effect URL hash-identical LightMapDC-fx_h2Q6dQAjy4_9VxSffSaIT).

## Verdict

**The engine's runtime binding equals the source.dae authoring table for every
material the scene table binds (299/301 exact; 2 corona-path exceptions); the
compiled material-level sampler slots are -1 placeholders by design.** The
browser's source.dae binding table (s45, 99.1%/98.8% GLB agreement) is the
correct engine-faithful source. Two independent signals: (a) the compiled
index data + the patching code path in libKRHP.so; (b) the name-matched
agreement with the independent XML table.

## Blocker (dynamic confirmation only)

The tracer run of constructMaterial/createMaterial under unicorn is blocked by
an environment regression: unicorn 2.1.4 (s25-era harness ran on an older
build). The ORIGINAL s25 BdaeHarness now performs 0 file reads and faults in
the allocator lock path (glf::Condition::Wait with garbage condition, verified
identical for the unmodified harness), and CResFileManager's singleton is
uninitialized. Lock stubs + get() stub + zip/raw IReadFile variants all tried;
CResFile ctor reached but faults on a half-initialized object virtual. Static
chain above is complete without it.

## Artifacts

s47_t1_fixup.py, s47_t1_xref.py, s47_t1_disasm_caller.py, s47_t1_xref2.py,
s47_t1_disasm2.py, s47_t1_loader_run.py, s47_t1_cresfile.py, s47_t1_node73.py,
s47_t1_nodescan.py, s47_t1_bind_extract.py, s47_t1_bind_extract2.py,
s47_t1_compare.py, s47_t1_bindings_v2.json, s47_t1_engine_vs_authoring.json.
