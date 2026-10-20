#!/usr/bin/env python3
"""S41 T3b: usage counts (uncommented!), pointer arrays over the name pool,
and code refs to any such array base."""
import re, struct, sys, zipfile
sys.path.insert(0, '/home/z/my-project/scripts')

# ---- 1. uncommented-usage counts ----
Z = zipfile.ZipFile('/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')
raw = Z.read('com.gameloft.android.AMAZ.GloftKRAS/files/data/game_config.gla')
NAME = b'MC_MAX_DISTANCE'
occ = []
p = 0
while True:
    i = raw.find(NAME, p)
    if i < 0: break
    occ.append(i); p = i + 1

def line_start(buf, i):
    a = buf.rfind(b'\n', 0, i)
    return a + 1

stats = {'total': len(occ), 'commented': 0, 'uncommented': 0,
         'uncommented_arith': 0, 'uncommented_cmp': 0, 'uncommented_callarg': 0, 'other': 0}
for i in occ:
    ls = line_start(raw, i)
    pre = raw[ls:i]
    commented = pre.lstrip().startswith(b'--') or pre.rstrip().endswith(b'--')
    ctx = raw[max(0, i - 60):i + 60]
    if commented:
        stats['commented'] += 1
        continue
    stats['uncommented'] += 1
    if re.search(rb'[-+*/%]\s*MC_MAX_DISTANCE|MC_MAX_DISTANCE\s*[-+*/%]|\*\s*MC_MAX_DISTANCE', ctx):
        stats['uncommented_arith'] += 1
    elif re.search(rb'MC_MAX_DISTANCE\s*(<|>|<=|>=|==|~=)', ctx):
        stats['uncommented_cmp'] += 1
    elif re.search(rb'\w\w+\s*\(', ctx) and b'(' in ctx:
        stats['uncommented_callarg'] += 1
    else:
        stats['other'] += 1
print('usage stats:', stats)

# ---- 2. pointer arrays over the name pool ----
SO = '/tmp/my-project/work/TDKR-Game/extraction/lib_libKRHP.so'
d = open(SO, 'rb').read()
phoff = struct.unpack_from('<I', d, 0x1c)[0]
phnum = struct.unpack_from('<H', d, 0x2c)[0]
segs = []
for i2 in range(phnum):
    o = phoff + i2 * 32
    t, off, va, pa, fs, ms = struct.unpack_from('<8I', d, o)[:6]
    if t == 1 and fs > 0: segs.append((va, off, fs, ms))

def v2o(va):
    for v, o, s, m in segs:
        if v <= va < v + s: return o + (va - v)
    return None

def o2v(o):
    for v, oo, s, m in segs:
        if oo <= o < oo + s: return v + (o - oo)
    return None

LOAD_MAX = max(v + s for v, o, s, m in segs)

pool_strs = {'MC_MAX_DISTANCE': 0xb30948, 'CAMERA_SHAKE_BOMB': 0xb3089c,
             'INTERFERENCE_COOLDOWN_TIME': 0xb30958, 'REWARD_PROPERTY': 0xb30938,
             'gCurSoundZone': 0xb30974, 'MC_SOUND_DISTANCE': 0xb30818}
for nm, va in pool_strs.items():
    pword = struct.pack('<I', va)
    hits = []
    o = 0
    while True:
        i = d.find(pword, o)
        if i < 0 or i > LOAD_MAX: break
        v = o2v(i)
        if v is not None: hits.append(v)
        o = i + 1
    print(f'pointer words to {nm} ({va:#x}): {[hex(x) for x in hits[:8]]}')
    if hits:
        # dump the array neighborhood to see if it's a (ptr,value) table
        a0 = v2o(hits[0])
        ctxwords = struct.unpack_from('<8I', d, a0 - 16)
        print('   array context [-4..+3]:', [hex(x) for x in ctxwords])
