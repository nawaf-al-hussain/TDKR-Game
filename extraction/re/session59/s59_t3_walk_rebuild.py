#!/usr/bin/env python3
"""s59 T3: rebuild the gol structural walker (s57/s58 method, scripts were lost).
Base = lvc_readseq_s30.json (78 comps, rep tokens); overrides = the ENGINE-derived
template sequences documented in s57/s58 notes. Calibration target: 326/653 ok,
30/50 carriers (s58). Then blocker breakdown + fractions."""
import struct, json, collections

GOL = '/tmp/my-project/work/data/gol.bin'
RS = json.load(open('/tmp/my-project/work/ghpages_mig_wt/playable/lvc_readseq_s30.json'))
COMPONENTS = {}
for k, v in RS['components'].items():
    try: COMPONENTS[int(k)] = v
    except ValueError: pass
NAT = {'i': 4, 'f': 4, 'c': 1, 'B': 1, 's': 2, 'STR': 4}
HEALTH_ID, AWARE_ID = 0x0ddcd6c4, 0x6754056b

# s57/s58 ENGINE-derived TEMPLATE sequences (override the lvc instance shapes):
OVR = {
    0x5441a117: ['STR']*8,                                        # StateSet template: 8 string indices
    0x3ef5108d: ['rep1', ['i'], [['i', 'i']]],                    # DropCollectible i + n*(i,i)
    0x44c6e9e5: ['i'] + ['c']*6 + ['i']*4 + ['f']*3,              # NpcAI 38 B
    0x3e2bb040: ['i', 'i', 'f', 'i'],                             # WantedGenerator 16 B
    0x54989cb1: ['c']*3 + ['f']*16 + ['c']*3 + ['i', 'cnt', 'repab'],  # ActorBase 78+5n
    0x592ce07c: ['c', 'f', 'f', 'c', 'f', 'f'],                   # Motion 18 B
    0x40c6b80a: ['CUST'],                                         # CustomizeActor exact walk
    0x2db081e2: ['raw16'],                                        # Collision template = 16-B base flat
    0x33702f4a: ['f']*5,                                          # Sniper 20 B
    HEALTH_ID: ['f', 'c', 'i', 'i'],                              # Health 13 B (f@0, c, i1, i2)
    AWARE_ID: ['f']*16,                                           # Awareness 64 B
}
for k, v in OVR.items(): COMPONENTS[k] = v

class R:
    __slots__ = ('p', 'nstr')
    def __init__(self, p): self.p = p; self.nstr = 0

def walk(payload, p, toks):
    """returns (ok, endpos). STR = 4-B BE string-table index."""
    for t in toks:
        if isinstance(t, list):  # rep form from s30: ['rep','last',[...]]
            k = t[0]
            if k == 'rep':
                return (False, p)  # s30 rep handled only via special keys below
        k = t
        if k == 'raw16': p += 16
        elif k == 'CUST':
            # i(n) + n*(STR,STR,STR,i(m),m*STR) + i + i
            if p + 4 > len(payload): return (False, p)
            n = struct.unpack_from('>i', payload, p)[0]; p += 4
            if n < 0 or n > 64: return (False, p)
            for _ in range(n):
                for _ in range(3):
                    if p + 4 > len(payload): return (False, p)
                    p += 4  # STR index
                if p + 4 > len(payload): return (False, p)
                m = struct.unpack_from('>i', payload, p)[0]; p += 4
                if m < 0 or m > 256: return (False, p)
                p += 4 * m
            if p + 8 > len(payload): return (False, p)
            p += 8
        elif k == 'repab':  # ActorBase tail: count read earlier in 'cnt'; n*(i + c)
            # uses last 'cnt' value passed via closure — handled by caller inline
            return (False, p)
        elif k == 'cnt' or k == 'rep1':
            return (False, p)  # handled inline by caller
        elif k in NAT: p += NAT[k]
        else: return (False, p)
    return (True, p)

def walk_actorbase(payload, p):
    # c*3, f*16, c*3, i, i=count, count*(i + c)
    p += 3 + 64 + 3
    if p + 8 > len(payload): return (False, p, 0)
    cnt = struct.unpack_from('>i', payload, p + 4)[0]
    if cnt < 0 or cnt > 4096: return (False, p, 0)
    p += 8
    p += 5 * cnt
    if p > len(payload): return (False, p, cnt)
    return (True, p, cnt)

def walk_dropcoll(payload, p):
    if p + 4 > len(payload): return (False, p)
    n = struct.unpack_from('>i', payload, p)[0]; p += 4
    if n < 0 or n > 4096: return (False, p)
    p += 8 * n
    return (p <= len(payload), p)

def walk_comp(cid, payload, p):
    spec = COMPONENTS.get(cid)
    if spec is None: return (False, p, 'unknown')
    try:
        if cid == 0x54989cb1:
            ok, p2, _ = walk_actorbase(payload, p)
            return (ok, p2, None)
        if cid == 0x3ef5108d:
            ok, p2 = walk_dropcoll(payload, p)
            return (ok, p2, None)
        # generic list (with s30 rep tokens flattened where 'last'-driven)
        if spec and isinstance(spec, list) and spec and isinstance(spec[0], list) and spec[0][0] == 'rep':
            # rep-driven s30 spec: ['rep','last',[body]] — count = the int just read before? s30
            # semantics: rep 'last' = repeat count = the LAST read int field. Implement generic.
            r = Rep(payload, p)
            r.run(spec)
            return (True, r.p, None)
        ok, p2 = walk(payload, p, spec)
        return (ok, p2, None)
    except Exception:
        return (False, p, 'exc')

class Rep:
    def __init__(self, buf, p): self.buf = buf; self.p = p; self.last = 0
    def run(self, spec):
        for tok in spec:
            if tok[0] == 'rep':
                cnt = self.last if tok[1] == 'last' else 0
                for _ in range(max(cnt, 0)):
                    self.run(tok[2])
            else:
                k = tok[0]; sz = tok[1] if len(tok) > 1 else NAT.get(k, 4)
                if k == 'STR':
                    self.p += 4
                    self.last = struct.unpack_from('>i', self.buf, self.p - 4)[0]
                elif k in ('i', 'f', 'u'):
                    self.p += 4
                    self.last = struct.unpack_from('>i', self.buf, self.p - 4)[0]
                elif k in ('c', 'B'): self.p += 1
                elif k == 's': self.p += 2
                else: raise ValueError(k)

d = open(GOL, 'rb').read()
assert d[:4] == b'DICT'
table_off = struct.unpack_from('>I', d, 4)[0]
nrec = struct.unpack_from('>I', d, 13)[0]
offs = [struct.unpack_from('>I', d, 17 + 4*i)[0] for i in range(nrec)]
# string table: strings live after the table? (s56: strings[] read from header area)
# s56 read: l = BE i; text — starting right after the offs table? find: strings begin at table_off
strings = []
sp = table_off
while sp < len(d) and len(strings) < 20000:
    if sp + 4 > len(d): break
    l = struct.unpack_from('>i', d, sp)[0]
    if l < 0 or l > 200 or sp + 4 + l > len(d): break
    strings.append(d[sp+4:sp+4+l].decode('utf-8', 'replace')); sp += 4 + l

ok_n = 0; fails = []; carriers_ok = 0; carriers_n = 0; cfails = []
blockers = collections.Counter()
for ri in range(nrec):
    ro = offs[ri]
    oid = struct.unpack_from('>I', d, ro)[0]
    m = struct.unpack_from('>I', d, ro+4)[0]
    p = ro + 8 + 4*m
    n = struct.unpack_from('>H', d, p)[0]
    nameidx = struct.unpack_from('>I', d, p+2)[0]
    nm = strings[nameidx] if 0 <= nameidx < len(strings) else f'?{nameidx}'
    nxt = offs[ri+1] if ri+1 < nrec else len(d)
    payload = d[p+6+6*n:nxt]
    comps = [struct.unpack_from('>IH', d, p+6+6*ci) for ci in range(n)]
    pos = 0; okall = True; why = None
    has_ha = any(c[0] == HEALTH_ID for c in comps) and any(c[0] == AWARE_ID for c in comps)
    for ci, (cid, x) in enumerate(comps):
        okc, p2, tag = walk_comp(cid, payload, pos)
        if not okc:
            okall = False
            why = f'comp {hex(cid)} FAIL@{pos}' + (f' ({tag})' if tag else '')
            blockers[hex(cid)] += 1
            break
        pos = p2
    if okall and pos != len(payload):
        okall = False
        why = f'len-mismatch walked={pos} payload={len(payload)}'
        blockers['LEN-MISMATCH'] += 1
    if has_ha: carriers_n += 1
    if okall:
        ok_n += 1
        if has_ha: carriers_ok += 1
    else:
        fails.append([nm, hex(oid), [why]])
        if has_ha: cfails.append([nm, hex(oid), [why]])

print(f'walk: {ok_n}/{nrec} templates close; carriers {carriers_ok}/{carriers_n}')
print('top blockers:', blockers.most_common(12))
json.dump({'ok': ok_n, 'n': nrec, 'carriers_ok': carriers_ok, 'carriers_n': carriers_n,
           'blockers': blockers.most_common(), 'fails': fails[:40], 'cfails': cfails[:40]},
          open('/home/z/my-project/scripts/s59_t3_walk_out.json', 'w'), indent=1)
