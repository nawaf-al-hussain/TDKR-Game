#!/usr/bin/env python3
"""S35 T1a17: clip names 655..920; duplicates? and name↔segment count math."""
import struct, json

AD = '/tmp/my-project/work/data/batman_anims.bdae'
ad = open(AD, 'rb').read()
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]

def cstr(v):
    if 0 < v < len(ad):
        e = ad.find(b'\0', v)
        if 0 < e - v < 90:
            return ad[v:e].decode('latin1')
    return None

clips = []
o = 0x11580
for i in range(921):
    nameOff, ts, te = struct.unpack_from('<3I', ad, o + 12 * i)
    clips.append((cstr(nameOff), ts, te, nameOff))

print('clips 655..680:')
for i in range(655, 681):
    print(f'  clip {i:3d}: {clips[i][0]:40} [{clips[i][1]}..{clips[i][2]}]')
print('clips 915..920:')
for i in range(915, 921):
    print(f'  clip {i:3d}: {clips[i][0]:40} [{clips[i][1]}..{clips[i][2]}]')

names = [c[0] for c in clips]
dups = {}
for i, n in enumerate(names):
    dups.setdefault(n, []).append(i)
dupcounts = {n: v for n, v in dups.items() if len(v) > 1}
print(f'\nunique names: {len(dups)}/921; duplicated names: {len(dupcounts)}')
for n, v in list(dupcounts.items())[:12]:
    print(f'  {n}: {v}')

# name-prefix census
import collections
pref = collections.Counter()
for n in names:
    parts = n.split('_')
    pref['_'.join(parts[1:3])] += 1
print('\nname family census (top 20):', pref.most_common(20))
