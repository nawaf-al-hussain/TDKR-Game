#!/usr/bin/env python3
"""Session 26 T1 — censuses + validation battery from the PURE parser."""
import json, sys, struct, collections, re

sys.path.insert(0, '/home/z/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

TABLE_DIR = '/home/z/my-project/work/TDKR-Game/extraction/re/session26'
DATA = '/home/z/my-project/work/data'
OUT = '/tmp/my-project/work/s26_t1'

NAMES = {  # class names for census keys
    '766542306': 'CCollisionComponent', '938977454': 'CTriggerComponent',
    '1253615565': 'CSmartLightComponent', '257920253': 'CAnimationComponent',
    '234759960': 'CEffectComponent(STR)', '1419287729': 'CActorBaseComponent',
    '912063847': 'CBeastObjectComponent', '209554351': 'CSoundAndLight?',
    '1923007858': 'CComponentBuiltinBox', '1955669699': 'CBoxNode-like',
    '880049854': 'CInteractionComponent', '6754056b'.replace('6754056b','1733559659'): 'CAwarenessComponent',
    '397182239': 'CCinematicComponent', '831119443': 'CTrafficSetting',
}


def main():
    table, templates = lvc_pure.load_table(TABLE_DIR)
    gol = json.load(open(f'{TABLE_DIR}/lvc_gol_templates.json'))
    tmpl_names = gol['names']
    reg = set(open('/home/z/my-project/work/TDKR-Game/extraction/ghidra/'
                   'lua_api.txt').read().split())
    print(f'registry: {len(reg)} Lua API functions')

    summary = {}
    all_records = {}
    for isl in ('GothamCity', 'GothamCity_Island2'):
        toks = []
        res = lvc_pure.parse(f'{DATA}/{isl}.lvc', table, templates,
                             tokens_out=toks)
        recs = res['records']
        strings = res['strings']
        d = res['data']
        summary[isl] = dict(records=len(recs),
                            header_count=res['nrec_hdr'],
                            table_off=res['table_off'],
                            nstr=len(strings))
        all_records[isl] = (recs, toks)

        # --- (a) typeId known-set ----------------------------------------
        known = set(templates) | {-1} | {0x2662, 0x2661, 0xdbbb8, 0x2669,
            0x2666, 0x798f, 0x4741, 0x2667, 0xbba, 0x265f, 0x1869f, 0x1011,
            0x265e, 0x2653, 0x14050, 0x14051, 0x2657, 0x267d}
        tc = collections.Counter(hex(t & 0xFFFFFFFF) for _, _, t, _, _ in recs)
        unk = {t: c for t, c in tc.items() if int(t, 16) not in known}
        summary[isl]['distinct_typeids'] = len(tc)
        summary[isl]['unknown_tid_records'] = sum(unk.values())
        summary[isl]['unknown_tid_distinct'] = len(unk)

        # --- (b) STR index invariant -------------------------------------
        nstr = len(strings)
        bad = 0
        tot_str = 0
        for t in toks:
            if t[0] == 'STR':
                tot_str += 1
                v = t[3]
                if isinstance(v, int) and not (-1 <= v < nstr):
                    bad += 1
        summary[isl]['str_reads'] = tot_str
        summary[isl]['str_index_violations'] = bad

        # --- per-typeId census with example names ------------------------
        census_tid = {}
        for t, c in tc.most_common():
            e = {'0x2662': 'player spawn (batman.bdae)',
                 '0x2666': 'waypoint', '0x4741': 'waypoint',
                 '0x798f': 'waypoint+collider chain',
                 '0x2653': 'level properties', '0x2657': 'level init',
                 '0x1011': 'zone?', '0x14050': 'mesh longdist',
                 '0x14051': 'mesh longdist', '0x2661': 'light',
                 '0x2667': 'zone-load', '0x2669': 'weather',
                 '0x267d': 'navmesh', '0x265e': 'compbase', '0x265f': '?',
                 '0x1869f': 'bakegroup', '-0x1': 'terminator'}.get(t)
            if e is None and t in tmpl_names:
                e = tmpl_names[t]
            census_tid[t] = [c, e]
        summary[isl]['per_typeid'] = census_tid

    # ---- (c) 873 banked boundaries --------------------------------------
    banked = json.load(open('/tmp/my-project/work/banked_bounds_gc.json'))
    recs, _ = all_records['GothamCity']
    by_off = {r[1]: r for r in recs}
    ok = 0
    for bid, off, tid, end in banked:
        r = by_off.get(int(off, 16))
        if r and r[3] == int(end, 16):
            ok += 1
    summary['banked_bounds'] = f'{ok}/{len(banked)} reproduced by the pure parser'

    # ---- (d) benign-fault census (from the engine walk records) ----------
    for isl in ('GothamCity', 'GothamCity_Island2'):
        wrecs = json.load(open(
            f'/tmp/my-project/work/s26_v2_{isl}_records.json'))
        nb = sum(1 for r in wrecs if r[4])
        tb = sum(r[3] - r[1] for r in wrecs if r[4])
        summary[isl]['benign_fault_records'] = nb
        summary[isl]['benign_fault_bytes'] = tb

    json.dump(summary, open(f'{OUT}_validation.json', 'w'), indent=1)
    print(json.dumps({k: v for k, v in summary.items()
                      if k in ('GothamCity', 'GothamCity_Island2',
                               'banked_bounds')}, indent=1)[:2200])


if __name__ == '__main__':
    main()
