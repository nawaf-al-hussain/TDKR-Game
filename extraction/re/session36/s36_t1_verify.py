#!/usr/bin/env python3
"""S36 T1j: byte-exact verification (fixed endianness) + full nova field dump."""
import struct, sys, json
sys.path.insert(0, '/home/z/my-project/scripts')
from s36_t1_trace import Emu

NM = '/tmp/my-project/work/TDKR_assets/raw/game_config/GothamCity_502299_navdata.nm'
nm = open(NM, 'rb').read()
emu = Emu()
emu.load_nm(nm)
st = emu.run_create()
mu = emu.mu
f = emu.dump()
soup_p, cells_p, grid_p = f['f14_soup'], f['f18_cells'], f['f64_grid']
vcount, ccount = f['f08_vcount'], f['f0c_ccount']

# soup value-compare (file BE f32 vs mem LE f32)
soup_mem = bytes(mu.mem_read(soup_p, vcount * 12))
mism = 0
for i in range(vcount):
    x, y, z = struct.unpack_from('<3f', soup_mem, i * 12)
    xf, yf, zf = struct.unpack_from('>3f', nm, 2 + i * 12)
    if not (x == xf and y == yf and z == zf):
        mism += 1
        if mism <= 2: print('soup diff at', i, (x, y, z), (xf, yf, zf))
print(f'soup value-identical: {vcount - mism}/{vcount}')

# cells: file 15-B BE vs mem 16-B LE
cells_mem = bytes(mu.mem_read(cells_p, ccount * 16))
cs = 2 + vcount * 12 + 4
bad = 0
regions = {}
links = 0
for i in range(ccount):
    v0, v1, v2, n0, n1, n2 = struct.unpack_from('<6H', cells_mem, i * 16)
    reg, ch = struct.unpack_from('<H', cells_mem, i * 16 + 12)[0], cells_mem[i * 16 + 14]
    n0s = n0 - 0x10000 if n0 > 0x7FFF else n0
    n1s = n1 - 0x10000 if n1 > 0x7FFF else n1
    n2s = n2 - 0x10000 if n2 > 0x7FFF else n2
    s = nm[cs + i * 15: cs + i * 15 + 15]
    fv = struct.unpack_from('>6H', s, 0)
    freg = struct.unpack_from('>H', s, 12)[0]
    fch = s[14]
    # file n* are BE s16
    fn = []
    for k in range(3):
        w = struct.unpack_from('>H', s, 6 + 2 * k)[0]
        fn.append(w - 0x10000 if w > 0x7FFF else w)
    memv = (v0, v1, v2)
    memn = (n0s, n1s, n2s)
    if memv != fv[:3] or memn != tuple(fn) or reg != freg or ch != fch:
        bad += 1
        if bad <= 2:
            print('cell diff', i, memv, memn, reg, ch, '|', fv[:3], fn, freg, fch)
    regions[freg] = regions.get(freg, 0) + 1
    links += sum(1 for n in (n0s, n1s, n2s) if n >= 0)
print(f'cells identical (engine BE parse): {ccount - bad}/{ccount}, bad={bad}')
print(f'distinct regions={len(regions)}, total directed links={links}')

# full nova dump
nova = emu.nova
nb = bytes(mu.mem_read(nova, 0x68))
words = struct.unpack('<26I', nb)
print('nova full:', ' '.join(f'{w:08x}' for w in words))
print('nova+0x5c (region-pair tbl ptr) =', hex(words[23]), ' +0x60 count =', words[24])

# BatCave control
NM2 = '/tmp/my-project/work/TDKR_assets/raw/game_config/BatCave_313590_navdata.nm'
nm2 = open(NM2, 'rb').read()
emu2 = Emu()
emu2.load_nm(nm2)
st2 = emu2.run_create()
mu2 = emu2.mu
f2 = emu2.dump()
if emu2.stream_obj:
    cur2 = struct.unpack('<I', mu2.mem_read(emu2.stream_obj + 0xC, 4))[0]
    print(f'BatCave: status={st2} cursor={cur2}/{len(nm2)} vcount={f2["f08_vcount"]} ccount={f2["f0c_ccount"]} X={f2["f10_X"]}')
    cells2 = bytes(mu2.mem_read(f2['f18_cells'], f2['f0c_ccount'] * 16))
    regs2 = set()
    l2 = 0
    for i in range(f2['f0c_ccount']):
        regs2.add(struct.unpack_from('<H', cells2, i * 16 + 12)[0])
        for k in range(3):
            w = struct.unpack_from('<H', cells2, i * 16 + 6 + 2 * k)[0]
            if w != 0xFFFF: l2 += 1
    print(f'BatCave distinct regions={len(regs2)} (engine X field={f2["f10_X"]}), links={l2}')
json.dump({'gotham': {'vcount': vcount, 'ccount': ccount, 'regions': len(regions), 'links': links,
                      'cells_bad': bad, 'soup_mism': mism, 'nova_5c': hex(words[23]), 'nova_60': words[24]}},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session36_t1_verify.json', 'w'), indent=1)
