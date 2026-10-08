#!/usr/bin/env python3
"""Restore working asset tree after sandbox reset:
1. pull every l_gothamcity chunk -> raw/l_gothamcity/*.bdae
2. pull game_config chunks (lvc) -> raw/game_config/
3. decode every l_gothamcity_tex + commons_tex texture -> textures_png/<archive>/<name>.png
"""
import os, struct, sys
import texture2ddecoder
from PIL import Image

RAW = "/home/z/my-project/download/TDKR_assets/raw"
PNG = "/home/z/my-project/download/TDKR_assets/textures_png"

def gla_entries(path):
    d = open(path, 'rb').read(16)
    _, idx_size, table_bytes, n = struct.unpack('>IIII', d)
    tbl = open(path, 'rb').read(16 + n * 16)[16:]
    pool_start = 16 + n * 16
    pool_end = idx_size
    pool = open(path, 'rb').read(pool_end)[pool_start:]
    out = []
    for i in range(n):
        off, sz, no, _ = struct.unpack('>IIII', tbl[i*16:(i+1)*16])
        name = pool[no:pool.index(b'\0', no)].decode('ascii', 'replace')
        out.append((name, off, sz))
    return out

def pull_chunks(gla_path, out_dir, subdir=''):
    os.makedirs(out_dir, exist_ok=True)
    data = open(gla_path, 'rb').read()
    ents = gla_entries(gla_path)
    n = 0
    for name, off, sz in ents:
        base = name.split('/')[-1]
        p = os.path.join(out_dir, base)
        with open(p, 'wb') as f:
            f.write(data[off:off+sz])
        n += 1
    return n

def decode_pvr(buf):
    hs, h, w, mips, flags, dsz, bpp, mr, mg, mb, ma, magic, nsurf = struct.unpack('<13I', buf[:52])
    if hs == 44:
        hs, h, w, mips, flags, dsz, bpp, mr, mg, mb, ma = struct.unpack('<11I', buf[:44])
    payload = buf[hs:]
    if bpp == 4:  # ETC1
        base = ((w+3)//4) * ((h+3)//4) * 8
        px = texture2ddecoder.decode_etc1(payload[:base], w, h)
        if isinstance(px, int):
            px = px.to_bytes(w*h*4, 'little')
        return Image.frombytes('RGBA', (w, h), bytes(px)[:w*h*4], 'raw', 'BGRA'), flags
    if bpp == 16:  # RGB565
        a = np.frombuffer(payload[:w*h*2], '<u2').reshape(h, w)
        r = ((a >> 11) & 31) * 255 // 31
        g = ((a >> 5) & 63) * 255 // 63
        b = (a & 31) * 255 // 31
        alpha = 255 if not (flags & 2) else ((a >> 15) * 255)
        img = np.dstack([r, g, b, np.full((h, w), 255, np.uint8)]).astype(np.uint8)
        return Image.fromarray(img, 'RGBA'), flags
    if bpp == 24:  # RGB888 BGR order
        a = np.frombuffer(payload[:w*h*3], np.uint8).reshape(h, w, 3)
        img = np.dstack([a[:, :, 2], a[:, :, 1], a[:, :, 0], np.full((h, w), 255, np.uint8)])
        return Image.fromarray(img.astype(np.uint8), 'RGBA'), flags
    if bpp == 32:  # RGBA8888
        a = np.frombuffer(payload[:w*h*4], np.uint8).reshape(h, w, 4)
        img = np.dstack([a[:, :, 2], a[:, :, 1], a[:, :, 0], a[:, :, 3]])
        return Image.fromarray(img.astype(np.uint8), 'RGBA'), flags
    return None, flags

import numpy as np

def decode_all(tex_gla, out_arch):
    os.makedirs(os.path.join(PNG, out_arch), exist_ok=True)
    data = open(tex_gla, 'rb').read()
    ents = gla_entries(tex_gla)
    ok = fail = zipc = 0
    for name, off, sz in ents:
        base = name.split('/')[-1]
        buf = data[off:off+sz]
        outp = os.path.join(PNG, out_arch, base + '.png')
        if buf[:4] == b'PK\x03\x04':
            zipc += 1
            continue
        try:
            img, flags = decode_pvr(buf)
            if img is None:
                fail += 1
                continue
            img.save(outp)
            ok += 1
        except Exception as e:
            fail += 1
    print(f'{out_arch}: {ok} decoded, {fail} failed, {zipc} zip-split')

if __name__ == '__main__':
    F = os.path.join(RAW, 'com.gameloft.android.AMAZ.GloftKRAS', 'files')
    n = pull_chunks(os.path.join(F, 'data', 'l_gothamcity.gla'), os.path.join(RAW, 'l_gothamcity'))
    print('l_gothamcity chunks:', n)
    os.makedirs(os.path.join(RAW, 'game_config'), exist_ok=True)
    n = pull_chunks(os.path.join(F, 'data', 'game_config.gla'), os.path.join(RAW, 'game_config'))
    print('game_config chunks:', n)
    decode_all(os.path.join(F, 'textures', 'l_gothamcity_tex.gla'), 'l_gothamcity_tex')
    decode_all(os.path.join(F, 'textures', 'commons_tex.gla'), 'commons_tex')
