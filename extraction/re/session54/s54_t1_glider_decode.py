#!/usr/bin/env python3
"""s54 T1 step 26: decode the glide parameters from the gol.bin 'Glider'
(0x2674) and 'Glider_Plunge' (0x4c741) template payloads.

Reload flow (verified in disasm): for every template record, every component
(flag 0 or 1) is created via GenerateComponentTemplate(cid, stream) with the
stream positioned at the record's template-payload region; the component's
Load() reads its values THERE. Flag only controls lvc-record override.

CComponentGlide::Load = ReadInt + 22xReadFloat + ReadInt (ARM-verified).
CComponentGrapplingGun (0xdd583de) params precede it in the payload.
"""
import struct
import json

GOL = '/tmp/my-project/work/data/gol.bin'
d = open(GOL, 'rb').read()
table_off = struct.unpack_from('>I', d, 4)[0]
nrec = struct.unpack_from('>I', d, 13)[0]
offs = [struct.unpack_from('>I', d, 17 + 4 * i)[0] for i in range(nrec)]

# string table
pos = table_off
nstr = struct.unpack_from('>i', d, pos)[0]; pos += 4
strings = []
for i in range(nstr):
    ln = struct.unpack_from('>i', d, pos)[0]; pos += 4
    strings.append(d[pos:pos + ln].decode('utf-8', 'replace')); pos += ln

def parse_record(off):
    p = off
    oid = struct.unpack_from('>I', d, p)[0]; p += 4
    m = struct.unpack_from('>I', d, p)[0]; p += 4
    misc = [struct.unpack_from('>I', d, p + 4 * k)[0] for k in range(m)]
    p += 4 * m
    n = struct.unpack_from('>H', d, p)[0]; p += 2
    name_idx = struct.unpack_from('>I', d, p)[0]; p += 4
    name = strings[name_idx] if name_idx < len(strings) else '<idx %d>' % name_idx
    comps = []
    for j in range(n):
        tid = struct.unpack_from('>I', d, p)[0]
        fl = struct.unpack_from('>H', d, p + 4)[0]
        comps.append((tid, fl))
        p += 6
    return oid, misc, name, comps, p

# build offset -> next offset map
valid = sorted(o for o in offs if o != 0xFFFF and o < table_off)
nxt = {}
for a, b in zip(valid, valid[1:]):
    nxt[a] = b
nxt[valid[-1]] = table_off

for want in (0x2674, 0x4c741):
    off = None
    for o in valid:
        oid, misc, name, comps, p = parse_record(o)
        if oid == want:
            off = o
            break
    if off is None:
        print('template %#x not found' % want)
        continue
    oid, misc, name, comps, p = parse_record(off)
    payload = d[p:nxt[off]]
    print('\n=== %#x %r (payload %d B @%#x) ===' % (oid, name, len(payload), p))
    print('  comps:', [(hex(t), f) for t, f in comps])
    # hexdump
    for row in range(0, min(len(payload), 400), 16):
        chunk = payload[row:row + 16]
        hexs = ' '.join('%02x' % b for b in chunk)
        asci = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        print('    %04x  %-47s  %s' % (row, hexs, asci))
    # try: first component 0xdd583de, second 0x110ce1f
    # CComponentGlide = i + 22f + i = 92 bytes; try parsing the LAST 92 bytes
    if len(payload) >= 92:
        tail = payload[-92:]
        int1 = struct.unpack_from('>i', tail, 0)[0]
        fls = [round(struct.unpack_from('>f', tail, 4 + 4 * k)[0], 6) for k in range(22)]
        int2 = struct.unpack_from('>i', tail, 92 - 4)[0]
        print('  TAIL-as-glide: int1=%d int2=%d' % (int1, int2))
        for k, f in enumerate(fls):
            print('    f[%02d] (+%#03x) = %g' % (k, 8 + 4 * k, f))
