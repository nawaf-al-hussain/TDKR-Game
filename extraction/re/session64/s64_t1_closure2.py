#!/usr/bin/env python3
"""S64 T1 step 8: apply the three code-derived spec fixes and re-run the FULL closure.
1. StateSet/SlowMotion: element = [i k, k x (i,i,f,f,i,c,c)] (no per-element param)
   - CAS disasm 0x3b61ec/0x3b62a0/0x3b63e4..0x3b6468/0x3b6494.
2. CameraParams (0x7d561d33 / reader 0x3bf038): insert c,c between the 3rd head int
   and the first STR (stream byte reads @0x3bf0e0/@0x3bf0f4) - 77 -> 79 B.
3. Glide (0x0110ce1f / reader 0x3c0938): 21 floats not 20 (read census + s55 reading)
   - 88 -> 92 B.
Nulls: perm / rot7 / ss-swap / param-restored (wrong-shape calibration)."""
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
E = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session64/s64_t1_final_specs.json'))

SS = '0x5441a117'
s1 = copy.deepcopy(E[SS])
c1 = s1[1][2][28][2]
e1 = c1[10][2]
if len(e1) >= 3 and e1[0] == 'i' and e1[2] == 'i':
    del e1[2]          # s63 shape -> code-exact (idempotent)
E[SS] = s1

# Camera fix: insert c,c after the 3 ints (position 11)
cam = list(E['0x7d561d33'])
assert cam[:11] == ['f'] * 8 + ['i'] * 3 and cam[11] == 'STR', cam[:13]
cam.insert(11, 'c')
cam.insert(12, 'c')
E['0x7d561d33'] = cam

# Glide fix: 21 floats (insert one more 'f' before the final int)
gl = list(E['0x0110ce1f'])
assert gl[0] == 'i' and gl[-1] == 'i' and gl.count('f') == 20
gl.insert(-1, 'f')
E['0x0110ce1f'] = gl

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
                                 'lastcomp': '0x%08x' % comps[-1]})
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
print('[S64 fixed] exact %d/653 (%.2f%%) pass %d/653 (%.2f%%) fail %d na %d' % (
    r['exact'], 100 * r['exact'] / 653, r['exact'] + r['bounds'],
    100 * (r['exact'] + r['bounds']) / 653, r['fail'], r['na']))
print('tails:', r['tails'])

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

s_swap = copy.deepcopy(E[SS])
cswap = s_swap[1][2][28][2]
cswap[4], cswap[6] = cswap[6], cswap[4]
E2 = dict(E); E2[SS] = s_swap
sub = [x for x in recs if x[1] in ('Helicopter', 'Helicopter_Bane', 'Military_Heli',
                                   'Test_Object', 'BatPod', 'TheBatDrive',
                                   'Batman_01_Movement', 'Enemy_Melee_Attack')]
r4 = do_walk(sub, E2, want_fails=True)
res['NULL_SS_SWAP'] = {'exact': r4['exact'], 'pass': r4['exact'] + r4['bounds'],
                       'fails': [f['name'] for f in r4['fails']]}
print('[NULL-ss-swap] exact %d pass %d fails %s' % (
    r4['exact'], r4['exact'] + r4['bounds'], res['NULL_SS_SWAP']['fails']))

E3 = dict(E)
s3 = copy.deepcopy(E[SS])
c3 = s3[1][2][28][2]
c3[10][2].append('i')
E3[SS] = s3
r5 = do_walk([x for x in recs if x[1] in ('Helicopter', 'Helicopter_Bane', 'Military_Heli',
                                          'Test_Object', 'BatPod', 'TheBatDrive',
                                          'Batman_01_Movement', 'Enemy_Melee_Movement')],
             E3, want_fails=True)
res['NULL_PARAM_RESTORED'] = {'exact': r5['exact'], 'pass': r5['exact'] + r5['bounds'],
                              'fails': [f['name'] for f in r5['fails']]}
print('[NULL-param-restored] exact %d pass %d fails %s (content templates must fail)' % (
    r5['exact'], r5['exact'] + r5['bounds'], res['NULL_PARAM_RESTORED']['fails']))

# camera/glide deliberate-wrong nulls: revert each fix on the calibration subset
E4 = dict(E)
E4['0x7d561d33'] = [t for i2, t in enumerate(cam) if i2 not in (11, 12)]
subc = [x for x in recs if x[1].startswith('Camera_1')][:8]
r6 = do_walk(subc, E4, want_fails=True)
res['NULL_CAM_REVERT'] = {'exact': r6['exact'], 'n': len(subc)}
print('[NULL-cam-revert] exact %d/%d (reverted camera must drop)' % (r6['exact'], len(subc)))
E5 = dict(E)
gl2 = list(gl); gl2.pop(-2)
E5['0x0110ce1f'] = gl2
subg = [x for x in recs if x[1] in ('Glider', 'Glider_Plunge')]
r7 = do_walk(subg, E5, want_fails=False)
res['NULL_GLIDE_REVERT'] = {'exact': r7['exact'], 'n': len(subg)}
print('[NULL-glide-revert] exact %d/%d (reverted glide must drop)' % (r7['exact'], len(subg)))

json.dump(res, open('/tmp/my-project/work/TDKR-Game/extraction/re/session64/s64_t1_closure.json', 'w'), indent=1)
json.dump(E, open('/tmp/my-project/work/TDKR-Game/extraction/re/session64/s64_t1_final_specs.json', 'w'), indent=1)
print('saved')
