#!/usr/bin/env python3
"""S32 T3a: triggers — identify the trigger census class, extract all records
with owner TRS, disasm CComponentTrigger::IsObjectInside, compute world
volumes + extents distribution, verify a known spawn."""
import sys, json, struct, math, collections
import numpy as np

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

TAB = '/tmp/my-project/work/re29/lvc_readseq_s30.json'
GOL = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json'
templates = {int(k, 16): v for k, v in json.load(open(GOL))['templates'].items()}
tab = json.load(open(TAB))
res = lvc_pure.parse("/tmp/my-project/work/data/GothamCity.lvc", tab,
                     templates, None)
d, strings = res['data'], res['strings']
tid_of = {rid: tid for rid, s0, tid, e, k in res['records']}
base = {rid: int(o, 16) for rid, o, sz in res['census'].get('1362553', [])}


def read_trs(rid):
    if rid not in base:
        return None
    rr = lvc_pure.Reader(d, strings)
    rr.p = base[rid]
    bt = []
    rr.tok('c', out=bt); rr.tok('i', out=bt)
    for _ in range(9):
        rr.tok('f', out=bt)
    rr.tok('c', out=bt); rr.tok('c', out=bt); rr.tok('c', out=bt)
    return [t[3] for t in bt if t[0] == 'f']


# candidate trigger classes: records whose payload parses as [i][f9][i][c][STR?]
def try_trigger_records(cid):
    out = []
    for rid, off, sz in res['census'].get(cid, []):
        off = int(off, 16)
        if sz != 118:
            continue
        rr = lvc_pure.Reader(d, strings)
        rr.p = off
        try:
            i0 = rr.tok('i')
            f9 = [rr.tok('f') for _ in range(9)]
            i1 = rr.tok('i')
            c0 = rr.tok('c')
            s = rr.tok('STR')
        except Exception:
            continue
        out.append((rid, i0[3], f9, i1[3], c0[3], s))
    return out


for cid in ('880049854', '234759960', '1955669699', '912063847',
            '1923007858', '1419287729', '209554351', '1496113276'):
    got = try_trigger_records(cid)
    if len(got) > 50:
        f9s = [g[2] for g in got]
        # r21 shape: f9 = (0, x, y, z, 0, 0, H, 1, 1)
        like = sum(1 for f in f9s
                   if f[0] == 0 and f[4] == 0 and f[5] == 0
                   and abs(f[7] - 1) < 1e-6 and abs(f[8] - 1) < 1e-6)
        print(f'class {cid}: {len(got)} 118-B records, r21-shape {like}')
        if like > 100:
            hs = sorted(f[6] for f in f9s)
            print(f'   H range [{hs[0]:.2f}, {hs[-1]:.2f}]')
            json.dump(dict(cid=cid, n=len(got),
                           records=[[g[0], g[1], g[2], g[3], g[4],
                                     str(g[5])] for g in got]),
                      open('/tmp/s32_triggers_raw.json', 'w'))
            break
