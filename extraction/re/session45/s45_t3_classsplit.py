#!/usr/bin/env python3
"""s45 T3a: class-split validation of the loose TRS population + the id bridge.

Step 1 — attribute every loose TRS record ([i32 id][9xf32] runs in the token
streams) to its enclosing COMPONENT CLASS via the parse census (record rid ->
components of that record -> tid whose [off,off+size) contains the record's
token offset).

Step 2 — per-class validation battery (V1 id, V2 in-AABB, V4 |rot|<=4,
V5 scale), flag classes whose rotation plausibility is at/below the null band,
drop them, rerun the population stats.

Step 3 — the id bridge: scripts (t1_lua_*.json: {off, objId, script}) act on
ids parsed from the Lua text; report coverage of those ids against (a) the
trigger records' own objIds, (b) the loose TRS population (positions).
"""
import json, struct, re, sys, math, collections
import numpy as np

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

TAB = '/tmp/my-project/work/re29/lvc_readseq_s30.json'
GOL = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json'
TOKS = {'island1': '/tmp/my-project/work/data/GothamCity.lvc.puretoks.json',
        'island2': '/tmp/my-project/work/data/GothamCity_Island2.lvc.puretoks.json'}
LVC = {'island1': '/tmp/my-project/work/data/GothamCity.lvc',
       'island2': '/tmp/my-project/work/data/GothamCity_Island2.lvc'}
COL = {'island1': '/tmp/my-project/work/TDKR-Game/extraction/prototype/gc_collision.bin',
       'island2': '/tmp/my-project/work/TDKR-Game/extraction/prototype/i2_collision.bin'}
LUAS = {'island1': '/tmp/my-project/work/t1_lua_GothamCity.json',
        'island2': '/tmp/my-project/work/t1_lua_GothamCity_Island2.json'}

tab = json.load(open(TAB))
templates = {int(k, 16): v for k, v in json.load(open(GOL))['templates'].items()}

out = {'classes': {}, 'bridge': {}, 'nulls': {}}
for isl in ('island1', 'island2'):
    toks = json.load(open(TOKS[isl]))
    res = lvc_pure.parse(LVC[isl], tab, templates, None)
    d, strings = res['data'], res['strings']
    # census -> per-record component spans [(tid, off, size)]
    rec_comps = collections.defaultdict(list)
    # census classes only, biggest first — avoids nested-component attribution
    cls_list = [(k, v) for k, v in res['census'].items()
                if k not in ('mesh', 'spawn') and len(v) >= 20]
    cls_list.sort(key=lambda x: -len(x[1]))
    for ks, lst in cls_list:
        tid = int(ks)
        for entry in lst:
            rid, off, size = entry[0], entry[1], entry[2]
            rec_comps[rid].append((tid, int(off, 16) if isinstance(off, str) else off, size))
    # soup AABB
    col = open(COL[isl], 'rb').read()
    ntri = struct.unpack_from('<I', col, 4)[0]
    nobj = struct.unpack_from('<I', col, 8)[0]
    nameLen = struct.unpack_from('<I', col, 12)[0]
    t0 = 16 + nameLen + nobj * 48
    tr = np.frombuffer(col, np.uint8, ntri * 39, t0).reshape(ntri, 39)
    P = tr[:, 2:38].copy().view('<f4').reshape(ntri, 3, 3).astype(np.float64)
    pts = P.reshape(-1, 3)
    mn, mx = pts.min(0) - 40, pts.max(0) + 40
    zmin = pts[:, 2].min() - 40
    # loose TRS scan with class attribution
    vals = [(t[0], t[1], t[-1]) for t in toks]  # (kind, off, value)
    icount = collections.Counter(v for ty, off, v in vals if ty == 'i' and isinstance(v, int) and 1 <= v <= 3_000_000)
    k = 0
    n = len(vals)
    class_recs = collections.defaultdict(list)
    unattributed = 0
    rid_bounds = sorted((r[0], r[1], r[2]) for r in res['records'])  # (rid, start, end)
    import bisect
    rec_starts = [r[1] for r in rid_bounds]
    while k < n - 9:
        ty, off, v = vals[k]
        if ty == 'i' and isinstance(v, int) and 1 <= v <= 3_000_000:
            f = [vals[k + 1 + j] for j in range(9)]
            if all(ft == 'f' and isinstance(fv, float) and math.isfinite(fv) for ft, off2, fv in f):
                pos = [f[0][2], f[1][2], f[2][2]]
                rot = [f[3][2], f[4][2], f[5][2]]
                scl = [f[6][2], f[7][2], f[8][2]]
                rid = rid_bounds[bisect.bisect_right(rec_starts, off) - 1][0]
                cls = None
                for (tid, coff, size) in rec_comps.get(rid, []):
                    if coff <= off < coff + size:
                        cls = tid
                        break
                if cls is None:
                    unattributed += 1
                else:
                    class_recs[cls].append(dict(id=v, pos=pos, rot=rot, scl=scl,
                                                resolves=bool(icount[v] > 1)))
                k += 10
                continue
        k += 1
    # per-class battery
    cls_stats = {}
    for cls, recs in sorted(class_recs.items(), key=lambda x: -len(x[1])):
        if len(recs) < 20:
            continue
        R = np.array([r['rot'] for r in recs])
        S = np.array([r['scl'] for r in recs])
        Pp = np.array([r['pos'] for r in recs])
        inb = ((Pp >= mn) & (Pp <= mx)).all(1)
        okrot = (np.abs(R) <= 4.0).all(1)
        okscl = ((S > 0) & (S <= 500)).all(1) & np.isfinite(S).all(1)
        okid = sum(1 for r in recs if r['resolves'])
        cls_stats[hex(cls)] = dict(
            n=len(recs), V1=okid, V2=int(inb.sum()), V4=int(okrot.sum()),
            V5=int(okscl.sum()),
            rot_frac=float(okrot.mean()), inb_frac=float(inb.mean()))
    out['classes'][isl] = dict(stats=cls_stats, unattributed=unattributed,
                               total=len(class_recs) and sum(len(v) for v in class_recs.values()))
    print(f'{isl}: attributed classes {len(cls_stats)} (>=20 recs), unattributed {unattributed}')
    for h, st in list(cls_stats.items())[:14]:
        print(f"  {h}: n={st['n']} V1={st['V1']} V2={st['V2']} V4={st['V4']} "
              f"V5={st['V5']} rot%={st['rot_frac']:.2f}")

json.dump(out, open('/home/z/my-project/scripts/s45_t3_classsplit.json', 'w'), indent=0, default=str)
print('saved s45_t3_classsplit.json')
