#!/usr/bin/env python3
"""Parse gol.bin (Game Object Library template DB) — layout derived from
CGameObjectManager::Reload @0x366104 (disasm) + byte-verified:

  'DICT' | u32be tableOffset | u8 flag | u16be tag | u16be version=3
  | u32be NREC | NREC x u32be recordOffset
  per record @offset:
    u32be objectId | u32be m | m x u32be (misc list -> map_B, unused for framing)
    u16be n | u32be nameIdx (index into string table)
    n x (u32be compTypeId, u16be flagword)   # flag = flagword != 0
    (template data for flag!=0 components follows — skipped, next offset known)
"""
import struct, json, sys

d = open('/home/z/work/tdkr/gol.bin', 'rb').read()
assert d[:4] == b'DICT'
table_off = struct.unpack_from('>I', d, 4)[0]
tag = struct.unpack_from('>H', d, 9)[0]
ver = struct.unpack_from('>H', d, 11)[0]
nrec = struct.unpack_from('>I', d, 13)[0]
offs = [struct.unpack_from('>I', d, 17 + 4 * i)[0] for i in range(nrec)]
print(f'tag={tag:#x} ver={ver} nrec={nrec} table@{table_off:#x}')

# string table (for resolving nameIdx)
strings = []
pos = table_off
nstr = struct.unpack_from('>i', d, pos)[0]; pos += 4
for i in range(nstr):
    ln = struct.unpack_from('>i', d, pos)[0]; pos += 4
    strings.append(d[pos:pos + ln].decode('utf-8', 'replace')); pos += ln

templates = {}   # objectId -> list of (flag, compTypeId)
names = {}
bad = []
for i, off in enumerate(offs):
    if off == 0xFFFF or off >= table_off:
        bad.append((i, off)); continue
    p = off
    key = struct.unpack_from('>I', d, p)[0]; p += 4
    m = struct.unpack_from('>I', d, p)[0]; p += 4 + 4 * m
    n = struct.unpack_from('>H', d, p)[0]; p += 2
    name_idx = struct.unpack_from('>I', d, p)[0]; p += 4
    name = strings[name_idx] if name_idx < len(strings) else f'<idx {name_idx}>'
    comps = []
    ok = True
    for j in range(n):
        tid = struct.unpack_from('>I', d, p)[0]
        fl = struct.unpack_from('>H', d, p + 4)[0]
        comps.append((1 if fl else 0, tid))
        p += 6
    if key in templates:
        print(f'  DUP key {key:#x} at rec {i}')
    templates[key] = comps
    names[key] = name

print(f'parsed {len(templates)} templates, {len(bad)} bad offsets {bad[:5]}')
ncomp = sum(len(v) for v in templates.values())
print(f'total component entries: {ncomp}')
# census of component typeIds
from collections import Counter
c = Counter(tid for v in templates.values() for (_, tid) in v)
print(f'distinct component typeIds: {len(c)}')
for tid, cnt in c.most_common(30):
    f1 = sum(1 for v in templates.values() for (fl, t) in v if t == tid and fl == 1)
    print(f'  {tid:#010x}  total {cnt:5d}  flag1 {f1:5d}')
json.dump({'templates': {hex(k): [[f, t] for f, t in v] for k, v in templates.items()},
           'names': {hex(k): n for k, n in names.items()}},
          open('/home/z/work/tdkr/gol_templates.json', 'w'), indent=0)
print('saved gol_templates.json')
