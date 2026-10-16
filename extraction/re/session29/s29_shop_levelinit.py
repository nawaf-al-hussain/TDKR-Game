#!/usr/bin/env python3
"""S29 T1: natively measure shop's LevelInit record (differs from islands); bank span."""
import sys, struct, json, collections
sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session25')
import lvc_pure
from lvc_tracer import Tracer, STREAM, READERS, NESTING_PARENTS

DATA = '/tmp/my-project/work/data'
LV_INIT_LOAD = 0x2018F0  # CComponentLevelInit::Load

d = open(f'{DATA}/shop.lvc', 'rb').read()
table_off = struct.unpack_from('>I', d, 4)[0]
nstr = struct.unpack_from('>i', d, table_off)[0]
pos = table_off + 4
strings = []
for i in range(nstr):
    ln = struct.unpack_from('>i', d, pos)[0]; pos += 4
    strings.append(d[pos:pos + ln].decode('utf-8', 'replace')); pos += ln

tr = Tracer()
tr.load_lvc(d, strings)
tr.set_cursor(0x15)          # after the tid (record starts 0x11, tid 4 B)
comp = tr.new_component()
err = tr.run(LV_INIT_LOAD, [comp, STREAM])
size = tr.get_cursor() - 0x15
print(f'shop LevelInit::Load: err={err} size={size} -> record end {0x15+size:#x} (native said 0x146)')
# fold tokens
def fold_tokens(events, end, buf, strs):
    out = []
    ev = events; n = len(ev); i = 0
    while i < n:
        addr, cur = ev[i]
        name = READERS.get(addr)
        if name is None: i += 1; continue
        if addr in NESTING_PARENTS:
            if i + 1 < n and ev[i + 1][1] == cur and ev[i + 1][0] == 0x339914: i += 1
            sz = (ev[i + 1][1] if i + 1 < n else end) - cur
            idx = struct.unpack_from('>i', buf, cur)[0]
            val = strs[idx] if 0 <= idx < len(strs) else None
            out.append(['STR', cur, sz, idx if val is None else val])
        else:
            sz = (ev[i + 1][1] if i + 1 < n else end) - cur
            kind = {'ReadInt': 'i', 'Read_intref': 'i', 'Read_uintref': 'i'}.get(name, 'f')
            if sz == 1: kind = 'c'
            val = None
            if kind == 'i': val = struct.unpack_from('>i', buf, cur)[0]
            elif kind == 'f': val = struct.unpack_from('>f', buf, cur)[0]
            elif kind == 'c': val = buf[cur]
            out.append([kind, cur, sz, val])
        i += 1
        if i < n and ev[i][1] <= cur: break
    return out

toks = fold_tokens(tr.trace.events, 0x15 + size, d, strings)
print(f'tokens: {len(toks)}; first 8: {[t[0] for t in toks[:8]]}')

# bank into engine_cases as span for shop's table_off
TAB_DIR = '/tmp/my-project/work/TDKR-Game/extraction/re/session26'
table = json.load(open(f'{TAB_DIR}/lvc_readseq.json'))
table.setdefault('span_toks_e', {}).setdefault('9815', {})
table.setdefault('spans_e', {}).setdefault('9815', {})
tid = '9815'  # 0x2657
full_toks = [['i', 0x11, 4, 9815]] + toks
table['span_toks_e'][tid][str(table_off)] = full_toks
table['spans_e'][tid][str(table_off)] = 4 + size
print('spans_e for 0x2657 now:', {k: v for k, v in table['spans_e'][tid].items()})
json.dump({'spans_e': table['spans_e'], 'span_toks_e': table['span_toks_e']},
          open('/tmp/my-project/work/re29/s29_spans_e_shop.json', 'w'), indent=0)
print('banked to s29_spans_e_shop.json')
