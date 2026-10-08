#!/usr/bin/env python3
"""Cluster zone-object-stream string references (bdae names + BakeGroup pages).
Efficient: single pass building the u32 histogram? No — scan each target index's
byte pattern with find(). BE u32 refs only; ALSO count LE."""
import struct, sys, re

def analyze(lvcname):
    d = open(f'/home/z/my-project/download/TDKR_assets/raw/game_config/{lvcname}.lvc', 'rb').read()
    tbl_off = struct.unpack_from('>I', d, 4)[0]
    p = tbl_off; cnt = struct.unpack_from('>I', d, p)[0]; p += 4
    strings = []
    for _ in range(cnt):
        ln = struct.unpack_from('>I', d, p)[0]; p += 4
        strings.append(d[p:p + ln].decode('utf-8', 'replace')); p += ln
    targets = {}
    for i, s in enumerate(strings):
        if s.endswith('.bdae') or s.startswith('BakeGroup'):
            targets[i] = s
    print(f"=== {lvcname}: {cnt} strings, {len(targets)} bdae/BakeGroup targets")
    refs = []
    for i, s in targets.items():
        pat = struct.pack('>I', i)
        o = 9
        while True:
            o = d.find(pat, o, tbl_off)
            if o < 0: break
            refs.append((o, i, s)); o += 1
    refs.sort()
    print(f"  {len(refs)} BE u32 refs in stream")
    clusters = []
    cur = []
    for q in refs:
        if cur and q[0] - cur[-1][0] > 260:
            clusters.append(cur); cur = []
        cur.append(q)
    if cur: clusters.append(cur)
    print(f"  {len(clusters)} clusters")
    out = []
    for cl in clusters:
        bdaes = [(q, s) for q, v, s in cl if s.endswith('.bdae') and 'collision' not in s]
        cols = [(q, s) for q, v, s in cl if 'collision' in s]
        bakes = [(q, s) for q, v, s in cl if s.startswith('BakeGroup')]
        if bakes:
            out.append(dict(lo=cl[0][0], hi=cl[-1][0], bdae=bdaes, col=cols, bake=bakes))
    for r in out:
        print(f"  [{r['lo']:#x}-{r['hi']:#x}] bdae={[s for _, s in r['bdae']][:3]} "
              f"bake={[s for _, s in r['bake']][:4]} col={[s.split('_collision')[0] for _, s in r['col']][:2]}")
    return d, strings, out

if __name__ == '__main__':
    for lv in ('GothamCity', 'GothamCity_Island2'):
        analyze(lv)
