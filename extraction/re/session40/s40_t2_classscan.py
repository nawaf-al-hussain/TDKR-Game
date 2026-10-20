#!/usr/bin/env python3
"""S40 T2: scan every census class in GothamCity.lvc for [id][pos] candidates;
identify which class carries the script object-id space."""
import sys, json, struct
import numpy as np
sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

GOL = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json'
templates = {int(k, 16): v for k, v in json.load(open(GOL))['templates'].items()}
tab = json.load(open('/tmp/my-project/work/re29/lvc_readseq_s30.json'))
res = lvc_pure.parse('/tmp/my-project/work/data/GothamCity.lvc', tab, templates, None)
d, cens = res['data'], res['census']

# script-referenced ids (same CALL_RE as s38)
import re
SCRIPTS = json.load(open('/home/z/my-project/scripts/s34_t4_scripts.json'))
if isinstance(SCRIPTS, dict):
    SCRIPTS = SCRIPTS['all_scripts']
CALL_RE = re.compile(
    r'\b(?:Enable|Disable|ShowObject|HideObject|EnableShowObject|SpawnObject|'
    r'ObjectGetPosition|SetObjectPos|MoveObject|Activate|Deactivate|'
    r'SetObjectVisible|ActorSetState|KillActor|ActorLookTo|SetActorSpeedWalk|'
    r'SetActorSpeedRun|NPCAttackTarget|NPCGoToPath|NPCSetSniper|NPCSetStance|'
    r'StartEventAtObjectNode|HideOccluder|ShowOccluder)\s*\(\s*(\d{5,})', re.I)
callee = set()
owners = set()
for s in SCRIPTS:
    if s.get('obj_id') is not None:
        owners.add(int(s['obj_id']))
    for m in CALL_RE.finditer(s['script']):
        callee.add(int(m.group(1)))
TRIGS = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session36/session36_t2_volumes.json'))
trig_ids = {t['id'] for t in TRIGS}
print(f'callee {len(callee)}, owners {len(owners)}, trigger-table ids {len(trig_ids)}')

def plausible_pos(p):
    return abs(p[0]) < 2200 and abs(p[1]) < 2200 and abs(p[2]) < 400

results = {}
for cls, recs in sorted(cens.items(), key=lambda kv: -len(kv[1])):
    if not recs: continue
    ids_le, ids_be = set(), set()
    npos = 0
    idpos = {}
    for rec in recs[:4000]:
        if isinstance(rec, dict):
            rid = rec.get('id', rec.get('rid'))
            off = rec.get('off')
            sz = rec.get('size', rec.get('sz', 48))
        else:
            rid, off = rec[0], rec[1]
            sz = rec[2] if len(rec) > 2 else 48
        o = int(off, 16) if isinstance(off, str) else off
        sz = sz or 48
        raw = d[o:o+sz]
        # try every 4-aligned window: candidate id (LE/BE) + candidate pos (next 12 B)
        for a in range(0, min(len(raw) - 16, 24), 4):
            v32 = struct.unpack_from('<I', raw, a)[0]
            b32 = struct.unpack_from('>I', raw, a)[0]
            for v, is_be in ((v32, False), (b32, True)):
                if not (100000 <= v <= 3000000): continue
                p = struct.unpack_from('<3f', raw, a + 4)
                pb = struct.unpack_from('>3f', raw, a + 4)
                for pp in (p, pb):
                    if plausible_pos(pp):
                        (ids_be if is_be else ids_le).add(v)
                        if v not in idpos:
                            idpos[v] = pp
                        npos += 1
                        break
    res_c = len(callee & (ids_le | ids_be))
    own_c = len(owners & (ids_le | ids_be))
    trig_c = len(trig_ids & (ids_le | ids_be))
    results[cls] = (len(recs), len(ids_le | ids_be), res_c, own_c, trig_c)
    if res_c or trig_c or own_c:
        print(f'class {cls}: n={len(recs)} uniq_ids={len(ids_le|ids_be)} '
              f'callee~{res_c}/{len(callee)} owners~{own_c}/{len(owners)} trig~{trig_c}/{len(trig_ids)}')
json.dump({k: list(v) for k, v in results.items()},
          open('/tmp/my-project/scripts/s40_t2_classscan.json', 'w'), indent=1)
