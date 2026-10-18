#!/usr/bin/env python3
"""S34 T1: locate _008_run data block (sequential validation like idle) and
decode. Report keys/channel, loop wrap, validation battery with nulls."""
import struct, json, math
import numpy as np

AD = '/tmp/my-project/work/data/batman_anims.bdae'
ad = open(AD, 'rb').read()
u32a = lambda o: struct.unpack_from('<I', ad, o)[0]
f32a = lambda o: struct.unpack_from('<f', ad, o)[0]
N = len(ad)

T = 0x204bb70
NE = 156
pairs = [(u32a(T + 8*k), u32a(T + 8*k + 4)) for k in range(NE)]
names = None
# channel names: find the 32-B name group near the table (like idle @0xb53c for
# the 0x53200 table). The name group precedes/follows; scan window before table.
def cstr(v):
    if 0 < v < N:
        e = ad.find(b'\0', v)
        if 0 < e - v < 90:
            try: return ad[v:e].decode('latin1')
            except Exception: return None

names = []
for probe in range(T - 0x8000, T + 0x8000, 4):
    w = struct.unpack_from('<8I', ad, probe)
    if w[2] and w[3] == 1 and w[5] == 1 and cstr(w[2]) and '-node-' in (cstr(w[2]) or ''):
        # check next entry too
        w2 = struct.unpack_from('<8I', ad, probe + 32)
        if w2[2] and w2[3] == 1 and w2[5] == 1 and cstr(w2[2]) and '-node-' in (cstr(w2[2]) or ''):
            nm = cstr(w[2])
            names.append((probe, nm))
if names:
    print(f'name group starts @0x{names[0][0]:06x}: {names[0][1]}')
    base = names[0][0]
    nlist = []
    o = base
    while True:
        w = struct.unpack_from('<8I', ad, o)
        if not (w[2] and w[3] == 1 and w[5] == 1 and cstr(w[2])): break
        nlist.append(cstr(w[2])); o += 32
    print(f'{len(nlist)} names, first 4: {nlist[:4]}, last 2: {nlist[-2:]}')
else:
    nlist = []
    print('no name group found near table')

# locate data: scan bases, full sequential validation
def validate(base):
    pos = base
    ok = 0
    for k, (off, ln) in enumerate(pairs):
        if ln == 0: continue
        is_time = (k % 2 == 0)
        if is_time:
            n = ln // 4
            w = [u32a(pos + 4*j) for j in range(n)]
            if not all(w[i] < w[i+1] for i in range(n-1)) or w[-1] >= 2_000_000:
                return ok, pos
        else:
            if ln % 16 == 0 and ln >= 0x20:
                m = ln // 16
                for i in range(m):
                    q = [f32a(pos + 16*i + 4*c) for c in range(4)]
                    nr = math.sqrt(sum(x*x for x in q))
                    if not (0.95 < nr < 1.05): return ok, pos
            elif ln % 12 == 0:
                m = ln // 12
                for i in range(m):
                    v = [f32a(pos + 12*i + 4*c) for c in range(3)]
                    if max(abs(x) for x in v) > 1e5: return ok, pos
            else: return ok, pos
        ok += 1
        pos += ln
    return ok, pos

best = None
for base in range(T + NE*8, T + NE*8 + 0x2000, 4):
    ok, end = validate(base)
    if best is None or ok > best[1]:
        best = (base, ok, end)
    if ok == NE: break
print(f'\nbest base: 0x{best[0]:06x} validated {best[1]}/{NE}, end 0x{best[2]:06x}')
json.dump(dict(table=T, base=best[0], end=best[2], npairs=NE,
               names=nlist, pairs=pairs),
          open('/home/z/my-project/scripts/s34_t1_runloc.json', 'w'))
