#!/usr/bin/env python3
"""S41 T3: script-side usage of MC_MAX_DISTANCE (nil-would-error vs guarded)."""
import re, struct, sys, zipfile

Z = zipfile.ZipFile('/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip')
raw = Z.read('com.gameloft.android.AMAZ.GloftKRAS/files/data/game_config.gla')
print('game_config.gla size:', len(raw))

NAME = b'MC_MAX_DISTANCE'
occ = []
p = 0
while True:
    i = raw.find(NAME, p)
    if i < 0: break
    occ.append(i)
    p = i + 1
print('occurrences:', len(occ))

# script boundaries: the gla embeds lua sources; script name markers vary.
# Use a generic window classification instead.
GUARD_PAT = re.compile(rb'(if\s+MC_MAX_DISTANCE|MC_MAX_DISTANCE\s+and|and\s+MC_MAX_DISTANCE|'
                       rb'MC_MAX_DISTANCE\s+or|or\s+MC_MAX_DISTANCE|type\s*\(\s*MC_MAX_DISTANCE|'
                       rb'tonumber\s*\(\s*MC_MAX_DISTANCE|rawget|pcall)')
CLASSIFY = {
    'cmp': re.compile(rb'MC_MAX_DISTANCE\s*(<|>|<=|>=|==|~=)\s*[\w.]|[\w.]\s*(<|>|<=|>=|==|~=)\s*MC_MAX_DISTANCE'),
    'arith': re.compile(rb'MC_MAX_DISTANCE\s*[-+*/%]|\*\s*MC_MAX_DISTANCE|[-+/%]\s*MC_MAX_DISTANCE'),
    'index': re.compile(rb'MC_MAX_DISTANCE\s*\['),
    'call_arg': re.compile(rb'\w+\s*\([^()]*MC_MAX_DISTANCE'),
    'assign': re.compile(rb'(local\s+)?[\w.]+\s*=\s*MC_MAX_DISTANCE'),
    'guard': GUARD_PAT,
}
counts = {}
for i in occ:
    lo, hi = max(0, i - 100), min(len(raw), i + 140)
    ctx = raw[lo:hi]
    tags = [k for k, rx in CLASSIFY.items() if rx.search(ctx)]
    # printable context
    txt = ''.join(chr(c) if 32 <= c < 127 else ('\n' if c == 10 else '.') for c in ctx)
    print(f'\n--- @0x{i:x} tags={tags}')
    print(txt.replace('\n', ' | ')[:240])
    for t in tags:
        counts[t] = counts.get(t, 0) + 1

print('\nusage-type counts (a site may match several):', counts)

# also the 16 constant-like names from s39 — quick presence table for siblings
for nm in (b'CAMERA_SHAKE_BOMB', b'UNDERGROUND', b'FACE_BATMAN', b'ZONE'):
    c = raw.count(nm)
    print(f'script presence of {nm.decode()}: {c}')
