#!/usr/bin/env python3
"""s54 T1 step 13: scan ALL lvc files for records instantiating the Glider
(0x2674) / Glider_Plunge (0x4c741) templates, and decode any CComponentGlide
component payload (flag-0: ReadInt + 22xReadFloat + ReadInt from the record).

Walks records with the s26 framing (lvc_readseq + lvc_gol_templates) but
intercepts glide-template records before the component replay.
"""
import json
import struct
import sys
import os

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import importlib.util

spec = importlib.util.spec_from_file_location(
    'lvc_pure', '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_pure.py')
lp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lp)

GLIDE_CLASS = 17878559          # 0x110ce1f CComponentGlide
GLIDER_TIDS = (0x2674, 0x4c741)  # Glider, Glider_Plunge
# other candidate: any template whose component list contains GLIDE_CLASS
gol = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json'))
templates = {int(k, 16): v for k, v in gol['templates'].items()}
names = gol['names']
glide_tids_all = [t for t, v in templates.items() if any(c == GLIDE_CLASS for _, c in v)]
print('templates carrying CComponentGlide:', [(hex(t), names.get(hex(t), names.get(str(t), '?'))) for t in glide_tids_all])
print('their flags:', {hex(t): [[f, hex(c)] for f, c in templates[t]] for t in glide_tids_all})

table, _ = lp.load_table('/tmp/my-project/work/TDKR-Game/extraction/re/session26')

NAT = {'i': 4, 'f': 4, 'c': 1, 'B': 1, 's': 2, 'STR': 4}

files = sorted('/tmp/my-project/work/data/' + f for f in os.listdir('/tmp/my-project/work/data')
               if f.endswith('.lvc'))
for path in files:
    d = open(path, 'rb').read()
    if d[:4] not in (b'DICT',):
        print(path, 'unexpected magic', d[:4])
        continue
    table_off = struct.unpack_from('>I', d, 4)[0]
    # strings table (same framing as lvc)
    # lvc framing per lvc_pure: 'DICT'|u32be tableOffset|u8|u16be tag|u16be ver|u32be nrec(discarded)
    # strings: at table_off
    pos = table_off
    nstr = struct.unpack_from('>i', d, pos)[0]; pos += 4
    strings = []
    for i in range(nstr):
        ln = struct.unpack_from('>i', d, pos)[0]; pos += 4
        strings.append(d[pos:pos + ln].decode('utf-8', 'replace')); pos += ln

    # walk records; decode framing minimally: for generic tids, replay flag-0 reads
    # via readseq; for glide-template tids, decode the glide component by hand.
    cur = 17
    found = []
    rid = 0
    try:
        while cur < table_off:
            rec_start = cur
            tid = struct.unpack_from('>I', d, cur)[0]
            rid += 1
            if tid == 0xFFFFFFFF:
                cur += 4
                continue
            if tid in templates:
                p = cur + 4
                for flag, cid in templates[tid]:
                    if flag != 0:
                        continue
                    if cid == GLIDE_CLASS:
                        # decode: ReadInt + 22 floats + ReadInt (all BE)
                        int1 = struct.unpack_from('>i', d, p)[0]; p += 4
                        fl = [struct.unpack_from('>f', d, p + 4 * k)[0] for k in range(22)]
                        p += 88
                        int2 = struct.unpack_from('>i', d, p)[0]; p += 4
                        found.append((hex(tid), names.get(hex(tid), '?'), hex(rec_start),
                                      int1, fl, int2, p - rec_start))
                    elif cid in table:
                        toks = [t[0] for t in table[cid]]
                        for t in toks:
                            p += NAT[t]
                    else:
                        # unknown class: cannot advance - stop this file
                        found.append(('UNFRAMABLE', hex(tid), names.get(hex(tid), '?'), hex(rec_start)))
                        break
                cur = p
            else:
                # dedicated/unknown tid: 4-byte skip per lvc_pure note? no - dedicated have
                # real sequences; do not attempt - only detect glide tids among generic
                # (non-template) tids are dedicated records; skip them by delegating
                # to readseq 'dedicated' when known, else stop.
                if tid == 0x2674 or tid == 0x4c741:
                    found.append(('GLIDE-TID-NONGENERIC', hex(tid), hex(rec_start)))
                cur += 4  # unknown/dedicated: cannot frame cheaply; advance 4 and resync is unsafe
                break
    except Exception as e:
        print(path, 'walk stopped:', e)
    if found:
        print('\n==', path)
        for f2 in found:
            print('  ', f2)
