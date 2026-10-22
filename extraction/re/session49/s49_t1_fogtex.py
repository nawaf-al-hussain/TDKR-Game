#!/usr/bin/env python3
"""s49 T1d: decode GC_VerticalFOG.tga + 000_default.tga (LUT) + fog_street_level.tga."""
import struct
import numpy as np

def gla_member(path, want):
    d = open(path, 'rb').read()
    _, idxsz, tabsz, n = struct.unpack('>IIII', d[:16])
    pool = d[16 + n*16: idxsz]
    for i in range(n):
        o, s, no, _ = struct.unpack('>IIII', d[16+i*16: 16+i*16+16])
        e = pool.index(b'\0', no)
        if pool[no:e].decode('ascii','replace').lower() == want.lower():
            return d[o:o+s]
    raise SystemExit('missing ' + want)

def decode_tdkr_tex(u8):
    """TDKR tex container: [tag 0x34][h][w]... PVR! at 44; ETC1 payload at 52."""
    tag, h, w = struct.unpack_from('<III', u8, 0)
    is_pvr = bytes(u8[44:48]) == b'PVR!'
    print(f'  tag {tag:#x} {w}x{h} pvr={is_pvr} len={len(u8)}')
    if not is_pvr:
        return None
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        'cr', '/tmp/my-project/work/TDKR-Game/extraction/re/session42/s42_t2_cleanroom.py')
    cr = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cr)
    bw, bh = (w+3)//4, (h+3)//4
    need = bw*bh*8
    rgba = cr.decode_etc1_cleanroom(np.frombuffer(u8, np.uint8, need, 52), w, h)
    return rgba

CT = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/textures/commons_tex.gla'
GT = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/textures/l_gothamcity_tex.gla'
for path, name in ((GT, 'GC_VerticalFOG.tga'), (CT, '000_default.tga'),
                   (CT, 'fog_street_level.tga'), (GT, 'GC_VerticalFOG_Island2.tga')):
    u8 = gla_member(path, name)
    print(name, len(u8), 'bytes, head:', u8[:48].hex())
    r = decode_tdkr_tex(u8)
    if r is not None:
        print('   decoded', r.shape, 'mean', r[:, :, :3].mean(axis=(0,1)),
              'alpha mean', r[:, :, 3].mean())
        np.save(f'/tmp/my-project/work/TDKR-Game/extraction/re/session49/s49_tex_{name.replace(".tga","").lower()}.npy', r)
        # corner samples
        print('   center px', r[r.shape[0]//2, r.shape[1]//2], 'corner', r[0,0], r[-1,-1])
