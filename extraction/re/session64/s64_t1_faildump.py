#!/usr/bin/env python3
"""S64 T1 step 1: instrumented fail dump for the 13 OOB templates.
Reuses the s63 closure machinery (same specs, zero fitted rules) and reports
WHERE each walk dies: component index, payload offset, remaining bytes,
last walk tokens, and a hex dump at the failure point."""
import struct, json, sys

SRC = '/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py'
exec(open(SRC).read().split('recs, strings = parse_gol()')[0])

class OOB(Exception):
    pass

def walk_spec(toks, buf, p, end, log=None, strs=None):
    last = 0
    for t in toks:
        if isinstance(t, list):
            if t and t[0] == 'rep':
                n = last
                if log is not None:
                    log.append(['rep%d' % n, repr(t)[:50], p])
                if n <= 0:
                    continue
                if n > 100000:
                    raise OOB()
                for _ in range(n):
                    p = walk_spec(t[2], buf, p, end, log, strs)
                continue
            if t and t[0] == 'call':
                raise ValueError('call')
            if t and t[0] == 'inline':
                p = walk_spec(t[2], buf, p, end, log, strs)
                continue
            if len(t) == 1 and isinstance(t[0], str) and t[0] in NAT:
                t = t[0]
            elif len(t) == 2 and isinstance(t[0], str) and t[0] in NAT and isinstance(t[1], int):
                if p + t[1] > end:
                    raise OOB()
                p += t[1]
                last = 0
                continue
            elif len(t) >= 3 and t[0] == 'fat':
                for _ in range(t[2]):
                    p = walk_spec([t[1]], buf, p, end, log, strs)
                last = 0
                continue
            else:
                raise ValueError('tok %r' % (t,))
        sz = NAT.get(t)
        if sz is None:
            raise ValueError('tok %r' % (t,))
        if p + sz > end:
            raise OOB()
        if t == 'i':
            last = struct.unpack_from('>i', buf, p)[0]
            if log is not None:
                log.append(['i=%d' % last, '', p])
        elif t == 'c':
            last = buf[p]
            if log is not None:
                log.append(['c=%d' % last, '', p])
        elif t == 's':
            last = struct.unpack_from('>h', buf, p)[0]
            if log is not None:
                log.append(['s=%d' % last, '', p])
        elif t == 'STR':
            idx = struct.unpack_from('>I', buf, p)[0]
            sv = ''
            if strs is not None and idx < len(strs):
                sv = strs[idx][:24]
            if log is not None:
                log.append(['STR#%d%s' % (idx, ('=' + sv) if sv else ''), '', p])
        if log is not None and log and log[-1][0][0] not in ('i', 'c', 's', 'S'):
            pass
        p += sz
    return p

recs, strings = parse_gol()
specs61 = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_reader_specs.json'))
plan = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session62/s62_t1_specplan.json'))
by_reader = {}
for k, v in specs61.items():
    by_reader[int(v['reader'], 16)] = v['spec']
D64 = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session63/s63_t1_final_specs.json'))
E = D64  # the exact committed table

FAILS = ['Batman_01_Movement', 'Batman_02_Flying', 'Batman_04_Combat', 'Batman_08_Takedown',
         'Batman_30_Combat_Strike1', 'Batman_31_Combat_Strike2', 'Batman_32_Combat_Strike3',
         'Batman_33_Combat_HeavyStrike', 'Batman_39_Combat_CounterStrike',
         'Enemy_Melee_Attack', 'Enemy_Melee_Hurt', 'Enemy_Melee_Movement', 'Enemy_Ranged_Hurt']

out = {}
for oid, name, comps, flags, payload in recs:
    if name not in FAILS:
        continue
    p = 0; end = len(payload); rec = {'size': end, 'ncomp': len(comps), 'comps': []}
    for ci, cid in enumerate(comps):
        key = '0x%08x' % cid
        spec = E.get(key)
        if spec is None:
            rec['comps'].append({'i': ci, 'id': key, 'err': 'nocase'})
            p = None
            break
        log = []
        p0 = p
        try:
            p = walk_spec(spec, payload, p, end, log, strings)
            rec['comps'].append({'i': ci, 'id': key, 'p0': p0, 'p1': p, 'ok': True})
        except OOB:
            lastp = p0
            for entry in log:
                try:
                    if entry[2] > lastp:
                        lastp = entry[2]
                except Exception:
                    pass
            tail = payload[lastp:lastp + 48]
            before = payload[max(0, lastp - 32):lastp]
            rec['comps'].append({'i': ci, 'id': key, 'p0': p0, 'err': 'OOB',
                                 'lastpos': lastp, 'remaining': end - lastp,
                                 'hex': tail.hex(), 'hex_before': before.hex(),
                                 'lastlog': log[-25:]})
            p = None
            break
        except Exception as e:
            rec['comps'].append({'i': ci, 'id': key, 'p0': p0, 'err': str(e)[:60]})
            p = None
            break
    if p == end:
        rec['verdict'] = 'EXACT'
    out[name] = rec

for name, rec in out.items():
    print('==', name, 'payload', rec['size'], 'B,', rec['ncomp'], 'comps ->', rec.get('verdict'))
    for c in rec['comps']:
        if c.get('ok'):
            print('   comp %d %s ok %d..%d' % (c['i'], c['id'], c['p0'], c['p1']))
        elif 'lastpos' in c:
            print('   comp %d %s OOB at %d (remaining %d)' % (c['i'], c['id'], c['lastpos'], c['remaining']))
            print('   before:', c['hex_before'])
            print('   at    :', c['hex'])
            for lg in c['lastlog']:
                print('     %6d  %s %s' % (lg[2], lg[0][:28], lg[1][:40]))
        else:
            print('   comp %d %s ERR %s' % (c['i'], c['id'], c.get('err')))

json.dump(out, open('/tmp/my-project/work/TDKR-Game/extraction/re/session64/s64_t1_faildump.json', 'w'), indent=1)
print('saved s64_t1_faildump.json')
