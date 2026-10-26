#!/usr/bin/env python3
"""S62 T1: full record dump with manual layout for one template."""
import struct, sys

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

target_name = sys.argv[1] if len(sys.argv) > 1 else 'C4_Explosive'
idx = strings.index(target_name)
for k in range(nrec):
    ro = offs[k]
    oid = struct.unpack_from('>I', d, ro)[0]
    m = struct.unpack_from('>I', d, ro + 4)[0]
    p = ro + 8 + 4 * m
    n = struct.unpack_from('>H', d, p)[0]
    nameidx = struct.unpack_from('>I', d, p + 2)[0]
    if nameidx != idx:
        continue
    nxt = offs[k + 1] if k + 1 < nrec else len(d)
    print(f'RECORD {target_name}: ro={ro:#x} oid={oid:#x} m={m} p={p:#x} n={n} nxt={nxt:#x} payload={nxt-(p+6+6*n)} B')
    print('refs:', [struct.unpack_from('>I', d, ro + 8 + 4 * i)[0] for i in range(m)])
    for ci in range(n):
        cid = struct.unpack_from('>I', d, p + 6 + 6 * ci)[0]
        fl = struct.unpack_from('>H', d, p + 10 + 6 * ci)[0]
        print(f'  comp[{ci}] id={cid:#010x} flag={fl}')
    ps = p + 6 + 6 * n
    pay = d[ps:nxt]
    print(f'payload @{ps:#x} len {len(pay)}:')
    for i in range(0, len(pay), 16):
        print(f'  {i:4d}: ' + pay[i:i+16].hex(' '))
    # manual walk with engine-verified specs
    print('manual walk (engine-verified sequences):')
    q = 0
    def show(label, nbytes):
        nonlocal_q = None
    SEQ = [('CBase', ['c','i'] + ['f']*10 + ['c','c','c']),
           ('CMesh', ['STR','c','c','c','c']),
           ('BeastComponent', ['f']*4 + ['STR'] + ['f']*4 + ['STR']),
           ('BeastGlobal', ['i','i','STR'])]
    NAT = {'i':4,'f':4,'c':1,'STR':4}
    for cname, seq in SEQ:
        vals = []
        start = q
        try:
            for t in seq:
                sz = NAT[t]
                if q + sz > len(pay):
                    vals.append(f'<OOB {t}@{q}>')
                    q = len(pay)
                    break
                if t == 'i':
                    vals.append(struct.unpack_from('>i', pay, q)[0])
                elif t == 'f':
                    vals.append(round(struct.unpack_from('>f', pay, q)[0], 4))
                elif t == 'c':
                    vals.append(pay[q])
                else:
                    si = struct.unpack_from('>i', pay, q)[0]
                    vals.append(f'STR[{si}]=' + (strings[si] if 0 <= si < len(strings) else '<OOB>'))
                q += sz
        except Exception as e:
            vals.append(f'<ERR {e}>')
            break
        print(f'  {cname:15s} @{start:3d}..{q:3d}: {vals}')
    print(f'  walked to q={q}, payload len={len(pay)}')
    break
