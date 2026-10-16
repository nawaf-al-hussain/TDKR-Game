#!/usr/bin/env python3
"""S29 T1 FINAL: authoritative 12-level run with the s29 spec set + banked spans."""
import sys, json, collections
sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

TAB = '/tmp/my-project/work/TDKR-Game/extraction/re/session26'
table, templates = lvc_pure.load_table(TAB)
comps = table['components']
comps[str(0xC69A6A7)] = ['i', 'i']                     # CComponentZonesLink::Load @0x2e7430
comps[str(0x2AD64F3D)] = ['f', 'f', 'i', 'i']          # CPlaneNodeComponent::Load @0x2a0728
comps[str(0x10FCFD6)] = []                             # CDummyComponent::Load @0x22a368 (0 reads)
comps[str(0x2888019A)] = ['i', 'f', 'f', 'f', 'f', 'f', 'f', 'i']  # CComponentBaseWorldBox::Load @0x2e6a08
comps[str(0x39E32181)] = ['i', ['rep', 'last', ['i']]]             # CComponentMetaZone::Load @0x3c13f8
comps[str(0x7F88E44E)] = []                            # CComponentBuiltinCollisionBox (0-read fit; see report)
for k in ('661', '1075', '8278', '320811', '18987', '174419', '3008'):
    comps.setdefault(k, [])
extra = json.load(open('/tmp/my-project/work/re29/s29_spans_extra.json'))
CINE = str(0x17AC851F)
have = {(x[0], x[1]) for x in table['spans'][CINE]}
for sp in extra['spans'].get(CINE, []):
    if (sp[0], sp[1]) not in have:
        table['spans'][CINE].append(sp); have.add((sp[0], sp[1]))
for off, toks in extra['span_toks'].get(CINE, {}).items():
    table['span_toks'][CINE].setdefault(off, toks)
se = json.load(open('/tmp/my-project/work/re29/s29_spans_e_shop.json'))
table['spans_e'] = se['spans_e']; table['span_toks_e'] = se['span_toks_e']
# persist the final table
json.dump(table, open('/tmp/my-project/work/re29/lvc_readseq_s29.json', 'w'), indent=0)

LEVELS = ['GothamCity', 'GothamCity_Island2', 'BatCave', 'l_menu', 'shop', 'Stadion',
          'Police_Station', 'StockExchange', 'Underground', 'Military', 'ThePit', 'Test']
res = {}
for lv in LEVELS:
    stats = collections.Counter()
    try:
        r = lvc_pure.parse(f'/tmp/my-project/work/data/{lv}.lvc', table, templates, stats=stats)
        res[lv] = dict(ok=True, n=len(r['records']), toff=hex(r['table_off']))
        print(f'{lv:20s} OK {len(r["records"]):6d} records, table {r["table_off"]:#x}')
    except Exception as e:
        res[lv] = dict(ok=False, err=f'{type(e).__name__}: {str(e)[:110]}')
        print(f'{lv:20s} FAIL {type(e).__name__}: {str(e)[:110]}')
json.dump(res, open('/tmp/my-project/work/re29/s29_final_levels.json', 'w'), indent=1)
ok = [k for k, v in res.items() if v['ok']]
print(f'\n{len(ok)}/12 parse to table end: {ok}')
