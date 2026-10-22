#!/usr/bin/env python3
"""s49 T1d: CWeatherManager ctor / SetLevelProperties / SetFog* static read."""
import json, struct
import capstone
sy = json.load(open('/tmp/my-project/work/so_syms.json'))
by_name = sy['by_name']
d = open('/tmp/my-project/work/re29/libKRHP.so', 'rb').read()

# ELF vaddr->offset
e_shoff, = struct.unpack_from('<I', d, 0x20)
e_shentsize, e_shnum = struct.unpack_from('<HH', d, 0x2e)
secs = []
for i in range(e_shnum):
    o = e_shoff + i * e_shentsize
    _, typ, _, addr, off, size = struct.unpack_from('<IIIIII', d, o)
    secs.append((addr, off, size, typ))
def v2o(v):
    for addr, off, size, typ in secs:
        if typ and addr and addr <= v < addr + size:
            return off + (v - addr)
    return None

md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_THUMB)
md.detail = False

def disasm(name, maxins=260):
    s = by_name.get(name)
    if not s:
        print('missing', name); return
    v = int(s, 16) if isinstance(s, str) else int(s['addr'], 16)
    o = v2o(v & ~1)
    code = d[o:o + maxins * 4]
    out = []
    for ins in md.disasm(code, v & ~1):
        out.append(f'{ins.address:#x}  {ins.mnemonic} {ins.op_str}')
        if len(out) >= maxins: break
    return out

for fn in ['_ZN15CWeatherManagerC2EP24CTemplateLevelProperties',
           '_ZN15CWeatherManager18SetLevelPropertiesEP24CTemplateLevelProperties',
           '_ZN15CWeatherManager11SetFogColorERKN6glitch4core8vector4dIfEE',
           '_ZN15CWeatherManager14SetFogDistanceEff',
           '_ZN15CWeatherManager4InitEv',
           '_ZN15CWeatherManager5ResetEv']:
    print('='*20, fn)
    for l in (disasm(fn) or [])[:120]:
        print(l)
