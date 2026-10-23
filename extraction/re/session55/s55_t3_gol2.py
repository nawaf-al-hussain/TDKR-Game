#!/usr/bin/env python3
"""s55 T3 step 2: proper gol record parse (comps at p+6) — find templates carrying
CComponentGrapplingGun (comp id family *0dd583) and dump their payloads; verify the
glide block (0x0110ce1f) parses to s54's values; census 0xaae6a in lvc + scripts."""
import struct, json, os, importlib.util

GOL = '/tmp/my-project/work/data/gol.bin'
d = open(GOL, 'rb').read()
table_off = struct.unpack_from('>I', d, 4)[0]
nrec = struct.unpack_from('>I', d, 13)[0]
offs = [struct.unpack_from('>I', d, 17 + 4 * i)[0] for i in range(nrec)]
pos = table_off
nstr = struct.unpack_from('>i', d, pos)[0]; pos += 4
strings = []
for _ in range(nstr):
    l = struct.unpack_from('>i', d, pos)[0]; pos += 4
    strings.append(d[pos:pos + l].decode('utf-8', 'replace')); pos += l

out = {}
glide_check = {}
gun_records = []
target_records = []
for ri in range(nrec):
    ro = offs[ri]
    oid = struct.unpack_from('>I', d, ro)[0]
    m = struct.unpack_from('>I', d, ro + 4)[0]
    p = ro + 8 + 4 * m
    n = struct.unpack_from('>H', d, p)[0]
    nameidx = struct.unpack_from('>I', d, p + 2)[0]
    nm = strings[nameidx] if 0 <= nameidx < len(strings) else '?'
    nxt = offs[ri + 1] if ri + 1 < nrec else len(d)
    comps = []
    for ci in range(n):
        ct, fw = struct.unpack_from('>IH', d, p + 6 + 6 * ci)
        comps.append((ct, fw))
    ids = [c[0] for c in comps]
    if oid in (0x2674, 0x4c741, 0xaae6a) or any((i & 0xFFFFFFF) == 0x0dd583 or i == 0x0110ce1f for i in ids):
        q = p + 6 + 6 * n
        payload = d[q:nxt]
        rec = {'oid': hex(oid), 'name': nm, 'comps': [[hex(c[0]), c[1]] for c in comps],
               'payload_len': len(payload)}
        # payload floats BE starting after a u16 marker
        fl = []
        for o4 in range(0, min(len(payload), 200) - 3, 4):
            fl.append(round(struct.unpack_from('>f', payload, o4)[0], 4))
        rec['payload_be_f32_aligned'] = fl[:40]
        rec['payload_hex'] = payload[:128].hex()
        key = nm if nm != '?' else hex(oid)
        if (oid & 0xFFFFFFFF) in (0x2674, 0x4c741) or any(i == 0x0110ce1f for i in ids):
            glide_check[key] = rec
        if any((i & 0xFFFFFFF) == 0x0dd583 for i in ids):
            gun_records.append(rec)
        if oid == 0xaae6a:
            target_records.append(rec)

print('=== glide-component templates ===')
print(json.dumps(glide_check, indent=1)[:4000])
print('\n=== grappling-gun-component templates ===')
print(json.dumps(gun_records, indent=1)[:4000])
print('\n=== 0xaae6a (Enemy_Grapnel_Target) ===')
print(json.dumps(target_records, indent=1)[:2500])
json.dump({'glide': glide_check, 'gun': gun_records, 'target': target_records},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session55/s55_t3_gol_dump.json', 'w'), indent=1)
