# RE session 9 — zone-stream archive (the streamed near-field city)

## Discovery: GothamCity*.zip inside l_gothamcity.gla

`l_gothamcity.gla` contains SIX PK/ZIP chunks the exporter had never touched:

| chunk | bytes | content |
|---|---|---|
| GothamCity.zip | 41,080,993 | island 1 full-detail street level |
| GothamCity_Island2.zip | 37,926,329 | island 2 full detail |
| GothamCity_low.zip | 25,298,749 | island 1 low LOD |
| GothamCity_Island2_low.zip | 22,491,217 | island 2 low LOD |
| GothamCity_low_inorm.zip | 22,104,505 | island 1 low (inverse-normal?) |
| GothamCity_Island2_low_inorm.zip | 19,625,168 | island 2 low variant |

168.5 MB total — the streamed street-level city (roads, sidewalks, parks,
street props, rooftop equipment) that renders when the camera is on the
ground. The deployed viewer (sessions 1-8) only used the LongDist skyline +
footprint tiers; this is where the real near-field density lives.

## Zone zip payload (8 entries)

- `GothamCity_materials.bdae` — **nested ZIP** with 5 BRES variants
  (big/little-endian × quantized/not) + `source.dae` (the original COLLADA:
  307 materials island 1 / 196 island 2, 25 unique base material names,
  `tiles` ×128, `Material__69` ×66, `Material__3242` ×36...) +
  `dependancies.txt` (shader/texture dependency list) + `version.nfo`.
- `stream_info.bin` (32 B) — 6×f32 world AABB + (u32 vertexCount, u32 batchCount=197)
- `lod_table.bin` — `[u32 N=1526][N×(u32 off,u32 sz)]` segment descriptor
  table + `[u32 M=5317][M×u32]` leaf index stream (strip over segment ids,
  0xFFFFFFFF separators, values 0..1525)
- `lod_data.bin` (36.6 MB) — all segment vertex+index blocks, then the
  descriptor table (last ~325 KB), then BIH payload
- `batch_info.bin` (60,483 B) — `[u32 197]` + bit-packed per-batch records
  (contains vertex element sizes 20/12/16 — vertex format declarations)
- `bih_struct.bin` (73.5 KB) — AABB + BIH nodes
- `bih_data.bin` (271 KB) — `[u32 5317]` + per-leaf payload (culling)
- `lod_selector.bin` (36 KB) — tag stream: u32 tags 'rang', 'proj', 1=name;
  per-batch LOD range/projection data (read by CDoubleBufferedLODStreaming ctor)

## Proved binary layouts (data-verified)

Descriptor (per segment, 140-1290 B at lod_table pair offsets — pairs point
into lod_data END region; base 100 B + 50 B per extra LOD block):
```
+0   u32 triCount (whole segment)
+4   6×f32 3D bounds (y, x, z order, 2 corners)      [+16 second bounds block]
+68  u32 dataOff   (absolute offset into lod_data of this segment's block)
+72  u32 =4        (constant)
+76  u32 vBytes    (LOD0 vertex bytes)
+80  u32 iBytes    (LOD0 index bytes)
+84  u32 fmt1      (packed UV/scaleoffset data — per segment)
+88  u32 fmt2
+92  u32 0x00010000
+96  u32 0xffff0000 (LOD0 terminator)
+100..    packed 64 B + further LOD blocks at +168 (same 36 B layout:
          [off][4][vBytes][iBytes][fmt1][fmt2][0x00010000][0xffff0000])
```

Segment data block (at dataOff):
```
+0    u32 header   (0x5150c200 / 0x5150ca20 ... — sentinel seen on degenerate
                    quad; role TBD, 4 B always present before vertices)
+4    vertices     (vBytes; stride 24 B typical, 20 B on some — auto-picked
                    by (vBytes%stride==0 && maxIndex<vBytes/stride && coords sane))
        24B: [f32 a][f32 b][f32 c][u32 oct-normal][u32 X][u32 Y]
        20B: [f32 a][f32 b][f32 c][u32 oct-normal][u32 uv]
        (a, b) = game x/y, c = game z (up). oct-normal = 2×snorm16 octahedral
        (0x7fff8001 → (1,-1) → +x for walls; 0x00810000 → (0,0.006) → up for
        ground). X/Y dwords: 130 seen as constant on walls, 0xffffffff on the
        sentinel — UV/extra channel split TBD (batch_info likely declares it).
+4+vBytes  indices (iBytes; u16 triangle strips, 0xFFFF = strip cut)
```

Validation: sum over 1526 descriptors of (4+vBytes+iBytes) for LOD0 blocks
covers the pre-descriptor region exactly; extracted coordinate AABB matches
stream_info word-for-word; island 1 = 1,517/1,526 segments decoded
(651,431 verts, 785,053 tris), island 2 = 1,020 segments (536,668 verts,
660,668 tris).

## Materials — authoritative binding STILL OPEN

The zone's own material graph is in `little_endian_not_quantized.bdae`
(BRES 0xFFFE; texture list parses, 176 images) but its material DB is a
compiled-COLLADA structure (image library = (id,init_from) string-offset
pairs starting 0x22a94; then effects/materials) that ground_truth.py's
sampler-record scan does NOT match (0 records). `source.dae` gives
materials+effects but no per-instance texture values. The batch→material
link is inside batch_info.bin's bitstream (197 records; vertex element
sizes visible but not yet parsed).

Consequence: street-tier textures are bound by constrained heuristics
(scripts/export_zone.py v4): flat ground → island bake family at 2x (the
zone 'tiles' materials are LightMapDC — bake-lit, consistent with the
LongDist Roads meshes); small-UV-box flats with strong scores →
grass/dirt/sand albedo tiles; props < 15 units with decisive scores →
Z1_Props atlases; everything else → __dark. Authoritative parse of the
compiled material DB (+ batch_info bitstream) is the follow-up that
replaces the heuristics.

## Engine side (symbols)

Loader = glitch::scene::CDoubleBufferedLODStreaming<
  CDoubleBufferedDynamicBatchMesh<SDoubleBufferedDynamicBatchMeshDefaultConfig>>
ctor @0x45e190 (args: this, IReadFile lod_selector, IReadFile lod_data,
IReadFile lod_table, CSceneManager*) — reads selector tag stream ('rang',
'proj'), lod_table ([N][pairs][M][u32s]) exactly as decoded above.
CDoubleBufferedDynamicBatchMesh ctor @0x45c750 reads bih_struct (AABB first,
then counts/arrays). process() @0x469d94 streams segment blocks.
Strings 'stream_info.bin/bih_data.bin/bih_struct.bin/batch_info.bin/
_materials.bdae/lod_table.bin/lod_data.bin/lod_selector.bin' at .so
0xb40704.. (PC-relative refs).
