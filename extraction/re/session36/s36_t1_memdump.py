#!/usr/bin/env python3
"""S36 T1i: re-run Create, dump in-memory soup/cells/grid, compare vs static file parse."""
import struct, sys, json
sys.path.insert(0, '/home/z/my-project/scripts')
from s36_t1_trace import Emu

NM = '/tmp/my-project/work/TDKR_assets/raw/game_config/GothamCity_502299_navdata.nm'
nm = open(NM, 'rb').read()
emu = Emu()
emu.load_nm(nm)
st = emu.run_create()
print('status:', st)
mu = emu.mu
f = emu.dump()
soup_p, cells_p, grid_p = f['f14_soup'], f['f18_cells'], f['f64_grid']
vcount, ccount = f['f08_vcount'], f['f0c_ccount']

# 1) soup vs file
soup_mem = bytes(mu.mem_read(soup_p, vcount * 12))
soup_file = nm[2:2 + vcount * 12]
print('soup identical to file bytes 2..:', soup_mem == soup_file)
if soup_mem != soup_file:
    diffs = sum(1 for a, b in zip(soup_mem, soup_file) if a != b)
    print('  diff bytes:', diffs)

# 2) cells vs static 15-B records
cells_mem = bytes(mu.mem_read(cells_p, ccount * 16))
cs = 2 + vcount * 12 + 4
bad = 0; regions = set(); sym_ok = 0; sym_bad = 0
nlinks = 0
cells = []
for i in range(ccount):
    m = cells_mem[i*16:(i+1)*16]
    v0, v1, v2, n0, n1, n2, reg, ch = struct.unpack_from('<6HhHBB?', m[:15])if False else (None,)*8
    v0, v1, v2 = struct.unpack_from('<3H', m, 0)
    n0, n1, n2 = struct.unpack_from('<3h', m, 6)
    reg = struct.unpack_from('<H', m, 12)[0]
    ch = m[14]; pad = m[15]
    s = nm[cs + i*15: cs + i*15 + 15]
    v0f, v1f, v2f = struct.unpack_from('<3H', s, 0)
    n0f, n1f, n2f = struct.unpack_from('<3h', s, 6)
    regf = struct.unpack_from('<H', s, 12)[0]
    chf = s[14]
    if (v0, v1, v2, n0, n1, n2, reg, ch) != (v0f, v1f, v2f, n0f, n1f, n2f, regf, chf):
        bad += 1
        if bad <= 3:
            print(f'  cell {i} mem=({v0},{v1},{v2},{n0},{n1},{n2},{reg},{ch}) file=({v0f},{v1f},{v2f},{n0f},{n1f},{n2f},{regf},{chf})')
    regions.add(reg)
    cells.append((v0, v1, v2, n0, n1, n2, reg))
    if pad != 0 and bad < 3:
        pass
print(f'cells identical (mem 16-B vs file 15-B packed): {ccount-bad}/{ccount} bad={bad}')
print('distinct regions:', len(regions), 'min', min(regions), 'max', max(regions))

# neighbour symmetry over ALL links
nb = {}
for i, (v0, v1, v2, n0, n1, n2, reg) in enumerate(cells):
    for n in (n0, n1, n2):
        if n != -1 and n != 0xFFFF:
            nb.setdefault(i, set()).add(n)
tot = sum(len(s) for s in nb.values())
ok = 0
for a, ss in nb.items():
    for b in ss:
        if b < ccount and a in nb.get(b, ()):
            ok += 1
print(f'neighbour links total={tot} symmetric={ok} ratio={ok/tot if tot else 0:.4f}')

# 3) grid object dump
g = bytes(mu.mem_read(grid_p, 0x9F))
gv = struct.unpack_from('<20I', g, 0)
print('grid object first 80 B:', ' '.join(f'{x:08x}' for x in gv[:20]))
gnx, gny = struct.unpack_from('<2I', g, 8)
gcnt = struct.unpack_from('<I', g, 0x10)[0]
gminx, gminy, gmaxx, gmaxy = struct.unpack_from('<4f', g, 0x14)
ent_p = struct.unpack_from('<I', g, 4)[0]
print(f'grid: nx={gnx} ny={gny} count={gcnt} bbox=({gminx:.2f},{gminy:.2f},{gmaxx:.2f},{gmaxy:.2f}) entries@0x{ent_p:x}')
# entries: 12-B each [u8 n][u16 off][u16 cnt]... from Load: entry[0]=N, entry[4]=ptr?, entry[8]=cnt?
nodes_total = 0; ids_total = 0; empty = 0
node_ptrs = set()
for i in range(gnx * gny):
    e = bytes(mu.mem_read(ent_p + i * 12, 12))
    n = e[0]
    p, c = struct.unpack_from('<2I', e, 4)
    if n == 0:
        empty += 1
        continue
    nodes_total += n
    node_ptrs.add(p)
print(f'grid entries: {gnx*gny}, empty={empty}, nodes={nodes_total}, distinct node-list ptrs={len(node_ptrs)}')
# dump one node list
some = sorted(node_ptrs)[:1]
if some:
    arr = bytes(mu.mem_read(some[0], 12))
    print('first node-list words:', [hex(x) for x in struct.unpack('<3I', arr)])
# region count from X field
print('nova.f10_X (engine region count field) =', f['f10_X'])
json.dump({'status': st, 'fields': {k: f[k] for k in f},
           'soup_identical': soup_mem == soup_file,
           'cells_bad': bad, 'regions': len(regions), 'links': tot, 'sym': ok,
           'grid_nx': gnx, 'grid_ny': gny, 'grid_empty': empty, 'grid_nodes': nodes_total},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session36_t1_memdump.json', 'w'), indent=1)
