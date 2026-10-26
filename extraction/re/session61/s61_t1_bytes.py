#!/usr/bin/env python3
"""S61 T1 step 12: byte-level ground truth on gol.bin records.
Dump raw layout of: a pure (all-cased) record, the 0x378ded9b vehicle record,
the Bane template, the Merc template. Test alternative readings of the pairs region."""
import struct, json

d = open('/home/z/my-project/work/data/gol.bin', 'rb').read()
tableOff = struct.unpack_from('>I', d, 4)[0]
nrec = struct.unpack_from('>I', d, 13)[0]
offs = [struct.unpack_from('>I', d, 17 + 4 * i)[0] for i in range(nrec)]
pos = tableOff
nstr = struct.unpack_from('>i', d, pos)[0]
pos += 4
strings = []
for i in range(nstr):
    l = struct.unpack_from('>i', d, pos)[0]
    pos += 4
    strings.append(d[pos:pos + l].decode('latin1'))
    pos += l

cases = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session60/s60_gct_cases.json'))
CASE_IDS = set(int(k, 0) for k in cases)

recs = []
for ri in range(nrec):
    ro = offs[ri]
    oid = struct.unpack_from('>I', d, ro)[0]
    m = struct.unpack_from('>i', d, ro + 4)[0]
    p = ro + 8 + 4 * m
    n = struct.unpack_from('>H', d, p)[0]
    nameidx = struct.unpack_from('>I', d, p + 2)[0]
    comps = [(struct.unpack_from('>I', d, p + 6 + 6 * ci)[0],
              struct.unpack_from('>H', d, p + 10 + 6 * ci)[0]) for ci in range(n)]
    recs.append((ri, oid, m, p, n, nameidx, comps, ro))

def show(label, want=None):
    for (ri, oid, m, p, n, nameidx, comps, ro) in recs:
        nm = strings[nameidx] if nameidx < nstr else '?'
        hit = (want == 'pure' and all(c[0] in CASE_IDS for c in comps) and len(comps) >= 2) or \
              (want == 'vehicle' and any(c[0] == 0x378ded9b for c in comps)) or \
              (want and nm == want)
        if not hit:
            continue
        nxt = offs[ri + 1] if ri + 1 < nrec else len(d)
        print(f"\n=== {label}: [{ri}] oid {oid:#x} name {nm!r} m {m} n {n} span {ro:#x}..{nxt:#x}")
        print(f"  list1: {[hex(struct.unpack_from('>I', d, ro+8+4*k)[0]) for k in range(m)]}")
        print(f"  @p {p:#x}: u16 n = {n}, nameidx = {nameidx}")
        for ci, (cid, flag) in enumerate(comps):
            csym = 'cased' if cid in CASE_IDS else 'UNKNOWN'
            print(f"    comp[{ci}] id {cid:#010x} flag {flag:#06x}  {csym}")
        # payload region after pairs
        ps = p + 6 + 6 * n
        print(f"  payload {ps:#x}..{nxt:#x} ({nxt-ps} B): {d[ps:ps+48].hex(' ')[:94]}")
        return

show('PURE (first all-cased)', 'pure')
show('VEHICLE (0x378ded9b)', 'vehicle')
show('Bane', 'Bane')
show('Merc?', 'Bane_Movement')

# Alternative reading test on the vehicle record: are the "unknown" ids maybe (u16,u16) pairs?
# and does the m-list perhaps contain the TRUE class ids?
for (ri, oid, m, p, n, nameidx, comps, ro) in recs:
    nm = strings[nameidx] if nameidx < nstr else '?'
    if nm == 'Police_Car':
        nxt = offs[ri + 1] if ri + 1 < nrec else len(d)
        print(f"\n=== Police_Car [{ri}] oid {oid:#x} m {m} n {n}")
        print(f"  list1: {[hex(struct.unpack_from('>I', d, ro+8+4*k)[0]) for k in range(m)]}")
        print(f"  comps: {[(hex(a), hex(b)) for a, b in comps]}")
        print(f"  raw @ro: {d[ro:ro+8+4*m].hex(' ')}")
        print(f"  raw @p..: {d[p:p+6+6*n].hex(' ')}")
        break
