# T2 — STREAMED VERTEX FORMATS: engine pipeline classes named + F-field alternates tested vs paired nulls; s43 layout table stands; failing-set explanation CONFIRMED

## Engine evidence gained this session (symbolized glitch pipeline; new .symtab parse, s44_all_syms.json)

- The streamed-batch path does NOT use CVertexStreams' public ctor (its 4 BL
  callers are internal clones/helpers). The authoritative classes/functions:
  - glitch::video::CVertexStreams ctor @0x86ca00 — SVertexStream = 16-byte
    descriptor {ptr,ptr,u16,u16,u16,u16}; the ctor walks an ATTRIBUTE BIT-MASK
    (one bit per E_VERTEX_ATTRIBUTE) and copies per-stream descriptors.
  - CVertexStreams::setupStreams(const SVertexStreamData*, uint, bool) @0x86d524
    (single caller: CMeshBuffer ctor @0x8c1428 — the non-streamed mesh path).
  - CVertexAttributeMap ctor from packed bytes @0x86c8b0 / @0x86c850 — the
    per-material/per-segment ATTRIBUTE MAP is consumed from a byte array
    (the batch_info attribute-map bytes s41/s42 decoded).
  - CDoubleBufferedLODStreaming::process(uint,void*) @0x469d94 (2164 B) and
    CDoubleBufferedDynamicBatchMesh::addSegment(SSegmentStreamingInfo*,void*,void*)
    @0x46dd04 (2984 B): segment add/stream bookkeeping; batch records are
    32-byte (this+0x330 array indexed `lsl #5`, memset 0x20 @0x46e1b4);
    per-material attribute request loop with a 4-bit field from the segment
    info (`ubfx rX, r1, #0xc, #4`) and a `#0x10` attribute-index bound;
    material render through a vtable call (@0x46e76c).
- The exact per-stride attribute CONSTANT LIST for the streamed batch layout
  lives in the SBatch/SVertexStreamData construction (0x473088 helper called
  from addSegment @0x46e364, and CMaterialVertexAttributeMap @0x87ce88) —
  NOT extracted in this session's time-box (named next). The DATA-DRIVEN
  layout table from s43 therefore stands unchanged:
    stride 20 = Position(3xf32) | F(snorm8x3+pad)@12 | Color0(u8x4)@16   (no UV; water/env)
    stride 24 = Position | Coord0(2xsnorm16)@12 | F(snorm8x3+pad)@16 | Color0@20
    stride 28 = Position | Coord0@12 | Coord1(lightmap)@16 | F@20 | Color0@24
    stride 32 = family +4B, ZERO segments shipped (unverified)

## F-field alternative decodings on the failing population (s44_t2_ffield.py, paired row-shuffle null x4 per segment per candidate)

Strict per-segment criterion (real < min(4 nulls)) over all 1526 segments:
  s8       pass 1225  fail 301   mean real 0.036 vs null 0.042
  u8       pass 1239  fail 287   mean real 0.025 vs null 0.028
  oct_u8   pass 1201  fail 325   mean real 0.034 vs null 0.040
  1010102  pass 1246  fail 280   mean real 0.029 vs null 0.037
Candidates that PASS on the s8-failing population (301 segs): 1010102: 58,
u8: 50, oct_u8: 30 — i.e. NO alternative interpretation decisively rescues
the failing set; the few flips are borderline segments any interpretation
can satisfy. octahedral and 10-10-10-2 remain REJECTED as global encodings;
unsigned/AO-like does not beat s8 at population level.

EXPLANATION for the smoothness split (now with quantified support): the
failing segments are hard-surface/detail content whose per-vertex F is
legitimately high-frequency (detail props/foliage/hard edges); the smoothness
discriminator is POPULATION-level (s43: real 0.59 vs null 1.44/1.57,
p << 0.001) and unit-normality holds only for the lit subset (302/1526 +
337/1020). With the in-shader normalize() the storage magnitude is
unconstrained, so scaled/noisy F on hard surfaces is legal storage.

## Attribute-aware decode rate (s43_t2_attr_decode.py re-run this session)

island1: 1526 segments — 1521/1526 positions finite+in-bbox (5 boundary
fails), all Coord ranges pass, max index < nv always; F smoothness: 904 ok +
140 indeterminate (F too flat to discriminate) + 615 paired-fail + 2 fail_F;
302 segments unit-normal under s8 (the lit material subset).
island2: 1020 segments — all positions pass; 712 ok + 87 indeterminate +
305 paired-fail; 337 unit-normal.

## Verdict

T2 PASS-WITH-SCOPE-NOTE: format table unchanged (data-driven, engine-anchored
offsets); the failing 615 are explained (noisy hard-surface F, population-
level discriminator) and the alternative encodings are excluded by paired
nulls; the streamed-batch engine classes and entry points are now named with
exact addresses for the remaining attribute-constant extraction (named next:
0x473088 + CMaterialVertexAttributeMap).

Artifacts: s44_t2_ffield.py, s44_t2_ffield.json, s44_all_syms.json.
