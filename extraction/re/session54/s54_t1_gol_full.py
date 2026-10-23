#!/usr/bin/env python3
"""s54 T1 step 4: full gol.bin record dump including flag!=0 template data.

Layout (from s24 parse_gol.py, extended):
  'DICT' | u32be tableOffset | u8 | u16be tag | u16be ver | u32be NREC
  | NREC x u32be recordOffset
  per record:
    u32be objectId | u32be m | m x u32be misc
    u16be n | u32be nameIdx | n x (u32be compTypeId, u16be flagword)
    template data (flag!=0 payloads) until next record offset
"""
import struct, json, sys

GOL = '/tmp/my-project/work/data/gol.bin'
d = open(GOL, 'rb').read()
assert d[:4] == b'DICT'
table_off = struct.unpack_from('>I', d, 4)[0]
nrec = struct.unpack_from('>I', d, 13)[0]
offs = [struct.unpack_from('>I', d, 17 + 4 * i)[0] for i in range(nrec)]
print('table@%#x nrec=%d' % (table_off, nrec))

# string table
strings = []
pos = table_off
nstr = struct.unpack_from('>i', d, pos)[0]; pos += 4
for i in range(nstr):
    ln = struct.unpack_from('>i', d, pos)[0]; pos += 4
    strings.append(d[pos:pos + ln].decode('utf-8', 'replace')); pos += ln
print('strings:', nstr)

def parse_record(off, next_off):
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
    payload = d[p:next_off]
    return dict(oid=oid, misc=misc, name=name, comps=comps,
                payload=payload, payload_off=p)

# find record for target template ids
targets = {0x7990: 'Glide', 0xaae6a: 'Enemy_Grapnel_Target',
           0x4c6f1: 'Batman', 0x4c6f3: 'Batman_02_Flying'}
records = {}
for i, off in enumerate(offs):
    if off == 0xFFFF or off >= table_off:
        continue
    nxt = table_off
    for o2 in sorted(set(x for x in offs if off < x < table_off)):
        nxt = o2
        break
    r = parse_record(off, nxt)
    records[r['oid']] = r

for tid, nm in targets.items():
    r = records.get(tid)
    if not r:
        print('template %#x (%s) NOT FOUND' % (tid, nm))
        continue
    print('\n=== %#x %r ===' % (tid, r['name']))
    print('  misc (%d):' % len(r['misc']), [hex(x) for x in r['misc'][:8]])
    print('  comps:', [(hex(t), f) for t, f in r['comps']])
    print('  payload: %d bytes @%#x' % (len(r['payload']), r['payload_off']))
    pl = r['payload']
    # hexdump first 256 bytes
    for row in range(0, min(len(pl), 256), 16):
        chunk = pl[row:row + 16]
        hexs = ' '.join('%02x' % b for b in chunk)
        asci = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        print('    %04x  %-47s  %s' % (row, hexs, asci))
