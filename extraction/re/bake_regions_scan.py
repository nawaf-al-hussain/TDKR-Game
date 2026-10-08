#!/usr/bin/env python3
"""Extract BeastBakeGroup-style payload: for every BakeGroup_*.tga string
reference in the zone object streams, decode the float group that follows
(the bake region / density) and the nearest bdae mesh name.
Validation across all records tells us the field semantics."""
import struct, json, re

def load(lvcname):
    d = open(f'/home/z/my-project/download/TDKR_assets/raw/game_config/{lvcname}.lvc', 'rb').read()
    tbl_off = struct.unpack_from('>I', d, 4)[0]
    p = tbl_off; cnt = struct.unpack_from('>I', d, p)[0]; p += 4
    strings = []
    for _ in range(cnt):
        ln = struct.unpack_from('>I', d, p)[0]; p += 4
        strings.append(d[p:p + ln].decode('utf-8', 'replace')); p += ln
    return d, tbl_off, cnt, strings

def bestr(d, o, cnt):
    v = struct.unpack_from('>I', d, o)[0]
    return v if 0 <= v < cnt else None

def scan(lvcname):
    d, tbl_off, cnt, strings = load(lvcname)
    bake_idx = {i for i, s in enumerate(strings) if s.startswith('BakeGroup')}
    bdae_idx = {i: s for i, s in enumerate(strings) if s.endswith('.bdae')}
    rows = []
    for bi in sorted(bake_idx):
        pat = struct.pack('>I', bi)
        o = 9
        while True:
            o = d.find(pat, o, tbl_off)
            if o < 0: break
            # floats following: 4 BE floats
            fl = [struct.unpack_from('>f', d, o + 4 + k * 4)[0] for k in range(4)]
            nxt = bestr(d, o + 20, cnt)
            # nearest bdae string within [-256, +64]
            near = []
            for q in range(max(9, o - 256), min(tbl_off - 4, o + 64)):
                v = bestr(d, q, cnt)
                if v in bdae_idx:
                    near.append((q - o, bdae_idx[v]))
            rows.append(dict(off=o, page=strings[bi], floats=fl,
                             nxt=strings[nxt] if nxt else None, near=near[:6]))
            o += 1
    return rows

for lv in ('GothamCity', 'GothamCity_Island2'):
    rows = scan(lv)
    print(f"===== {lv}: {len(rows)} BakeGroup refs")
    for r in rows:
        fl = ['%.5g' % v for v in r['floats']]
        print(f"  @{r['off']:#08x} {r['page']:<38} f=[{', '.join(fl)}]  next={r['nxt']!r}")
        for dq, s in r['near'][:4]:
            if 'collision' not in s and 'placeholder' not in s:
                print(f"        bdae({dq:+d}): {s}")
