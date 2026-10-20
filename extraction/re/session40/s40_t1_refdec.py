#!/usr/bin/env python3
"""S40 T1b: bit-exact Python ETC1 decoder for the TDKR .tga layout,
calibrated empirically against texture2ddecoder (which matches the pool PNGs
pixel-exactly). Verify on ALL ETC1 (bpp=4) textures in all tex archives.

Layout (per 8-byte block, 4x4 texels, row-major blocks):
  b0,b1,b2 = R,G,B packing: diff mode -> base5=b>>3, delta3=b&7 (signed, color2 only)
                              individual mode -> col1=b>>4, col2=b&15 (4-bit)
  b3       = [t1:3](7-5) [t2:3](4-2) [diff:1](1) [flip:1](0)
  b4,b5    = planeH u16 (b4 | b5<<8): bit (x*4+y) in col order [2,3,0,1]
  b6,b7    = planeL u16 (b6 | b7<<8): bit (x*4+y) in col order [0,1,2,3]
  mod(x,y) = L(x,y) | H(x,y)<<1
  color: flip=0 -> x<2 uses color1/table1; else color2/table2
         flip=1 -> y<2 uses color1/table1; else color2/table2
  out     = clamp(expand(c) + MOD[t][mod], 0, 255); alpha=255
  expand: diff 5-bit -> (v<<3)|(v>>2); individual 4-bit -> (v<<4)|v
  MOD = [[2,8,-2,-8],[5,17,-5,-17],[9,29,-9,-29],[13,42,-13,-42]]
"""
import struct, zipfile, json, sys
import numpy as np
import texture2ddecoder as t2d

MOD = np.array([[2, 8, -2, -8], [5, 17, -5, -17], [9, 29, -9, -29], [13, 42, -13, -42],
                [18, 60, -18, -60], [24, 80, -24, -80], [33, 106, -33, -106],
                [47, 183, -47, -183]], np.int64)  # ENGINE tables = the STANDARD ETC1 intensity modifier table [corrected s41]

def expand5(v): return ((v << 3) | (v >> 2)) & 255
def expand4(v): return ((v << 4) | v) & 255
EXP5 = np.array([expand5(v) for v in range(32)], np.int64)
EXP4 = np.array([expand4(v) if v < 16 else 0 for v in range(32)], np.int64)

def decode_blocks(buf, w, h):
    """Returns HxWx4 uint8 RGBA."""
    BW, BH = (w + 3) // 4, (h + 3) // 4
    blocks = np.frombuffer(buf, np.uint8).reshape(BH * BW, 8).astype(np.int64)
    b0, b1, b2, b3 = blocks[:, 0], blocks[:, 1], blocks[:, 2], blocks[:, 3]
    mH0, mH1, mL0, mL1 = blocks[:, 4], blocks[:, 5], blocks[:, 6], blocks[:, 7]
    diff = (b3 >> 1) & 1
    flip = b3 & 1
    t1 = (b3 >> 5) & 7   # full 3-bit modifier table index (8 tables)
    t2 = (b3 >> 2) & 7

    base = np.stack([b0 >> 3, b1 >> 3, b2 >> 3], 1)                    # NB x 3
    delta = np.stack([b0 & 7, b1 & 7, b2 & 7], 1)
    sdelta = np.where(delta >= 4, delta - 8, delta)
    c1d = base
    c2d = np.clip(base + sdelta, 0, 31)
    c1i = np.stack([b0 >> 4, b1 >> 4, b2 >> 4], 1)
    c2i = np.stack([b0 & 15, b1 & 15, b2 & 15], 1)
    c1 = np.where(diff[:, None] == 1, c1d, c1i)
    c2 = np.where(diff[:, None] == 1, c2d, c2i)

    NB = BH * BW
    # mod planes: value 0..3 per (texel y,x) per block
    # planeH bit index: x=2 -> y (bits0-3), x=3 -> 4+y, x=0 -> 8+y, x=1 -> 12+y
    # planeL bit index: x=0 -> y, x=1 -> 4+y, x=2 -> 8+y, x=3 -> 12+y
    pH = (mH0 | (mH1 << 8))  # NB: planeH u16, byte4 = low byte
    pL = (mL1 | (mL0 << 8))  # NB: planeL u16, byte7 = low byte (calibrated)
    mods = np.zeros((NB, 4, 4), np.int64)
    H = np.zeros((NB, 4, 4), np.int64)
    L = np.zeros((NB, 4, 4), np.int64)
    Hcol = [2, 3, 0, 1]
    for x in range(4):
        hb = Hcol[x] * 4
        lb = x * 4
        for y in range(4):
            H[:, y, x] = (pH >> (hb + y)) & 1
            L[:, y, x] = (pL >> (lb + y)) & 1
    mods = L + (H << 1)

    out = np.zeros((NB, 4, 4, 4), np.int64)  # NB, y, x, RGBA
    for y in range(4):
        for x in range(4):
            use1 = (flip == 0) & (x < 2) if False else None
            if False: pass
            sel1 = ((flip == 0) & (x < 2)) | ((flip == 1) & (y < 2))
            c = np.where(sel1[:, None], c1, c2)
            t = np.where(sel1, t1, t2)
            exp = np.where(diff[:, None] == 1,
                           EXP5[c], EXP4[c])
            m = mods[:, y, x]
            tab = MOD[t, m]  # NB
            v = np.clip(exp + tab[:, None] if tab.ndim > 1 else exp + tab[:, None], 0, 255)
            out[:, y, x, 0] = v[:, 0]
            out[:, y, x, 1] = v[:, 1]
            out[:, y, x, 2] = v[:, 2]
            out[:, y, x, 3] = 255
    img = out.reshape(BH, BW, 4, 4, 4).transpose(0, 2, 1, 3, 4).reshape(BH * 4, BW * 4, 4)
    return img[:h, :w].astype(np.uint8)

def read_archive(z, arch):
    d = z.read('com.gameloft.android.AMAZ.GloftKRAS/files/textures/' + arch)
    n = struct.unpack_from('>I', d, 12)[0]
    pool = 16 + n * 16
    ents = []
    for i in range(n):
        off, size, nameOff = struct.unpack_from('>3I', d, 16 + i * 16)
        nb = pool + nameOff
        e = d.index(b'\0', nb)
        ents.append((d[nb:e].decode('latin1'), off, size))
    return d, ents

def main():
    z = zipfile.ZipFile('/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')
    archs = ['actors_tex.gla', 'commons_tex.gla', 'l_batcave_tex.gla',
             'l_gothamcity_tex.gla', 'l_menu_tex.gla', 'l_military_tex.gla',
             'l_policestation_tex.gla']
    tot = ok = fail = 0
    worst = []
    fails = []
    for arch in archs:
        d, ents = read_archive(z, arch)
        for (name, off, size) in ents:
            hdr = d[off:off+52]
            if len(hdr) < 52: continue
            hs, hgt, wid, mips, flags, dsz, bpp = struct.unpack_from('<7I', hdr, 0)
            if bpp != 4 or hs != 52: continue
            tot += 1
            base = ((wid+3)//4) * ((hgt+3)//4) * 8
            px = bytes(d[off+52: off+52+base])
            mine = decode_blocks(px, wid, hgt)  # RGBA
            ref = np.frombuffer(t2d.decode_etc1(px, wid, hgt), np.uint8).reshape(hgt, wid, 4)
            ref_rgba = ref[:, :, [2, 1, 0, 3]]  # BGRA -> RGBA
            mism = int(np.any(mine != ref_rgba, axis=2).sum())
            if mism == 0:
                ok += 1
            else:
                fail += 1
                fails.append((arch, name, mism))
                if len(worst) < 5: worst.append((arch, name, wid, hgt, mism))
    print(f'ETC1 textures checked: {tot}, exact: {ok}, mismatches: {fail}')
    for f in fails[:10]: print('  FAIL', f)
    json.dump({'total': tot, 'exact': ok, 'failed': fail, 'fails': fails[:20]},
              open('/home/z/my-project/scripts/s40_t1_refdec_result.json', 'w'), indent=1)

if __name__ == '__main__':
    main()
