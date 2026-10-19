#!/usr/bin/env python3
"""S38 T4: hunt the animation-graph/state data across ALL archive members +
.so rodata, with POSITIVE CONTROLS.

Targets (Lua state strings): Idle, Ranged_Run, Grapnel, Glide, Melee, ...
Search corpus: every member of every .gla in the release zip (164 entries),
game_config.gla, actors.gla, commons.gla + others; plus libKRHP.so rodata.
Positive controls: strings KNOWN to exist per file (clip names in
batman_anims.bdae; engine API names in rodata)."""
import struct, zipfile, json, re, sys
import numpy as np

ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
z = zipfile.ZipFile(ZIP)
names = z.namelist()
print('zip entries:', len(names))

STATE_STRINGS = ['Idle', 'Ranged_Run', 'Grapnel', 'Glide', 'Melee', 'Run', 'Walk',
                 'Jump', 'Fall', 'Land', 'Dodge', 'Dive', 'Grapple', 'AimRun',
                 'Ranged_Idle', 'Baton', 'Cape', 'Land_Hard', 'WallLand']
# positive controls (strings we KNOW exist somewhere)
CONTROLS = ['_001_idle_stand', '_008_run', 'Bip01_Pelvis', 'chara_Batman_DIFFUSE',
            'GetDistFromMC', 'lua_setglobal', 'PVRTCDecompress']

def scan(data, label, pats, out):
    hits = {}
    for p in pats:
        n = data.count(p.encode())
        if n: hits[p] = n
    if hits:
        out[label] = hits
    return hits

results = {}
control_hits = {}
# 1. all .gla members (raw bytes)
gla_files = [n for n in names if n.endswith('.gla')]
print('gla archives:', len(gla_files))
for g in gla_files:
    d = z.read(g)
    n = struct.unpack_from('>I', d, 12)[0]
    pool = 16 + n * 16
    st_hits = {}
    # positive control inside this archive: any member name strings
    cn = scan(d, g, CONTROLS, control_hits)
    # brute-force scan the WHOLE archive for state strings (headers + bodies + pools)
    scan(d, g, STATE_STRINGS, st_hits)
    # per-member scan for the big archives
    if st_hits or cn:
        for i in range(n):
            o = 16 + i * 16
            off, size, nameOff = struct.unpack_from('>3I', d, o)
            nb = pool + nameOff
            e = d.index(b'\0', nb)
            nm = d[nb:e].decode('latin1')
            if off + size > len(d): continue
            member = d[off:off + size]
            h = scan(member, f'{g}::{nm}', STATE_STRINGS, results)
    for k, v in st_hits.items():
        results.setdefault(g + ' [ARCHIVE-LEVEL]', {}).update({k2: v2 for k2, v2 in v.items() if k2 in STATE_STRINGS})

# 2. .so rodata
SO = open('/tmp/my-project/work/re29/libKRHP.so', 'rb').read()
rodata_hits = {}
for p in STATE_STRINGS:
    c = SO.count(p.encode())
    if c: rodata_hits[p] = c
results['libKRHP.so [whole file]'] = rodata_hits
cn = scan(SO, 'libKRHP.so', CONTROLS, control_hits)

print('\n=== POSITIVE CONTROLS (must hit) ===')
print(json.dumps(control_hits, indent=1)[:800])
print('\n=== STATE-STRING HITS ===')
print(json.dumps(results, indent=1)[:2500])
json.dump({'state_hits': results, 'controls': control_hits},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session38/s38_t4_animgraph_scan.json', 'w'), indent=1)
print('saved s38_t4_animgraph_scan.json')
