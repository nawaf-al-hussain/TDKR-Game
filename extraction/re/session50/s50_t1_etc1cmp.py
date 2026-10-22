#!/usr/bin/env python3
"""s50 T1: compare the JS ETC1 decoder (etc1_tdkr.js, via node) against the Python
cleanroom decoder on the actual LightMapDC textures. If they differ, the JS-vs-Python
corr gap is decoder disagreement, not rendering."""
import struct, subprocess, json, io, zipfile
import numpy as np
from PIL import Image
import importlib.util

spec = importlib.util.spec_from_file_location(
    'cr', '/tmp/my-project/work/TDKR-Game/extraction/re/session42/s42_t2_cleanroom.py')
cr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cr)

TEXGLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/textures/l_gothamcity_tex.gla'
NODE_DEC = r"""
const fs = require('fs');
const ETC1 = require(process.argv[2]);
const tex = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const buf = Buffer.from(tex.blocks, 'base64');
const rgba = ETC1.decodeRGBA(new Uint8Array(buf), tex.w, tex.h);
fs.writeFileSync(process.argv[4], JSON.stringify({w: tex.w, h: tex.h, rgba: Array.from(rgba)}));
"""
open('/tmp/my-project/work/TDKR-Game/extraction/re/session50/_node_etc1.js', 'w').write(NODE_DEC)

tg = open(TEXGLA, 'rb').read()
_, idxsz2, tabsz2, n2 = struct.unpack('>IIII', tg[:16])
pool2 = tg[16 + n2 * 16:idxsz2]

def tex_member(want):
    for i in range(n2):
        o, s, no, _ = struct.unpack('>IIII', tg[16 + i * 16:16 + i * 16 + 16])
        nm2 = pool2[no:pool2.index(b'\0', no)].decode('ascii', 'replace')
        if nm2.lower() == want.lower():
            return tg[o:o + s]
    return None

def unwrap_split(u8):
    if bytes(u8[:4]) != b'PK\x03\x04':
        return {'rgb': u8}
    out = {}; pos = 0
    while pos + 30 <= len(u8) and bytes(u8[pos:pos + 4]) == b'PK\x03\x04':
        csz = struct.unpack_from('<I', u8, pos + 18)[0]
        nlen = struct.unpack_from('<H', u8, pos + 26)[0]
        elen = struct.unpack_from('<H', u8, pos + 28)[0]
        nm = u8[pos + 30:pos + 30 + nlen].decode('latin1')
        dstart = pos + 30 + nlen + elen
        if nm.strip() != 'SPLIT':
            out[nm] = u8[dstart:dstart + csz]
        pos = dstart + csz
    return out

# main LightMapDC-family diffuse textures (roads/ground) + footprint + a LM page
NAMES = ['GC_Road_Main.tga', 'GC_Road_01.tga', 'GC_Sidewalk.tda', 'GC_Footprint_VD_Items.tga',
         'BakeGroup_Island1_B0.tga', 'GC_Ground.tga', 'GC_RiverBed.tga', 'GC_Water.tga']
# fall back: enumerate first 24 texture names
allnames = []
for i in range(n2):
    o, s, no, _ = struct.unpack('>IIII', tg[16 + i * 16:16 + i * 16 + 16])
    allnames.append(pool2[no:pool2.index(b'\0', no)].decode('ascii', 'replace'))
use = [n for n in NAMES if tex_member(n)]
if len(use) < 4:
    use = allnames[:12]
print('testing %d textures: %s' % (len(use), use))

import base64
results = []
for nm in use:
    tu = tex_member(nm)
    if tu is None:
        continue
    try:
        parts = unwrap_split(tu)
        pvr = parts['rgb.pvr'] if 'rgb.pvr' in parts else parts['rgb']
        th_, tw = struct.unpack_from('<II', pvr, 4)
        bw, bh = (tw + 3) // 4, (th_ + 3) // 4
        blocks = np.frombuffer(pvr, np.uint8, bw * bh * 8, 52)
        # Python decode
        py = cr.decode_etc1_cleanroom(blocks, tw, th_)
        pyrgba = py[:, :, :3].astype(np.int32).ravel()
        # JS decode
        payload = json.dumps({'w': int(tw), 'h': int(th_),
                              'blocks': base64.b64encode(blocks.tobytes()).decode()})
        open('/tmp/my-project/work/TDKR-Game/extraction/re/session50/_tex_payload.json', 'w').write(payload)
        r = subprocess.run(['node', '/tmp/my-project/work/TDKR-Game/extraction/re/session50/_node_etc1.js',
                            '/tmp/my-project/work/city_slice_wt/playable/etc1_tdkr.js',
                            '/tmp/my-project/work/TDKR-Game/extraction/re/session50/_tex_payload.json',
                            '/tmp/my-project/work/TDKR-Game/extraction/re/session50/_tex_out.json'],
                           capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            print(nm, 'NODE FAIL', r.stderr[:200]); continue
        out = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session50/_tex_out.json'))
        js = np.array(out['rgba'], np.int32).reshape(-1, 4)[:, :3].ravel()
        neq = int((pyrgba != js).sum())
        frac = neq / len(pyrgba)
        mad = float(np.abs(pyrgba - js).mean())
        results.append((nm, tw, th_, frac, mad))
        print('%-32s %dx%d  mismatching channels %.5f  MAD %.3f' % (nm, tw, th_, frac, mad))
    except Exception as e:
        print(nm, 'ERR', repr(e)[:120])
bad = [r for r in results if r[3] > 0]
print('textures with ANY decoder mismatch: %d / %d' % (len(bad), len(results)))
