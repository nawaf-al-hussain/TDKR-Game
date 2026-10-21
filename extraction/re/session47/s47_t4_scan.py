#!/usr/bin/env python3
"""s47 T4: do any lvc name-pool strings contain non-ASCII bytes? If none,
UTF-8-with-replacement and latin1 agree byte-for-byte on every name and the
s46 latin1 digest is already the unified correct decoding; if some, test the
UTF-8 validity of the high-byte runs and pick the engine-faithful decoding
(Lua strings and file names are byte strings -> bytes-preserving latin1)."""
import struct, io, zipfile, json, hashlib
import numpy as np

GLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/game_config.gla'
g = open(GLA, 'rb').read()
_, idxsz, tabsz, n = struct.unpack('>IIII', g[:16])
pool = g[16 + n * 16:idxsz]
levels = {}
for i in range(n):
    o, s, no, _ = struct.unpack('>IIII', g[16 + i * 16:16 + i * 16 + 16])
    nm = pool[no:pool.index(b'\0', no)].decode('ascii', 'replace')
    if nm.endswith('.lvc'):
        levels[nm] = g[o:o + s]
print('lvc levels:', [(k, len(v)) for k, v in levels.items()])

report = {}
for nm, data in levels.items():
    # extract printable ASCII runs (>=4 chars) that are terminated by \0 or
    # a non-printable — the name-pool convention used by the lvc parsers
    runs = []
    high_bytes = 0
    i = 0
    L = len(data)
    start = None
    while i < L:
        c = data[i]
        if 32 <= c < 127:
            if start is None:
                start = i
            i += 1
        elif c >= 128:
            # high byte inside/outside a run
            if start is not None and i - start >= 4:
                runs.append((start, data[start:i]))
            start = None
            high_bytes += 1
            i += 1
        else:
            if start is not None and i - start >= 4:
                runs.append((start, data[start:i]))
            start = None
            i += 1
    if start is not None and i - start >= 4:
        runs.append((start, data[start:i]))
    # count runs CONTAINING high bytes: rescan properly (high bytes glued to runs)
    glued = 0
    samples = []
    i = 0
    while i < L:
        j = i
        while j < L and (32 <= data[j] < 127 or data[j] >= 128):
            j += 1
        seg = data[i:j]
        if j - i >= 6 and any(b >= 128 for b in seg):
            glued += 1
            if len(samples) < 5:
                samples.append((hex(i), seg[:40]))
        i = max(j, i + 1)
    report[nm] = {'high_byte_count': high_bytes, 'glued_runs': glued,
                  'samples': [(a, s.decode('latin1')) for a, s in samples]}
    print(nm, 'high bytes:', high_bytes, 'runs containing high bytes:', glued,
          'samples:', report[nm]['samples'][:3])

# UTF-8 validity test on the high-byte regions (whole-file attempt)
for nm, data in levels.items():
    try:
        data.decode('utf-8')
        ok = True
    except UnicodeDecodeError as e:
        ok = False
    print(nm, 'whole-buffer valid UTF-8:', ok)

json.dump(report, open('/tmp/my-project/work/TDKR-Game/extraction/re/session47/s47_t4_scan.json', 'w'), indent=1)
print('saved s47_t4_scan.json')
