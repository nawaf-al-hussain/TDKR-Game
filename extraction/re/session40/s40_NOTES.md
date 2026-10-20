# Session 40 (round 30) notes

## State on entry
Remote: main bd7c709, gh-pages a1bf3b1 (v21.1 LIVE), gh-pages-staged 39298a4,
essentials-s36 7c8defc — all as expected. Local repo survived; one untracked
s39c file committed. Credentials: leftover git credential-store file
(/home/z/.git-credentials, mode 600, 75 bytes) DELETED at session start and
`credential.helper = store` removed from ~/.gitconfig. No token this session
-> no push; local commits + verified bundles.

## T1 (bf71bae gh-pages, main mirror) — PASS: ETC1 PROVEN, JS DECODER, STREET PATCH
1. Header format-code histogram over ALL 910 texture chunks in the 7 tex
   archives: 862 valid PVR-v2-LE headers + 48 ZIP-split stream continuations
   (PK zip signature, "SPLIT" member). Codes (flags & 0xff): 0x36 x647 (ETC1),
   0x13 x205 (RGB565), 0x15 x8 (RGB888), 0x12 x2 (RGBA8888). NO other code.
2. Engine mapping (disassembly): CImageLoaderPVR::loadTextureHeader reads the
   52 B LE header, magic 'PVR!', then dispatches on flags&0xff through a
   97-entry jump table -> E_PIXEL_FORMAT in STextureDesc+4. Code 0x36 -> enum
   29; pixel_format::decompress @0x800f84 special-cases fmt 29 = ETC1 (before
   the PFDTable size checks) -> decompressETC1 (statics: modifierTable
   @0xb88710, tableCWShift [5,2,2,8], tableCWMask [7,2], differentialMode
   [0x2,0x2], modeBit [0x2,0x1], flipBit [0x1,0x1,0x0,0x1000000] — all
   consistent with the file layout: t1 bits 7-5, t2 bits 4-2, diff bit 1,
   flip bit 0 of byte3).
   PVRTC ROUTE RETIRED WITH NUMBERS: PVRTCDecompress @0x744148 has exactly TWO
   call sites, both inside pixel_format::decompress, reachable only for
   fmt in {21,22}; the loader produces enum 22 only from header codes 0x0c/0x18
   and enum 21 from none — ZERO occurrences in the OBB. So the engine's
   PVRTC decoder is dead code for every texture in the game. Positive control
   answered in the negative by exhaustive xref (ARM BL any-cond + Thumb BL/BLX
   + literal pools; scanner validated against the two known call sites).
3. Decode: Python reference decoder (calibrated against texture2ddecoder with
   synthetic probes, which is pixel-exact vs the pool PNGs on 17 spot checks
   incl. 2048^2 street atlases) decodes 647/647 ETC1 textures BIT-EXACT.
   Nulls (Gargoyle / BakeGroup_Island1_A0 / Roads0): real 0.00% mismatch vs
   col-major block order 87.3/96.7/94.2%, shuffled blocks 93.7/97.9/97.6%,
   s39-style word-swap 99.98/99.82/99.78% (mean |err| 50-76 vs 0).
   BYTE LAYOUT: b0-2 = RGB (diff: base5=b>>3, delta3=b&7 SIGNED color2-only;
   individual: 4444), b3 = [t1:3][t2:3][diff:1][flip:1], b4-7 = 16 2-bit
   modifiers as TWO BIT-PLANES: planeH = LE u16 of b4,b5 (texel col order
   [2,3,0,1]), planeL = u16 with b7 as LOW byte (col order [0,1,2,3]);
   mod = L + 2*H; out = clamp(expand(c) + MOD[t][m], 0, 255) with expand5 =
   (v<<3)|(v>>2), expand4 = (v<<4)|v; flip=0: x<2 uses color1/t1, flip=1: y<2.
   MODIFIER TABLES = the ENGINE's 8 tables (32 entries @0xb88710); tables 5-7
   DIFFER from the ETC2-spec punchthrough numbers: {24,80},{33,106},{47,183}
   (not 74/109/159) — using spec numbers breaks 521/647 textures.
4. JS decoder playable/etc1_tdkr.js: node parity 647/647 SHA256-exact (5.8 s).
5. pipeline.html: street patch BakeGroup_Island1_Roads0.tga (2048^2, chunk
   @11,198,218 in l_gothamcity_tex.gla) stream-inflated from the USER's zip and
   decoded in-browser (63 ms), SHA256 in-page == Python reference
   (52fcbf32...), textured ground patch + 2D preview, 0 console errors,
   READY ~1.5 s.
6. s39 FINDINGS RECLASSIFIED (PVRTC route retired):
   - "555 packing / colA bit15 flags" (s39 part 8): ARTIFACT — those fields
     belong to the engine's PVRTC word layout, not the file; the file has no
     555 fields at all (bytes 0-2 are per-channel base|delta).
   - "transposed Morton addressing" (s39 part 8): ARTIFACT of block-order
     confusion; blocks are LINEAR row-major (null: col-major 87-97% wrong).
   - "8x4 texel cells / anisotropic corners": ARTIFACT — ETC1 is 4x4; the
     apparent anisotropy came from decoding ETC mod data as PVRTC bilinear
     weights.
   - "byte3 bit1 always set, values {2,3,6,7,22,23,26,27,43,0b}" (s39): STILL
     VALID and now EXPLAINED — bit1 = diff flag (1 = diff mode), bits 7-5/4-2
     = modifier table indices (3-bit, 8 tables).
   - "bytes 4-7 = 16x2-bit modulation, hist [0.61,0.12,0.12,0.15]" (s39): STILL
     VALID (it IS the modulation), but the s39 bit->texel map was not.
   - "engine PVRTCDecompress expects [4B mod][2B][2B]" (s39 part 2): STILL
     VALID as a statement about the engine, now MOOT (never called for files).
   - "u32swap TV 34.2 vs null 64.4" (s39): ARTIFACT (partial-overlap
     coincidence; word-swap decode = 99.8% wrong).
   - Mod-weight fit / midpoint probing from s39: MOOT (weights are the standard
     per-table modifiers; no uniform-mod fit needed).
7. LIVE PAGE HAD A REAL BUG (found by the gate): s39 T7 (a1bf3b1) introduced
   `const names` redeclaration (module SyntaxError) + Object.keys() on a Map
   (always [] -> every input guard broken). The live pipeline page could not
   load ANY file since v21.1 shipped. Fixed (single [...dir.keys()]).
8. Batman RGB888 path: memory order is B,G,R — verified pixel-exact vs the
   pool on all 8 bpp=24 textures; the live page swapped R/B (invisible on the
   grey suit). Fixed; also height(+4)/width(+8) field order fixed.

Artifacts: extraction/re/session40/s40_t1*.{py,js,json} + this file.
