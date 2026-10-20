# S39c T2 findings — the .tga format CRACKED (structure + transform + engine geometry)

## Verdict: structure+transform PROVEN; exact decode parity pending corner-mod micro-geometry

## 1. Container (new)
Each .tga entry = PVR-style container: +0 u32 0x34 (header size 52), +4 w, +8 h,
+12 bytes-per-block (8), +16 u32 (0x136, role TBD), +20 data size, +24 mip count,
+32 zero-pad, +44 "PVR!" magic, +48 version 1, +52 = block data (mips sequential:
256^2=32768 B, 128^2=8192 B, ...). Data starts at +52 (endpoint smoothness proof;
the +16=0x136 field is NOT the data offset — s38/s39 probes at +52 were correct).

## 2. File block (8 B) = [3B RGB888 endpoint A][1B X][4B mod]
- bytes 0-2 = endpoint A in RGB888 (proven: mip-chain LUT-inverse consistency RMSE 0.37!)
- byte 3 = 44 unique values, bit1 of low nibble ALWAYS set: {02,03,06,07,0b,13,22,23,26,27,43...}
  = colB-related field (exact semantics still open: delta-pack OR colB-lo under a 4443 colB)
- bytes 4-7 = the 32-bit modulation word (verbatim into engine mod slot)

## 3. Engine block layout (proven by probes + disasm 0x746e34)
[u32 mod][u32 colors] where colors = [colA u16le][colB u16le].
FOUR color-format paths selected by per-endpoint bit15:
- colA bit15=0 (0x7472f8): [B3:1-3][G4:4-7][R4:8-11][A3:12-14->alpha=34v], expansions LUT-measured
- colA bit15=1 (0x747da8): OPAQUE 555: R5=[10-14], G5=[5-9], B4=[1-4] (expand x|x>>4), alpha=15
- colB bit15=0: [B4:0-3 linear 247/15][G4:4-7 GA-curve][R4:8-11 GA][A3:12-14]
- colB bit15=1 (0x747bb0): OPAQUE 555: R5=[10-14], G5=[5-9], B5=[0-4], alpha=15 (ABSOLUTE, not delta)
colA bit0 (read fresh per corner!) = modulation mode: 1 = 16 sequential 2-bit fields
(ubfx #0,#2,...,#30), 0 = checkerboard patterns (v1/v2 = two phases, v0/v3 = all-A/all-B).

## 4. THE FILE'S PATH = colA bit15=1 (555!)
colA = 0x8000 | (modmode<<0) | ((b>>4)<<1) | ((g>>3)<<5) | ((r>>3)<<10).
MIP-ORACLE PROOF: with this pack, ds2(decode(mip0)) vs decode(mip1) RMSE dropped
26.4 -> 5.47-5.58 (pure-endpoint data floor 0.37; the residual = cross-mip mod-detail
penalty, which is UNCORRELATED between mips by construction). The 4443-style pack
(r>>4,g>>4,b>>5) used by all s38/s39 candidates was WRONG (field bleeding under the
555 reading) — explains every prior "noise" result.

## 5. Block addressing = TRANSPOSED Morton (proven by single-block influence maps)
Engine index bit 2i = ROW (by) bit i; bit 2i+1 = COLUMN (bx) bit i+1... i.e. y-first
interleave (my earlier me() = x-first was transposed). Influence maps: L=1->row band 1,
L=2->col, L=4->row 2, L=8->col 4, L=16->row 4, L=32->col 8, L=64->row 8; L>=128 (col
bit 4 = 16 >= 16 cols) = NO influence, exactly as the interleave predicts.
NOTE: for square textures (64x64 blocks) transpose is invisible to the mip oracle —
only the influence-map method exposed it.

## 6. Geometry = 8x4 texels per block, anisotropic corner grid (opA=1 = 2bpp!)
- r6=8 at impl entry (opA!=0) = BLOCK WIDTH IN TEXELS (opA=0 -> 4 = 4bpp 4x4).
- Corner colors: X period 8 px (corners at px 4+8k, values = blend of adjacent block
  endpoints), Y period 4 px. Bilinear-tent proof (probe D) + influence bands agree.
- 16 mod fields cover the 8x4 cell (2x2-texel pairs); weights (bit0=1 path):
  out = (A*(8-w) + B*w) >> 3, w in {0,3,5,8} for field values {0,1,2,3} (integer,
  floor semantics verified: 140*5>>3=87, 140*3>>3=52).
- Checkerboard mode (bit0=0): v1/v2 = two antiphase per-texel A/B checkerboards,
  v0/v3 = uniform A/B (probes 4F/4G/5#3).

## 7. Oracle methodology notes (for the record)
- mip self-consistency ds2-RMSE: SYNTHETIC consistent-mips floor = 40 (bilinear scale
  effect dominates!) — the oracle validates the A-side only and inherently penalizes
  mod detail (mips re-derive mods). Pure-endpoint floor (no engine): 0.37.
- Single-block influence maps (red-block probing) = the decisive geometry tool.

## 8. Remaining (named next, well-scoped)
1. byte3 exact semantics: delta-pack vs colB-lo. Discriminator: uniform-mod blocks
   (mod all-0 / all-3) in real data -> decoded color = f(A, byte3, v); invert LUTs.
2. Mod field -> (2x2-texel pair) assignment inside the 8x4 cell (16 single-field
   influence probes with colB != colA).
3. Then Python+JS decoders reach BIT-EXACT engine parity; street patch on pipeline page.
4. s38's "engine-through-file = noise" verdict stands CORRECTED: the noise was the
   4443-mispack + x/y-transposed morton, not the engine layout itself.

## Banked artifacts (this session)
s39b_t2_rot.py/.json (rotation test), s39b_t2_probe2(v2).py, s39b_t2_probe3.py
(LUTs, field order, bilinear), s39b_t2_probe4/5/6.py (mode bit, checkerboard, LUTs),
s39b_t2_geom*.py (PVR container), s39b_t2_Tscan/miporacle/ordertest/colbscan2.py
(candidate scans), s39b_t2_floor.py (pure-data floor 0.37), s39b_t2_calib.py
(synthetic floor 40), s39b_t2_linmap/probe7/8/9.py (influence maps -> transposed
morton + 8x4 geometry), s39b_t2_555scan.py (THE 555 proof: 26.4 -> 5.47),
s39b_t2_colbprobe.py (colB absolute), scripts in /home/z/my-project/scripts/.
