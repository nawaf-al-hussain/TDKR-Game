#!/usr/bin/env python3
"""S63 T1 final: patch closure2 with the engine-true nested StateSet spec, re-run full closure.
Adds the StateSet-shape-swap null (wrongly ordered CAS lists must break the 6 content templates).
Outputs: s63_t1_closure.json + s63_t1_final_specs.json"""
import json

SRC = '/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t1_closure2.py'
DST = '/tmp/my-project/work/TDKR-Game/extraction/re/session63/s63_t1_closure3.py'

src = open(SRC).read()
OLD = """    0x3b8e9c: ['i'] + ['STR'] * 7,                           # StateSet"""
NEW = """    0x3b8e9c: ['i', ['rep', 'last', [
        'STR', 'i', 'i', 'c', 'c', 'c', 'c', 'c', 'c', 'c',
        'f', 'f', 'i', 'f', 'f', 'f', 'f', 'f', 'f', 'f',
        'c', 'f', 'i', 'i', 'i', 'c', 'c', 'i',
        ['rep', 'last', ['STR',
            'i', ['rep', 'last', ['STR', 'i', ['rep', 'last', ['STR', 'i', 'i', 'i', 'i']]]],
            'i', ['rep', 'last', ['STR', 'i', ['rep', 'last', ['i', 'i', 'STR', 'c']]]],
            'i', ['rep', 'last', ['i', ['rep', 'last', ['i', 'i', 'STR', 'i', 'c']]]],
            'i', ['rep', 'last', ['i', ['rep', 'last', ['i', 'i', 'STR', 'STR', 'c']]]],
            'i', ['rep', 'last', ['i', ['rep', 'last', ['i', 'i', 'f', 'f', 'i', 'c', 'c']], 'i']]]],
        'i', ['rep', 'last', ['i', 'i', 'i', 'i', 'i', 'i', 'f', 'i', 'i', 'STR', 'i']]]],
        ] + ['STR'] * 7,                       # StateSet: s63 engine-true nested (CCS 82-B head + 5 CAS lists + triggers)"""
assert src.count(OLD) == 1, src.count(OLD)
src = src.replace(OLD, NEW)
# remove the duplicate flat StateSet line (second occurrence in D, line with trailing comment)
OLD2 = """    0x3b8e9c: ['i'] + ['STR'] * 7,                         # StateSet (32B = count-0 case; count-driven nested form decoded, CAS body open)"""
assert src.count(OLD2) == 1
src = src.replace(OLD2, '    # (s63: duplicate flat StateSet entry removed - nested engine-true spec above)')

# retarget outputs + add the SS-shape-swap null before the json dump
src = src.replace("/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t1_closure.json",
                  "/tmp/my-project/work/TDKR-Game/extraction/re/session63/s63_t1_closure.json")
src = src.replace("/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t1_final_specs.json",
                  "/tmp/my-project/work/TDKR-Game/extraction/re/session63/s63_t1_final_specs.json")
NULL_ADD = '''
# S63 NULL: swap the CAS list2/list3 track shapes inside the StateSet spec (wrongly ordered)
_ss = E['0x5441a117']
def _swap_ss(spec):
    import copy
    s = copy.deepcopy(spec)
    state = s[1][2]
    cas = state[28][2]          # ['rep','last',[CAS-body]] -> CAS-body
    l2 = cas[2]; l3 = cas[4]    # list2 block, list3 block
    cas[2], cas[4] = l3, l2
    return s
E2 = dict(E); E2['0x5441a117'] = _swap_ss(E['0x5441a117'])
r_ss = do_walk([r for r in recs if r[1] in ('BatPod', 'Helicopter', 'Helicopter_Bane', 'Military_Heli', 'Test_Object', 'TheBatDrive')], E2, want_fails=True)
res['NULL_SS_SWAP'] = {'exact': r_ss['exact'], 'pass': r_ss['exact'] + r_ss['bounds'],
                       'fails': [f['name'] for f in r_ss.get('fails', [])]}
print('[NULL-ss-swap] exact %d pass %d fails %s (content templates must break)' % (
    r_ss['exact'], r_ss['exact'] + r_ss['bounds'], res['NULL_SS_SWAP']['fails']))

json.dump'''
src = src.replace("\njson.dump", NULL_ADD, 1)
# also retarget the print header
src = src.replace("[S62 corrected]", "[S63 nested-StateSet]")
open(DST, 'w').write(src)
print('patched closure written:', DST)
