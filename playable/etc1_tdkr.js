/* ETC1_TDKR — bit-exact ETC1 decoder for TDKR .tga (PVR2-header) payloads.
 * Session 40 calibration (see extraction/re/session40 notes):
 *   per 8-byte block (4x4 texels, row-major blocks):
 *     b0,b1,b2 = R,G,B: diff mode  -> base5 = b>>3, delta3 = b&7 (SIGNED, color2 only)
 *                    individual   -> col1 = b>>4, col2 = b&15 (4-bit)
 *     b3       = [t1:3](bits7-5) [t2:3](4-2) [diff:1](1) [flip:1](0)
 *     b4,b5    = planeH u16 LE (b4 | b5<<8): bit index -> texel x order [2,3,0,1], y = bit%4
 *     b6,b7    = planeL u16 with byte7 as LOW byte (b7 | b6<<8): x order [0,1,2,3]
 *     mod(x,y) = L(x,y) | H(x,y)<<1
 *     flip=0: x<2 -> color1/table1 ; flip=1: y<2 -> color1/table1
 *     out    = clamp(expand(c) + MOD[t][m], 0, 255)   (modifier applied in 8-bit space)
 *     expand: 5-bit (v<<3)|(v>>2); 4-bit (v<<4)|v ; alpha = 255
 *   Modifier tables = the ENGINE's (libKRHP.so glitch::decompressETC1 statics @0xb88710);
 *   tables 5-7 differ from the ETC2-spec punchthrough numbers: {24,80},{33,106},{47,183}.
 *   Validated: 647/647 ETC1 textures in the OBB decode pixel-exact vs texture2ddecoder
 *   (which matches the reference pool PNGs byte-for-byte).
 */
(function (root) {
  const MOD = new Int16Array([
    2, 8, -2, -8,  5, 17, -5, -17,  9, 29, -9, -29,  13, 42, -13, -42,
    18, 60, -18, -60,  24, 80, -24, -80,  33, 106, -33, -106,  47, 183, -47, -183
  ]);
  const EXP5 = new Uint8Array(32);
  for (let v = 0; v < 32; v++) EXP5[v] = ((v << 3) | (v >> 2)) & 255;
  const EXP4 = new Uint8Array(16);
  for (let v = 0; v < 16; v++) EXP4[v] = ((v << 4) | v) & 255;

  function decodeRGBA(u8, w, h) {
    const BW = (w + 3) >> 2, BH = (h + 3) >> 2;
    const out = new Uint8Array(w * h * 4);
    for (let by = 0; by < BH; by++) {
      for (let bx = 0; bx < BW; bx++) {
        const o = (by * BW + bx) * 8;
        const b0 = u8[o], b1 = u8[o + 1], b2 = u8[o + 2], b3 = u8[o + 3];
        const b4 = u8[o + 4], b5 = u8[o + 5], b6 = u8[o + 6], b7 = u8[o + 7];
        const diff = (b3 >> 1) & 1, flip = b3 & 1;
        const t1 = (b3 >> 5) & 7, t2 = (b3 >> 2) & 7;
        const planeH = b4 | (b5 << 8);
        const planeL = b7 | (b6 << 8);
        let c1r, c1g, c1b, c2r, c2g, c2b;
        if (diff) {
          const rb = b0 >> 3, db = b0 & 7, gb = b1 >> 3, dg = b1 & 7, bb = b2 >> 3, dbb = b2 & 7;
          c1r = EXP5[rb]; c1g = EXP5[gb]; c1b = EXP5[bb];
          const sd = v => (v & 4) ? (v - 8) : v;
          c2r = EXP5[Math.min(31, Math.max(0, rb + sd(db)))];
          c2g = EXP5[Math.min(31, Math.max(0, gb + sd(dg)))];
          c2b = EXP5[Math.min(31, Math.max(0, bb + sd(dbb)))];
        } else {
          c1r = EXP4[b0 >> 4]; c1g = EXP4[b1 >> 4]; c1b = EXP4[b2 >> 4];
          c2r = EXP4[b0 & 15]; c2g = EXP4[b1 & 15]; c2b = EXP4[b2 & 15];
        }
        for (let y = 0; y < 4; y++) {
          const py = by * 4 + y;
          if (py >= h) break;
          for (let x = 0; x < 4; x++) {
            const px = bx * 4 + x;
            if (px >= w) continue;
            const sel1 = flip ? (y < 2) : (x < 2);
            const t = sel1 ? t1 : t2;
            const hb = x < 2 ? (8 + x * 4 + y) : ((x - 2) * 4 + y);
            const lb = x < 2 ? (x * 4 + y) : (8 + (x - 2) * 4 + y);
            const m = ((planeL >> lb) & 1) | (((planeH >> hb) & 1) << 1);
            const mv = MOD[t * 4 + m];
            const q = (py * w + px) * 4;
            const cr = sel1 ? c1r : c2r, cg = sel1 ? c1g : c2g, cb = sel1 ? c1b : c2b;
            let r = cr + mv; r = r < 0 ? 0 : (r > 255 ? 255 : r);
            let g = cg + mv; g = g < 0 ? 0 : (g > 255 ? 255 : g);
            let b = cb + mv; b = b < 0 ? 0 : (b > 255 ? 255 : b);
            out[q] = r; out[q + 1] = g; out[q + 2] = b; out[q + 3] = 255;
          }
        }
      }
    }
    return out;
  }

  const api = { decodeRGBA, MOD, EXP5, EXP4 };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  root.ETC1_TDKR = api;
})(typeof window !== 'undefined' ? window : globalThis);
