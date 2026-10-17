#!/usr/bin/env python3
"""S30 T4 (v3): export GothamCity collision soup via lvc_pure.parse census.
parse() returns census[ctid] = (rid, cstart, size) per component; collision
components are re-read locally; TRS from the same record's CComponentBase."""
import json, struct, sys, math

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

TAB = '/tmp/my-project/work/re29/lvc_readseq_s30.json'
GOL = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json'
OUT_BIN = '/tmp/my-project/work/TDKR-Game/extraction/prototype/gc_collision.bin'

C_BASE = 1362553
C_COLL = 766542306

tab = json.load(open(TAB))
templates = {int(k, 16): v for k, v in json.load(open(GOL))['templates'].items()}
LV = '/tmp/my-project/work/data/GothamCity.lvc'
res = lvc_pure.parse(LV, tab, templates, None)
d, strings = res['data'], res['strings']

# record tid per rid
tid_of = {rid: tid for rid, start, tid, end, kind in res['records']}

# component spans
coll_spans = res['census'].get(str(C_COLL), [])
base_spans = {rid: (int(off, 16), sz) for rid, off, sz in
              res['census'].get(str(C_BASE), [])}
print(f'collision comps {len(coll_spans)}, base comps {len(base_spans)}')


def euler_to_m(rx, ry, rz):
    cx, sx = math.cos(rx), math.sin(rx)
    cy, sy = math.cos(ry), math.sin(ry)
    cz, sz = math.cos(rz), math.sin(rz)
    return (cz*cy, cz*sy*sx - sz*cx, cz*sy*cx + sz*sx,
            sz*cy, sz*sy*sx + cz*cx, sz*sy*cx - cz*sx,
            -sy,   cy*sx,            cy*cx)


def parse_collision(buf, off, strings):
    """Re-walk one collision component: [c][c][STR][i][c][c][i][c]
    + prims: [STR][i n] + n x ([f x9][c]) ... + [i] tail."""
    r = lvc_pure.Reader(buf, strings)
    r.p = off
    toks = []
    r.tok('c', out=toks); r.tok('c', out=toks)
    r.tok('STR', out=toks)
    r.tok('i', out=toks)
    r.tok('c', out=toks); r.tok('c', out=toks)
    r.tok('i', out=toks)
    r.tok('c', out=toks)
    prims = []
    # prims loop: count = last scalar (the [i] before [c]... the spec:
    # [c] prim count then rep last [ [STR][i] + rep last [f9, c] ] + [i] tail
    # follow the actual spec:
    spec = tab['components'][str(C_COLL)]
    # replay with token capture to segment
    toks2 = []
    r.p = off
    lvc_pure.replay(spec, r, toks2)
    # segment: STR (prim name) -> next i = tri count -> next (cnt*9) f + cnt c
    j = 0
    n = len(toks2)
    while j < n:
        if toks2[j][0] == 'STR':
            pname = toks2[j][3]
            k = j + 1
            while k < n and toks2[k][0] != 'i':
                k += 1
            cnt = toks2[k][3] if k < n else 0
            fl = [t[3] for t in toks2[k+1:] if t[0] == 'f']
            bl = [t[3] for t in toks2[k+1:] if t[0] == 'c']
            tris = [(fl[m*9:(m+1)*9], bl[m] if m < len(bl) else 0)
                    for m in range(cnt) if len(fl) >= (m+1)*9]
            prims.append((pname, tris))
            j = k + 1 + cnt * 10
        else:
            j += 1
    return prims


objects = []
ntris = 0
for rid, coff, csz in coll_spans:
    coff = int(coff, 16)
    tid = tid_of.get(rid)
    trs = None
    if rid in base_spans:
        boff, bsz = base_spans[rid]
        # CComponentBase tokens: [c][i] + 9f + c,c,c
        rr = lvc_pure.Reader(d, strings)
        rr.p = boff
        bt = []
        try:
            rr.tok('c', out=bt); rr.tok('i', out=bt)
            for _ in range(9):
                rr.tok('f', out=bt)
            rr.tok('c', out=bt); rr.tok('c', out=bt); rr.tok('c', out=bt)
            trs = [t[3] for t in bt if t[0] == 'f']
        except Exception:
            trs = None
    prims = parse_collision(d, coff, strings)
    n = sum(len(t) for _, t in prims)
    ntris += n
    objects.append(dict(rid=rid, tid=tid, trs=trs, prims=prims, ntri=n))

print(f'objects with collision: {len(objects)}, triangles {ntris}')
nnull = sum(1 for o in objects if o['trs'] is None)
print(f'objects without TRS: {nnull}')

# write binary
out = bytearray(b'TCS1')
out += struct.pack('<II', ntris, len(objects))
nameblob = bytearray()
nrec = bytearray()
trirec = bytearray()
oid = 0
for o in objects:
    nm = o['prims'][0][0].encode('latin1', 'replace')[:100] if o['prims'] else b'?'
    name_off = len(nameblob)
    nameblob += nm
    trs = o['trs'] or [0.0]*9
    nrec += struct.pack('<IHHI', name_off, len(nm), oid, o['ntri'])
    nrec += struct.pack('<9f', *trs)
    if o['trs']:
        m = euler_to_m(trs[3], trs[4], trs[5])
    for pname, tris in o['prims']:
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
    oid += 1
out += struct.pack('<I', len(nameblob)) + nameblob + nrec + trirec
open(OUT_BIN, 'wb').write(bytes(out))
print(f'wrote {OUT_BIN}: {len(out)/1e6:.1f} MB')
json.dump([dict(rid=o['rid'], tid=hex(o['tid']) if o['tid'] else None,
                ntri=o['ntri'], trs=o['trs'],
                name=o['prims'][0][0] if o['prims'] else None)
           for o in objects[:40]], open('/tmp/s30_t4_sample.json', 'w'), indent=1)
