#!/usr/bin/env python3
"""s42 T2a: CLEAN-ROOM ETC1 decoder written from the Khronos ETC1 spec only
(OES_texture_ETC1 / ETC2-RGB block semantics), compared against the s41
Python reference on ALL 647 ETC1 chunks (every mip level) via SHA256, plus nulls.

Spec semantics implemented (bit layout as in the spec figure, expressed on the
file's little-endian bytes b0..b7):
  b0 = R5<<3|dR (diff) or R1a<<4|R1b (individual); same for G(b1), B(b2)
  b3 = cw1<<5 | cw2<<2 | diff<<1 | flip
  MSB pixel-index plane: b5 = columns 0,1 (low nibble = column 0), b4 = columns 2,3
  LSB pixel-index plane: b6 = columns 0,1,                    b7 = columns 2,3
  within a nibble, bit j = row j
  subblocks: flip=0 -> vertical split (cols 0-1 = colors1/table1, cols 2-3 = colors2/table2)
             flip=1 -> horizontal split (rows 0-1 / rows 2-3)
  modifier index = msb*2 + lsb; table rows are the STANDARD ETC1 intensity
  modifier tables; pixel = clamp(base8 + modifier, 0, 255)
"""
import hashlib, json, struct, sys, zipfile
import numpy as np
sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session41')
from s41_refdec_lib import read_archive

ARCHS = ['actors_tex.gla', 'commons_tex.gla', 'l_batcave_tex.gla',
         'l_gothamcity_tex.gla', 'l_menu_tex.gla', 'l_military_tex.gla',
         'l_policestation_tex.gla']
MAN = '/tmp/my-project/work/TDKR-Game/extraction/re/session41/s41_t2_chunks.manifest.json'

# STANDARD ETC1 intensity modifier tables (spec table 3.17.2 / OES_texture_ETC1)
MOD = np.array([[2, 8, -2, -8], [5, 17, -5, -17], [9, 29, -9, -29], [13, 42, -13, -42],
                [18, 60, -18, -60], [24, 80, -24, -80], [33, 106, -33, -106],
                [47, 183, -47, -183]], np.int64)

EXP5 = np.array([((v << 3) | (v >> 2)) & 255 for v in range(32)], np.int64)
EXP4 = np.array([((v << 4) | v) & 255 for v in range(16)], np.int64)


def s3(x):
    return x - 8 * (x >= 4)


def decode_etc1_cleanroom(buf, w, h):
    """buf = NB*8 bytes of ETC1 blocks (w,h multiples handled per spec: dims padded to 4)."""
    NB = ((w + 3) // 4) * ((h + 3) // 4)
    B = np.frombuffer(buf, np.uint8, NB * 8).reshape(NB, 8).astype(np.int64)
    b0, b1, b2, b3, b4, b5, b6, b7 = (B[:, i] for i in range(8))
    diff = (b3 >> 1) & 1
    flip = b3 & 1
    t1 = (b3 >> 5) & 7
    t2 = (b3 >> 2) & 7

    # base colors per spec (differential vs individual)
    c1r = np.where(diff == 1, EXP5[b0 >> 3], EXP4[b0 >> 4])
    c1g = np.where(diff == 1, EXP5[b1 >> 3], EXP4[b1 >> 4])
    c1b = np.where(diff == 1, EXP5[b2 >> 3], EXP4[b2 >> 4])
    c2r = np.where(diff == 1, EXP5[np.clip((b0 >> 3) + s3(b0 & 7), 0, 31)], EXP4[b0 & 15])
    c2g = np.where(diff == 1, EXP5[np.clip((b1 >> 3) + s3(b1 & 7), 0, 31)], EXP4[b1 & 15])
    c2b = np.where(diff == 1, EXP5[np.clip((b2 >> 3) + s3(b2 & 7), 0, 31)], EXP4[b2 & 15])

    # pixel index planes (MSB/LSB) per spec layout. NOTE the ETC1 quirk: the
    # two planes store their byte halves in OPPOSITE order —
    #   MSB: b5 = columns 0,1 (low nibble = col 0), b4 = columns 2,3
    #   LSB: b7 = columns 0,1 (low nibble = col 0), b6 = columns 2,3
    msb = np.zeros((NB, 4, 4), np.int64)
    lsb = np.zeros((NB, 4, 4), np.int64)
    for col in range(4):
        mbyte = b5 if col < 2 else b4
        lbyte = b7 if col < 2 else b6
        sh = (col % 2) * 4
        for row in range(4):
            msb[:, row, col] = (mbyte >> (sh + row)) & 1
            lsb[:, row, col] = (lbyte >> (sh + row)) & 1

    idx = msb * 2 + lsb
    cols = np.arange(4)
    sub = (cols >= 2)[None, None, :]  # vertical split default
    sub = np.where(flip[:, None, None] == 1, (np.arange(4) >= 2)[None, :, None], sub)
    tab = np.where(sub, t2[:, None, None], t1[:, None, None])
    cr = np.where(sub, c2r[:, None, None], c1r[:, None, None])
    cg = np.where(sub, c2g[:, None, None], c1g[:, None, None])
    cb = np.where(sub, c2b[:, None, None], c1b[:, None, None])
    mod = MOD[tab, idx]
    out = np.clip(np.stack([cr + mod, cg + mod, cb + mod], -1), 0, 255).astype(np.uint8)
    rgba = np.zeros((NB, 4, 4, 4), np.uint8)
    rgba[:, :, :, :3] = out
    rgba[:, :, :, 3] = 255
    BH, BW = (h + 3) // 4, (w + 3) // 4
    # image assembly: block nb = bh*BW + bx (row-major); pixel rows within the block
    # are the 2nd axis -> transpose to (bh, py, bx, px) before the final reshape
    img = rgba.reshape(BH, BW, 4, 4, 4).transpose(0, 2, 1, 3, 4).reshape(BH * 4, BW * 4, 4)
    return img[:h, :w]


def chain_layout(w, h, avail):
    out = []
    pos = 0
    while True:
        s = ((w + 3) // 4) * ((h + 3) // 4) * 8
        if pos + s > avail:
            break
        out.append((w, h, s))
        pos += s
        if w == 1 and h == 1:
            break
        w = max(1, w // 2)
        h = max(1, h // 2)
    return out, pos


def main():
    man = json.load(open(MAN))
    ref = {c['name']: c for c in man['chunks'] if c['kind'] == 'ETC1'}
    z = zipfile.ZipFile('/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')
    n_chunks = 0
    n_levels = 0
    mism = []
    blocks_total = 0
    for arch in ARCHS:
        d, ents = read_archive(z, arch)
        for (name, off, size) in ents:
            key = f'{arch}:{name}'
            if key not in ref:
                continue
            full = d[off:off + size]
            hs, hgt, wid, mips, flags, dsz, bpp = struct.unpack_from('<7I', full[:52], 0)
            assert bpp == 4 and hs == 52 and (flags & 0xff) == 0x36
            lv, consumed = chain_layout(wid, hgt, dsz)
            if consumed != dsz:
                mism.append({'name': key, 'issue': f'chain {consumed}!={dsz}'})
                continue
            mrec = ref[key]
            p = 52
            for (lw, lh, s) in lv:
                raw = full[p:p + s]
                p += s
                dec = decode_etc1_cleanroom(raw, lw, lh)
                sha = hashlib.sha256(dec.tobytes()).hexdigest()
                blocks_total += s // 8
                n_levels += 1
                want = mrec['levels'][lv.index((lw, lh, s))]['sha'] if False else None
            # compare in order
            p = 52
            for li, (lw, lh, s) in enumerate(lv):
                raw = full[p:p + s]
                p += s
                sha = hashlib.sha256(decode_etc1_cleanroom(raw, lw, lh).tobytes()).hexdigest()
                if sha != mrec['levels'][li]['sha']:
                    mism.append({'name': key, 'level': li, 'w': lw, 'h': lh})
            n_chunks += 1
    print(f"clean-room vs s41 reference: chunks {n_chunks}, levels {n_levels}, "
          f"blocks {blocks_total}, mismatches {len(mism)}")
    if mism:
        print("  first mismatches:", mism[:5])

    # ---- nulls ----
    rng = np.random.RandomState(7)
    # N1: random blocks — clean-room must equal the independent reference decoder
    #     (both implement the same spec; agreement on adversarial input = conformance)
    agree = 0
    trials = 40
    for _ in range(trials):
        w = int(rng.randint(1, 5) * 4)
        h = int(rng.randint(1, 5) * 4)
        nb = (w // 4) * (h // 4)
        buf = rng.randint(0, 256, nb * 8).astype(np.uint8).tobytes()
        a = decode_etc1_cleanroom(buf, w, h)
        from s41_refdec_lib import decode_blocks
        b = decode_blocks(buf, w, h)
        agree += int(np.array_equal(a, b))
    print(f"null N1 random-block conformance (clean-room == s41 ref on garbage): {agree}/{trials}")
    # N2: cross-texture null (shuffled pairing): clean-room(X) vs ref(Y), X!=Y -> ~0
    d, ents = read_archive(z, 'actors_tex.gla')
    tx = {}
    for (name, off, size) in ents:
        hs, hgt, wid, mips, flags, dsz, bpp = struct.unpack_from('<7I', d[off:off + 52], 0)
        if bpp == 4 and hs == 52 and (flags & 0xff) == 0x36 and wid == 32 and name not in tx:
            tx[name] = d[off + 52:off + 52 + 512]
        if len(tx) >= 2:
            break
    ks = sorted(tx)
    if len(ks) >= 2:
        a = decode_etc1_cleanroom(tx[ks[0]], 32, 32)
        from s41_refdec_lib import decode_blocks
        b = decode_blocks(tx[ks[1]], 32, 32)
        print(f"null N2 cross-texture agreement (expect ~0): "
              f"{np.array_equal(a, b)} ({(a == b).mean():.4f})")
    # N3: single-bit sensitivity
    buf = bytearray(tx[ks[0]])
    buf[3] ^= 0x02  # flip the diff bit
    a1 = decode_etc1_cleanroom(bytes(buf), 32, 32)
    a0 = decode_etc1_cleanroom(tx[ks[0]], 32, 32)
    print(f"null N3 single-bit sensitivity (decoders must differ): {not np.array_equal(a0, a1)}")


if __name__ == '__main__':
    main()
