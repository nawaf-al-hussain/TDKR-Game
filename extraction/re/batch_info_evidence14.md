# batch_info.bin — LAYOUT SOLVED (session 14), value semantics open

## TL;DR

The zone `batch_info.bin` files are **per-MATERIAL tables**, not per-batch
records:

```
batch_info.bin := u32(197) + M × 197-byte records
                 M = material count of the zone's <island>_materials.bdae
                    GothamCity          M = 307  (file 60,483 B = 4 + 307×197)
                    GothamCity_Island2  M = 196  (file 38,616 B = 4 + 196×197)
record(m) := byte0 = m  (the material index — 307/307 and 196/196 exact,
                          wraps mod 256 for m ≥ 256)
             + 196 bytes = one byte per slot of a FIXED 196-slot space
```

- The leading `u32 = 197` in BOTH files is the **record stride in bytes**,
  NOT a record count.  The same `197` is the last u32 of the zone's
  `stream_info.bin` — so it is a per-zone CONSTANT the engine stores twice.
- The earlier interpretations ("197 records of 307/196 B", "307/196-byte
  fixed records") are DEAD.  The exact divisions that motivated them are
  real but arithmetic coincidences of the TRUE layout:
  (filesize − 4) / 197 = M = material count, exactly, because the file IS
  M records of 197 bytes.
- The byte grid is NOT row-major over (197 × M): the records live at
  stride 197 from the body start, which is what put the material indices
  on the "diagonal" of the mis-gridded view (body[197k] == k held 195/195
  and, with mod-256, 307/307).

## stream_info.bin (32 B, both zones) — also decoded

```
[6 × f32]  axis-aligned streaming bbox of the zone (LE)
           GothamCity          min ≈ (-1605.99, -1312.34, -27.39)
                               max ≈ (  178.20,  -246.82, 203.72)
           GothamCity_Island2  min ≈ (-1087.72,  -858.42, -27.14)
                               max ≈ (  290.59,   535.18,  90.28)
[u32 X]    234,466 (island1) / 303,832 (island2) — meaning open
[u32 197]  the batch_info record stride (same constant as the file header)
```

## What the 196 bytes inside a record look like

Statistics over all records of both islands:

- **0xFF in 13.4% of cells (both islands — same fraction), 0x00 in 68.3%**,
  remaining ~18% carry values 0..254 with **saturation at 254** (0xFE).
- The 0xFF cells form runs of exactly **12–13** (540 runs of 13 in island1)
  — contiguous slot ranges unused by that material.
- Adjacent batch-slots hold similar values (adjacent-slot similarity 0.99
  island2 / 0.99 island1 col-wise) — spatial coherence along the slot axis.
- Values are NOT monotone along slots; per-record max sums to 74,934
  (island1) / 47,949 (island2) — no clean match to segment counts
  (1,526 / 1,020), so the value semantics are still open (see below).
- Several records embed small groups of IEEE f32 LE (16 B + 3 × 8 B with
  4-byte zero gaps, around in-record offsets ~75–115).  Sampled values are
  tiny (1e-6..1e-4), 0.4-0.5, 0.85-0.97 and ±2.6 — consistent with UV
  rects (u0,v0,u1,v1) or normalized bounds.  Example from island2 material
  1's record: 3.6e-4, 1.8e-4, 0, 0.4814, -2.587.

## Candidate readings of the 196 slots (open)

1. **Fixed batch pool**: the engine's streaming batch pool has a constant
   size (196 or 197 with slot 0 = the self-index).  CLevelStreaming_DB /
   CDoubleBufferedDynamicBatchMesh allocate fixed pools; both islands
   sharing the SAME slot count (196) while their segment counts differ
   (1,526 vs 1,020) supports a fixed-size engine pool, not per-zone data.
2. cell(m, s) = per-(material, slot) quantity saturating at 254 — segment
   counts (a material can exceed 254 segs in one slot → cap), or 8-bit
   quantized weights/areas.
3. 0x00 vs 0xFF as two distinct "empty" codes (allocated-but-empty vs
   not-applicable).

What would settle it: the engine reader.  `CLevelStreaming_DB::Load`
(0x406dfc, symbol `_ZN18CLevelStreaming_DB4LoadE...`) orchestrates; the
per-file parse is in non-exported helpers (bl targets from Load:
0x4043f8 = CLevel::LoadGlobalObjects, 0x3dac58 ×8, 0x42e2bc ×7,
0x455e2c ×6).  NOTE: the stream name table ('.zip', 'stream_info.bin',
'bih_data.bin', 'bih_struct.bin', 'batch_info.bin', '_materials.bdae',
'lod_table.bin', 'lod_data.bin', 'lod_selector.bin') at .rodata 0xb40704
has **NO absolute pointers anywhere in the image** (verified by full-file
literal scan ±0x800) — it is indexed at runtime via a computed base, so
finding the reader needs the enum-index code path, not a string xref.

## Hexdumps for the collaborator

### First 64 bytes — GothamCity (island1)

```
00000000  c5 00 00 00 00 00 00 ff ff ff ff ff ff ff ff ff  ................
00000010  ff ff ff ff ff ff 01 02 ff ff ff ff ff ff ff ff  ................
00000020  ff ff ff ff 00 03 00 00 00 00 00 00 00 00 00 06  ................
00000030  00 03 00 14 00 0c 00 00 00 10 00 00 00 03 00 14  ................
```

### First 64 bytes — GothamCity_Island2

```
00000000  c5 00 00 00 00 00 00 ff ff ff ff ff ff ff ff ff  ................
00000010  ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff  ................
00000020  ff ff ff ff 00 01 00 00 00 00 00 00 00 00 00 06  ................
00000030  00 03 00 0c 00 00 00 00 00 00 00 00 00 00 00 00  ................
```

Reading under the SOLVED layout: island1 record 0 (material 0) =
`00 | 00 00 ff×15 01 02 ff×12 00 03 00×9 06 00 03 00 14 00 0c ...`
island2 record 0 (material 0) =
`00 | 00 00 ff×22 00 01 00×9 06 00 03 00 0c ...` (the earlier
"record template" sightings were these material-0/1 records mis-sliced).

### Two consecutive records — island1 (material 0, material 1)

```
material 0 @ body 0x000 (file 0x004), 197 B:
00000000  00 00 00 ff ff ff ff ff ff ff ff ff ff ff ff ff  ................
00000010  ff ff 01 02 ff ff ff ff ff ff ff ff ff ff ff ff  ................
00000020  ff ff ff 00 03 00 00 00 00 00 00 00 00 00 06 00  ................
00000030  03 00 14 00 0c 00 00 00 10 00 00 00 03 00 14 00  ................
00000040  10 00 00 00 11 00 01 00 04 00 14 00 00 00 00 00  ................
00000050  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
...  (zeros through 0xc0)
000000c0  00 00 00 00 00 00 00 00 00 00 01 00 00 ff ff ff  ................
material 1 @ body 0x0c5 (file 0x0c9), 197 B:
000000c0  00 00 00 00 00 00 00 00 00 00 01 00 00 ff ff ff  ^
000000d0  ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
000000e0  ff ff ff ff ff ff ff ff ff 00 01 00 00 00 00 00
000000f0  00 00 00 00 06 00 03 00 0c 00 00 00 00 00 00 00
...  (zeros)
```

(note: island1 material 1's record starts `01 00 00 ff...` — first byte =
index 1; the record boundaries sit at file offsets 4+197·m.)

### Two consecutive records — island2 (material 0, material 1)

```
material 0 @ body 0x000 (file 0x004), 197 B:
00 00 00 ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
ff ff ff ff ff ff ff ff 00 01 00 00 00 00 00 00 00 00 00 06 00 03 00 0c
00 00 00 00 ... (zeros to end)
material 1 @ body 0x0c5 (file 0x0c9), 197 B:
01 00 01 02 ff ff ff ff ff ff ff ff ff ff ff ff ff 03 04 ff ff ff ff ff
ff ff ff ff ff ff ff ff 00 05 00 00 00 00 00 00 00 00 00 06 00 03 00 1c
00 0c 00 00 00 01 00 02 00 02 00 1c 00 10 00 00 00 02 00 02 00 02 00 1c
00 14 00 00 00 10 00 00 00 03 00 1c 00 18 00 00 00 11 00 01 00 04 00 1c
00 00 ... (zeros) ... then float groups:
13 c3 b7 39 | dd 66 36 39 | 00 00 00 00 | 40 59 f6 3e | 32 fe 25 c0
00 00 00 00 | 40 23 88 35 41 3b 19 36 | 00 00 00 00 | 56 1a 5e 3f
99 fd 14 3f | 00×8 | 06 00×3 01 00×17(end)
```

### lod_table.bin — first 5 rows

Layout (proved session 9): `[u32 N][N × (u32 off, u32 sz)][u32 M][M × u32]`.

```
GothamCity          N = 1,526 segments, M = 5,317 leaf refs, 33,484 B
GothamCity_Island2  N = 1,020 segments, M = 3,504 leaf refs, 22,184 B

island1 rows (off into lod_data.bin, sz):
  0: off 0x02296354  sz 248
  1: off 0x0229644c  sz 248
  2: off 0x02296544  sz 248
  3: off 0x0229663c  sz 248
  4: off 0x02296734  sz 248
island2 rows:
  0: off 0x01f7683e  sz 140
  1: off 0x01f768ca  sz 140
  2: off 0x01f76956  sz 140
  3: off 0x01f769e2  sz 140
  4: off 0x01f76a6e  sz 140
(segment byte sizes overall: island1 140..1290, island2 140..1190;
 most common 140 — segment blocks are small and uniform)
```

### Material name order (source.dae inside <island>_materials.bdae)

The names below are in library_materials order — the SAME order as the
batch_info records (record m ↔ name[m]) is the working hypothesis to
verify.  Full lists are committed at
`extraction/re/batch_info_material_names14.txt`; the first 8:

```
island1 (307): _1_-_Default_1xVPfvJcrg_rQF69AzBla, Null Material,
  StorageBox_pKSKQEDc8M_2iSKoUn9jv, Material__6034_xdCAB7nmt6_wNEFXgz2lI,
  Material__340_CZEYIFmh2K_CXJxhZFaBp, _1_-_Default_X4l28T8yGh_WmqflCvCVi,
  Material__356_mJcKbWsYbs_lisPNWCIT, Material__356_mJcKbWsYbs_CbfmmRlYK ...
island2 (196): Null Material, Material__4221_0W4tpNHUR8_fAGa34PFrs,
  Material__4221_0W4tpNHUR8_859i09eK8F, Material__4221_0W4tpNHUR8_2qDuEgRiSQ,
  Material__18441_1mj3g9vBJ2_DDQn19BblM, ...
```

Regenerate any time:
`python3 extraction/re/parse_zone_collada.py` (needs the zones unzipped).

## What changed vs the previous brief

- "both files begin u32 197; (size−4)/197 exact (307/196)" — EXPLAINED:
  197 = record stride, 307/196 = record COUNT = material count.
- "island-2 repeating 196-byte record template with drifting tokens" —
  EXPLAINED: that was the material-0/1 records of the TRUE 197-stride
  layout sliced at the wrong period; the "drift" was the material index
  byte at each record start.
- "197 matches nothing counted so far" — RESOLVED: 197 = fixed record
  stride = fixed engine pool/record size, stored in stream_info.bin too.

## Ranked next steps

1. Disasm the batch_info parser (via CLevelStreaming_DB::Load helpers —
   the name table has no string xrefs; go through the enum-index code
   path) and read the field widths at the call sites.
2. Match material m's 196 slot values against the street GLB meshes'
   materials (the gt DB gives per-mesh material + segment provenance) —
   if slot s ≈ a batch of the streaming pool, mesh counts per
   (material, slot) should track the values.
3. Explain stream_info's X u32 (234,466 / 303,832).
4. Check bih_struct/bih_data for a 196/197-slot pool structure.
