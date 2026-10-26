#!/usr/bin/env python3
"""S61 T1 step 9b: parse every .gla ARCHIVE (BE, entries+name pool), find members whose
content matches the gol magic (IDCT / OG+ver3), parse them with the engine layout,
census comp ids vs the GCT 65-case set."""
import zipfile, struct, json

ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
PREFIX = 'com.gameloft.android.AMAZ.GloftKRAS/files/'

z = zipfile.ZipFile(ZIP)
names = [n for n in z.namelist() if n.endswith('.gla')]

cases = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session60/s60_gct_cases.json'))
cases['0x222567e3'] = {}
CASE_IDS = set(int(k, 0) for k in cases)

def parse_archive(d):
    if len(d) < 16:
        return None
    tag, indexSize, tableBytes, numEntries = struct.unpack_from('>4I', d, 0)
    if numEntries == 0 or numEntries > 100000:
        return None
    if tableBytes != (numEntries + 1) * 16:
        return None
    entries = []
    for i in range(numEntries):
        off, sz, nameOff, pad = struct.unpack_from('>4I', d, 16 + i * 16)
        end = 16 + tableBytes + nameOff
        e = d.index(b'\x00', end)
        nm = d[end:e].decode('latin1')
        entries.append((off, sz, nm))
    return entries

def parse_gol(d):
    if len(d) < 21:
        return None
    magic = d[0:4]
    if magic == b'IDCT':
        pass
    elif magic[0:1] == b'O' and magic[1:2] == b'G' and struct.unpack_from('>H', d, 2)[0] == 3:
        pass
    else:
        return None
    try:
        tableOff = struct.unpack_from('>I', d, 4)[0]
        nrec = struct.unpack_from('>I', d, 13)[0]
        if nrec <= 0 or nrec > 200000 or tableOff >= len(d):
            return None
        offs = [struct.unpack_from('>I', d, 17 + 4 * i)[0] for i in range(nrec)]
        if any(o >= len(d) for o in offs):
            return None
        pos = tableOff
        nstr = struct.unpack_from('>i', d, pos)[0]
        pos += 4
        if nstr < 0 or nstr > 200000:
            return None
        strings = []
        for i in range(nstr):
            l = struct.unpack_from('>i', d, pos)[0]
            pos += 4
            if l < 0 or pos + l > len(d):
                return None
            strings.append(d[pos:pos + l].decode('latin1'))
            pos += l
        ids2 = set()
        list1 = set()
        names = set()
        ncomp = 0
        unknown = set()
        for ri in range(nrec):
            ro = offs[ri]
            if ro + 8 > len(d):
                return None
            m = struct.unpack_from('>i', d, ro + 4)[0]
            if m < 0 or m > 1000:
                return None
            p = ro + 8 + 4 * m
            if p + 6 > len(d):
                return None
            n = struct.unpack_from('>H', d, p)[0]
            if p + 6 + 6 * n > len(d):
                return None
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
        return {'nrec': nrec, 'nstr': nstr, 'ncomp': ncomp, 'distinct_id2': len(ids2),
                'unknown_id2': len(unknown), 'id2': sorted(hex(v) for v in ids2),
                'unknown': sorted(hex(v) for v in unknown), 'list1': len(list1),
                'names_count': len(names), 'names': sorted(names)}
    except Exception:
        return None

found = []
for n in names:
    d = z.read(n)
    entries = parse_archive(d)
    if not entries:
        print(f"{n}: NOT a parseable archive")
        continue
    for off, sz, nm in entries:
        if off + sz > len(d) or sz < 21 or sz > 20_000_000:
            continue
        g = parse_gol(d[off:off + sz])
        if g:
            g['archive'] = n
            g['member'] = nm
            g['size'] = sz
            found.append(g)
            print(f"\n*** GOL: {n} :: {nm} ({sz} B)")
            print(f"    nrec {g['nrec']} nstr {g['nstr']} comps {g['ncomp']} distinct id2 {g['distinct_id2']} UNKNOWN {g['unknown_id2']} list1 {g['list1']} names {g['names_count']}")
            print(f"    names sample: {g['names'][:6]}")
            print(f"    unknown ids: {g['unknown'][:12]}")

print(f"\nTOTAL gol streams found: {len(found)}")
json.dump(found, open('/tmp/my-project/work/TDKR-Game/extraction/re/session61/s61_t1_gol_members.json', 'w'), indent=1)
