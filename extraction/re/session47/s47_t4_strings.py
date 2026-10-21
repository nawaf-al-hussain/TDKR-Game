#!/usr/bin/env python3
"""s47 T4: are any lvc STRING tokens non-ASCII? (s46's value digest encoded
strings as latin1 on both sides.) Collect all STR tokens from the three
largest lvc levels via lvc_pure, count bytes >= 0x80, test UTF-8 validity,
and record the engine-faithful decoding (Lua strings / file names are byte
strings -> latin1/bytes preserves them; UTF-8-replacement would corrupt
arbitrary bytes)."""
import sys, struct, json, hashlib
sys.path.insert(0, '/tmp/my-project/work/TDKR-Game/extraction/re/session26')
import lvc_pure

GLA = '/tmp/my-project/raw/com.gameloft.android.AMAZ.GloftKRAS/files/data/game_config.gla'
TAB = '/tmp/my-project/work/re29/lvc_readseq_s30.json'
GOL = '/tmp/my-project/work/TDKR-Game/extraction/re/session26/lvc_gol_templates.json'

g = open(GLA, 'rb').read()
_, idxsz, tabsz, n = struct.unpack('>IIII', g[:16])
pool = g[16 + n * 16:idxsz]
lvcs = []
for i in range(n):
    o, s, no, _ = struct.unpack('>IIII', g[16 + i * 16:16 + i * 16 + 16])
    nm = pool[no:pool.index(b'\0', no)].decode('ascii', 'replace')
    if nm.endswith('.lvc'):
        lvcs.append((nm, o, s))
lvcs.sort(key=lambda t: -t[2])
table = json.load(open(TAB))
templates = json.load(open(GOL))

out = {}
for (nm, o, s) in lvcs[:3]:
    data = g[o:o + s]
    tmp = f'/tmp/my-project/scripts_t4_{nm}.lvc'
    open(tmp, 'wb').write(data)
    tokens = []
    lvc_pure.parse(tmp, table, templates, tokens, None)
    strs = []
    for (kind, off, size, val) in tokens:
        if kind == 'STR':
            if isinstance(val, str):
                strs.append(val)
            elif isinstance(val, (bytes, bytearray)):
                strs.append(val.decode('latin1'))
    hi = [t for t in strs if any(ord(c) > 127 for c in t)]
    utf8_ok = 0
    for t in strs:
        try:
            t.encode('latin1').decode('utf-8')
            utf8_ok += 1
        except UnicodeDecodeError:
            pass
    h = hashlib.sha256()
    for t in sorted(strs):
        h.update(t.encode('latin1'))
        h.update(b'\n')
    out[nm] = {'strings': len(strs), 'with_high_bytes': len(hi),
               'samples_high': hi[:6], 'valid_utf8_when_latin1_bytes': utf8_ok,
               'latin1_sorted_digest': h.hexdigest()}
    print(nm, 'strings:', len(strs), 'with high bytes:', len(hi),
          '| high-byte samples:', hi[:4], '| latin1-bytes valid utf8:',
          utf8_ok, '| digest', out[nm]['latin1_sorted_digest'][:16])

json.dump(out, open('/tmp/my-project/work/TDKR-Game/extraction/re/session47/s47_t4_strings.json', 'w'), indent=1)
print('saved s47_t4_strings.json')
