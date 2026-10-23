#!/usr/bin/env python3
"""s55 T3: CComponentGrapplingGun::Load decode + payload extraction + Enemy_Grapnel_Target census.

(1) ARM disasm of CComponentGrapplingGun::Load @0x3bb510 (bound 0x3bb6ac) — count
    ReadInt/ReadFloat/ReadString calls in order -> field layout.
(2) Locate the 'Glider' (0x2674) and 'Glider_Plunge' (0x4c741) gol template payloads;
    the grappling-gun component block precedes the glide block (s54); parse it with the
    Load layout and print values; ALSO parse the glide block as a sanity check
    (must reproduce s54's 4,16,14,...,-45,...,600).
(3) Enemy_Grapnel_Target template 0xaae6a: existence in gol templates, instance count
    in all lvc files (pure parser), references in scripts (game_config.gla Lua).
    Null: same census for a shuffled/wrong template id (expect ~0).
"""
import struct, subprocess, bisect, importlib.util, os, sys, re, json

SO = '/tmp/my-project/work/re29/libKRHP.so'
data = open(SO, 'rb').read()

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

syms = []
for line in subprocess.run(['nm', SO], capture_output=True, text=True).stdout.splitlines():
    p = line.split()
    if len(p) == 3 and not p[2].startswith('$'):
        try:
            syms.append((int(p[0], 16), p[2]))
        except ValueError:
            pass
syms.sort()
addrs = [a for a, _ in syms]
def sym_of(v):
    i = bisect.bisect_right(addrs, v) - 1
    return syms[i][1] if i >= 0 else '<none>'

print('=== (1) CComponentGrapplingGun::Load @0x3bb510 ===')
lo, hi = 0x3bb510, 0x3bb6ac
calls = []
for ins in md.disasm(data[lo:lo + (hi - lo)], lo):
    note = ''
    if ins.mnemonic in ('bl', 'blx'):
        try:
            t = int(ins.op_str.replace('#', ''), 16)
            note = '-> ' + sym_of(t)
            calls.append((hex(ins.address), note))
        except ValueError:
            pass
    print('%08x %-8s %-32s %s' % (ins.address, ins.mnemonic, ins.op_str, note))
from collections import Counter
cc = Counter(c[1] for c in calls)
print('\ncall census:', dict(cc))

print('\n=== (2) Glider template payload re-parse ===')
GOL = '/tmp/my-project/work/data/gol.bin'
d = open(GOL, 'rb').read()
assert d[:4] == b'DICT'
table_off = struct.unpack_from('>I', d, 4)[0]
nrec = struct.unpack_from('>I', d, 13)[0]
offs = [struct.unpack_from('>I', d, 17 + 4 * i)[0] for i in range(nrec)]
pos = table_off
nstr = struct.unpack_from('>i', d, pos)[0]; pos += 4
strings = []
for _ in range(nstr):
    l = struct.unpack_from('>i', d, pos)[0]; pos += 4
    strings.append(d[pos:pos + l].decode('utf-8', 'replace')); pos += l
print('nrec=%d nstr=%d' % (nrec, nstr))
# walk records; find Glider 0x2674 / Glider_Plunge 0x4c741 / 0xaae6a
found = {}
for ri in range(nrec):
    ro = offs[ri]
    oid = struct.unpack_from('>I', d, ro)[0]
    m = struct.unpack_from('>I', d, ro + 4)[0]
    nxt = offs[ri + 1] if ri + 1 < nrec else len(d)
    nameidx = None
    p = ro + 8 + 4 * m
    n = struct.unpack_from('>H', d, p)[0]
    # nameIdx is u32 right after n
    nameidx = struct.unpack_from('>I', d, p + 1)[0] if False else None
    try:
        nm = strings[struct.unpack_from('>I', d, p + 1)[0]] if len(strings) else '?'
    except Exception:
        nm = '?'
    if oid in (0x2674, 0x4c741, 0xaae6a) or 'Glider' in nm or 'Grapnel_Target' in nm or 'aae6a' in nm.lower():
        # dump comp list + template payload
        q = p + 5 + 6 * n
        comps = []
        for ci in range(n):
            ct, fw = struct.unpack_from('>IH', d, p + 5 + 6 * ci)
            comps.append((hex(ct), fw))
        payload = d[q:nxt]
        found[hex(oid)] = {'name': nm, 'm': m, 'comps': comps, 'payload_len': len(payload),
                           'payload_hex_head': payload[:64].hex(),
                           'payload_f32': [round(v, 4) for v in struct.unpack_from('<%df' % min(32, len(payload) // 4), payload)] if len(payload) >= 4 else []}
print(json.dumps(found, indent=1)[:3000])
json.dump(found, open('/tmp/my-project/work/TDKR-Game/extraction/re/session55/s55_t3_glider_payloads.json', 'w'), indent=1)
