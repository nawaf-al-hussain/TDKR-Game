#!/usr/bin/env python3
"""S61 T1 step 3: parse gol.bin with the ENGINE-TRUE layout (from GOM::Load disasm)
and census the id2 population vs the GCT case set (65 = 64 s60 + 0x222567e3).
Also: list1 vs list2 comparison, name census, category ids, carriers.
Outputs s61_t1_parse.json + console report.
"""
import struct, json, subprocess

GOL = '/home/z/my-project/work/data/gol.bin'
d = open(GOL, 'rb').read()
print(f"gol.bin {len(d)} B")

def u32(o):
    return struct.unpack_from('>I', d, o)[0]

def i32(o):
    return struct.unpack_from('>i', d, o)[0]

def u16(o):
    return struct.unpack_from('>H', d, o)[0]

# header per s57 parser: tableOff@4, nrec@13, offs@17
tableOff = u32(4)
nrec = u32(13)
offs = [u32(17 + 4 * i) for i in range(nrec)]
print(f"nrec {nrec}, tableOff {tableOff:#x}")
pos = tableOff
nstr = i32(pos)
pos += 4
strings = []
for i in range(nstr):
    l = i32(pos)
    pos += 4
    strings.append(d[pos:pos + l].decode('latin1'))
    pos += l
print(f"nstr {nstr}")

cases = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session60/s60_gct_cases.json'))
cases['0x222567e3'] = {"id": "0x222567e3", "note": "s61: found by exhaustive literal census, missed by s60"}
CASE_IDS = set(int(k, 0) for k in cases)

records = []
all_id2 = set()
all_list1 = set()
unknown = {}
for ri in range(nrec):
    ro = offs[ri]
    oid = u32(ro)
    m = i32(ro + 4)
    list1 = [u32(ro + 8 + 4 * k) for k in range(m)] if m > 0 else []
    p = ro + 8 + 4 * m
    n = u16(p)
    nameidx = u32(p + 2)
    name = strings[nameidx] if nameidx < nstr else f"<idx {nameidx}>"
    comps = []
    for ci in range(n):
        cid = u32(p + 6 + 6 * ci)
        flag = u16(p + 10 + 6 * ci)
        comps.append((cid, flag))
        all_id2.add(cid)
        if cid not in CASE_IDS:
            unknown[cid] = unknown.get(cid, 0) + 1
    for v in list1:
        all_list1.add(v)
    nxt = offs[ri + 1] if ri + 1 < nrec else len(d)
    records.append({'oid': oid, 'name': name, 'm': m, 'list1': list1, 'n': n,
                    'comps': comps, 'span': (p + 6 + 6 * n, nxt)})

print(f"\n=== id2 census ===")
print(f"distinct id2 values: {len(all_id2)}")
incase = sorted(v for v in all_id2 if v in CASE_IDS)
notin = sorted(all_id2 - CASE_IDS)
print(f"in 65-case set: {len(incase)} / {len(all_id2)}")
print(f"NOT in case set ({len(notin)}): {[hex(v) for v in notin[:40]]}")
print(f"\n=== list1 (m-list) census ===")
print(f"distinct list1 values: {len(all_list1)}")
l1_in = sorted(v for v in all_list1 if v in CASE_IDS)
print(f"in case set: {len(l1_in)}; sample of list1 values: {[hex(v) for v in sorted(all_list1)[:20]]}")
l1_notin = all_list1 - CASE_IDS
print(f"list1 not in case set: {len(l1_notin)}")

# list1 vs list2 relationship per record
same = sum(1 for r in records if [c[0] for c in r['comps']] == r['list1'])
print(f"records where list1 == comp-id list: {same}/{nrec}")
m_eq_n = sum(1 for r in records if r['m'] == r['n'])
print(f"records where m == n: {m_eq_n}/{nrec}")

# names
names = sorted(set(r['name'] for r in records))
print(f"\n=== names: {len(names)} distinct, sample: {names[:15]}")

# category / special ids
for cat in (0x3438ab08, 0x378ded9b, 0x163a6):
    n_have = sum(1 for r in records if any(c[0] == cat for c in r['comps']))
    n_isoid = sum(1 for r in records if r['oid'] == cat)
    print(f"{cat:#010x}: as-id2 in {n_have} records; as-oid {n_isoid}")

# templates fully in case set
pure = [r for r in records if all(c[0] in CASE_IDS for c in r['comps'])]
print(f"\ntemplates with ALL comps in 65-case set: {len(pure)}/{nrec}")
json.dump({'nrec': nrec, 'nstr': nstr,
           'records': [{'oid': hex(r['oid']), 'name': r['name'], 'm': r['m'],
                        'n': r['n'], 'comps': [[hex(a), hex(b)] for a, b in r['comps']],
                        'list1': [hex(v) for v in r['list1']]} for r in records],
           'unknown_id2': {hex(k): v for k, v in sorted(unknown.items())},
           'all_id2': [hex(v) for v in sorted(all_id2)]},
          open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_parse.json', 'w'), indent=1)
print("wrote s61_t1_parse.json")
