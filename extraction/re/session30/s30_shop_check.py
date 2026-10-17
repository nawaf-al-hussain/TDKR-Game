#!/usr/bin/env python3
"""S30 T1b: shop walk vs the native engine walk (walk_records_shop.json),
with the corrected 0x4CA5F00E spec. Reports the first divergence and the
tail semantics."""
import json, struct, sys, collections

sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

tab = json.load(open('/tmp/my-project/work/re29/lvc_readseq_s30.json'))
templates = {int(k, 16): v for k, v in json.load(open(
    '/tmp/my-project/work/TDKR-Game/extraction/re/session26/'
    'lvc_gol_templates.json'))['templates'].items()}

d = open('/tmp/my-project/work/data/shop.lvc', 'rb').read()
table_off = struct.unpack_from('>I', d, 4)[0]
pos = table_off
nstr = struct.unpack_from('>i', d, pos)[0]; pos += 4
strings = []
for _ in range(nstr):
    ln = struct.unpack_from('>i', d, pos)[0]; pos += 4
    strings.append(d[pos:pos + ln].decode('utf-8', 'replace')); pos += ln

native = json.load(open('/tmp/my-project/work/walk_records_shop.json'))
nat = {int(x['off'], 16): x for x in native}

r = lvc_pure.Reader(d, strings)
records = []
cur = 17
match = mism = 0
first_mismatch = None
derail = None
try:
    while cur < table_off:
        rec_start = cur
        tid = struct.unpack_from('>i', d, cur)[0]
        r.p = cur
        if tid == -1:
            r.tok('i', None); kind = 'skip(-1)'
        elif str(tid) in tab['dedicated']:
            lvc_pure.replay(tab['dedicated'][str(tid)], r, None)
            kind = f'ded {tid:#x}'
        elif str(tid) in tab['engine_cases']:
            lvc_pure.replay(tab['engine_cases'][str(tid)], r, None)
            kind = f'eng {tid:#x}'
        elif tid in templates:
            comps = templates[tid]
            r.tok('i', None)
            for flag, ctid in comps:
                if flag:
                    continue
                spec = tab['components'].get(str(ctid))
                if spec is None:
                    raise RuntimeError(f'no spec for {ctid:#x} @{cur:#x}')
                lvc_pure.replay(spec, r, None)
            kind = f'tmpl {tid:#x}'
        else:
            r.tok('i', None); kind = f'skip {tid:#x}'
        cur = r.p
        records.append((rec_start, tid, cur, kind))
        if rec_start in nat:
            n = nat[rec_start]
            if int(n['end'], 16) == cur and int(n['tid'], 16) == (tid & 0xffffffff):
                match += 1
            else:
                mism += 1
                if first_mismatch is None:
                    first_mismatch = (len(records), hex(rec_start), hex(tid & 0xffffffff),
                                      hex(cur), n['tid'], n['end'], n['ok'])
except RuntimeError as e:
    derail = (rec_start, tid, str(e)[:120])

print(f'walked {len(records)} records; native-matched {match}, mismatched {mism}')
if first_mismatch:
    print('FIRST MISMATCH (rec#, off, our tid, our end, nat tid, nat end, nat ok):',
          first_mismatch)
if derail:
    print('RUNTIME ERROR (no spec):', derail)
print('native walk: 123 records, last end', native[-1]['end'],
      'ok', native[-1]['ok'])
tail = [x for x in native if int(x['off'], 16) >= 0x3ccc]
print(f'native tail records (>= 0x3ccc): {len(tail)}; all ok except last:',
      [(x['off'], x['tid'], x['ok']) for x in tail])
