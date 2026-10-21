# T5 — 615 vs 301 RECONCILED (criteria differ, population identical); engine declaration hunt advanced but the +16 field's engine semantics remain UNRESOLVED (time-box)

## Count reconciliation (from the SHARED saved per-segment data, s44_t2_ffield.json)

The same 1,526 island1 segments underlie both sessions' numbers. On the saved
per-segment rows (s + null_med + null_min per segment):
- s43 criterion (s < one shuffled-null median): **238 fail** (stride 24: 165,
  stride 20: 73); pass+indeterminate 1,288 = s43's reported "904 pass" family.
- s44 strict criterion (s < min of 4 nulls): **301 fail**.
- s43's REPORTED 615 = its own looser single-null paired run (615 island1 +
  305 island2, with ~7 segments skipped by the four!=4 filter).
No population contradiction: the sessions applied different criteria
(single-null vs min-of-4, different shuffle construction/normalization) to the
identical segment set; 301 is the strict number, 238 the analogous criterion
on shared data, 615 the historical loose count.

## Engine evidence gained (disassembly)

- **CVertexAttributeMap(uchar*) ctor @0x86c8b0 = a raw 30-BYTE copy**
  (mov r2,#0x1e + memcpy helper 0xa4e1c) — the batch_info attribute map IS 30
  bytes copied verbatim; the three ctor variants (@0x86c8b0/0x86c8d0/0x86c8f4)
  copy from src, src+4, src+4 respectively. CMaterialVertexAttributeMap
  @0x87ce88 allocates 0x24-B objects and performs the SAME 0x1e-byte copy per
  material — one 30-byte map per material, no per-entry decoding in the ctor.
- addSegment's per-material request loop @0x46e6fc: `ubfx ip, r1, #0xc, #4`
  extracts a 4-bit UNIT field from the segment request word, then walks the
  bitmask r2 = 1,2,4,8,16 (`tst r2, lr` against the material's usage byte at
  [unit-table + r3]) — a sampler-unit request, not a vertex-attribute
  declaration.
- **Correction to the s44 notes: 0x473088 is NOT a constant list** — it is
  glitch::core::CInterleavedDataAllocator<...> (called from addSegment
  @0x46e364 with r1=[fp+4], r2=[r5+0x24], r3=sb). The streamed per-stride
  vertex declaration is constructed through this allocator + the
  SSegmentStreamingInfo fields ([fp+4], [r5+0x24]) + the 30-byte
  CMaterialVertexAttributeMap; the tracer dump on a hand-built structure
  remains the named next step (NOT DONE — time-box).

## Standing state of the +16 3-byte field

The engine-declared semantics for the +16 field (stride 24) remain UNRESOLVED;
the s43/s44 data-driven account (s8-smooth on the lit subset, legitimately
noisy on hard-surface content, oct/1010102 rejected) stands as the best
current interpretation, now with the count discrepancy removed. The engine
evidence above narrows where the declaration lives (interleaved allocator +
30-byte material map) for the next session's tracer dump.

Artifacts: none new beyond the disassembly probes (reconciliation used the
committed s44_t2_ffield.json).
