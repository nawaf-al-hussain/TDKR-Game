# S39 T2 findings — the real .tga block format is NOT PVRTC

## Verdict: PARTIAL (structure cracked; decode not landed)

## The format (new, data-proven)
Each 4x4 block = 8 bytes, LINEAR block order (not Morton):
- bytes 0-2: RGB888 endpoint A - smooth (byte0/2: 41 unique, byte1: 52; means
  37/42.5/36.9 = dark stone grey); consecutive blocks differ by +-1-2.
- byte 3: flags/alpha-ish (44 unique values, mean 8.0; sample 02/07/0b/13/4e).
- bytes 4-7: modulation, 16x2-bit (near-full entropy: 245-250 unique per byte;
  classic checkerboards present, e.g. `77 77 88 88`; plain LSB-first 2-bit
  histogram = [0.612, 0.119, 0.118, 0.152] - flat-texture-like, dominated by 0).

Evidence (independent signals):
1. Byte-value statistics + repetition (e.g. block = `18 18 18 02 3f cc 00 00` -
   three equal channel bytes = RGB888 grey endpoint).
2. Entropy partition (3 smooth + 1 small + 4 high-entropy bytes).
3. 2-bit field histogram of bytes 4-7 matches PVRTC-style modulation usage.
4. Under this read, block-resolution endpoint fields give TV 5.8-7.4 vs
   random-word null 175.9, and Morton block order LOSES to linear (8.7/7.0).

## Why every earlier decode failed
- The file is NOT standard PVRTC (no 555/554/3443/3444 fields - bit15 of the
  color word NEVER set, bit31 = 0.2%; the "fields" are byte-wide RGB).
- The engine PVRTCDecompress @0x746e34 reads a DIFFERENT layout ([4B mod][2B
  555 color][2B 555 color], colors at +4) - running file data through it
  (any flag/word order/Morton variant) yields noise BY CONSTRUCTION.
- The u32swap TV drop (34.2 vs null 64.4) was partial-overlap coincidence.
- Modulation-weight metrics (TV) are INSENSITIVE to mod correctness - s38's
  "modulation table solved" described the ENGINE's weights, not the file's.

## Engine semantics re-measured this session (unicorn probes, opA=1)
- mode bit31: NO effect on the probed single-block cases (both branches give
  plain 555 expand); P (bits 1-15 of color word) = plain 555; Q (bits 16-30)
  = delta-style extraction, exact formula still open.
- Canonical PowerVR reference (Native_SDK PVRTDecompress.cpp) ported to numpy:
  mod word = FIRST u32, color = SECOND; WordModMode = colorData bit 0;
  weights {0,3,5,8}/8 or {0,4,8,14-punch}; bilinear P,Q,R,S with wrap.

## Banked artifacts
- Engine treatment search: s39_t2_treatments.py / s39_t2_refine.py (unicorn).
- Synthetic probes: s39_t2_mode0probe.py, s39_t2_delta.py.
- Canonical port + variants: s39_t2_stdproto.py, s39_t2_full.py.
- Byte-level format analysis: scripts + PNGs (s39_t2_*).

## Next session (named)
1. Disassemble the conversion-path caller @0x800f84 (function start = the push
   at 0x800f84 itself; `sub r0,#0x11` = internal-id dispatch) to find the
   file-layout -> engine-layout pre-transform (endpoint-B derivation + mod
   reordering).
2. Fit the mod->weight mapping from uniform-mod blocks in the real file data
   (blocks with bytes4-7 constant give texel color = f_v(A_rgb, byte3, v)).
3. Then: Python+JS decoders, 10-texture parity vs a re-derived oracle, and the
   textured street patch in the pipeline page.
