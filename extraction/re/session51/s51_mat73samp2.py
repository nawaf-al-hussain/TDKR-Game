#!/usr/bin/env python3
"""s51 T1k: v2 - PVR mip chain via tex gla member table + mat73+others sampler raw dump."""
import struct, io, zipfile, sys
import numpy as np

BDAE = '/tmp/my-project/work/zone/GothamCity/GothamCity_materials.bdae'
TEXGLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/textures/l_gothamcity_tex.gla'
LE = zipfile.ZipFile(io.BytesIO(open(BDAE, 'rb').read())).read('little_endian_not_quantized.bdae')
NB = len(LE)
w32 = np.frombuffer(LE, '<u4', NB // 4)

def cstr(off, maxn=96):
    if not (0 < off < NB): return None
    e = int(LE.find(b'\0', off))
    if e < 0 or e == off or e - off > maxn: return None
    try: t = LE[off:e].decode('ascii')
    except Exception: return None
    return t if all(32 <= ord(c) < 127 for c in t) else None

IMG_BASE, IMG_N = 0x22a9c, 176
imgs = [(int(w32[(IMG_BASE + i * 12) // 4]), int(w32[(IMG_BASE + i * 12 + 8) // 4])) for i in range(IMG_N)]

# ---- tex gla member table (replicating s50 pyref head) ----
tg = open(TEXGLA, 'rb').read()
_, idxsz2, _, n2 = struct.unpack('>IIII', tg[:16])
pool2 = tg[16 + n2 * 16:idxsz2]
print('tex gla: n_members=%d' % n2)
_mem = {}
for i in range(n2):
    o, s, no, _ = struct.unpack('>IIII', tg[16 + i * 16:16 + i * 16 + 16])
    nm = pool2[no:pool2.index(b'\0', no)].decode('ascii', 'replace')
    _mem[nm.lower()] = (o, s, nm)

def tex_member_raw(name):
    o, s, nm = _mem[name.lower()]
    return tg[o:o + s], nm, s

# find the actual texture names used by zone mats
def sampler_block(mid):
    a = 0x5fea0 + mid * 36
    ws = [int(w32[(a + k * 4) // 4]) for k in range(9)]
    out = []
    for j in range(ws[4]):
        pa = ws[5] + j * 24
        pw = [int(w32[(pa + k * 4) // 4]) for k in range(6)]
        pname = cstr(pw[0])
        ent = {'name': pname, 'type': pw[1], 'count': pw[2]}
        if pw[2] == 13 and pw[3] == 1:
            v1 = pw[4]
            # header [1, ptr=v1+24] then value struct at v1+24: 6 words
            val = [int(w32[(v1 + 24 + k * 4) // 4]) for k in range(6)]
            idx = val[0]
            ent['value'] = val
            ent['img'] = cstr(imgs[idx][1]) if 0 <= idx < IMG_N else None
        out.append(ent)
    return cstr(ws[3]), out

for mid in (73, 302, 153, 156, 300):
    eff, params = sampler_block(mid)
    print('mat %d effect %r' % (mid, eff))
    for p in params:
        if 'value' in p:
            v = p['value']
            f = struct.unpack('<4f', struct.pack('<4I', *v[2:6]))
            print('  %-14s img=%-34r val=[%#x,%#x] scale/offset=%s' % (p['name'], p['img'], v[0], v[1], ['%.4f' % x for x in f]))
        else:
            print('  %-14s type=%d count=%d' % (p['name'], p['type'], p['count']))

# ---- mip chain check: member size vs level0 size ----
print()
print('=== mip chain check ===')
cands = []
for lo, (o, s, nm) in _mem.items():
    if any(k in lo for k in ('roads', 'bakegroup_island1', 'lightmap', '_lm')):
        cands.append((lo, o, s, nm))
cands.sort()
for lo, o, s, nm in cands[:24]:
    u8 = tg[o:o + s]
    if u8[:4] == b'PK\x03\x04':
        print('%-42s ZIP-split member (size %d)' % (nm, s))
        continue
    th_, tw = struct.unpack_from('<II', u8, 4)
    bw, bh = (tw + 3) // 4, (th_ + 3) // 4
    lvl0 = bw * bh * 8
    extra = len(u8) - 52 - lvl0
    print('%-42s %dx%d lvl0=%d member=%d extra=%d %s' % (nm, tw, th_, lvl0, len(u8), extra, 'MIPS?' if extra > 0 else ''))
