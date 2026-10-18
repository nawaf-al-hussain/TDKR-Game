#!/usr/bin/env python3
"""S36 T1g: parse the post-cell zone (Y u16, grid class, grid records) for all .nm files."""
import struct, math, json

BASE = '/tmp/my-project/work/TDKR_assets/raw/game_config'

def parse(path):
    d = open(path, 'rb').read()
    n = len(d)
    vcount = struct.unpack_from('>H', d, 0)[0]
    soup_end = 2 + vcount * 12
    X = struct.unpack_from('>H', d, soup_end)[0]
    ccount = struct.unpack_from('>H', d, soup_end + 2)[0]
    cells_start = soup_end + 4
    cells_end = cells_start + ccount * 15
    if cells_end + 3 > n:
        return {'file': path.split('/')[-1], 'error': f'cells overrun {cells_end}>{n}'}
    Y = struct.unpack_from('>H', d, cells_end)[0]
    gclass = d[cells_end + 2]
    o = cells_end + 3
    out = {'file': path.split('/')[-1], 'size': n, 'vcount': vcount, 'X': X,
           'ccount': ccount, 'cells_start': cells_start, 'cells_end': cells_end,
           'Y': Y, 'gridClass': gclass}
    if gclass != 0:
        out['grid'] = 'QUADTREE (Load=bx lr, no data)'
        out['grid_end'] = o
        return out
    nx, ny = struct.unpack_from('>HH', d, o); o += 4
    fl = struct.unpack_from('>4f', d, o); o += 16
    out.update({'nx': nx, 'ny': ny, 'bbox': [round(f, 2) for f in fl]})
    nrec = 0; total_nodes = 0; total_ids = 0; empty = 0
    try:
        for i in range(nx * ny):
            N = d[o]; o += 1
            if N == 0:
                empty += 1
                continue
            for k in range(N):
                f = struct.unpack_from('>f', d, o)[0]; o += 4
                a = struct.unpack_from('>H', d, o)[0]; o += 2
                b = struct.unpack_from('>H', d, o)[0]; o += 2
                o += b * 2
                total_nodes += 1; total_ids += b
                if o > n: raise IndexError
        out.update({'grid_records': nrec, 'grid_empty': empty, 'nodes': total_nodes,
                    'ids': total_ids, 'grid_end': o, 'slack': n - o})
    except IndexError:
        out.update({'grid_error': f'overrun at 0x{o:x}', 'grid_records': nrec})
    return out

import glob, os
files = sorted(glob.glob(BASE + '/*_navdata.nm'))
res = [parse(f) for f in files]
for r in res:
    print(json.dumps(r))
json.dump(res, open('/tmp/my-project/work/TDKR-Game/extraction/re/session36_t1_gridparse.json', 'w'), indent=1)
