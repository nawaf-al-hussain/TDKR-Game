# s47 T2 — batch descriptor layout: END-offset semantics; 307/307 tile; 1526/1526 stride; @16/@20 3-byte field = packed signed-byte NORMAL

## Corrected descriptor semantics (resolves the s46 contradiction)

Descriptor = 12 B, **BE u16 sextuplet {attr, B, C, stride, off, pad}** at
record offset 40 (N = u8 @33; batch_info record stride 197, 307 records):

- `attr` = the engine vertex-attribute enum (0 Position, 1..15 TexCoord0-14,
  16 Normal, 17 Color0, 18 Color1) — confirmed by the tiling + semantic tests.
- `C` = E_VERTEX_ATTRIBUTE_VALUE_TYPE; size table **[1,1,2,2,4,4,4]
  (Byte,UByte,Short,UShort,Int,UInt,Float) at 0xb8613c** in libKRHP.so.
- **`off` is the END offset (exclusive), not the start.** The attribute spans
  [prev_end, off); the last descriptor's off == 0 means "[prev_end, stride)".
- size = B x VAVT_size[C]; **B == 0 marks the 3-byte packed normal** (3 signed
  bytes + 1 pad).

Under s46's START reading, Position@12 (12 B) overlapped TexCoord0@16 —
impossible; under END reading everything chains exactly. The B=6 for Position
counts 16-bit units (6 x 2 B = 12 B = f32x3); C=3 (UShort class, 2 B).

## Declaration classes (all 307 materials)

| stride | attrs in file order | count |
|---|---|---|
| 24 | Position[0,12) TexCoord0[12,16) TexCoord1[16,20) Normal[20,24) 3B+pad | 276 |
| 24 | Position[0,12) TexCoord0[12,16) Normal[16,20) 3B+pad Color0[20,24) | 9 |
| 28 | Position[0,12) TexCoord0[12,16) TexCoord1[16,20) Normal[20,24) 3B+pad Color0[24,28) | 9 |
| 20 | Position[0,12) TexCoord0[12,16) Color0[16,20) | 10 |
| 20 | Position[0,12) Normal[12,16) 3B+pad Color0[16,20) | 1 |
| 20 | Position[0,12) TexCoord0[12,16) Normal[16,20) 3B+pad | 1 |
| 12 | Position[0,12) | 1 |

**Tiling EXACT: 307/307** (chain + end == stride). A (B,C)-shuffle null inside
a record still tiles (size multiset preserved) — that null is uninformative
and was discarded; the discriminating nulls are semantic (below).

## File-stream vs render-copy: FILE STREAM

- Seg stride agreement: **1526/1526** (s46: 1507/1526; the 19 vb-ambiguous
  segs are exactly resolved by the declarations).
- Positions @0 f32x3: 667,188 vertices decoded; **100.0000% inside the
  bih_struct root AABB** (x[-1620.0,185.2] z[-1312.7,-246.8] y[-24.5,171.5];
  the bih bbox is (x,y,z) while the stream stores (x,z,y)); structural errors
  (e.g. a 4-B-off base) produce NaN/pattern garbage and are caught.
- The @0 f32x3 positions are the SAME bytes s46 proved BIT-IDENTICAL to the
  deployed street GLB (986/986 segs) — the file stream and the declaration
  agree.
- UVs (snorm16 /32767): 2622 TC0/TC1 blocks, **0 non-finite or |v|>8**.

## The 3-byte field = packed signed-byte NORMAL (engine attr 16)

- signed bytes /127: |n|-1 median **0.024** over 400 blocks (261/400 within
  0.15 of unit length); bias-127.5 decode: 0.395; random-byte null: 0.188.
- Semantic label-shuffle null (decode the Color0 slot as a normal, blocks with
  both attrs): real 0.024 vs color-slot **2.478** vs random 0.975.
- s46's "@16 = TexCoord0" conclusion is REFUTED; the s46 task book's
  "Normal@16" guess is REHABILITATED with the correction that the normal sits
  @20 in the dominant 276-material class and @16 in the 9-material class —
  the END-offset semantics is what fixes both.
- The s46 strict smoothing-failure count (301) is unaffected by this rename:
  the normal VALUES are where s46's smoothness test read them (the 3-byte
  field), only the attribute NAME and the start offsets were wrong.

## Verdict

The batch_info descriptors are the **file-stream vertex declarations** with
END-offset semantics; they tile exactly for all 307 materials, match all 1526
segment strides, and their attr assignment passes the positional/UV/normal
semantic tests against independent artifacts (bih AABB, s46 GLB bit-match)
while the semantic nulls separate by >8x. The 3-byte field is the packed
signed-byte normal; TexCoord1 @16 (276-class) is the lightmap-coord input the
s45/s46 lightmap chain (w4_raw*s133+s145) consumes.

## Artifacts

s47_t2_dump.py, s47_t2_validate.py, s47_t2_nulls.py, s47_t2_nulls.json.
