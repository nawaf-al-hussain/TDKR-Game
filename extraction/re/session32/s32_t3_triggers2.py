#!/usr/bin/env python3
"""S32 T3b: full trigger decode — records, owner TRS, gol template,
IsObjectInside disasm, world volumes, spawn verification."""
import sys, json, struct, math, collections
import numpy as np

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

TAB = '/tmp/my-project/work/re29/lvc_readseq_s30.json'
GOL = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json'
templates = {int(k, 16): v for k, v in json.load(open(GOL))['templates'].items()}
tab = json.load(open(TAB))
res = lvc_pure.parse('/tmp/my-project/work/data/GothamCity.lvc', tab,
                     templates, None)
d, strings = res['data'], res['strings']
tid_of = {rid: tid for rid, s0, tid, e, k in res['records']}
base = {rid: int(o, 16) for rid, o, sz in res['census'].get('1362553', [])}

TRG = '938977454'
trigs = []
for rid, off, sz in res['census'].get(TRG, []):
    off = int(off, 16)
    rr = lvc_pure.Reader(d, strings)
    rr.p = off
    toks = []
    rr.tok('i', out=toks)
    n0 = len(toks)
    for _ in range(9):
        rr.tok('f', out=toks)
    f9 = [t[3] for t in toks[n0:]]
    rr.tok('i', out=toks)
    rr.tok('c', out=toks)
    s = rr.tok('STR', out=toks)
    trigs.append(dict(rid=rid, off=off, i0=toks[0][3],
                      f9=f9, i1=toks[10][3], flag=toks[11][3],
                      lua=str(s) if s is not None else None,
                      tid=tid_of.get(rid)))
print(f'triggers parsed: {len(trigs)}')
shape = collections.Counter(
    (t['f9'][0] == 0, t['f9'][4] == 0, t['f9'][5] == 0,
     round(t['f9'][7], 3), round(t['f9'][8], 3)) for t in trigs)
print('f9 shape census (f0==0,f4==0,f5==0,f7,f8):', shape.most_common(4))
hs = [t['f9'][6] for t in trigs]
print(f'H range [{min(hs):.2f}, {max(hs):.2f}], hist bucketed:',
      collections.Counter(round(h, 0) for h in hs).most_common(8))
flags = collections.Counter(t['flag'] for t in trigs)
print('flag census:', flags.most_common(6))
luas = collections.Counter(t['lua'] for t in trigs)
print(f'distinct lua fns: {len(luas)}; top: {luas.most_common(4)}')

# owner TRS
n_trs = 0
xyz = []
for t in trigs:
    trs = None
    if t['rid'] in base:
        rr = lvc_pure.Reader(d, strings)
        rr.p = base[t['rid']]
        bt = []
        rr.tok('c', out=bt); rr.tok('i', out=bt)
        for _ in range(9):
            rr.tok('f', out=bt)
        rr.tok('c', out=bt); rr.tok('c', out=bt); rr.tok('c', out=bt)
        trs = [x[3] for x in bt if x[0] == 'f']
        n_trs += 1
    t['trs'] = trs
    if trs:
        xyz.append(trs[:3])
print(f'owner TRS found: {n_trs}/{len(trigs)}')
if xyz:
    xyz = np.array(xyz)
    print(f'  owner pos x [{xyz[:,0].min():.1f},{xyz[:,0].max():.1f}] '
          f'y [{xyz[:,1].min():.1f},{xyz[:,1].max():.1f}] '
          f'z [{xyz[:,2].min():.1f},{xyz[:,2].max():.1f}]')

# f9 pos vs owner pos: are they the same?
same = sum(1 for t in trigs if t['trs'] and
           abs(t['f9'][1] - t['trs'][0]) < 0.01 and
           abs(t['f9'][2] - t['trs'][1]) < 0.01 and
           abs(t['f9'][3] - t['trs'][2]) < 0.01)
print(f'f9 pos == owner TRS pos: {same}/{len(trigs)}')

# gol template for trigger tids
tids = collections.Counter(t['tid'] for t in trigs)
print('trigger tids:', dict(list(tids.most_common(6))))
for tid, n in tids.most_common(3):
    tp = templates.get(tid)
    if tp:
        print(f'  template {tid:#x}: {json.dumps(tp)[:220]}')

# IsObjectInside disasm
import re
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
SO = '/tmp/my-project/work/apk_lib/lib/armeabi-v7a/libKRHP.so'
so = open(SO, 'rb').read()
syms = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/'
                      'session25/so_syms.json'))
by_addr = syms['by_addr']
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
print('\n=== IsObjectInside @0x24a28c ===')
cnt = 0
for ins in md.disasm(so[0x24a28c:0x24a28c + 0x180], 0x24a28c):
    tag = ''
    if ins.mnemonic in ('bl', 'blx'):
        mm = re.search(r'0x([0-9a-f]+)', ins.op_str)
        if mm and int(mm.group(1), 16) in by_addr:
            tag = ' ; ' + re.sub(r'^_ZN\d+', '',
                                 by_addr[int(mm.group(1), 16)])[:60]
    print(f'{ins.address:x}: {ins.mnemonic:8s} {ins.op_str}{tag}')
    cnt += 1
    if cnt >= 70:
        break
json.dump(dict(n=len(trigs),
               records=[dict(rid=t['rid'], tid=t['tid'], f9=t['f9'],
                             flag=t['flag'], lua=t['lua'], trs=t['trs'])
                        for t in trigs[:2000]]),
          open('/home/z/my-project/download/s32_t3_triggers.json', 'w'))
print('\nwrote s32_t3_triggers.json')
