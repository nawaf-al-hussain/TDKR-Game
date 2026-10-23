#!/usr/bin/env python3
"""s54 T2: grapple-target census.

Session 53 established: grapple targets are OBJECT-ANCHOR virtuals
(CWayPointObject::GetGrapnelTargetPosition @0x2a9024 / CGameObject @0x360c40),
not navmesh edge flags. The anchor candidates in the level data are the
waypoint records (engine cases 0x798f / 0x2666 / 0x4741 - the dispatcher
news CWayPointObject for them). This census:
  1. counts waypoint records per level (all 12 lvc files),
  2. extracts their positions from the pure-parser token streams,
  3. samples positions and reports the nearest walkable navmesh cell
     (GothamCity nm) with distance.
Also: which WAYPOINT records carry a grapple-capable marker (the payload's
conditional fields), and the 'Enemy_Grapnel_Target' gol template (0xaae6a)
usage (spawned by scripts, not lvc).
"""
import json
import struct
import importlib.util

spec = importlib.util.spec_from_file_location(
    'lvc_pure', '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_pure.py')
lp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lp)

table, templates = lp.load_table('/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import os
files = sorted('/tmp/my-project/work/data/' + f for f in os.listdir('/tmp/my-project/work/data')
               if f.endswith('.lvc'))

WAYPOINT_TIDS = {0x798f, 0x2666, 0x4741}
census = {}
for path in files:
    name = os.path.basename(path)
    try:
        tokens = []
        res = lp.parse(path, table, templates, tokens)
    except Exception as e:
        census[name] = {'error': str(e)[:80]}
        continue
    wps = []
    for rid, rs, tid, end, kind in res['records']:
        if tid in WAYPOINT_TIDS:
            wps.append((rid, rs, tid))
    census[name] = {'records': len(res['records']), 'complete': res['complete'],
                    'waypoints': len(wps)}
    census[name + '_offs'] = [(r[0], r[1], hex(r[2])) for r in wps[:3]]
    # positions: token stream scan is expensive; do a direct byte decode for
    # waypoint 0x798f framing: [i id][c][3f pos][11 x i32][i][i] + builtin cyl 45B
    if name in ('GothamCity.lvc', 'GothamCity_Island2.lvc'):
        pts = []
        d = res['data']
        for rid, rs, tid in wps:
            p = rs + 4  # skip tid
            oid = struct.unpack_from('>i', d, p)[0]; p += 4
            flag = d[p]; p += 1
            pos = struct.unpack_from('>3f', d, p); p += 12
            pts.append((oid, flag, [round(v, 2) for v in pos]))
        census[name + '_pts'] = pts

for k in sorted(census):
    if not k.endswith('_pts') and not k.endswith('_offs'):
        print(k, census[k])

# nearest walkable cell for a sample of GothamCity waypoints
nmj = None
for cand in ('/tmp/my-project/work/TDKR-Game/download/nm_gothamcity.json',
             '/tmp/my-project/work/data/GothamCity_502299_navdata.nm'):
    if os.path.exists(cand):
        print('nav source:', cand)
        break
