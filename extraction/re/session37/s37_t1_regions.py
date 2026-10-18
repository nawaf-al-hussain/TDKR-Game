#!/usr/bin/env python3
"""S37 T1b: file-side region census on GothamCity .nm.
- region id histogram from cell field 7 (u16 BE)
- ids >= regionCount: which, how many cells each
- cross-region neighbour links (does the n-graph cross regions AT ALL?)
- grid node-list region values vs cell regions (the 1,035 candidates)
- nulls: shuffled region labels
"""
import struct, json
from collections import defaultdict, Counter
import numpy as np

BASE = '/tmp/my-project/work/TDKR_assets/raw/game_config'
NM = BASE + '/GothamCity_502299_navdata.nm'
nm = open(NM, 'rb').read()
vcount = struct.unpack_from('>H', nm, 0)[0]
soup_end = 2 + vcount * 12
region_count_hdr = struct.unpack_from('>H', nm, soup_end)[0]
ccount = struct.unpack_from('>H', nm, soup_end + 2)[0]
cs = soup_end + 4
print(f'vcount={vcount} regionCount(hdr)={region_count_hdr} ccount={ccount}')

regs = np.zeros(ccount, dtype=np.int64)
n0 = np.zeros(ccount, dtype=np.int64); n1 = np.zeros(ccount, dtype=np.int64); n2 = np.zeros(ccount, dtype=np.int64)
for i in range(ccount):
    base = cs + i * 15
    v = struct.unpack_from('>6H', nm, base)
    n0[i], n1[i], n2[i] = v[3], v[4], v[5]
    regs[i] = struct.unpack_from('>H', nm, base + 12)[0]
f = lambda w: np.where(w > 0x7FFF, w.astype(np.int64) - 0x10000, w)
n0, n1, n2 = f(n0), f(n1), f(n2)

hist = Counter(regs.tolist())
distinct = sorted(hist)
print(f'distinct region ids in cells: {len(distinct)} (hdr says {region_count_hdr})')
over = [r for r in distinct if r >= region_count_hdr]
print(f'ids >= {region_count_hdr}: {over}')
for r in over:
    print(f'  id {r}: {hist[r]} cells')
print('top-5 regions by cells:', hist.most_common(5))
singles = [r for r in distinct if hist[r] == 1]
print(f'regions with exactly 1 cell: {len(singles)}')

links = 0; cross = 0
cross_pairs = []
for i in range(ccount):
    for n in (n0[i], n1[i], n2[i]):
        if n >= 0:
            links += 1
            if regs[n] != regs[i]:
                cross += 1
                if len(cross_pairs) < 8:
                    cross_pairs.append((i, int(n), int(regs[i]), int(regs[n])))
print(f'directed links={links}  CROSS-REGION links={cross}')
for p in cross_pairs:
    print('  cross:', p)

gs = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session36/session36_t1_gridparse.json'))
g = [x for x in gs if 'GothamCity' in x['file']][0]
nx, ny = g['nx'], g['ny']
o2 = g['cells_end'] + 3 + 4 + 16
node_regions = Counter()
node_total = 0
for i in range(nx * ny):
    N = nm[o2]; o2 += 1
    for k in range(N):
        o2 += 4
        a_ = struct.unpack_from('>H', nm, o2)[0]; o2 += 2
        b_ = struct.unpack_from('>H', nm, o2)[0]; o2 += 2
        o2 += b_ * 2
        node_regions[a_] += 1
        node_total += 1
print(f'grid per-region nodes: {node_total} nodes across {len(node_regions)} distinct region ids')
grid_only = sorted(set(node_regions) - set(distinct))
cell_only = sorted(set(distinct) - set(node_regions))
print(f'region ids in grid but NOT in cells: {len(grid_only)}: {grid_only[:12]}')
print(f'region ids in cells but NOT in grid: {len(cell_only)}: {cell_only[:12]}')
union = set(distinct) | set(node_regions)
print(f'UNION of distinct ids (cells U grid) = {len(union)}')

rng = np.random.default_rng(37)
sh = regs.copy(); rng.shuffle(sh)
cross_null = 0
for i in range(ccount):
    for n in (n0[i], n1[i], n2[i]):
        if n >= 0 and sh[n] != sh[i]:
            cross_null += 1
p = np.array([hist[r] for r in distinct], dtype=float)
p /= p.sum()
exp_null = links * (1.0 - float((p ** 2).sum()))
print(f'NULL: shuffled-label cross links = {cross_null} (real = {cross}); '
      f'random-label expectation = {exp_null:.0f}')

json.dump({'vcount': int(vcount), 'regionCount_hdr': int(region_count_hdr), 'ccount': int(ccount),
           'distinct_ids': len(distinct), 'over_ids': {str(r): hist[r] for r in over},
           'singles': len(singles), 'links': int(links), 'cross_region_links': int(cross),
           'cross_pairs_sample': cross_pairs,
           'grid_nodes': int(node_total), 'grid_distinct': len(node_regions),
           'grid_only': grid_only, 'cell_only': cell_only, 'union': len(union),
           'null_shuffled_cross': int(cross_null), 'null_expected': exp_null},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session37/s37_t1_regions.json', 'w'), indent=1)
print('saved s37_t1_regions.json')
