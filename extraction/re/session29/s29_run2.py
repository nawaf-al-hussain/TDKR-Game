#!/usr/bin/env python3
"""S29 T1: empirical spec fitting — run levels with candidate specs, iterate on failures."""
import json, struct, sys, collections
sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

TAB_DIR = '/tmp/my-project/work/TDKR-Game/extraction/re/session26'
DATA = '/tmp/my-project/work/data'
table, templates = lvc_pure.load_table(TAB_DIR)
comps = table['components']

def hx(v): return str(v)

# resolved real specs (decimal keys!)
comps['208250535'] = ['i', 'i']                    # 0xC69A6A7 CComponentZonesLink [i][i]
comps['717509821'] = ['f', 'f', 'i', 'i']          # 0x2AD64F3D CPlaneNodeComponent [f][f][i][i]
comps['2141219662'] = ['f'] * 0 + []               # placeholder replaced below
# 0x7F88E44E = CComponentBuiltinCollisionBox::Load @0x2e1c58 -> disassemble to confirm grammar
# For now: mark unknowns as 0-read candidates
ZERO_CANDIDATES = {
    '661': '0x295 l_menu', '1075': '0x433 shop', '8278': '0x2056 Stadion',
    '320811': '0x4E52B Police', '18987': '0x4A2B StockEx', '174419': '0x2A953 Underg',
    '3008': '0xBC0 Military2', '538342478': '0x201B2E3E?', '2139759438': '0x7F8ED4E',
    '17760542': '0x10FF796 Dummy', '681657818': '0x288AE7DA', '93985': '0x16F31 shopitem',
}
for k in ZERO_CANDIDATES:
    comps.setdefault(k, [])

LEVELS = ['l_menu', 'shop', 'Stadion', 'Police_Station', 'StockExchange',
          'Underground', 'Military', 'ThePit']
results = {}
for lv in LEVELS:
    stats = collections.Counter()
    try:
        res = lvc_pure.parse(f'{DATA}/{lv}.lvc', table, templates, stats=stats)
        results[lv] = dict(ok=True, nrec=len(res['records']))
        print(f'{lv:16s} OK {len(res["records"])} records')
    except lvc_pure.SpanNeeded as e:
        results[lv] = dict(ok=False, err=('SPAN', hex(e.pos)))
        print(f'{lv:16s} SPAN-needed at {e.pos:#x}')
    except Exception as e:
        results[lv] = dict(ok=False, err=(type(e).__name__, str(e)[:120]))
        print(f'{lv:16s} {type(e).__name__}: {str(e)[:120]}')
json.dump(results, open('/tmp/my-project/work/re29/s29_level_run2.json', 'w'), indent=1)
