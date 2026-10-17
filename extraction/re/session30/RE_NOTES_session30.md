# RE Notes — Session 30 (round 20)

## T1: the lvc parser runs with ZERO emulator-measured spans

### Cinematic (CCinematicComponent 0x17AC851F) — static spec, spans retired
Both Load functions were inverted from disassembly (full reader spines in
`cine_spine.txt` / `conttracks_spine.txt`):

- `CComponentCinematic::Load` **@0x2dce20, ret @0x2ddf8c** (the class's own
  Load = CCinematicComponent::Load @0x292b4c, vt+0x10 of vtable 0xbd24d0,
  which only constructs a 0x50-B CComponentCinematic and tail-calls 0x2dce20
  once — no other stream reads):
  `head [i dur][c][f][c]`
  `sec1 [i n1] + n1 x { [i][i cnt] + cnt x [i][i][i][i] }`   (16-B elems)
  `sec2 [i n2] + n2 x { [i cnt] + cnt x [i][i][STR][c] }`    (16-B elems)
  `sec3 [i n3] + n3 x { [i cnt] + cnt x [i][i][STR] }`       (12-B elems)
  `sec4 [i n4] + n4 x { [STR][i cnt] + cnt x [i][i][f x6] }` (32-B keys)
  `sec5 [i n5] + n5 x CContainerTracksAnimatedObject::Load`
- `CContainerTracksAnimatedObject::Load` **@0x2d9118, ret @0x2dad20** —
  the s29 dump of this function was TRUNCATED (ended 0x2d9984); the real
  function has EIGHT sections and ~38 more reader calls:
  `[i A]; [i B] + B x [STR][i][f][i][i];`
  `[i C] + C x { [STR][i cnt] + cnt x [f][f][f][i][i] };`
  `[i D] + D x { [STR][i cnt] + cnt x [STR][f][f][f][i][i] };`
  `[i E] + E x { [STR][i cnt] + cnt x [f][f][f][i][i] };`
  `[i F] + F x { [i cnt] + cnt x [i][i][STR] };`
  `[i G] + G x { [i cnt] + cnt x [STR][i][i][STR][c] };`
  `[i H] + H x { [i cnt] + cnt x [i][i][STR][STR][c][f][c][c] }`

Validation (`s30_cine_validate.py`): **95/95 real banked instances
byte-exact** (kinds, sizes, offsets AND values incl. STR resolution).
The 96th banked "span" (@1075, 34 B) is a STALE ARTIFACT: it lies inside
Underground's dedicated record 12 (0x1011, 1007..1077), was banked during an
intermediate s29 run when Underground framing still diverged, and the
engine's 34-B "read" there is a garbage-prefix-until-fault. With the final
spec set no level ever hits a cinematic component at that offset.

### shop — first differing record, tail tids, "2-byte residual"
Native ground truth: `walk_records_shop.json` (123-record engine walk).
- **First record that differs: record 5 (@0x17a, tid 0x16F31)** — the pure
  parser's 0x4CA5F00E (CComponentNewShopItemProperty) spec read only the
  40-B head. The real Load **@0x202ae4 (ret @0x203128)**, reached through
  the GENERIC switch (case @0x36958c, vtable 0xbd0a30, Load slot **vt+0x10**),
  continues with `[i count] + count x 51 B` where one item =
  `[c][i][i][f][f][f][f][STR][STR][STR][STR][i][c][i][c]`.
  rec5 native = 4 (tid) + 40 + 5x51 = 299 B ✓.
- After the fix: **123/123 native shop records match 1:1** (3 apparent
  mismatches are tid -1 signedness in the comparison, same 4-B consumption).
- The r19 "tail tids 0x16F3C-0x16F88" are **artifacts of the rec5
  under-read** (junk data words misread as tids), NOT real tids. The native
  tail: 0x3ccc..0x3cf0 = 9 four-byte skips (0x474c = template whose only
  component 0x1D50AA73 is unregistered -> 4-B record, positive-controlled;
  0x2711/0x34/0x0/-1/0x96 not templates -> skips; native ok=True each).
- At **0x3cf0 tid 0x19f0a1 IS a registered template** and the ENGINE itself
  mis-frames the exporter junk there: native walk ok=False, consumed to
  stream end (0x7433). The pure parser (component specs) lands 0x40ed.
  Both landings are arbitrary inside junk — **no u16/ReadShort reader, no
  count/sentinel read; the "2-byte residual" cause = exporter junk tail
  that the engine can only skip/mis-frame** (cause named per the PASS
  criterion). The engine's record-loop bound is the STREAM SIZE (r16
  disasm; shop's native walk ran past table_off to file end), so 0x40ec
  was never an engine boundary for shop.

### LevelInit trailing word ("i_nz") — REFUTED as engine semantics
The 0x2657 record = a template record whose component walk ends with
CTemplateLevelProperties::Load **@0x2023bc**: after LevelInit::Load
(0x2018f0) it reads `[f][STR][f][f]`, sub-load 0x202000, then an
**UNCONDITIONAL `ReadInt` @0x20240c** stored to [this+0x128], ret @0x202414.
Native tracer runs of 0x2023bc (this session): shop ends **0x14a**,
GothamCity **0x54c**, Island2 **0x330** — each exactly 4 B past the s25/s29
walker's record end (0x146/0x548/0x32c): the walker's spec omitted the word
on EVERY level. The fitted `i_nz` rule was a byte-equivalent patch over that
artifact (GC/I2 word 31004=0x791C "absorbed", shop word 0 "left as tid-0
record"). s30 replaces `i_nz` with unconditional `[i]`; all levels still
frame identically. Two independent signals: the disassembly + three fresh
native runs.

### CTrafficSetting (0x3189E053) — the last span class decoded
`CTrafficSetting::Load @0x1ffa1c, ret @0x1ffeb4`:
`head [i][c][f x3][STR][f x6]; [i n1] + n1 x [i][i][i];`
`[i n2] + n2 x { [i][i][i cnt] + cnt x [STR][f] + [i] }`.
Validation: **15/15 banked instances byte-exact** (`s30_traffic_validate.py`).

### Level status (pure parser, s30 table — ZERO measured spans)
10/12 to table end (GC 14313, I2 7474, BatCave 92, l_menu 31, Stadion 274,
Police 653, StockEx 2023, Underground 2653, Military 773, ThePit 700);
shop frames 123/123 native-verified records to 0x3cf0, then exporter junk
(cause named above); Test = data corruption (bogus STR index 960462848 at
0x464 vs a 124-entry pool; r17 engine-confirmed). Grammar unresolved: NONE.

### Independence (leave-one-out)
The s30 table contains no per-level measured data: spans/spans_e/span_toks
are gone, the 0x2657/0x798f engine-case specs are static, GCT templates come
from gol.bin (global), and the 0-read specs are .so-unregistration facts
(positive-controlled). Every level is therefore held-out; 10/12 parse with
the same table, and I2 parses with zero I2-derived bytes in any spec.

### JS vs Python
`test_lvc_s30.js` + `s30_expected.json` (Python-generated boundaries +
per-record SHA1 token hashes): **10/10 levels PASS** (GC 1584 ms, I2 1433 ms,
rest < 600 ms). The JS parser needed no code change — the new specs are
table data.

### Header count (offset 13)
Unchanged from r19: no fit across the 10 parsed levels; engine discards the
field (LoadRawLvl @0x4891f8 reads r6, never used). Still unexplained,
exporter-side bookkeeping.

## T2: Batman skin — descriptors decoded, skin records found (verdict PARTIAL, major upgrade)

### Per-mesh attribute descriptors (engine-verified)
- ENGINE side (new code @0x7ad8b0, loop @0x7ad92c): walks **12-B descriptors**
  with the **attribute id byte at +4**; a 30-entry jump switch maps attr id to
  a configureStream(this, slot, type, fmt, comps):
  - attr 0 Position, 16 Normal, 19-26 Tangent0-3/Binormal0-3 -> fmt 6, 3 comps = **f32x3 (12 B)**
  - attr 1-14 TexCoord0-13 -> fmt 6, 2 comps = **f32x2 (8 B)**
  - attr 17/18 Color0/1 -> fmt 1, 4 comps = **u8x4 (4 B)**
  - attr 29 InstanceId -> u8 (1 B)
  - **attr 27 SkinWeights / 28 SkinIndices -> SKIP: no vertex stream is
    created** — the engine's own case code re-confirms r19: skin data is NOT
    in the vertex.
- FILE side (batman.bdae mesh block): the pre-vertex head @0x4afc..0x4b5c =
  8 x (u32 offset, u32 fmt, u32 comps) as THREE ARRAYS (SoA):
  offsets {0,12,24,36,48,60,72,76}; (fmt,comps) = (6,3)x6, (2,2)x2;
  6x12 + 2x4 = **80 B stride** exactly. fmt 6 = f32, fmt 2 = 2-B fixed point.
  Vertex layout: Pos@0, Normal@12 (|N|=1), Tan0@24, Bin0@36, Tan1@48, Bin1@60,
  two 4-B streams @72/@76.

### The 786/1449 anomaly explained
Pair@24/36 x-product = **-N for 2028, +N for 801, other 67** (left-handed
main frame). Pair@48/60 = **+N 819 / -N 593 / other 37** — the second frame's
handedness FLIPS across the mesh: it is a second UV-set tangent frame whose
sign mirrors with the UV mapping. r19's "786 pass / 663 fail" = the +N
subset under a strict equality test. Both |T| and |B| are unit (median 1.000).

### UVs located and verified (with nulls)
The two 4-B streams = **two UV sets in 4.12 fixed point (u16/4096)**:
- value range [0.000, 15.999] — exactly [0,16) = a 4x4 tile atlas space;
- 15/16 atlas tiles occupied by the mesh;
- adjacent-vertex same-tile fraction **49.6% vs shuffled null 7.0%** (7x).
- REFUTED with numbers: f16 decode (6.3% of values in [0,1] vs shuffled null
  28.3%); plain u16/65535 UV (adjacent-coherence ratio only 0.39-0.51).

### Skin data found: per-vertex records @0x31774
**1449 x 20 B = [u8 bone x4][f32 weight x4]**:
- weight sums == 1.0 for **1449/1449** vertices;
- 30 distinct bone ids (1..30, max 30);
- vertex 0: bones (21, 5, 22, 0), weights (0.846, 0.08, 0.074, 0.0).

### Inverse bind matrices found @0x5a210
**38 x 64 B, row-major affine with w-column [0,0,0,1]** (row-vector
convention), orthonormal rotation rows (norms 1.000/1.000, dot 0.000),
translations e.g. M0 t=(0.3524,-1.1860,-1.0011). A second copy of the same
transforms exists as (quat, translation) pairs right after (0x5a710.., z
sign-flipped: rec t=(1.264,-0.649,+0.622) == mat7 t=(1.264,-0.649,-0.622)).

### Resisting block (named, with evidence)
Bind-pose reproduction (v' = sum_k w_k B_k A_k v == v) is NOT yet achieved:
the 38-matrix array's axis convention and order do not directly match the
1449-vertex mesh's 30-bone palette (translations z ~ -1.0..-1.2 vs vertex z
0..1.87; best axis-map search (x,-y,-z) still gives median local distance
1.37 vs random-bone null 1.55 — no discrimination). The skin record array
(30 bones) and the bind matrix array (38 bones) belong to association steps
that resist: the -mesh-skin section's bone-order table (the ~841-entry u16
list @0x30614, values < 200) is the likely bridge but is undecoded.
Everything else (descriptors, frames, UVs, weights, indices, matrices) is
located and verified — verdict **PARTIAL** (weights/indices located,
bind pose not yet reproduced).
