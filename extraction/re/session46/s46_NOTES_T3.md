# s46 T3 — batch_info vertex declarations DECODED (307/307); stride field VALIDATED (1507/1526 + null); @16 = TexCoord0 (task guess refuted); counts reconciled — PASS

## Record structure (batch_info.bin, 60,483 B = {u32 stride=197} + 307 x 197 B)

- `[0..2]` u16 mat id (LE; rec73 = 73), `[4..32)` 28-B unit-map (small increasing
  marks 01/02/03... = texture-unit-ish list), `[32..40)` header (N = u8 @33),
  `[40..40+12N)` N x 12-B descriptors, **BIG-ENDIAN u16 fields**:
  `{attr, unit, type, stride, offset, pad}`.
- attr = engine E_VERTEX_ATTRIBUTE id (s43 enum: 0=Position, 1=TexCoord0,
  2=TexCoord1, 16=Normal, 17=Color0); unit = small int (census 0/1/2/6);
  type = data-type code (2/4 = 4-B, 3 = 12-B-or-unresolved, 1 = 4-B);
  stride = the material's vertex stride; offset = slot offset.

## Declaration table per stride class (xN materials)

- **stride 24** (285 mats): Normal(t3)@0 | Position(t3)@12 | TexCoord0(t2)@16 | TexCoord1(t2)@20
- **stride 24 variant** (9 mats): Color0(t4)@0 | Position(t3)@12 | TexCoord0(t2)@16 | Normal(t3)@20
- **stride 28** (9 mats): Color0(t4)@0 | Position(t3)@12 | TexCoord0(t2)@16 | TexCoord1(t2)@20 | Normal(t3)@24
- **stride 20** (12 mats): Color0(t4)@0 or Normal(t3)@0 | Position(t3)@12 | TexCoord0(t2)@16 (no TexCoord1)

## Validation

- Per-seg stride agreement: **1507/1526** segs declare exactly their detected
  vertex stride. The 19 "mismatches" are ALL stride-ambiguous segs (vb
  divisible by both 20 and 24) on the mixed-stride materials (300/303/...):
  the declaration DISAMBIGUATES them (declared stride wins; the s43/s44
  greedy 24-preference was the arbitrary choice).
- Shuffled-material null: re-assigning declarations to materials at random ->
  12.1% mismatch vs real 1.25% (10x separation).
- Offset tiling with natural type sizes does NOT close (24 = 12+?+4+4):
  the offset/type-size semantics need the engine's attribute-type table
  (s43's type-name pool) — plausibly CInterleavedDataAllocator repacked slots
  (s45's correction). Named-next: type table from the engine, then exact
  repacked layout.

## The @16 answer (task question)

- **@16 = TexCoord0 (attr 1, type 2) in ALL stride classes** — the task's
  guess (attr 16 = Normal at stride-24 @16) is REFUTED by the declaration.
- Normal (attr 16, type 3) sits at @0 (stride 24) / @24 (stride 28); Color0
  (attr 17, type 4) at @0 where present.
- NOTE: this declaration is the RENDER/allocator layout requested per
  material — it is a DIFFERENT thing from the s43/s44 STREAM storage layout
  (pos@0, uv0@12, F@16, color@20) that the smoothness analyses used; both are
  real, and this decode explains what the engine does with the streamed
  fields (addBatch: CMaterialVertexAttributeMap::allocate from this record).

## Failing-smoothness counts (238 / 301 / 615) — reconciled

- s43 single-null criterion: 238 fail (one shuffled null per seg).
- s44 strict min-of-4 nulls: 301 fail (seg must beat ALL four shuffles) —
  **ADOPTED** (conservative).
- s43's reported 615 = its looser single-null run + island2's 305 — a
  criterion/population mixture, not a contradiction (s45 reconciliation
  stands; same 1,526-island1 population for 238/301).

## Artifacts
s46_t3_batchinfo.py, s46_t3_decode.py, s46_t3_final.py,
s46_t3_batchinfo_decoded.json, s46_t3_final.json.
