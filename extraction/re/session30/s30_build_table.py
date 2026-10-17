#!/usr/bin/env python3
"""S30 T1: build the canonical read-sequence table (lvc_readseq_s30.json):
  - all round-19 component specs (from s29_final_run.py)
  - CCinematicComponent 0x17AC851F: STATIC spec from disassembly
    (CComponentCinematic::Load @0x2dce20 + CContainerTracksAnimatedObject::Load
     @0x2d9118) replacing the 96 measured spans
  - validate all 12 levels with the pure parser
"""
import json, struct, sys, collections

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

TAB26 = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_readseq.json'
S29 = '/tmp/my-project/work/re29/lvc_readseq_s29.json'
OUT = '/tmp/my-project/work/re29/lvc_readseq_s30.json'

CINE = '397182239'

# static spec (s30_cine_validate.py CCINEMATIC)
CCINEMATIC = [
    ['i'], ['c'], ['f'], ['c'],
    ['i'],
    ['rep', 'last', [
        ['i'], ['i'],
        ['rep', 'last', [['i'], ['i'], ['i'], ['i']]],
    ]],
    ['i'],
    ['rep', 'last', [
        ['i'],
        ['rep', 'last', [['i'], ['i'], ['STR'], ['c']]],
    ]],
    ['i'],
    ['rep', 'last', [
        ['i'],
        ['rep', 'last', [['i'], ['i'], ['STR']]],
    ]],
    ['i'],
    ['rep', 'last', [
        ['STR'], ['i'],
        ['rep', 'last', [['i'], ['i'], ['f'], ['f'], ['f'],
                         ['f'], ['f'], ['f']]],
    ]],
    ['i'],
    ['rep', 'last', [
        ['i'],                                   # A
        ['i'],                                   # B
        ['rep', 'last', [['STR'], ['i'], ['f'], ['i'], ['i']]],
        ['i'],                                   # C
        ['rep', 'last', [
            ['STR'], ['i'],
            ['rep', 'last', [['f'], ['f'], ['f'], ['i'], ['i']]],
        ]],
        ['i'],                                   # D
        ['rep', 'last', [
            ['STR'], ['i'],
            ['rep', 'last', [['STR'], ['f'], ['f'], ['f'], ['i'], ['i']]],
        ]],
        ['i'],                                   # E
        ['rep', 'last', [
            ['STR'], ['i'],
            ['rep', 'last', [['f'], ['f'], ['f'], ['i'], ['i']]],
        ]],
        ['i'],                                   # F
        ['rep', 'last', [
            ['i'],
            ['rep', 'last', [['i'], ['i'], ['STR']]],
        ]],
        ['i'],                                   # G
        ['rep', 'last', [
            ['i'],
            ['rep', 'last', [['STR'], ['i'], ['i'], ['STR'], ['c']]],
        ]],
        ['i'],                                   # H
        ['rep', 'last', [
            ['i'],
            ['rep', 'last', [['i'], ['i'], ['STR'], ['STR'], ['c'],
                             ['f'], ['c'], ['c']]],
        ]],
    ]],
]


def build():
    tab = json.load(open(TAB26))
    # ensure r19 specs present (idempotent)
    comps = tab['components']
    comps[str(0xC69A6A7)] = ['i', 'i']
    comps[str(0x2AD64F3D)] = ['f', 'f', 'i', 'i']
    comps[str(0x10FCFD6)] = []
    comps[str(0x2888019A)] = ['i', 'f', 'f', 'f', 'f', 'f', 'f', 'i']
    comps[str(0x39E32181)] = ['i', ['rep', 'last', ['i']]]
    comps[str(0x7F88E44E)] = []
    for k in ('661', '1075', '8278', '320811', '18987', '174419', '3008'):
        comps.setdefault(k, [])
    comps.setdefault('491825779', [])   # 0x1D50AA73 unregistered (r19 positive-controlled)
    # s30: shop NewShopItemProperty item loop (from @0x202ae4, Load slot vt+0x10)
    comps[str(0x4CA5F00E)] = [
        ['i'], ['STR'], ['STR'], ['i'], ['i'], ['f'], ['f'], ['f'],
        ['c'], ['c'], ['c'], ['c'],
        ['i'],
        ['rep', 'last', [
            ['c'], ['i'], ['i'], ['f'], ['f'], ['f'], ['f'],
            ['STR'], ['STR'], ['STR'], ['STR'], ['i'], ['c'], ['i'], ['c'],
        ]],
    ]
    # s30: LevelInit trailing word UNCONDITIONAL (0x20240c), replacing i_nz
    spec9815 = tab['engine_cases'].get('9815')
    if spec9815 and spec9815[-1] and spec9815[-1][0] == 'i_nz':
        spec9815[-1] = ['i', 4]
    # s30: CTrafficSetting static spec (@0x1ffa1c..0x1ffeb4)
    tab['components']['831119443'] = [
        ['i'], ['c'], ['f'], ['f'], ['f'], ['STR'],
        ['f'], ['f'], ['f'], ['f'], ['f'], ['f'],
        ['i'],
        ['rep', 'last', [['i'], ['i'], ['i']]],
        ['i'],
        ['rep', 'last', [
            ['i'], ['i'], ['i'],
            ['rep', 'last', [['STR'], ['f']]],
            ['i'],
        ]],
    ]
    tab.get('spans', {}).pop('831119443', None)
    tab.get('span_toks', {}).pop('831119443', None)
    # replace the cinematic span spec with the static one
    tab['components'][CINE] = CCINEMATIC
    # drop per-instance span bookkeeping for the class (keep other classes)
    tab.get('spans', {}).pop(CINE, None)
    tab.get('span_toks', {}).pop(CINE, None)
    meta = tab.setdefault('meta', {})
    meta['cine_static'] = {
        'class': 'CCinematicComponent 0x17AC851F',
        'derived_from': [
            'CComponentCinematic::Load @0x2dce20..0x2ddf8c (ret)',
            'CContainerTracksAnimatedObject::Load @0x2d9118..0x2dad20 (ret)',
        ],
        'sections': 'head[i,c,f,c]; n1 x{i,i,cnt x i4}; n2 x{i,cnt x i,i,STR,c};'
                    ' n3 x{i,cnt x i,i,STR}; n4 x{STR,i,cnt x i,i,f6};'
                    ' n5 x ContTracks{A;B x STR,i,f,i,i; C x STR,i,cnt x f,f,f,i,i;'
                    ' D x STR,i,cnt x STR,f,f,f,i,i; E x STR,i,cnt x f,f,f,i,i;'
                    ' F x i,cnt x i,i,STR; G x i,cnt x STR,i,i,STR,c;'
                    ' H x i,cnt x i,i,STR,STR,c,f,c,c}',
    }
    json.dump(tab, open(OUT, 'w'), indent=0)
    print('wrote', OUT)
    return tab


def main():
    tab = build()
    templates = {int(k, 16): v for k, v in
                 json.load(open('/tmp/my-project/work/TDKR-Game/extraction/'
                                're/session26/lvc_gol_templates.json'))['templates'].items()}
    import glob
    levels = sorted(glob.glob('/tmp/my-project/work/data/*.lvc'))
    for path in levels:
        name = path.rsplit('/', 1)[1][:-4]
        try:
            tokens = []
            res = lvc_pure.parse(path, tab, templates, tokens, collections.Counter())
            last = res['records'][-1]
            nrec = len(res['records'])
            complete = last[3] == res['table_off']
            print(f'{name:22s} {nrec:6d} records  end {last[3]:#x} '
                  f'table {res["table_off"]:#x}  {"OK" if complete else "MISMATCH"}')
        except lvc_pure.SpanNeeded as e:
            print(f'{name:22s} SPAN NEEDED @ {e.pos:#x}')
        except Exception as e:
            print(f'{name:22s} {type(e).__name__}: {str(e)[:120]}')


if __name__ == '__main__':
    main()
