#!/usr/bin/env python3
"""S64 T1 step 5: FULL closure with the code-exact no-param SlowMotion element.
Spec change (code-derived, CAS disasm 0x3b61ec/0x3b62a0/0x3b63e4..0x3b6468/0x3b6494):
SlowMotion element = [i k, k x (i,i,f,f,i,c,c)] - the s63 trailing 'i' is removed.
Nulls: perm / rot7 / ss-shape-swap. Plus tail analysis for the tail classes."""
import struct, json, collections, random, copy

SRC = '/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_walker2.py'
exec(open(SRC).read().split('recs, strings = parse_gol()')[0])

def walk_spec(toks, buf, p, end):
    last = 0
    for t in toks:
        if isinstance(t, list):
            if t and t[0] == 'rep':
                n = last
                if n <= 0:
                    continue
                if n > 100000:
                    raise OOB()
                for _ in range(n):
                    p = walk_spec(t[2], buf, p, end)
                continue
            if t and t[0] == 'call':
                raise ValueError('call')
            if t and t[0] == 'inline':
                p = walk_spec(t[2], buf, p, end)
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
                    p = walk_spec([t[1]], buf, p, end)
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
        elif t == 'c':
            last = buf[p]
        elif t == 's':
            last = struct.unpack_from('>h', buf, p)[0]
        p += sz
    return p

recs, strings = parse_gol()
E = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session63/s63_t1_final_specs.json'))

# THE FIX (code-derived): SlowMotion element loses its trailing 'i'
SS = '0x5441a117'
s1 = copy.deepcopy(E[SS])
c1 = s1[1][2][28][2]
e1 = c1[10][2]
assert e1[0] == 'i' and e1[2] == 'i'
del e1[2]
E[SS] = s1

def do_walk(recs_, table, rot=0, want_fails=False, want_tailinfo=False):
    exact = bounds = fail = na = 0
    fails = []
    tails = collections.Counter()
    tailinfo = []
    for oid, name, comps, flags, payload in recs_:
        if rot:
            payload = payload[rot:] + payload[:rot]
        if not comps:
            na += 1
            continue
        p = 0; end = len(payload); reason = None
        try:
            for cid in comps:
                spec = table.get('0x%08x' % cid)
                if spec is None:
                    reason = 'nocase:%s' % cid; break
                p = walk_spec(spec, payload, p, end)
        except OOB:
            reason = 'OOB'
        except ValueError as e:
            reason = 'err:%s' % str(e)[:30]
        if reason:
            fail += 1
            fails.append({'name': name, 'reason': reason})
        elif p == end:
            exact += 1
        else:
            bounds += 1
            tails['tail:%d' % (end - p)] += 1
            if want_tailinfo:
                tailinfo.append({'name': name, 'tail': end - p,
                                 'lastcomp': '0x%08x' % comps[-1], 'ncomp': len(comps)})
    r = {'exact': exact, 'bounds': bounds, 'fail': fail, 'na': na,
         'tails': dict(tails.most_common(16))}
    if want_fails:
        r['fails'] = fails
    if want_tailinfo:
        r['tailinfo'] = tailinfo
    return r

res = {}
r = do_walk(recs, E, want_fails=True, want_tailinfo=True)
res['S64_ENGINE'] = r
print('[S64 no-param] exact %d/653 (%.1f%%) pass %d/653 (%.1f%%) fail %d na %d' % (
    r['exact'], 100 * r['exact'] / 653, r['exact'] + r['bounds'],
    100 * (r['exact'] + r['bounds']) / 653, r['fail'], r['na']))
print('tails:', r['tails'])
print('fails:', r['fails'][:10])

# tail:4 census
t4 = [t for t in r['tailinfo'] if t['tail'] == 4]
comp_dist = collections.Counter(t['lastcomp'] for t in t4)
print('tail:4 n=%d last-component census: %s' % (len(t4), dict(comp_dist.most_common(6))))
print('tail:4 names:', [t['name'] for t in t4][:30])

# nulls
random.seed(61)
ids = [k for k in E]
perm = ids[:]
random.shuffle(perm)
t2 = dict(zip(ids, [E[k] for k in perm]))
r2 = do_walk(recs, t2)
res['NULL_PERM'] = {'exact': r2['exact'], 'pass': r2['exact'] + r2['bounds']}
print('[NULL-perm] exact %d (real %d)' % (r2['exact'], r['exact']))

r3 = do_walk(recs, E, rot=7)
res['NULL_ROT7'] = {'exact': r3['exact'], 'pass': r3['exact'] + r3['bounds']}
print('[NULL-rot7] exact %d' % r3['exact'])

# ss-shape-swap null: swap l2/l3 shapes (wrong order must break content templates)
s_swap = copy.deepcopy(E[SS])
cswap = s_swap[1][2][28][2]
cswap[4], cswap[6] = cswap[6], cswap[4]     # l2 block <-> l3 block
E2 = dict(E); E2[SS] = s_swap
sub = [x for x in recs if x[1] in ('Helicopter', 'Helicopter_Bane', 'Military_Heli',
                                   'Test_Object', 'BatPod', 'TheBatDrive',
                                   'Batman_01_Movement', 'Enemy_Melee_Attack')]
r4 = do_walk(sub, E2, want_fails=True)
res['NULL_SS_SWAP'] = {'exact': r4['exact'], 'pass': r4['exact'] + r4['bounds'],
                       'fails': [f['name'] for f in r4['fails']]}
print('[NULL-ss-swap] exact %d pass %d fails %s' % (
    r4['exact'], r4['exact'] + r4['bounds'], res['NULL_SS_SWAP']['fails']))

# NEW null: restore the param (the s63 shape) - the deliberate-wrong calibration case
E3 = dict(E)
s3 = copy.deepcopy(E[SS])
c3 = s3[1][2][28][2]
e3 = c3[10][2]
e3.append('i')
E3[SS] = s3
r5 = do_walk([x for x in recs if x[1] in ('Helicopter', 'Helicopter_Bane', 'Military_Heli',
                                          'Test_Object', 'BatPod', 'TheBatDrive',
                                          'Batman_01_Movement', 'Enemy_Melee_Movement')],
             E3, want_fails=True)
res['NULL_PARAM_RESTORED'] = {'exact': r5['exact'], 'pass': r5['exact'] + r5['bounds'],
                              'fails': [f['name'] for f in r5['fails']]}
print('[NULL-param-restored] exact %d pass %d fails %s (content templates must fail)' % (
    r5['exact'], r5['exact'] + r5['bounds'], res['NULL_PARAM_RESTORED']['fails']))

json.dump(res, open('/tmp/my-project/work/TDKR-Game/extraction/re/session64/s64_t1_closure.json', 'w'), indent=1)
json.dump(E, open('/tmp/my-project/work/TDKR-Game/extraction/re/session64/s64_t1_final_specs.json', 'w'), indent=1)
print('saved')
