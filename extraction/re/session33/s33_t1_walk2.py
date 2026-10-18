#!/usr/bin/env python3
"""S33 T1 final v2: re-anchoring walk + pose test."""
import struct, math, json
import numpy as np

AD = '/tmp/my-project/work/data/batman_anims.bdae'
MD = '/tmp/my-project/work/data/batman.bdae'
ad = open(AD, 'rb').read()
md = open(MD, 'rb').read()
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]
f32a = lambda o: struct.unpack_from('<f', ad, o)[0]
u32m = lambda o: struct.unpack_from('<I', md, o)[0]

def cstr_a(v):
    if 0 < v < len(ad):
        e = ad.find(b'\0', v)
        if 0 < e - v < 90:
            try: return ad[v:e].decode('latin1')
            except Exception: pass

names = []
o = 0xb53c
while True:
    w = struct.unpack_from('<8I', ad, o)
    if not (w[2] and cstr_a(w[2]) and w[3] == 1 and w[5] == 1): break
    names.append(cstr_a(w[2]))
    o += 32
pairs = [(u32a(0x53200 + 8 * k), u32a(0x53200 + 8 * k + 4)) for k in range(156)]

def ticks_asc(p, n):
    w = [u32a(p + 4 * j) for j in range(n)]
    return all(w[i] < w[i + 1] for i in range(n - 1)) and w[-1] < 2_000_000

def quats_unit(p, n):
    bad = 0
    for i in range(n):
        q = [f32a(p + 16 * i + 4 * c) for c in range(4)]
        s = sum(x * x for x in q)
        if not (math.isfinite(s) and abs(math.sqrt(s) - 1) < 5e-3):
            bad += 1
    return bad <= max(1, n // 20)

def vecs_finite(p, n):
    return all(math.isfinite(f32a(p + 4 * i)) and abs(f32a(p + 4 * i)) < 100
               for i in range(3 * n))

chans = {}
placements = []
pos = 0x536e8
for k, (off, ln) in enumerate(pairs):
    nm = names[k // 2] if k // 2 < len(names) else f'?{k}'
    bare = nm.split('-node-')[0]
    track = nm.split('-node-')[1] if '-node-' in nm else '?'
    is_time = (k % 2 == 0)
    n_iter = ln // 4 if is_time else (ln // 16 if (ln % 16 == 0 and ln >= 0x20)
                                      else ln // 12)
    placed = None
    # pass 1: shape test with pads 0..32
    for pad in range(0, 40, 4):
        p = pos + pad
        if p + ln > len(ad): break
        if ln == 0: placed = p; break
        if is_time and ticks_asc(p, n_iter): placed = p; break
        if (not is_time) and ln % 16 == 0 and ln >= 0x20 and quats_unit(p, n_iter):
            placed = p; break
        if (not is_time) and ln % 12 == 0 and ln >= 0x18 and 0x20 > ln and vecs_finite(p, n_iter):
            placed = p; break
        if (not is_time) and ln % 12 == 0 and ln >= 0x18 and vecs_finite(p, n_iter) and \
           ln % 16 != 0:
            placed = p; break
    # pass 2 (re-anchor): for TIME streams, find an ascending n_iter-tick array
    if placed is None and is_time and ln >= 8:
        for pad in range(0, 512, 4):
            p = pos + pad
            if p + ln > len(ad): break
            if ticks_asc(p, n_iter): placed = p; break
    if placed is None and (not is_time) and ln % 16 == 0 and ln >= 0x20:
        for pad in range(0, 512, 4):
            p = pos + pad
            if p + ln > len(ad): break
            if quats_unit(p, n_iter): placed = p; break
    if placed is None:
        placements.append((nm, None, ln))
        continue
    key = 'time' if is_time else track
    ent = chans.setdefault(bare, {})
    ent[key] = dict(off=placed, len=ln, n=n_iter)
    placements.append((nm, placed, ln))
    pos = placed + ln

bad = [(nm, ln) for nm, p, ln in placements if p is None]
print(f'walk: {len(placements) - len(bad)}/{len(placements)} placed; end 0x{pos:x}')
for nm, p, ln in placements:
    if p is None or not nm.startswith('Bip01_CBone'):
        print(f'  {nm:42s} {"UNPLACED" if p is None else hex(p):9s} len 0x{ln:x}')

# tick spans of key body bones
print('\nbody channels:')
for nm in ('Bip01', 'Bip01_Pelvis', 'Bip01_Spine', 'Bip01_Spine1', 'Bip01_Neck',
           'Bip01_Head', 'Bip01_L_Thigh', 'Bip01_L_Calf', 'Bip01_L_Foot',
           'Bip01_R_Thigh', 'Bip01_R_Calf', 'Bip01_R_Foot',
           'Bip01_L_Clavicle', 'Bip01_L_UpperArm', 'Bip01_L_Forearm', 'Bip01_L_Hand',
           'Bip01_R_Clavicle', 'Bip01_R_UpperArm', 'Bip01_R_Forearm', 'Bip01_R_Hand'):
    if nm in chans:
        d = {}
        for kk, v in chans[nm].items():
            if kk == 'time':
                d['t'] = f'[{u32a(v["off"])}..{u32a(v["off"] + 4 * v["n"] - 4)}]x{v["n"]}'
            else:
                d[kk] = v['n']
        print(f'  {nm:22s} {d}')

json.dump({nm: {k: v for k, v in ch.items()} for nm, ch in chans.items()},
          open('/tmp/my-project/scripts/s33_t1_chans.json', 'w'), indent=0)
print('saved chans')
