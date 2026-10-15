#!/usr/bin/env python3
"""Summarize the engine-driven walk into T1 deliverables:
- per-island coverage + per-class consumption table
- collision census (components, prims, triangles)
- trigger->Lua ownership map (full script text)
- spawn census (batman spawns, NPC spawns with names)
- mesh placement records (skyline / reflections)
Output: work/t1_deliverables.json (compact) — the full detail stays in the
walk_census_*.json artifacts.
"""
import json
import struct
import collections

DATA = '/home/z/my-project/work/data'


def load_strings(path):
    d = open(path, 'rb').read()
    table_off = struct.unpack_from('>I', d, 4)[0]
    pos = table_off
    nstr = struct.unpack_from('>i', d, pos)[0]
    pos += 4
    strings = []
    for i in range(nstr):
        ln = struct.unpack_from('>i', d, pos)[0]
        pos += 4
        strings.append(d[pos:pos + ln].decode('utf-8', 'replace'))
        pos += ln
    return d, strings


out = {}
for island in ('GothamCity', 'GothamCity_Island2'):
    d, strings = load_strings(f'{DATA}/{island}.lvc')
    rep = json.load(open(f'/home/z/my-project/work/walk_rep_{island}.json'))
    cens = json.load(open(
        f'/home/z/my-project/work/walk_census_{island}.json'))
    entry = dict(
        records=rep['records'], complete=rep['complete'],
        end=rep['end'], table_off=rep['table_off'],
        classes={k: v for k, v in sorted(rep['classes_bytes'].items(),
                                         key=lambda kv: -kv[1]['n'])},
    )

    # collision census
    col = cens.get('0x2db081e2', [])
    nprims = ntris = 0
    max_tri = 0
    for c in col:
        off = int(c['off'], 16)
        p = off + 16
        nprim = d[p]
        p += 1
        nprims += nprim
        for _ in range(nprim):
            p += 4  # name idx
            ntri = struct.unpack_from('>i', d, p)[0]
            p += 4
            ntris += ntri
            max_tri = max(max_tri, ntri)
            p += ntri * 37
    entry['collision'] = dict(components=len(col), prims=nprims,
                              triangles=ntris, max_prims_tris=max_tri)

    # trigger->Lua
    trg = cens.get('0x37f7a8ae', [])
    lua = []
    for c in trg:
        off = int(c['off'], 16)
        p = off + 4 + 36 + 4 + 1   # skip i, 9f, i, c
        idx = struct.unpack_from('>i', d, p)[0]
        s = strings[idx] if 0 <= idx < len(strings) else ''
        objid = struct.unpack_from('>i', d, off)[0]
        lua.append(dict(off=hex(off), objId=objid, script=s))
    entry['triggers'] = dict(components=len(trg), with_script=len(lua),
                             total_script_bytes=sum(len(x['script'])
                                                    for x in lua))
    json.dump(lua, open(
        f'/home/z/my-project/work/t1_lua_{island}.json', 'w'))

    # spawns
    entry['spawns'] = len(cens.get('spawn', []))
    batman = [s for s in cens.get('spawn', [])
              if 'batman' in s.get('name', '')]
    entry['batman_spawns'] = batman
    entry['mesh_records'] = cens.get('mesh', [])
    out[island] = entry

    print(f"=== {island}: {entry['records']} records complete="
          f"{entry['complete']}")
    print(f"  collision: {entry['collision']}")
    print(f"  triggers: {entry['triggers']['components']} comps, "
          f"{entry['triggers']['with_script']} with Lua scripts "
          f"({entry['triggers']['total_script_bytes']} B of Lua)")
    print(f"  spawns: {entry['spawns']} (batman: {len(batman)})")
    print(f"  mesh records: {len(entry['mesh_records'])}")

json.dump(out, open('/home/z/my-project/work/t1_deliverables.json',
                    'w'), indent=1)
print('wrote t1_deliverables.json + t1_lua_*.json')
