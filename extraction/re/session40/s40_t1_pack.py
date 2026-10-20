#!/usr/bin/env python3
"""S40 T1c: pack all ETC1 mip0 payloads + SHA256 manifest of reference RGBA
for the node parity test."""
import struct, zipfile, json, hashlib
import numpy as np
import texture2ddecoder as t2d

Z = zipfile.ZipFile('/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')
ARCHS = ['actors_tex.gla', 'commons_tex.gla', 'l_batcave_tex.gla',
         'l_gothamcity_tex.gla', 'l_menu_tex.gla', 'l_military_tex.gla',
         'l_policestation_tex.gla']
OUT_BIN = '/home/z/my-project/scripts/s40_t1_mip0.pack'
OUT_MAN = '/home/z/my-project/scripts/s40_t1_manifest.json'

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

man = []
blob = bytearray()
blob += struct.pack('<I', 0)  # count placeholder
count = 0
for arch in ARCHS:
    d, ents = read_archive(Z, arch)
    for (name, off, size) in ents:
        hdr = d[off:off+52]
        if len(hdr) < 52: continue
        hs, hgt, wid, mips, flags, dsz, bpp = struct.unpack_from('<7I', hdr, 0)
        if bpp != 4 or hs != 52: continue
        base = ((wid+3)//4) * ((hgt+3)//4) * 8
        px = bytes(d[off+52: off+52+base])
        ref = np.frombuffer(t2d.decode_etc1(px, wid, hgt), np.uint8).reshape(hgt, wid, 4)
        ref_rgba = ref[:, :, [2, 1, 0, 3]]  # -> RGBA
        sha = hashlib.sha256(ref_rgba.tobytes()).hexdigest()
        man.append({'name': f'{arch}:{name}', 'w': wid, 'h': hgt, 'sha': sha,
                    'off': len(blob)})
        nb = name.encode('latin1')
        blob += struct.pack('<H', len(nb)) + nb
        blob += struct.pack('<IIII', wid, hgt, base, 0)
        blob += px
        count += 1
struct.pack_into('<I', blob, 0, count)
open(OUT_BIN, 'wb').write(bytes(blob))
json.dump(man, open(OUT_MAN, 'w'))
print(f'packed {count} textures, {len(blob)/1e6:.1f} MB -> {OUT_BIN}')
