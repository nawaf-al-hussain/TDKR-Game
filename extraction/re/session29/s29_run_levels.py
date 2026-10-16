#!/usr/bin/env python3
"""S29 T1: extend lvc_readseq.json with round-19 resolved specs; test all 12 levels."""
import json, struct, sys, copy, collections
sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

TAB_DIR = '/tmp/my-project/work/TDKR-Game/extraction/re/session26'
OUT_DIR = '/tmp/my-project/work/re29'
DATA = '/tmp/my-project/work/data'

table, templates = lvc_pure.load_table(TAB_DIR)
comps = table['components']

# --- round-19 resolved specs (from disasm + symbols) ---
NEW = {
    '208230695':  ['i', 'i'],                    # 0xC69A6A7 CComponentZonesLink::Load @0x2e7430: [i][i]
    '717509821':  ['f', 'f', 'i', 'i'],          # 0x2AD64F3D CPlaneNodeComponent::Load @0x2a0728: [f][f][i][i]
    '864369134':  [],                            # 0x3377F0E absent from .so (positive-controlled scan) -> 0 reads
    '2141219662': [],                            # 0x7F88E44E GCT null-default (engine crash path; 0 bytes in practice)
    '17760542':   [],                            # 0x10FF796 CDummyComponent::Load @0x22a368 reads 0 bytes (s28)
}
comps.update(NEW)

# 0x7F8ED4E = fixed 40 B [3f][7i] (s28 auto-fit); 0x288AE7DA = 6 fixed groups (s28)
comps['2139759438'] = ['f', 'f', 'f', 'i', 'i', 'i', 'i', 'i', 'i', 'i']   # 0x7F8ED4E
# 0x288AE7DA = 6 groups; group shape unknown from s28 note "WorldBox-like" -- try later if hit
# 0x16f31 = 14-token head + count x 15-token body (s28) -- shape TBD from instances if hit

def run_level(name, tab, tmpl):
    stats = collections.Counter()
    try:
        res = lvc_pure.parse(f'{DATA}/{name}.lvc', tab, tmpl, stats=stats)
        n = len(res['records'])
        return True, n, dict(stats), None
    except lvc_pure.SpanNeeded as e:
        return False, None, dict(stats), ('SPAN', hex(e.pos))
    except Exception as e:
        return False, None, dict(stats), (type(e).__name__, str(e)[:160])

LEVELS = ['GothamCity', 'GothamCity_Island2', 'BatCave', 'l_menu', 'shop', 'Stadion',
          'Police_Station', 'StockExchange', 'Underground', 'Military', 'ThePit', 'Test']
results = {}
for lv in LEVELS:
    ok, n, stats, err = run_level(lv, table, templates)
    results[lv] = dict(ok=ok, nrec=n, err=err, stats=stats)
    print(f'{lv:22s} {"OK " if ok else "FAIL"} {n if n else "":>6} {err if err else ""}')
json.dump(results, open(f'{OUT_DIR}/s29_level_run1.json', 'w'), indent=1)
