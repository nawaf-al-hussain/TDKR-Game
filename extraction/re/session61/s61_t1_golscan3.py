#!/usr/bin/env python3
"""S61 T1 step 13: find ALL gol-structured streams (DICT ... 'GO\\0' ver3) across:
- every member of every .gla archive
- the extracted .lvc files
Census each: nrec, distinct id2, unknown count."""
import zipfile, struct, json, os, glob

ZIP = '/tmp/my-project/raw/TDKR_v1.1.6b_APK_OBB.zip'
z = zipfile.ZipFile(ZIP)
names = [n for n in z.namelist() if n.endswith('.gla')]

cases = json.load(open('/tmp/my-project/work/TDKR-Game/extraction/re/session60/s60_gct_cases.json'))
CASE_IDS = set(int(k, 0) for k in cases)

def gol_probe(d):
    """Is d a gol stream? Engine: DICT magic, then tableOff u32, 'GO\\0', ver u8=3 (or bare GO+3)."""
    if len(d) < 24:
        return None
    if d[0:4] == b'DICT':
        to = struct.unpack_from('>I', d, 4)[0]
        if d[9:11] == b'GO' and struct.unpack_from('>H', d, 11)[0] == 3:
            return ('dict', to)
    elif d[0:2] == b'GO' and struct.unpack_from('>H', d, 2)[0] == 3:
        return ('bare', None)
    return None

def parse_gol(d, hdr):
    kind, to = hdr
    base = 13 if kind == 'dict' else 5
    nrec = struct.unpack_from('>I', d, base)[0]
    if nrec <= 0 or nrec > 200000 or base + 4 + 4 * nrec > len(d):
        return None
    offs = [struct.unpack_from('>I', d, base + 4 + 4 * i)[0] for i in range(nrec)]
    if any(o >= len(d) for o in offs):
        return None
    pos = to
    nstr = struct.unpack_from('>i', d, pos)[0]
    pos += 4
    if nstr < 0 or nstr > 300000 or pos + 4 * nstr > len(d):
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
    unknown = set()
    ncomp = 0
    names = set()
    refs = 0
    for ri in range(nrec):
        ro = offs[ri]
        if ro + 8 > len(d):
            return None
        m = struct.unpack_from('>i', d, ro + 4)[0]
        if m < 0 or m > 4096:
            return None
        refs += m
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
    return {'nrec': nrec, 'nstr': nstr, 'ncomp': ncomp, 'refs': refs,
            'distinct_id2': len(ids2), 'unknown': len(unknown),
            'unknown_list': sorted(hex(v) for v in unknown)[:14],
            'names_count': len(names), 'names': sorted(names)[:6]}

def check(label, d, src):
    h = gol_probe(d)
    if not h:
        return
    r = parse_gol(d, h)
    if r:
        print(f"\n*** GOL {label} [{src}] kind {h[0]} size {len(d):,}")
        print(f"    nrec {r['nrec']} nstr {r['nstr']} comps {r['ncomp']} refs {r['refs']} "
              f"distinct id2 {r['distinct_id2']} UNKNOWN {r['unknown']}")
        print(f"    names({r['names_count']}): {r['names']}")
        print(f"    unknown: {r['unknown_list']}")
        return r
    else:
        print(f"? gol-header but parse failed: {label} [{src}]")

# 1) all .gla members
for n in names:
    d = z.read(n)
    entries = None
    try:
        tag, indexSize, tableBytes, numEntries = struct.unpack_from('>4I', d, 0)
        if numEntries and tableBytes == (numEntries + 1) * 16:
            entries = []
            for i in range(numEntries):
                off, sz, nameOff, pad = struct.unpack_from('>4I', d, 16 + i * 16)
                e = 16 + tableBytes + nameOff
                e2 = d.find(b'\x00', e)
                nm = d[e:e2].decode('latin1') if e2 > e else f'@{e}'
                if 0 < sz <= len(d) - off:
                    entries.append((off, sz, nm))
    except Exception:
        pass
    if not entries:
        continue
    for off, sz, nm in entries:
        if sz < 24 or sz > 30_000_000:
            continue
        try:
            sub = d[off:off + sz]
        except Exception:
            continue
        check(f"{n.split('/')[-1]}::{nm}", sub, 'gla-member')

# 2) extracted lvc files
for p in sorted(glob.glob('/home/z/my-project/work/data/*.lvc')):
    d = open(p, 'rb').read()
    check(os.path.basename(p), d, 'lvc')
