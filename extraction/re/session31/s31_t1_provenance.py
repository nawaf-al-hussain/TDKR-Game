#!/usr/bin/env python3
"""S31 T1.1: spec provenance table + usage census + fitted-removal experiment.

Classifies every spec in the canonical s30 table (lvc_readseq_s30.json):
  STATIC_DISASM   - decoded from libKRHP.so disassembly (address evidence)
  ENGINE_CASE     - real dispatcher cases (0x2657 LevelInit, 0x798f waypoint)
  LOOP_VERIFIED   - hand-derived loop specs, byte-verified on every island record
  FITTED_ISLAND   - token pattern harvested from the GothamCity+Island2 walks
  FITTED_TEST     - raw-N spans tracer-measured on Test.lvc (hex-format keys;
                    unreachable by the decimal-keyed canonical parser)
  ZERO_READ       - [] spec: class unregistered in .so -> CreateObject
                    null-check consumes the tid only (engine fact)

Then: usage counts per level for every class, and the removal experiment:
drop all FITTED_ISLAND component specs, re-run all 12 levels, report the
first missing class + stop offset per level.
"""
import json, struct, sys, collections

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

TAB = '/tmp/my-project/work/re29/lvc_readseq_s30.json'
GOL = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json'
DATA = '/tmp/my-project/work/data'
LEVELS = ['GothamCity', 'GothamCity_Island2', 'BatCave', 'l_menu', 'shop',
          'Stadion', 'Police_Station', 'StockExchange', 'Underground',
          'Military', 'ThePit', 'Test']
ISLANDS = {'GothamCity', 'GothamCity_Island2'}
NON_ISLAND = [l for l in LEVELS if l not in ISLANDS]

STATIC = {
    '1285943310': 'CComponentNewShopItemProperty::Load @0x202ae4 (ret 0x203128), generic-switch case @0x36958c vt 0xbd0a30 slot+0x10',
    '397182239':  'CCinematicComponent::Load @0x2dce20 + CContainerTracksAnimatedObject::Load @0x2d9118 (8 sections)',
    '831119443':  'CTrafficSetting::Load @0x1ffa1c (ret 0x1ffeb4)',
    '690565296':  'shop class Load @0x203858: [i,STR,i]',
    '1153971665': 'shop class Load @0x203764: [i,STR,STR,i,STR,STR,STR]',
    '787639378':  'CSoundAndLight loop from Load @0x1feb64 (islands always n=0)',
    '208250535':  'CComponentZonesLink::Load @0x2e7430: [i][i] (factory case @0x369d58 + symbol)',
    '718688061':  'CPlaneNodeComponent::Load @0x2a0728: [f][f][i][i] (factory @0x22453c, GetType @0x2e1db0)',
    '680001946':  'WorldBox: [i][f x6][i] (factory/disasm, r19)',
    '971186561':  'MetaZone: [i n]+n x [i] (disasm, r19)',
    '2139677774': 'GCT null-default path: 0 bytes in practice (r19)',
    '17813462':   'CDummyComponent::Load @0x22a368: 0 reads (r19; s28 hex typo corrected)',
    '1362553':    'CComponentBase::Load @0x14ca79: [c][i]+9f+[c][c][c]',
    '1387399':    'name comp @0x152b87: [STR][raw4]',
    '718446662':  'CGroupObject::ReadBuiltinData (0x2ad2a046): [c][c][i]+i-list',
}
ENGINE_CASES = {'9815': 'CComponentLevelInit::Load @0x2018f0 + CTemplateLevelProperties::Load @0x2023bc (unconditional ReadInt @0x20240c)',
                '31119': 'waypoint engine case 0x798f (67 B + 3f + builtin cylinder 45 B)'}
LOOP_VERIFIED = {
    '766542306': 'CCollisionComponent',
    '1253615565': 'CSmartLightComponent',
    '931672584': 'CSoundAndLight',
    '1734173459': 'NPC-pos-list',
    '1419287729': 'CActorBaseComponent (raw7 head = inlined sibling reads)',
}

tab = json.load(open(TAB))
comps, ded, eng = tab['components'], tab['dedicated'], tab['engine_cases']


def classify(spec, key):
    if key == 'REC':
        return 'DEAD_PSEUDO', 'record-framing pseudo-entry (decimal-keyed parser never looks it up)'
    if not key.isdigit():
        return 'FITTED_TEST', 'Test.lvc raw-N span, engine-tracer measured (r17); hex-format key - dead for decimal lookup'
    if key in STATIC:
        return 'STATIC_DISASM', STATIC[key]
    if key in ENGINE_CASES:
        return 'ENGINE_CASE', ENGINE_CASES[key]
    if key in LOOP_VERIFIED:
        return 'LOOP_VERIFIED', LOOP_VERIFIED[key] + ' - hand-derived, byte-verified on every island record'
    if spec == [] or spec == [['i', 4]] and False:
        pass
    if spec == []:
        return 'ZERO_READ', 'unregistered in .so -> CreateObject default-insert, 0 component reads (positive-controlled)'
    if key in ded:
        return 'FITTED_ISLAND', 'dedicated-record pattern from GothamCity+Island2 walks (single pattern per tid)'
    return 'FITTED_ISLAND', 'token pattern harvested from GothamCity+Island2 native walks (single pattern per class)'


rows = []
for k, v in sorted(comps.items(), key=lambda kv: (not kv[0].isdigit(), int(kv[0]) if kv[0].isdigit() else 0)):
    prov, ev = classify(v, k)
    rows.append((k, prov, ev, len(v)))
for k, v in sorted(ded.items(), key=lambda kv: int(kv[0])):
    prov, ev = classify(v, k)
    rows.append((k, prov, ev, len(v)))
for k, v in sorted(eng.items(), key=lambda kv: int(kv[0])):
    prov, ev = classify(v, k)
    rows.append((k, prov, ev, len(v)))

cnt = collections.Counter(r[1] for r in rows)
print('=== PROVENANCE SUMMARY (canonical s30 table) ===')
for k, c in cnt.most_common():
    print(f'  {k}: {c}')

templates = {int(k, 16): v for k, v in json.load(open(GOL))['templates'].items()}

# ---- usage census + full run ----
print('\n=== 12-LEVEL RUN (canonical table) ===')
use = {}
runok = {}
for lv in LEVELS:
    stats = collections.Counter()
    try:
        res = lvc_pure.parse(f'{DATA}/{lv}.lvc', tab, templates, None, stats)
        last = res['records'][-1]
        ok = res['complete']
        runok[lv] = (ok, len(res['records']),
                     None if ok else f'cursor {res["final_cursor"]:#x} != table {res["table_off"]:#x}')
        use[lv] = set(res['census'].keys())
        print(f'  {lv:22s} {"OK " if ok else "MISMATCH"} {len(res["records"]):6d} recs')
    except Exception as e:
        runok[lv] = (False, None, f'{type(e).__name__}: {str(e)[:90]}')
        use[lv] = set()
        print(f'  {lv:22s} FAIL {runok[lv][2]}')

# ---- removal experiment ----
# removal experiment: fitted COMPONENT specs only (dedicated removal produces
# a framing artifact: dedicated tids are dual-registered as gol templates and
# records fall through to the wrong branch - reported separately)
tab2 = json.loads(json.dumps(tab))
removed = [k for k, v in tab2['components'].items()
           if k.isdigit() and classify(v, k)[0] == 'FITTED_ISLAND']
removed_ded = [k for k, v in tab2['dedicated'].items()
               if classify(v, k)[0] == 'FITTED_ISLAND']
for k in removed:
    del tab2['components'][k]
print(f'\n=== REMOVAL EXPERIMENT: dropped {len(removed)} FITTED_ISLAND component specs '
      f'(dedicated specs kept; {len(removed_ded)} of them are island-fitted and load-bearing) ===')
rem = {}
for lv in LEVELS:
    stats = collections.Counter()
    try:
        res = lvc_pure.parse(f'{DATA}/{lv}.lvc', tab2, templates, None, stats)
        rem[lv] = (res['complete'], len(res['records']),
                   None if res['complete'] else f'cursor {res["final_cursor"]:#x}')
    except RuntimeError as e:
        rem[lv] = (False, None, str(e)[:120])
    except Exception as e:
        rem[lv] = (False, None, f'{type(e).__name__}: {str(e)[:120]}')
    status = 'PARSES-ON' if rem[lv][0] else f'STOPS: {rem[lv][2]}'
    print(f'  {lv:22s} {status}')

# fitted classes exercised outside the islands
fitted_set = set(removed) | set(removed_ded)
for lv in NON_ISLAND:
    fl = sorted(use[lv] & fitted_set, key=lambda x: int(x) if x.isdigit() else 0)
    print(f'  {lv:22s} fitted classes used: {len(fl)} '
        f'[{", ".join(hex(int(x)) for x in fl[:8])}{'...' if len(fl) > 8 else ""}]')
non_isl_union = set().union(*[use[lv] for lv in NON_ISLAND]) & fitted_set
print(f'  union over 8 non-island levels: {len(non_isl_union)} fitted classes')

json.dump(dict(provenance=[dict(key=r[0], prov=r[1], evidence=r[2],
                                ntok=r[3]) for r in rows],
               usage={lv: sorted(use[lv]) for lv in LEVELS},
               run={lv: dict(ok=runok[lv][0], nrec=runok[lv][1],
                             err=runok[lv][2]) for lv in LEVELS},
               removal={lv: dict(ok=rem[lv][0], nrec=rem[lv][1],
                                 err=rem[lv][2]) for lv in LEVELS},
               removed_keys=removed,
               removed_ded=removed_ded,
               non_island_fitted_union=sorted(non_isl_union)),
          open('/home/z/my-project/download/s31_t1_provenance.json', 'w'),
          indent=1)
print('\nwrote /home/z/my-project/download/s31_t1_provenance.json')
