#!/usr/bin/env python3
"""S61 T1 step 9: scan every .gla archive for embedded gol streams (IDCT / OG magic)
and census the comp-id population of each gol found.
Determines: which gol does GOM::Load consume; is there a per-level gol with all-cased ids?"""
import zipfile, struct, io, json, subprocess

ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
PREFIX = 'com.gameloft.android.AMAZ.GloftKRAS/files/'

z = zipfile.ZipFile(ZIP)
names = [n for n in z.namelist() if n.endswith('.gla')]
print(f"{len(names)} .gla members")

cases = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session60/s60_gct_cases.json'))
cases['0x222567e3'] = {}
CASE_IDS = set(int(k, 0) for k in cases)

def parse_gol(d, label):
    """Parse a gol stream with the engine layout; return census."""
    if len(d) < 21:
        return None
    magic = d[0:4]
    if magic == b'IDCT':
        pass
    elif magic[0:2] == b'OG' and struct.unpack_from('>H', d, 2)[0] == 3:
        pass
    else:
        return None
    # header per s57: tableOff u32 @4, nrec u32 @13, offs @17
    # but wait: engine reads: magic(4B via ReadInt) then... the OG path reads u16 OG + u16 ver(3).
    # s57: tableOff@4, nrec@13, offs@17 — implies header: magic4 + tableoff4 + ???5 bytes + nrec4
    tableOff = struct.unpack_from('>I', d, 4)[0]
    nrec = struct.unpack_from('>I', d, 13)[0]
    if nrec <= 0 or nrec > 100000 or tableOff >= len(d):
        return None
    offs = [struct.unpack_from('>I', d, 17 + 4 * i)[0] for i in range(nrec)]
    pos = tableOff
    nstr = struct.unpack_from('>i', d, pos)[0]
    pos += 4
    strings = []
    ok = True
    try:
        for i in range(nstr):
            l = struct.unpack_from('>i', d, pos)[0]
            pos += 4
            if l < 0 or pos + l > len(d):
                ok = False
                break
            strings.append(d[pos:pos + l].decode('latin1'))
            pos += l
    except Exception:
        ok = False
    if not ok:
        return None
    ids2 = set()
    list1 = set()
    names = set()
    ncomp = 0
    unknown = set()
    spans_ok = 0
    for ri in range(nrec):
        ro = offs[ri]
        if ro + 8 > len(d):
            return None
        m = struct.unpack_from('>i', d, ro + 4)[0]
        p = ro + 8 + 4 * m
        if p + 6 > len(d):
            return None
        n = struct.unpack_from('>H', d, p)[0]
        nameidx = struct.unpack_from('>I', d, p + 2)[0]
        if nameidx < nstr:
            names.add(strings[nameidx])
        for ci in range(n):
            cid = struct.unpack_from('>I', d, p + 6 + 6 * ci)[0]
            ids2.add(cid)
            ncomp += 1
            if cid not in CASE_IDS:
                unknown.add(cid)
        for k in range(m):
            list1.add(struct.unpack_from('>I', d, ro + 8 + 4 * k)[0])
    return {'label': label, 'magic': magic[:4], 'nrec': nrec, 'nstr': nstr,
            'ncomp': ncomp, 'distinct_id2': len(ids2), 'unknown_id2': len(unknown),
            'id2_list': sorted(hex(v) for v in ids2),
            'unknown_list': sorted(hex(v) for v in unknown),
            'distinct_list1': len(list1), 'names_sample': sorted(names)[:8],
            'names_all_count': len(names)}

results = []
for n in names:
    with z.open(n) as f:
        head = f.read(4)
    if head not in (b'IDCT', b'OG\x00\x03', b'OG\x03'):
        continue
    d = z.read(n)
    r = parse_gol(d, n)
    if r:
        results.append(r)
        print(f"{n}: nrec {r['nrec']} nstr {r['nstr']} comps {r['ncomp']} "
              f"distinct id2 {r['distinct_id2']} UNKNOWN {r['unknown_id2']} list1 {r['distinct_list1']}")

print(f"\n{len(results)} gol streams found in .gla members")

# Also: the level .gla files may contain the gol as an INTERNAL member (gla archive format).
# gla archive: header + member table. Check the gla_scan tooling knowledge:
# read first 64 bytes of each .gla to see if it's an archive with member names
for n in names[:3]:
    d = z.read(n)[:64]
    print(f"\n{n} first 64 B: {d[:48].hex()}")

json.dump(results, open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_gol_streams.json', 'w'), indent=1)
