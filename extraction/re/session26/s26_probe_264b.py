#!/usr/bin/env python3
"""Compare walk-style vs engine-style component reads for one record region."""
import sys, struct, json

sys.path.insert(0, '/home/z/my-project/work/TDKR-Game/extraction/re/session25')
sys.path.insert(0, '/home/z/my-project/scripts')
from lvc_tracer import Tracer, STREAM, READERS
import s26_lnobj_harness as H

DATA = '/home/z/my-project/work/data'
d = open(f'{DATA}/GothamCity.lvc', 'rb').read()
table_off = struct.unpack_from('>I', d, 4)[0]
pos = table_off
nstr = struct.unpack_from('>i', d, pos)[0]
pos += 4
strings = []
for i in range(nstr):
    ln = struct.unpack_from('>i', d, pos)[0]
    pos += 4
    strings.append(d[pos:pos + ln].decode('utf-8', 'replace'))
    pos += ln
gol = json.load(open('/home/z/my-project/work/TDKR-Game/extraction/re/'
                     'session24/gol_templates.json'))
templates = {int(k, 16): v for k, v in gol['templates'].items()}
fac = {int(k, 16): int(v['load'], 16)
       for k, v in json.load(open('/home/z/my-project/work/'
                                  'factory_switch.json')).items()
       if v.get('load')}
gct = {int(k, 16): int(v['load'], 16)
       for k, v in json.load(open('/home/z/my-project/work/'
                                  'gct_switch.json')).items() if v.get('load')}
loads = json.load(open('/home/z/my-project/work/TDKR-Game/extraction/re/'
                       'session24/component_loads.json'))
syms = json.load(open('/home/z/my-project/work/so_syms.json'))['by_name']
load_addrs = {}
for tid, e in loads.items():
    s = e.get('load_sym')
    if s and s in syms:
        load_addrs[int(tid, 16)] = int(syms[s], 16)

tr = Tracer()
tr.load_lvc(d, strings)
H.build(tr)
H.load_gol_dict(tr, open(f'{DATA}/gol.bin', 'rb').read())
H.populate_gom(tr)
H.install_stubs(tr)

for off, tid in ((0x15f1, 0x264b), (0x1667, 0x264b), (0x16dd, 0x264b)):
    tmpl = templates[tid]
    print(f'\n=== record @{off:#x} tid={tid:#x} tmpl={tmpl}')
    tr.set_cursor(off + 4)
    for flag, ctid in tmpl:
        if flag:
            continue
        c0 = tr.get_cursor()
        la = fac.get(ctid) or gct.get(ctid) or load_addrs.get(ctid)
        tr.benign_fault = None
        err = tr.run(la, [tr.new_component(), STREAM])
        used = tr.get_cursor() - c0
        ev = [(READERS.get(a, hex(a))) for a, c in tr.trace.events]
        import collections
        cnt = collections.Counter(ev)
        print(f'  ctid {ctid:#x} la={la:#x} used={used} err={err} '
              f'benign={tr.benign_fault} readers={dict(cnt)}')
        # last few events with cursors
        for a, c in tr.trace.events[-4:]:
            print(f'     {READERS.get(a, hex(a))} @{c:#x} '
                  f'bytes={d[c:c+16].hex()}')
