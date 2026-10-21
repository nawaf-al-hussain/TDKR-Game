# s46 T1 — engine runtime material binding: chain DECODED, per-material image table NOT statically present (all in-DB/zone candidates eliminated) — PARTIAL

## Engine chain (all decoded from libKRHP.so this session)

1. `CDoubleBufferedDynamicBatchMesh<Default>::addBatch(u32)` @0x46d2c4 (2,616 B):
   - reads **u16 material id from the IReadFile at [mesh+0xa4]** (the batch_info-like
     zone file) at offset `matIdx * [mesh+0xa8] + 4` (seek vtbl+0x18, read-2 vtbl+0xc);
   - calls `CColladaDatabase::constructMaterial(driver, u16, scene, rootSceneNode)`
     @0x7bd0ec (60 B): indexes the DB material array (count @db+0x78, array @db+0x7c),
     **36-byte entries** (`idx*36`), forwards to
   - `constructMaterial(driver, SMaterial*, scene)` @0x7bd1bc (620 B): SMaterial =
     {+0: char* name, +4: effect-instance obj}; resolves via the scene factory
     ([scene+0x140]+0x28, vtbl+0x30/0x3c/0x20 calls; strips '\\'/'/' from the
     resolved name, registers via factory vtbl+0x2c) and builds the CMaterial
     through the effect-instance vtbl+0x38 call; result stored to SBatch{+8:
     CMaterial*, +0xc: CMaterialVertexAttributeMap*} (getBatchMaterial @0x44ef08
     confirms the SBatch layout); then
     `CMaterialVertexAttributeMap::allocate(CMaterialRenderer)` @0x87d110 — the
     s44 30-byte attribute-map path, per batch.
2. `setMaterialParameter<CMaterial, SSetParam>` @0x7891d0 (2,680 B): dispatches on
   the material-renderer reflection entry's value-type byte ([r7+9], 16 B
   reflection entries, count [..+0xc]); **sampler case (type 13) @0x78952c**:
   iterates SSetParam+0x14 value array (20 B entries), skips null-entry slots,
   `CColladaDatabase::constructImage(IVideoDriver*, SImage*)` @0x7bd5fc builds the
   ITexture from the DB SImage, `IMaterialParameters::setParameter<ITexture>(slot,
   unit, tex)`, then `applyTextureSampler` with the SSamplerState from
   SSetParam+4..+10.
3. `CCustomColladaFactory::getSamplerState` @0x43d504 (40 B): out.filter = 1;
   **out.wrap = (byte@[db->+0x18]+0x2f) > 1 ? 3 : 1** — a DB-GLOBAL byte, NOT
   per-material. Closes s45's pending wrap item: no per-material wrap state
   exists anywhere; engine default = internal enum 1 (REPEAT-equivalent), 3 =
   the clamp variant.

## Where compiled sampler slots are filled — elimination results

- Compiled DB setparam values: **651/651 sampler entries** (307 nodes, full
  population — extends s45's 2-record walk) have value block = {1, next_ptr,
  0xff, 0xff, 0xff, 0xff} with terminal 0xffffffff. No image linkage at v1/v2
  or one dereference deeper (0 hits).
- Image-table pointer hunt (176 name_ptrs + 176 tga_ptrs as u32):
  back region 0x36ac8..0x6f164 = **0 hits**; technique/pass/uniform regions = none;
  **all six zone bins = 0 hits** (lod_table 33,484 B, stream_info 32 B,
  batch_info 60,483 B, bih_struct 73,501 B, bih_data 270,969 B, lod_selector 36,126 B).
- String co-location material-name <-> tga-name within +-160 B: **0/22**
  occurrences (first 20 materials, all their pool occurrences).
- batch_info role in the binding: NONE for textures — addBatch consumes only the
  u16 material index (and T3's vertex declarations via the attribute map).
- BRES header mapped: sections 0x3c..0x168a8 (dir+offset array), 0x168a8..0x229b4
  (name pool, 49,420 B), 0x229b4..0x22a94 (224 B, small — unidentified),
  0x22a94..0x6f164 (image table + effect-instance nodes + back region).

## Conclusion (honest)

The engine fills sampler slots ONLY through per-instance SSetParam application
(constructScene path). For the 307 streamed city materials, no static
per-material image binding exists in the compiled DB or the zone bins; the
remaining candidates are (a) DB-loader synthesis from the unmapped 224 B
section / offset-array encodings, (b) lvc per-object records, (c)
CResFileManager registry (@0x7dcc7c registers IReadFile+CColladaDatabase pairs).
The browser implementation keeps the s45 source.dae instance_effect table as
its binding source — its 99.1%/98.8% agreement with the deployed street GLB
stands unchanged; what changed is that we now know the engine CANNOT be getting
these bindings from the compiled DB's sampler slots either.

## Artifacts

s46_t1_disasm.py, s46_t1_valptrs.py (+ s46_t1_setparam_walk.json),
s46_t1_backregion.py, s46_t1_region_dump.py, s46_t1_poolscan.py.
