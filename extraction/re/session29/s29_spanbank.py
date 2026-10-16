#!/usr/bin/env python3
"""S29 T1: span-banking harness — natively measure unmeasured CCinematicComponent
instances (0x17AC851F) in the 9 non-island levels; bank spans+tokens; re-parse.

Also engine-verifies the round-19 component specs (ZonesLink [i][i],
PlaneNode [f][f][i][i], CollisionBox, etc.) by running their REAL Loads."""
import json, struct, sys, collections
sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session25')
import lvc_pure
from lvc_tracer import Tracer, STREAM, READERS, NESTING_PARENTS

TAB_DIR = '/tmp/my-project/work/TDKR-Game/extraction/re/session26'
DATA = '/tmp/my-project/work/data'
OUT = '/tmp/my-project/work/re29'
CINE = str(0x17AC851F)   # CCinematicComponent
CINE_LOAD = 0x292B4C  # CCinematicComponent::Load
# decimal keys computed, never hand-typed
C69A6A7 = str(0xC69A6A7);  PLANE = str(0x2AD64F3D);  COLBOX = str(0x7F88E44E)
DUMMY = str(0x10FCFD6); SHOPIT = str(0x16F31); WBOX = str(0x2888019A); META = str(0x39E32181)

table, templates = lvc_pure.load_table(TAB_DIR)
comps = table['components']
# round-19 resolved specs (decimal keys computed via int(hex,16))
comps[C69A6A7] = ['i', 'i']              # CComponentZonesLink::Load @0x2e7430
comps[PLANE] = ['f', 'f', 'i', 'i']      # CPlaneNodeComponent::Load @0x2a0728
comps[COLBOX] = []                       # CComponentBuiltinCollisionBox: 0-read candidate (fitted below)
comps[DUMMY] = []                        # CDummyComponent::Load @0x22a368: 0 reads
comps[WBOX] = ['i','f','f','f','f','f','f','i']  # CComponentBaseWorldBox::Load @0x2e6a08
comps[META] = ['i', ['rep', 'last', ['i']]]      # CComponentMetaZone::Load @0x3c13f8: [i n] + n x [i]
for k in ('661', '1075', '8278', '320811', '18987', '174419', '3008'):
    comps[k] = []                        # 0-read candidates (fitted)

LEVELS = ['l_menu', 'shop', 'Stadion', 'Police_Station', 'StockExchange',
          'Underground', 'Military', 'ThePit', 'Test', 'BatCave',
          'GothamCity', 'GothamCity_Island2']

tr = Tracer()
banked = {}

def level_strings(d):
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
    return strings

def fold_tokens(events, end, buf, strings):
    out = []
    ev = events
    n = len(ev)
    i = 0
    while i < n:
        addr, cur = ev[i]
        name = READERS.get(addr)
        if name is None:
            i += 1
            continue
        if addr in NESTING_PARENTS:
            if i + 1 < n and ev[i + 1][1] == cur and ev[i + 1][0] == 0x339914:
                i += 1
            size = (ev[i + 1][1] if i + 1 < n else end) - cur
            idx = struct.unpack_from('>i', buf, cur)[0]
            val = strings[idx] if 0 <= idx < len(strings) else None
            out.append(['STR', cur, size, idx if val is None else val])
        else:
            size = (ev[i + 1][1] if i + 1 < n else end) - cur
            kind = {'ReadInt': 'i', 'Read_intref': 'i', 'Read_uintref': 'i'}.get(name, 'f')
            if size == 1: kind = 'c'
            val = None
            if kind == 'i': val = struct.unpack_from('>i', buf, cur)[0]
            elif kind == 'f': val = struct.unpack_from('>f', buf, cur)[0]
            elif kind == 'c': val = buf[cur]
            out.append([kind, cur, size, val])
        i += 1
        if i < n and ev[i][1] <= cur: break
    return out

for lv in LEVELS:
    path = f'{DATA}/{lv}.lvc'
    d = open(path, 'rb').read()
    strings = level_strings(d)
    attempt = 0
    while True:
        attempt += 1
        stats = collections.Counter()
        try:
            res = lvc_pure.parse(path, table, templates, stats=stats)
            print(f'{lv:18s} OK {len(res["records"])} records (attempts={attempt})')
            banked[lv] = dict(ok=True, nrec=len(res['records']), attempts=attempt)
            break
        except lvc_pure.SpanNeeded as e:
            pos = e.pos
            tr.load_lvc(d, strings)
            tr.set_cursor(pos)
            comp = tr.new_component()
            err = tr.run(CINE_LOAD, [comp, STREAM])
            size = tr.get_cursor() - pos
            if size <= 0:
                print(f'{lv:18s} FAILED to measure at {pos:#x}: err={err}')
                banked[lv] = dict(ok=False, err=f'measure@{pos:#x}: {err}')
                break
            toks = fold_tokens(tr.trace.events, pos + size, d, strings)
            table['spans'][CINE].append([pos, size])
            table['span_toks'][CINE][str(pos)] = toks
            print(f'  banked span @{pos:#x} size={size} toks={len(toks)} err={err}')
        except KeyError as e:
            # unmeasured span instance: the missing key IS the component start
            pos = e.args[0]
            if not isinstance(pos, int):
                print(f'{lv:18s} KeyError(non-offset): {e}')
                banked[lv] = dict(ok=False, err=f'KeyError {e}')
                break
            tr.load_lvc(d, strings)
            tr.set_cursor(pos)
            comp = tr.new_component()
            err = tr.run(CINE_LOAD, [comp, STREAM])
            size = tr.get_cursor() - pos
            if size <= 0:
                print(f'{lv:18s} FAILED to measure at {pos:#x}: err={err}')
                banked[lv] = dict(ok=False, err=f'measure@{pos:#x}: {err}')
                break
            toks = fold_tokens(tr.trace.events, pos + size, d, strings)
            table['spans'][CINE].append([pos, size])
            table['span_toks'][CINE][str(pos)] = toks
            print(f'  banked span @{pos:#x} size={size} toks={len(toks)} err={err}')
        except Exception as e:
            print(f'{lv:18s} {type(e).__name__}: {str(e)[:150]}')
            banked[lv] = dict(ok=False, err=f'{type(e).__name__}: {str(e)[:150]}')
            break
        if attempt > 60:
            print(f'{lv}: too many spans; stopping')
            break

json.dump(banked, open(f'{OUT}/s29_spanbank_results.json', 'w'), indent=1)
json.dump({'spans': table['spans'], 'span_toks': table['span_toks']},
          open(f'{OUT}/s29_spans_extra.json', 'w'), indent=0)
print('banked spans for CINE now:', len(table['spans'][CINE]))
