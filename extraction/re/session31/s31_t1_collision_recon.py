#!/usr/bin/env python3
"""S31 T1: reconcile collision counts r16 census (137,893) vs r20 export (137,853).

Correctly re-walks all GothamCity CCollisionComponents (following the spec:
prefix c,c,STR,i,c,c,i,c + n_outer=[c] + n_outer x {[STR][i] + n x [f9][c]}
+ [i] tail) and diffs per-object against the r20 gc_collision.bin counts.
Hypothesis: s30_t4_export3.parse_collision grabbed the PREFIX [i] as the
first prim's triangle count (first 'i' after the prefix STR), misframing
objects with prefix_i != 0.
"""
import json, struct, sys, collections

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

TAB = '/tmp/my-project/work/re29/lvc_readseq_s30.json'
GOL = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json'
BIN = '/tmp/my-project/work/TDKR-Game/extraction/prototype/gc_collision.bin'
C_BASE = 1362553
C_COLL = 766542306

tab = json.load(open(TAB))
templates = {int(k, 16): v for k, v in json.load(open(GOL))['templates'].items()}
res = lvc_pure.parse('/tmp/my-project/work/data/GothamCity.lvc', tab,
                     templates, None)
d, strings = res['data'], res['strings']
tid_of = {rid: tid for rid, start, tid, end, kind in res['records']}
coll_spans = res['census'].get(str(C_COLL), [])
base_spans = {rid: int(off, 16) for rid, off, sz in
              res['census'].get(str(C_BASE), [])}


def walk_correct(off):
    """Spec-following walk: returns (prefix_i, n_outer, prims, flags_hist)."""
    r = lvc_pure.Reader(d, strings)
    r.p = off
    t = []
    r.tok('c', out=t); r.tok('c', out=t); r.tok('STR', out=t)
    r.tok('i', out=t); r.tok('c', out=t); r.tok('c', out=t); r.tok('i', out=t)
    prefix_i = t[3]
    r.tok('c', out=t)                      # n_outer (may be signed-byte)
    n_outer = t[-1][3]
    prims = []
    fh = collections.Counter()
    for _ in range(max(n_outer, 0)):
        r.tok('STR', out=t)
        r.tok('i', out=t)
        cnt = t[-1][3]
        tris = []
        for _ in range(max(cnt, 0)):
            f9 = [r.tok('f') for _ in range(9)]
            fl = r.tok('c')
            tris.append((f9, fl))
            fh[fl] += 1
        prims.append((t[-2 - cnt * 10] if False else None, tris))
    r.tok('i')                             # tail
    end = r.p
    return prefix_i, n_outer, sum(len(p[1]) for p in prims), fh, end


# ---- r20 bin per-object ----
dd = open(BIN, 'rb').read()
ntris_b, nobj_b = struct.unpack_from('<II', dd, 4)
nbs = struct.unpack_from('<I', dd, 12)[0]
p = 16 + nbs
bin_objs = []
for i in range(nobj_b):
    noff, nlen, oid, ntri = struct.unpack_from('<IHHI', dd, p)
    bin_objs.append(dict(oid=oid, ntri=ntri,
                         name=dd[16 + noff:16 + noff + nlen].decode('latin1', 'replace')))
    p += 48

# ---- correct re-walk per object (file order == bin order) ----
total = 0
fh_all = collections.Counter()
diffs = []
rows = []
for i, (rid, coff, csz) in enumerate(coll_spans):
    coff = int(coff, 16)
    prefix_i, n_outer, ntri, fh, end = walk_correct(coff)
    total += ntri
    fh_all.update(fh)
    b = bin_objs[i] if i < len(bin_objs) else None
    if b is None or b['ntri'] != ntri:
        diffs.append(dict(idx=i, rid=rid, off=hex(coff), prefix_i=prefix_i,
                          n_outer=n_outer, correct_ntri=ntri,
                          bin_ntri=(b['ntri'] if b else None),
                          name=(b['name'] if b else None)))
    rows.append(dict(idx=i, rid=rid, off=hex(coff), prefix_i=prefix_i,
                     n_outer=n_outer, ntri=ntri, bin_ntri=b['ntri'],
                     name=(b['name'] if b else None)))

print(f'correct re-walk: objects {len(coll_spans)}, triangles {total}')
print(f'flag histogram (correct): {dict(sorted(fh_all.items()))}')
print(f'r20 bin total: {ntris_b}')
print(f'differing objects: {len(diffs)}')
for x in diffs[:20]:
    print('  ', x)
# check: is prefix_i != 0 exactly on the differing objects?
mism = [(r['idx'], r['prefix_i'], r['ntri'], r['bin_ntri'])
        for r in rows if r['ntri'] != r['bin_ntri']]
nonzero = [(r['idx'], r['prefix_i']) for r in rows if r['prefix_i'] != 0]
print(f'\nobjects with prefix_i != 0: {len(nonzero)}')
print(f'objects with count mismatch: {len(mism)}')
print('prefix_i values on mismatched:', sorted(set(m[1] for m in mism)))
# flag attribution diff
bin_fh = collections.Counter()
p2 = p
for i in range(nobj_b):
    pass
# recompute bin flag hist from trirec
trirec_off = 16 + nbs + nobj_b * 48
q = trirec_off
for i in range(ntris_b):
    oid = struct.unpack_from('<H', dd, q)[0]
    fl = dd[q + 38]
    bin_fh[fl] += 1
    q += 39
print('\nflag hist bin  :', dict(sorted(bin_fh.items())))
print('flag hist corr :', dict(sorted(fh_all.items())))
delta = {k: fh_all[k] - bin_fh.get(k, 0) for k in set(fh_all) | set(bin_fh)
         if fh_all[k] != bin_fh.get(k, 0)}
print('delta (corr - bin):', delta)

json.dump(dict(correct_total=total, bin_total=ntris_b,
               flag_correct=dict(fh_all), flag_bin=dict(bin_fh),
               diffs=diffs),
          open('/home/z/my-project/download/s31_t1_collision_recon.json', 'w'),
          indent=1)
print('\nwrote /home/z/my-project/download/s31_t1_collision_recon.json')
