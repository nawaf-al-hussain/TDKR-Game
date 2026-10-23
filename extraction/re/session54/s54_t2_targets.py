#!/usr/bin/env python3
"""s54 T2 (2/2): waypoint flag census + nearest-walkable-triangle for samples.
Grapple-target identification: CWayPointObject::GetGrapnelTargetPosition is a
virtual on waypoint objects; the flag byte in the waypoint record frames the
payload type. Output: s54_t2_waypoints.json"""
import json
import struct
import importlib.util
import random

import numpy as np

spec = importlib.util.spec_from_file_location(
    'lvc_pure', '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_pure.py')
lp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lp)

table, templates = lp.load_table('/tmp/my-project/work/TDKR-Game/extraction/re/session26')
WAYPOINT_TIDS = {0x798f, 0x2666, 0x4741}

out = {'sign_convention': 'nearest-walkable distance in u, lower=better; '
       'flag byte values per waypoint record; samples are deterministic (seed 54)',
       'levels': {}}
random.seed(54)

for name in ('GothamCity.lvc', 'GothamCity_Island2.lvc', 'Police_Station.lvc',
             'StockExchange.lvc', 'Underground.lvc', 'ThePit.lvc', 'Military.lvc',
             'Stadion.lvc', 'BatCave.lvc'):
    path = '/tmp/my-project/work/data/' + name
    res = lp.parse(path, table, templates, None)
    d = res['data']
    wps = []
    for rid, rs, tid, end, kind in res['records']:
        if tid in WAYPOINT_TIDS:
            p = rs + 4
            oid = struct.unpack_from('>i', d, p)[0]; p += 4
            flag = d[p]; p += 1
            pos = struct.unpack_from('>3f', d, p)
            wps.append(dict(oid=oid, flag=flag, pos=[round(v, 2) for v in pos]))
    flags = {}
    for w in wps:
        flags[w['flag']] = flags.get(w['flag'], 0) + 1
    out['levels'][name] = {
        'waypoints': len(wps),
        'flag_census': flags,
        'sample': wps[:5],
    }
    if name.startswith('GothamCity') and 'Island2' not in name:
        # nearest walkable triangle for 200 random waypoints (GothamCity nm)
        nmf = '/tmp/my-project/work/TDKR_assets/raw/game_config/GothamCity_502299_navdata.nm'
        dnm = open(nmf, 'rb').read()
        N = len(dnm)
        fa = np.frombuffer(dnm[2:2 + (N - 2) // 4 * 4], '>f4').astype(np.float64)
        T = len(fa) // 3
        tr = fa[:T * 3].reshape(T, 3)
        ok = (tr[:, 2] > -60) & (tr[:, 2] < 450) & (np.abs(tr[:, 0]) < 2000) & \
             (np.abs(tr[:, 1]) < 2000) & np.isfinite(tr).all(axis=1)
        badw = np.convolve((~ok).astype(int), np.ones(12, int), 'valid') >= 4
        b = int(np.argmax(badw)) if badw.any() else int(ok.sum())
        tris = tr[:b]          # (b,3) walkable vertex points (s34 nm decode units)
        cents = tris           # nearest-walkable-point test uses the vertices directly
        sample = random.sample(wps, min(200, len(wps)))
        rows = []
        for w in sample:
            p = np.array(w['pos'])
            dists = np.linalg.norm(cents[:, :3] - p, axis=1)
            # 2D distance on x/y with z within 12 u (walkable surface proximity)
            dxy = np.linalg.norm(cents[:, :2] - p[:2], axis=1)
            zok = np.abs(cents[:, 2] - p[2]) < 12
            cand = np.where(zok)[0]
            if len(cand):
                i = cand[np.argmin(dxy[cand])]
                rows.append(dict(oid=w['oid'], flag=w['flag'], pos=w['pos'],
                                 nearest_xy=round(float(dxy[i]), 2),
                                 nearest_cell=[round(float(v), 1) for v in cents[i]],
                                 within2m=bool(dxy[i] < 2.0)))
            else:
                rows.append(dict(oid=w['oid'], flag=w['flag'], pos=w['pos'],
                                 nearest_xy=None, nearest_cell=None, within2m=False))
        rate = sum(1 for r in rows if r['within2m']) / len(rows)
        out['levels'][name]['nearest_walkable_sample'] = dict(
            n=len(rows), within2m_rate=round(rate, 4), rows=rows[:20])
        # random-position null: same count of uniform points inside the bbox
        lo = cents.min(axis=0); hi = cents.max(axis=0)
        rnd = np.random.RandomState(54)
        pts = rnd.uniform(lo, hi, size=(len(rows), 3))
        r2 = []
        for p in pts:
            dxy = np.linalg.norm(cents[:, :2] - p[:2], axis=1)
            zok = np.abs(cents[:, 2] - p[2]) < 12
            cand = np.where(zok)[0]
            r2.append(bool(len(cand)) and bool(dxy[cand].min() < 2.0))
        out['levels'][name]['random_null_within2m_rate'] = round(float(np.mean(r2)), 4)
    out['levels'][name]['waypoints'] = len(wps)

json.dump(out, open('/tmp/my-project/work/TDKR-Game/extraction/re/session54/s54_t2_waypoints.json', 'w'), indent=1)
for k, v in out['levels'].items():
    nw = (v.get('nearest_walkable_sample') or {})
    print('%-24s wps=%5d flags=%s within2m=%s (null %s)' % (
        k, v['waypoints'], dict(list(v['flag_census'].items())[:6]),
        nw.get('within2m_rate'), out['levels'][k].get('random_null_within2m_rate')))
