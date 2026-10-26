#!/usr/bin/env python3
"""S62 T1: dump raw payloads of templates containing a given component id."""
import struct, json, sys

GOL = '/home/z/my-project/work/data/gol.bin'
d = open(GOL, 'rb').read()
table_off = struct.unpack_from('>I', d, 4)[0]
nrec = struct.unpack_from('>I', d, 13)[0]
offs = [struct.unpack_from('>I', d, 17 + 4 * i)[0] for i in range(nrec)]
pos = table_off
nstr = struct.unpack_from('>i', d, pos)[0]; pos += 4
strings = []
for _ in range(nstr):
    l = struct.unpack_from('>i', d, pos)[0]; pos += 4
    strings.append(d[pos:pos + l].decode('latin1')); pos += l

target = int(sys.argv[1], 16) if len(sys.argv) > 1 else 0x59a8390c
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 6

recs = []
for k in range(nrec):
    ro = offs[k]
    oid = struct.unpack_from('>I', d, ro)[0]
    m = struct.unpack_from('>I', d, ro + 4)[0]
    p = ro + 8 + 4 * m
    n = struct.unpack_from('>H', d, p)[0]
    nameidx = struct.unpack_from('>I', d, p + 2)[0]
    nxt = offs[k + 1] if k + 1 < nrec else len(d)
    payload = d[p + 6 + 6 * n:nxt]
    comps = [struct.unpack_from('>I', d, p + 6 + 6 * ci)[0] for ci in range(n)]
    recs.append((oid, strings[nameidx] if nameidx < len(strings) else '?', comps, payload))

shown = 0
for oid, name, comps, payload in recs:
    if target in comps:
        print(f'{name:32s} oid={oid:08x} len={len(payload):4d} comps={[hex(c) for c in comps]}')
        print('  hex:', payload[:48].hex(' '))
        # interpret as i,i,STR
        if len(payload) >= 12:
            i1, i2 = struct.unpack_from('>ii', payload, 0)
            slen = struct.unpack_from('>i', payload, 8)[0]
            s = payload[12:12 + slen] if 0 <= slen < 64 else b'<bad>'
            print(f'  as i,i,len+str: {i1}, {i2}, slen={slen} str={s!r} rest={payload[12+len(s):].hex(" ") if 0<=slen<64 else ""}')
        shown += 1
        if shown >= limit:
            break
print(f'(showing {shown} of templates containing {target:#x})')
