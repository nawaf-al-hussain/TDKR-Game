#!/usr/bin/env python3
"""s43 T1g: game_config.gla analysis — which script FILES read MC_MAX_DISTANCE,
any dynamic global-assignment patterns (rawset/_G[..]=), and the chunk inventory."""
import re, struct, collections, zlib

P = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/game_config.gla'
raw = open(P, 'rb').read()
print('size', len(raw), 'head', raw[:16].hex())

# is it a GLA container? (big-endian: u32 tag, indexSize, tableBytes, numEntries)
tag, idxsz, tabsz, nent = struct.unpack_from('>4I', raw, 0)
print(f'BE header: tag=0x{tag:x} idxSz={idxsz} tabSz={tabsz} nEntries={nent}')
if 0 < nent < 100000 and tabsz == (nent + 1) * 16:
    ents = []
    for i in range(nent):
        o, s, no, _ = struct.unpack_from('>4I', raw, 16 + i * 16)
        ents.append((o, s, no))
    # name pool
    pool_start = 16 + nent * 16
    names = []
    for i in range(nent):
        no = ents[i][2]
        e = raw.find(b'\0', pool_start + no)
        names.append(raw[pool_start + no:e].decode('ascii', 'replace'))
    print('GLA container OK:', nent, 'entries; first names:', names[:8])
else:
    # maybe little-endian
    tag, idxsz, tabsz, nent = struct.unpack_from('<4I', raw, 0)
    print(f'LE header: tag=0x{tag:x} idxSz={idxsz} tabSz={tabsz} nEntries={nent}')
    ents = None
    names = None

MEMBERS = []
if ents:
    for i, (o, s, no) in enumerate(ents):
        if s > 0 and o + s <= len(raw):
            MEMBERS.append((names[i], o, s))
else:
    # fallback: treat as raw source blob; find chunk boundaries by lua comments
    MEMBERS.append(('<whole>', 0, len(raw)))

print('members:', len(MEMBERS))

read_re = re.compile(rb'MC_MAX_DISTANCE')
write_re = re.compile(rb'MC_MAX_DISTANCE\s*=')
dyn_re = re.compile(rb'rawset\s*\(|_G\s*\[\s*["\']MC_|setfenv|loadstring\s*\(')
hits_read = collections.Counter()
hits_write = collections.Counter()
dyn_hits = collections.Counter()
total_reads = 0
for (nm, o, s) in MEMBERS:
    blob = raw[o:o + s]
    n = len(read_re.findall(blob))
    w = len(write_re.findall(blob))
    d = len(dyn_re.findall(blob))
    if n:
        hits_read[nm] += n
        total_reads += n
    if w:
        hits_write[nm] += w
    if d:
        dyn_hits[nm] += d

print(f'\nMC_MAX_DISTANCE reads: total {total_reads} across {len(hits_read)} member files')
for nm, c in hits_read.most_common(15):
    print(f'  {c:5d}  {nm}')
print('\nwrites:', dict(hits_write) if hits_write else 'NONE')
print('\ndynamic-assignment pattern hits (rawset/_G[/setfenv/loadstring):')
for nm, c in dyn_hits.most_common(10):
    print(f'  {c:5d}  {nm}')

# context sample: first 3 arithmetic uses
m = raw.find(b'5 * MC_MAX_DISTANCE')
if m < 0:
    m = raw.find(b'MC_MAX_DISTANCE')
print('\nsample context:')
print(raw[max(0, m - 120):m + 120].decode('ascii', 'replace'))
