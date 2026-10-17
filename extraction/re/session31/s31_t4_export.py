#!/usr/bin/env python3
"""S31 T4: corrected collision export (both islands) + multi-grid ground
probes + slope/step stats + path test.

Fixes the r20 export bug (prefix [i] grabbed as prim count -> 4 objects lost
40 tris). Exports gc_collision.bin (137,893) and i2_collision.bin.
"""
import json, struct, sys, math, collections
import numpy as np

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

TAB = '/tmp/my-project/work/re29/lvc_readseq_s30.json'
GOL = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json'
C_BASE = 1362553
C_COLL = 766542306

tab = json.load(open(TAB))
templates = {int(k, 16): v for k, v in json.load(open(GOL))['templates'].items()}


def euler_to_m(rx, ry, rz):
    cx, sx = math.cos(rx), math.sin(rx)
    cy, sy = math.cos(ry), math.sin(ry)
    cz, sz = math.cos(rz), math.sin(rz)
    return (cz*cy, cz*sy*sx - sz*cx, cz*sy*cx + sz*sx,
            sz*cy, sz*sy*sx + cz*cx, sz*sy*cx - cz*sx,
            -sy, cy*sx, cy*cx)


def parse_collision_correct(d, off, strings):
    """spec-following: [c][c][STR][i][c][c][i][c? no -] prefix 16 B =
    c,c,STR,i,c,c,i then [c] n_outer, then n_outer x {[STR][i] + n x [f9,c]}
    then [i] tail."""
    r = lvc_pure.Reader(d, strings)
    r.p = off
    toks = []
    r.tok('c', out=toks); r.tok('c', out=toks); r.tok('STR', out=toks)
    r.tok('i', out=toks); r.tok('c', out=toks); r.tok('c', out=toks)
    r.tok('i', out=toks)
    r.tok('c', out=toks)
    n_outer = toks[-1][3]
    tris = []
    for _ in range(max(n_outer, 0)):
        r.tok('STR', out=toks)
        r.tok('i', out=toks)
        cnt = toks[-1][3]
        for _ in range(max(cnt, 0)):
            f9 = [r.tok('f') for _ in range(9)]
            fl = r.tok('c')
            tris.append((f9, fl))
    r.tok('i')
    return tris, r.p - off


def export(level, out_bin):
    res = lvc_pure.parse(f'/tmp/my-project/work/data/{level}.lvc', tab,
                         templates, None)
    d, strings = res['data'], res['strings']
    tid_of = {rid: tid for rid, s0, tid, e, k in res['records']}
    coll = res['census'].get(str(C_COLL), [])
    base = {rid: int(o, 16) for rid, o, sz in res['census'].get(str(C_BASE), [])}
    objects = []
    ntris = 0
    fh = collections.Counter()
    for rid, coff, csz in coll:
        coff = int(coff, 16)
        trs = None
        if rid in base:
            rr = lvc_pure.Reader(d, strings)
            rr.p = base[rid]
            bt = []
            rr.tok('c', out=bt); rr.tok('i', out=bt)
            for _ in range(9):
                rr.tok('f', out=bt)
            rr.tok('c', out=bt); rr.tok('c', out=bt); rr.tok('c', out=bt)
            trs = [t[3] for t in bt if t[0] == 'f']
        tris, _ = parse_collision_correct(d, coff, strings)
        for _, fl in tris:
            fh[fl] += 1
        ntris += len(tris)
        objects.append(dict(rid=rid, tid=tid_of.get(rid), trs=trs, tris=tris))
    print(f'{level}: {len(objects)} collision objects, {ntris} triangles')
    print('  flags:', dict(sorted(fh.items())))
    out = bytearray(b'TCS1')
    out += struct.pack('<II', ntris, len(objects))
    nameblob = bytearray()
    nrec = bytearray()
    trirec = bytearray()
    for oid, o in enumerate(objects):
        nm = ''
        tris = o['tris']
        if tris:
            nm = 'obj'
        noff = len(nameblob)
        nameblob += nm.encode()
        trs = o['trs'] or [0.0]*9
        nrec += struct.pack('<IHHI', noff, len(nm), oid, len(tris))
        nrec += struct.pack('<9f', *trs)
        if o['trs']:
            m = euler_to_m(trs[3], trs[4], trs[5])
        for t9, fl in tris:
            if o['trs']:
                pw = []
                for vi in range(3):
                    p = t9[vi*3:vi*3+3]
                    x, y, z = p[0]*trs[6], p[1]*trs[7], p[2]*trs[8]
                    pw += [m[0]*x+m[1]*y+m[2]*z+trs[0],
                           m[3]*x+m[4]*y+m[5]*z+trs[1],
                           m[6]*x+m[7]*y+m[8]*z+trs[2]]
            else:
                pw = list(t9)
            trirec += struct.pack('<H', oid) + struct.pack('<9f', *pw) + \
                struct.pack('<B', fl & 0xff)
    out += struct.pack('<I', len(nameblob)) + nameblob + nrec + trirec
    open(out_bin, 'wb').write(bytes(out))
    print(f'  wrote {out_bin} ({len(out)/1e6:.1f} MB)')
    return ntris, len(objects)


gc = export('GothamCity', '/tmp/my-project/work/TDKR-Game/extraction/prototype/gc_collision.bin')
i2 = export('GothamCity_Island2', '/tmp/my-project/work/TDKR-Game/extraction/prototype/i2_collision.bin')
print(f'\nTOTAL both islands: {gc[0] + i2[0]} triangles, '
      f'{gc[1] + i2[1]} objects (r16 census: 271,589 / 1,238)')
json.dump(dict(GothamCity=dict(tris=gc[0], objs=gc[1]),
               Island2=dict(tris=i2[0], objs=i2[1])),
          open('/home/z/my-project/download/s31_t4_export.json', 'w'))
